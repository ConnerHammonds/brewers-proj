from itertools import product
from math import comb

GAMES_IN_SEASON = 162
SD_VS_ARI_GAMES = 3
P_ARI_BEATS_SD = 0.6

# Listed in tiebreaker order
STANDINGS = {
    "CHC": (83, 67),
    "PHI": (83, 67),
    "SD": (81, 68),
    "ARI": (79, 71),
}


def win_distribution(games, p_win):
    return {wins: comb(games, wins) * p_win**wins * (1 - p_win) ** (games - wins) for wins in range(games + 1)}


games_left = {team: GAMES_IN_SEASON - wins - losses for team, (wins, losses) in STANDINGS.items()}

chc_wins = win_distribution(games_left["CHC"], 0.5)
phi_wins = win_distribution(games_left["PHI"], 0.5)
sd_wins_vs_others = win_distribution(games_left["SD"] - SD_VS_ARI_GAMES, 0.5)
ari_wins_vs_others = win_distribution(games_left["ARI"] - SD_VS_ARI_GAMES, 0.5)
ari_wins_vs_sd = win_distribution(SD_VS_ARI_GAMES, P_ARI_BEATS_SD)

order_probability = {}
for chc, phi, sd, ari, ari_vs_sd in product(chc_wins, phi_wins, sd_wins_vs_others, ari_wins_vs_others, ari_wins_vs_sd):
    probability = chc_wins[chc] * phi_wins[phi] * sd_wins_vs_others[sd] * ari_wins_vs_others[ari] * ari_wins_vs_sd[ari_vs_sd]

    final_wins = {
        "CHC": STANDINGS["CHC"][0] + chc,
        "PHI": STANDINGS["PHI"][0] + phi,
        "SD": STANDINGS["SD"][0] + sd + SD_VS_ARI_GAMES - ari_vs_sd,
        "ARI": STANDINGS["ARI"][0] + ari + ari_vs_sd,
    }

    # sorted() keeps the original order for tied teams, which applies the tiebreaker
    order = tuple(sorted(STANDINGS, key=lambda team: -final_wins[team]))
    order_probability[order] = order_probability.get(order, 0) + probability

most_likely = sorted(order_probability.items(), key=lambda item: -item[1])
for order, probability in most_likely[:3]:
    print(f"{' > '.join(order)}: {probability:.2%}")
