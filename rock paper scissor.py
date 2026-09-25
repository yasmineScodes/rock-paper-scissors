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

def show_frame(frame):
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
char_title_img = load_img("characters.png", (400, 80))
player_img     = load_img("player.jpg",     (120, 60))
gumball_img    = load_img("gumball.png",    (90, 124))
darwin_img     = load_img("darwin.png",     (90, 111))
elsa_img       = load_img("elsa.png",       (90, 119))
iceking_img    = load_img("iceking.gif",    (90, 100))

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
char_title.place(x=200, y=60)

# ── player label + number ──
player_label = tk.Label(char_frame, image=player_img, bg=BG_COLOR)
player_label.image = player_img
player_label.place(x=480, y=490)

# player number image (1 or 2)
player_num_display = tk.Label(char_frame, bg=BG_COLOR)
player_num_display.place(x=620, y=480)

# ── name input ──
name_var = tk.StringVar()
name_entry = tk.Entry(char_frame, textvariable=name_var, font=("Courier", 14),
                      bg="white", fg="#1a6ebd", relief="flat",
                      highlightthickness=2, highlightcolor="#1a6ebd",
                      highlightbackground="#a0c8f0", width=14)
name_entry.place(x=60, y=500)

# ── characters setup ──
CHAR_BASE_Y   = 220
CHAR_FLOAT_AMP   = 8
CHAR_FLOAT_SPEED = 0.04
CHAR_TICK_MS     = 30

chars_info = [
    {"name": "gumball",  "img": gumball_img,  "x": 80,  "base_w": 90,  "base_h": 124},
    {"name": "darwin",   "img": darwin_img,   "x": 230, "base_w": 90,  "base_h": 111},
    {"name": "elsa",     "img": elsa_img,     "x": 390, "base_w": 90,  "base_h": 119},
    {"name": "iceking",  "img": iceking_img,  "x": 550, "base_w": 90,  "base_h": 100},
]

char_labels    = []
char_angles    = []
char_selected  = [False, False, False, False]
char_hovering  = [False, False, False, False]

# current player being assigned (0 = p1, 1 = p2)
current_player_turn = [0]
p1_char = [None]
p2_char = [None]

def make_char_label(i, info):
    lbl = tk.Label(char_frame, image=info["img"], bg=BG_COLOR, cursor="hand2")
    lbl.image = info["img"]
    lbl.place(x=info["x"], y=CHAR_BASE_Y)
    return lbl

for i, info in enumerate(chars_info):
    lbl = make_char_label(i, info)
    char_labels.append(lbl)
    char_angles.append(i * 0.8)

def select_char(i):
    name = chars_info[i]["name"]
    turn = current_player_turn[0]

    # deselect previously selected for this player
    for j in range(4):
        if turn == 0 and p1_char[0] == chars_info[j]["name"]:
            char_selected[j] = False
        elif turn == 1 and p2_char[0] == chars_info[j]["name"]:
            char_selected[j] = False

    char_selected[i] = True
    if turn == 0:
        p1_char[0] = name
    else:
        p2_char[0] = name

    # resize to big immediately
    info = chars_info[i]
    char_labels[i].place_configure(
        width=int(info["base_w"] * 1.3),
        height=int(info["base_h"] * 1.3),
        y=CHAR_BASE_Y - 10
    )

def on_char_enter(i):
    def handler(e):
        if not char_selected[i] and not char_hovering[i]:
            char_hovering[i] = True
            info = chars_info[i]
            char_labels[i].place_configure(
                width=int(info["base_w"] * 1.2),
                height=int(info["base_h"] * 1.2)
            )
    return handler

def on_char_leave(i):
    def handler(e):
        char_hovering[i] = False
        if not char_selected[i]:
            info = chars_info[i]
            char_labels[i].place_configure(
                width=info["base_w"],
                height=info["base_h"]
            )
    return handler

for i, lbl in enumerate(char_labels):
    lbl.bind("<Enter>",    on_char_enter(i))
    lbl.bind("<Leave>",    on_char_leave(i))
    lbl.bind("<Button-1>", lambda e, idx=i: select_char(idx))

# ── floating animation ──
char_anim_angles = [i * 0.8 for i in range(4)]

def animate_chars():
    for i, lbl in enumerate(char_labels):
        if not char_selected[i]:
            char_anim_angles[i] += CHAR_FLOAT_SPEED
            offset = int(CHAR_FLOAT_AMP * math.sin(char_anim_angles[i]))
            info = chars_info[i]
            lbl.place_configure(y=CHAR_BASE_Y + offset)
    char_frame.after(CHAR_TICK_MS, animate_chars)

animate_chars()

# ── player number display ──
def update_player_num():
    turn = current_player_turn[0]
    img = number_imgs_small["one"] if turn == 0 else number_imgs_small["two"]
    player_num_display.config(image=img)
    player_num_display.image = img

update_player_num()

# ── hover for top buttons ──
pause3_hovering = False
exit4_hovering  = False

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

pause_btn3.bind("<Enter>", on_pause3_enter)
pause_btn3.bind("<Leave>", on_pause3_leave)
exit_btn4.bind("<Enter>",  on_exit4_enter)
exit_btn4.bind("<Leave>",  on_exit4_leave)

# ── wire next_btn2 from rounds → char frame ──
next_btn2.bind("<Button-1>", lambda e: go_to_char_frame())

def go_to_char_frame():
    # reset selections
    for i in range(4):
        char_selected[i] = False
        char_hovering[i] = False
        info = chars_info[i]
        char_labels[i].place_configure(
            width=info["base_w"],
            height=info["base_h"],
            y=CHAR_BASE_Y
        )
    p1_char[0] = None
    p2_char[0] = None
    current_player_turn[0] = 0
    update_player_num()
    name_var.set("")
    show_frame(char_frame)

# ── Start ─────────────────────────────────────────────────
show_frame(home_frame)
root.mainloop()