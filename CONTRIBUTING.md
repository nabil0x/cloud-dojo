# Contributing to Cloud Dojo

## Ways to contribute
- New quests (with Done checks + XP), study guides, quest concept pages
- Better emulator coverage, new capstone ideas, typo fixes
- Awesome-list-grade polish: clearer explanations, better diagrams

## Quest authoring rules
1. Every quest needs: title, XP, steps, and a **Done check** (a command with expected output — no output, no XP).
2. Match the existing template in any phase `README.md` + `quests/<ID>.md` format (Concept / Uses / Key info / Pitfalls / Done check / Links).
3. Update `shared/progress.json` (new quest entry), then re-run `python3 shared/render_dashboard.py`.

## Workflow
1. Fork, branch, commit in small atomic units.
2. Open a PR describing what learners can now do that they couldn't before.

No real credentials, no billable resources left running, no AI-slop filler. Welcome to the dojo. 🥋
