# 🕵️ The Secret Lives of AI Agents

> Three tiny, runnable demos of what happens when AI agents interact — they invent a language,
> build a culture, and dream up worlds. Each runs on a laptop in seconds. No GPU, no API key,
> pure Python standard library. Grounded in real multi-agent research.

**Repo:** [github.com/Shridhar-2205/secret-lives-of-agents](https://github.com/Shridhar-2205/secret-lives-of-agents) — ⭐ if you like it.

**Topics:** `multi-agent` · `emergent-communication` · `world-models` · `ai-agents` · `python`

## The series

| # | Post | The idea | Grounded in |
|---|------|----------|-------------|
| 1 | [Agents invent their own language](01-invented-language/) | Two agents with no shared words negotiate a private code → **~97%** | Lazaridou et al., *Emergence of (Natural) Language* ([1612.07182](https://arxiv.org/abs/1612.07182)) |
| 2 | [Agents build a culture](02-emergent-culture/) | Forgetful agents keep a story alive on a decaying notepad → present **100%** vs 11% | Perez et al., *Cultural Evolution in Populations of LLMs* ([2403.08882](https://arxiv.org/abs/2403.08882)) |
| 3 | [Agents in a dreamed-up world](03-dreamed-world/) | Only the *multiplayer* world model stays true 15 frames ahead → **100%** vs 0% | Ha & Schmidhuber, *World Models* ([1803.10122](https://arxiv.org/abs/1803.10122)) |

## Run any of them

```bash
cd 01-invented-language && python demo.py
cd 02-emergent-culture  && python demo.py
cd 03-dreamed-world     && python demo.py
```

Each folder has a `README.md`, a small `demo.py`, and a `BLOG.md` write-up. These are POCs:
the *mechanism* is faithful to the paper, the code is kept tiny on purpose.

---

*By **Shridhar Shah**, Senior Software Engineer on the AI team at Cisco.
[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)*
