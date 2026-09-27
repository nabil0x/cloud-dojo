# Agent Guidelines for cloud-dojo

Course repo: gamified Docker + AWS learning path. XP economy is load-bearing; do not inflate it casually.

## Source-of-truth files
- `shared/progress.json` — quests, XP, badges, log. Re-render with `python3 shared/render_dashboard.py`.
- `shared/progress.py` — check/uncheck/reset/status/menu CLI. Prefer it over hand-editing JSON.
- `ROADMAP.md` + `GAME-RULES.md` — phases, levels, badges. Changing XP totals requires updating levels, dashboard copy, and README badges together.

## Content conventions
- Quests: title, XP, steps, **Done check** (exact command + expected output). No output, no XP.
- Quest pages live in `quests/<ID>.md` (+ generated `.html`); sections: Concept / Uses / Key info / Pitfalls / Done check / Links.
- Self-checks in `assessments/` carry **no XP** (honor system); answers in `<details>` blocks.
- Study guides (`STUDY.md`) teach concepts; READMEs run quests. Never mix the two jobs.
- No real credentials anywhere (`test`/`test` only). Every billable phase ends in a teardown boss.

## Toolchain
- Python scripts are stdlib-only. Keep them that way.
- Validate course integrity: `python3 shared/validate_course.py`.
- Git: `GIT_MASTER=1` prefix on every command. Atomic commits per directory; no co-author trailers.
