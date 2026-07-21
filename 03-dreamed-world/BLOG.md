---
title: "AI Agents That Live Inside a Dreamed-Up World"
subtitle: "An agent watches a game, learns to hallucinate the next frame, then plays inside its own dream — but only the model that knows players react to each other stays true."
slug: agents-in-a-dreamed-world
canonical: https://dev.to/shridhar_shah2297/ai-agents-that-live-inside-a-dreamed-up-world-3n4j
tags: artificial-intelligence, machine-learning, llm, python
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/secret-lives-of-agents@main/assets/covers/cover-03.png
seoTitle: "AI Agents That Live Inside a Dreamed-Up World"
seoDescription: "An agent learns a world model from game footage and dreams 15 frames ahead. Only the multiplayer model that captures reactions stays true. A tiny, runnable demo."
---

**TL;DR:** The hottest idea in agents right now: don't feed them the real world — let them
**dream** it. An agent watches some footage, learns to hallucinate the next frame, and
practices inside its own head. I built a tiny one, and found the catch: a dream only stays
true if it knows the players **react to each other.** Runs on a laptop.

---

## The world

Two players in an 11-cell corridor: a predator steps toward the prey, the prey steps away.
Every move is a *reaction*. An agent watches random games, then closes its eyes and **dreams
15 frames ahead**, feeding each prediction back in as the next input. I built two dreamers
from the exact same footage:

- **single-player** — predicts each player from its own position alone
- **multiplayer** — predicts both positions *together*

Training an agent inside its own learned dream goes back to Ha & Schmidhuber's
[*World Models*](https://arxiv.org/abs/1803.10122) (2018); the open frontier is making that
dream **multiplayer** — modeling agents *reacting to each other*, not just physics.

## The 10-second version

% of the dream still matching reality, this many frames ahead:

| frames ahead | 1 | 3 | 5 | 10 | 15 |
|---|---|---|---|---|---|
| single-player dream | 11 | 0 | 0 | 9 | 0 |
| **multiplayer dream** | **100** | **100** | **100** | **100** | **100** |

The single-player dream falls apart almost immediately; the multiplayer one stays locked to
reality. That gap is the whole point — and, as we'll see, it comes down to what each model is
even *able* to represent.

## How it works

```python
real = dream = start
for _ in range(15):
    real  = real_next(*real)   # what actually happens
    dream = model(*dream)      # feed the dream its OWN last frame
    match += (dream == real)
```

Same footage, same loop. The only difference: whether the model predicts the two players
**jointly** or independently.

## Why single-player collapses

The prey moves *because* the predator moved. A single-player model looks at each player in
isolation, so it structurally **can't represent that reaction** — its errors compound each
frame until the dream is fiction. The multiplayer model conditions on both, so it captures the
coupling. To be fair, this isn't a surprising empirical result so much as a demonstration:
the corridor is deterministic, so the outcome really follows from what each model is *allowed
to see*. That's exactly why the framing matters.

> A dream you can act in is a superpower — an agent can practice a thousand risky moves for
> free. But a dream that forgets everyone else reacts to you isn't practice. It's a delusion.

## Why it's exciting

**The proven part:** training agents inside a learned dream works — from
[*World Models*](https://arxiv.org/abs/1803.10122) (2018) to [DreamerV3](https://arxiv.org/abs/2301.04104)
(2023) mastering 150+ tasks, and [Genie](https://arxiv.org/abs/2402.15391) (2024) learning
playable worlds from video alone. Dreamed worlds let agents rehearse infinitely, safely, at
zero real-world cost.

**Where it's heading:** those dreams are mostly single-agent today. The 2026 push is
**multiplayer** — worlds where agents model each other. The lesson from this demo is the whole
ballgame: model the reactions or the dream drifts. Get it right and agents can plan *against
each other* entirely in imagination.

## How faithful is this?

A real world model learns from raw pixels with a neural net, in a noisy, stochastic world.
This is that mechanism stripped to its core — a frequency table over a tiny, deterministic
game. It's built to make the intuition concrete, not to reproduce the papers; those (linked
below) do the heavy, learned version.

## Try it

```bash
git clone https://github.com/Shridhar-2205/secret-lives-of-agents
cd secret-lives-of-agents/03-dreamed-world && python demo.py
```

## The series — *The Secret Lives of AI Agents*

1. [Agents invent their own language](https://dev.to/shridhar_shah2297/i-watched-two-ai-agents-invent-their-own-language-51n2)
2. [Agents build a culture on a decaying notepad](https://dev.to/shridhar_shah2297/i-gave-3-ai-agents-a-decaying-notepad-and-they-built-a-culture-1n3n)
3. **Agents that live inside dreamed-up worlds** (you're here)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco.
[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Sources & further reading:**
> Ha & Schmidhuber, [*World Models*](https://arxiv.org/abs/1803.10122) (2018) — the "train inside a dream" idea ·
> Hafner et al., [*Mastering Diverse Domains through World Models*](https://arxiv.org/abs/2301.04104) (DreamerV3, 2023) ·
> Bruce et al., [*Genie: Generative Interactive Environments*](https://arxiv.org/abs/2402.15391) (2024).
