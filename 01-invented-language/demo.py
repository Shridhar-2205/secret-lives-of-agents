"""
Agents Invent Their Own Language (a Lewis signaling game).

A sender sees a secret object and sends a meaningless symbol; a receiver guesses the object.
On a correct guess, both strengthen that object<->symbol habit. That's the only feedback.
They converge on a shared code (~97%). Reseed -> a different code. No memory -> never sets.
Pure standard library; runs in under a second.
"""

import random

OBJECTS = ["apple", "banana", "cherry", "grape", "lemon"]
SYMBOLS = ["\u25c7", "\u25b3", "\u25cb", "\u2606", "\u25a1"]  # ◇ △ ○ ☆ □


class Agent:
    """Habit tallies: object->symbol and symbol->object, reinforced by what works."""

    def __init__(self, seed):
        self.rng = random.Random(seed)
        self.wins = 0
        self.o2s = {o: dict.fromkeys(SYMBOLS, 0.0) for o in OBJECTS}
        self.s2o = {s: dict.fromkeys(OBJECTS, 0.0) for s in SYMBOLS}

    def _pick(self, habits):
        explore = max(0.02, 0.4 / (1 + 0.05 * self.wins))  # explore early, exploit later
        if self.rng.random() < explore:
            return self.rng.choice(list(habits))
        best = max(habits.values())
        return self.rng.choice([k for k, v in habits.items() if v == best])

    def say(self, obj):
        return self._pick(self.o2s[obj])

    def guess(self, sym):
        return self._pick(self.s2o[sym])

    def reward(self, obj, sym):
        self.o2s[obj][sym] += 1
        self.s2o[sym][obj] += 1
        self.wins += 1


class Goldfish(Agent):
    """Same game, but only recalls the last few rounds — so no code ever sets."""

    def __init__(self, seed, window=6):
        super().__init__(seed)
        self.window, self.recent = window, []

    def say(self, obj):
        hits = [s for o, s in self.recent if o == obj]
        return max(set(hits), key=hits.count) if hits else self.rng.choice(SYMBOLS)

    def guess(self, sym):
        hits = [o for o, s in self.recent if s == sym]
        return max(set(hits), key=hits.count) if hits else self.rng.choice(OBJECTS)

    def reward(self, obj, sym):
        self.recent = (self.recent + [(obj, sym)])[-self.window:]


def play(sender, receiver, rounds, seed):
    """Run the game; return accuracy over the last 200 rounds at a few checkpoints."""
    rng, window, curve = random.Random(seed), [], {}
    for r in range(1, rounds + 1):
        obj = rng.choice(OBJECTS)
        sym = sender.say(obj)
        won = receiver.guess(sym) == obj
        if won:
            sender.reward(obj, sym)
            receiver.reward(obj, sym)
        window = (window + [won])[-200:]
        if r in (1, 200, 500, 1000, 2000):
            curve[r] = sum(window) / len(window)
    return curve


def code(agent):
    return {o: max(agent.o2s[o], key=agent.o2s[o].get) for o in OBJECTS}


def main():
    print("\nAgents Invent Their Own Language")
    print(f"  {len(OBJECTS)} objects, {len(SYMBOLS)} meaningless symbols. Blind guess = {1/len(OBJECTS):.0%}.\n")

    a, b = Agent(11), Agent(12)
    for r, acc in play(a, b, 2000, seed=1).items():
        bar = "\u2588" * int(acc * 30)
        print(f"    round {r:>4}: {acc:>4.0%}  {bar}")

    print("\n  The code they agreed on:      ", " ".join(f'{o}={s}' for o, s in code(a).items()))
    c, d = Agent(241), Agent(242)
    play(c, d, 2000, seed=24)
    print("  Reseed -> a DIFFERENT code:   ", " ".join(f'{o}={s}' for o, s in code(c).items()))

    g = play(Goldfish(31), Goldfish(32), 2000, seed=3)
    print(f"\n  Without memory: {g[2000]:.0%} — stuck near chance; no shared code ever forms.\n")


if __name__ == "__main__":
    main()
