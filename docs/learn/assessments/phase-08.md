# Self-check — RAG Capstone (no XP, honor system)

Score 7+ before the boss fight.

## 1. Before writing code, what flows does the design doc require you to draw, and what justifies an arrow?

<details><summary>Show answer</summary>
Three flows: data flow (where docs live, how they're indexed, what answers), request flow (client to gateway to function to KB to model and back), and failure flow (KB down, model throttled, auth fails). Every arrow needs a one-line justification, like "SQS between API and indexer because ingestion spikes 100x at upload." If you can't justify an arrow, delete the box.
</details>

## 2. Your system is cheap at 100 requests but ruinous at 1M. Why is this common, and when do you need to know it?

<details><summary>Show answer</summary>
Because unit economics (cents per request) multiply, and the cost driver at scale is rarely the one that dominates at tiny volume: model tokens and endpoint hours compound fast. Systems that look cheap at 100 requests and collapse at 1M are the norm. You need to know which kind yours is before the demo, not after the bill.
</details>

## 3. What breaks if you skip the failure-flow diagram?

<details><summary>Show answer</summary>
You design for the happy path and discover the failure modes live, in front of an audience. KB down, model throttled, and auth failures each need a planned response (retry, fallback, clear error). Drawing them first surfaces the gaps while they're cheap to fix. If it isn't drawn, it isn't handled.
</details>

## 4. Chunking: what breaks if chunks are too big, and what breaks if they're too small?

<details><summary>Show answer</summary>
Too big dilutes the match: the retriever returns a wall of text where the answer is buried and the model gets noisy context. Too small strips context: the chunk no longer means anything on its own. The sane starting range is 300 to 800 tokens with overlap. Chunking strategy matters more than the embedding model.
</details>

## 5. Why is a 5-question eval set graded honestly better than vibes, and what does fewer than 4 of 5 grounded mean?

<details><summary>Show answer</summary>
A small, written eval set beats vibes because it's repeatable: future-you reruns it after every change to catch regressions. Fewer than 4 of 5 grounded means the retrieval or the prompt needs rework, not a pass. Keep it in the repo as `eval.md` so it survives past the demo.
</details>

## 6. Name the four API hardening items. What breaks if CORS is `*` with credentials, and if throttling is missing?

<details><summary>Show answer</summary>
Auth (authorizer on every route: JWT or IAM), throttling (per-route rate limits plus quotas), CORS (exact origins, never `*` with credentials), and validation (max input length and request schemas). `*` with credentials lets any origin call your authenticated API. Missing throttling invites abuse, and Bedrock costs scale directly with abuse.
</details>

## 7. Timeouts cascade: gateway 29s, function 15 min max, model call. What breaks if you leave the defaults in place?

<details><summary>Show answer</summary>
The layers disagree. The gateway caps at 29 seconds, so a function allowed to run longer than that can keep working after the client has already gotten a timeout error. Set each layer deliberately, with the model call inside the function's budget, or the defaults surprise you mid-demo.
</details>

## 8. Why is destroy-and-rebuild-from-CI the only real proof your IaC is complete? What breaks if you rebuild by hand?

<details><summary>Show answer</summary>
If the system comes back from CI after a full destroy, everything needed to run it is truly in code. Anything rebuilt by hand is tech debt with a demo date: it works once, has no source of truth, and can't be reproduced by anyone else. The rebuild is the test.
</details>

## 9. You pin model IDs, container SHAs, and provider versions. What breaks if `latest` appears anywhere?

<details><summary>Show answer</summary>
`latest` means "works today, mystery tomorrow." The system can change under you between runs with no code change, so a working demo becomes unreproducible and bugs can't be traced to a version. Pinning is what makes the rebuild byte-for-byte.
</details>

## 10. For the demo you write expected answers before asking. Why, and what do hiring managers actually read afterward?

<details><summary>Show answer</summary>
Writing the expected answer first turns the demo into a test rather than a performance: you know whether the system passed or you got lucky. Include one adversarial prompt-injection question ("ignore your instructions"), because handling it gracefully is the point. Afterward, hiring managers read `RETRO.md`, not your architecture: what broke, estimate-versus-actual cost, and one thing you would redesign.
</details>
