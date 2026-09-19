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
There is no macOS binary; macOS users can run from source as above.

## Building locally

Uses the same command as CI:

```bash
uv sync --group build
uv run python -m PyInstaller aurebesh.spec --distpath dist --workpath build/pyinstaller
```

The binary is written to `dist/`.

## Development

```bash
uv sync --group dev
uv run pytest          # tests
uv run ruff check .    # lint
```

Both run automatically on every push and pull request (Python 3.10–3.13,
Linux + Windows).

## CLI translator

A lightweight command-line transliterator is also included. Letters within a
word are separated by one space and words by two, so output round-trips:

```bash
# English → Aurebesh names
python tools/translate.py to-ab "Hello there"
# → Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth

# Aurebesh names → English
python tools/translate.py to-en "Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth"
# → HELLO THERE

# Custom separators, stdin input
echo "Hello there" | python tools/translate.py to-ab --separator - --word-separator " / "
# → Herf-Enth-Leth-Leth-Osk / Trill-Herf-Enth-Resh-Enth
```

## Fonts

The `fonts/` directory contains the Aurebesh OTF font family (regular,
bold, italic, and condensed variants). The GUI uses `Aurebesh.otf` by
default; swap the filename in `tools/gui.py` to change weight or style.

## Repository layout

```
aurebesh_translator/
├── tools/
│   ├── __init__.py          # Package marker + __version__
│   ├── gui.py               # GUI application (tkinter + Pillow)
│   ├── translate.py         # CLI transliterator + shared glyph-name map
│   └── generate_icon.py     # Regenerates icons/icon.{png,ico}
├── tests/                   # pytest suite (CLI, GUI helpers, assets)
├── fonts/                   # Aurebesh OTF family + Audiowide title font
├── icons/                   # App icon (window/taskbar + Windows .exe)
├── docs/                    # README screenshot
├── aurebesh.spec            # PyInstaller build spec
├── pyproject.toml           # Project metadata, deps, pytest + ruff config
├── uv.lock                  # Locked dependency versions
├── .python-version          # Interpreter used locally and in CI
├── CHANGELOG.md
├── LICENSE                  # MIT (code)
├── THIRD_PARTY_NOTICES.md   # Font licences + trademark note
└── .github/
    ├── dependabot.yml       # Weekly action / dependency bumps
    └── workflows/
        ├── test.yml         # CI: lint + tests on push / PR
        └── build.yml        # CI: builds Linux + Windows binaries on tag push
```

## Releasing

Tag a version and push — GitHub Actions builds both binaries and
publishes a release automatically:

```bash
git tag v1.0.0
git push --tags
```

## Licence

The code is released under the [MIT License](LICENSE).

The bundled fonts are **not** MIT-licensed and keep their own terms — see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md):

- **Aurebesh** family by Neale Davidson / [Pixel Sagas](https://www.pixelsagas.com)
  — free for personal use; commercial use requires a licence from the author.
- **Audiowide** by Astigmatic — [SIL Open Font License 1.1](THIRD_PARTY_NOTICES.md#audiowide-fontsaudiowidettf).

*Star Wars* and *Aurebesh* are trademarks of Lucasfilm Ltd. This is an
unofficial fan project, not affiliated with or endorsed by Lucasfilm or Disney.
