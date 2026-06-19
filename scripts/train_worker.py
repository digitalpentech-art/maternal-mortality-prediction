import os
import subprocess
import time

def run_training_job():
    print("Starting background training job...")
    try:
        # Assuming training takes some time, run it in a subprocess
        subprocess.run(["python", "scripts/train_models.py"], check=True)
        print("Training completed successfully.")
    except Exception as e:
        print(f"Training failed: {e}")

if __name__ == "__main__":
    # In a real scenario, this could be triggered by a timer or a webhook
    # For now, it's a simple script that can be executed as a background worker
    run_training_job()
