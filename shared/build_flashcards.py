#!/usr/bin/env python3
"""Build Anki-importable flashcards from GLOSSARY.md.

Usage: python3 shared/build_flashcards.py
Output: flashcards/cloud-dojo.csv  (File > Import in Anki; separator: tab)
Cards: "TERM (group)" on the front, the one-line definition on the back.
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "GLOSSARY.md"
OUT = ROOT / "flashcards" / "cloud-dojo.csv"


def main():
    group, cards = None, []
    for line in GLOSSARY.read_text().splitlines():
        m = re.match(r"## (.+)", line)
        if m:
            group = m.group(1)
            continue
        m = re.match(r"- \*\*(.+?)\*\* — (.+)", line)
        if m and group:
            cards.append((f"{m.group(1)} ({group})", m.group(2)))
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        csv.writer(f, delimiter="\t").writerows(cards)
    print(f"flashcards: {len(cards)} cards -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
