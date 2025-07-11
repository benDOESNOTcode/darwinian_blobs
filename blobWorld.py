# === File: blobWorld.py ===
# Simulates the ecosystem of blobs across days
from blob import Blob
from dataLogger import DataLogger
from config import SIMULATION_DAYS, LOG_FILE, MAX_BLOBS
import random

class BlobWorld:
    def __init__(self, initial_blobs, logger=None):
        self.blobs = initial_blobs
        self.day = 0
        self.logger = logger or DataLogger(LOG_FILE)

    def play_round(self, blob1, blob2):
        if not (blob1.alive and blob2.alive) or blob1.color == blob2.color:
            return

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
            blob2.record_result("loss")
            print(f"{blob1.color} ({blob1.strategy_key}) beats {blob2.color} ({blob2.strategy_key})")
        else:
            result = "loss"
            reward1, reward2 = -1, 1
            if len(self.blobs) < MAX_BLOBS:
                self.blobs.append(blob2.reproduce())
            blob1.record_result("loss")
            print(f"{blob2.color} ({blob2.strategy_key}) beats {blob1.color} ({blob1.strategy_key})")

        if hasattr(blob1.strategy, "update"):
            blob1.strategy.update(c1, reward1)
        if hasattr(blob2.strategy, "update"):
            blob2.strategy.update(c2, reward2)

        self.logger.log(self.day, blob1, blob2, c1, c2, result)

    def simulate(self):
        for day in range(SIMULATION_DAYS):
            self.day = day
            alive_blobs = [b for b in self.blobs if b.alive]
            alive_count = len(alive_blobs)

            remaining_colors = set(b.color for b in alive_blobs)
            if len(remaining_colors) == 1:
                winner_color = remaining_colors.pop()
                winner = next(b for b in alive_blobs if b.color == winner_color)
                print(f"\nAll remaining blobs are {winner_color}. Last color standing: {winner_color} (e.g. blob {winner.id}).")
                return

            if alive_count <= 1:
                if alive_blobs:
                    w = alive_blobs[0]
                    print(f"\nLast blob standing: {w.id} ({w.color}, {w.strategy_key})")
                else:
                    print("\nNo blobs remain.")
                return

            print(f"\n--- Day {day} | Alive blobs: {alive_count} ---")

            # Randomized cross-color pairing
            pool = alive_blobs[:]
            random.shuffle(pool)
            pairs = []
            while len(pool) > 1:
                b1 = pool.pop(0)
                idx = next((i for i, b in enumerate(pool) if b.color != b1.color), None)
                if idx is not None:
                    b2 = pool.pop(idx)
                    pairs.append((b1, b2))
                else:
                    pool.insert(0, b1)
                    break

            if not pairs:
                print(f"\nNo cross-color matches possible on Day {day}. Stopping simulation.")
                break

            for b1, b2 in pairs:
                self.play_round(b1, b2)

        # Final results
        final_alive = [b for b in self.blobs if b.alive]
        print(f"\nSimulation ended after {SIMULATION_DAYS} days with {len(final_alive)} blobs alive.")
        if final_alive:
            print("\nSurviving blobs:")
            for b in final_alive:
                print(f"- {b.id} ({b.color}, {b.strategy_key})")
