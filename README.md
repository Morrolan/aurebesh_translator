# Aurebesh Translator

A Star Wars-themed GUI that translates English text into Aurebesh — the written language of the Star Wars galaxy — in real time.

![Aurebesh Translator](https://raw.githubusercontent.com/Morrolan/aurebesh_translator/main/docs/screenshot.png)

## Features

- Live side-by-side translation as you type
- Renders authentic Aurebesh glyphs using a bundled OTF font
- Glyph name strip (e.g. `Herf-Enth-Leth-Leth-Osk`) for reference
- Star Wars colour palette — deep space black, Imperial gold
- Scrollable output canvas (mousewheel / trackpad)

## Running from source

**Requirements:** Python 3.10+, [Pillow](https://pillow.readthedocs.io/), tkinter

Tkinter ships with Python on Windows and macOS. On Linux install it via your package manager first:

```bash
# Debian / Ubuntu / Parrot
sudo apt install python3-tk

# Fedora / RHEL
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

Then:

```bash
uv sync
uv run python tools/gui.py
```

## Pre-built binaries

Download the latest release for your platform from the
[Releases](https://github.com/Morrolan/aurebesh_translator/releases) page:

| Platform | File |
|----------|------|
| Linux (x86-64) | `aurebesh-translator` |
| Windows (x86-64) | `aurebesh-translator.exe` |

No installation required — both are self-contained single-file executables.

## Building locally

```bash
python3 -m venv .venv
.venv/bin/pip install pyinstaller pillow      # Linux / macOS
# .venv\Scripts\pip install pyinstaller pillow  # Windows

.venv/bin/python -m PyInstaller aurebesh.spec --distpath dist --workpath build/pyinstaller
```

The binary is written to `dist/`.

## CLI translator

A lightweight command-line transliterator is also included:

```bash
# English → Aurebesh names
python tools/translate.py to-ab "Hello there"
# → Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth

# Aurebesh names → English
python tools/translate.py to-en "Herf Enth Leth Leth Osk"
# → HELLO
```

## Fonts

The `fonts/` directory contains the Aurebesh OTF font family (regular,
bold, italic, and condensed variants). The GUI uses `Aurebesh.otf` by
default; swap the filename in `tools/gui.py` to change weight or style.

## Repository layout

```
aurebesh_translator/
├── tools/
│   ├── gui.py          # GUI application (tkinter + Pillow)
│   └── translate.py    # CLI transliterator
├── fonts/              # Aurebesh OTF font family
├── aurebesh.bas        # Original 8×8 bitmap glyph data (reference)
├── aurebesh.spec       # PyInstaller build spec
└── .github/
    └── workflows/
        └── build.yml   # CI: builds Linux + Windows binaries on tag push
```

## Releasing

Tag a version and push — GitHub Actions builds both binaries and
publishes a release automatically:

```bash
git tag v1.0.0
git push --tags
```
