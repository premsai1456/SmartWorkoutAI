import json
import os
import matplotlib.pyplot as plt

FILE = "data/progress.json"

def show_progress_graph():
    print("DEBUG: Graph function called")  # <-- IMPORTANT

    if not os.path.exists(FILE):
        print("No data found!")
        return

    with open(FILE, "r") as f:
        data = json.load(f)

    if not data:
        print("No progress recorded yet!")
        return

    reps = [d.get("reps", 0) for d in data]
    accuracy = [d.get("accuracy", 0) for d in data]

    sessions = list(range(1, len(data) + 1))

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(sessions, reps, marker='o')
    plt.title("Reps Progress")

    plt.subplot(1, 2, 2)
    plt.plot(sessions, accuracy, marker='o')
    plt.title("Accuracy Progress")

    plt.tight_layout()
    plt.show()