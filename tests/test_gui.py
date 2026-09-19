"""Headless tests for the pure helpers in tools/gui.py.

No Tk window is created; importing the module only needs tkinter to be
installed, not a display.
"""

import sys

import pytest

gui = pytest.importorskip("tools.gui", reason="tkinter not available")


class TestWrapLines:
    """``len`` is used as the width measure so 1 char == 1 px."""

    def test_short_text_stays_on_one_line(self):
        assert gui.wrap_lines("hello", 100, len) == ["hello"]

    def test_wraps_at_word_boundary(self):
        assert gui.wrap_lines("aa bb cc", 5, len) == ["aa bb", "cc"]

    def test_single_overlong_word_is_not_split(self):
        assert gui.wrap_lines("abcdefghij", 3, len) == ["abcdefghij"]

    def test_newlines_start_new_lines(self):
        assert gui.wrap_lines("aa\nbb", 100, len) == ["aa", "bb"]

    def test_blank_paragraph_becomes_empty_line(self):
        assert gui.wrap_lines("aa\n\nbb", 100, len) == ["aa", "", "bb"]

    def test_empty_text(self):
        assert gui.wrap_lines("", 100, len) == [""]

    def test_uses_measure_callback(self):
        # every string measures as 1000px, so every word wraps
        assert gui.wrap_lines("a b c", 10, lambda s: 1000) == ["a", "b", "c"]


class TestGlyphNames:
    def test_single_word(self):
        assert gui.glyph_names("Hello") == "Herf-Enth-Leth-Leth-Osk"

    def test_words_separated_by_two_spaces(self):
        assert gui.glyph_names("Hi yo") == "Herf-Isk  Yirt-Osk"

    def test_non_letters_skipped(self):
        assert gui.glyph_names("R2-D2!") == "Resh-Dorn"

    def test_case_insensitive(self):
        assert gui.glyph_names("hi") == gui.glyph_names("HI")

    def test_leading_trailing_whitespace_stripped(self):
        assert gui.glyph_names("  hi  ") == "Herf-Isk"

    def test_empty(self):
        assert gui.glyph_names("") == ""


class TestHexToRgb:
    @pytest.mark.parametrize(
        "hex_str,rgb",
        [("#000000", (0, 0, 0)), ("#ffd700", (255, 215, 0)), ("06060f", (6, 6, 15))],
    )
    def test_conversion(self, hex_str, rgb):
        assert gui._hex_to_rgb(hex_str) == rgb


class TestResource:
    def test_dev_mode_resolves_relative_to_repo_root(self, monkeypatch):
        monkeypatch.delattr(sys, "frozen", raising=False)
        assert gui._resource("fonts") == gui.Path(gui.__file__).parent.parent / "fonts"

    def test_frozen_mode_uses_meipass(self, monkeypatch, tmp_path):
        monkeypatch.setattr(sys, "frozen", True, raising=False)
        monkeypatch.setattr(sys, "_MEIPASS", str(tmp_path), raising=False)
        assert gui._resource("fonts") == tmp_path / "fonts"

    def test_bundled_resources_exist(self):
        assert (gui.FONT_DIR / "Aurebesh.otf").is_file()
        assert (gui.FONT_DIR / "Audiowide.ttf").is_file()
        assert gui.ICON_PATH.is_file()
