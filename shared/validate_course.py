#!/usr/bin/env python3
"""Validate course integrity. Fails loudly on drift.

Usage: python3 shared/validate_course.py
Checks: every quest ID in progress.json has quests/<ID>.md;
XP sums to total_xp; phase README links resolve; badges match GAME-RULES.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []


def fail(msg):
    errors.append(msg)


def main():
    data = json.loads((ROOT / "shared" / "progress.json").read_text())
    quest_ids = [q["id"] for ph in data["phases"] for q in ph["quests"]]
    for qid in quest_ids:
        if not (ROOT / "quests" / f"{qid}.md").exists():
            fail(f"missing quest page: quests/{qid}.md")
    xp = sum(q["xp"] for ph in data["phases"] for q in ph["quests"])
    if xp != data["total_xp"]:
        fail(f"XP sum {xp} != total_xp {data['total_xp']}")
    rules = (ROOT / "GAME-RULES.md").read_text()
    for ph in data["phases"]:
        for part in ph["badge"].split("+"):
            badge_name = " ".join(part.split()[1:])
            if badge_name and badge_name not in rules:
                fail(f"badge not in GAME-RULES: {badge_name}")
    link_re = re.compile(r"\[(?:[^\]]+)\]\(([^)#]+)(?:#[^)]+)?\)")
    for md in list(ROOT.glob("*.md")) + list(ROOT.glob("phase-*/README.md")) + [
        ROOT / "track-iam-sandbox" / "README.md",
        ROOT / "module-moto-testing" / "README.md",
    ]:
        for target in link_re.findall(md.read_text()):
            if target.startswith(("http", "mailto:", "#", ".")) or "@" in target:
                continue
            if not (md.parent / target.split("#")[0]).exists():
                fail(f"broken link in {md.relative_to(ROOT)}: {target}")
    if errors:
        print("\n".join(f"FAIL: {e}" for e in errors))
        return 1
    print(f"course valid: {len(quest_ids)} quests, {xp} XP, links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
