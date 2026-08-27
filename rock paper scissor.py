import tkinter as tk
from PIL import Image, ImageTk
import math
from random import randint

root = tk.Tk()
root.title("Rock Paper Scissors Shoot")
root.geometry("800x600")
root.resizable(False, False)

BG_COLOR = "#d6eeff"

# ── Frames ──────────────────────────────────────────────
home_frame   = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
setup_frame  = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
game_frame   = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
result_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)

for frame in (home_frame, setup_frame, game_frame, result_frame):
    frame.place(x=0, y=0, width=800, height=600)

def show_frame(frame):
    frame.tkraise()

# ── Image loader ─────────────────────────────────────────
def load_img(path, size):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(img)

options_img  = load_img("options.png",  (100, 100))
exit_img     = load_img("exit.png",     (100, 100))
title1_img   = load_img("rps.png",      (500, 100))
title2_img   = load_img("shoot.png",    (400,  80))
play_img     = load_img("play.png",     (220, 168))
rock_img     = load_img("rock.png",     (105, 105))
paper_img    = load_img("paper.png",    ( 90,  90))
scissors_img = load_img("scissors.png", (105, 105))

# ── Home screen ──────────────────────────────────────────
options_btn = tk.Label(home_frame, image=options_img, bg=BG_COLOR)
options_btn.image = options_img
options_btn.place(x=5, y=5)

exit_btn = tk.Label(home_frame, image=exit_img, bg=BG_COLOR)
exit_btn.image = exit_img
exit_btn.place(x=695, y=5)
exit_btn.bind("<Button-1>", lambda e: root.destroy())

title1 = tk.Label(home_frame, image=title1_img, bg=BG_COLOR)
title1.image = title1_img
title1.place(x=150, y=130)

title2 = tk.Label(home_frame, image=title2_img, bg=BG_COLOR)
title2.image = title2_img
title2.place(x=200, y=235)

play_btn = tk.Label(home_frame, image=play_img, bg=BG_COLOR)
play_btn.image = play_img
play_btn.place(x=290, y=345)
play_btn.bind("<Button-1>", lambda e: show_frame(setup_frame))

icons = {}

rock_left = tk.Label(home_frame, image=rock_img, bg=BG_COLOR)
rock_left.image = rock_img
rock_left.place(x=28, y=130)
icons["rock_L"] = (rock_left, 130)

paper_left = tk.Label(home_frame, image=paper_img, bg=BG_COLOR)
paper_left.image = paper_img
paper_left.place(x=12, y=310)
icons["paper_L"] = (paper_left, 310)

scissors_left = tk.Label(home_frame, image=scissors_img, bg=BG_COLOR)
scissors_left.image = scissors_img
scissors_left.place(x=50, y=465)
icons["scissors_L"] = (scissors_left, 465)

rock_right = tk.Label(home_frame, image=rock_img, bg=BG_COLOR)
rock_right.image = rock_img
rock_right.place(x=610, y=110)
icons["rock_R"] = (rock_right, 110)

paper_right = tk.Label(home_frame, image=paper_img, bg=BG_COLOR)
paper_right.image = paper_img
paper_right.place(x=688, y=300)
icons["paper_R"] = (paper_right, 300)

scissors_right = tk.Label(home_frame, image=scissors_img, bg=BG_COLOR)
scissors_right.image = scissors_img
scissors_right.place(x=648, y=460)
icons["scissors_R"] = (scissors_right, 460)

# ── Floating animation ───────────────────────────────────
FLOAT_AMP   = 10
FLOAT_SPEED = 0.05
TICK_MS     = 30

phases = {
    "rock_L":     0.0,
    "paper_L":    1.1,
    "scissors_L": 2.3,
    "rock_R":     0.7,
    "paper_R":    1.8,
    "scissors_R": 3.0,
}

angles = dict(phases)

def animate():
    for key, (widget, base_y) in icons.items():
        angles[key] += FLOAT_SPEED
        offset = int(FLOAT_AMP * math.sin(angles[key]))
        widget.place_configure(y=base_y + offset)
    root.after(TICK_MS, animate)

animate()

# ── Setup screen (placeholder) ───────────────────────────
tk.Label(setup_frame, text="Setup Screen — coming soon",
         bg=BG_COLOR, font=("Arial", 24)).place(x=200, y=250)
tk.Label(setup_frame, text="← Back", bg=BG_COLOR,
         font=("Arial", 14), cursor="hand2").place(x=20, y=20)

# ── Game screen (placeholder) ────────────────────────────
tk.Label(game_frame, text="Game Screen — coming soon",
         bg=BG_COLOR, font=("Arial", 24)).place(x=200, y=250)

# ── Result screen (placeholder) ──────────────────────────
tk.Label(result_frame, text="Result Screen — coming soon",
         bg=BG_COLOR, font=("Arial", 24)).place(x=200, y=250)

# ── Game logic ───────────────────────────────────────────
def valid_choice(mot):
    return mot in ["rock", "paper", "scissors"]

def random_choice():
    choice = randint(1, 3)
    if choice == 1:
        return "rock"
    elif choice == 2:
        return "paper"
    else:
        return "scissors"

def get_winner(choice1, choice2):
    if choice1 == choice2:
        return 0
    elif (
        (choice1 == "rock" and choice2 == "scissors") or
        (choice1 == "paper" and choice2 == "rock") or
        (choice1 == "scissors" and choice2 == "paper")
    ):
        return 1
    else:
        return 2

# ── Start ─────────────────────────────────────────────────
show_frame(home_frame)
root.mainloop()