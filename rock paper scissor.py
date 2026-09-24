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

def load_img_bg(path, size, bg):
    img = Image.open(path).convert("RGBA")
    background = Image.new("RGBA", img.size, bg)
    background.paste(img, mask=img.split()[3] if img.mode == "RGBA" else None)
    background = background.resize(size, Image.Resampling.NEAREST)
    return ImageTk.PhotoImage(background)

options_img  = load_img("options.png",  (50, 50))
exit_img     = load_img("exit.png",     (50, 50))
title1_img   = load_img("rps.png",      (500, 100))
title2_img   = load_img("shoot.png",    (400, 80))
play_img     = load_img("play.png",     (220, 168))
rock_img     = load_img("rock.png",     (105, 105))
paper_img    = load_img("paper.png",    (90, 90))
scissors_img = load_img("scissors.png", (105, 105))
pause_img    = load_img_bg("pause.jpg", (50, 50), (214, 238, 255))
home_img     = load_img_bg("home.jpg",  (50, 50), (214, 238, 255))
comp_img     = load_img("comp.jpg",     (180, 115))
next_img     = load_img("next.gif",     (180, 115))
p2_img       = load_img("2p.gif",       (180, 115))

# ═══════════════════════════════════════════════════════════
# HOME SCREEN
# ═══════════════════════════════════════════════════════════
options_btn = tk.Label(home_frame, image=options_img, bg=BG_COLOR)
options_btn.image = options_img
options_btn.place(x=5, y=5)
options_hovering = False

def on_options_enter(e):
    global options_hovering
    if not options_hovering:
        options_hovering = True
        options_btn.place_configure(x=5, y=-5)

def on_options_leave(e):
    global options_hovering
    options_hovering = False
    options_btn.place_configure(x=5, y=5)

options_btn.bind("<Enter>", on_options_enter)
options_btn.bind("<Leave>", on_options_leave)

exit_btn = tk.Label(home_frame, image=exit_img, bg=BG_COLOR)
exit_btn.image = exit_img
exit_btn.place(x=745, y=5)
exit_btn.bind("<Button-1>", lambda e: root.destroy())
exit_hovering = False

def on_exit_enter(e):
    global exit_hovering
    if not exit_hovering:
        exit_hovering = True
        exit_btn.place_configure(y=-5)

def on_exit_leave(e):
    global exit_hovering
    exit_hovering = False
    exit_btn.place_configure(y=5)

exit_btn.bind("<Enter>", on_exit_enter)
exit_btn.bind("<Leave>", on_exit_leave)

title1 = tk.Label(home_frame, image=title1_img, bg=BG_COLOR)
title1.image = title1_img
title1.place(x=150, y=130)

title2 = tk.Label(home_frame, image=title2_img, bg=BG_COLOR)
title2.image = title2_img
title2.place(x=200, y=235)

play_btn = tk.Label(home_frame, image=play_img, bg=BG_COLOR)
play_btn.image = play_img
play_btn.place(x=290, y=345)
hovering = False

def on_enter(e):
    global hovering
    if not hovering:
        hovering = True
        play_btn.place_configure(x=275, y=345, width=270, height=206)

def on_leave(e):
    global hovering
    hovering = False
    play_btn.place_configure(x=290, y=345, width=220, height=168)

play_btn.bind("<Enter>", on_enter)
play_btn.bind("<Leave>", on_leave)
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

# ═══════════════════════════════════════════════════════════
# SETUP SCREEN
# ═══════════════════════════════════════════════════════════
selected_mode = None

pause_btn = tk.Label(setup_frame, image=pause_img, bg=BG_COLOR)
pause_btn.image = pause_img
pause_btn.place(x=5, y=5)

exit_btn2 = tk.Label(setup_frame, image=exit_img, bg=BG_COLOR)
exit_btn2.image = exit_img
exit_btn2.place(x=745, y=5)
exit_btn2.bind("<Button-1>", lambda e: root.destroy())

p2_btn = tk.Label(setup_frame, image=p2_img, bg=BG_COLOR)
p2_btn.image = p2_img
p2_btn.place(x=150, y=250)

comp_btn = tk.Label(setup_frame, image=comp_img, bg=BG_COLOR)
comp_btn.image = comp_img
comp_btn.place(x=470, y=250)

next_btn = tk.Label(setup_frame, image=next_img, bg=BG_COLOR)
next_btn.image = next_img
next_btn.place(x=310, y=420)

def select_mode(mode):
    global selected_mode
    selected_mode = mode
    if mode == "2p":
        p2_btn.place_configure(y=260)
        comp_btn.place_configure(y=250)
    else:
        comp_btn.place_configure(y=260)
        p2_btn.place_configure(y=250)

p2_btn.bind("<Button-1>",   lambda e: select_mode("2p"))
comp_btn.bind("<Button-1>", lambda e: select_mode("comp"))

pause_hovering = False
exit2_hovering = False
comp_hovering  = False
next_hovering  = False
p2_hovering    = False

def on_pause_enter(e):
    global pause_hovering
    if not pause_hovering:
        pause_hovering = True
        pause_btn.place_configure(y=-5)

def on_pause_leave(e):
    global pause_hovering
    pause_hovering = False
    pause_btn.place_configure(y=5)

def on_exit2_enter(e):
    global exit2_hovering
    if not exit2_hovering:
        exit2_hovering = True
        exit_btn2.place_configure(y=-5)

def on_exit2_leave(e):
    global exit2_hovering
    exit2_hovering = False
    exit_btn2.place_configure(y=5)

def on_comp_enter(e):
    global comp_hovering
    if not comp_hovering and selected_mode != "comp":
        comp_hovering = True
        comp_btn.place_configure(y=240)

def on_comp_leave(e):
    global comp_hovering
    comp_hovering = False
    if selected_mode != "comp":
        comp_btn.place_configure(y=250)

def on_next_enter(e):
    global next_hovering
    if not next_hovering:
        next_hovering = True
        next_btn.place_configure(y=410)

def on_next_leave(e):
    global next_hovering
    next_hovering = False
    next_btn.place_configure(y=420)

def on_p2_enter(e):
    global p2_hovering
    if not p2_hovering and selected_mode != "2p":
        p2_hovering = True
        p2_btn.place_configure(y=240)

def on_p2_leave(e):
    global p2_hovering
    p2_hovering = False
    if selected_mode != "2p":
        p2_btn.place_configure(y=250)

pause_btn.bind("<Enter>", on_pause_enter)
pause_btn.bind("<Leave>", on_pause_leave)
exit_btn2.bind("<Enter>", on_exit2_enter)
exit_btn2.bind("<Leave>", on_exit2_leave)
comp_btn.bind("<Enter>",  on_comp_enter)
comp_btn.bind("<Leave>",  on_comp_leave)
next_btn.bind("<Enter>",  on_next_enter)
next_btn.bind("<Leave>",  on_next_leave)
p2_btn.bind("<Enter>",    on_p2_enter)
p2_btn.bind("<Leave>",    on_p2_leave)

# ═══════════════════════════════════════════════════════════
# GAME SCREEN (placeholder)
# ═══════════════════════════════════════════════════════════
tk.Label(game_frame, text="Game Screen — coming soon",
         bg=BG_COLOR, font=("Arial", 24)).place(x=200, y=250)

# ═══════════════════════════════════════════════════════════
# RESULT SCREEN (placeholder)
# ═══════════════════════════════════════════════════════════
tk.Label(result_frame, text="Result Screen — coming soon",
         bg=BG_COLOR, font=("Arial", 24)).place(x=200, y=250)

# ═══════════════════════════════════════════════════════════
# GAME LOGIC
# ═══════════════════════════════════════════════════════════
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
# ═══════════════════════════════════════════════════════════
# PAUSE FRAME
# ═══════════════════════════════════════════════════════════
pause_home_img   = load_img_bg("home.jpg",    (150, 150), (214, 238, 255))
pause_resume_img = load_img_bg("options.png", (150, 150), (214, 238, 255))
pause_exit_img   = load_img("exit.png",       (60, 60))

pause_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
pause_frame.place(x=0, y=0, width=800, height=600)

pause_exit_btn = tk.Label(pause_frame, image=pause_exit_img, bg=BG_COLOR)
pause_exit_btn.image = pause_exit_img
pause_exit_btn.place(x=730, y=5)

pause_home_btn = tk.Label(pause_frame, image=pause_home_img, bg=BG_COLOR)
pause_home_btn.image = pause_home_img
pause_home_btn.place(x=180, y=225)

pause_resume_btn = tk.Label(pause_frame, image=pause_resume_img, bg=BG_COLOR)
pause_resume_btn.image = pause_resume_img
pause_resume_btn.place(x=470, y=225)

current_frame_before_pause = [None]

def show_pause(from_frame):
    current_frame_before_pause[0] = from_frame
    pause_frame.tkraise()

def resume_game():
    if current_frame_before_pause[0]:
        current_frame_before_pause[0].tkraise()

pause_exit_btn.bind("<Button-1>",   lambda e: resume_game())
pause_home_btn.bind("<Button-1>",   lambda e: show_frame(home_frame))
pause_resume_btn.bind("<Button-1>", lambda e: resume_game())
pause_btn.bind("<Button-1>",        lambda e: show_pause(setup_frame))

pe_hovering = False
ph_hovering = False
pr_hovering = False

def on_pe_enter(e):
    global pe_hovering
    if not pe_hovering:
        pe_hovering = True
        pause_exit_btn.place_configure(y=-5)

def on_pe_leave(e):
    global pe_hovering
    pe_hovering = False
    pause_exit_btn.place_configure(y=5)

def on_ph_enter(e):
    global ph_hovering
    if not ph_hovering:
        ph_hovering = True
        pause_home_btn.place_configure(y=215)

def on_ph_leave(e):
    global ph_hovering
    ph_hovering = False
    pause_home_btn.place_configure(y=225)

def on_pr_enter(e):
    global pr_hovering
    if not pr_hovering:
        pr_hovering = True
        pause_resume_btn.place_configure(y=215)

def on_pr_leave(e):
    global pr_hovering
    pr_hovering = False
    pause_resume_btn.place_configure(y=225)

pause_exit_btn.bind("<Enter>",   on_pe_enter)
pause_exit_btn.bind("<Leave>",   on_pe_leave)
pause_home_btn.bind("<Enter>",   on_ph_enter)
pause_home_btn.bind("<Leave>",   on_ph_leave)
pause_resume_btn.bind("<Enter>", on_pr_enter)
pause_resume_btn.bind("<Leave>", on_pr_leave)

# ═══════════════════════════════════════════════════════════
# ROUNDS FRAME
# ═══════════════════════════════════════════════════════════
plus_img_r       = load_img("plus.jpg",   (80, 80))
moins_img_r      = load_img("moins.jpg",  (80, 80))
rounds_title_img = load_img("rounds.png", (400, 100))

number_imgs_small = {
    "one":   load_img("one.gif",   (80, 80)),
    "two":   load_img("two.gif",   (80, 80)),
    "three": load_img("three.gif", (80, 80)),
    "four":  load_img("four.gif",  (80, 80)),
    "five":  load_img("five.gif",  (80, 80)),
    "six":   load_img("six.gif",   (80, 80)),
    "seven": load_img("seven.gif", (80, 80)),
    "eight": load_img("eight.gif", (80, 80)),
    "nine":  load_img("nine.gif",  (80, 80)),
}

digit_map = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
    6: "six", 7: "seven", 8: "eight", 9: "nine"
}

rounds_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
rounds_frame.place(x=0, y=0, width=800, height=600)

rounds_val = [1]

# ── top buttons ──
pause_btn2 = tk.Label(rounds_frame, image=pause_img, bg=BG_COLOR)
pause_btn2.image = pause_img
pause_btn2.place(x=5, y=5)
pause_btn2.bind("<Button-1>", lambda e: show_pause(rounds_frame))

exit_btn3 = tk.Label(rounds_frame, image=exit_img, bg=BG_COLOR)
exit_btn3.image = exit_img
exit_btn3.place(x=745, y=5)
exit_btn3.bind("<Button-1>", lambda e: root.destroy())

# ── ROUNDS title centered ──
rounds_title = tk.Label(rounds_frame, image=rounds_title_img, bg=BG_COLOR)
rounds_title.image = rounds_title_img
rounds_title.place(x=200, y=80)

# ── row: minus | number(s) | plus all centered at y=260 ──
# minus at x=160, plus at x=560, number zone center=400
moins_btn = tk.Label(rounds_frame, image=moins_img_r, bg=BG_COLOR, cursor="hand2")
moins_btn.image = moins_img_r
moins_btn.place(x=160, y=260)

# two digit labels, will be positioned dynamically
rounds_display_left  = tk.Label(rounds_frame, bg=BG_COLOR)
rounds_display_right = tk.Label(rounds_frame, bg=BG_COLOR)
rounds_display_left.place(x=0, y=260)   # positioned in update_display
rounds_display_right.place(x=0, y=260)  # positioned in update_display

plus_btn_r = tk.Label(rounds_frame, image=plus_img_r, bg=BG_COLOR, cursor="hand2")
plus_btn_r.image = plus_img_r
plus_btn_r.place(x=560, y=260)

# ── next button centered ──
next_btn2 = tk.Label(rounds_frame, image=next_img, bg=BG_COLOR)
next_btn2.image = next_img
next_btn2.place(x=310, y=430)

# ── logic ──
CENTER_X = 400
BASE_Y   = 260

def update_display(direction):
    val = rounds_val[0]

    if val < 10:
        # single digit — center one image at 400
        rounds_display_left.config(image='')
        rounds_display_left.image = None
        img = number_imgs_small[digit_map[val]]
        rounds_display_right.config(image=img)
        rounds_display_right.image = img
        # center single: x = CENTER_X - 40 (half of 80)
        rounds_display_right.place_configure(x=CENTER_X - 40)
        rounds_display_left.place_configure(x=-100)  # hide off screen
    else:
        tens  = val // 10
        units = val % 10
        img_l = number_imgs_small[digit_map[tens]]
        img_r = number_imgs_small[digit_map[units]] if units in digit_map else number_imgs_small["one"]
        rounds_display_left.config(image=img_l)
        rounds_display_left.image = img_l
        rounds_display_right.config(image=img_r)
        rounds_display_right.image = img_r
        # center two: total width = 160+8gap, start = CENTER_X - 84
        rounds_display_left.place_configure(x=CENTER_X - 84)
        rounds_display_right.place_configure(x=CENTER_X + 4)

    shift = -15 if direction == "up" else 15
    rounds_display_left.place_configure(y=BASE_Y + shift)
    rounds_display_right.place_configure(y=BASE_Y + shift)
    rounds_frame.after(80, lambda: [
        rounds_display_left.place_configure(y=BASE_Y),
        rounds_display_right.place_configure(y=BASE_Y)
    ])

update_display("up")

def add_round():
    if rounds_val[0] < 21:
        rounds_val[0] += 2
        update_display("up")

def sub_round():
    if rounds_val[0] > 1:
        rounds_val[0] -= 2
        update_display("down")

moins_btn.bind("<Button-1>",  lambda e: sub_round())
plus_btn_r.bind("<Button-1>", lambda e: add_round())

# ── hover animations ──
moins_hovering  = False
plus_r_hovering = False
next2_hovering  = False
pause2_hovering = False
exit3_hovering  = False

def on_moins_enter(e):
    global moins_hovering
    if not moins_hovering:
        moins_hovering = True
        moins_btn.place_configure(y=250)

def on_moins_leave(e):
    global moins_hovering
    moins_hovering = False
    moins_btn.place_configure(y=260)

def on_plus_r_enter(e):
    global plus_r_hovering
    if not plus_r_hovering:
        plus_r_hovering = True
        plus_btn_r.place_configure(y=250)

def on_plus_r_leave(e):
    global plus_r_hovering
    plus_r_hovering = False
    plus_btn_r.place_configure(y=260)

def on_next2_enter(e):
    global next2_hovering
    if not next2_hovering:
        next2_hovering = True
        next_btn2.place_configure(y=420)

def on_next2_leave(e):
    global next2_hovering
    next2_hovering = False
    next_btn2.place_configure(y=430)

def on_pause2_enter(e):
    global pause2_hovering
    if not pause2_hovering:
        pause2_hovering = True
        pause_btn2.place_configure(y=-5)

def on_pause2_leave(e):
    global pause2_hovering
    pause2_hovering = False
    pause_btn2.place_configure(y=5)

def on_exit3_enter(e):
    global exit3_hovering
    if not exit3_hovering:
        exit3_hovering = True
        exit_btn3.place_configure(y=-5)

def on_exit3_leave(e):
    global exit3_hovering
    exit3_hovering = False
    exit_btn3.place_configure(y=5)

moins_btn.bind("<Enter>",   on_moins_enter)
moins_btn.bind("<Leave>",   on_moins_leave)
plus_btn_r.bind("<Enter>",  on_plus_r_enter)
plus_btn_r.bind("<Leave>",  on_plus_r_leave)
next_btn2.bind("<Enter>",   on_next2_enter)
next_btn2.bind("<Leave>",   on_next2_leave)
pause_btn2.bind("<Enter>",  on_pause2_enter)
pause_btn2.bind("<Leave>",  on_pause2_leave)
exit_btn3.bind("<Enter>",   on_exit3_enter)
exit_btn3.bind("<Leave>",   on_exit3_leave)

next_btn.bind("<Button-1>", lambda e: show_frame(rounds_frame) if selected_mode else None)
# ── Start ─────────────────────────────────────────────────
show_frame(home_frame)
root.mainloop()