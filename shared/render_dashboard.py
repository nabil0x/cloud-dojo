#!/usr/bin/env python3
"""Render dashboard.html from progress.json.

Usage:
    python3 shared/render_dashboard.py        # run from repo root

Source of truth: shared/progress.json (statuses: done | in_progress | locked).
Output: dashboard.html (self-contained, no external deps, works via file://).
"""
import html
import json
import re
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "shared" / "progress.json"
OUT = ROOT / "dashboard.html"

LEVELS = [
    (0, "Cloud Cadet"),
    (100, "Container Cadet"),
    (250, "Bucket Builder"),
    (400, "Compose Commander"),
    (550, "Lambda Launcher"),
    (750, "Cloud Captain"),
    (1000, "Platform Engineer"),
    (1300, "Dojo Master"),
]

STATUS_STYLE = {
    "done": ("✅", "done"),
    "in_progress": ("▶️", "active"),
    "locked": ("🔒", "locked"),
    "active": ("▶️", "active"),
}


def esc(s):
    return html.escape(str(s))


def level_for(xp):
    name = LEVELS[0][1]
    for threshold, title in LEVELS:
        if xp >= threshold:
            name = title
    return name


def next_level(xp):
    for threshold, title in LEVELS:
        if xp < threshold:
            return threshold, title
    return None, None


def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def md_to_html(text):
    out, in_list, in_code = [], False, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_code:
                out.append("</code></pre></div>")
            else:
                out.append('<div class="codewrap"><button class="copybtn" type="button">copy</button><pre><code>')
            in_code = not in_code
            continue
        if in_code:
            out.append(esc(line))
            continue
        if line.startswith("# "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h1>{md_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h2>{md_inline(line[3:])}</h2>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{md_inline(line[2:])}</li>")
        elif not line.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<p>{md_inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


QUEST_CSS = """:root{--bg:#0d1117;--card:#161b22;--line:#30363d;--txt:#e6edf3;
--mut:#8b949e;--grn:#3fb950;--amb:#d29922;--blu:#58a6ff;--pur:#bc8cff}
*{box-sizing:border-box}body{background:var(--bg);color:var(--txt);
font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;margin:0;
padding:24px;max-width:860px;margin-inline:auto;line-height:1.6}
.crumb{margin-bottom:14px;font-size:.9rem}.crumb a{color:var(--blu);text-decoration:none}
.hero{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:18px}
.hero h1{font-size:1.4rem;margin:0 0 6px}.meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;
color:var(--mut);font-size:.9rem}
.pill{padding:2px 10px;border-radius:999px;font-size:.8rem;border:1px solid var(--line)}
.pill.done{color:var(--grn);border-color:var(--grn)}.pill.active{color:var(--amb);border-color:var(--amb)}
.pill.locked{color:var(--mut)}
article{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px 22px}
article h2{font-size:1.05rem;margin:20px 0 8px;color:var(--blu)}article h2:first-child{margin-top:0}
article p{margin:8px 0}article ul{margin:8px 0;padding-left:22px}article li{margin:4px 0}
article a{color:var(--blu)}code{background:#21262d;padding:2px 6px;border-radius:6px;
font-family:ui-monospace,monospace;font-size:.88em}
pre{background:#010409;border:1px solid var(--line);border-radius:8px;padding:12px;overflow-x:auto}
pre code{background:none;padding:0}
.codewrap{position:relative}
.copybtn{position:absolute;top:8px;right:8px;background:#21262d;color:var(--mut);
border:1px solid var(--line);border-radius:6px;padding:2px 8px;font-size:.75rem;cursor:pointer}
.copybtn:hover{color:var(--txt);border-color:var(--blu)}
.nav{display:flex;justify-content:space-between;gap:12px;margin:18px 0;flex-wrap:wrap}
.nav-btn{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px;
color:var(--txt);text-decoration:none;font-size:.9rem}.nav-btn:hover{border-color:var(--blu)}
footer{color:var(--mut);font-size:.85rem;margin-top:16px}footer code{background:#21262d;
padding:2px 6px;border-radius:6px}"""

QUEST_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title — Cloud Dojo</title>
<style>$css</style>
</head>
<body>
<div class="crumb"><a href="../dashboard.html">← Cloud Dojo dashboard</a> · $phase</div>
<div class="hero">
<h1>$quest_id — $quest_title</h1>
<div class="meta"><span class="pill $cls">$status</span><span>$xp XP</span><span>$phase</span></div>
</div>
<article>
$body
</article>
<div class="nav"><span>$prev</span><span>$next</span></div>
<footer>Source: <code>quests/$quest_id.md</code> · re-run <code>python3 shared/render_dashboard.py</code> after editing.</footer>
<script>
document.querySelectorAll(".copybtn").forEach(function(b){
  b.addEventListener("click", function(){
    var t = b.parentElement.querySelector("pre").innerText;
    function done(){ b.textContent = "copied"; setTimeout(function(){ b.textContent = "copy"; }, 1200); }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(t).then(done, function(){ fallback(); });
    } else { fallback(); }
    function fallback(){
      var ta = document.createElement("textarea");
      ta.value = t; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); done(); } catch(e) {}
      document.body.removeChild(ta);
    }
  });
});
</script>
</body>
</html>
""")


def render_quest_pages(data):
    quests_dir = ROOT / "quests"
    flat = [(ph, q) for ph in data["phases"] for q in ph["quests"]]
    count = 0
    for i, (ph, q) in enumerate(flat):
        src = quests_dir / f'{q["id"]}.md'
        if not src.exists():
            continue
        prev = next_ = ""
        if i > 0:
            p = flat[i - 1][1]
            prev = f'<a class="nav-btn" href="{esc(p["id"])}.html">← {esc(p["id"])} {esc(p["title"])}</a>'
        if i < len(flat) - 1:
            n = flat[i + 1][1]
            next_ = f'<a class="nav-btn" href="{esc(n["id"])}.html">{esc(n["id"])} {esc(n["title"])} →</a>'
        icon, cls = STATUS_STYLE.get(q["status"], ("🔒", "locked"))
        label = {"done": "done", "in_progress": "in progress"}.get(q["status"], "locked")
        (quests_dir / f'{q["id"]}.html').write_text(
            QUEST_TEMPLATE.substitute(
                title=esc(f'{q["id"]} {q["title"]}'),
                css=QUEST_CSS,
                phase=esc(ph["name"]),
                quest_id=esc(q["id"]),
                quest_title=esc(q["title"]),
                xp=q["xp"],
                cls=cls,
                status=f"{icon} {label}",
                body=md_to_html(src.read_text()),
                prev=prev,
                next=next_,
                quest_id_raw=esc(q["id"]),
            )
        )
        count += 1
    print(f"quest pages rendered: {count}")


def main():
    data = json.loads(PROGRESS.read_text())
    xp = data["xp"]
    total = data["total_xp"]
    pct = min(100, round(xp / total * 100)) if total else 0
    level = level_for(xp)
    nxt, nxt_name = next_level(xp)
    earned_badges = set(data.get("badges", []))

    badge_cards = []
    for ph in data["phases"]:
        earned = ph["badge"] in earned_badges
        cls = "badge earned" if earned else "badge"
        badge_cards.append(
            f'<div class="{cls}"><div class="b-emoji">{esc(ph["badge"].split()[0])}</div>'
            f'<div class="b-name">{esc(" ".join(ph["badge"].split()[1:]))}</div>'
            f'<div class="b-state">{"earned" if earned else "locked"}</div></div>'
        )

    phase_cards = []
    for ph in data["phases"]:
        p_icon, p_cls = STATUS_STYLE.get(ph["status"], ("🔒", "locked"))
        quests = []
        for q in ph["quests"]:
            q_icon, q_cls = STATUS_STYLE.get(q["status"], ("🔒", "locked"))
            quests.append(
                f'<li class="quest {q_cls}"><span class="q-icon">{q_icon}</span>'
                f'<span class="q-id">{esc(q["id"])}</span>'
                f'<a class="q-title q-link" href="quests/{esc(q["id"])}.html">{esc(q["title"])}</a>'
                f'<span class="q-xp">{q["xp"]} XP</span></li>'
            )
        done_xp = sum(q["xp"] for q in ph["quests"] if q["status"] == "done")
        phase_cards.append(
            f'<section class="phase {p_cls}"><header><span class="p-icon">{p_icon}</span>'
            f'<h2>{esc(ph["name"])}</h2>'
            f'<span class="p-xp">{done_xp}/{ph["badge_xp"]} XP</span></header>'
            f'<ul>{"".join(quests)}</ul></section>'
        )

    log_rows = "".join(
        f'<tr><td>{esc(e.get("date", "—"))}</td><td>{esc(e.get("quest", "—"))}</td>'
        f'<td>{e.get("xp", 0):+d}</td><td>{e.get("total", "—")}</td></tr>'
        for e in data.get("log", [])
    ) or '<tr><td colspan="4" class="muted">No XP earned yet — the journey begins at Q0.1.</td></tr>'

    nxt_text = f"{nxt - xp} XP to <b>{esc(nxt_name)}</b>" if nxt else "Max level reached 🏆"

    OUT.write_text(f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>☁️ Cloud Dojo — Journey Dashboard</title>
<style>
:root {{--bg:#0d1117;--card:#161b22;--line:#30363d;--txt:#e6edf3;--mut:#8b949e;
--grn:#3fb950;--amb:#d29922;--blu:#58a6ff;--pur:#bc8cff;}}
* {{box-sizing:border-box}} body {{background:var(--bg);color:var(--txt);
font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;margin:0;padding:24px;max-width:960px;margin-inline:auto}}
h1 {{font-size:1.8rem;margin:0 0 4px}} .sub {{color:var(--mut);margin-bottom:20px}}
.hero {{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px;margin-bottom:20px}}
.lvl {{font-size:1.2rem;margin-bottom:8px}} .bar {{background:#21262d;border-radius:8px;height:22px;overflow:hidden}}
.fill {{background:linear-gradient(90deg,var(--blu),var(--pur));height:100%;width:{pct}%;transition:width .4s}}
.meta {{display:flex;justify-content:space-between;color:var(--mut);margin-top:6px;font-size:.9rem}}
.badges {{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}}
.badge {{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px;text-align:center;filter:grayscale(1);opacity:.55}}
.badge.earned {{filter:none;opacity:1;border-color:var(--grn)}}
.b-emoji {{font-size:2rem}} .b-name {{font-weight:600;margin-top:4px}} .b-state {{color:var(--mut);font-size:.8rem}}
.phase {{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin-bottom:14px}}
.phase.locked {{opacity:.6}} .phase header {{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.phase h2 {{font-size:1.05rem;margin:0;flex:1}} .p-xp {{color:var(--mut);font-size:.85rem}}
ul {{list-style:none;margin:0;padding:0}} .quest {{display:flex;gap:10px;align-items:center;
padding:7px 4px;border-top:1px solid var(--line);font-size:.95rem}}
.quest.locked {{color:var(--mut)}} .quest.in_progress {{color:var(--txt)}}
.quest.done {{color:var(--txt)}} .quest.done .q-title {{text-decoration:line-through}}
.q-id {{font-family:ui-monospace,monospace;color:var(--blu);min-width:44px}}
.q-title {{flex:1}} .q-xp {{color:var(--mut);font-size:.85rem;white-space:nowrap}}
.q-link {{color:inherit;text-decoration:none;border-bottom:1px dotted var(--mut)}}
.q-link:hover {{color:var(--blu);border-bottom-color:var(--blu)}}
#qsearch{{width:100%;background:var(--card);border:1px solid var(--line);border-radius:8px;
color:var(--txt);padding:10px 14px;font-size:.95rem;margin:4px 0 14px}}
table {{width:100%;border-collapse:collapse;font-size:.9rem}} td,th {{padding:6px 8px;border-top:1px solid var(--line);text-align:left}}
.muted {{color:var(--mut)}} footer {{color:var(--mut);font-size:.85rem;margin-top:20px}}
code {{background:#21262d;padding:2px 6px;border-radius:6px}}
</style>
</head>
<body>
<h1>☁️ Cloud Dojo — Journey Dashboard</h1>
<div class="sub">Docker from scratch + AWS basics · gamified · {esc(xp)} XP earned</div>
<div class="hero">
<div class="lvl">Level — <b>{esc(level)}</b></div>
<div class="bar"><div class="fill"></div></div>
<div class="meta"><span>{esc(xp)} / {esc(total)} XP ({pct}%)</span><span>{nxt_text}</span></div>
</div>
<h2>Badges</h2>
<div class="badges">{"".join(badge_cards)}</div>
<h2>Phases &amp; Quests</h2>
<input id="qsearch" placeholder="Filter 57 quests (e.g. lambda, iam, volumes)..." autocomplete="off">
{"".join(phase_cards)}
<h2>XP Log</h2>
<div class="hero"><table><tr><th>Date</th><th>Quest</th><th>XP</th><th>Total</th></tr>{log_rows}</table></div>
<footer>Click any quest title to open its styled concept page. Update <code>shared/progress.json</code>, then re-run <code>python3 shared/render_dashboard.py</code> to refresh this page.</footer>
<script>
var box=document.getElementById("qsearch");
box.addEventListener("input",function(){{
var t=box.value.toLowerCase();
document.querySelectorAll(".phase").forEach(function(ph){{
var any=false;
ph.querySelectorAll(".quest").forEach(function(q){{
var hit=q.textContent.toLowerCase().indexOf(t)>=0;
q.style.display=hit?"":"none";
if(hit){{any=true;}}
}});
ph.style.display=any?"":"none";
}});
}});
</script>
</body>
</html>
""")
    render_quest_pages(data)
    print(f"dashboard.html rendered: {xp}/{total} XP, level '{level}'")


if __name__ == "__main__":
    main()
