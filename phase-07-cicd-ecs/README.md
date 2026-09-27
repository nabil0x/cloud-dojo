# Phase 7 — CI/CD + ECS (150 XP)

**Status:** 🔒 locked — unlocks after Phase 6.
**Goal:** push code, watch a pipeline ship it to managed containers.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** GitHub repo (free Actions minutes) + sandbox for ECS/ECR. Fargate tasks bill while running — teardown is Q7.5.
**Starter files:** `.github/workflows/ci.yml` skeleton (triggers done, steps are TODOs) — the TODOs ARE the quests.

## Quests

### Q7.1 Prod-ready image + ECR (25 XP)
1. Harden the Phase 2 app image: pinned base tag, non-root `USER`, `.dockerignore`, `HEALTHCHECK`.
2. Create a real ECR repo in the sandbox, `aws ecr get-login-password | docker login`, push `:v1`.
- **Done check:** paste the push digest + the ECR console/CLI image listing.

### Q7.2 Pipeline: build + test on push (35 XP)
1. Add `.github/workflows/ci.yml`: on push → checkout → build image → run unit tests (even trivial ones) → fail loudly on purpose once.
2. Fix, watch green.
- **Done check:** paste the red run URL/title + the green run URL/title. Both are required evidence.

### Q7.3 Pipeline pushes to ECR (30 XP)
1. Extend the workflow: OIDC or access-key auth to AWS, build, tag with git SHA, push to your ECR repo.
2. Push a commit changing one string in the app; verify the new SHA-tagged image appears.
- **Done check:** paste the workflow log lines showing login + push + the new tag in ECR.

### Q7.4 Fargate service, live (35 XP)
1. ECS cluster + task definition (your image, 0.25 vCPU / 0.5 GB) + Fargate service (1 task) + CloudWatch log group. Terraform from Phase 6 encouraged.
2. Reach the task (public IP / ENI) and hit `/health` + `/s3` (pointed at sandbox emulator? No — point at real sandbox S3 or stub; note your choice).
- **Done check:** paste the `curl` outputs from the *live* task + `aws ecs describe-services` showing `runningCount: 1`.

### Q7.5 👹 Boss: push-to-deploy + teardown (25 XP, badge 🚀)
1. Change the app, push, watch the pipeline redeploy (new task revision serving).
2. Then scale service to 0, delete service/cluster/task-def, verify billing clean.
- **Done check:** paste the deploy log tail + the post-teardown `list-services` (empty) + billing note. Par: commit-to-live under 10 minutes, $0 left behind.

**Standing rule for this phase:** every deploy goes through the pipeline. `docker push` or console-click deploys from your laptop don't count and will be mocked.
