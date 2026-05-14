import tkinter as tk
from PIL import Image, ImageTk
from dashboard.dashboard import Dashboard


class LoginPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Smart Workout AI")

        # FULLSCREEN
        self.root.attributes('-fullscreen', True)

        # EXIT ON ESC
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        # -------- BACKGROUND IMAGE (FIXED) --------
        self.bg_image = Image.open("assets/fitness_bg.png")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.bg_image = self.bg_image.resize((screen_w, screen_h))
        self.bg = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")

        # -------- DARK OVERLAY (IMPORTANT) --------
        self.canvas.create_rectangle(
            0, 0, screen_w, screen_h,
            fill="black", stipple="gray25"
        )

        # -------- LOGIN CARD --------
        frame = tk.Frame(self.root, bg="#121212", padx=40, pady=30)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame,
                 text="Smart Workout AI",
                 font=("Segoe UI", 22, "bold"),
                 fg="white", bg="#121212").pack(pady=10)

        self.username = tk.Entry(frame,
                                 font=("Segoe UI", 12),
                                 bg="#2a2a2a",
                                 fg="white",
                                 insertbackground="white",
                                 relief="flat")
        self.username.pack(pady=10, fill="x")

        self.password = tk.Entry(frame,
                                 show="*",
                                 font=("Segoe UI", 12),
                                 bg="#2a2a2a",
                                 fg="white",
                                 insertbackground="white",
                                 relief="flat")
        self.password.pack(pady=10, fill="x")

        tk.Button(frame,
                  text="Login",
                  command=self.login,
                  bg="#00c853",
                  fg="white",
                  font=("Segoe UI", 12, "bold"),
                  relief="flat",
                  padx=20, pady=8).pack(pady=15)

        # EXIT BUTTON
        tk.Button(self.root,
                  text="Exit",
                  command=self.root.destroy,
                  bg="red",
                  fg="white").place(x=20, y=20)

    def login(self):
        if self.username.get() and self.password.get():
            self.root.destroy()
            Dashboard().run()

    def run(self):
        self.root.mainloop()