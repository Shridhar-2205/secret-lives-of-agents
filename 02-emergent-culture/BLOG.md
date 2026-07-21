---
title: "I Gave 3 AI Agents a Decaying Notepad and They Built a Culture"
subtitle: "One shared memory that keeps fading, three minimal agents, no boss — and a story that outlives every note that carried it."
slug: agents-build-a-culture
canonical: https://dev.to/shridhar_shah2297/i-gave-3-ai-agents-a-decaying-notepad-and-they-built-a-culture-1n3n
tags: artificial-intelligence, machine-learning, llm, python
cover: https://cdn.jsdelivr.net/gh/Shridhar-2205/secret-lives-of-agents@main/assets/covers/cover-02.png
seoTitle: "I Gave 3 AI Agents a Decaying Notepad and They Built a Culture"
seoDescription: "Three minimal agents share one decaying notepad and keep a story alive far beyond any single note — a tiny, runnable demo of emergent culture and stigmergy."
---

**TL;DR:** Give a few bare-bones agents nothing but a shared notepad that constantly fades,
and they spontaneously build a **culture** — a story they keep alive together, long after any
single note has decayed to nothing. No coordinator, one tiny rule. Runs on a laptop.

---

## The setup

Three agents share one whiteboard. Every tick, everything on it fades; a note left alone dies
in **~4 ticks**. Each tick an agent scribbles a noisy observation, and a **swarm** agent also
reinforces whatever's currently strongest. That's the whole rule. It's **stigmergy** — how
termites build cathedrals by reacting to each other's mud (Grassé, 1959) — and the same
dynamic that lets populations of agents settle on shared conventions
([Perez et al., 2024](https://arxiv.org/abs/2403.08882)).

## The 10-second version

| | ❌ Each on its own | ✅ The swarm |
|---|---|---|
| A shared story exists | **11%** of ticks | **100%** |
| Same story tick-to-tick | **3%** | **99%** |

## How it works

```python
pad[observation] += 0.3            # everyone adds a little noise
if imitate:                         # the entire "culture" rule:
    leader = strongest(pad)         #   reinforce what the group already backs
    pad[leader] += 1.0
# every note decays each tick
```

## The part that got me

```
Tick 0:   group rallies around  "water down"
Tick 100: group still holds     "water down"
   ...but that original note faded to ~8e-31 within a few ticks.
   It survived only because the agents rewrote it 300 times.
```

The story is 100 ticks old; the note that started it has been gone since tick ~4. What
persists isn't any note — it's the *meaning*, re-inscribed by the group. It's the Ship of
Theseus: no original plank left, yet the ship sails on. Reseed and a different story wins —
the agreement is what's real.

## Why it matters

**The proven part:** stigmergy — coordination through traces left in a shared medium — is old
biology (Grassé, 1959), and populations of LLM agents have already been shown to form and
transmit shared conventions ([Perez et al., 2024](https://arxiv.org/abs/2403.08882)). This
demo distills it to a single rule on a decaying pad.

**Where it's heading:** we keep trying to fix agent memory with bigger storage. This points
the other way — a **group** of forgetful agents in 2026 can hold knowledge no single one
could, just by reminding each other. Persistence becomes a property of the *society*, not the
context window.

> These agents can't remember much alone. Together, on a whiteboard that won't stop erasing
> itself, they keep a story alive as long as they care to. That's culture.

## How faithful is this?

This is stigmergy distilled to one reinforcement rule on a decaying dictionary — not LLM
agents reasoning in language. It shows the *dynamic* (a shared story outliving the notes that
carried it); the cited work studies it with real populations of generative agents.

## Try it

```bash
git clone https://github.com/Shridhar-2205/secret-lives-of-agents
cd secret-lives-of-agents/02-emergent-culture && python demo.py
```

## The series — *The Secret Lives of AI Agents*

1. [Agents invent their own language](https://dev.to/shridhar_shah2297/i-watched-two-ai-agents-invent-their-own-language-51n2)
2. **Agents build a culture on a decaying notepad** (you're here)
3. [Agents that live inside dreamed-up worlds](https://dev.to/shridhar_shah2297/ai-agents-that-live-inside-a-dreamed-up-world-3n4j)

---

**Shridhar Shah** — Senior Software Engineer on the AI team at Cisco.
[GitHub](https://github.com/Shridhar-2205) · [LinkedIn](https://www.linkedin.com/in/shridhar-shah-220b1721b/)

> **Sources & further reading:**
> Stigmergy (Grassé, 1959) — the biology of indirect coordination ·
> Park et al., [*Generative Agents: Interactive Simulacra of Human Behavior*](https://arxiv.org/abs/2304.03442) (2023) ·
> Perez et al., [*Cultural Evolution in Populations of Large Language Models*](https://arxiv.org/abs/2403.08882) (2024).
