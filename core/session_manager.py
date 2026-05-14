import sqlite3
import os
import time
from datetime import datetime

class SessionManager:
    """Manages workout sessions, logging to SQLite, and session summaries."""
    def __init__(self, db_path="data/session_logs.db"):
        self.db_path = db_path
        self.start_time = time.time()
        self.session_data = {} # {exercise_name: {"reps": 0, "accuracies": []}}
        self._init_db()

    def _init_db(self):
        """Initializes the database schema and ensures the data directory exists."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS session_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exercise_name TEXT,
                    reps INTEGER,
                    accuracy REAL,
                    timestamp DATETIME
                )
            ''')
            conn.commit()

    def update_session(self, exercise_name, reps, accuracy):
        """Updates the in-memory session data for summary reporting."""
        if exercise_name not in self.session_data:
            self.session_data[exercise_name] = {"reps": 0, "accuracies": []}
        
        # We only update if reps changed or to collect accuracy samples
        self.session_data[exercise_name]["reps"] = reps
        self.session_data[exercise_name]["accuracies"].append(accuracy)

    def log_session_to_db(self, exercise_name, reps, accuracy):
        """Logs a completed set/session segment to the database."""
        if reps == 0:
            return
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO session_logs (exercise_name, reps, accuracy, timestamp) 
                VALUES (?, ?, ?, ?)
            ''', (exercise_name, reps, accuracy, datetime.now()))
            conn.commit()

    def print_summary(self):
        """Prints the final session summary to the console."""
        end_time = time.time()
        duration = int(end_time - self.start_time)
        
        print("\n" + "="*27)
        print("===== SESSION SUMMARY =====")
        
        for exercise, data in self.session_data.items():
            avg_acc = sum(data["accuracies"]) / len(data["accuracies"]) if data["accuracies"] else 0
            print(f"{exercise}: {data['reps']} reps | {avg_acc:.1f}% accuracy")
            # Log final state to DB on exit
            self.log_session_to_db(exercise, data["reps"], avg_acc)
            
        print(f"Duration: {duration} seconds")
        print("="*27 + "\n")
