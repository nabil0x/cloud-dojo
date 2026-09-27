# Cloud Dojo — Game Rules

## XP
- Every quest states its XP. Quest counts only when its **Done check** passes.
- Log XP with `python3 shared/progress.py check <ID>` (or the interactive menu) —
  it records the log, unlocks the next quest, and refreshes the dashboard. No log, no XP.

## Levels
| Level | Title | XP range |
|---|---|---|
| 1 | Cloud Cadet | 0–99 |
| 2 | Container Cadet | 100–249 |
| 3 | Bucket Builder | 250–399 |
| 4 | Compose Commander | 400–549 |
| 5 | Lambda Launcher | 550–749 |
| 6 | Cloud Captain | 750–999 |
| 7 | Platform Engineer | 1000–1299 |
| 8 | Dojo Master | 1300–1600 |

## Badges (one per phase/track)
- 🐳 Container Cadet — finish Phase 0 boss (Q0.6)
- 🪣 Bucket Builder — finish Phase 1 (all Q1.x)
- 🧩 Compose Commander — finish Phase 2 boss (Q2.5)
- ⚡ Lambda Launcher — finish Phase 3 (all Q3.x)
- 🛡️ IAM Initiate — finish Track T (all T.x)
- 🏗️ Cloud Architect — finish Phase 4 boss (Q4.5)
- 🤖 Model Wrangler — finish Phase 5 boss (Q5.5)
- 🧱 Stack Builder — finish Phase 6 boss (Q6.5)
- 🚀 Release Runner — finish Phase 7 boss (Q7.5)
- 🏆 Grandmaster — finish the capstone boss (Q8.5)
- 🧪 Test Pilot — finish Module M boss (M.3)
- 🔐 Vault Keeper — finish Track T+ (all T.5–T.8)

## Rules
1. **Quests in order.** No skipping ahead inside a phase.
2. **Boss fights gate phases.** You cannot start the next phase until the boss is done.
3. **Verify, don't claim.** Each quest has a Done check (a command with expected output). Paste the output to claim XP.
4. **Break it once per phase.** Deliberately break something (wrong port, `localhost` from a container, deleted volume) and fix it — that's where the learning lives.
5. **Track T is real AWS only.** IAM/billing quests never count on an emulator.
6. **Stuck > 20 minutes?** Ask for a hint — hints cost 0 XP, quitting costs everything.

## Session ritual
1. Open `PROGRESS.md`, note current XP/level.
2. Run `bash shared/check.sh` to confirm the playground is healthy.
3. Do the next quest. Paste Done-check output. Log XP.
