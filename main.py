from game_logic import Game, Player, PlayerId, StrategyProfile, Action, Rewards
import random
import itertools

strategy_profiles = list(StrategyProfile.__members__.values())

def main():
    scores = {}
    rewards = Rewards(AA = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 5},
                      BA = {PlayerId.PLAYER_ONE: 5, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 1},)

    for player1_strategy, player2_strategy in itertools.product(strategy_profiles, strategy_profiles):
        player1 = Player(name='player1', player_id=PlayerId.PLAYER_ONE, strategy_profile=player1_strategy)
        player2 = Player(name='player2', player_id=PlayerId.PLAYER_TWO, strategy_profile=player2_strategy)
        g = Game(rewards, player1, player2)
        g.run_game(steps = 10)

        player1_score = scores.get(player1.strategy_profile, 0)
        player2_score = scores.get(player2.strategy_profile, 0)
        scores[player1.strategy_profile] = player1_score + g.history.get_score_at(-1, PlayerId.PLAYER_ONE)
        scores[player2.strategy_profile] = player2_score + g.history.get_score_at(-1, PlayerId.PLAYER_TWO)

    for item in sorted(scores.items(), key=lambda x: x[1]):
        print(item[0].name + ": " + str(item[1]))

if __name__ == "__main__":
    main()