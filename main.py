from game_logic import Game, Player, PlayerId, StrategyProfile, Action, Rewards
import random
def main():
    strategy_profiles = list(StrategyProfile.__members__.values())
    player1_strategy = random.choice(strategy_profiles)
    player2_strategy = random.choice(strategy_profiles)
    player1 = Player(name = 'player1', player_id = PlayerId.PLAYER_ONE, strategy_profile = player1_strategy)
    player2 = Player(name = 'player2', player_id = PlayerId.PLAYER_TWO, strategy_profile = player2_strategy)
    rewards = Rewards(AA = {PlayerId.PLAYER_ONE: 10, PlayerId.PLAYER_TWO: 10},
                      AB = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3},
                      BB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 0},)
    g = Game(rewards, player1, player2)

    g.run_game(steps = 5)
    print(g)

if __name__ == "__main__":
    main()