# === File: config.py ===
# Stores simulation settings and blob strategy mapping

STRATEGIES = {
    "dominant": "DominantStrategy",
    "random": "RandomStrategy",
    "mirror": "MirrorStrategy",
    "rl": "ReinforcementLearningStrategy",
}

SIMULATION_DAYS = 100
LOG_FILE = "simulation_log.csv"
MAX_BLOBS = 100  # Safety limit to prevent infinite growth