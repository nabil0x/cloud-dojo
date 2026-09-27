# Curriculum Matrix — objectives, prerequisites, time

Each phase is independently finishable. Read the row before starting it.

| Phase | Objectives (you will be able to…) | Prerequisites | Est. time | Exit proof |
|---|---|---|---|---|
| 0 Docker foundations | run/stop/inspect any container; write a Dockerfile; read layer cache | Docker installed | 3–5 days | Q0.6 boss on a custom port |
| 1 First AWS services | CRUD S3/SQS/DynamoDB via CLI; persist with volumes; use bridge DNS | Phase 0 | 1 week | bucket + queue + table created and deleted by you |
| 2 Compose capstone | run emulator + app as one stack; debug service DNS; seed on demand | Phase 1 | 3–4 days | `up --build` gives working app → emulator path |
| 3 Lambda images | build/push/invoke image functions; wire event triggers | Phase 2 | 1 week | image you built fires on an event |
| M Moto testing | test AWS-touching Python offline; choose mock vs server mode | Phase 1 | 2–3 days | green suite against `moto_server` |
| 4 EC2/VPC/RDS | launch + network + scope a VM and database; tear down cleanly | Phase 1, free sandbox | 1 week | $0 bill + terminated resources |
| 5 Bedrock/SageMaker | invoke models; ground answers; train + deploy + delete | Phase 4, free sandbox | 1–2 weeks | $0 bill + cost notes |
| 6 Terraform | write/plan/apply/destroy infra; manage state; import | Phase 3 | 1 week | clean destroy + sandbox plan read |
| 7 CI/CD + ECS | pipeline build/test/push; Fargate deploy + teardown | Phase 6, GitHub account | 1 week | commit-to-live < 10 min, $0 left |
| 8 RAG capstone | design, cost, ship, demo, demolish a full AI system | Phases 5 + 7 | 2–3 weeks | live demo + `RETRO.md` + $0 |
| T Real-AWS track | enforce IAM for real; budget/alarm; read bills | Phase 1, free sandbox | alongside | explain why emulator IAM is fake |

Total path: roughly 8–12 weeks at a few hours per week.
