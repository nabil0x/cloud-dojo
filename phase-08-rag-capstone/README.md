# Phase 8 — RAG Capstone: Grandmaster Build (200 XP)

**Status:** 🔒 locked — unlocks after Phase 7. This is the final boss of the dojo.
**Goal:** design, ship, demo, and demolish a complete AI system using everything you learned.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** real sandbox. Budget it like an adult (see Q8.1) and clean it like one (see Q8.5).

## The build
A grounded chatbot over your own documents: **S3** (docs) → **Bedrock Knowledge Base** (retrieval) → **Lambda** (orchestration) → **API Gateway** (HTTPS front door) → all declared in **Terraform**, all shipped via **CI/CD**.
**Templates:** `DESIGN.md`, `eval.md`, `RETRO.md` — graded deliverables, fill them for real.

## Quests

### Q8.1 Design doc + cost estimate (30 XP)
1. Write `DESIGN.md` (in this folder): architecture diagram (boxes + arrows), service choices with one-line justifications, and a **cost table** (per-request tokens, endpoint hours, storage) with a monthly estimate at 100/10k/1M requests.
2. Get it reviewed (paste it here — review is part of the quest).
- **Done check:** `DESIGN.md` committed + cost table with three scale rows.

### Q8.2 Data + retrieval (40 XP)
1. Curate 10+ real documents into S3 (course notes, docs, papers — not lorem ipsum).
2. Bedrock Knowledge Base over the bucket; prove retrieval quality with 5 test questions (relevant chunk cited each time).
- **Done check:** paste all 5 Q/A pairs with cited sources. Fewer than 4/5 grounded = rework, not XP.

### Q8.3 API: Lambda + Gateway (40 XP)
1. Lambda function: query → KB retrieve → model generate → JSON answer with citations.
2. API Gateway HTTP API in front, JWT or IAM authorizer (Track T.8 pays off), CORS configured, throttling set.
- **Done check:** paste `curl` of the live endpoint returning a cited answer + the auth-rejected `curl` (401/403) proving the gate works.

### Q8.4 IaC + pipeline (50 XP)
1. Everything from Q8.2–Q8.3 expressed in Terraform (Phase 6) and deployed through the Phase 7 pipeline.
2. `terraform destroy` + re-`apply` from CI reproduces the system byte-for-byte (test it once).
- **Done check:** paste the destroy log + the CI re-apply log + the post-rebuild `curl` still answering.

### Q8.5 👹 Boss: demo + demolish + retrospective (40 XP, badge 🏆)
1. Live demo: 3 questions, one adversarial ("ignore your instructions…"), all handled.
2. Full teardown: destroy, verify billing clean, archive `DESIGN.md` + retrospective (`RETRO.md`: what broke, cost vs estimate, what you'd change).
- **Done check:** demo transcript + `Destroy complete!` + `RETRO.md` committed. This is your portfolio piece — make it look like one.

**Standing rule for this phase:** no manual console creations. If it isn't in Terraform, it doesn't exist. The demo gods punish click-ops.
