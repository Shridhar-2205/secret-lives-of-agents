"""
Agents Build a Culture (stigmergy on a decaying notepad).

Three agents share one notepad where every note fades each tick (a note dies in ~4 ticks).
Each tick an agent jots a noisy observation; a "swarm" agent also reinforces whatever is
currently strongest. From that one rule, a shared story emerges and persists the whole run —
kept alive only because the group keeps rewriting it. Pure standard library.
"""

import random

FACTS = ["grubs west", "river north", "cave safe", "fire east",
         "berries up", "water down", "hunt dawn", "storm soon"]
DECAY, FORGET, RESET = 0.5, 0.1, 1.0   # halve each tick; forget if faint; strong rewrite


def horizon():
    t, s = 0, RESET
    while s >= FORGET:
        s *= DECAY
        t += 1
    return t


def run(imitate, ticks, seed):
    rng, pad = random.Random(seed), {}
    first = first_tick = final = None
    rewrites = present = stable = 0
    prev = None

    for t in range(ticks):
        for k in list(pad):                    # everything fades; faint notes are forgotten
            pad[k] *= DECAY
            if pad[k] < FORGET:
                del pad[k]
        for _ in range(3):                     # three agents act
            obs = rng.choice(FACTS)            # a noisy observation, jotted weakly
            pad[obs] = pad.get(obs, 0) + 0.3
            if imitate and pad:                # the whole "culture" rule:
                leader = max(pad, key=pad.get) #   reinforce what the group is rallying around
                pad[leader] = pad.get(leader, 0) + RESET
                rewrites += 1

        top = max(pad, key=pad.get) if pad else None
        share = pad[top] / sum(pad.values()) if pad else 0
        if share > 0.5:                        # a single story dominates the pad
            present += 1
            if first is None:
                first, first_tick = top, t
            stable += (top == prev)
            prev, final = top, top
        else:
            prev = None
    return dict(present=present / ticks, stable=stable / ticks,
                first=first, first_tick=first_tick, final=final, rewrites=rewrites)


def main():
    ticks = 100
    solo = run(imitate=False, ticks=ticks, seed=7)
    swarm = run(imitate=True, ticks=ticks, seed=7)

    print("\nAgents Build a Culture — 3 agents, one decaying notepad, no boss")
    print(f"  A note left untouched dies in ~{horizon()} ticks. This run is {ticks} ticks.\n")
    print(f"   {'':38}{'shared story exists':>20}{'stays the same':>16}")
    print(f"   {'Each agent on its own':38}{solo['present']:>19.0%}{solo['stable']:>16.0%}")
    print(f"   {'The swarm (reinforce shared)':38}{swarm['present']:>19.0%}{swarm['stable']:>16.0%}\n")

    origin = RESET * (DECAY ** (ticks - swarm["first_tick"]))
    print(f"  Tick {swarm['first_tick']}: group rallies around  \"{swarm['first']}\"")
    print(f"  Tick {ticks}: group still holds     \"{swarm['final']}\"")
    print(f"    ...the original note faded to ~{origin:.0e} within a few ticks;")
    print(f"    it survived only because agents rewrote it {swarm['rewrites']} times.")
    other = run(imitate=True, ticks=ticks, seed=13)
    print(f"  Reseed -> a different story wins: \"{other['final']}\". The agreement is what's real.\n")


if __name__ == "__main__":
    main()
