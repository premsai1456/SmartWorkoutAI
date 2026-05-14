import tkinter as tk
from fitness.recommender import FitnessRecommender
import main  # IMPORTANT

class Dashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dashboard")

        # FULLSCREEN
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#121212")

        tk.Label(self.root, text="Dashboard",
                 font=("Segoe UI", 24, "bold"),
                 fg="white", bg="#121212").pack(pady=40)

        tk.Button(self.root,
                  text="Posture Correction",
                  command=self.open_posture,
                  bg="#2962ff", fg="white",
                  width=25, height=2).pack(pady=20)

        tk.Button(self.root,
                  text="Fitness Planner",
                  command=self.open_fitness,
                  bg="#00c853", fg="white",
                  width=25, height=2).pack(pady=20)

        # EXIT
        tk.Button(self.root, text="Exit",
                  command=self.root.destroy,
                  bg="red", fg="white").place(x=20, y=20)

    def open_posture(self):
        self.root.destroy()
        main.main()   # SAME WINDOW EXECUTION

    def open_fitness(self):
        self.root.destroy()
        FitnessRecommender().run()

    def run(self):
        self.root.mainloop()