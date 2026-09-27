# Phase 3 — Study Guide: Lambda Container Images

Serverless compute, shipped as a Docker image you already know how to build.

## 1. Lambda execution model (30-second version)
- You upload code; AWS runs it **per event** (S3 upload, SQS message, HTTP request...). No servers to manage, billed per millisecond of execution.
- Each invocation gets a **handler** call: `handler(event, context)` — `event` is the trigger payload, `context` carries runtime info (time remaining, request ID).
- **Cold start**: first invocation (or scale-up) pays container-startup latency. Small images + lean dependencies = faster starts. This is where your Phase 0 layer knowledge pays off again.
- **Execution role**: the IAM role Lambda assumes — it can only touch what the role allows. (Real IAM; on the emulator it's decorative. Track T explains why that matters.)

## 2. Two packaging modes: zip vs image
- **Zip**: code + deps zipped, 250 MB limit. Simple, fine for small functions.
- **Image**: full container image (up to 10 GB), built `FROM public.ecr.aws/lambda/python:3.13` (or node/go/java variants). Needed for big dependencies, system packages, or — our case — learning the Docker↔serverless bridge.
- The base image provides the **Runtime Interface Client**: your `CMD` just names the handler (`app.handler`). Same Dockerfile skills, new base.

## 3. ECR — the registry piece
- **ECR (Elastic Container Registry)**: private Docker registry per AWS account/region. Flow is universal: `create-repository` → `tag` → `login` → `push` → reference by URI.
- Image URI shape: `<registry>/<repo>:<tag>`. Locally the emulator serves its own registry (LocalStack: `localhost.localstack.cloud:4510/...`).
- Tags are mutable pointers (`:latest` moves); **digests** (`sha256:...`) are the immutable truth. The Q3.2 Done check asks for the digest for exactly this reason.

## 4. Create + invoke + triggers
- `create-function --package-type Image --code ImageUri=<uri>`: registers the image as a function. No `--handler`/`--runtime` needed — the image declares them.
- `invoke --payload '{...}' out.json`: synchronous test call. The response + logs tell you what happened.
- **Event source mappings / triggers**: SQS queue → function (polling, batch size, DLQ on failure), S3 event → function (object created → process). Q3.4 wires one end-to-end: an event in one service causes code to run with zero servers involved.

## 5. Limits that shape design (real AWS)
- 15-minute max execution, 10 GB RAM, 512 MB–10 GB ephemeral storage, concurrency quotas. Functions must be short, stateless (state goes to S3/DynamoDB), and idempotent (SQS can deliver twice — Phase 1, §2 returns).

## Further reading (official, short)
- Lambda concepts + handler basics — https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html
- Lambda container images — https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
- ECR push/pull flow — https://docs.aws.amazon.com/ecr/latest/userguide/docker-push-ecr-image.html
