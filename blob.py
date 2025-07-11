# === File: blob.py ===
# Defines the Blob class, representing an individual entity
from strategy import STRATEGY_CLASSES
from config import COLORS

# Counter to track IDs per color
from collections import defaultdict

color_counters = defaultdict(int)

def print_final_blob_counts():
    print("Final Blob Counts:")
    for color, count in sorted(color_counters.items()):
        color_code = COLORS.get(color, "")
        reset_code = COLORS["reset"]
        print(f"{color_code}{color}: {count}{reset_code}")

class Blob:
    def __init__(self, color, strategy_name):
        self.color = color
        self.strategy_key = strategy_name
        StrategyClass = STRATEGY_CLASSES[strategy_name]
        self.strategy = StrategyClass()
        self.history = []
        # Track losses and alive status
        self.losses = 0
        self.alive = True
        # Assign readable ID
        self.id = f"{self.color}{color_counters[self.color]:02d}"
        color_counters[self.color] += 1

    def choose(self, opponent_color, opponent_history):
        choice, reason = self.strategy.choose(opponent_color, opponent_history)
        color_code = COLORS.get(self.strategy_key, "")
        reset_code = COLORS["reset"]
        print(f"{color_code}{self.id} ({self.strategy_key}) chooses {choice} by {reason}{reset_code}")
        self.history.append((choice, reason))
        return choice

    def reproduce(self):
        return Blob(self.color, self.strategy_key)

    def record_result(self, result):
        if result == "loss":
            self.losses += 1
            if self.losses >= 4:
                self.alive = False
