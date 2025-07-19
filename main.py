import argparse

from game_constants import GAMES
from tournament_logic import run_round_robin_tournament

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

    game_rewards = GAMES.get(args.game_type, "PRISONERS_DILEMMA")

    scores = run_round_robin_tournament(game_rewards,args)

    print(f"Average scores per strategy in {args.game_type} with random action probability {args.p_random_action}:")
    for strat, score in sorted(scores.items(), key=lambda x: -x[1]):
        print(f"{strat.name}: {score:.2f}")
if __name__ == "__main__":
    main()