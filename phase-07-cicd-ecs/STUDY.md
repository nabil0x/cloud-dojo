# Phase 7 — Study Guide: CI/CD + ECS

From "runs on my laptop" to "ships itself."

## 1. CI/CD in one paragraph
- **CI**: every push builds + tests in a clean room. Red means "don't merge," not "works on mine."
- **CD**: every green main-branch build ships (or stages for approval). Artifacts are immutable (git-SHA tags, never moving `:latest` for deploys).
- The pipeline is code (`.github/workflows/*.yml`): triggers → jobs → steps. Read failed logs top-down; the first error is usually the only real one.

## 2. Images for production (Q7.1's checklist)
- **Pinned tags** (`python:3.13-slim`, never `latest`), **non-root USER**, **`.dockerignore`** (no `.git`, no secrets, smaller context), **HEALTHCHECK** (orchestrator knows dead from alive).
- Multi-stage builds (defer from Phase 0, use now): build deps in one stage, ship only runtime in the final stage. Smaller image = faster deploys + smaller attack surface.

## 3. ECR + pipeline auth
- `aws ecr get-login-password --region X | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com` — the standard incantation; in Actions, prefer **OIDC role assumption** over long-lived keys (no secrets to leak).
- Tag every build with the commit SHA (`myapp:abc1234`) plus a moving tag if you like. Rollback = redeploy the previous SHA. That's the whole release strategy at this scale.

## 4. ECS on Fargate (vocabulary)
- **Cluster** (logical pool) → **task definition** (image + CPU/RAM + env + log config — versioned, immutable revisions) → **service** (desired count of tasks, keeps N running) → **task** (one running container set).
- **Fargate** = serverless containers (no EC2 to manage); **EC2 launch type** = you manage the hosts (cheaper at scale, more ops). Start Fargate.
- Task roles (what the container may call) vs execution roles (what ECS needs to pull images/write logs) — IAM separation again (Track T pays off here).
- Logs go to CloudWatch by default (`awslogs` driver) — debugging a dead task starts in the log group, not in the console's green dots.

## 5. Deploy + teardown economics
- Fargate bills per vCPU/GB-second while tasks run; ALBs/ECR storage/NAT add up. The Q7.5 teardown (scale 0 → delete) exists because a forgotten service is a subscription you didn't sign up for.
- `desiredCount: 0` stops billing for tasks while keeping the config — useful mid-project; full delete at phase end.

## Further reading (official, short)
- GitHub Actions workflow syntax — https://docs.github.com/en/actions/reference/workflows/workflow-syntax-for-github-actions
- ECS task definitions + Fargate — https://docs.aws.amazon.com/AmazonECS/latest/developerguide/
- ECR push flow — https://docs.aws.amazon.com/ecr/latest/userguide/docker-push-ecr-image.html
