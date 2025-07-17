from game_logic import Game, Player, PlayerId, StrategyProfile, Action, Rewards
def main():
    player_cooperate = Player(name = 'player_cooperate', player_id = 0, strategy_profile = StrategyProfile.ALWAYS_COOPERATE)
    player_defect = Player(name = 'player_defect', player_id = 0, strategy_profile = StrategyProfile.ALWAYS_DEFECT)

    rewards = Rewards(AA = {PlayerId.PLAYER_ONE: 10, PlayerId.PLAYER_TWO: 10},
                      AB = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3},
                      BB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 0},)
    g = Game(rewards, player_cooperate, player_defect)
    g.run_game(steps = 5)
    print(g)

if __name__ == "__main__":
    main()