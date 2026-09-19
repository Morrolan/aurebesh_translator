"""Integrity checks for bundled fonts, icons and the PyInstaller spec."""

import re
from pathlib import Path

import pytest
from PIL import Image, ImageFont

from tools import generate_icon

ROOT = Path(__file__).resolve().parent.parent
FONT_FILES = sorted((ROOT / "fonts").glob("*.[ot]tf"))
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class TestFonts:
    def test_expected_font_files_present(self):
        names = {p.name for p in FONT_FILES}
        assert "Aurebesh.otf" in names
        assert "Audiowide.ttf" in names
        assert len(names) == 9

    @pytest.mark.parametrize("font_path", FONT_FILES, ids=lambda p: p.name)
    def test_font_loads(self, font_path):
        font = ImageFont.truetype(str(font_path), 24)
        family, _style = font.getname()
        assert family

    @pytest.mark.parametrize(
        "font_path", [p for p in FONT_FILES if p.name.startswith("Aurebesh")], ids=lambda p: p.name
    )
    def test_aurebesh_font_has_glyph_for_every_letter(self, font_path):
        font = ImageFont.truetype(str(font_path), 40)
        missing = [c for c in LETTERS + LETTERS.lower() if font.getmask(c).getbbox() is None]
        assert missing == []


class TestIcons:
    def test_committed_png(self):
        with Image.open(ROOT / "icons" / "icon.png") as img:
            assert img.size == (generate_icon.SIZE, generate_icon.SIZE)
            assert img.mode == "RGBA"

    def test_committed_ico_contains_all_sizes(self):
        with Image.open(ROOT / "icons" / "icon.ico") as img:
            assert img.info["sizes"] == {(s, s) for s in generate_icon.ICO_SIZES}

    def test_generator_output(self, tmp_path):
        png_path, ico_path = generate_icon.write_icons(tmp_path)
        with Image.open(png_path) as png:
            assert png.size == (512, 512)
            assert png.mode == "RGBA"
            # corners are transparent (rounded rect), centre has the gold glyph
            assert png.getpixel((0, 0))[3] == 0
        with Image.open(ico_path) as ico:
            assert ico.info["sizes"] == {(s, s) for s in generate_icon.ICO_SIZES}


class TestSpec:
    def test_spec_resources_exist(self):
        """Every ROOT / "x" / "y" path referenced in aurebesh.spec must exist."""
        spec = (ROOT / "aurebesh.spec").read_text()
        refs = re.findall(r'ROOT((?:\s*/\s*"[^"]+")+)', spec)
        assert refs, "no ROOT / ... paths found in spec"
        for ref in refs:
            parts = re.findall(r'"([^"]+)"', ref)
            path = ROOT.joinpath(*parts)
            assert path.exists(), f"spec references missing path: {path}"
