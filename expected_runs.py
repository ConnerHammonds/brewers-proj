from itertools import product

P_WALK = 0.15 
P_K = 0.55
P_HR = 0.05
P_FLY = 0.25
P_SCORE_ON_TAG = 0.75


def walk(bases):
    first, second, third = bases
    if not first:
        return (1, second, third), 0
    if not second:
        return (1, 1, third), 0
    if not third:
        return (1, 1, 1), 0
    return (1, 1, 1), 1


# expected[(outs, bases)] = expected runs from this state to the end of the inning
states = [(outs, bases) for outs in range(3) for bases in product([0, 1], repeat=3)]
expected = {state: 0.0 for state in states}


def runs_left(outs, bases):
    return 0.0 if outs >= 3 else expected[(outs, bases)]


# Walks and home runs don't add outs, so states point back at each other.
# Repeating the update until the numbers stop changing solves this exactly.
for _ in range(100):
    for outs, bases in states:
        first, second, third = bases

        walk_bases, walk_runs = walk(bases)
        walk_value = walk_runs + runs_left(outs, walk_bases)

        strikeout_value = runs_left(outs + 1, bases)

        hr_value = 1 + sum(bases) + runs_left(outs, (0, 0, 0))

        # With 2 outs the fly out ends the inning, so there is no tag-up
        if third and outs < 2:
            bases_after_tag = (first, second, 0)
            scores = 1 + runs_left(outs + 1, bases_after_tag)
            thrown_out = runs_left(outs + 2, bases_after_tag)
            fly_value = P_SCORE_ON_TAG * scores + (1 - P_SCORE_ON_TAG) * thrown_out
        else:
            fly_value = runs_left(outs + 1, bases)

        expected[(outs, bases)] = (
            P_WALK * walk_value
            + P_K * strikeout_value
            + P_HR * hr_value
            + P_FLY * fly_value
        )

runs_per_inning = expected[(0, (0, 0, 0))]
print(f"Expected runs per inning: {runs_per_inning:.4f}")
print(f"Expected runs per 9 innings: {9 * runs_per_inning:.4f}")