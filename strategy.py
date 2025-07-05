# === File: strategy.py ===
# Contains blob decision-making strategies
import random
from collections import defaultdict, deque
import torch
import torch.nn as nn
import torch.nn.functional as F

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

# NeuralNet strategy (simple MLP)
class SimpleNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(3 * 5, 16)
        self.fc2 = nn.Linear(16, 3)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        return self.fc2(x)

class NeuralNetStrategy(StrategyBase):
    def __init__(self):
        self.model = SimpleNN()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.CrossEntropyLoss()
        self.history = []

    def encode_history(self, history):
        vec = {"rock": [1, 0, 0], "paper": [0, 1, 0], "scissors": [0, 0, 1]}
        flat = [vec[m] for m in history[-5:]]
        while len(flat) < 5:
            flat.insert(0, [0, 0, 0])
        return torch.tensor([sum(flat, [])], dtype=torch.float32)

    def choose(self, opponent_color, opponent_history):
        recent = [h[0] for h in opponent_history][-5:] if opponent_history else []
        x = self.encode_history(recent)
        with torch.no_grad():
            out = self.model(x)
        pred = torch.argmax(out).item()
        return ["rock", "paper", "scissors"][pred], "mlp prediction"

    def update(self, chosen, reward):
        if not self.history:
            return
        target = torch.tensor([[{"rock": 0, "paper": 1, "scissors": 2}[chosen]]], dtype=torch.long)
        x = self.encode_history(self.history)
        pred = self.model(x)
        loss = self.criterion(pred, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

# LSTM strategy
class LSTMNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(input_size=3, hidden_size=16, batch_first=True)
        self.fc = nn.Linear(16, 3)

    def forward(self, x):
        _, (hn, _) = self.lstm(x)
        return self.fc(hn.squeeze(0))

class LSTMStrategy(StrategyBase):
    def __init__(self):
        self.model = LSTMNet()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        self.criterion = nn.CrossEntropyLoss()

    def encode_sequence(self, history):
        vec = {"rock": [1, 0, 0], "paper": [0, 1, 0], "scissors": [0, 0, 1]}
        seq = [vec[m] for m in history[-5:]]
        while len(seq) < 5:
            seq.insert(0, [0, 0, 0])
        return torch.tensor([seq], dtype=torch.float32)

    def choose(self, opponent_color, opponent_history):
        recent = [h[0] for h in opponent_history][-5:] if opponent_history else []
        x = self.encode_sequence(recent)
        with torch.no_grad():
            out = self.model(x)
        pred = torch.argmax(out).item()
        return ["rock", "paper", "scissors"][pred], "lstm prediction"

    def update(self, chosen, reward):
        pass  # can be trained later using stored data

# mapping for Blob constructor
STRATEGY_CLASSES = {
    'random': RandomStrategy,
    'dominant': DominantStrategy,
    'mirror': MirrorStrategy,
    'rl': ReinforcementLearningStrategy,
    'mlp': NeuralNetStrategy,
    'lstm': LSTMStrategy,
}
