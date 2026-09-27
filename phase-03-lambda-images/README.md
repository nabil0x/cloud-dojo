# Phase 3 — Lambda Container Images (150 XP)

**Status:** 🔒 locked — unlocks after the Phase 2 boss.
**Goal:** ship serverless code as a Docker image and run it as a function.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Note:** this phase runs smoothest on LocalStack; MiniStack/Floci equivalents
are flagged per quest. The Dockerfile and push pattern are identical everywhere.
**Starter files:** `lambda/handler.py` + `lambda/Dockerfile` (+ `.dockerignore`) — build on them, don't start blank.

## Quests

### Q3.1 Build a Lambda image (40 XP)
1. Create `lambda/` with a handler (`def handler(event, context): ... return {"ok": True}`)
   and a Dockerfile starting `FROM public.ecr.aws/lambda/python:3.13`.
2. `docker build -t dojo-lambda .` — observe how few layers change when only the handler edits.
- **Done check:** paste `docker images | grep dojo-lambda` + `docker image history dojo-lambda --format '{{.CreatedBy}}'` (first 5 lines).

### Q3.2 Push to the local ECR (40 XP)
1. Create repo `dojo-lambda` in the emulator's ECR.
2. Tag `dojo-lambda` for the local registry (`localhost.localstack.cloud:4510/...` on LocalStack) and push.
- **Done check:** paste the push output's final `digest:` line.

### Q3.3 Create + invoke (40 XP)
1. `create-function --package-type Image --code ImageUri=<your pushed URI>`.
2. `invoke` it with a test payload and read the response.
- **Done check:** paste the invoke response JSON.

### Q3.4 Wire an event trigger (30 XP, badge ⚡)
1. Connect SQS `dojo-queue` (or an S3 event) to your function as a trigger.
2. Send a message / upload a file and prove the function fired (logs or a DynamoDB write).
- **Done check:** paste the trigger evidence (log line or the written item).

**Break-it bonus (rule #4):** push an image built for the wrong architecture
(arm64 vs amd64) and read the error carefully before rebuilding.
Note the fix in `PROGRESS.md`.
