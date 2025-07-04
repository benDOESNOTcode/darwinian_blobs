# === File: strategy.py ===
# Contains blob decision-making strategies
import random
from collections import defaultdict, deque

class StrategyBase:
    def choose(self, opponent_color, opponent_history):
        raise NotImplementedError

class RandomStrategy(StrategyBase):
    def choose(self, *_):
        return random.choice(["rock", "paper", "scissors"]), "random"

class DominantStrategy(StrategyBase):
    def __init__(self, dominant_choice="rock", bias=0.6):
        self.dominant = dominant_choice
        self.bias = bias

    def choose(self, *_):
        if random.random() < self.bias:
            return self.dominant, "biased"
        alt = random.choice([c for c in ["rock", "paper", "scissors"] if c != self.dominant])
        return alt, "random"

class MirrorStrategy(StrategyBase):
    def __init__(self):
        self.opponent_moves = defaultdict(lambda: deque(maxlen=4))

    def choose(self, opponent_color, opponent_history):
        if opponent_history:
            self.opponent_moves[opponent_color].append(opponent_history[-1][0])
        moves = self.opponent_moves[opponent_color]
        if len(moves) < 2:
            return random.choice(["rock", "paper", "scissors"]), "random (insufficient history)"

        count = {"rock": 0, "paper": 0, "scissors": 0}
        for move in moves:
            count[move] += 1
        most_common = max(count, key=lambda k: count[k])
        if list(count.values()).count(count[most_common]) > 1:
            return random.choice(["rock", "paper", "scissors"]), "random (tie in frequency)"

        if most_common == "rock":
            return "paper", "mirror"
        elif most_common == "paper":
            return "scissors", "mirror"
        else:
            return "rock", "mirror"

class ReinforcementLearningStrategy(StrategyBase):
    def __init__(self):
        self.q_table = {move: 0 for move in ["rock", "paper", "scissors"]}
        self.alpha = 0.1  # learning rate
        self.gamma = 0.9  # discount factor

    def choose(self, opponent_color, opponent_history):
        # Pick the action with highest value or explore
        if random.random() < 0.2:  # epsilon-greedy
            action = random.choice(["rock", "paper", "scissors"])
            return action, "explore"
        action = max(self.q_table, key=self.q_table.get)
        return action, "exploit"

    def update(self, chosen, reward):
        old_value = self.q_table[chosen]
        self.q_table[chosen] = old_value + self.alpha * (reward - old_value)

# mapping for Blob constructor
STRATEGY_CLASSES = {
    'random': RandomStrategy,
    'dominant': DominantStrategy,
    'mirror': MirrorStrategy,
    'rl': ReinforcementLearningStrategy,
}
