import re
from pathlib import Path

import pytest

from tools import __version__
from tools.translate import (
    AUREBESH,
    AUREBESH_TO_EN,
    aurebesh_to_eng,
    build_parser,
    eng_to_aurebesh,
    main,
)

ROOT = Path(__file__).resolve().parent.parent


class TestAurebeshMap:
    def test_all_26_letters_present(self):
        assert set(AUREBESH.keys()) == set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_all_values_unique(self):
        values = list(AUREBESH.values())
        assert len(values) == len(set(values))

    def test_known_entries(self):
        assert AUREBESH["A"] == "Aurek"
        assert AUREBESH["H"] == "Herf"
        assert AUREBESH["Z"] == "Zerek"

    def test_reverse_map_is_true_inverse(self):
        assert len(AUREBESH_TO_EN) == 26
        for letter, name in AUREBESH.items():
            assert AUREBESH_TO_EN[name.upper()] == letter

    def test_gui_shares_the_same_map(self):
        gui = pytest.importorskip("tools.gui")
        assert gui.AUREBESH is AUREBESH


class TestEngToAurebesh:
    def test_single_letter(self):
        assert eng_to_aurebesh("A") == "Aurek"

    def test_word(self):
        assert eng_to_aurebesh("Hello") == "Herf Enth Leth Leth Osk"

    def test_case_insensitive(self):
        assert eng_to_aurebesh("hello") == eng_to_aurebesh("HELLO")

    def test_custom_separator(self):
        assert eng_to_aurebesh("AB", "-") == "Aurek-Besh"

    def test_words_separated_by_double_space(self):
        assert eng_to_aurebesh("Hi there") == "Herf Isk  Trill Herf Enth Resh Enth"

    def test_custom_word_separator(self):
        assert eng_to_aurebesh("Hi yo", "-", " / ") == "Herf-Isk / Yirt-Osk"

    def test_newlines_preserved(self):
        assert eng_to_aurebesh("Hi\nyo") == "Herf Isk\nYirt Osk"

    def test_multiple_spaces_collapse_to_one_word_gap(self):
        assert eng_to_aurebesh("A   B") == "Aurek  Besh"

    def test_non_alpha_passed_through(self):
        assert eng_to_aurebesh("A1B") == "Aurek 1 Besh"

    def test_empty_string(self):
        assert eng_to_aurebesh("") == ""


class TestAurebeshToEng:
    def test_single_name(self):
        assert aurebesh_to_eng("Aurek") == "A"

    def test_case_insensitive(self):
        assert aurebesh_to_eng("herf") == "H"
        assert aurebesh_to_eng("HERF") == "H"

    def test_word_is_joined(self):
        assert aurebesh_to_eng("Herf Enth Leth Leth Osk") == "HELLO"

    def test_words_split_on_double_space(self):
        assert aurebesh_to_eng("Herf Isk  Trill Herf Enth Resh Enth") == "HI THERE"

    def test_custom_separators(self):
        assert aurebesh_to_eng("Herf-Isk / Yirt-Osk", "-", " / ") == "HI YO"

    def test_newlines_preserved(self):
        assert aurebesh_to_eng("Herf Isk\nYirt Osk") == "HI\nYO"

    def test_unknown_token_passed_through(self):
        assert aurebesh_to_eng("Blarg") == "Blarg"
        assert aurebesh_to_eng("Aurek 1 Besh") == "A1B"

    def test_empty_string(self):
        assert aurebesh_to_eng("") == ""


class TestRoundtrip:
    @pytest.mark.parametrize("letter", list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    def test_every_letter(self, letter):
        assert aurebesh_to_eng(eng_to_aurebesh(letter)) == letter

    @pytest.mark.parametrize(
        "text",
        [
            "HELLO THERE",
            "GENERAL KENOBI",
            "MAY THE FORCE\nBE WITH YOU",
            "R2 D2 AND C 3PO",
            "A B C",
        ],
    )
    def test_multi_word(self, text):
        assert aurebesh_to_eng(eng_to_aurebesh(text)) == text

    @pytest.mark.parametrize("sep,word_sep", [("-", " "), ("_", " / "), ("|", "\t")])
    def test_multi_word_with_custom_separators(self, sep, word_sep):
        text = "HELLO THERE"
        assert aurebesh_to_eng(eng_to_aurebesh(text, sep, word_sep), sep, word_sep) == text


class TestCli:
    def test_to_ab_from_args(self, capsys):
        main(["to-ab", "Hello", "there"])
        assert capsys.readouterr().out == "Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth\n"

    def test_to_en_from_args(self, capsys):
        main(["to-en", "Herf Enth Leth Leth Osk"])
        assert capsys.readouterr().out == "HELLO\n"

    def test_reads_stdin_when_no_text(self, capsys, monkeypatch):
        import io

        monkeypatch.setattr("sys.stdin", io.StringIO("hi\n"))
        main(["to-ab"])
        assert capsys.readouterr().out == "Herf Isk\n"

    def test_separator_flags(self, capsys):
        main(["to-ab", "--separator", "-", "--word-separator", " / ", "Hi yo"])
        assert capsys.readouterr().out == "Herf-Isk / Yirt-Osk\n"

    def test_invalid_mode_exits_nonzero(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["sideways", "hi"])
        assert exc.value.code != 0
        assert "invalid choice" in capsys.readouterr().err

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit) as exc:
            main(["--version"])
        assert exc.value.code == 0
        assert capsys.readouterr().out.strip().endswith(__version__)

    def test_parser_defaults(self):
        args = build_parser().parse_args(["to-ab"])
        assert args.separator == " "
        assert args.word_separator == "  "
        assert args.text == []


class TestVersion:
    def test_matches_pyproject(self):
        pyproject = (ROOT / "pyproject.toml").read_text()
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
        assert match, "no version in pyproject.toml"
        assert match.group(1) == __version__
