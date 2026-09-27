# Phase 2 — Compose Capstone (150 XP)

**Status:** 🔒 locked — unlocks after Phase 1.
**Goal:** emulator + your app as one `docker compose` stack.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Files here:** `compose.yaml` (the stack), `app/` (your service).

## Quests

### Q2.1 Stack up the emulator (30 XP)
1. `cd phase-02-compose && docker compose up -d emulator`
2. `curl -s http://localhost:4566/_ministack/health`
- **Done check:** paste the health JSON + `docker compose ps`.

### Q2.2 Add the app service (40 XP)
1. Read `app/app.py` + `app/Dockerfile` (already scaffolded).
2. `docker compose up -d --build`, then `curl localhost:8080/health` and `curl localhost:8080/s3`.
- **Done check:** paste both responses.

### Q2.3 The DNS lesson (30 XP)
1. Break it on purpose: set the app's `AWS_ENDPOINT_URL` to `http://localhost:4566`, rebuild, watch `/s3` fail.
2. Fix it back to `http://emulator:4566`, rebuild, watch it pass.
- **Done check:** paste the failing response + the passing response, and one sentence on why.

### Q2.4 Seed on demand (25 XP)
1. With the stack up, run `bash ../shared/seed.sh` from the host.
2. `curl localhost:8080/s3` must now list `dojo-bucket`.
- **Done check:** paste the `/s3` response showing the bucket.

### Q2.5 👹 Boss: full rebuild loop (25 XP, badge 🧩)
1. `docker compose down -v` (everything gone, including volumes).
2. `docker compose up -d --build` + re-seed + verify `/health` and `/s3`.
- **Done check:** paste all three outputs in order. Time yourself — under 3 minutes is the par.

## Swap note
Default emulator is MiniStack (no signup). To use LocalStack instead:
image → `localstack/localstack`, add `LOCALSTACK_AUTH_TOKEN`, keep port 4566.
The app does not change — that is the lesson.
