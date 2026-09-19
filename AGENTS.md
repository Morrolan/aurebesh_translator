# Repository Guidelines

## Project Structure & Module Organization
- `tools/gui.py` is the tkinter + Pillow GUI; it renders Aurebesh live using the bundled OTF font (`fonts/Aurebesh.otf`), not any bitmap data.
- `tools/translate.py` is the CLI transliterator (English ↔ Aurebesh glyph names), driven by the letter→name map at the top of the file.
- `fonts/` holds the bundled Aurebesh OTF family (regular, bold, italic, condensed variants) plus the Audiowide title font.
- `icons/` holds the generated app icon (`icon.png` for the window/taskbar icon, `icon.ico` embedded into the Windows build); regenerate both with `tools/generate_icon.py`.
- `tests/` holds pytest unit tests; `aurebesh.spec` and `.github/workflows/build.yml` define the PyInstaller packaging and CI build matrix.
- Keep the repository root minimal; place new helpers under `tools/` and new tests under `tests/`.

## Build, Test, and Development Commands
- Run the GUI from source: `uv sync && uv run python tools/gui.py` (requires tkinter — see README for OS install steps).
- Run the test suite: `uv run pytest`.
- Transliterate sample text with `python tools/translate.py to-ab "Hello there"` or reverse with `python tools/translate.py to-en "Herf Enth Leth Leth Osk"`.
- Build a standalone binary the way CI does: `uv run --group build python -m PyInstaller aurebesh.spec --distpath dist --workpath build/pyinstaller`.
- Regenerate the app icon after palette/branding changes: `python tools/generate_icon.py`.

## Coding Style & Naming Conventions
- Standard PEP 8 Python: 4-space indents, type hints where practical, small self-contained functions.
- Favor small, self-contained additions; avoid introducing dependencies unless required for the GUI, packaging, or tests.

## Testing Guidelines
- Add pytest tests under `tests/`, named after the feature they cover (e.g. `test_translate.py`).
- When changing rendering (fonts, layout, colours) in `tools/gui.py`, include a before/after screenshot in the PR description since there's no automated visual check.

## Commit & Pull Request Guidelines
- Use imperative, scope-focused commit subjects (e.g. `Fix PyInstaller PIL hidden import`); keep commits atomic so reviewers can isolate changes.
- PRs should summarize the intent, mention how the change was validated (tests run, GUI screenshot, CLI output), and link related issues when available.
