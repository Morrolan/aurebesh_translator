#!/usr/bin/env python3
"""
Simple Aurebesh <-> English transliterator.

Usage:
  python tools/translate.py to-ab "Hello there"
  python tools/translate.py to-en "Herf Enth Leth Leth Osk  Trill Herf Enth Resh Enth"

Letters within a word are joined by --separator (default: one space) and
words are joined by --word-separator (default: two spaces), so the output
of ``to-ab`` can always be fed back through ``to-en``.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in (None, ""):  # run as ``python tools/translate.py``
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools import __version__  # noqa: E402

AUREBESH: dict[str, str] = {
    "A": "Aurek",
    "B": "Besh",
    "C": "Cresh",
    "D": "Dorn",
    "E": "Enth",
    "F": "Forn",
    "G": "Grek",
    "H": "Herf",
    "I": "Isk",
    "J": "Jenth",
    "K": "Krill",
    "L": "Leth",
    "M": "Mern",
    "N": "Nern",
    "O": "Osk",
    "P": "Peth",
    "Q": "Qek",
    "R": "Resh",
    "S": "Senth",
    "T": "Trill",
    "U": "Usk",
    "V": "Vev",
    "W": "Wesk",
    "X": "Xesh",
    "Y": "Yirt",
    "Z": "Zerek",
}

AUREBESH_TO_EN = {value.upper(): key for key, value in AUREBESH.items()}

DEFAULT_SEPARATOR = " "
DEFAULT_WORD_SEPARATOR = "  "


def eng_to_aurebesh(
    text: str,
    separator: str = DEFAULT_SEPARATOR,
    word_separator: str = DEFAULT_WORD_SEPARATOR,
) -> str:
    """Translate English letters to Aurebesh glyph names.

    Letters within a word are joined by ``separator``; words are joined by
    ``word_separator``. Newlines are preserved so paragraph structure survives.
    Characters with no Aurebesh equivalent (digits, punctuation) pass through.
    """
    output: list[str] = []
    for chunk in re.split(r"(\s+)", text):
        if not chunk:
            continue
        if chunk.isspace():
            output.append(chunk if "\n" in chunk else word_separator)
            continue
        output.append(separator.join(AUREBESH.get(c.upper(), c) for c in chunk))
    return "".join(output)


def aurebesh_to_eng(
    text: str,
    separator: str = DEFAULT_SEPARATOR,
    word_separator: str = DEFAULT_WORD_SEPARATOR,
) -> str:
    """Translate Aurebesh glyph names back to English letters.

    Inverse of :func:`eng_to_aurebesh`: tokens separated by ``separator`` are
    letters of one word, groups separated by ``word_separator`` are words.
    Unknown tokens pass through unchanged.
    """
    word_re = re.compile(f"(?:{re.escape(word_separator)})+")
    letter_re = re.compile(f"(?:{re.escape(separator)})+")

    output: list[str] = []
    for line_chunk in re.split(r"(\n+)", text):
        if not line_chunk:
            continue
        if "\n" in line_chunk:
            output.append(line_chunk)
            continue
        words = []
        for word in word_re.split(line_chunk.strip()):
            tokens = (t for t in letter_re.split(word) if t)
            words.append("".join(AUREBESH_TO_EN.get(t.upper(), t) for t in tokens))
        output.append(" ".join(words))
    return "".join(output)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Aurebesh <-> English transliterator")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "mode",
        choices=("to-ab", "to-en"),
        help="to-ab for English to Aurebesh, to-en for Aurebesh to English",
    )
    parser.add_argument(
        "text",
        nargs="*",
        help="Text to translate. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "--separator",
        default=DEFAULT_SEPARATOR,
        help="Separator between glyph names within a word (default: one space).",
    )
    parser.add_argument(
        "--word-separator",
        default=DEFAULT_WORD_SEPARATOR,
        help="Separator between words (default: two spaces).",
    )
    return parser


def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return " ".join(args.text)
    return sys.stdin.read().strip()


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    source = read_input(args)
    if args.mode == "to-ab":
        result = eng_to_aurebesh(source, args.separator, args.word_separator)
    else:
        result = aurebesh_to_eng(source, args.separator, args.word_separator)
    print(result)


if __name__ == "__main__":
    main()
