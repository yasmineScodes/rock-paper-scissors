import tkinter as tk
from PIL import Image, ImageTk
import math
from random import randint

root = tk.Tk()
root.title("Rock Paper Scissors Shoot")
root.geometry("800x600")
root.resizable(False, False)

BG_COLOR = "#d6eeff"

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

# ── Load all images ───────────────────────────────────────
options_img      = load_img("options.png",  (50, 50))
exit_img         = load_img("exit.png",     (50, 50))
title1_img       = load_img("rps.png",      (500, 100))
title2_img       = load_img("shoot.png",    (400, 80))
play_img         = load_img("play.png",     (220, 168))
rock_img         = load_img("rock.png",     (105, 105))
paper_img        = load_img("paper.png",    (90, 90))
scissors_img     = load_img("scissors.png", (105, 105))
pause_img        = load_img_bg("pause.jpg", (50, 50), (214, 238, 255))
home_img         = load_img_bg("home.jpg",  (50, 50), (214, 238, 255))
comp_img         = load_img("comp.jpg",     (180, 115))
next_img         = load_img("next.gif",     (180, 115))
p2_img           = load_img("2p.gif",       (180, 115))
plus_img_r       = load_img("plus.jpg",     (80, 80))
moins_img_r      = load_img("moins.jpg",    (80, 80))
rounds_title_img = load_img("rounds.png",   (400, 100))
pause_home_img   = load_img_bg("home.jpg",    (150, 150), (214, 238, 255))
pause_resume_img = load_img_bg("options.png", (150, 150), (214, 238, 255))
pause_exit_img   = load_img("exit.png",       (60, 60))
sfx_img     = load_img("sfx.gif",     (60, 60))
nosfx_img   = load_img("nosfx.gif",   (71, 56))
music_img   = load_img("music.gif",   (60, 54))
nomusic_img = load_img("nomusic.gif", (60, 56))
cursor_img       = load_img("cursor.gif",      (30, 62))

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

# ── Frames ──────────────────────────────────────────────
home_frame   = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
setup_frame  = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
rounds_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
game_frame   = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
result_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
pause_frame  = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
menu_frame   = tk.Frame(root, width=800, height=600, bg=BG_COLOR)

for frame in (home_frame, setup_frame, rounds_frame,
              game_frame, result_frame, pause_frame, menu_frame):
    frame.place(x=0, y=0, width=800, height=600)

pending = []

def schedule(ms, fn):
    pending.append(root.after(ms, fn))

def cancel_timers():
    for t in pending:
        root.after_cancel(t)
    pending.clear()

def show_frame(frame):
    cancel_timers()
    frame.tkraise()

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
        options_btn.place_configure(y=-5)

def on_options_leave(e):
    global options_hovering
    options_hovering = False
    options_btn.place_configure(y=5)

options_btn.bind("<Enter>",    on_options_enter)
options_btn.bind("<Leave>",    on_options_leave)
options_btn.bind("<Button-1>", lambda e: show_menu(home_frame))

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

play_btn.bind("<Enter>",    on_enter)
play_btn.bind("<Leave>",    on_leave)
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

FLOAT_AMP   = 10
FLOAT_SPEED = 0.05
TICK_MS     = 30

phases = {
    "rock_L": 0.0, "paper_L": 1.1, "scissors_L": 2.3,
    "rock_R": 0.7, "paper_R": 1.8, "scissors_R": 3.0,
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

pause_btn.bind("<Enter>",    on_pause_enter)
pause_btn.bind("<Leave>",    on_pause_leave)
pause_btn.bind("<Button-1>", lambda e: show_pause(setup_frame))
exit_btn2.bind("<Enter>",    on_exit2_enter)
exit_btn2.bind("<Leave>",    on_exit2_leave)
comp_btn.bind("<Enter>",     on_comp_enter)
comp_btn.bind("<Leave>",     on_comp_leave)
next_btn.bind("<Enter>",     on_next_enter)
next_btn.bind("<Leave>",     on_next_leave)
next_btn.bind("<Button-1>",  lambda e: show_frame(rounds_frame) if selected_mode else None)
p2_btn.bind("<Enter>",       on_p2_enter)
p2_btn.bind("<Leave>",       on_p2_leave)

# ═══════════════════════════════════════════════════════════
# ROUNDS FRAME
# ═══════════════════════════════════════════════════════════
pause_btn2 = tk.Label(rounds_frame, image=pause_img, bg=BG_COLOR)
pause_btn2.image = pause_img
pause_btn2.place(x=5, y=5)
pause_btn2.bind("<Button-1>", lambda e: show_pause(rounds_frame))

exit_btn3 = tk.Label(rounds_frame, image=exit_img, bg=BG_COLOR)
exit_btn3.image = exit_img
exit_btn3.place(x=745, y=5)
exit_btn3.bind("<Button-1>", lambda e: root.destroy())

rounds_title = tk.Label(rounds_frame, image=rounds_title_img, bg=BG_COLOR)
rounds_title.image = rounds_title_img
rounds_title.place(x=200, y=80)

moins_btn = tk.Label(rounds_frame, image=moins_img_r, bg=BG_COLOR, cursor="hand2")
moins_btn.image = moins_img_r
moins_btn.place(x=160, y=260)

rounds_display_left  = tk.Label(rounds_frame, bg=BG_COLOR)
rounds_display_right = tk.Label(rounds_frame, bg=BG_COLOR)
rounds_display_left.place(x=0,   y=260)
rounds_display_right.place(x=0,  y=260)

plus_btn_r = tk.Label(rounds_frame, image=plus_img_r, bg=BG_COLOR, cursor="hand2")
plus_btn_r.image = plus_img_r
plus_btn_r.place(x=560, y=260)

next_btn2 = tk.Label(rounds_frame, image=next_img, bg=BG_COLOR)
next_btn2.image = next_img
next_btn2.place(x=310, y=430)

rounds_val = [1]
CENTER_X   = 400
BASE_Y     = 260

def update_display(direction):
    val = rounds_val[0]
    if val < 10:
        rounds_display_left.config(image='')
        rounds_display_left.image = None
        img = number_imgs_small[digit_map[val]]
        rounds_display_right.config(image=img)
        rounds_display_right.image = img
        rounds_display_right.place_configure(x=CENTER_X - 40)
        rounds_display_left.place_configure(x=-100)
    else:
        tens  = val // 10
        units = val % 10
        img_l = number_imgs_small[digit_map[tens]]
        img_r = number_imgs_small[digit_map[units]] if units in digit_map else number_imgs_small["one"]
        rounds_display_left.config(image=img_l)
        rounds_display_left.image = img_l
        rounds_display_right.config(image=img_r)
        rounds_display_right.image = img_r
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

# ═══════════════════════════════════════════════════════════
# PAUSE FRAME
# ═══════════════════════════════════════════════════════════
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
pause_resume_btn.bind("<Button-1>", lambda e: show_menu(pause_frame))

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
# MENU FRAME
# ═══════════════════════════════════════════════════════════
frame_before_menu = [None]

def show_menu(from_frame):
    frame_before_menu[0] = from_frame
    menu_frame.tkraise()

def close_menu():
    if frame_before_menu[0]:
        frame_before_menu[0].tkraise()

exit_menu_btn = tk.Label(menu_frame, image=exit_img, bg=BG_COLOR)
exit_menu_btn.image = exit_img
exit_menu_btn.place(x=745, y=5)
exit_menu_btn.bind("<Button-1>", lambda e: close_menu())

exit_menu_hovering = False

def on_exit_menu_enter(e):
    global exit_menu_hovering
    if not exit_menu_hovering:
        exit_menu_hovering = True
        exit_menu_btn.place_configure(y=-5)

def on_exit_menu_leave(e):
    global exit_menu_hovering
    exit_menu_hovering = False
    exit_menu_btn.place_configure(y=5)

exit_menu_btn.bind("<Enter>", on_exit_menu_enter)
exit_menu_btn.bind("<Leave>", on_exit_menu_leave)

SLIDER_X     = 250
SLIDER_W     = 400
SLIDER_SFX_Y = 200
SLIDER_MUS_Y = 360

sfx_val   = [50]
music_val = [50]

sfx_icon = tk.Label(menu_frame, image=sfx_img, bg=BG_COLOR)
sfx_icon.image = sfx_img
sfx_icon.place(x=150, y=SLIDER_SFX_Y - 5)

sfx_bar = tk.Canvas(menu_frame, width=SLIDER_W, height=8,
                    bg="#a0c8f0", highlightthickness=0)
sfx_bar.place(x=SLIDER_X, y=SLIDER_SFX_Y + 26)

sfx_cursor_btn = tk.Label(menu_frame, image=cursor_img, bg=BG_COLOR)
sfx_cursor_btn.image = cursor_img
sfx_cursor_btn.place(x=SLIDER_X + int(sfx_val[0] / 100 * SLIDER_W) - 15,
                     y=SLIDER_SFX_Y)

music_icon = tk.Label(menu_frame, image=music_img, bg=BG_COLOR)
music_icon.image = music_img
music_icon.place(x=150, y=SLIDER_MUS_Y - 5)

music_bar = tk.Canvas(menu_frame, width=SLIDER_W, height=8,
                      bg="#a0c8f0", highlightthickness=0)
music_bar.place(x=SLIDER_X, y=SLIDER_MUS_Y + 26)

music_cursor_btn = tk.Label(menu_frame, image=cursor_img, bg=BG_COLOR)
music_cursor_btn.image = cursor_img
music_cursor_btn.place(x=SLIDER_X + int(music_val[0] / 100 * SLIDER_W) - 15,
                       y=SLIDER_MUS_Y)

def update_sfx_icon():
    img = nosfx_img if sfx_val[0] == 0 else sfx_img
    sfx_icon.config(image=img)
    sfx_icon.image = img

def update_music_icon():
    img = nomusic_img if music_val[0] == 0 else music_img
    music_icon.config(image=img)
    music_icon.image = img

def on_sfx_drag(e):
    x = max(0, min(e.x, SLIDER_W))
    sfx_val[0] = int(x / SLIDER_W * 100)
    sfx_cursor_btn.place_configure(x=SLIDER_X + x - 15)
    update_sfx_icon()

def on_music_drag(e):
    x = max(0, min(e.x, SLIDER_W))
    music_val[0] = int(x / SLIDER_W * 100)
    music_cursor_btn.place_configure(x=SLIDER_X + x - 15)
    update_music_icon()

def on_sfx_cursor_drag(e):
    abs_x = sfx_cursor_btn.winfo_x() - SLIDER_X + e.x
    abs_x = max(0, min(abs_x, SLIDER_W))
    sfx_val[0] = int(abs_x / SLIDER_W * 100)
    sfx_cursor_btn.place_configure(x=SLIDER_X + abs_x - 15)
    update_sfx_icon()

def on_music_cursor_drag(e):
    abs_x = music_cursor_btn.winfo_x() - SLIDER_X + e.x
    abs_x = max(0, min(abs_x, SLIDER_W))
    music_val[0] = int(abs_x / SLIDER_W * 100)
    music_cursor_btn.place_configure(x=SLIDER_X + abs_x - 15)
    update_music_icon()

sfx_bar.bind("<B1-Motion>",        on_sfx_drag)
sfx_bar.bind("<Button-1>",         on_sfx_drag)
music_bar.bind("<B1-Motion>",      on_music_drag)
music_bar.bind("<Button-1>",       on_music_drag)
sfx_cursor_btn.bind("<B1-Motion>", on_sfx_cursor_drag)
music_cursor_btn.bind("<B1-Motion>", on_music_cursor_drag)


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
        (choice1 == "rock"     and choice2 == "scissors") or
        (choice1 == "paper"    and choice2 == "rock")     or
        (choice1 == "scissors" and choice2 == "paper")
    ):
        return 1
    else:
        return 2

# ═══════════════════════════════════════════════════════════
# CHARACTER FRAME
# ═══════════════════════════════════════════════════════════
BG_RGB = (214, 238, 255)

def make_variants(path, h):
    """Same-height versions: normal, hover, selected, disabled (faded)."""
    base = Image.open(path).convert("RGBA")
    def size(s):
        return (round(base.width * h * s / base.height), round(h * s))
    v = {}
    for key, s in (("n", 1.0), ("h", 1.2), ("s", 1.3)):
        v[key] = ImageTk.PhotoImage(base.resize(size(s), Image.Resampling.NEAREST))
    bg   = Image.new("RGBA", base.size, BG_RGB + (255,))
    comp = Image.alpha_composite(bg, base)
    faded = Image.blend(bg, comp, 0.3)
    v["d"] = ImageTk.PhotoImage(faded.resize(size(1.0), Image.Resampling.NEAREST))
    return v

CHAR_H = 150   # every character gets the same height

char_title_img = load_img("characters.png", (600, 120))          # bigger title
player_img     = load_img("player.png",     (180, 90))           # bigger "PLAYER"
num_small      = {1: load_img("one.gif", (55, 55)),              # smaller number
                  2: load_img("two.gif", (55, 55))}
next_char_img  = load_img("next.gif",       (150, 96))

chars_info = [
    {"name": "gumball", "file": "gumball.png", "cx": 100},
    {"name": "darwin",  "file": "darwin.png",  "cx": 300},
    {"name": "elsa",    "file": "elsa.png",    "cx": 500},
    {"name": "iceking", "file": "iceking.gif", "cx": 700},
]
for info in chars_info:
    info["imgs"] = make_variants(info["file"], CHAR_H)

char_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
char_frame.place(x=0, y=0, width=800, height=600)

# ── top buttons ──
pause_btn3 = tk.Label(char_frame, image=pause_img, bg=BG_COLOR)
pause_btn3.image = pause_img
pause_btn3.place(x=5, y=5)
pause_btn3.bind("<Button-1>", lambda e: show_pause(char_frame))

exit_btn4 = tk.Label(char_frame, image=exit_img, bg=BG_COLOR)
exit_btn4.image = exit_img
exit_btn4.place(x=745, y=5)
exit_btn4.bind("<Button-1>", lambda e: root.destroy())

# ── title ──
char_title = tk.Label(char_frame, image=char_title_img, bg=BG_COLOR)
char_title.image = char_title_img
char_title.place(x=100, y=40)

# ── bottom row:  PLAYER [1]  [name box]            [NEXT] ──
ROW_CY = 520

player_label = tk.Label(char_frame, image=player_img, bg=BG_COLOR)
player_label.image = player_img
player_label.place(x=30, y=ROW_CY, anchor="w")

player_num_display = tk.Label(char_frame, bg=BG_COLOR)
player_num_display.place(x=222, y=ROW_CY, anchor="w")

name_var = tk.StringVar()
name_entry = tk.Entry(char_frame, textvariable=name_var, font=("Courier", 18, "bold"),
                      bg="white", fg="#1a6ebd", relief="flat",
                      highlightthickness=3, highlightcolor="#1a6ebd",
                      highlightbackground="#a0c8f0", justify="center")
name_entry.place(x=295, y=ROW_CY, anchor="w", width=270, height=48)

char_next_btn = tk.Label(char_frame, image=next_char_img, bg=BG_COLOR, cursor="hand2")
char_next_btn.image = next_char_img
char_next_btn.place(x=620, y=ROW_CY, anchor="w")

# ── characters ──
CHAR_CY          = 300
CHAR_FLOAT_AMP   = 10
CHAR_FLOAT_SPEED = 0.15      # faster up/down
CHAR_TICK_MS     = 30

char_labels   = []
char_hovering = [False] * 4
selected_idx  = [None]        # character picked by the current player
taken         = set()         # characters already used by player 1
char_angles   = [i * 0.9 for i in range(4)]

current_player_turn = [0]     # 0 = player 1, 1 = player 2
p1_char, p2_char = [None], [None]
p1_name, p2_name = ["Player 1"], ["Player 2"]

def refresh_char(i):
    imgs = chars_info[i]["imgs"]
    if i in taken:
        key = "d"
    elif selected_idx[0] == i:
        key = "s"
    elif char_hovering[i]:
        key = "h"
    else:
        key = "n"
    char_labels[i].config(image=imgs[key], cursor="arrow" if i in taken else "hand2")
    char_labels[i].image = imgs[key]

for i, info in enumerate(chars_info):
    lbl = tk.Label(char_frame, image=info["imgs"]["n"], bg=BG_COLOR, cursor="hand2")
    lbl.image = info["imgs"]["n"]
    lbl.place(x=info["cx"], y=CHAR_CY, anchor="center")
    char_labels.append(lbl)

def select_char(i):
    if i in taken:
        return                      # already chosen by player 1
    old = selected_idx[0]
    selected_idx[0] = i
    if old is not None:
        refresh_char(old)
    refresh_char(i)

def on_char_enter(i):
    def h(e):
        char_hovering[i] = True
        refresh_char(i)
    return h

def on_char_leave(i):
    def h(e):
        char_hovering[i] = False
        refresh_char(i)
    return h

for i, lbl in enumerate(char_labels):
    lbl.bind("<Enter>",    on_char_enter(i))
    lbl.bind("<Leave>",    on_char_leave(i))
    lbl.bind("<Button-1>", lambda e, idx=i: select_char(idx))

def animate_chars():
    for i, lbl in enumerate(char_labels):
        if selected_idx[0] == i or i in taken:
            lbl.place_configure(y=CHAR_CY)
        else:
            char_angles[i] += CHAR_FLOAT_SPEED
            lbl.place_configure(y=CHAR_CY + int(CHAR_FLOAT_AMP * math.sin(char_angles[i])))
    char_frame.after(CHAR_TICK_MS, animate_chars)

animate_chars()

def update_player_num():
    img = num_small[current_player_turn[0] + 1]
    player_num_display.config(image=img)
    player_num_display.image = img

update_player_num()

# ── NEXT logic ──
def flash_name():
    name_entry.config(highlightbackground="red", highlightcolor="red")
    name_entry.focus_set()

def reset_name_border(*_):
    name_entry.config(highlightbackground="#a0c8f0", highlightcolor="#1a6ebd")

name_var.trace_add("write", reset_name_border)

def char_next():
    if selected_idx[0] is None:
        return
    name = name_var.get().strip()
    if not name:                       # name is required
        flash_name()
        return
    turn = current_player_turn[0]

    if turn == 0:
        p1_char[0] = chars_info[selected_idx[0]]["name"]
        p1_name[0] = name
        if selected_mode == "2p":
            taken.add(selected_idx[0])
            selected_idx[0] = None
            current_player_turn[0] = 1
            name_var.set("")
            update_player_num()
            for i in range(4):
                refresh_char(i)
        else:
            free = [i for i in range(4) if i != selected_idx[0]]
            p2_char[0] = chars_info[free[randint(0, len(free) - 1)]]["name"]
            p2_name[0] = "Computer"
            show_vs()
    else:
        p2_char[0] = chars_info[selected_idx[0]]["name"]
        p2_name[0] = name
        show_vs()

char_next_btn.bind("<Button-1>", lambda e: char_next())

# ── hover effects ──
pause3_hovering = False
exit4_hovering  = False
cnext_hovering  = False

def on_pause3_enter(e):
    global pause3_hovering
    if not pause3_hovering:
        pause3_hovering = True
        pause_btn3.place_configure(y=-5)

def on_pause3_leave(e):
    global pause3_hovering
    pause3_hovering = False
    pause_btn3.place_configure(y=5)

def on_exit4_enter(e):
    global exit4_hovering
    if not exit4_hovering:
        exit4_hovering = True
        exit_btn4.place_configure(y=-5)

def on_exit4_leave(e):
    global exit4_hovering
    exit4_hovering = False
    exit_btn4.place_configure(y=5)

def on_cnext_enter(e):
    global cnext_hovering
    if not cnext_hovering:
        cnext_hovering = True
        char_next_btn.place_configure(y=ROW_CY - 10)

def on_cnext_leave(e):
    global cnext_hovering
    cnext_hovering = False
    char_next_btn.place_configure(y=ROW_CY)

pause_btn3.bind("<Enter>",    on_pause3_enter)
pause_btn3.bind("<Leave>",    on_pause3_leave)
exit_btn4.bind("<Enter>",     on_exit4_enter)
exit_btn4.bind("<Leave>",     on_exit4_leave)
char_next_btn.bind("<Enter>", on_cnext_enter)
char_next_btn.bind("<Leave>", on_cnext_leave)

# ── wire rounds → character screen ──
def go_to_char_frame():
    taken.clear()
    selected_idx[0] = None
    p1_char[0] = p2_char[0] = None
    current_player_turn[0] = 0
    name_var.set("")
    update_player_num()
    for i in range(4):
        char_hovering[i] = False
        refresh_char(i)
    show_frame(char_frame)

next_btn2.bind("<Button-1>", lambda e: go_to_char_frame())
# ═══════════════════════════════════════════════════════════
# VS FRAME
# ═══════════════════════════════════════════════════════════
from PIL import ImageDraw

def load_img_transparent(path, size):
    img = Image.open(path).convert("RGBA")
    ImageDraw.floodfill(img, (0, 0), (255, 0, 255, 0), thresh=40)
    return ImageTk.PhotoImage(img.resize(size, Image.Resampling.NEAREST))

vs_pause_img = load_img_transparent("pause.jpg", (50, 50))

vs_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
vs_frame.place(x=0, y=0, width=800, height=600)

vs_canvas = tk.Canvas(vs_frame, width=800, height=600,
                      highlightthickness=0, bd=0, bg=BG_COLOR)
vs_canvas.place(x=0, y=0)

vs_bg_item    = vs_canvas.create_image(0, 0, anchor="nw")
vs_pause_item = vs_canvas.create_image(5,   5, anchor="nw", image=vs_pause_img)
vs_exit_item  = vs_canvas.create_image(745, 5, anchor="nw", image=exit_img)

vs_bg_photo = [None]

def show_vs():
    reset_match()
    a, b = p1_char[0], p2_char[0]
    photo = None
    for fname in (f"{a}.{b}.png", f"{b}.{a}.png"):
        try:
            photo = load_img(fname, (800, 600))
            break
        except FileNotFoundError:
            continue
    if photo is None:
        print(f"VS picture not found for {a} / {b}")
    vs_bg_photo[0] = photo
    vs_canvas.itemconfig(vs_bg_item, image=photo if photo else "")
    for item in (vs_pause_item, vs_exit_item):
        vs_canvas.tag_raise(item)
    show_frame(vs_frame)
    schedule(3500, start_choose)          # auto-continue after 3.5 s

def vs_hover(item, base_y):
    def enter(e):
        vs_canvas.coords(item, vs_canvas.coords(item)[0], base_y - 10)
    def leave(e):
        vs_canvas.coords(item, vs_canvas.coords(item)[0], base_y)
    vs_canvas.tag_bind(item, "<Enter>", enter)
    vs_canvas.tag_bind(item, "<Leave>", leave)

vs_hover(vs_pause_item, 5)
vs_hover(vs_exit_item,  5)
vs_canvas.tag_bind(vs_pause_item, "<Button-1>", lambda e: show_pause(vs_frame))
vs_canvas.tag_bind(vs_exit_item,  "<Button-1>", lambda e: root.destroy())

# ═══════════════════════════════════════════════════════════
# SHARED HELPERS FOR THE GAME SCREENS
# ═══════════════════════════════════════════════════════════
HAND_FILES = {"rock": "rock.gif", "paper": "paper.gif", "scissors": "scissors.gif"}
HANDS = ["rock", "paper", "scissors"]

def load_h(path, h):
    """Load an image at a given height, keeping its proportions."""
    base = Image.open(path).convert("RGBA")
    return ImageTk.PhotoImage(
        base.resize((round(base.width * h / base.height), h), Image.Resampling.NEAREST))

def add_lift(w, base_y, dy=10):
    w.bind("<Enter>", lambda e: w.place_configure(y=base_y - dy))
    w.bind("<Leave>", lambda e: w.place_configure(y=base_y))

hand_var    = {k: make_variants(f, 150) for k, f in HAND_FILES.items()}  # n / h / s
hand_center = {k: load_h(f, 240) for k, f in HAND_FILES.items()}         # computer spin
hand_reveal = {k: load_h(f, 180) for k, f in HAND_FILES.items()}         # reveal
hand_small  = {k: load_h(f, 150) for k, f in HAND_FILES.items()}         # countdown (sides)

# "shoot" frames: big -> small, fast
_shoot = Image.open("shoot.png").convert("RGBA")
_px = _shoot.load()
_W, _H = _shoot.size

def _diff(a, b):
    return sum(abs(a[i] - b[i]) for i in range(4))

# repair 1-pixel-wide glitch columns (differs from both neighbours, which match each other)
_shoot = Image.open("shoot.png").convert("RGBA")
_bg    = Image.new("RGBA", _shoot.size, BG_RGB + (255,))
_shoot = Image.alpha_composite(_bg, _shoot).convert("RGB")
_px = _shoot.load()
_W, _H = _shoot.size

def _d(a, b):
    return sum(abs(a[i] - b[i]) for i in range(3))

# count, for each column, the pixels that differ from BOTH neighbours
# while the two neighbours look alike -> that's a thin line
_counts = {}
for _x in range(1, _W - 1):
    n = 0
    for _y in range(_H):
        l, c, r = _px[_x - 1, _y], _px[_x, _y], _px[_x + 1, _y]
        if _d(l, r) < 20 and _d(c, l) > 25:
            n += 1
    _counts[_x] = n

_top = sorted(_counts.items(), key=lambda kv: -kv[1])[:5]
print("most suspicious columns (x, pixels):", _top)

for _x, n in _counts.items():
    if n >= 4:                                  # repair from the left neighbour
        for _y in range(_H):
            _px[_x, _y] = _px[_x - 1, _y]
        print("repaired column", _x)
SHOOT_STEPS   = 8        # 8 steps x 40 ms = 0.32 s
SHOOT_STEP_MS = 40
shoot_frames = []
for s in range(SHOOT_STEPS + 1):
    w = round(640 - (640 - 220) * s / SHOOT_STEPS)
    shoot_frames.append(ImageTk.PhotoImage(
        _shoot.resize((w, round(w * _shoot.height / _shoot.width)),
                      Image.Resampling.NEAREST)))

score = [0, 0]

def reset_match():
    score[0] = score[1] = 0

# ═══════════════════════════════════════════════════════════
# CHOOSE FRAME  (Player 1 / Player 2 pick a hand)
# ═══════════════════════════════════════════════════════════
top_player_img = load_img("player.png", (240, 120))
top_num = {1: load_img("one.gif", (70, 70)), 2: load_img("two.gif", (70, 70))}
choose_next_img = load_img("next.gif", (150, 96))

choose_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
choose_frame.place(x=0, y=0, width=800, height=600)

c_pause = tk.Label(choose_frame, image=pause_img, bg=BG_COLOR)
c_pause.image = pause_img
c_pause.place(x=5, y=5)
c_pause.bind("<Button-1>", lambda e: show_pause(choose_frame))
add_lift(c_pause, 5)

c_exit = tk.Label(choose_frame, image=exit_img, bg=BG_COLOR)
c_exit.image = exit_img
c_exit.place(x=745, y=5)
c_exit.bind("<Button-1>", lambda e: root.destroy())
add_lift(c_exit, 5)

c_title = tk.Label(choose_frame, image=top_player_img, bg=BG_COLOR)
c_title.image = top_player_img
c_title.place(x=235, y=30)

c_num = tk.Label(choose_frame, image=top_num[1], bg=BG_COLOR)
c_num.image = top_num[1]
c_num.place(x=495, y=55)

c_next = tk.Label(choose_frame, image=choose_next_img, bg=BG_COLOR, cursor="hand2")
c_next.image = choose_next_img
c_next.place(x=790, y=590, anchor="se")
add_lift(c_next, 590)

HAND_CX, HAND_CY = {"rock": 160, "paper": 400, "scissors": 640}, 310
hand_lbls  = {}
hand_hov   = {k: False for k in HANDS}
hand_ang   = {k: i * 0.9 for i, k in enumerate(HANDS)}
hand_sel   = [None]
hands_active = [True]
comp_active  = [False]
choose_turn  = [0]                 # 0 = player 1, 1 = player 2
p1_pick, p2_pick = [None], [None]

comp_lbl = tk.Label(choose_frame, bg=BG_COLOR)   # the big spinning hand (vs computer)

def refresh_hand(k):
    key = "s" if hand_sel[0] == k else ("h" if hand_hov[k] else "n")
    img = hand_var[k][key]
    hand_lbls[k].config(image=img)
    hand_lbls[k].image = img

def select_hand(k):
    if comp_active[0]:
        return
    old = hand_sel[0]
    hand_sel[0] = k
    if old is not None:
        refresh_hand(old)
    refresh_hand(k)

def hand_enter(k):
    hand_hov[k] = True
    refresh_hand(k)

def hand_leave(k):
    hand_hov[k] = False
    refresh_hand(k)

for k in HANDS:
    lbl = tk.Label(choose_frame, image=hand_var[k]["n"], bg=BG_COLOR, cursor="hand2")
    lbl.image = hand_var[k]["n"]
    lbl.place(x=HAND_CX[k], y=HAND_CY, anchor="center")
    lbl.bind("<Enter>",    lambda e, k=k: hand_enter(k))
    lbl.bind("<Leave>",    lambda e, k=k: hand_leave(k))
    lbl.bind("<Button-1>", lambda e, k=k: select_hand(k))
    hand_lbls[k] = lbl

def animate_hands():
    if hands_active[0]:
        for k in HANDS:
            if hand_sel[0] == k:
                hand_lbls[k].place_configure(y=HAND_CY)
            else:
                hand_ang[k] += 0.15
                hand_lbls[k].place_configure(y=HAND_CY + int(10 * math.sin(hand_ang[k])))
    choose_frame.after(30, animate_hands)

animate_hands()

def set_top_num(n):
    c_num.config(image=top_num[n])
    c_num.image = top_num[n]

def start_choose():
    choose_turn[0] = 0
    p1_pick[0] = p2_pick[0] = None
    hand_sel[0] = None
    comp_active[0] = False
    comp_lbl.place_forget()
    for k in HANDS:
        hand_hov[k] = False
        hand_lbls[k].place(x=HAND_CX[k], y=HAND_CY, anchor="center")
        refresh_hand(k)
    hands_active[0] = True
    set_top_num(1)
    show_frame(choose_frame)

# ── vs computer: one big hand changing every 0.5 s for 3 s ──
def start_computer():
    hands_active[0] = False
    for l in hand_lbls.values():
        l.place_forget()
    set_top_num(2)
    comp_active[0] = True
    comp_lbl.place(x=400, y=330, anchor="center")
    comp_tick(0)

def comp_tick(n):
    if n >= 6:
        finish_computer()
        return
    img = hand_center[HANDS[n % 3]]
    comp_lbl.config(image=img)
    comp_lbl.image = img
    schedule(500, lambda: comp_tick(n + 1))

def finish_computer():
    cancel_timers()
    comp_active[0] = False
    p2_pick[0] = random_choice()
    go_round()

def choose_next():
    if comp_active[0]:                 # Next skips the 3 s wait
        finish_computer()
        return
    if hand_sel[0] is None:
        return
    if choose_turn[0] == 0:
        p1_pick[0] = hand_sel[0]
        if selected_mode == "2p":
            choose_turn[0] = 1
            hand_sel[0] = None
            set_top_num(2)
            for k in HANDS:
                refresh_hand(k)
        else:
            start_computer()
    else:
        p2_pick[0] = hand_sel[0]
        go_round()

c_next.bind("<Button-1>", lambda e: choose_next())

# ═══════════════════════════════════════════════════════════
# ROUND FRAME  (countdown -> shoot -> reveal -> score)
# ═══════════════════════════════════════════════════════════
round_frame = tk.Frame(root, width=800, height=600, bg=BG_COLOR)
round_frame.place(x=0, y=0, width=800, height=600)

r_pause = tk.Label(round_frame, image=pause_img, bg=BG_COLOR)
r_pause.image = pause_img
r_pause.place(x=5, y=5)
r_pause.bind("<Button-1>", lambda e: show_pause(round_frame))
add_lift(r_pause, 5)

r_exit = tk.Label(round_frame, image=exit_img, bg=BG_COLOR)
r_exit.image = exit_img
r_exit.place(x=745, y=5)
r_exit.bind("<Button-1>", lambda e: root.destroy())
add_lift(r_exit, 5)

NAME_FONT  = ("Courier", 24, "bold")
SCORE_FONT = ("Courier", 56, "bold")

r_name1  = tk.Label(round_frame, bg=BG_COLOR, fg="#1a6ebd", font=NAME_FONT)
r_name2  = tk.Label(round_frame, bg=BG_COLOR, fg="#1a6ebd", font=NAME_FONT)
r_score1 = tk.Label(round_frame, bg=BG_COLOR, fg="#1a6ebd", font=SCORE_FONT)
r_score2 = tk.Label(round_frame, bg=BG_COLOR, fg="#1a6ebd", font=SCORE_FONT)
r_name1.place(x=200, y=100, anchor="center")
r_name2.place(x=600, y=100, anchor="center")
r_score1.place(x=200, y=470, anchor="center")
r_score2.place(x=600, y=470, anchor="center")

r_center = tk.Label(round_frame, bg=BG_COLOR)                       # shoot
r_result = tk.Label(round_frame, bg=BG_COLOR, fg="#1a6ebd",
                    font=("Courier", 28, "bold"))                    # "DRAW"
r_hand1  = tk.Label(round_frame, bg=BG_COLOR)
r_hand2  = tk.Label(round_frame, bg=BG_COLOR)

r_next = tk.Label(round_frame, image=choose_next_img, bg=BG_COLOR, cursor="hand2")
r_next.image = choose_next_img
add_lift(r_next, 590)

def show_center(img):
    r_center.config(image=img)
    r_center.image = img
    r_center.place(x=400, y=300, anchor="center")

def update_scores():
    r_score1.config(text=str(score[0]))
    r_score2.config(text=str(score[1]))
HAND_MS = 600            # time each hand shows (was 1000) - lower = faster
TICK_MS_CD = 20
PER_HAND = HAND_MS // TICK_MS_CD

def countdown_tick(tick):
    idx   = tick // PER_HAND
    phase = (tick % PER_HAND) / PER_HAND
    if tick % PER_HAND == 0:
        img = hand_small[HANDS[idx]]
        r_hand1.config(image=img); r_hand1.image = img
        r_hand2.config(image=img); r_hand2.image = img
    y = 300 - int(30 * math.sin(math.pi * phase))
    r_hand1.place(x=200, y=y, anchor="center")
    r_hand2.place(x=600, y=y, anchor="center")

def hide_side_hands():
    r_hand1.place_forget()
    r_hand2.place_forget()

def go_round():
    hide_side_hands()
    r_center.place_forget()
    r_next.place_forget()
    r_result.config(text="")
    r_result.place_forget()
    r_name1.config(text=p1_name[0])
    r_name2.config(text=p2_name[0])
    update_scores()
    show_frame(round_frame)

    total = 3 * HAND_MS
    for tick in range(3 * PER_HAND):
        schedule(tick * TICK_MS_CD, lambda t=tick: countdown_tick(t))

    schedule(total, hide_side_hands)
    for s in range(SHOOT_STEPS + 1):
        schedule(total + s * SHOOT_STEP_MS, lambda s=s: show_center(shoot_frames[s]))

    schedule(total + SHOOT_STEPS * SHOOT_STEP_MS + 300, reveal)

def reveal():
    r_center.place_forget()
    r_hand1.config(image=hand_reveal[p1_pick[0]])
    r_hand1.image = hand_reveal[p1_pick[0]]
    r_hand2.config(image=hand_reveal[p2_pick[0]])
    r_hand2.image = hand_reveal[p2_pick[0]]
    r_hand1.place(x=200, y=300, anchor="center")
    r_hand2.place(x=600, y=300, anchor="center")
    schedule(900, resolve)

def resolve():
    w = get_winner(p1_pick[0], p2_pick[0])
    if w == 0:
        r_result.config(text="DRAW")       # score unchanged
        r_result.place(x=400, y=300, anchor="center")
    else:
        score[w - 1] += 1
        update_scores()
    r_next.place(x=790, y=590, anchor="se")

result_text = tk.Label(result_frame, text="", bg=BG_COLOR, fg="#1a6ebd",
                       font=("Arial", 28, "bold"))
result_text.place(x=400, y=350, anchor="center")

def round_next():
    target = rounds_val[0] // 2 + 1        # first to win the majority of rounds
    if max(score) >= target:
        winner = p1_name[0] if score[0] > score[1] else p2_name[0]
        result_text.config(text=f"{winner} wins!\n{score[0]} - {score[1]}")
        show_frame(result_frame)
    else:
        start_choose()

r_next.bind("<Button-1>", lambda e: round_next())

# ═══════════════════════════════════════════════════════════
# RESULT FRAME  (winner screen)
# ═══════════════════════════════════════════════════════════
char_files = {info["name"]: info["file"] for info in chars_info}
res_imgs   = {name: load_h(f, 220) for name, f in char_files.items()}

res_pause = tk.Label(result_frame, image=pause_img, bg=BG_COLOR)
res_pause.image = pause_img
res_pause.place(x=5, y=5)
res_pause.bind("<Button-1>", lambda e: show_pause(result_frame))
add_lift(res_pause, 5)

res_exit = tk.Label(result_frame, image=exit_img, bg=BG_COLOR)
res_exit.image = exit_img
res_exit.place(x=745, y=5)
res_exit.bind("<Button-1>", lambda e: root.destroy())
add_lift(res_exit, 5)

res_title = tk.Label(result_frame, bg=BG_COLOR, fg="#1a6ebd",
                     font=("Courier", 36, "bold"))
res_title.place(x=400, y=110, anchor="center")

RES_CY = 300
res_char = tk.Label(result_frame, bg=BG_COLOR)
res_char.place(x=400, y=RES_CY, anchor="center")

res_score = tk.Label(result_frame, bg=BG_COLOR, fg="#1a6ebd",
                     font=("Courier", 56, "bold"))
res_score.place(x=400, y=500, anchor="center")

res_ang = [0.0]

def animate_result():
    res_ang[0] += 0.15
    res_char.place_configure(y=RES_CY + int(12 * math.sin(res_ang[0])))
    result_frame.after(30, animate_result)

animate_result()

def show_result():
    w    = 0 if score[0] > score[1] else 1
    name = p1_name[0] if w == 0 else p2_name[0]
    char = p1_char[0]  if w == 0 else p2_char[0]
    res_title.config(text=f"{name} wins!")
    res_char.config(image=res_imgs[char])
    res_char.image = res_imgs[char]
    res_score.config(text=f"{score[0]} - {score[1]}")
    show_frame(result_frame)

def round_next():
    target = rounds_val[0] // 2 + 1        # first to win the majority of rounds
    if max(score) >= target:
        show_result()
    else:
        start_choose()

r_next.bind("<Button-1>", lambda e: round_next())

# ── Start ─────────────────────────────────────────────────
show_frame(home_frame)
root.mainloop()