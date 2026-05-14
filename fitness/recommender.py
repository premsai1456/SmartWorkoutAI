import tkinter as tk
from PIL import Image, ImageTk

# NEW IMPORT (GRAPH)
from utils.progress_graph import show_progress_graph


class FitnessRecommender:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Fitness AI")

        # FULLSCREEN
        self.root.attributes('-fullscreen', True)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # -------- SCREEN SIZE --------
        self.root.update_idletasks()
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        # -------- BACKGROUND IMAGE --------
        try:
            image = Image.open("assets/fitness_bg.png")
            image = image.resize((self.screen_w, self.screen_h))
            self.bg = ImageTk.PhotoImage(image)
        except:
            self.bg = None

        self.canvas = tk.Canvas(self.root,
                                width=self.screen_w,
                                height=self.screen_h)
        self.canvas.pack(fill="both", expand=True)

        if self.bg:
            self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        # DARK OVERLAY
        self.canvas.create_rectangle(
            0, 0, self.screen_w, self.screen_h,
            fill="black", stipple="gray25"
        )

        # -------- MAIN CARD --------
        self.main_frame = tk.Frame(self.root, bg="#121212", padx=40, pady=30)
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):

        tk.Label(self.main_frame,
                 text="Fitness Planner",
                 font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#121212").pack(pady=10)

        # INPUTS
        self.weight = self.create_input("Weight (kg)")
        self.height = self.create_input("Height (cm)")
        self.age = self.create_input("Age")

        # GOAL
        tk.Label(self.main_frame,
                 text="Select Goal",
                 fg="#bbb", bg="#121212").pack(pady=10)

        self.goal = tk.StringVar(value="Bulking")

        for g in ["Bulking", "Cutting", "Maintenance"]:
            tk.Radiobutton(self.main_frame,
                           text=g,
                           variable=self.goal,
                           value=g,
                           fg="white",
                           bg="#121212",
                           selectcolor="#333").pack(anchor="w")

        # GENERATE BUTTON
        tk.Button(self.main_frame,
                  text="Generate Plan",
                  command=self.generate_plan,
                  bg="#00c853",
                  fg="white",
                  font=("Segoe UI", 12, "bold"),
                  padx=20, pady=10).pack(pady=10)

        # GRAPH BUTTON (NEW FEATURE)
        tk.Button(self.main_frame,
                  text="View Progress Graph",
                  command=show_progress_graph,
                  bg="#2962ff",
                  fg="white",
                  font=("Segoe UI", 11, "bold"),
                  padx=15, pady=8).pack(pady=10)

        # OUTPUT
        self.output = tk.Text(self.main_frame,
                              height=12,
                              width=50,
                              bg="#1e1e1e",
                              fg="white")
        self.output.pack(pady=10)

        # BACK BUTTON
        tk.Button(self.root,
                  text="Back",
                  command=self.go_back,
                  bg="red",
                  fg="white").place(x=20, y=20)

    # ---------------- INPUT FIELD ----------------
    def create_input(self, label):
        tk.Label(self.main_frame,
                 text=label,
                 fg="#bbb",
                 bg="#121212").pack(anchor="w")

        entry = tk.Entry(self.main_frame,
                         bg="#2a2a2a",
                         fg="white",
                         insertbackground="white")
        entry.pack(fill="x", pady=5)

        return entry

    # ---------------- LOGIC ----------------
    def generate_plan(self):
        try:
            weight = float(self.weight.get())
            height = float(self.height.get())
            age = int(self.age.get())
            goal = self.goal.get()

            # -------- BMR --------
            bmr = 10 * weight + 6.25 * height - 5 * age + 5

            # -------- CALORIES --------
            calories = bmr * 1.55

            if goal == "Bulking":
                calories += 300
            elif goal == "Cutting":
                calories -= 300

            # -------- MACROS --------
            protein = weight * 2
            fats = weight * 0.8
            carbs = (calories - (protein * 4 + fats * 9)) / 4

            result = f"""
🔥 Calories: {int(calories)}

🥩 Protein: {int(protein)} g
🥑 Fats: {int(fats)} g
🍚 Carbs: {int(carbs)} g

🎯 Goal: {goal}

💪 Workout Plan:
- 4–5 days/week
- Progressive overload

😴 Sleep:
7–9 hours
"""

            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, result)

        except:
            self.output.delete(1.0, tk.END)
            self.output.insert(tk.END, "⚠ Please enter valid inputs!")

    # ---------------- BACK ----------------
    def go_back(self):
        self.root.destroy()
        from dashboard.dashboard import Dashboard
        Dashboard().run()

    def run(self):
        self.root.mainloop()