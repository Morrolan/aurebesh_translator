import pytest
from tools.translate import AUREBESH, aurebesh_to_eng, eng_to_aurebesh


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


class TestEngToAurebesh:
    def test_single_letter(self):
        assert eng_to_aurebesh("A", " ") == "Aurek"

    def test_word(self):
        assert eng_to_aurebesh("Hello", " ") == "Herf Enth Leth Leth Osk"

    def test_case_insensitive(self):
        assert eng_to_aurebesh("hello", " ") == eng_to_aurebesh("HELLO", " ")

    def test_custom_separator(self):
        assert eng_to_aurebesh("AB", "-") == "Aurek-Besh"

    def test_whitespace_between_words_preserved(self):
        result = eng_to_aurebesh("Hi there", " ")
        assert result == "Herf Isk Trill Herf Enth Resh Enth"

    def test_non_alpha_passed_through(self):
        assert eng_to_aurebesh("A1B", " ") == "Aurek 1 Besh"

    def test_empty_string(self):
        assert eng_to_aurebesh("", " ") == ""


class TestAurebeshToEng:
    def test_single_name(self):
        assert aurebesh_to_eng("Aurek") == "A"

    def test_case_insensitive(self):
        assert aurebesh_to_eng("herf") == "H"
        assert aurebesh_to_eng("HERF") == "H"

    def test_multiple_names(self):
        # each space-separated token maps to one letter
        assert aurebesh_to_eng("Herf Enth Leth Leth Osk") == "H E L L O"

    def test_unknown_token_passed_through(self):
        assert aurebesh_to_eng("Blarg") == "Blarg"

    def test_empty_string(self):
        assert aurebesh_to_eng("") == ""


class TestRoundtrip:
    @pytest.mark.parametrize("letter", list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    def test_every_letter(self, letter):
        name = eng_to_aurebesh(letter, " ")
        assert aurebesh_to_eng(name) == letter
