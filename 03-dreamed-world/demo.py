"""
Agents in a Dreamed-Up World (a learned world model you can roll out).

Two players share a corridor: a predator steps toward a prey, the prey steps away — so every
move is a reaction to the other. An agent learns the world by watching random games, then
"dreams" 15 frames ahead by feeding its own predictions back in. A single-player model (each
player from its own cell) drifts fast; a multiplayer model (both cells) stays true. Stdlib.
"""

import random

N = 11  # corridor cells 0 .. N-1


def clamp(x):
    return max(0, min(N - 1, x))


def sign(x):
    return (x > 0) - (x < 0)


def real_next(p, q):
    """True rules: predator steps toward prey, prey steps away. Both react to the other."""
    return clamp(p + sign(q - p)), clamp(q - sign(q - p))


def watch(episodes, seed):
    """Learn from footage: two models built from the SAME games."""
    rng = random.Random(seed)
    multi, one_p, one_q = {}, {}, {}
    for _ in range(episodes):
        p, q = rng.randint(0, N - 1), rng.randint(0, N - 1)
        for _ in range(N):
            p2, q2 = real_next(p, q)
            multi.setdefault((p, q), {}).setdefault((p2, q2), 0)
            one_p.setdefault(p, {}).setdefault(p2, 0)
            one_q.setdefault(q, {}).setdefault(q2, 0)
            multi[(p, q)][(p2, q2)] += 1
            one_p[p][p2] += 1
            one_q[q][q2] += 1
            p, q = p2, q2
    return multi, (one_p, one_q)


def top(counts, default):
    return max(counts, key=counts.get) if counts else default


def dream_multi(multi, p, q):
    return top(multi.get((p, q)), (p, q))


def dream_single(models, p, q):
    one_p, one_q = models
    return top(one_p.get(p), p), top(one_q.get(q), q)


def rollout_match(dream, horizon, trials):
    """Dream `horizon` frames ahead from many starts; % still matching reality at each step."""
    match = [0] * horizon
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        p, q = 0, 0
        while p == q:
            p, q = rng.randint(0, N - 1), rng.randint(0, N - 1)
        real = fake = (p, q)
        for h in range(horizon):
            real, fake = real_next(*real), dream(*fake)
            match[h] += (fake == real)
    return [m / trials for m in match]


def main():
    multi, single = watch(episodes=800, seed=0)
    H, trials = 15, 300
    m = rollout_match(lambda p, q: dream_multi(multi, p, q), H, trials)
    s = rollout_match(lambda p, q: dream_single(single, p, q), H, trials)

    print("\nAgents in a Dreamed-Up World — how long does the dream stay true?")
    print(f"  Two players in an {N}-cell corridor; dream {H} frames ahead, feeding it back in.\n")
    cols = (1, 3, 5, 10, 15)
    row = lambda a: "".join(f"{a[h-1]*100:>5.0f}" for h in cols)
    print("   frames ahead        " + "".join(f"{h:>5}" for h in cols))
    print(f"   single-player dream {row(s)}   (% still matching reality)")
    print(f"   multiplayer dream   {row(m)}   (% still matching reality)\n")
    print("  The single-player dream can't see that players react to each other, so it drifts")
    print("  and collapses. The multiplayer dream stays locked to reality the whole rollout.\n")


if __name__ == "__main__":
    main()
