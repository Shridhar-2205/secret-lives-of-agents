"""
Publish every <post>/BLOG.md in this repo to dev.to (Forem v1 API).

How it works:
  - Reads the YAML front matter (title, slug, tags, subtitle, seoDescription, cover,
    ignorePost) from each `*/BLOG.md`.
  - Creates a new article, or updates the existing one if an article with the same title is
    already on your account (so re-running is safe and idempotent).
  - `ignorePost: true` is published as a dev.to **draft** (published: false) — useful for the
    weekly drip; flip it to false to make the post live.
  - All posts are grouped under the "Secret Lives of AI Agents" series on dev.to.

Secrets / config (provided as environment variables by the GitHub Action):
  - DEVTO_API_KEY  (required)  Generate at https://dev.to/settings/extensions

Docs: https://developers.forem.com/api/v1 . No secret is ever hard-coded; the key is read
from the environment only.
"""

import os
import re
import sys
import glob
import time

import requests
import yaml

API = "https://dev.to/api"
TOKEN = os.environ.get("DEVTO_API_KEY", "").strip()
SERIES = "Secret Lives of AI Agents"
TIMEOUT = 30

# dev.to tags must be lowercase alphanumeric, max 4 per article. Map our front-matter
# slugs to clean dev.to tags; anything unknown is sanitized (non-alphanumeric stripped).
TAG_MAP = {
    "ai": "ai",
    "artificial-intelligence": "ai",
    "machine-learning": "machinelearning",
    "llm": "llm",
    "agents": "agents",
    "programming": "programming",
    "python": "python",
    "security": "security",
}

HEADERS = {
    "api-key": TOKEN,
    "accept": "application/vnd.forem.api-v1+json",
    "content-type": "application/json",
}


def retry_after_seconds(resp):
    """How long to wait after a 429, from the Retry-After header or the error message."""
    header = resp.headers.get("Retry-After", "")
    if header.isdigit():
        return int(header) + 2
    match = re.search(r"(\d+)\s*second", resp.text)
    return (int(match.group(1)) + 2) if match else 60


def api(method, path, **kwargs):
    """Call the Forem API and return parsed JSON, retrying on rate limits (429)."""
    for _ in range(10):
        resp = requests.request(method, f"{API}{path}", headers=HEADERS, timeout=TIMEOUT, **kwargs)
        if resp.status_code == 429:
            wait = min(retry_after_seconds(resp), 310)
            print(f"  rate limited — waiting {wait}s before retrying {method} {path} ...")
            time.sleep(wait)
            continue
        if resp.status_code >= 400:
            raise RuntimeError(f"{method} {path} -> {resp.status_code}: {resp.text[:300]}")
        return resp.json() if resp.content else {}
    raise RuntimeError(f"{method} {path}: still rate limited after retries")


def existing_articles():
    """Return {title: id} for all of the authenticated user's articles."""
    found = {}
    page = 1
    while True:
        batch = api("GET", f"/articles/me/all?per_page=100&page={page}")
        if not batch:
            break
        for art in batch:
            found[art["title"]] = art["id"]
        if len(batch) < 100:
            break
        page += 1
    return found


def parse_post(path):
    """Split a BLOG.md into (front_matter_dict, article_markdown)."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    if not text.lstrip().startswith("---"):
        raise ValueError(f"{path}: missing YAML front matter")

    _, fm_raw, body = text.split("---", 2)
    fm = yaml.safe_load(fm_raw) or {}

    if not fm.get("title"):
        raise ValueError(f"{path}: front matter is missing required 'title'")

    # Safety net: drop a LinkedIn block if one ever sneaks back in (it's not part of the article).
    cut = re.search(r"^##.*LinkedIn post.*$", body, flags=re.MULTILINE)
    if cut:
        body = body[: cut.start()]

    return fm, body.strip()


def unwrap_markdown(text):
    """Join hard-wrapped prose into single-line paragraphs.

    dev.to renders every single newline as a <br>, so source files that wrap prose at a fixed
    column look jagged. This reflows paragraphs and blockquotes onto one line while leaving
    code fences, tables, lists, and headings untouched.
    """
    lines = text.split("\n")
    out, prose, quote = [], [], []
    in_code = False

    def flush_prose():
        if prose:
            out.append(" ".join(prose))
            prose.clear()

    def flush_quote():
        if quote:
            out.append("> " + " ".join(quote))
            quote.clear()

    def flush():
        flush_prose()
        flush_quote()

    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            flush()
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        if s == "":
            flush()
            out.append("")
            continue
        # Indented continuation of a wrapped list item / previous block.
        if line[:1] == " " and not re.match(r"^\s*([-*+]\s|\d+\.\s)", line):
            if prose:
                prose.append(s)
            elif quote:
                quote.append(s)
            elif out and out[-1].strip():
                out[-1] = out[-1].rstrip() + " " + s
            else:
                prose.append(s)
            continue
        if s.startswith(">"):
            flush_prose()
            quote.append(s.lstrip(">").strip())
            continue
        flush_quote()
        if re.match(r"^(#{1,6}\s|[-*+]\s|\d+\.\s|\|)", s) or s.startswith("---") or s.startswith("==="):
            flush_prose()
            out.append(line)
            continue
        prose.append(s)

    flush()
    return "\n".join(out)


def build_tags(fm):
    """Up to 4 lowercase-alphanumeric dev.to tags, de-duplicated, order preserved."""
    tags = []
    for raw in str(fm.get("tags", "")).split(","):
        slug = raw.strip().lower()
        if not slug:
            continue
        tag = TAG_MAP.get(slug, re.sub(r"[^a-z0-9]", "", slug))
        if tag and tag not in tags:
            tags.append(tag)
    return tags[:4]


def build_article(fm, body):
    body = unwrap_markdown(body)
    # dev.to has no subtitle field, so surface it as an italic lead line under the title.
    subtitle = fm.get("subtitle")
    if subtitle:
        body = f"*{subtitle}*\n\n{body}"

    article = {
        "title": fm["title"],
        "body_markdown": body,
        "published": fm.get("ignorePost") is not True,
        "series": SERIES,
        "tags": build_tags(fm),
    }
    if fm.get("cover"):
        article["main_image"] = fm["cover"]
    description = fm.get("seoDescription") or subtitle
    if description:
        article["description"] = description
    return {"article": article}


def main():
    if not TOKEN:
        raise SystemExit("DEVTO_API_KEY is not set. Add it as a repository secret.")

    existing = existing_articles()
    print(f"dev.to: {len(existing)} existing articles on your account.\n")

    posts = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "*", "BLOG.md")))
    created = updated = 0
    for path in posts:
        name = os.path.basename(os.path.dirname(path))
        fm, body = parse_post(path)
        payload = build_article(fm, body)

        if fm["title"] in existing:
            art = api("PUT", f"/articles/{existing[fm['title']]}", json=payload)
            print(f"  update  {name}  -> {art.get('url')}")
            updated += 1
        else:
            art = api("POST", "/articles", json=payload)
            state = "published" if payload["article"]["published"] else "draft"
            print(f"  create  {name}  ({state})  -> {art.get('url')}")
            created += 1
            time.sleep(2)  # stay under dev.to's create rate limit

    print(f"\nDone. {created} created, {updated} updated.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # surface a clean message in the Action log
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
