# Phase 1 — First AWS Services (150 XP)

**Status:** 🔒 locked — unlocks after the Phase 0 boss.
**Goal:** create S3/SQS/DynamoDB resources with the AWS CLI against the emulator.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Prereq:** emulator on `http://localhost:4566`, env from `shared/.env.example`.

## Quests

### Q1.1 S3 buckets and objects (30 XP)
1. `aws --endpoint-url=http://localhost:4566 s3 mb s3://dojo-bucket`
2. Upload a file, list it, download it back, delete it.
- **Done check:** paste `aws --endpoint-url=... s3 ls s3://dojo-bucket` before and after delete.

### Q1.2 SQS queues + SNS topics (30 XP)
1. Create queue `dojo-queue`, send a message, receive it, delete it.
2. Create topic `dojo-topic`, subscribe the queue, publish, verify delivery.
- **Done check:** paste the received message JSON.

### Q1.3 DynamoDB table + CRUD (30 XP)
1. Create table `Dojo` (partition key `id`, `PAY_PER_REQUEST`).
2. `put-item`, `get-item`, `scan`, `delete-item`.
- **Done check:** paste the `get-item` output showing your item.

### Q1.4 Volumes: survive a restart (30 XP)
1. Restart the emulator container **without** a volume: observe data is gone.
2. Re-run with `-v dojo-data:/var/lib/localstack` (or the MiniStack data path), re-seed via `bash shared/seed.sh`, restart again: observe data survives.
- **Done check:** paste `s3 ls` after the second restart showing `dojo-bucket`.

### Q1.5 Env vars: the universal switch (15 XP)
1. Export `AWS_ENDPOINT_URL=http://localhost:4566` + fake creds + region.
2. Re-run a Q1.1 command **without** `--endpoint-url`.
- **Done check:** paste `env | grep AWS_` (redact nothing — all fake) + the working command.

### Q1.6 Bridge DNS: containers talking (15 XP)
1. `docker network create dojo-net`; attach the emulator; run a second container on the same network.
2. From the second container, reach the emulator **by container name** (not an IP).
- **Done check:** paste the successful `curl http://<name>:4566/_ministack/health` from inside the second container.

**Break-it bonus (rule #4):** delete the volume from Q1.4 on purpose and re-seed from scratch.
Note recovery time in `PROGRESS.md`.
