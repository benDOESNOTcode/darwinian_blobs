# === File: config.py ===
# Stores simulation settings and blob strategy mapping

STRATEGIES = {
    "dominant": "DominantStrategy",
    "random": "RandomStrategy",
    "mirror": "MirrorStrategy",
    "rl": "ReinforcementLearningStrategy",
    "mlp": "NeuralNetStrategy",
    "lstm": "LSTMStrategy",
}

SIMULATION_DAYS = 100
LOG_FILE = "simulation_log.csv"
MAX_BLOBS = 100  # Safety limit to prevent infinite growth

# Terminal colors for blob types
COLORS = {
    "dominant": "\033[91m",  # red
    "random": "\033[94m",    # blue
    "mirror": "\033[92m",    # green
    "rl": "\033[95m",        # purple
    "mlp": "\033[93m",       # orange/yellow
    "lstm": "\033[90m",      # gray/black
    "reset": "\033[0m",      # reset
}
