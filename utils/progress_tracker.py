import json
import os

FILE = "data/progress.json"

def save_progress(exercise, reps, accuracy):
    data = []

    # LOAD SAFELY
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
            data = []  # FIX corrupted file

    # APPEND NEW DATA
    data.append({
        "exercise": exercise,
        "reps": reps,
        "accuracy": accuracy
    })

    # SAVE SAFELY
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)