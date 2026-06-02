import tkinter as tk
from workout import start_workout
from db import get_leaderboard
from graph import show_graph
from analytics import user_stats
from PIL import Image, ImageTk
import os

def main_ui():

    root = tk.Tk()
    root.geometry("1000x650")
    root.title("AI Gym Trainer")
    root.configure(bg="#0b0b0b")

    BASE_DIR = os.path.dirname(__file__)

    def load_img(path, size=(160,160)):
        img = Image.open(os.path.join(BASE_DIR, path))
        img = img.resize(size)
        return ImageTk.PhotoImage(img)

    user = {}

    # ================= PREMIUM LOGIN =================
    bg_img = load_img("images/bg.jpg", (1000,650))
    bg = tk.Label(root, image=bg_img)
    bg.image = bg_img
    bg.place(x=0, y=0, relwidth=1, relheight=1)

    login_card = tk.Frame(root, bg="#111111", bd=0)
    login_card.place(relx=0.5, rely=0.5, anchor="center")

    name = tk.StringVar()
    password = tk.StringVar()
    weight = tk.StringVar()
    height = tk.StringVar()

    def input_box(parent, label, var):
        tk.Label(parent, text=label,
                 fg="#00ffcc", bg="#111111",
                 font=("Arial",12,"bold")).pack(anchor="w", pady=(5,0))

        tk.Entry(parent, textvariable=var,
                 font=("Arial",12),
                 width=25,
                 bd=0,
                 highlightthickness=2,
                 highlightbackground="#333",
                 highlightcolor="#00ffcc").pack(pady=5)

    tk.Label(login_card,
             text="AI GYM TRAINER",
             fg="white",
             bg="#111111",
             font=("Arial",18,"bold")).pack(pady=10)

    input_box(login_card, "Name", name)
    input_box(login_card, "Password", password)
    input_box(login_card, "Weight", weight)
    input_box(login_card, "Height", height)

    def login():
        if not name.get():
            return

        user["name"] = name.get()
        bg.destroy()
        login_card.destroy()
        dashboard()

    tk.Button(login_card,
              text="START TRAINING",
              command=login,
              bg="#00ffcc",
              fg="black",
              font=("Arial",13,"bold"),
              width=18,
              height=2,
              bd=0).pack(pady=15)

    # ================= DASHBOARD =================
    def dashboard():

        frame = tk.Frame(root, bg="#0b0b0b")
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=f"Welcome {user['name']}",
                 fg="white", bg="#0b0b0b",
                 font=("Arial",16,"bold")).pack(pady=10)

        main = tk.Frame(frame, bg="#0b0b0b")
        main.pack()

        # LEFT (WORKOUT TYPES)
        left = tk.Frame(main, bg="#0b0b0b")
        left.pack(side="left", padx=50)

        upper_img = load_img("images/upper.png")
        lower_img = load_img("images/lower.png")

        def gym_button(parent, img, text, cmd):
            btn = tk.Button(parent,
                            image=img,
                            text=text,
                            compound="top",
                            command=cmd,
                            bg="#1a1a1a",
                            fg="white",
                            font=("Arial",11,"bold"),
                            width=180,
                            height=200,
                            bd=0,
                            activebackground="#00ffcc")
            btn.image = img
            btn.pack(pady=15)

        gym_button(left, upper_img, "Upper Body",
                   lambda: exercises("Upper"))

        gym_button(left, lower_img, "Lower Body",
                   lambda: exercises("Lower"))

        # RIGHT (STATS)
        right = tk.Frame(main, bg="#0b0b0b")
        right.pack(side="right", padx=50)

        tk.Label(right, text="🏆 Leaderboard",
                 fg="#00ffcc", bg="#0b0b0b",
                 font=("Arial",14,"bold")).pack()

        for d in get_leaderboard():
            tk.Label(right,
                     text=f"{d[0]} - {d[1]} reps",
                     fg="white", bg="#0b0b0b").pack()

        tk.Label(right, text="📊 Stats",
                 fg="#00ffcc", bg="#0b0b0b",
                 font=("Arial",14)).pack(pady=10)

        tk.Label(right,
                 text=user_stats(user["name"]),
                 fg="white", bg="#0b0b0b").pack()

        tk.Button(right,
                  text="SHOW GRAPH",
                  command=lambda: show_graph(user["name"]),
                  bg="#00ffcc",
                  fg="black",
                  width=15,
                  height=2,
                  bd=0).pack(pady=10)

    # ================= EXERCISES =================
    def exercises(type):

        win = tk.Toplevel(root)
        win.geometry("500x550")
        win.configure(bg="#0b0b0b")

        if type == "Upper":
            ex = [
                ("Push-up","pushup.png"),
                ("Pull-up","pullup.png"),
                ("Bicep Curl","bicep.png"),
                ("Shoulder Press","shoulder.png")
            ]
        else:
            ex = [
                ("Squat","squat.png"),
                ("Lunges","lunges.png"),
                ("Deadlift","deadlift.png")
            ]

        tk.Label(win, text=f"{type} Workouts",
                 fg="#00ffcc", bg="#0b0b0b",
                 font=("Arial",16,"bold")).pack(pady=10)

        for name_ex, img_file in ex:

            img = load_img(f"images/{img_file}", (120,120))

            btn = tk.Button(win,
                            image=img,
                            text=name_ex,
                            compound="top",
                            command=lambda x=name_ex:
                            start_workout(user["name"], x),
                            bg="#1a1a1a",
                            fg="white",
                            font=("Arial",10,"bold"),
                            bd=0)
            btn.image = img
            btn.pack(pady=10)

    root.mainloop()