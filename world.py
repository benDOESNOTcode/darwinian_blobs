# === File: world.py ===
# Entry point to run the blob simulation
from blobWorld import BlobWorld
from blob import Blob
from dataLogger import DataLogger
from config import STRATEGIES, LOG_FILE

if __name__ == "__main__":
    # Initialize four blobs with different strategies
    blobs = [
        Blob(color="red", strategy_name="dominant"),
        #Blob(color="blue", strategy_name="random"),
        Blob(color="green", strategy_name="mirror"),
        Blob(color="purple", strategy_name="rl"),
        Blob(color="orange", strategy_name="mlp"),
        Blob(color="black", strategy_name="lstm"),

    ]
    logger = DataLogger(LOG_FILE)
    world = BlobWorld(initial_blobs=blobs, logger=logger)
    world.simulate()
    print(f"Simulation complete. Results logged to {LOG_FILE}")
