#!/usr/bin/env python3
"""Cloud Dojo progress tracker: check/uncheck quests, reset, interactive menu.

Usage:
    python3 shared/progress.py                 # interactive check menu
    python3 shared/progress.py status          # XP, level, badges, per-phase
    python3 shared/progress.py check Q0.1 [--force]
    python3 shared/progress.py uncheck Q0.1
    python3 shared/progress.py reset [--yes]

Every mutation saves shared/progress.json and re-renders the dashboard.
Game rules: quests complete in order; use --force to override (your call).
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "shared" / "progress.json"
PHASE_ORDER = [
    "phase-00", "phase-01", "phase-02", "phase-03",
    "phase-04", "phase-05", "phase-06", "phase-07", "phase-08",
]
ICON = {"done": "[x]", "in_progress": "[>]", "locked": "[ ]"}


def load():
    return json.loads(PROGRESS.read_text())


def render():
    subprocess.run(
        [sys.executable, str(ROOT / "shared" / "render_dashboard.py")],
        check=True, capture_output=True, text=True,
    )


def save(d):
    PROGRESS.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
    render()


def iter_quests(d):
    for ph in d["phases"]:
        for q in ph["quests"]:
            yield ph, q


def find(d, qid):
    qid = qid.strip().upper()
    for ph, q in iter_quests(d):
        if q["id"].upper() == qid:
            return ph, q
    return None, None


def recalc(d):
    d["xp"] = sum(q["xp"] for _, q in iter_quests(d) if q["status"] == "done")
    d["badges"] = [
        ph["badge"] for ph in d["phases"]
        if ph["quests"] and all(q["status"] == "done" for q in ph["quests"])
    ]
    total = 0
    for e in d.get("log", []):
        total += e["xp"]
        e["total"] = total


def level_name(xp):
    sys.path.insert(0, str(ROOT / "shared"))
    from render_dashboard import level_for
    return level_for(xp)


def prerequisites_met(ph, q):
    for other in ph["quests"]:
        if other["id"] == q["id"]:
            break
        if other["status"] != "done":
            return False, other["id"]
    return True, None


def advance(d, ph, q):
    """Unlock the next quest; on phase completion award badge + open next phase."""
    quests = ph["quests"]
    idx = next(i for i, x in enumerate(quests) if x["id"] == q["id"])
    rest = quests[idx + 1:]
    nxt = next((x for x in rest if x["status"] == "locked"), None)
    if nxt is not None:
        nxt["status"] = "in_progress"
        return f"unlocked {nxt['id']}"
    ph["status"] = "done"
    msg = f"phase complete — badge earned: {ph['badge']}"
    if ph["id"] in PHASE_ORDER:
        followers = PHASE_ORDER[PHASE_ORDER.index(ph["id"]) + 1:]
        if followers:
            nph = next(p for p in d["phases"] if p["id"] == followers[0])
            if nph["status"] == "locked":
                nph["status"] = "active"
                nph["quests"][0]["status"] = "in_progress"
                msg += f"; opened {nph['name']} ({nph['quests'][0]['id']})"
    if q["id"] == "Q1.1":
        for pid, first in (("track-t", "T.1"), ("module-m", "M.1")):
            side = next(p for p in d["phases"] if p["id"] == pid)
            if side["status"] == "locked":
                side["status"] = "active"
                side["quests"][0]["status"] = "in_progress"
        msg += "; opened Track T + Module M"
    return msg


def do_check(d, qid, force=False):
    ph, q = find(d, qid)
    if q is None:
        return f"unknown quest: {qid}"
    if q["status"] == "done":
        return f"{q['id']} already done"
    ok, blocker = prerequisites_met(ph, q)
    if not ok and not force:
        return f"blocked: finish {blocker} first (or retry with --force)"
    q["status"] = "done"
    d.setdefault("log", []).append({
        "date": date.today().isoformat(),
        "quest": f"{q['id']} {q['title']}",
        "xp": q["xp"],
        "total": 0,
    })
    extra = advance(d, ph, q)
    recalc(d)
    save(d)
    return f"checked {q['id']} (+{q['xp']} XP) — {extra} — total {d['xp']}"


def do_uncheck(d, qid):
    ph, q = find(d, qid)
    if q is None:
        return f"unknown quest: {qid}"
    if q["status"] != "done":
        return f"{q['id']} is not done (nothing to uncheck)"
    q["status"] = "in_progress"
    d["log"] = [e for e in d.get("log", []) if not e["quest"].startswith(q["id"] + " ")]
    recalc(d)
    save(d)
    return f"unchecked {q['id']} (-{q['xp']} XP) — total {d['xp']}"


def do_reset(d, yes=False):
    if not yes:
        ans = input("Reset ALL progress to zero? Type RESET to confirm: ").strip()
        if ans != "RESET":
            return "reset cancelled"
    for ph in d["phases"]:
        ph["status"] = "active" if ph["id"] == "phase-00" else "locked"
        for q in ph["quests"]:
            q["status"] = "in_progress" if q["id"] == "Q0.1" else "locked"
    d["xp"] = 0
    d["badges"] = []
    d["log"] = []
    save(d)
    return "progress reset — back to Q0.1"


def do_status(d):
    lines = [f"{d['xp']}/{d['total_xp']} XP · Level: {level_name(d['xp'])}"]
    lines.append("Badges: " + (", ".join(d["badges"]) if d["badges"] else "none yet"))
    for ph in d["phases"]:
        done = sum(q["xp"] for q in ph["quests"] if q["status"] == "done")
        lines.append(f"  [{ph['status'][:6]}] {ph['name']}: {done}/{ph['badge_xp']} XP")
    return "\n".join(lines)


def menu(d):
    print("Cloud Dojo — check menu (type a number to toggle, s status, r reset, q quit)")
    while True:
        print(f"\n{d['xp']}/{d['total_xp']} XP · Level: {level_name(d['xp'])}")
        index = {}
        n = 0
        for ph in d["phases"]:
            print(f"  {ph['name']} [{ph['status']}]")
            for q in ph["quests"]:
                n += 1
                index[str(n)] = q["id"]
                print(f"    {n:>2}. {ICON[q['status']]} {q['id']} {q['title']} ({q['xp']} XP)")
        try:
            cmd = input("\n> ").strip().lower()
        except EOFError:
            print("\nbye")
            return
        if cmd in ("q", "quit", "exit"):
            print("bye — progress saved, dashboard fresh")
            return
        if cmd in ("s", "status"):
            print(do_status(d))
        elif cmd in ("r", "reset"):
            print(do_reset(d))
        elif cmd in index:
            qid = index[cmd]
            _, q = find(d, qid)
            print(do_uncheck(d, qid) if q["status"] == "done" else do_check(d, qid))
        else:
            print("unknown command (number toggles, s status, r reset, q quit)")


def main(argv):
    d = load()
    if not argv or argv[0] == "menu":
        menu(d)
    elif argv[0] == "status":
        print(do_status(d))
    elif argv[0] == "check" and len(argv) >= 2:
        print(do_check(d, argv[1], force="--force" in argv))
    elif argv[0] == "uncheck" and len(argv) >= 2:
        print(do_uncheck(d, argv[1]))
    elif argv[0] == "reset":
        print(do_reset(d, yes="--yes" in argv))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
