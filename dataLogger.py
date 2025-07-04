# === File: dataLogger.py ===
# Handles logging of match results to a CSV file
import csv

class DataLogger:
    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                "day", "blob1_id", "blob1_color", "blob1_strategy",
                "blob2_id", "blob2_color", "blob2_strategy",
                "blob1_choice", "blob2_choice", "result"
            ])

    def log(self, day, blob1, blob2, choice1, choice2, result):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                day, blob1.id, blob1.color, blob1.strategy_key,
                blob2.id, blob2.color, blob2.strategy_key,
                choice1, choice2, result
            ])
