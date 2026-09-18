# Repository Guidelines

## Project Structure & Module Organization
- `aurebesh.bas` is the single source for 8x8 Aurebesh bitmap glyphs, expressed as `const uint_8 data[]` blocks with inline `' letter` comments; keep glyphs ordered alphabetically and separated by blank lines for readability.
- If you add helpers, place render/preview scripts under `tools/` and any future tests under `tests/`; keep the repository root minimal.

## Build, Test, and Development Commands
- No build pipeline exists; treat `aurebesh.bas` as an includeable data file. Make edits directly and sanity-check layout locally.
- Verify each glyph has eight rows with this quick check:  
  ```bash
  awk '/^0x/{c++} /^};/{print "rows:",c; c=0}' aurebesh.bas
  ```
- Transliterate sample text with `python tools/translate.py to-ab "Hello there"` or reverse with `python tools/translate.py to-en "Herf Enth Leth Leth Osk"`.
- If you create visualization helpers, document their usage here (e.g., `python tools/preview.py` to render glyphs as ASCII).

## Coding Style & Naming Conventions
- Keep the `const uint_8 data[] = { ... };  ' letter` pattern; one glyph per block. Use two-space indents inside braces and uppercase hexadecimal (`0x3C` not `0x3c`) for consistency.
- Maintain trailing inline comments for glyph labels (`' a`, `' b`, etc.) and align braces/spacing to match existing blocks.
- Favor small, self-contained additions; avoid introducing dependencies unless required for preview/testing scripts.

## Testing Guidelines
- Manual verification is expected today. If adding scripts, include a fast check that flags non-8-row glyphs and malformed hex.
- Name any new tests after the glyph or feature they cover (e.g., `test_aurek_rendering`). Store fixtures next to the tests that consume them.
- When modifying glyph shapes, provide a brief note or screenshot in the PR description showing before/after rendering from your preview tool.

## Commit & Pull Request Guidelines
- Use imperative, scope-focused commit subjects (e.g., `Add resh glyph bitmap`); keep commits atomic so reviewers can isolate changes.
- PRs should summarize the intent, list affected glyphs, mention how you validated the data, and include artifacts (render output or the `awk` check result).
- Link related issues or tickets when available; request review if you adjust glyph shapes, ordering, or introduce new helper scripts.
