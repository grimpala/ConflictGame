from enum import Enum

class StrategyProfile(Enum):
    ALWAYS_COOPERATE = 1
    ALWAYS_DEFECT = 2
    TIT_FOR_TAT = 3

class Action(Enum):
    COOPERATE = 1
    DEFECT = 2

class PlayerId(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class Rewards:
    def __init__(self, AA, AB, BB):
        self.AA = AA
        self.AB = AB
        self.BB = BB
    def player_rewards(self, player1_action, player2_action, player_id):
        if player1_action == Action.COOPERATE and player2_action == Action.COOPERATE:
            return self.AA[player_id]
        elif player1_action != player2_action:
            return self.AB[player_id]
        return self.BB[player_id]

class Player:
    def __init__(self, player_id, name, strategy_profile):
        self.strategy_profile = strategy_profile
        self.player_id = player_id
        self.name = name
    def select_action(self, history):
        if self.strategy_profile == StrategyProfile.ALWAYS_COOPERATE:
            return Action.COOPERATE
        elif self.strategy_profile == StrategyProfile.ALWAYS_DEFECT:
            return Action.DEFECT
        elif self.strategy_profile == StrategyProfile.TIT_FOR_TAT:
            if len(history) == 0:
                return Action.COOPERATE
            opponent_last_action = history[-1][1 - self.player_id]
            return Action.DEFECT if opponent_last_action == Action.DEFECT else Action.COOPERATE
        return Action.COOPERATE

class GameHistory:
    def __init__(self):
        self.history = []
    def append_history(self, player1_reward, player2_reward, player1_action, player2_action):
        prev_score_1, prev_score_2 = 0, 0
        if len(self.history) > 0:
            prev_score_1 += self.get_score_at(-1, PlayerId.PLAYER_ONE)
            prev_score_2 += self.get_score_at(-1, PlayerId.PLAYER_TWO)
        data = {PlayerId.PLAYER_ONE: {
            "reward": player1_reward + prev_score_1,
            "action": player1_action,
        },
        PlayerId.PLAYER_TWO: {
            "reward": player2_reward + prev_score_2,
            "action": player2_action,
        }}
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
    def run_game(self, steps = 1):
        for _ in range(steps):
            player1_action = self.player1.select_action(self.history)
            player2_action = self.player2.select_action(self.history)
            player1_reward = self.rewards.player_rewards(player1_action, player2_action, PlayerId.PLAYER_ONE)
            player2_reward = self.rewards.player_rewards(player1_action, player2_action, PlayerId.PLAYER_TWO)
            self.history.append_history(player1_reward, player2_reward, player1_action, player2_action)
    def get_history(self):
        return self.history
    def __str__(self):
        s = ""
        for idx, history_step in enumerate(self.history.get_raw_history()):
            s += f"t={idx}:\n"
            s += f"\t{self.player1.name}: action: {self.history.get_action_at(idx, PlayerId.PLAYER_ONE)}, score: {self.history.get_score_at(idx, PlayerId.PLAYER_ONE)}"
            s += f"\t{self.player2.name}: action: {self.history.get_action_at(idx, PlayerId.PLAYER_TWO)}, score: {self.history.get_score_at(idx, PlayerId.PLAYER_TWO)}"
            s += "\n"
        return s