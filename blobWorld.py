# === File: blobWorld.py ===
# Simulates the ecosystem of blobs across days
from blob import Blob
from dataLogger import DataLogger
from config import SIMULATION_DAYS, LOG_FILE, MAX_BLOBS

class BlobWorld:
    def __init__(self, initial_blobs, logger=None):
        self.blobs = initial_blobs
        self.day = 0
        self.logger = logger or DataLogger(LOG_FILE)

    def play_round(self, blob1, blob2):
        c1 = blob1.choose(blob2.color, blob2.history)
        c2 = blob2.choose(blob1.color, blob1.history)
        if c1 == c2:
            result = "draw"
            reward1, reward2 = 0, 0
        elif (c1, c2) in [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")]:
            result = "win"
            reward1, reward2 = 1, -1
            if len(self.blobs) < MAX_BLOBS:
                self.blobs.append(blob1.reproduce())
        else:
            result = "loss"
            reward1, reward2 = -1, 1
            if len(self.blobs) < MAX_BLOBS:
                self.blobs.append(blob2.reproduce())

        if hasattr(blob1.strategy, "update"):
            blob1.strategy.update(c1, reward1)
        if hasattr(blob2.strategy, "update"):
            blob2.strategy.update(c2, reward2)

        self.logger.log(self.day, blob1, blob2, c1, c2, result)

    def simulate(self):
        for day in range(SIMULATION_DAYS):
            self.day = day
            current_blobs = self.blobs[:]
            for i in range(0, len(current_blobs), 2):
                if i+1 < len(current_blobs):
                    self.play_round(current_blobs[i], current_blobs[i+1])
