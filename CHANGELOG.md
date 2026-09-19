# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- MIT `LICENSE` for the code and `THIRD_PARTY_NOTICES.md` covering the bundled
  Pixel Sagas Aurebesh fonts (personal use) and Audiowide (SIL OFL 1.1).
- `--version` and `--word-separator` flags on the CLI transliterator.
- Test workflow that runs lint + tests on every push and pull request across
  Python 3.10–3.13 on Linux and Windows.
- Ruff lint configuration and a Dependabot config for GitHub Actions and uv.
- Tests for the CLI, GUI text helpers, bundled fonts/icons and the PyInstaller spec.

### Changed
- The GUI now re-renders on every text mutation (including mouse-driven paste),
  not just on key release.
- The GUI imports the glyph-name map from `tools/translate.py` instead of
  keeping its own copy.
- `.python-version` is now committed so local and CI builds use the same interpreter.

### Fixed
- `to-ab` now separates words with two spaces and `to-en` joins letters back
  into words, so multi-word text round-trips (`Hello there` → `HELLO THERE`).
  Previously word boundaries were lost and `to-en` returned `H E L L O`.

### Removed
- Non-functional `aurebesh-translate` console-script entry in `pyproject.toml`.

## [1.0.0] — 2026-09-18

### Added
- Initial release: tkinter + Pillow GUI with live side-by-side Aurebesh
  rendering, glyph-name reference strip, CLI transliterator, and PyInstaller
  builds for Linux and Windows via GitHub Actions.
