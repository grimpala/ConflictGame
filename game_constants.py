from game_logic import PlayerId, StrategyProfile, Rewards

STRATEGY_PROFILES = list(StrategyProfile.__members__.values())
GAMES = {
    "PRISONERS_DILEMMA": Rewards(AA = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 5},
                      BA = {PlayerId.PLAYER_ONE: 5, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 1}),
    "HAWK_DOVE": Rewards(AA = {PlayerId.PLAYER_ONE: 2, PlayerId.PLAYER_TWO: 2},
                      AB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 4},
                      BA = {PlayerId.PLAYER_ONE: 4, PlayerId.PLAYER_TWO: 1},
                      BB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 0}),
    "COORDINATION": Rewards(AA = {PlayerId.PLAYER_ONE: 4, PlayerId.PLAYER_TWO: 4},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 1},
                      BA = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 1}),
    "STAG_HUNT": Rewards(AA = {PlayerId.PLAYER_ONE: 4, PlayerId.PLAYER_TWO: 4},
                      AB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 3},
                      BA = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 0},
                      BB = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 3}),
    "SNOWDRIFT": Rewards(AA = {PlayerId.PLAYER_ONE: 2, PlayerId.PLAYER_TWO: 2},
                      AB = {PlayerId.PLAYER_ONE: 1, PlayerId.PLAYER_TWO: 3},
                      BA = {PlayerId.PLAYER_ONE: 3, PlayerId.PLAYER_TWO: 1},
                      BB = {PlayerId.PLAYER_ONE: 0, PlayerId.PLAYER_TWO: 0}),
}