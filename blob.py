# === File: blob.py ===
# Defines the Blob class, representing an individual entity
from strategy import STRATEGY_CLASSES

# Counter to track IDs per color
from collections import defaultdict

color_counters = defaultdict(int)

class Blob:
    def __init__(self, color, strategy_name):
        self.color = color
        self.strategy_key = strategy_name
        StrategyClass = STRATEGY_CLASSES[strategy_name]
        self.strategy = StrategyClass()
        self.history = []
        self.id = f"{self.color}{color_counters[self.color]:02d}"
        color_counters[self.color] += 1

    def choose(self, opponent_color, opponent_history):
        choice, reason = self.strategy.choose(opponent_color, opponent_history)
        print(f"{self.id} ({self.strategy_key}) chooses {choice} by {reason}")
        self.history.append((choice, reason))
        return choice

    def reproduce(self):
        return Blob(self.color, self.strategy_key)