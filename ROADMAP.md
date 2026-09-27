# Cloud Dojo — Full Roadmap

Docker from scratch + AWS basics, practiced through local emulators.
Lessons have NOT started — this file is the map. We play phase by phase.

## Phase map

| # | Folder | Theme | Skills unlocked | XP |
|---|---|---|---|---|
| 0 | `phase-00-docker-foundations/` | Docker foundations | install, `run`, ports, logs, lifecycle, Dockerfile, layers/cache | 100 |
| 1 | `phase-01-aws-first-services/` | First AWS services + Docker storage/network | S3, SQS/SNS, DynamoDB via CLI; volumes, env vars, bridge DNS | 150 |
| 2 | `phase-02-compose/` | Compose capstone | multi-container stack, service DNS, seed scripts, rebuild loop | 150 |
| 3 | `phase-03-lambda-images/` | Lambda container images | build Lambda image, local ECR push, create + invoke, event trigger | 150 |
| T | `track-iam-sandbox/` | Real-AWS parallel track (IAM/security/billing) | IAM, Secrets/KMS/SSM, observability, API auth, budgets | 200 |
| 6 | `phase-06-terraform-iac/` | Infrastructure as code | HCL, plan/apply, state, import, multi-resource | 150 |
| 7 | `phase-07-cicd-ecs/` | Ship it: pipeline + Fargate | Actions, ECR, task defs, deploy + teardown | 150 |
| 8 | `phase-08-rag-capstone/` | Grandmaster build (final) | Design, RAG eval, hardened API, IaC+CI, demo+retro | 200 |
| M | `module-moto-testing/` | Testing AWS code (standalone) | pytest + mock_aws, fixtures, server mode | 50 |
| 4 | `phase-04-ec2-vpc-rds/` | Real compute + networking + DB | EC2, VPC/SGs, AMIs/EBS, RDS Postgres, teardown discipline | 150 |
| 5 | `phase-05-bedrock-sagemaker/` | AI services (real AWS) | Bedrock invoke + RAG, SageMaker train + endpoint, cost audit | 150 |

**Total: 1600 XP.** Badges: one per phase + track, plus module + capstone (see `GAME-RULES.md`).

## Phase 0 — Docker foundations (100 XP)
Goal: run any container with confidence.
- Q0.1 Install + `hello-world` (10)
- Q0.2 Run the emulator container (15)
- Q0.3 Ports, logs, stop/rm lifecycle (15)
- Q0.4 Write + build a Dockerfile (20)
- Q0.5 Layers and build cache (20)
- Q0.6 Boss: run emulator on a custom port with a name you choose (20)
- Exit: you can explain image vs container in one sentence each.

## Phase 1 — First AWS services (150 XP)
Goal: create real-feeling S3/SQS/DynamoDB resources with the AWS CLI.
- Q1.1 CLI config + S3 buckets/objects (30)
- Q1.2 SQS queues + SNS topics (30)
- Q1.3 DynamoDB table + CRUD (30)
- Q1.4 Volumes: persist emulator state across restarts (30)
- Q1.5 Env vars: `AWS_ENDPOINT_URL` + dummy creds (15)
- Q1.6 Bridge network: container-to-container DNS (15)
- Exit: bucket + queue + table created, listed, and deleted by you.

## Phase 2 — Compose capstone (150 XP)
Goal: emulator + your app as one stack.
- Q2.1 `compose up` the emulator (30)
- Q2.2 Add the app service (40)
- Q2.3 Fix service DNS (`http://emulator:4566`, never `localhost`) (30)
- Q2.4 Seed script: bucket/queue/table on demand (25)
- Q2.5 Boss: full rebuild + verify loop (25)
- Exit: `docker compose up --build` gives a working app → emulator path.

## Phase 3 — Lambda container images (150 XP)
Goal: ship serverless code as a Docker image.
- Q3.1 Build a Lambda image from an AWS base image (40)
- Q3.2 Push it to the emulator's local ECR (40)
- Q3.3 Create + invoke the function (40)
- Q3.4 Wire an event trigger (S3 or SQS → Lambda) (30)
- Exit: an image you built runs as a function and fires on an event.

## Track T — Real-AWS parallel track (100 XP, anytime)
Goal: cover what emulators can't teach (IAM enforcement, console, billing).
- T.1 Claim a free sandbox (Builder Center Sandbox / Skill Builder) (20)
- T.2 IAM users, groups, policies (30)
- T.3 Least privilege + MFA (25)
- T.4 Budgets, billing alarm, Cost Anomaly Detection (25)
- Exit: you can explain why emulator IAM is not real IAM.

## Phase 4 — EC2 + VPC + RDS (150 XP)
Goal: real VMs, real networking, real database — then a clean teardown.
- Q4.1 VPC anatomy: default VPC, subnets, routes, IGW (30)
- Q4.2 Launch EC2 + scoped security groups + SSH (40)
- Q4.3 AMIs, EBS, stop/start billing lesson (25)
- Q4.4 RDS Postgres with SG-to-SG access (30)
- Q4.5 👹 Boss: nuke everything + $0 proof (25)
- Exit: you can explain SGs vs NACLs and what bills while stopped.

## Phase 5 — Bedrock + SageMaker (150 XP)
Goal: API-first AI, grounded answers, trained + deployed model — then a cost audit.
- Q5.1 First model call: temperature comparison (30)
- Q5.2 Ground it: Knowledge Base / hand-rolled RAG (35)
- Q5.3 SageMaker training run + artifact in S3 (35)
- Q5.4 Deploy endpoint, invoke, delete immediately (25)
- Q5.5 👹 Boss: $0 audit + per-unit cost notes (25)
- Exit: you can price tokens, endpoints, and training before creating them.

## Phase 6 — Terraform IaC (150 XP)
Goal: versioned infrastructure; plan before apply, destroy when done.
- Q6.1 First config: provider + bucket on emulator (30)
- Q6.2 Variables + outputs (25)
- Q6.3 State: list, show, import (30)
- Q6.4 Multi-resource apply (35)
- Q6.5 👹 Boss: destroy + clean proof (30)
- Exit: you read plans like code reviews.

## Phase 7 — CI/CD + ECS (150 XP)
Goal: push code, pipeline ships it to Fargate.
- Q7.1 Prod-ready image + ECR push (25)
- Q7.2 Pipeline: build + test, red then green (35)
- Q7.3 Pipeline pushes to ECR by SHA (30)
- Q7.4 Fargate service, live (35)
- Q7.5 👹 Boss: push-to-deploy + teardown (25)
- Exit: commit-to-live in under 10 minutes, $0 left behind.

## Phase 8 — RAG Capstone (200 XP, final)
Goal: designed, shipped, demoed, demolished AI system.
- Q8.1 Design doc + 3-scale cost table (30)
- Q8.2 Data + retrieval, 5-question eval (40)
- Q8.3 Hardened API: auth, throttle, CORS (40)
- Q8.4 Everything in Terraform via pipeline (50)
- Q8.5 👹 Boss: demo + demolish + retrospective (40)
- Exit: a portfolio piece with DESIGN.md + RETRO.md.

## Module M — Moto Testing (50 XP, standalone)
Goal: fast offline tests for AWS-touching Python.
- M.1 First mocked test (15)
- M.2 Fixtures: DynamoDB + SQS (20)
- M.3 👹 Boss: server mode (15)
- Exit: you know what mocks prove and what they can't.

## Order of play
Phase 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7 → **8 (capstone)**, with Track T
running alongside from Phase 1 onward and Module M playable any time
after Phase 1. No skipping a boss fight.
