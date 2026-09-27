# Phase 5 — Study Guide: Bedrock + SageMaker

Shipping AI features: API-first models, grounding, training, deployment — and the bills each creates.

## 1. Bedrock: foundation models as an API
- **Models on tap**: Claude, Llama, Mistral, Titan, Nova — invoked like any AWS API, no GPUs to manage. Some models need one-time **access requests** per region.
- **Inference parameters**: `temperature` (randomness; 0 = deterministic), `top_p`, `max_tokens` (cost + latency cap). Q5.1 makes you *feel* temperature instead of memorizing it.
- **Pricing**: per 1k input/output tokens, varies wildly by model. azure-sized habit: always check the per-model rate before bulk jobs. Output tokens cost more than input.
- **Knowledge Bases + Agents**: managed RAG (Bedrock chunks/embeds/searches your S3 data) and tool-using agents. Use them before hand-rolling retrieval — then hand-roll once to learn what's inside.

## 2. RAG in one paragraph (Q5.2's theory)
- Retrieval-Augmented Generation = **retrieve** relevant chunks (丐embeddings + vector search) → **stuff** them into the prompt → **generate** a grounded answer. Kills hallucination on private data without fine-tuning.
- Failure modes to recognize: wrong chunks retrieved (embedding/search problem), right chunks but ignored (prompt problem), stale index (pipeline problem). Diagnose in that order.

## 3. SageMaker: the full ML platform
- **Studio / notebook instances**: dev environments with instance-type muscle. Stop them when you stop working — they bill like EC2.
- **Training jobs**: managed, metered compute: submit script + data (S3) + instance type → metrics + model artifact back in S3. Spot/managed-spot can cut costs sharply.
- **JumpStart**: prebuilt models + notebooks for fine-tune/deploy — the fastest way to Q5.3 without writing training loops.
- **Endpoints**: real-time inference behind autoscaling. Billed per instance-hour **while they exist**, idle or not. Hence Q5.4's delete-immediately rule.
- **Batch Transform** (know the name): offline inference over S3 datasets, no persistent endpoint — cheaper whenever real-time isn't required.

## 4. Data plumbing for ML on AWS (vocabulary)
- **S3**: cheap lake for datasets/artifacts. **EFS**: shared POSIX filesystem for notebooks. **FSx for Lustre**: HPC-speed training I/O — fast, expensive, for serious training throughput.
- **Glue/Athena**: catalog + SQL over S3 for dataset exploration before you ever train.

## 5. Cost discipline (the phase's real lesson)
- Tokens (Bedrock), instance-hours (endpoints, notebooks, training), storage (artifacts, snapshots). Three meters, all running until you stop them.
- Ritual: before creating anything billable, note its rate; after deleting, verify in billing. Q5.5 turns this into a graded quest so it becomes reflex.

## Further reading (official, short)
- Bedrock concepts + inference params — https://docs.aws.amazon.com/bedrock/latest/userguide/
- RAG with Knowledge Bases — https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- SageMaker training + endpoints — https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-training.html
