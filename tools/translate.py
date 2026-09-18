#!/usr/bin/env python3
"""
Simple Aurebesh <-> English transliterator.

Usage:
  python tools/translate.py to-ab "Hello there"
  python tools/translate.py to-en "Herf Enth Leth Leth Osk"
"""

from __future__ import annotations

import argparse
import re
from typing import Dict

AUREBESH: Dict[str, str] = {
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


def eng_to_aurebesh(text: str, separator: str) -> str:
    """Translate English letters to Aurebesh word names, preserving whitespace."""
    output = []
    for chunk in re.split(r"(\s+)", text):
        if chunk.isspace():
            output.append(chunk)
            continue
        translated = [
            AUREBESH.get(char.upper(), char) for char in chunk
        ]
        output.append(separator.join(translated))
    return "".join(output)


def aurebesh_to_eng(text: str) -> str:
    """Translate Aurebesh word names back to English letters, preserving whitespace."""
    output = []
    for chunk in re.split(r"(\s+)", text):
        if chunk.isspace():
            output.append(chunk)
            continue
        mapped = AUREBESH_TO_EN.get(chunk.upper(), chunk)
        output.append(mapped)
    return "".join(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aurebesh <-> English transliterator")
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
        default=" ",
        help="Separator between Aurebesh glyph names (default: space).",
    )
    return parser.parse_args()


def read_input(args: argparse.Namespace) -> str:
    if args.text:
        return " ".join(args.text)
    import sys

    return sys.stdin.read().strip()


def main() -> None:
    args = parse_args()
    source = read_input(args)
    if args.mode == "to-ab":
        result = eng_to_aurebesh(source, separator=args.separator)
    else:
        result = aurebesh_to_eng(source)
    print(result)


if __name__ == "__main__":
    main()
