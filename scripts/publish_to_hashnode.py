"""
Publish every <post>/BLOG.md in this repo to Hashnode.

How it works:
  - Reads the YAML front matter (title, slug, tags, subtitle, seoTitle, seoDescription,
    cover, ignorePost) from each `*/BLOG.md`.
  - Publishes a new post, or updates the existing one if a post with the same slug is
    already on the publication (so re-running is safe and idempotent).
  - Skips any post whose front matter has `ignorePost: true` (used for the weekly drip).
  - Only the article body is sent. As a safety net, anything from a "## ... LinkedIn post ..."
    heading onward is stripped (LinkedIn copy lives in POST.md, not in the article).

Secrets / config (provided as environment variables by the GitHub Action):
  - HASHNODE_PAT   (required)  Personal Access Token from https://hashnode.com/settings/developer
  - HASHNODE_HOST  (optional)  Publication host. Defaults to shridhar22.hashnode.dev

This talks to the public Hashnode GraphQL API (https://gql.hashnode.com). No secret is
ever hard-coded; the token is read from the environment only.
"""

import os
import re
import sys
import glob

import requests
import yaml

API = "https://gql.hashnode.com"
HOST = os.environ.get("HASHNODE_HOST", "shridhar22.hashnode.dev")
TOKEN = os.environ.get("HASHNODE_PAT", "").strip()
TIMEOUT = 30

# Pretty names for tag slugs (used only when creating a tag that doesn't exist yet).
TAG_NAMES = {
    "ai": "AI",
    "llm": "LLM",
    "artificial-intelligence": "Artificial Intelligence",
    "machine-learning": "Machine Learning",
    "agents": "AI Agents",
    "programming": "Programming",
    "python": "Python",
    "security": "Security",
}

PUBLISH_MUTATION = """
mutation Publish($input: PublishPostInput!) {
  publishPost(input: $input) { post { id slug url } }
}
"""

UPDATE_MUTATION = """
mutation Update($input: UpdatePostInput!) {
  updatePost(input: $input) { post { id slug url } }
}
"""

PUBLICATION_QUERY = """
query Pub($host: String!) {
  publication(host: $host) {
    id
    posts(first: 50) { edges { node { id slug } } }
  }
}
"""


def gql(query, variables):
    """Run a GraphQL request and return the `data` object, raising on any error."""
    resp = requests.post(
        API,
        json={"query": query, "variables": variables},
        headers={"Authorization": TOKEN, "Content-Type": "application/json"},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("errors"):
        raise RuntimeError(payload["errors"])
    return payload["data"]


def get_publication():
    """Return (publication_id, {slug: post_id}) for the configured host."""
    data = gql(PUBLICATION_QUERY, {"host": HOST})
    pub = data.get("publication")
    if not pub:
        raise SystemExit(f"No Hashnode publication found for host '{HOST}'.")
    existing = {e["node"]["slug"]: e["node"]["id"] for e in pub["posts"]["edges"]}
    return pub["id"], existing


def parse_post(path):
    """Split a BLOG.md into (front_matter_dict, article_markdown)."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    if not text.lstrip().startswith("---"):
        raise ValueError(f"{path}: missing YAML front matter")

    # Front matter is delimited by the first two `---`; the rest is the body
    # (which keeps its own `---` section dividers intact).
    _, fm_raw, body = text.split("---", 2)
    fm = yaml.safe_load(fm_raw) or {}

    for key in ("title", "slug"):
        if not fm.get(key):
            raise ValueError(f"{path}: front matter is missing required '{key}'")

    # Safety net: drop a LinkedIn block (and anything after it) if one ever sneaks back in.
    cut = re.search(r"^##.*LinkedIn post.*$", body, flags=re.MULTILINE)
    if cut:
        body = body[: cut.start()]

    return fm, body.strip()


def build_tags(fm):
    """Turn the comma-separated `tags` front-matter field into Hashnode tag objects."""
    tags = []
    for slug in str(fm.get("tags", "")).split(","):
        slug = slug.strip()
        if slug:
            tags.append({"slug": slug, "name": TAG_NAMES.get(slug, slug.replace("-", " ").title())})
    return tags


def build_input(fm, body):
    """Build the shared post input, omitting any empty fields (never sending null)."""
    data = {
        "title": fm["title"],
        "slug": fm["slug"],
        "contentMarkdown": body,
        "tags": build_tags(fm),
    }

    subtitle = fm.get("subtitle")
    if subtitle:
        data["subtitle"] = subtitle

    cover = fm.get("cover")
    if cover:
        data["coverImageOptions"] = {"coverImageURL": cover}

    meta = {
        "title": fm.get("seoTitle") or fm.get("title"),
        "description": fm.get("seoDescription") or fm.get("subtitle"),
    }
    meta = {k: v for k, v in meta.items() if v}
    if meta:
        data["metaTags"] = meta

    return data


def publish(pub_id, fm, body):
    inp = build_input(fm, body)
    inp["publicationId"] = pub_id
    return gql(PUBLISH_MUTATION, {"input": inp})["publishPost"]["post"]


def update(post_id, fm, body):
    inp = build_input(fm, body)
    inp["id"] = post_id
    return gql(UPDATE_MUTATION, {"input": inp})["updatePost"]["post"]


def main():
    if not TOKEN:
        raise SystemExit("HASHNODE_PAT is not set. Add it as a repository secret.")

    pub_id, existing = get_publication()
    print(f"Publication {HOST} ({pub_id}); {len(existing)} existing posts.\n")

    posts = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "*", "BLOG.md")))
    published = skipped = 0
    for path in posts:
        name = os.path.basename(os.path.dirname(path))
        fm, body = parse_post(path)

        if fm.get("ignorePost") is True:
            print(f"  skip    {name}  (ignorePost: true)")
            skipped += 1
            continue

        slug = fm["slug"]
        if slug in existing:
            post = update(existing[slug], fm, body)
            print(f"  update  {name}  -> {post['url']}")
        else:
            post = publish(pub_id, fm, body)
            print(f"  publish {name}  -> {post['url']}")
        published += 1

    print(f"\nDone. {published} published/updated, {skipped} skipped (ignored).")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # surface a clean message in the Action log
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
