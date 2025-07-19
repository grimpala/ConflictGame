from game_logic import Player, PlayerId, Game
from game_constants import STRATEGY_PROFILES

def run_round_robin_tournament(rewards, args):
    scores = {strategy: 0 for strategy in STRATEGY_PROFILES}
    matchups = [(s1, s2) for i, s1 in enumerate(STRATEGY_PROFILES)
                          for j, s2 in enumerate(STRATEGY_PROFILES) if i <= j]
    match_counts = {strategy: 0 for strategy in STRATEGY_PROFILES}

    for strat1, strat2 in matchups:
        p1 = Player(name=str(strat1), strategy_profile=strat1)
        p2 = Player(name=str(strat2), strategy_profile=strat2)
        game = Game(rewards, p1, p2)
        game.run_game(steps = args.tournament_steps, p_random_action = args.p_random_action)
        scores[strat1] += game.history.get_score_at(-1, PlayerId.PLAYER_ONE)
        scores[strat2] += game.history.get_score_at(-1, PlayerId.PLAYER_TWO)
        match_counts[strat1] += 1
        match_counts[strat2] += 1

    for strat in scores:
        if match_counts[strat] > 0:
            scores[strat] /= match_counts[strat]

    return scores
