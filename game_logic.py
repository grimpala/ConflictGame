from enum import Enum
import random

class StrategyProfile(Enum):
    RANDOM = 0
    ALWAYS_COOPERATE = 1
    ALWAYS_DEFECT = 2
    TIT_FOR_TAT = 3
    TIT_FOR_TWO_TATS = 4
    GRIM_TRIGGER = 5
    PAVLOV = 6

class Action(Enum):
    COOPERATE = 1
    DEFECT = 2

class PlayerId(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class Rewards:
    def __init__(self, AA, AB, BA, BB):
        self.AA = AA
        self.AB = AB
        self.BA = BA
        self.BB = BB
    def player_rewards(self, player1_action, player2_action, player_id):
        if player1_action == Action.COOPERATE and player2_action == Action.COOPERATE:
            return self.AA[player_id]
        elif player1_action == Action.COOPERATE and player2_action == Action.DEFECT:
            return self.AB[player_id]
        elif player1_action == Action.DEFECT and player2_action == Action.COOPERATE:
            return self.BA[player_id]
        return self.BB[player_id]

class Player:
    def __init__(self, name="", strategy_profile=StrategyProfile.RANDOM):
        self.strategy_profile = strategy_profile
        self.name = name
        self.player_id = None
    def set_player_id(self, player_id):
        self.player_id = player_id
    def select_action(self, history, p_random_action):
        # With probability p_random_action, choose a random action.
        if random.random() < p_random_action:
            return random.choice(list(Action.__members__.values()))
        opponent_player_id = PlayerId.PLAYER_TWO if self.player_id == PlayerId.PLAYER_ONE else PlayerId.PLAYER_ONE

        # Randomly choose an action.
        if self.strategy_profile == StrategyProfile.RANDOM:
            return random.choice(list(Action.__members__.values()))
        # Always cooperate.
        if self.strategy_profile == StrategyProfile.ALWAYS_COOPERATE:
            return Action.COOPERATE
        # Always defect.
        elif self.strategy_profile == StrategyProfile.ALWAYS_DEFECT:
            return Action.DEFECT
        # Cooperate unless the opponent defected last turn.
        elif self.strategy_profile == StrategyProfile.TIT_FOR_TAT:
            if len(history) > 0:
                opponent_last_action = history.get_action_at(-1, opponent_player_id)
                return Action.DEFECT if opponent_last_action == Action.DEFECT else Action.COOPERATE
            return Action.COOPERATE
        # If less than two moves have been played, cooperate. If the opponent has defected twice
        # in a row, defect. Else, cooperate.
        elif self.strategy_profile == StrategyProfile.TIT_FOR_TWO_TATS:
            if len(history) > 1:
                opponent_last_action = history.get_action_at(-1, opponent_player_id)
                opponent_last_last_action = history.get_action_at(-2, opponent_player_id)
                if opponent_last_action == Action.DEFECT and opponent_last_last_action == Action.DEFECT:
                    return Action.DEFECT
                return Action.COOPERATE
            return Action.COOPERATE
        # Cooperates in the first round. Once the opponent defects, will defect forever.
        elif self.strategy_profile == StrategyProfile.GRIM_TRIGGER:
            if len(history) == 0:
                return Action.COOPERATE
            opponent_last_action = history.get_action_at(-1, opponent_player_id)
            self_last_action = history.get_action_at(-1, self.player_id)
            if opponent_last_action == Action.DEFECT or self_last_action == Action.DEFECT:
                return Action.DEFECT
            return Action.COOPERATE
        elif self.strategy_profile == StrategyProfile.PAVLOV:
            if len(history) == 0:
                return Action.COOPERATE
            opponent_last_action = history.get_action_at(-1, opponent_player_id)
            self_last_action = history.get_action_at(-1, self.player_id)
            if opponent_last_action == Action.COOPERATE:
                return self_last_action
            elif opponent_last_action == Action.DEFECT:
                return Action.COOPERATE if self_last_action == Action.DEFECT else Action.DEFECT
            return Action.COOPERATE
        return Action.COOPERATE
class GameHistory:
    def __init__(self):
        self.history = []
    def __len__(self):
        return len(self.history)
    def append_history(self, player1_reward, player2_reward, player1_action, player2_action):
        prev_score_1, prev_score_2 = 0, 0
        if len(self.history) > 0:
            prev_score_1 += self.get_score_at(-1, PlayerId.PLAYER_ONE)
            prev_score_2 += self.get_score_at(-1, PlayerId.PLAYER_TWO)
        data = {
            PlayerId.PLAYER_ONE: {
                "reward": player1_reward + prev_score_1,
                "action": player1_action,
            },
            PlayerId.PLAYER_TWO: {
                "reward": player2_reward + prev_score_2,
                "action": player2_action,
            }
        }
        self.history.append(data)
    def get_raw_history(self):
        return self.history
    def get_history_at(self, idx):
        return self.history[idx]
    def get_score_at(self, idx, player_id):
        return self.history[idx][player_id]["reward"]
    def get_action_at(self, idx, player_id):
        return self.history[idx][player_id]["action"]

class Game:
    def __init__(self, rewards, player1, player2):
        self.rewards = rewards
        self.player1 = player1
        self.player2 = player2
        self.history = GameHistory()

        self.player1.set_player_id(PlayerId.PLAYER_ONE)
        self.player1.set_player_id(PlayerId.PLAYER_TWO)
    def run_game(self, steps = 1, p_random_action = 0):
        for _ in range(steps):
            player1_action = self.player1.select_action(self.history, p_random_action)
            player2_action = self.player2.select_action(self.history, p_random_action)
            player1_reward = self.rewards.player_rewards(player1_action, player2_action, PlayerId.PLAYER_ONE)
            player2_reward = self.rewards.player_rewards(player1_action, player2_action, PlayerId.PLAYER_TWO)
            self.history.append_history(player1_reward, player2_reward, player1_action, player2_action)
    def get_history(self):
        return self.history
    def __str__(self):
        s = "\n" + "="*96 + "\n"
        s += f"PLAYER1_STRATEGY={self.player1.strategy_profile.name}, PLAYER2_STRATEGY={self.player2.strategy_profile.name}\n"
        s += "="*96 + "\n"
        s += "REWARDS:\n"
        s += "\t   COOP \t DEFECT\n"
        s += f"COOP\t | {list(self.rewards.AA.values())} \t| {list(self.rewards.AB.values())} |\n"
        s += f"DEFECT\t | {list(self.rewards.AB.values())} \t| {list(self.rewards.BB.values())} |\n"
        s += "="*96 + "\n"
        for idx, history_step in enumerate(self.history.get_raw_history()):
            s += f"t={idx}:\n"
            s += f"\t{self.player1.name}:\n"
            s += f"\t\taction: {self.history.get_action_at(idx, PlayerId.PLAYER_ONE).name}, score: {self.history.get_score_at(idx, PlayerId.PLAYER_ONE)}\n"
            s += f"\t{self.player2.name}:\n"
            s += f"\t\taction: {self.history.get_action_at(idx, PlayerId.PLAYER_TWO).name}, score: {self.history.get_score_at(idx, PlayerId.PLAYER_TWO)}\n"
        return s