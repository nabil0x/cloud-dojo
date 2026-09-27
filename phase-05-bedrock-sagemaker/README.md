# Phase 5 — Bedrock + SageMaker (150 XP)

**Status:** 🔒 locked — unlocks after Phase 4.
**Goal:** call foundation models via API, ground one with your data, train/deploy in SageMaker — then delete every billable resource.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** ⚠️ **real AWS only** (sandbox with Bedrock access). Endpoints and training jobs bill by the minute — the teardown quests are load-bearing, not ceremonial.

## Quests

### Q5.1 First model call (30 XP)
1. In Bedrock console, request access to one chat model (e.g. Claude/Sonnet or Llama) if required in your region.
2. Invoke it twice via API/CLI: same prompt, different `temperature` (0 vs 1) and `max_tokens`. Compare.
- **Done check:** paste both responses (truncated) + one sentence on what temperature changed.

### Q5.2 Ground it with your data (35 XP)
1. Put 2–3 text files (course notes work great) in S3.
2. Build a Bedrock Knowledge Base over them (or hand-roll RAG: retrieve chunks yourself, stuff into the prompt) and ask a question only your files can answer.
- **Done check:** paste the grounded answer + the source chunk it cited. Ungrounded answers don't count.

### Q5.3 SageMaker training run (35 XP)
1. Open SageMaker Studio (or a notebook instance), run a small training job — a JumpStart fine-tune or a toy PyTorch script on a tiny dataset.
2. Track one metric (loss curve, even a bad one). Save the model artifact to S3.
- **Done check:** paste the training job status (`Completed`) + the S3 path of the artifact.

### Q5.4 Deploy an endpoint, then kill it (25 XP)
1. Deploy the model to a real-time endpoint (smallest instance that fits).
2. Invoke it, record latency + output — then **delete the endpoint and its config immediately**.
- **Done check:** paste the invocation output + the endpoint-deleted confirmation. An endpoint left running fails this quest retroactively.

### Q5.5 👹 Boss: $0 audit (25 XP, badge 🤖)
1. Verify: no endpoints, no notebook instances running, no training jobs stuck `InProgress`, Knowledge Base data sources you understand.
2. Open billing: confirm $0 (or sandbox-clean) and write the per-unit costs you observed (per-1k-tokens, endpoint $/hr).
- **Done check:** paste the resource-cleanup checklist + the cost notes. This is the muscle that lets you experiment fearlessly forever.

**Standing rule for this phase:** endpoints and notebook instances are deleted the same session they're created. No exceptions, no "I'll do it tomorrow."
