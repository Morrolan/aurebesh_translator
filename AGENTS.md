# Repository Guidelines

## Project Structure & Module Organization
- `tools/` is a package; `tools/__init__.py` holds `__version__`, which a test keeps in sync with `pyproject.toml` — bump both together.
- `tools/gui.py` is the tkinter + Pillow GUI; it renders Aurebesh live using the bundled OTF font (`fonts/Aurebesh.otf`), not any bitmap data. Its pure helpers (`wrap_lines`, `glyph_names`) live at module level so they can be tested headless.
- `tools/translate.py` is the CLI transliterator (English ↔ Aurebesh glyph names) and the single source of truth for the letter→name map (`AUREBESH`); the GUI imports it from there.
- `fonts/` holds the bundled Aurebesh OTF family (regular, bold, italic, condensed variants) plus the Audiowide title font.
- `icons/` holds the generated app icon (`icon.png` for the window/taskbar icon, `icon.ico` embedded into the Windows build); regenerate both with `tools/generate_icon.py`.
- `tests/` holds pytest unit tests; `aurebesh.spec` and `.github/workflows/build.yml` define the PyInstaller packaging and release build; `.github/workflows/test.yml` runs lint + tests on every push/PR.
- `LICENSE` is MIT and covers the code only; `THIRD_PARTY_NOTICES.md` carries the font licences (Pixel Sagas personal-use, Audiowide OFL) and must be updated if fonts are added or swapped.
- Keep the repository root minimal; place new helpers under `tools/` and new tests under `tests/`.

## Build, Test, and Development Commands
- Run the GUI from source: `uv sync && uv run python tools/gui.py` (requires tkinter — see README for OS install steps).
- Run the test suite: `uv run pytest`. Lint: `uv run ruff check .` (lint only — the formatter is intentionally not enforced so the aligned palette constants in `gui.py` stay readable).
- Transliterate sample text with `python tools/translate.py to-ab "Hello there"` or reverse with `python tools/translate.py to-en "Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth"` (one space between letters, two between words).
- Build a standalone binary the way CI does: `uv run --group build python -m PyInstaller aurebesh.spec --distpath dist --workpath build/pyinstaller`.
- Regenerate the app icon after palette/branding changes: `python tools/generate_icon.py`.

## Coding Style & Naming Conventions
- Standard PEP 8 Python: 4-space indents, type hints where practical, small self-contained functions.
- Favor small, self-contained additions; avoid introducing dependencies unless required for the GUI, packaging, or tests.

## Testing Guidelines
- Add pytest tests under `tests/`, named after the feature they cover (`test_translate.py` for the CLI, `test_gui.py` for GUI helpers, `test_assets.py` for fonts/icons/spec).
- Keep GUI logic testable by writing it as module-level pure functions rather than methods that need a Tk root.
- Record user-visible changes under `[Unreleased]` in `CHANGELOG.md`.
- When changing rendering (fonts, layout, colours) in `tools/gui.py`, include a before/after screenshot in the PR description since there's no automated visual check.

## Commit & Pull Request Guidelines
- Use imperative, scope-focused commit subjects (e.g. `Fix PyInstaller PIL hidden import`); keep commits atomic so reviewers can isolate changes.
- PRs should summarize the intent, mention how the change was validated (tests run, GUI screenshot, CLI output), and link related issues when available.
