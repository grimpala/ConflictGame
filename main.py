from game_logic import Game, Player, PlayerId, StrategyProfile, Rewards
import argparse
import random

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

# Basically mergesort -- runs a tournament on half1 and on half2, then competes the winners.
def run_tournament_round(participants, p_random_action, rewards, depth=0, print_tree=False):
    participants_half1 = participants[:len(participants)//2]
    participants_half2 = participants[len(participants)//2:]
    if len(participants_half1) == 0 and len(participants_half2) == 1:
        if print_tree:
            print(str(depth) + "\t"*depth + participants_half2[0].name)
        return participants_half2[0]

    winner_half1 = run_tournament_round(participants_half1, p_random_action, rewards, depth + 1)
    winner_half2 = run_tournament_round(participants_half2, p_random_action, rewards, depth + 1)
    g = Game(rewards, winner_half1, winner_half1)
    g.run_game(steps=10, p_random_action=p_random_action)
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

def run_tournament(rewards, p_random_action, num_tournament_nodes):
    scores = {}
    num_strategy_profiles = len(STRATEGY_PROFILES)
    tournament_participants = []
    for idx in range(num_tournament_nodes // num_strategy_profiles):
        for strategy_idx in range(num_strategy_profiles):
            player = Player(name = f"{STRATEGY_PROFILES[strategy_idx]}_{strategy_idx}",
                            strategy_profile=STRATEGY_PROFILES[strategy_idx])
            tournament_participants.append(player)
    return run_tournament_round(tournament_participants, p_random_action, rewards).strategy_profile.name

def run_repeated_tournaments(rewards, num_tournaments, p_random_action, num_tournament_nodes):
    winners = []
    for _ in range(num_tournaments):
        winners.append(run_tournament(rewards, p_random_action, num_tournament_nodes))
    return winners

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
    parser.add_argument('--game_type', type=str, default="PRISONERS_DILEMMA")
    args = parser.parse_args()

    game_rewards = GAMES[args.game_type]

    winners = run_repeated_tournaments(game_rewards,
                                       num_tournaments = args.num_tournaments,
                                       p_random_action = args.p_random_action,
                                       num_tournament_nodes = args.num_tournament_nodes)

    print(f"Among {len(winners)} tournaments in game {args.game_type} with {args.num_tournament_nodes} participants and random action probability {args.p_random_action}:")
    for winner in set(winners):
        print(f"{winner} won {100 * winners.count(winner)/len(winners)}% of the time.")
    print(f"The overall winner is {max(winners, key = lambda w: winners.count(w))}")
if __name__ == "__main__":
    main()