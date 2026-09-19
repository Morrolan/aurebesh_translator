#!/usr/bin/env python3
"""
Aurebesh Translator GUI
Side-by-side English → Aurebesh translator using the Aurebesh OTF font.
Requires: Pillow  (pip install pillow)
Run: python tools/gui.py
"""

import re
import sys
from pathlib import Path

try:
    import tkinter as tk
except ImportError:
    sys.exit(
        "tkinter is not installed.\n"
        "  Debian/Ubuntu/Parrot: sudo apt install python3-tk\n"
        "  Fedora/RHEL:          sudo dnf install python3-tkinter\n"
        "  Arch:                 sudo pacman -S tk\n"
    )

try:
    from PIL import Image, ImageDraw, ImageFont, ImageTk
except ImportError:
    sys.exit("Pillow is not installed. Run: uv sync  (or: pip install pillow)")

if __package__ in (None, ""):  # run as ``python tools/gui.py`` or as the frozen entry script
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.translate import AUREBESH  # noqa: E402


def _resource(relative: str) -> Path:
    """Resolve a bundled resource path — works both in dev and when frozen."""
    base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent.parent
    return base / relative


# ── Palette ───────────────────────────────────────────────────────────────────
BG          = "#06060f"
PANEL_BG    = "#0c0c1e"
INPUT_BG    = "#08081a"
BORDER      = "#1e1e40"
ACCENT      = "#ffd700"
BLUE_ACCENT = "#5599ff"
FOCUS_BLUE  = "#2e5aa8"
GLYPH_COLOR = "#ffd700"
TEXT_FG     = "#cce0ff"
MUTED       = "#404070"

FONT_DIR  = _resource("fonts")
FONT_SIZE = 40
ICON_PATH = _resource("icons") / "icon.png"


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def wrap_lines(text: str, max_px: int, measure) -> list[str]:
    """Word-wrap text to fit within max_px, respecting newlines.

    ``measure(str) -> float`` returns the rendered width of a string, e.g.
    ``ImageFont.FreeTypeFont.getlength``. Blank paragraphs become empty lines.
    """
    out: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        current = ""
        for word in para.split(" "):
            candidate = (current + " " + word).lstrip()
            if measure(candidate) > max_px and current:
                out.append(current)
                current = word
            else:
                current = candidate
        if current:
            out.append(current)
    return out


def glyph_names(text: str) -> str:
    """Build the reference strip: letters as hyphenated glyph names, words two spaces apart.

    Characters with no Aurebesh glyph (digits, punctuation) are skipped.
    """
    parts: list[str] = []
    for chunk in re.split(r"(\s+)", text):
        if chunk.isspace():
            parts.append("  ")
        elif chunk:
            parts.append("-".join(AUREBESH[c] for c in chunk.upper() if c in AUREBESH))
    return "".join(parts).strip()


class AurebeshApp(tk.Tk):
    MARGIN = 20
    VGAP   = 8   # extra vertical gap between lines

    def __init__(self) -> None:
        super().__init__()
        self.title("Aurebesh Translator")
        self.configure(bg=BG)
        self.geometry("1500x900")
        self.minsize(900, 600)

        self.ab_font    = ImageFont.truetype(str(FONT_DIR / "Aurebesh.otf"), FONT_SIZE)
        self.title_font = ImageFont.truetype(str(FONT_DIR / "Audiowide.ttf"), 36)
        self.sub_font   = ImageFont.truetype(str(FONT_DIR / "Audiowide.ttf"), 12)
        self._photo:       ImageTk.PhotoImage | None = None
        self._title_photo: ImageTk.PhotoImage | None = None

        self._icon_photo = ImageTk.PhotoImage(Image.open(ICON_PATH))
        self.iconphoto(True, self._icon_photo)

        self._build_ui()

    # ──────────────────────────────── UI ─────────────────────────────────────

    def _build_ui(self) -> None:
        tk.Frame(self, height=2, bg=ACCENT).pack(fill=tk.X)

        self.title_canvas = tk.Canvas(self, height=96, bg=BG, highlightthickness=0)
        self.title_canvas.pack(fill=tk.X)
        self.title_canvas.bind("<Configure>", lambda _: self._draw_title())

        tk.Frame(self, height=1, bg=ACCENT).pack(fill=tk.X)

        pane = tk.Frame(self, bg=BG)
        pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        pane.columnconfigure(0, weight=1, uniform="col")
        pane.columnconfigure(1, weight=1, uniform="col")
        pane.rowconfigure(0, weight=1)

        self._build_left(pane)
        self._build_right(pane)

    def _draw_title(self) -> None:
        c = self.title_canvas
        w = c.winfo_width() or 1500
        h = 72

        bg   = _hex_to_rgb(BG)
        gold = _hex_to_rgb(ACCENT)
        blue = _hex_to_rgb(BLUE_ACCENT)

        title = "AUREBESH TRANSLATOR"
        sub   = "GALACTIC BASIC STANDARD  ·  IMPERIAL TRANSLATION SERVICE"

        img  = Image.new("RGB", (w, h), bg)
        draw = ImageDraw.Draw(img)

        t_asc, t_desc = self.title_font.getmetrics()
        s_asc, s_desc = self.sub_font.getmetrics()
        t_h = t_asc + t_desc
        s_h = s_asc + s_desc
        gap = 6
        total = t_h + gap + s_h
        y0 = (h - total) // 2

        draw.text(((w - self.title_font.getlength(title)) / 2, y0),
                  title, font=self.title_font, fill=gold)
        draw.text(((w - self.sub_font.getlength(sub)) / 2, y0 + t_h + gap),
                  sub, font=self.sub_font, fill=blue)

        self._title_photo = ImageTk.PhotoImage(img)
        c.delete("all")
        c.create_image(0, 0, anchor="nw", image=self._title_photo)

    def _panel(self, parent: tk.Frame, col: int) -> tk.Frame:
        outer = tk.Frame(parent, bg=BORDER)
        outer.grid(row=0, column=col, sticky="nsew",
                   padx=(0, 5) if col == 0 else (5, 0))
        outer.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)
        inner = tk.Frame(outer, bg=PANEL_BG)
        inner.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        inner.rowconfigure(1, weight=1)
        inner.columnconfigure(0, weight=1)
        return inner

    def _section_label(self, parent: tk.Frame, row: int,
                       text: str, color: str) -> None:
        tk.Label(parent, text=text, font=("Courier New", 9, "bold"),
                 fg=color, bg=PANEL_BG, anchor="w",
                 ).grid(row=row, column=0, sticky="w", padx=10, pady=(10, 4))

    def _build_left(self, parent: tk.Frame) -> None:
        frame = self._panel(parent, 0)
        self._section_label(frame, 0, "◈  GALACTIC BASIC STANDARD", BLUE_ACCENT)

        self.input_box = tk.Text(
            frame, font=("Courier New", 13), wrap=tk.WORD,
            bg=INPUT_BG, fg=TEXT_FG, insertbackground=ACCENT,
            relief=tk.FLAT, bd=0, padx=12, pady=10,
            selectbackground="#1e2e6a",
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=FOCUS_BLUE,
        )
        self.input_box.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 6))
        # <<Modified>> fires on every mutation (typing, paste, undo), unlike
        # <KeyRelease>, which misses mouse-driven pastes.
        self.input_box.bind("<<Modified>>", self._on_modified)

        self.char_count_var = tk.StringVar(value="")
        tk.Label(frame, textvariable=self.char_count_var,
                 font=("Courier New", 8), fg=MUTED, bg=PANEL_BG, anchor="e",
                 ).grid(row=2, column=0, sticky="e", padx=10, pady=(0, 6))

    def _build_right(self, parent: tk.Frame) -> None:
        frame = self._panel(parent, 1)
        self._section_label(frame, 0, "◈  AUREBESH", ACCENT)

        self.canvas = tk.Canvas(frame, bg=INPUT_BG, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 4))
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        self.canvas.bind("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

        tk.Frame(frame, height=1, bg=BORDER).grid(row=2, column=0, sticky="ew", padx=6)
        self.names_text = tk.Text(
            frame, height=2, font=("Courier New", 8), wrap=tk.WORD,
            bg=PANEL_BG, fg=MUTED, relief=tk.FLAT, bd=0,
            padx=10, pady=5, state=tk.DISABLED,
        )
        self.names_text.grid(row=3, column=0, sticky="ew", padx=6, pady=(0, 6))

    # ──────────────────────────────── logic ──────────────────────────────────

    def _current_text(self) -> str:
        return self.input_box.get("1.0", tk.END).rstrip("\n")

    def _on_modified(self, _event=None) -> None:
        # Tk keeps firing <<Modified>> until the flag is cleared; clearing it
        # fires the event once more with the flag False, which we ignore.
        if not self.input_box.edit_modified():
            return
        self.input_box.edit_modified(False)
        self._on_change()

    def _on_change(self, _event=None) -> None:
        text = self._current_text()
        count = sum(1 for c in text.upper() if c in AUREBESH)
        self.char_count_var.set(f"{count} letter{'s' if count != 1 else ''}")
        self._render(text)

    def _on_canvas_resize(self, _event=None) -> None:
        self._render(self._current_text())

    def _render(self, text: str) -> None:
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10:
            return

        M    = self.MARGIN
        VGAP = self.VGAP
        bg   = _hex_to_rgb(INPUT_BG)
        gold = _hex_to_rgb(GLYPH_COLOR)

        lines = wrap_lines(text, cw - 2 * M, self.ab_font.getlength)

        # Measure line height from a reference string
        ascent, descent = self.ab_font.getmetrics()
        line_h = ascent + descent

        total_h = max(M + len(lines) * (line_h + VGAP) + M, ch)

        img = Image.new("RGB", (cw, total_h), bg)
        draw = ImageDraw.Draw(img)

        y = M
        for line in lines:
            if line:
                draw.text((M, y), line, font=self.ab_font, fill=gold)
            y += line_h + VGAP

        self._photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self._photo)
        self.canvas.configure(scrollregion=(0, 0, cw, total_h))

        # Update names strip
        self.names_text.configure(state=tk.NORMAL)
        self.names_text.delete("1.0", tk.END)
        self.names_text.insert("1.0", glyph_names(text))
        self.names_text.configure(state=tk.DISABLED)


if __name__ == "__main__":
    AurebeshApp().mainloop()
