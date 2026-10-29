"""Invisible Unicode (PRD H9): decode tag smuggling, ignore legitimate uses."""
import re
import unicodedata

ZERO_WIDTH = "​‌‍‎‏⁠⁡⁢⁣⁤﻿"
BIDI = "‪‫‬‭‮⁦⁧⁨⁩"
TAGS = re.compile("[\U000e0000-\U000e007f]")
RTL_LETTERS = re.compile("[֐-ࣿ]")


def decode_tags(text: str) -> str:
    """Unicode tag characters U+E0020..U+E007E map 1:1 to printable ASCII ("ASCII smuggling")."""
    return "".join(chr(ord(c) - 0xE0000) for c in TAGS.findall(text) if 0x20 <= ord(c) - 0xE0000 <= 0x7E)


def _emoji(ch: str) -> bool:
    return unicodedata.category(ch) == "So" or ch == "️" or 0x1F3FB <= ord(ch) <= 0x1F3FF


def suspicious_invisibles(text: str) -> list[str]:
    """Invisible characters that aren't explained by emoji joining or right-to-left script."""
    rtl = bool(RTL_LETTERS.search(text))
    found = []
    for i, ch in enumerate(text):
        if TAGS.match(ch):
            found.append(ch)
        elif ch == "‍" and 0 < i < len(text) - 1 and _emoji(text[i - 1]) and _emoji(text[i + 1]):
            continue  # emoji ZWJ sequence, e.g. a family emoji
        elif ch in "‎‏" + BIDI and rtl:
            continue  # direction marks in Arabic/Hebrew text
        elif ch in ZERO_WIDTH + BIDI:
            found.append(ch)
    return found


def strip_invisibles(text: str) -> str:
    return TAGS.sub("", "".join(c for c in text if c not in ZERO_WIDTH + BIDI))
