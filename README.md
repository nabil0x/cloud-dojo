# ☁️ Cloud Dojo — Learn Docker & AWS Hands-On (Gamified DevOps Course)

[![GitHub stars](https://img.shields.io/github/stars/nabil0x/cloud-dojo?style=social)](https://github.com/nabil0x/cloud-dojo)
[![License: MIT](https://img.shields.io/github/license/nabil0x/cloud-dojo)](LICENSE)
[![1600 XP](https://img.shields.io/badge/XP-1600-blueviolet)](ROADMAP.md)
[![57 quests](https://img.shields.io/badge/quests-57-blue)](ROADMAP.md)

**Learn Docker from scratch and AWS basics by running AWS locally — free, no AWS account needed.** A gamified, quest-based DevOps tutorial: 8 phases + a real-AWS track covering S3, EC2, Lambda, DynamoDB, SQS, VPC, RDS, Terraform, CI/CD with GitHub Actions and ECS, plus Bedrock and SageMaker for AI engineers — practiced hands-on with local AWS emulators (MiniStack, LocalStack, Moto).

<img src="docs/images/dashboard.png" width="700" alt="Cloud Dojo journey dashboard">

*Track 1600 XP across 8 phases on the dashboard — every quest title opens a concept page like this:*

<img src="docs/images/quest-page.png" width="700" alt="Quest concept page">

## Who is this for
- **Beginners** learning Docker from scratch and AWS fundamentals without surprise bills
- **Software engineers** going intermediate: Terraform, CI/CD, containers on ECS
- **AI engineers** who need Bedrock, SageMaker, S3 data lakes, and GPU instances without the ops maze

## What you'll learn
Docker (images, volumes, networks, Compose) → AWS core (IAM, S3, EC2, VPC, RDS, DynamoDB, Lambda, SQS/SNS) → infrastructure as code (Terraform) → shipping (GitHub Actions, ECR, ECS Fargate) → AI on AWS (Bedrock RAG, SageMaker training/endpoints) → a portfolio-ready RAG chatbot capstone.

**⭐ If this helps you learn, star the repo — it keeps the dojo alive.**

## Start here
1. Read `GAME-RULES.md` (2 min) — XP, levels, badges.
2. Read `ROADMAP.md` (5 min) — all 4 phases + the parallel IAM track.
3. Track yourself with `python3 shared/progress.py` — interactive check menu
   (`status`, `check Q0.1`, `uncheck Q0.1`, `reset`); it updates the dashboard for you.
4. **We begin at Phase 0 together when you say go.** Nothing is started yet.

## The map
| Phase | Folder | XP | Status |
|---|---|---|---|
| 0 — Docker foundations | `phase-00-docker-foundations/` | 100 | 🔒 locked |
| 1 — First AWS services | `phase-01-aws-first-services/` | 150 | 🔒 locked |
| 2 — Compose capstone | `phase-02-compose/` | 150 | 🔒 locked |
| 3 — Lambda container images | `phase-03-lambda-images/` | 150 | 🔒 locked |
| T — Real-AWS track (IAM/billing) | `track-iam-sandbox/` | 200 | 🔒 locked |
| 6 — Terraform IaC | `phase-06-terraform-iac/` | 150 | 🔒 locked |
| 7 — CI/CD + ECS | `phase-07-cicd-ecs/` | 150 | 🔒 locked |
| 8 — RAG capstone (final) | `phase-08-rag-capstone/` | 200 | 🔒 locked |
| M — Moto testing (standalone) | `module-moto-testing/` | 50 | 🔒 locked |
| 4 — EC2 + VPC + RDS | `phase-04-ec2-vpc-rds/` | 150 | 🔒 locked |
| 5 — Bedrock + SageMaker | `phase-05-bedrock-sagemaker/` | 150 | 🔒 locked |

## 📊 Journey dashboard
Open `dashboard.html` in your browser — XP bar, level, badges, and every quest.
It's generated from `shared/progress.json`: update that file, then re-run
`python3 shared/render_dashboard.py` to refresh.

## Prerequisites (install before Phase 0)
- Docker (Desktop on Mac/Windows, Engine on Linux)
- AWS CLI v2 (`aws --version`)
- `curl`

## Playground health check
```bash
bash shared/check.sh
```

## The one-sentence mental model
Your app talks to `http://localhost:4566` from your laptop,
but to `http://emulator:4566` from inside a container —
that single distinction is half of this entire course.

## FAQ
**Do I need an AWS account?** No for Phases 0–3, 6 and Module M (local emulators). Yes — a free sandbox, not your own card — for IAM, EC2, Bedrock and anything that bills.

**How long does it take?** Roughly 4–8 weeks at a few hours per week. Each phase is independently finishable.

**LocalStack vs MiniStack vs Moto — which one?** All three work here (same port, same endpoint pattern). Start with MiniStack (zero signup), use LocalStack for max fidelity, Moto for Python tests. The course swaps between them in one line.

**Will I get billed?** Not if you follow the teardown bosses (Q4.5, Q5.5, Q7.5, Q8.5) — every billable phase ends in a graded $0 audit.

**How is progress tracked?** `python3 shared/progress.py` — check quests, earn XP/badges, watch `dashboard.html` update.

## Contribute
Ideas, quests, fixes — see [CONTRIBUTING.md](CONTRIBUTING.md). PRs that teach something new get merged fast. 🥋
