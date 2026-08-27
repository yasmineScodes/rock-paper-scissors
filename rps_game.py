
import tkinter as tk
from tkinter import font as tkfont
import random   
import time
import math
import threading

# ── Optional pygame sound ──────────────────────────────────────
try:
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False

# ══════════════════════════════════════════════════════════════
#  COLOUR PALETTE  (pixel-art / retro feel)
# ══════════════════════════════════════════════════════════════
C = {
    "bg":        "#0d0d1a",   # near-black navy
    "panel":     "#1a1a2e",   # dark panel
    "card":      "#16213e",   # card bg
    "border":    "#0f3460",   # border accent
    "accent1":   "#e94560",   # hot pink / red
    "accent2":   "#53d8fb",   # cyan
    "accent3":   "#f5a623",   # amber
    "accent4":   "#7bed9f",   # mint green
    "txt":       "#e0e0e0",   # main text
    "txt_dim":   "#8888aa",   # dim text
    "btn":       "#0f3460",   # button bg
    "btn_hov":   "#e94560",   # button hover
    "btn_txt":   "#ffffff",
    "win":       "#f5a623",
    "lose":      "#e94560",
    "draw":      "#53d8fb",
    "overlay":   "#00000099",
}

# ══════════════════════════════════════════════════════════════
#  PIXEL-ART HAND SPRITES  (as canvas draw instructions)
# ══════════════════════════════════════════════════════════════
# Each sprite is a list of (x, y, w, h, colour) rectangles
# on a 64 × 64 grid, scaled at render time.

PIXEL_SIZE = 6   # px per "pixel" unit

SPRITES = {
    # ── ROCK ──────────────────────────────────────────────────
    "rock": [
        # Fist shape
        (20,30,24,4,"#c8a06e"),(18,26,28,6,"#c8a06e"),
        (16,22,30,6,"#c8a06e"),(18,18,26,6,"#c8a06e"),
        (20,14,22,6,"#c8a06e"),(20,10, 8,6,"#c8a06e"),
        (28,10, 8,6,"#c8a06e"),(36,10, 6,6,"#c8a06e"),
        # Knuckle line
        (20,22,30,2,"#a0784e"),
        # Outline shadow
        (16,34,32,4,"#a0784e"),(14,20,4,16,"#a0784e"),
        (46,20,4,16,"#a0784e"),
    ],
    # ── PAPER ─────────────────────────────────────────────────
    "paper": [
        # Palm
        (20,32,24,14,"#c8a06e"),(18,28,28,6,"#c8a06e"),
        # Fingers
        (20,8,6,22,"#c8a06e"),(28,6,6,24,"#c8a06e"),
        (36,8,6,22,"#c8a06e"),(44,10,6,20,"#c8a06e"),
        (14,14,6,18,"#c8a06e"),
        # Shadows
        (20,44,24,4,"#a0784e"),(14,12,4,20,"#a0784e"),
    ],
    # ── SCISSORS ──────────────────────────────────────────────
    "scissors": [
        # Palm
        (20,34,24,12,"#c8a06e"),(18,28,28,8,"#c8a06e"),
        # Two extended fingers
        (22,8,6,22,"#c8a06e"),(34,8,6,22,"#c8a06e"),
        # Closed fingers
        (14,18,6,16,"#c8a06e"),(46,18,6,14,"#c8a06e"),
        # V gap between scissors fingers
        (28,14,6,8,"#0d0d1a"),
        # Shadows
        (20,44,24,4,"#a0784e"),
    ],
    # ── NEUTRAL / WAITING ─────────────────────────────────────
    "neutral": [
        (20,32,24,14,"#c8a06e"),(18,28,28,6,"#c8a06e"),
        (20,10,6,20,"#c8a06e"),(28,10,6,20,"#c8a06e"),
        (36,10,6,20,"#c8a06e"),(44,12,6,18,"#c8a06e"),
        (14,14,6,18,"#c8a06e"),
        (20,44,24,4,"#a0784e"),(14,12,4,20,"#a0784e"),
    ],
}

SPRITE_COLOURS = {
    "rock":     "#e94560",
    "paper":    "#53d8fb",
    "scissors": "#f5a623",
    "neutral":  "#8888aa",
}

# ══════════════════════════════════════════════════════════════
#  AVATAR PIXEL DATA  (8×8 faces, scaled up)
# ══════════════════════════════════════════════════════════════
AVATAR_PIXELS = {
    "🐉 Dragon": {
        "normal": [
            "..RRRR..",
            ".R.RR.R.",
            "RYYRRYYР",
            "R.RRRR.R",
            ".RRRRRR.",
            "..RBBR..",
            ".RB..BR.",
            "..RRRR..",
        ],
        "happy": [
            "..RRRR..",
            ".R.RR.R.",
            "RYYRRYYР",
            "R^RRRR^R",
            ".RRRRRR.",
            "..RWWR..",
            ".RW^^WR.",
            "..RRRR..",
        ],
        "sad": [
            "..RRRR..",
            ".R.RR.R.",
            "RyyRRyyR",
            "R.RRRR.R",
            ".RRRRRR.",
            "..RbbR..",
            ".Rb..bR.",
            "..RRRR..",
        ],
        "colors": {"R":"#e94560","Y":"#f5a623","B":"#53d8fb","W":"#ffffff",
                   "y":"#c8a06e","b":"#336699","^":"#ff9900",".":""},
    },
    "🤖 Robot": {
        "normal": [
            ".BBBBBB.",
            "B.BBBB.B",
            "BCCBBCCB",
            "B.BBBB.B",
            ".BBBBBB.",
            ".B.BB.B.",
            ".BBBBBB.",
            "..BBBB..",
        ],
        "happy": [
            ".BBBBBB.",
            "B.BBBB.B",
            "BGGBBGGB",
            "B^BBBB^B",
            ".BBBBBB.",
            ".BWWWWB.",
            ".BBBBBB.",
            "..BBBB..",
        ],
        "sad": [
            ".BBBBBB.",
            "B.BBBB.B",
            "BrrBBrrB",
            "B.BBBB.B",
            ".BBBBBB.",
            ".Bvvvv B.",
            ".BBBBBB.",
            "..BBBB..",
        ],
        "colors": {"B":"#0f3460","C":"#53d8fb","G":"#7bed9f","W":"#ffffff",
                   "r":"#e94560","v":"#a0a0c0","^":"#f5a623",".":""},
    },
    "🧙 Wizard": {
        "normal": [
            "..PPPP..",
            ".PPPPPP.",
            "PPwwwwPP",
            "Pw.ww.wP",
            "PwwwwwwP",
            ".Pw..wP.",
            ".PwwwwP.",
            "..PPPP..",
        ],
        "happy": [
            "..PPPP..",
            ".PPPPPP.",
            "PPwwwwPP",
            "Pw^ww^wP",
            "PwwwwwwP",
            ".PwWWwP.",
            ".PwwwwP.",
            "..PPPP..",
        ],
        "sad": [
            "..PPPP..",
            ".PPPPPP.",
            "PPwwwwPP",
            "Pw.ww.wP",
            "PwwwwwwP",
            ".Pw..wP.",
            ".P_ww_P.",
            "..PPPP..",
        ],
        "colors": {"P":"#7c3aed","w":"#f5deb3","W":"#ffffff","^":"#000000",
                   "_":"#666688",".":""},
    },
    "🦊 Fox": {
        "normal": [
            ".OO..OO.",
            "OOOOOOOO",
            "OWO..OWO",
            "O..OO..O",
            ".OOOOOO.",
            "..OWWO..",
            ".OO..OO.",
            "..OOOO..",
        ],
        "happy": [
            ".OO..OO.",
            "OOOOOOOO",
            "OWO..OWO",
            "O^.OO.^O",
            ".OOOOOO.",
            "..OWWWO.",
            ".OO..OO.",
            "..OOOO..",
        ],
        "sad": [
            ".OO..OO.",
            "OOOOOOOO",
            "OWO..OWO",
            "O..OO..O",
            ".OOOOOO.",
            "..O__O..",
            ".OO..OO.",
            "..OOOO..",
        ],
        "colors": {"O":"#f5a623","W":"#ffffff","^":"#000000","_":"#996633",".":""},
    },
    "🐱 Cat": {
        "normal": [
            "GG....GG",
            "GGGGGGGG",
            "G.GGG.GG",   # eyes
            "GGGGGGGG",
            ".GGGGGG.",
            "..GWWG..",
            ".GG..GG.",
            "..GGGG..",
        ],
        "happy": [
            "GG....GG",
            "GGGGGGGG",
            "G^GGG^GG",
            "GGGGGGGG",
            ".GGGGGG.",
            "..GVVG..",
            ".GG..GG.",
            "..GGGG..",
        ],
        "sad": [
            "GG....GG",
            "GGGGGGGG",
            "G.GGG.GG",
            "GGGGGGGG",
            ".GGGGGG.",
            "..G__G..",
            ".GG..GG.",
            "..GGGG..",
        ],
        "colors": {"G":"#888888","W":"#ffffff","^":"#000000","V":"#ff9999",
                   "v":"#ffaaaa","_":"#555566",".":""},
    },
    "👾 Alien": {
        "normal": [
            ".GGGGGG.",
            "GGGGGGGG",
            "GYYGGYYG",
            "G.GGGG.G",
            ".GGGGGG.",
            ".G.GG.G.",
            "GG.GG.GG",
            "G......G",
        ],
        "happy": [
            ".GGGGGG.",
            "GGGGGGGG",
            "GYYGGYYG",
            "G^GGGG^G",
            ".GGGGGG.",
            ".GWWWWG.",
            "GG.GG.GG",
            "G......G",
        ],
        "sad": [
            ".GGGGGG.",
            "GGGGGGGG",
            "GyyGGyyG",
            "G.GGGG.G",
            ".GGGGGG.",
            ".G.GG.G.",
            "GG.GG.GG",
            "G......G",
        ],
        "colors": {"G":"#7bed9f","Y":"#ffffff","y":"#aaffaa","W":"#ffffff",
                   "^":"#000000",".":""},
    },
}
AVATARS = list(AVATAR_PIXELS.keys())

# ══════════════════════════════════════════════════════════════
#  SOUND  (generated via pygame if available)
# ══════════════════════════════════════════════════════════════

def _gen_tone(freq, duration_ms, volume=0.4, wave="sine"):
    """Generate a simple synthesised tone as a pygame Sound."""
    if not PYGAME_AVAILABLE:
        return None
    import array, math as _m
    rate = 22050
    n = int(rate * duration_ms / 1000)
    buf = array.array("h")
    for i in range(n):
        t = i / rate
        if wave == "sine":
            v = _m.sin(2 * _m.pi * freq * t)
        elif wave == "square":
            v = 1.0 if _m.sin(2 * _m.pi * freq * t) > 0 else -1.0
        else:
            v = (2 * ((freq * t) % 1) - 1)
        fade = min(1.0, min(i, n - i) / (rate * 0.01))
        buf.append(int(v * volume * 32767 * fade))
    # stereo
    stereo = array.array("h")
    for s in buf:
        stereo.append(s)
        stereo.append(s)
    snd = pygame.sndarray.make_sound(
        __import__("numpy").array(stereo, dtype=__import__("numpy").int16).reshape(-1, 2)
    )
    return snd


class SoundManager:
    def __init__(self):
        self.enabled = True
        self.volume = 0.6
        self._sounds = {}
        self._music_playing = False
        self._build_sounds()

    def _build_sounds(self):
        if not PYGAME_AVAILABLE:
            return
        try:
            import numpy as np
            rate = 22050

            def tone(freq, ms, vol=0.4, wave="sine"):
                n = int(rate * ms / 1000)
                t = np.linspace(0, ms / 1000, n, False)
                if wave == "sine":
                    s = np.sin(2 * np.pi * freq * t)
                elif wave == "square":
                    s = np.sign(np.sin(2 * np.pi * freq * t))
                else:
                    s = 2 * ((freq * t) % 1) - 1
                fade = np.minimum(np.arange(n), np.arange(n, 0, -1))
                fade = np.minimum(fade / (rate * 0.01), 1.0)
                s = (s * fade * vol * 32767).astype(np.int16)
                stereo = np.stack([s, s], axis=1)
                return pygame.sndarray.make_sound(stereo)

            self._sounds["click"]    = tone(440, 80,  0.3, "square")
            self._sounds["rock"]     = tone(180, 200, 0.5, "square")
            self._sounds["paper"]    = tone(320, 150, 0.4, "sine")
            self._sounds["scissors"] = tone(600, 120, 0.4, "sine")
            self._sounds["win"]      = tone(523, 400, 0.5, "sine")
            self._sounds["lose"]     = tone(220, 500, 0.4, "square")
            self._sounds["draw"]     = tone(380, 300, 0.4, "sine")
            self._sounds["countdown"]= tone(880, 100, 0.4, "square")
            self._sounds["shoot"]    = tone(1046,250, 0.5, "square")
            self._sounds["game_win"] = tone(784, 600, 0.6, "sine")
        except Exception:
            pass

    def play(self, name):
        if not self.enabled or not PYGAME_AVAILABLE:
            return
        snd = self._sounds.get(name)
        if snd:
            snd.set_volume(self.volume)
            snd.play()

    def start_music(self):
        pass   # procedural music omitted for portability

    def stop_music(self):
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass


SOUNDS = SoundManager()

# ══════════════════════════════════════════════════════════════
#  GAME LOGIC
# ══════════════════════════════════════════════════════════════
CHOICES = ["rock", "paper", "scissors"]
BEATS   = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
ICONS   = {"rock": "✊", "paper": "✋", "scissors": "✌️"}

def get_winner(a, b):
    """Return 'a', 'b', or 'draw'."""
    if a == b:
        return "draw"
    return "a" if BEATS[a] == b else "b"

DYNAMIC_PHRASES = {
    ("🤖 Robot", "🧙 Wizard"):  "Science vs Magic!",
    ("🐉 Dragon", "🦊 Fox"):    "Ancient rivals meet!",
    ("👾 Alien", "🤖 Robot"):   "Intergalactic duel!",
    ("🐱 Cat", "🐉 Dragon"):    "Brave kitty!",
}

def get_phrase(av1, av2):
    return (DYNAMIC_PHRASES.get((av1, av2)) or
            DYNAMIC_PHRASES.get((av2, av1)) or
            "Let the battle begin!")

# ══════════════════════════════════════════════════════════════
#  BASE FRAME
# ══════════════════════════════════════════════════════════════

class BaseFrame(tk.Frame):
    def __init__(self, master, app, **kw):
        super().__init__(master, bg=C["bg"], **kw)
        self.app = app

    # ── helpers ───────────────────────────────────────────────
    def label(self, parent, text, size=14, colour=None, bold=False, **kw):
        weight = "bold" if bold else "normal"
        f = tkfont.Font(family="Courier", size=size, weight=weight)
        return tk.Label(parent, text=text, font=f,
                        fg=colour or C["txt"], bg=C["bg"], **kw)

    def pixel_label(self, parent, text, size=18, colour=None, **kw):
        """Big pixelated heading."""
        f = tkfont.Font(family="Courier", size=size, weight="bold")
        return tk.Label(parent, text=text, font=f,
                        fg=colour or C["accent1"], bg=C["bg"], **kw)

    def btn(self, parent, text, cmd, width=16, colour=None):
        colour = colour or C["btn"]
        b = tk.Button(parent, text=text,
                      font=tkfont.Font(family="Courier", size=13, weight="bold"),
                      fg=C["btn_txt"], bg=colour, activebackground=C["btn_hov"],
                      activeforeground="#ffffff", relief="flat",
                      bd=0, padx=10, pady=6, width=width, cursor="hand2",
                      command=lambda: (SOUNDS.play("click"), cmd()))
        b.bind("<Enter>", lambda e: b.config(bg=C["btn_hov"]))
        b.bind("<Leave>", lambda e: b.config(bg=colour))
        return b

    def draw_avatar(self, canvas, avatar_key, state="normal", ox=0, oy=0, scale=4):
        data = AVATAR_PIXELS.get(avatar_key)
        if not data:
            return
        grid = data[state]
        colors = data["colors"]
        pw = scale
        for row_i, row in enumerate(grid):
            for col_i, ch in enumerate(row):
                col = colors.get(ch, "")
                if col:
                    x0 = ox + col_i * pw
                    y0 = oy + row_i * pw
                    canvas.create_rectangle(x0, y0, x0+pw, y0+pw,
                                            fill=col, outline="")

    def draw_hand(self, canvas, choice, ox=0, oy=0, scale=None, flip=False):
        scale = scale or PIXEL_SIZE
        rects = SPRITES.get(choice, SPRITES["neutral"])
        for (rx, ry, rw, rh, col) in rects:
            if flip:
                rx = 64 - rx - rw
            x0 = ox + rx * scale
            y0 = oy + ry * scale
            canvas.create_rectangle(x0, y0, x0+rw*scale, y0+rh*scale,
                                    fill=col, outline="")

    def top_bar(self, parent):
        """Small menu bar visible on game frames."""
        bar = tk.Frame(parent, bg=C["panel"], pady=4)
        bar.pack(fill="x", side="top")
        self.btn(bar, "🏠 Home",   self.app.go_home,   width=8,
                 colour=C["border"]).pack(side="left", padx=6)
        self.btn(bar, "🔁 Replay", self.app.replay,    width=8,
                 colour=C["border"]).pack(side="left", padx=2)
        self.btn(bar, "⏸ Pause",  self.app.pause,     width=8,
                 colour=C["border"]).pack(side="right", padx=6)
        self.btn(bar, "🚪 Exit",   self.app.root.quit, width=8,
                 colour=C["accent1"]).pack(side="right", padx=2)
        return bar

    def separator(self, parent, colour=None):
        tk.Frame(parent, bg=colour or C["border"], height=2).pack(
            fill="x", padx=20, pady=4)

# ══════════════════════════════════════════════════════════════
#  HOME FRAME
# ══════════════════════════════════════════════════════════════

class HomeFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._anim_offset = 0
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)

        # Title canvas
        self._title_canvas = tk.Canvas(self, bg=C["bg"], height=120,
                                       highlightthickness=0)
        self._title_canvas.grid(row=0, column=0, pady=(30, 0))
        self._draw_title()

        # Pixel hands row
        c = tk.Canvas(self, bg=C["bg"], width=260, height=80,
                      highlightthickness=0)
        c.grid(row=1, column=0, pady=10)
        self.draw_hand(c, "rock",     ox=0,   oy=8, scale=4)
        self.draw_hand(c, "paper",    ox=92,  oy=8, scale=4)
        self.draw_hand(c, "scissors", ox=184, oy=8, scale=4)

        tk.Frame(self, bg=C["bg"]).grid(row=2, column=0, pady=10)
        self.btn(self, "▶  START GAME", self.app.go_mode, width=20,
                 colour=C["accent1"]).grid(row=3, column=0, pady=6)
        self.btn(self, "⚙  SETTINGS",  self._settings, width=20,
                 colour=C["btn"]).grid(row=4, column=0, pady=6)
        self.btn(self, "🚪  EXIT",      self.app.root.quit, width=20,
                 colour=C["border"]).grid(row=5, column=0, pady=6)

        ver = self.label(self, "v1.0  ·  pixel edition", size=9,
                         colour=C["txt_dim"])
        ver.grid(row=6, column=0, pady=(20, 8))

        self._animate_title()

    def _draw_title(self):
        c = self._title_canvas
        c.delete("all")
        c.create_text(130, 30, text="ROCK PAPER",
                      font=tkfont.Font(family="Courier", size=26, weight="bold"),
                      fill=C["accent2"])
        c.create_text(130 + self._anim_offset, 75, text="SCISSORS",
                      font=tkfont.Font(family="Courier", size=30, weight="bold"),
                      fill=C["accent1"])
        c.create_text(130, 105, text="✊  ✋  ✌️",
                      font=tkfont.Font(family="Courier", size=18),
                      fill=C["accent3"])

    def _animate_title(self):
        self._anim_offset = int(4 * math.sin(time.time() * 2))
        self._draw_title()
        self.after(50, self._animate_title)

    def _settings(self):
        SettingsDialog(self, self.app)


# ══════════════════════════════════════════════════════════════
#  MODE SELECTION FRAME
# ══════════════════════════════════════════════════════════════

class ModeFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._mode = tk.StringVar(value="single")
        self._build()

    def _build(self):
        self.pixel_label(self, "SELECT MODE", size=22).pack(pady=(40, 20))
        self.separator(self)

        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=30)

        self._mk_card(row, "👤  SINGLE\nPLAYER", "single").pack(side="left", padx=20)
        self._mk_card(row, "👥  TWO\nPLAYER",   "multi" ).pack(side="left", padx=20)

        self.separator(self)
        nav = tk.Frame(self, bg=C["bg"])
        nav.pack(pady=20)
        self.btn(nav, "◀ BACK",  self.app.go_home,       colour=C["border"]).pack(side="left", padx=10)
        self.btn(nav, "NEXT ▶",  self._next,              colour=C["accent1"]).pack(side="left", padx=10)

    def _mk_card(self, parent, text, mode):
        colour = C["accent1"] if mode == "single" else C["accent2"]
        frame = tk.Frame(parent, bg=C["card"], bd=3,
                         relief="solid", cursor="hand2", width=160, height=160)
        frame.pack_propagate(False)
        lbl = tk.Label(frame, text=text,
                       font=tkfont.Font(family="Courier", size=14, weight="bold"),
                       fg=colour, bg=C["card"], justify="center")
        lbl.pack(expand=True)
        def select():
            SOUNDS.play("click")
            self._mode.set(mode)
            self._refresh_cards()
        frame.bind("<Button-1>", lambda e: select())
        lbl.bind("<Button-1>",   lambda e: select())
        self._cards = getattr(self, "_cards", {})
        self._cards[mode] = frame
        return frame

    def _refresh_cards(self):
        for mode, frame in self._cards.items():
            active = (self._mode.get() == mode)
            frame.config(bg=C["accent1"] if active else C["card"],
                         highlightbackground=C["accent1"] if active else C["border"])
        for w in self.winfo_children():
            pass   # labels inside cards update via re-select

    def _next(self):
        self.app.game_state["mode"] = self._mode.get()
        self.app.go_rounds()


# ══════════════════════════════════════════════════════════════
#  ROUNDS SELECTION FRAME
# ══════════════════════════════════════════════════════════════

class RoundsFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._rounds = tk.IntVar(value=3)
        self._build()

    def _build(self):
        self.pixel_label(self, "ROUNDS", size=22).pack(pady=(40, 10))
        self.label(self, "First to win majority of rounds wins!",
                   size=11, colour=C["txt_dim"]).pack()
        self.separator(self)

        ctrl = tk.Frame(self, bg=C["bg"])
        ctrl.pack(pady=30)

        tk.Button(ctrl, text="▼", font=tkfont.Font(family="Courier", size=18, weight="bold"),
                  fg=C["txt"], bg=C["btn"], activebackground=C["btn_hov"],
                  relief="flat", bd=0, padx=14, pady=4, cursor="hand2",
                  command=self._dec).pack(side="left", padx=10)

        self._num_lbl = tk.Label(ctrl,
                                 textvariable=self._rounds,
                                 font=tkfont.Font(family="Courier", size=42, weight="bold"),
                                 fg=C["accent3"], bg=C["bg"], width=3)
        self._num_lbl.pack(side="left")

        tk.Button(ctrl, text="▲", font=tkfont.Font(family="Courier", size=18, weight="bold"),
                  fg=C["txt"], bg=C["btn"], activebackground=C["btn_hov"],
                  relief="flat", bd=0, padx=14, pady=4, cursor="hand2",
                  command=self._inc).pack(side="left", padx=10)

        self.label(self, "(odd numbers, 1 – 21)", size=10,
                   colour=C["txt_dim"]).pack()
        self.separator(self)
        nav = tk.Frame(self, bg=C["bg"])
        nav.pack(pady=20)
        self.btn(nav, "◀ BACK", self.app.go_mode,   colour=C["border"]).pack(side="left", padx=10)
        self.btn(nav, "NEXT ▶", self._next,          colour=C["accent1"]).pack(side="left", padx=10)

    def _inc(self):
        SOUNDS.play("click")
        v = self._rounds.get()
        if v < 21:
            self._rounds.set(v + 2)

    def _dec(self):
        SOUNDS.play("click")
        v = self._rounds.get()
        if v > 1:
            self._rounds.set(v - 2)

    def _next(self):
        self.app.game_state["total_rounds"] = self._rounds.get()
        self.app.go_avatar()


# ══════════════════════════════════════════════════════════════
#  AVATAR / NAME SELECTION FRAME
# ══════════════════════════════════════════════════════════════

class AvatarFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._build()

    def _build(self):
        mode = self.app.game_state.get("mode", "single")
        players = 1 if mode == "single" else 2

        self.pixel_label(self, "PLAYER SETUP", size=20).pack(pady=(30, 10))
        self.separator(self)

        self._p_frames = []
        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=10, fill="x")

        for i in range(players):
            pf = self._player_panel(row, i)
            pf.pack(side="left", expand=True, padx=20)
            self._p_frames.append(pf)

        self.separator(self)
        nav = tk.Frame(self, bg=C["bg"])
        nav.pack(pady=20)
        self.btn(nav, "◀ BACK", self.app.go_rounds, colour=C["border"]).pack(side="left", padx=10)
        self.btn(nav, "NEXT ▶", self._next,          colour=C["accent1"]).pack(side="left", padx=10)

    def _player_panel(self, parent, idx):
        colours = [C["accent1"], C["accent2"]]
        frame = tk.Frame(parent, bg=C["card"], padx=16, pady=16,
                         bd=2, relief="solid")
        self.label(frame, f"PLAYER {idx+1}", size=13, bold=True,
                   colour=colours[idx]).pack()

        # Name entry
        name_var = tk.StringVar(value=f"Player{idx+1}")
        tk.Entry(frame, textvariable=name_var,
                 font=tkfont.Font(family="Courier", size=12),
                 fg=C["txt"], bg=C["panel"], insertbackground=C["txt"],
                 relief="flat", bd=4, width=14).pack(pady=8)

        # Avatar preview canvas
        av_canvas = tk.Canvas(frame, bg=C["card"], width=64, height=64,
                              highlightthickness=0)
        av_canvas.pack(pady=6)

        av_var = tk.StringVar(value=AVATARS[idx % len(AVATARS)])

        def refresh_av(*_):
            av_canvas.delete("all")
            self.draw_avatar(av_canvas, av_var.get(), scale=8)

        av_var.trace_add("write", refresh_av)

        # Prev / next avatar buttons
        nav_row = tk.Frame(frame, bg=C["card"])
        nav_row.pack()

        def prev_av():
            SOUNDS.play("click")
            cur = AVATARS.index(av_var.get())
            av_var.set(AVATARS[(cur - 1) % len(AVATARS)])
        def next_av():
            SOUNDS.play("click")
            cur = AVATARS.index(av_var.get())
            av_var.set(AVATARS[(cur + 1) % len(AVATARS)])

        tk.Button(nav_row, text="◀", font=tkfont.Font(family="Courier", size=11),
                  fg=C["txt"], bg=C["btn"], relief="flat", bd=0, padx=8,
                  cursor="hand2", command=prev_av).pack(side="left")
        self._av_name_lbl = tk.Label(nav_row, textvariable=av_var,
                                     font=tkfont.Font(family="Courier", size=9),
                                     fg=C["txt_dim"], bg=C["card"], width=12)
        self._av_name_lbl.pack(side="left")
        tk.Button(nav_row, text="▶", font=tkfont.Font(family="Courier", size=11),
                  fg=C["txt"], bg=C["btn"], relief="flat", bd=0, padx=8,
                  cursor="hand2", command=next_av).pack(side="left")

        refresh_av()
        frame._name_var = name_var
        frame._av_var   = av_var
        return frame

    def _next(self):
        gs = self.app.game_state
        gs["p1_name"]   = self._p_frames[0]._name_var.get() or "Player1"
        gs["p1_avatar"] = self._p_frames[0]._av_var.get()
        if gs["mode"] == "multi":
            gs["p2_name"]   = self._p_frames[1]._name_var.get() or "Player2"
            gs["p2_avatar"] = self._p_frames[1]._av_var.get()
        else:
            gs["p2_name"]   = "Computer"
            used = gs["p1_avatar"]
            choices = [a for a in AVATARS if a != used]
            gs["p2_avatar"] = random.choice(choices)
        self.app.go_vs()


# ══════════════════════════════════════════════════════════════
#  VS / INTRODUCTION FRAME
# ══════════════════════════════════════════════════════════════

class VSFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._build()

    def _build(self):
        gs = self.app.game_state
        self.pixel_label(self, "GET READY!", size=20).pack(pady=(30, 6))
        self.separator(self)

        arena = tk.Frame(self, bg=C["bg"])
        arena.pack(pady=20)

        # Player 1
        p1 = tk.Frame(arena, bg=C["bg"])
        p1.pack(side="left", padx=20)
        c1 = tk.Canvas(p1, bg=C["bg"], width=64, height=64, highlightthickness=0)
        c1.pack()
        self.draw_avatar(c1, gs["p1_avatar"], scale=8)
        self.label(p1, gs["p1_name"], size=13, bold=True,
                   colour=C["accent1"]).pack()

        # VS
        vs_f = tk.Frame(arena, bg=C["bg"])
        vs_f.pack(side="left", padx=30)
        self.pixel_label(vs_f, "VS", size=36, colour=C["accent3"]).pack()

        # Player 2
        p2 = tk.Frame(arena, bg=C["bg"])
        p2.pack(side="left", padx=20)
        c2 = tk.Canvas(p2, bg=C["bg"], width=64, height=64, highlightthickness=0)
        c2.pack()
        self.draw_avatar(c2, gs["p2_avatar"], scale=8)
        self.label(p2, gs["p2_name"], size=13, bold=True,
                   colour=C["accent2"]).pack()

        self.separator(self)
        phrase = get_phrase(gs["p1_avatar"], gs["p2_avatar"])
        self.label(self, phrase, size=13, colour=C["accent3"], bold=True).pack(pady=10)

        total = gs["total_rounds"]
        self.label(self, f"Best of {total} rounds  ·  First to {total//2+1} wins",
                   size=11, colour=C["txt_dim"]).pack()

        self.btn(self, "▶ FIGHT!", self.app.go_game, colour=C["accent1"],
                 width=18).pack(pady=30)


# ══════════════════════════════════════════════════════════════
#  GAMEPLAY FRAME
# ══════════════════════════════════════════════════════════════

class GameplayFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._build()

    def _build(self):
        self.top_bar(self)
        gs = self.app.game_state

        # Score bar
        score_row = tk.Frame(self, bg=C["panel"], pady=6)
        score_row.pack(fill="x")
        self._p1_score_lbl = tk.Label(
            score_row,
            text=f"{gs['p1_name']}  {gs['p1_score']}",
            font=tkfont.Font(family="Courier", size=14, weight="bold"),
            fg=C["accent1"], bg=C["panel"])
        self._p1_score_lbl.pack(side="left", padx=20)
        tk.Label(score_row, text="vs",
                 font=tkfont.Font(family="Courier", size=12),
                 fg=C["txt_dim"], bg=C["panel"]).pack(side="left")
        self._p2_score_lbl = tk.Label(
            score_row,
            text=f"{gs['p2_score']}  {gs['p2_name']}",
            font=tkfont.Font(family="Courier", size=14, weight="bold"),
            fg=C["accent2"], bg=C["panel"])
        self._p2_score_lbl.pack(side="right", padx=20)

        self._round_lbl = tk.Label(score_row,
            text=f"Round {gs['current_round']+1} / {gs['total_rounds']}",
            font=tkfont.Font(family="Courier", size=11),
            fg=C["txt_dim"], bg=C["panel"])
        self._round_lbl.pack(side="left", padx=20)

        # Whose turn?
        self._turn_lbl = self.pixel_label(self, "", size=18, colour=C["accent3"])
        self._turn_lbl.pack(pady=(16, 4))

        # Hand canvas
        self._hand_canvas = tk.Canvas(self, bg=C["bg"], width=320, height=200,
                                      highlightthickness=0)
        self._hand_canvas.pack(pady=6)

        self._status_lbl = self.label(self, "Make your choice!", size=12,
                                      colour=C["txt_dim"])
        self._status_lbl.pack()

        # Choice buttons
        btn_row = tk.Frame(self, bg=C["bg"])
        btn_row.pack(pady=20)
        for ch in CHOICES:
            self._choice_btn(btn_row, ch).pack(side="left", padx=10)

        self._buttons_frame = btn_row
        self._refresh()

    def _choice_btn(self, parent, choice):
        icon = ICONS[choice]
        col  = SPRITE_COLOURS[choice]
        b = tk.Button(parent,
                      text=f"{icon}\n{choice.upper()}",
                      font=tkfont.Font(family="Courier", size=13, weight="bold"),
                      fg=col, bg=C["card"], activebackground=col,
                      activeforeground=C["bg"], relief="flat", bd=0,
                      padx=16, pady=10, width=8, cursor="hand2",
                      command=lambda c=choice: self._on_choice(c))
        b.bind("<Enter>", lambda e, b=b, c=col: b.config(bg=c, fg=C["bg"]))
        b.bind("<Leave>", lambda e, b=b, c=col: b.config(bg=C["card"], fg=c))
        return b

    def _refresh(self):
        gs = self.app.game_state
        mode = gs["mode"]
        # In single-player mode p1 always goes first; in multi-player alternate
        if mode == "multi":
            whose = gs.get("whose_turn", 1)
            if whose == 1:
                name = gs["p1_name"]
                col  = C["accent1"]
            else:
                name = gs["p2_name"]
                col  = C["accent2"]
        else:
            name = gs["p1_name"]
            col  = C["accent1"]
        self._turn_lbl.config(text=f"{name}'s Turn", fg=col)
        self._update_hand("neutral")

        # score
        self._p1_score_lbl.config(
            text=f"{gs['p1_name']}  {gs['p1_score']}")
        self._p2_score_lbl.config(
            text=f"{gs['p2_score']}  {gs['p2_name']}")
        self._round_lbl.config(
            text=f"Round {gs['current_round']+1} / {gs['total_rounds']}")
        self._status_lbl.config(text="Make your choice!")
        self._set_buttons_state("normal")

    def _update_hand(self, choice, flip=False):
        c = self._hand_canvas
        c.delete("all")
        scale = 5
        aw = 64 * scale
        cx = 160
        self.draw_hand(c, choice, ox=cx - aw//2, oy=10, scale=scale, flip=flip)

    def _set_buttons_state(self, state):
        for w in self._buttons_frame.winfo_children():
            w.config(state=state)

    def _on_choice(self, choice):
        gs = self.app.game_state
        SOUNDS.play(choice)
        self._update_hand(choice)
        self._set_buttons_state("disabled")

        if gs["mode"] == "single":
            gs["p1_choice"] = choice
            self._status_lbl.config(text="Computer is choosing…", fg=C["txt_dim"])
            self.after(900, self._computer_choose)
        else:
            whose = gs.get("whose_turn", 1)
            if whose == 1:
                gs["p1_choice"] = choice
                gs["whose_turn"] = 2
                self.after(600, self._refresh)
            else:
                gs["p2_choice"] = choice
                gs["whose_turn"] = 1
                self.after(400, self.app.go_round_anim)

    def _computer_choose(self):
        gs = self.app.game_state
        gs["p2_choice"] = random.choice(CHOICES)
        self.app.go_round_anim()

    def activate(self):
        """Called when frame is shown."""
        self.app.game_state.setdefault("whose_turn", 1)
        self._refresh()


# ══════════════════════════════════════════════════════════════
#  ROUND ANIMATION FRAME  (Rock → Paper → Scissors → Shoot)
# ══════════════════════════════════════════════════════════════

class RoundAnimFrame(BaseFrame):
    STEPS = ["ROCK…", "PAPER…", "SCISSORS…", "✊✋✌️  SHOOT!"]
    STEP_CHOICES = ["rock", "paper", "scissors", None]

    def __init__(self, master, app):
        super().__init__(master, app)
        self._build()
        self._step = 0
        self._bob  = 0

    def _build(self):
        self._countdown_lbl = self.pixel_label(self, "ROCK…", size=28,
                                               colour=C["accent3"])
        self._countdown_lbl.pack(pady=(40, 10))

        self._hand_canvas = tk.Canvas(self, bg=C["bg"], width=400, height=240,
                                      highlightthickness=0)
        self._hand_canvas.pack(pady=10)

    def activate(self):
        self._step = 0
        self._animate()

    def _animate(self):
        gs  = self.app.game_state
        c   = self._hand_canvas
        step = self._step

        if step >= len(self.STEPS):
            # Show final choices then go to result
            self._show_final()
            return

        label = self.STEPS[step]
        self._countdown_lbl.config(text=label)
        SOUNDS.play("countdown" if step < 3 else "shoot")

        c.delete("all")
        bob = int(10 * math.sin(time.time() * 8))
        choice = self.STEP_CHOICES[step] or "neutral"
        scale = 5
        aw = 64 * scale
        # left hand (p1)
        self.draw_hand(c, choice, ox=20, oy=40 + bob, scale=scale)
        # right hand (p2) flipped
        self.draw_hand(c, choice, ox=400-aw-20, oy=40 - bob,
                       scale=scale, flip=True)

        self._step += 1
        self.after(700, self._animate)

    def _show_final(self):
        gs = self.app.game_state
        p1c = gs["p1_choice"]
        p2c = gs["p2_choice"]
        self._countdown_lbl.config(text="SHOOT!", fg=C["accent1"])
        c = self._hand_canvas
        c.delete("all")
        scale = 5
        aw = 64 * scale
        self.draw_hand(c, p1c, ox=20,          oy=40, scale=scale)
        self.draw_hand(c, p2c, ox=400-aw-20,   oy=40, scale=scale, flip=True)
        # labels
        c.create_text(20 + aw//2, 200,
                      text=f"{ICONS[p1c]} {p1c.upper()}",
                      font=tkfont.Font(family="Courier", size=14, weight="bold"),
                      fill=SPRITE_COLOURS[p1c])
        c.create_text(400 - aw//2 - 20, 200,
                      text=f"{p2c.upper()} {ICONS[p2c]}",
                      font=tkfont.Font(family="Courier", size=14, weight="bold"),
                      fill=SPRITE_COLOURS[p2c])
        self.after(1400, self.app.go_round_result)


# ══════════════════════════════════════════════════════════════
#  ROUND RESULT FRAME
# ══════════════════════════════════════════════════════════════

class RoundResultFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._build()

    def _build(self):
        self._result_lbl = self.pixel_label(self, "", size=26)
        self._result_lbl.pack(pady=(30, 10))

        arena = tk.Frame(self, bg=C["bg"])
        arena.pack(pady=10)

        self._c1 = tk.Canvas(arena, bg=C["bg"], width=80, height=80, highlightthickness=0)
        self._c1.pack(side="left", padx=20)
        self._n1 = self.label(arena, "", size=12, colour=C["accent1"])
        self._n1.pack(side="left")

        self.pixel_label(arena, "VS", size=16, colour=C["txt_dim"]).pack(side="left", padx=10)

        self._n2 = self.label(arena, "", size=12, colour=C["accent2"])
        self._n2.pack(side="left")
        self._c2 = tk.Canvas(arena, bg=C["bg"], width=80, height=80, highlightthickness=0)
        self._c2.pack(side="left", padx=20)

        self._score_lbl = self.label(self, "", size=13, colour=C["txt_dim"])
        self._score_lbl.pack(pady=8)

        self._next_lbl = self.label(self, "", size=11, colour=C["txt_dim"])
        self._next_lbl.pack()

    def activate(self):
        gs = self.app.game_state
        p1c = gs["p1_choice"]
        p2c = gs["p2_choice"]
        winner = get_winner(p1c, p2c)

        if winner == "draw":
            SOUNDS.play("draw")
            result_txt = "✦ DRAW! ✦"
            result_col = C["draw"]
            p1_state, p2_state = "normal", "normal"
        elif winner == "a":
            SOUNDS.play("win")
            gs["p1_score"] += 1
            result_txt = f"🏆 {gs['p1_name']} wins!"
            result_col = C["win"]
            p1_state, p2_state = "happy", "sad"
        else:
            SOUNDS.play("lose")
            gs["p2_score"] += 1
            result_txt = f"🏆 {gs['p2_name']} wins!"
            result_col = C["accent2"]
            p1_state, p2_state = "sad", "happy"

        gs["current_round"] += 1

        self._result_lbl.config(text=result_txt, fg=result_col)
        self._n1.config(text=gs["p1_name"])
        self._n2.config(text=gs["p2_name"])

        self._c1.delete("all")
        self._c2.delete("all")
        self.draw_avatar(self._c1, gs["p1_avatar"], state=p1_state, scale=10)
        self.draw_avatar(self._c2, gs["p2_avatar"], state=p2_state, scale=10)

        need = gs["total_rounds"] // 2 + 1
        self._score_lbl.config(
            text=f"{gs['p1_name']} {gs['p1_score']}  :  "
                 f"{gs['p2_score']} {gs['p2_name']}  "
                 f"(need {need} to win)")

        # Check if game over
        if gs["p1_score"] >= need:
            gs["game_winner"] = "p1"
            self._next_lbl.config(text="🏆 Game decided! Loading…")
            self.after(2000, self.app.go_end)
        elif gs["p2_score"] >= need:
            gs["game_winner"] = "p2"
            self._next_lbl.config(text="🏆 Game decided! Loading…")
            self.after(2000, self.app.go_end)
        elif gs["current_round"] >= gs["total_rounds"]:
            # All rounds done, tally
            if gs["p1_score"] > gs["p2_score"]:
                gs["game_winner"] = "p1"
            elif gs["p2_score"] > gs["p1_score"]:
                gs["game_winner"] = "p2"
            else:
                gs["game_winner"] = "draw"
            self._next_lbl.config(text="Game over! Loading…")
            self.after(2000, self.app.go_end)
        else:
            self._next_lbl.config(text="Next round in 2 seconds…")
            self.after(2200, self.app.go_game)


# ══════════════════════════════════════════════════════════════
#  END GAME FRAME
# ══════════════════════════════════════════════════════════════

class EndFrame(BaseFrame):
    def __init__(self, master, app):
        super().__init__(master, app)
        self._confetti = []
        self._anim_id  = None
        self._build()

    def _build(self):
        self._canvas = tk.Canvas(self, bg=C["bg"], highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)

        # Overlay widgets
        self._title = self.pixel_label(self, "", size=24, colour=C["win"])
        self._title.place(relx=0.5, rely=0.12, anchor="center")

        self._sub = self.label(self, "", size=14, colour=C["txt"])
        self._sub.place(relx=0.5, rely=0.22, anchor="center")

        # Avatars
        self._c1 = tk.Canvas(self, bg=C["bg"], width=80, height=80,
                              highlightthickness=0)
        self._c1.place(relx=0.3, rely=0.38, anchor="center")
        self._c2 = tk.Canvas(self, bg=C["bg"], width=80, height=80,
                              highlightthickness=0)
        self._c2.place(relx=0.7, rely=0.38, anchor="center")

        self._score_lbl = self.label(self, "", size=13, colour=C["txt_dim"])
        self._score_lbl.place(relx=0.5, rely=0.55, anchor="center")

        btn_f = tk.Frame(self, bg=C["bg"])
        btn_f.place(relx=0.5, rely=0.72, anchor="center")
        self.btn(btn_f, "🔁 REPLAY",  self.app.replay,     colour=C["accent1"]).pack(side="left", padx=8)
        self.btn(btn_f, "🏠 HOME",    self.app.go_home,    colour=C["btn"]).pack(side="left", padx=8)
        self.btn(btn_f, "🚪 EXIT",    self.app.root.quit,  colour=C["border"]).pack(side="left", padx=8)

    def activate(self):
        gs = self.app.game_state
        gw = gs.get("game_winner", "draw")

        if gw == "p1":
            SOUNDS.play("game_win")
            winner_name = gs["p1_name"]
            self._title.config(text=f"🏆 {winner_name} WINS!", fg=C["win"])
            p1_state, p2_state = "happy", "sad"
        elif gw == "p2":
            SOUNDS.play("game_win")
            winner_name = gs["p2_name"]
            self._title.config(text=f"🏆 {winner_name} WINS!", fg=C["accent2"])
            p1_state, p2_state = "sad", "happy"
        else:
            winner_name = None
            self._title.config(text="✦ IT'S A DRAW! ✦", fg=C["draw"])
            p1_state, p2_state = "normal", "normal"

        self._sub.config(
            text=f"{gs['p1_name']} vs {gs['p2_name']}  ·  "
                 f"Best of {gs['total_rounds']}")
        self._score_lbl.config(
            text=f"Final Score:  {gs['p1_name']} {gs['p1_score']}  -  "
                 f"{gs['p2_score']} {gs['p2_name']}")

        self._c1.delete("all")
        self._c2.delete("all")
        self.draw_avatar(self._c1, gs["p1_avatar"], state=p1_state, scale=10)
        self.draw_avatar(self._c2, gs["p2_avatar"], state=p2_state, scale=10)

        self._start_confetti()

    def _start_confetti(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
        self._confetti = [
            {
                "x": random.randint(0, 700),
                "y": random.randint(-40, -4),
                "dy": random.uniform(2, 5),
                "dx": random.uniform(-1.5, 1.5),
                "col": random.choice([C["accent1"], C["accent2"],
                                       C["accent3"], C["accent4"],
                                       "#ffffff"]),
                "size": random.randint(4, 10),
            }
            for _ in range(60)
        ]
        self._animate_confetti()

    def _animate_confetti(self):
        c = self._canvas
        c.delete("confetti")
        for p in self._confetti:
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            if p["y"] > 600:
                p["y"] = random.randint(-20, 0)
                p["x"] = random.randint(0, 700)
            s = p["size"]
            c.create_rectangle(p["x"], p["y"], p["x"]+s, p["y"]+s,
                                fill=p["col"], outline="", tags="confetti")
        self._anim_id = self.after(30, self._animate_confetti)

    def deactivate(self):
        if self._anim_id:
            self.after_cancel(self._anim_id)
            self._anim_id = None


# ══════════════════════════════════════════════════════════════
#  SETTINGS DIALOG
# ══════════════════════════════════════════════════════════════

class SettingsDialog(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.title("Settings")
        self.configure(bg=C["bg"])
        self.resizable(False, False)
        self.grab_set()
        self._build()

    def _build(self):
        f = tkfont.Font(family="Courier", size=13, weight="bold")
        tk.Label(self, text="⚙ SETTINGS", font=f,
                 fg=C["accent2"], bg=C["bg"]).pack(pady=(20, 10))

        # Sound toggle
        row = tk.Frame(self, bg=C["bg"])
        row.pack(pady=6, padx=30, fill="x")
        tk.Label(row, text="Sound FX:", font=tkfont.Font(family="Courier", size=12),
                 fg=C["txt"], bg=C["bg"]).pack(side="left")
        self._snd_var = tk.BooleanVar(value=SOUNDS.enabled)
        tk.Checkbutton(row, variable=self._snd_var, bg=C["bg"],
                       fg=C["accent1"], selectcolor=C["panel"],
                       command=self._toggle_sound).pack(side="right")

        # Volume
        row2 = tk.Frame(self, bg=C["bg"])
        row2.pack(pady=6, padx=30, fill="x")
        tk.Label(row2, text="Volume:", font=tkfont.Font(family="Courier", size=12),
                 fg=C["txt"], bg=C["bg"]).pack(side="left")
        self._vol_var = tk.DoubleVar(value=SOUNDS.volume)
        tk.Scale(row2, from_=0.0, to=1.0, resolution=0.05,
                 orient="horizontal", variable=self._vol_var,
                 bg=C["panel"], fg=C["txt"], highlightthickness=0,
                 troughcolor=C["border"], activebackground=C["accent1"],
                 command=self._set_volume, length=140).pack(side="right")

        tk.Button(self, text="CLOSE",
                  font=tkfont.Font(family="Courier", size=12, weight="bold"),
                  fg=C["btn_txt"], bg=C["accent1"], relief="flat", bd=0,
                  padx=20, pady=6, cursor="hand2",
                  command=self.destroy).pack(pady=20)

    def _toggle_sound(self):
        SOUNDS.enabled = self._snd_var.get()

    def _set_volume(self, val):
        SOUNDS.volume = float(val)


# ══════════════════════════════════════════════════════════════
#  PAUSE OVERLAY
# ══════════════════════════════════════════════════════════════

class PauseOverlay(tk.Toplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.overrideredirect(True)
        self.attributes("-alpha", 0.88)
        self.configure(bg=C["bg"])

        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        w = parent.winfo_width()
        h = parent.winfo_height()
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grab_set()
        self._build()

    def _build(self):
        f = tk.Frame(self, bg=C["bg"])
        f.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(f, text="⏸  PAUSED",
                 font=tkfont.Font(family="Courier", size=28, weight="bold"),
                 fg=C["accent3"], bg=C["bg"]).pack(pady=(0, 20))

        def btn(txt, cmd, col=None):
            b = tk.Button(f, text=txt,
                          font=tkfont.Font(family="Courier", size=14, weight="bold"),
                          fg=C["btn_txt"], bg=col or C["btn"],
                          activebackground=C["btn_hov"],
                          relief="flat", bd=0, padx=20, pady=8, width=16,
                          cursor="hand2", command=lambda: (SOUNDS.play("click"), cmd()))
            b.pack(pady=6)

        btn("▶  RESUME",  self.destroy)
        btn("🔁  REPLAY", lambda: (self.destroy(), self.app.replay()))
        btn("🏠  HOME",   lambda: (self.destroy(), self.app.go_home()))
        btn("⚙  SETTINGS",lambda: SettingsDialog(self, self.app))
        btn("🚪  EXIT",   self.app.root.quit, col=C["accent1"])


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════

class App:
    WIDTH  = 700
    HEIGHT = 580

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rock Paper Scissors  ✊ ✋ ✌️")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)
        self.root.configure(bg=C["bg"])

        # Try to set a pixel-art-ish icon (ignore if no icon file)
        try:
            self.root.iconbitmap("icon.ico")
        except Exception:
            pass

        self.game_state = {}
        self._frames    = {}
        self._current   = None

        self._init_frames()
        self.show("home")
        self.root.mainloop()

    # ── Frame management ──────────────────────────────────────
    def _init_frames(self):
        container = tk.Frame(self.root, bg=C["bg"])
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame_classes = {
            "home":         HomeFrame,
            "mode":         ModeFrame,
            "rounds":       RoundsFrame,
            "avatar":       AvatarFrame,
            "vs":           VSFrame,
            "game":         GameplayFrame,
            "round_anim":   RoundAnimFrame,
            "round_result": RoundResultFrame,
            "end":          EndFrame,
        }
        for name, cls in frame_classes.items():
            f = cls(container, self)
            f.grid(row=0, column=0, sticky="nsew")
            self._frames[name] = f

    def show(self, name):
        if self._current == "end":
            self._frames["end"].deactivate()
        frame = self._frames[name]
        frame.tkraise()
        self._current = name
        # Call activate() if defined
        if hasattr(frame, "activate"):
            frame.activate()

    # ── Navigation helpers ────────────────────────────────────
    def go_home(self):
        self._reset_game_state()
        self.show("home")

    def go_mode(self):
        # Rebuild mode frame for clean state
        self._frames["mode"].destroy()
        from types import SimpleNamespace
        # Rebuild in container
        container = self._frames["home"].master
        f = ModeFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["mode"] = f
        self.show("mode")

    def go_rounds(self):
        container = self._frames["home"].master
        f = RoundsFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["rounds"] = f
        self.show("rounds")

    def go_avatar(self):
        container = self._frames["home"].master
        f = AvatarFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["avatar"] = f
        self.show("avatar")

    def go_vs(self):
        container = self._frames["home"].master
        f = VSFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["vs"] = f
        self.show("vs")

    def go_game(self):
        self.game_state.setdefault("whose_turn", 1)
        container = self._frames["home"].master
        f = GameplayFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["game"] = f
        self.show("game")

    def go_round_anim(self):
        container = self._frames["home"].master
        f = RoundAnimFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["round_anim"] = f
        self.show("round_anim")

    def go_round_result(self):
        container = self._frames["home"].master
        f = RoundResultFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["round_result"] = f
        self.show("round_result")

    def go_end(self):
        container = self._frames["home"].master
        f = EndFrame(container, self)
        f.grid(row=0, column=0, sticky="nsew")
        self._frames["end"] = f
        self.show("end")

    def replay(self):
        """Replay with same settings."""
        gs = self.game_state
        saved = {
            "mode":         gs.get("mode", "single"),
            "total_rounds": gs.get("total_rounds", 3),
            "p1_name":      gs.get("p1_name", "Player1"),
            "p1_avatar":    gs.get("p1_avatar", AVATARS[0]),
            "p2_name":      gs.get("p2_name", "Computer"),
            "p2_avatar":    gs.get("p2_avatar", AVATARS[1]),
        }
        self._reset_game_state()
        self.game_state.update(saved)
        self.go_vs()

    def pause(self):
        PauseOverlay(self.root, self)

    def _reset_game_state(self):
        self.game_state = {
            "mode":          "single",
            "total_rounds":  3,
            "current_round": 0,
            "p1_score":      0,
            "p2_score":      0,
            "p1_name":       "Player1",
            "p2_name":       "Computer",
            "p1_avatar":     AVATARS[0],
            "p2_avatar":     AVATARS[1],
            "p1_choice":     None,
            "p2_choice":     None,
            "whose_turn":    1,
            "game_winner":   None,
        }


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    App()