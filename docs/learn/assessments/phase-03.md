# Self-check — Lambda Container Images (no XP, honor system)

Score 7+ before the boss fight.

## 1. Why does the Dockerfile start `FROM public.ecr.aws/lambda/python:3.13` instead of a plain `python:3.13`?
<details><summary>Show answer</summary>
The Lambda base image ships the Runtime Interface Client. That piece is what turns an ordinary container into a function at runtime. Because it is present, your `CMD` only names the handler (`app.handler`) and you never write a server or entrypoint yourself. Plain Python gives you neither the client nor the event/response contract.
</details>

## 2. You invoke twice with the same payload. The first takes ~400 ms, the second ~30 ms. Why?
<details><summary>Show answer</summary>
The first call paid a cold start: the container had to spin up and initialize the runtime. The second reused the warm execution environment, so only your handler code ran. Cold starts come back on scale-up or after idle. Smaller images and lean dependencies shrink them.
</details>

## 3. You edit only `handler.py` and rebuild. Why do so few layers show as changed in `docker image history`?
<details><summary>Show answer</summary>
Docker caches layers. As long as the earlier instructions (base image, dependency install) are unchanged, those layers reuse cache. Only the layer that copies the handler is rebuilt. That is why the Dockerfile order matters: copy dependency files and install first, copy your fast-changing code last.
</details>

## 4. Q3.2 asks for the push output's `digest:` line, not the tag. Why is the digest the "truth"?
<details><summary>Show answer</summary>
Tags are mutable pointers: `:latest` can be repointed to a different image at any time. A digest (`sha256:...`) names one exact image permanently. Pasting the digest proves which bytes you actually pushed, so it is the trustworthy reference.
</details>

## 5. What breaks if you push an image built for arm64 but the function runtime expects amd64?
<details><summary>Show answer</summary>
The function fails at startup or invoke with an architecture mismatch error, because the instructions in the image cannot run on the host CPU. Read the error carefully, rebuild for the correct platform (`--platform linux/amd64` on Apple Silicon), and push again. The Dockerfile and push flow themselves were fine.
</details>

## 6. Why does `create-function --package-type Image` not need `--handler` or `--runtime`?
<details><summary>Show answer</summary>
With the Image package type, the image itself already declares the handler and runtime: the base image supplies the runtime, and your `CMD` names the handler. Passing `--handler`/`--runtime` is for the zip packaging mode, where the platform has to be told what to run.
</details>

## 7. What breaks if your function reads from SQS and writes to DynamoDB without being idempotent?
<details><summary>Show answer</summary>
SQS can deliver the same message more than once (at-least-once delivery). Without idempotency your handler processes it twice, so you get duplicate records, double charges, or double emails. Make writes idempotent (for example, upsert keyed by message ID) so a repeat is harmless.
</details>

## 8. On the emulator the execution role is decorative. What is it doing on real AWS?
<details><summary>Show answer</summary>
The execution role is the IAM role Lambda assumes to run your function. The function can only touch what that role allows, and every call is checked. Emulators skip this enforcement, which is why behavior there can hide real `AccessDenied` failures. Track T shows the difference.
</details>

## 9. Predict what happens when a function needs 20 minutes but the maximum execution time is 15 minutes.
<details><summary>Show answer</summary>
It is killed at the 15-minute limit and returns a timeout error. The fix is design, not a bigger timeout: split the work, hand long jobs to a queue with continuation, or move them to a service built for long runs. Lambda functions must be short.
</details>

## 10. Why must Lambda functions be stateless, and where does state go instead?
<details><summary>Show answer</summary>
Each invocation may land on a fresh or recycled environment, so anything held in memory or on local disk cannot be trusted to survive to the next call. State belongs in S3, DynamoDB, or another durable store, which also makes the function safe to run in parallel.
</details>
