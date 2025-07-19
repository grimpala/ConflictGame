from game_logic import Game, Player, PlayerId, StrategyProfile, Rewards
import argparse
import random

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
def print_scores(scores):
    for item in sorted(scores.items(), key=lambda x: x[1]):
        print(item[0].name + ": " + str(item[1]))

# Basically mergesort -- runs a tournament on half1 and on half2, then competes the winners.
def run_elimination_tournament_round(participants, p_random_action, rewards, tournament_steps, depth=0, print_tree=False):
    participants_half1 = participants[:len(participants)//2]
    participants_half2 = participants[len(participants)//2:]
    if len(participants_half1) == 0 and len(participants_half2) == 1:
        if print_tree:
            print(str(depth) + "\t"*depth + participants_half2[0].name)
        return participants_half2[0]

    winner_half1 = run_elimination_tournament_round(participants_half1, p_random_action, rewards, depth + 1)
    winner_half2 = run_elimination_tournament_round(participants_half2, p_random_action, rewards, depth + 1)
    g = Game(rewards, winner_half1, winner_half2)
    g.run_game(steps = tournament_steps, p_random_action = p_random_action)
    winner_half1_score = g.history.get_score_at(-1, PlayerId.PLAYER_ONE)
    winner_half2_score = g.history.get_score_at(-1, PlayerId.PLAYER_TWO)
    if winner_half1_score > winner_half2_score:
        if print_tree:
            print("\t"*depth + winner_half1.name)
        return winner_half1
    else:
        if print_tree:
            print("\t"*depth + winner_half2.name)
        return winner_half2

def run_elimination_tournament(rewards, p_random_action, num_tournament_nodes, tournament_steps):
    scores = {}
    num_strategy_profiles = len(STRATEGY_PROFILES)
    tournament_participants = []
    for idx in range(num_tournament_nodes // num_strategy_profiles):
        for strategy_idx in range(num_strategy_profiles):
            player = Player(name = f"{STRATEGY_PROFILES[strategy_idx]}_{strategy_idx}",
                            strategy_profile=STRATEGY_PROFILES[strategy_idx])
            tournament_participants.append(player)
    return run_elimination_tournament_round(tournament_participants, p_random_action, rewards, tournament_steps).strategy_profile.name

def run_round_robin_tournament(rewards, p_random_action, tournament_steps):
    scores = {strategy: 0 for strategy in STRATEGY_PROFILES}
    matchups = [(s1, s2) for i, s1 in enumerate(STRATEGY_PROFILES)
                          for j, s2 in enumerate(STRATEGY_PROFILES) if i <= j]
    match_counts = {strategy: 0 for strategy in STRATEGY_PROFILES}

    for strat1, strat2 in matchups:
        p1 = Player(name=str(strat1), strategy_profile=strat1)
        p2 = Player(name=str(strat2), strategy_profile=strat2)
        game = Game(rewards, p1, p2)
        game.run_game(steps=tournament_steps, p_random_action=p_random_action)
        scores[strat1] += game.history.get_score_at(-1, PlayerId.PLAYER_ONE)
        scores[strat2] += game.history.get_score_at(-1, PlayerId.PLAYER_TWO)
        match_counts[strat1] += 1
        match_counts[strat2] += 1

    for strat in scores:
        if match_counts[strat] > 0:
            scores[strat] /= match_counts[strat]

    return scores

def main():
    parser = argparse.ArgumentParser(
        description = "Simulator of various game theory strategies.",
        formatter_class = argparse.RawDescriptionHelpFormatter,
        epilog = """
            Examples:
              # Basic simulation of 10 tournaments with 64 players (uniformly chosen) and 1% chance random action.
              python main.py --p_random_action 0.02 --num_tournament_nodes 64 --num_tournaments 10 --game_type COORDINATION
                """
    )
    parser.add_argument('--p_random_action', type=float, default=0.0,)
    parser.add_argument('--num_tournament_nodes', type=int, default=64,)
    parser.add_argument('--num_tournaments', type=int, default=10,)
    parser.add_argument('--tournament_steps', type=int, default=10)
    parser.add_argument('--game_type', type=str, default="PRISONERS_DILEMMA")
    args = parser.parse_args()

    game_rewards = GAMES[args.game_type]

    scores = run_round_robin_tournament(game_rewards,
                                        p_random_action = args.p_random_action,
                                        tournament_steps = args.tournament_steps)

    print(f"Average scores per strategy in {args.game_type} with random action probability {args.p_random_action}:")
    for strat, score in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"{strat.name}: {score:.2f}")
if __name__ == "__main__":
    main()