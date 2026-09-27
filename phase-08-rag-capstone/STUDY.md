# Phase 8 — Study Guide: Capstone Engineering

This phase isn't new services — it's **judgment**: scoping, costing, securing, shipping, and cleaning up a real system.

## 1. Architecture thinking (Q8.1)
- Draw boxes before writing code: data flow (where docs live → how they're indexed → what answers), request flow (client → gateway → function → KB → model → back), failure flow (KB down? model throttled? auth fails?).
- Every arrow needs a justification ("SQS between API and indexer because ingestion spikes 100x at upload time"). If you can't justify an arrow, delete the box.
- Cost table discipline: unit economics (¢/request) at 3 scales. Systems that are cheap at 100 requests and ruinous at 1M are the norm — know which yours is *before* the demo.

## 2. Retrieval quality is the product (Q8.2)
- Chunking strategy matters more than the embedding model: too big = diluted, too small = context-free. 300–800 tokens with overlap is the sane starting range.
- 5-question eval set, graded honestly, beats vibes. Keep it in the repo (`eval.md`) — future-you reruns it after every change.
- Metadata filtering (source, date, doc type) turns "search everything" into "search the right thing."

## 3. API hardening checklist (Q8.3)
- **Auth**: authorizer on every route (JWT or IAM). **Throttling**: per-route rate limits + quotas (Bedrock costs scale with abuse). **CORS**: exact origins, never `*` with credentials. **Validation**: max input length (tokens = money), request schemas.
- Timeouts cascade: gateway (29s max) < function (15 min max, set far lower) < model call. Set each deliberately or the defaults will surprise you mid-demo.

## 4. Reproducibility = professionalism (Q8.4)
- Destroy + rebuild from CI is the only proof your IaC is complete. Anything rebuilt by hand is tech debt with a demo date.
- Pin everything: model IDs, container SHAs, provider versions. `latest` anywhere means "works today, mystery tomorrow."

## 5. Demos and retros (Q8.5)
- Demo script: 3 questions (easy, hard, adversarial), each with the expected answer written down *before* you ask. Adversarial prompt-injection attempts belong in the demo — handling them gracefully is the point.
- `RETRO.md` honestly > perfect system: what broke, estimate-vs-actual cost, one thing you'd redesign. Hiring managers read retros; they skim architectures.

## Further reading (official, short)
- Bedrock Knowledge Bases + Agents — https://docs.aws.amazon.com/bedrock/latest/userguide/
- API Gateway HTTP APIs + authorizers — https://docs.aws.amazon.com/apigateway/latest/developerguide/
- AWS Well-Architected (Cost + Reliability pillars, skim) — https://docs.aws.amazon.com/well-architected/
