# Self-check — Bedrock + SageMaker (no XP, honor system)

Score 7+ before the boss fight.

## 1. Same prompt, `temperature` 0 versus 1. Predict the difference.
<details><summary>Show answer</summary>
At 0 the model is deterministic: it picks the highest-probability next token every time, so repeated calls look near identical. At 1 it samples more freely, so answers vary and can drift. For factual or structured output you want low temperature; for brainstorming you want it higher.
</details>

## 2. Why is output usually more expensive than input on Bedrock?
<details><summary>Show answer</summary>
Bedrock prices per 1k input and output tokens, and output tokens cost more because generation is the compute-heavy part. That is why `max_tokens` caps both cost and latency: it limits how much the model is allowed to generate. Always check the per-model rate before a bulk job.
</details>

## 3. Put RAG in order, then name the three failure modes.
<details><summary>Show answer</summary>
Retrieve relevant chunks, stuff them into the prompt, then generate a grounded answer. Failure modes, diagnose in this order: wrong chunks retrieved (embedding or search problem), right chunks but ignored (prompt problem), stale index (pipeline problem). Fixing in that order avoids chasing the wrong layer.
</details>

## 4. Why does RAG reduce hallucination on private data better than fine-tuning here?
<details><summary>Show answer</summary>
RAG grounds the answer in the actual retrieved text at request time, so the model can cite what it read. Fine-tuning changes behavior and style but does not guarantee the model will know a specific fact, and it is slower and costlier to update. For private data, retrieve-and-stuff is the fast, honest path.
</details>

## 5. What breaks if you leave a real-time SageMaker endpoint running overnight?
<details><summary>Show answer</summary>
You keep paying per instance-hour the entire time, whether or not anyone calls it. Endpoints bill while they exist, idle included. That is why Q5.4 requires deleting the endpoint and its config in the same session, and why an endpoint left running fails the quest retroactively.
</details>

## 6. What breaks if a notebook instance is left running after you stop working?
<details><summary>Show answer</summary>
It bills like an EC2 instance, per hour, while running. The compute does not care that you walked away. Stop it when you stop working, and delete it when the phase is done.
</details>

## 7. In one sentence, what does a SageMaker training job hand back, and where does it land?
<details><summary>Show answer</summary>
You give it a script, data in S3, and an instance type; it hands back metrics and a model artifact (the trained model) written to S3. The job itself is metered compute that stops when the job finishes, unlike an endpoint. Spot or managed-spot capacity can cut the cost sharply.
</details>

## 8. When is Batch Transform cheaper than a real-time endpoint?
<details><summary>Show answer</summary>
Batch Transform runs offline inference over a dataset in S3 with no persistent endpoint, so you pay only for the job, not for idle instance-hours. Use it whenever you do not need instant per-request answers. Choose it the moment "real-time" stops being a requirement.
</details>

## 9. What breaks if `max_tokens` is set too low?
<details><summary>Show answer</summary>
The response gets truncated: the model stops mid-answer because it hit the cap before finishing. You may see a truncated flag or an incomplete-sounding reply. The cap is a cost and latency guard, but set it high enough for a full answer.
</details>

## 10. What breaks if your region has not granted access to a model you are calling?
<details><summary>Show answer</summary>
The invoke fails with an access or model-not-available error, because some Bedrock models require a one-time access request per region. Enable access in the console for that region, then retry. The request itself was fine; the permission was missing.
</details>
