#!/usr/bin/env python3
"""Render a completion certificate from progress.json.

Usage: python3 shared/render_certificate.py "Your Name"
Output: certificate.html (print to PDF from the browser).
Requires: every quest done (1600/1600 XP). Refuses otherwise.
"""
import html
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "shared" / "progress.json"
OUT = ROOT / "certificate.html"


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "Cloud Dojo Graduate"
    data = json.loads(PROGRESS.read_text())
    if data["xp"] < data["total_xp"]:
        sys.exit(f"not yet: {data['xp']}/{data['total_xp']} XP — finish every quest first")
    badges = " · ".join(b.split()[0] for b in data["badges"])
    OUT.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Cloud Dojo Certificate</title>
<style>
body{{background:#0d1117;color:#e6edf3;font-family:system-ui,sans-serif;
display:flex;justify-content:center;padding:40px}}
.card{{border:3px solid #3fb950;border-radius:16px;padding:48px 64px;
text-align:center;max-width:720px}}
h1{{margin:0 0 8px}} .name{{font-size:2rem;color:#58a6ff;margin:16px 0}}
.meta{{color:#8b949e}} .badges{{font-size:1.6rem;margin:20px 0}}
@media print{{body{{background:#fff;color:#000}}.card{{border-color:#000}}}}
</style></head>
<body><div class="card">
<h1>Cloud Dojo — Grandmaster</h1>
<div class="name">{html.escape(name)}</div>
<p>completed the full journey: 8 phases, Track T, Module M —
{data['xp']}/{data['total_xp']} XP, 57 quests, capstone demoed and demolished.</p>
<div class="badges">{badges}</div>
<div class="meta">awarded {date.today().isoformat()} · verify: progress log in repo</div>
</div></body></html>
""")
    print(f"certificate rendered for {name}")


if __name__ == "__main__":
    main()
