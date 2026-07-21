---
title: "I Watched Two AI Agents Invent Their Own Language"
subtitle: "No shared words, no dictionary — just two agents that negotiate a private code from scratch and hit ~97%."
slug: agents-invent-their-own-language
canonical: https://dev.to/shridhar_shah2297/i-watched-two-ai-agents-invent-their-own-language-51n2
tags: artificial-intelligence, machine-learning, llm, python
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/secret-lives-of-agents@main/assets/covers/cover-01.png
seoTitle: "I Watched Two AI Agents Invent Their Own Language"
seoDescription: "Two agents with no shared words play a signaling game and invent a private code from scratch, reaching ~97%. A tiny, runnable demo of emergent communication."
---

**TL;DR:** Give two AI agents a reason to coordinate and they'll make up their own language —
one we never designed. I built the tiniest version: two agents, zero shared words, and from
"did we understand each other?" alone they invent a private code and hit **~97%**. Runs on a
laptop, no API key.

---

## The game

A **sender** sees a secret object (say 🍎) and holds up one of a few random shapes: ◇ △ ○ ☆ □.
A **receiver** sees only the shape and guesses the object. Right guess → both remember that
pairing. No dictionary, no translator. This is the classic **Lewis signaling game** — the
cleanest way to watch language appear from nothing.

## The 10-second version

| | ❌ No memory | ✅ Remembers |
|---|---|---|
| After 2,000 rounds | **~56%** (chance) | **~97%** |
| A language formed? | no | **yes** |

Blind guess = 20%. Watch it crystallize:

```
round    1:   0%
round  500:  94%
round 2000:  97%   apple=◇  banana=□  cherry=△  grape=☆  lemon=○
```

## How it works

Each agent keeps a tally of habits; a win reinforces the pairing on **both** sides:

```python
if receiver.guess(symbol) == obj:   # they understood each other
    sender.reward(obj, symbol)      # both strengthen the SAME link
    receiver.reward(obj, symbol)
```

That's it. Reseed and they invent a *different* code (`apple=☆ …`) — arbitrary, but agreed.
And memory is what makes it stick: agents that only recall the last few rounds stay near
chance — a shared code needs a shared, persistent history. This referential-game setup goes
back to [Lazaridou, Peysakhovich & Baroni (2017)](https://arxiv.org/abs/1612.07182), the first
to show neural agents inventing a working language from scratch.

## Why it's exciting (and a little eerie)

**The proven part:** two neural agents reliably invent a working code from scratch — shown
since [Lazaridou et al. (2017)](https://arxiv.org/abs/1612.07182) and surveyed in
[Lazaridou & Baroni (2020)](https://arxiv.org/abs/2006.02419). This demo just strips the idea
to 100 lines so you can watch it happen.

**Where it's heading:** the systems we're shipping in 2026 are LLM *swarms* that talk to each
other nonstop. A private, compressed code lets them coordinate faster and cheaper than plain
English — a real efficiency win. The flip side: if agents settle on a protocol we didn't
design, we may not be able to **read what they tell each other.**

> A language is just a bet that a symbol means the same thing on both ends. These agents make
> that bet round by round, with nobody refereeing.

## How faithful is this?

This is the classic referential game in ~100 lines — reinforcement over simple habit tables,
not a neural network. It captures the *mechanism* (a shared code emerging from feedback alone);
the papers below scale the same idea to real networks and richer, compositional languages.

## Try it

```bash
git clone https://github.com/Shridhar-2205/secret-lives-of-agents
cd secret-lives-of-agents/01-invented-language && python demo.py
```

## The series — *The Secret Lives of AI Agents*

1. **Agents invent their own language** (you're here)
2. [Agents build a culture on a decaying notepad](https://dev.to/shridhar_shah2297/i-gave-3-ai-agents-a-decaying-notepad-and-they-built-a-culture-1n3n)
3. [Agents that live inside dreamed-up worlds](https://dev.to/shridhar_shah2297/ai-agents-that-live-inside-a-dreamed-up-world-3n4j)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco.
[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Sources & further reading:**
> Lewis, *Convention* (1969) — the original signaling game ·
> Lazaridou, Peysakhovich & Baroni, [*Multi-Agent Cooperation and the Emergence of (Natural) Language*](https://arxiv.org/abs/1612.07182) (ICLR 2017) ·
> Havrylov & Titov, [*Emergence of Language with Multi-agent Games*](https://arxiv.org/abs/1705.11192) (NeurIPS 2017) ·
> Lazaridou & Baroni, [*Emergent Multi-Agent Communication in the Deep Learning Era*](https://arxiv.org/abs/2006.02419) (2020, survey).
