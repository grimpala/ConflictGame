from game_logic import Game, Player, PlayerId, StrategyProfile, Action, Rewards
import random
import itertools

STRATEGY_PROFILES = list(StrategyProfile.__members__.values())
GAMES = {
    "PRISONERS_DILEMMA": Rewards(AA = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 5},
                      BA = {PlayerId.PLAYER_ONE: 5, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 1}),
    "HAWK_DOVE": Rewards(AA = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 0},
                      AB = {PlayerId.PLAYER_ONE: 4, PlayerId.PLAYER_TWO: 1},
                      BA = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 4},
                      BB = {PlayerId.PLAYER_ONE: 2, PlayerId.PLAYER_TWO: 2}),
    "COORDINATION": Rewards(AA = {PlayerId.PLAYER_ONE: 4, PlayerId.PLAYER_TWO: 4},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 1},
                      BA = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 1})
}
def print_scores(scores):
    for item in sorted(scores.items(), key=lambda x: x[1]):
        print(item[0].name + ": " + str(item[1]))

def run_tournament(rewards):
    scores = {}

    for player1_strategy, player2_strategy in itertools.product(STRATEGY_PROFILES, STRATEGY_PROFILES):
        player1 = Player(name='player1', player_id=PlayerId.PLAYER_ONE, strategy_profile=player1_strategy)
        player2 = Player(name='player2', player_id=PlayerId.PLAYER_TWO, strategy_profile=player2_strategy)
        g = Game(rewards, player1, player2)
        g.run_game(steps = 10)

        player1_score = scores.get(player1.strategy_profile, 0)
        player2_score = scores.get(player2.strategy_profile, 0)
        scores[player1.strategy_profile] = player1_score + g.history.get_score_at(-1, PlayerId.PLAYER_ONE)
        scores[player2.strategy_profile] = player2_score + g.history.get_score_at(-1, PlayerId.PLAYER_TWO)

    return scores

def main():
    coordination_scores = run_tournament(GAMES["COORDINATION"])
    prisoners_dilemma_scores = run_tournament(GAMES["PRISONERS_DILEMMA"])
    hawk_dove_scores = run_tournament(GAMES["HAWK_DOVE"])

    combined_scores_fn = lambda k: coordination_scores.get(k, 0) + prisoners_dilemma_scores.get(k, 0) + hawk_dove_scores.get(k, 0)
    combined_scores = {k: combined_scores_fn(k) for k in STRATEGY_PROFILES}
    print_scores(combined_scores)
if __name__ == "__main__":
    main()