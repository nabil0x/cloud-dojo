# Phase 1 — Study Guide: First AWS Services

Concepts behind the S3 / SQS / SNS / DynamoDB quests, plus the Docker
storage/network ideas that make the emulator behave.

## 1. S3 — object storage
- **Buckets** (globally-unique names, regional) hold **objects** (key + bytes + metadata). No folders — keys with `/` only *look* hierarchical.
- Core ops: `mb/rb` (bucket), `put/get/delete` object, `ls`, `cp`, `sync`. Versioning, lifecycle rules, and presigned URLs exist on real AWS; the emulator covers buckets/objects faithfully.
- Mental model: an infinite key→value store where values can be gigabytes. Cheap, durable, slow-ish (milliseconds, not microseconds).

## 2. SQS — message queues
- **Producers** `send-message`, **consumers** `receive-message` → process → `delete-message`. Delete only *after* success, or the message returns.
- **Visibility timeout**: after receipt, a message hides for N seconds. Crash before delete → it reappears for someone else. This is at-least-once delivery, not exactly-once — your consumer must be idempotent.
- **DLQ (dead-letter queue)**: after max receives, the message moves aside for inspection instead of poisoning the queue forever.
- FIFO queues exist (ordering + dedup) but standard queues are the default to learn first.

## 3. SNS — pub/sub notifications
- **Topics** broadcast to **subscriptions** (SQS queues, Lambda functions, email...). One publish → many deliveries.
- Classic pattern you'll wire: SNS topic → SQS queue subscription (fan-out: one event, several queues).
- SNS doesn't store: if nobody is subscribed, the message goes nowhere.

## 4. DynamoDB — NoSQL key-value + documents
- **Table** with a **partition key** (`HASH`), optionally a **sort key** (`RANGE`). The partition key decides which storage node owns the item — hot partitions (one key getting all traffic) are the classic scaling failure.
- Reads: `get-item` (one key, fast) vs `query` (one partition, sorted) vs `scan` (whole table, expensive — fine for learning, alarming in production).
- `PAY_PER_REQUEST` (on-demand) vs provisioned capacity: on-demand for learning, provisioned when you can predict traffic and want to pay less.
- Items are schemaless JSON-ish; indexes (GSI/LSI) are how you query by non-key attributes.

## 5. Talking to the emulator: endpoint + credentials
- Every AWS SDK/CLI call needs three things: **endpoint** (where), **credentials** (who), **region** (which partition of the API).
- `AWS_ENDPOINT_URL=http://localhost:4566` redirects *all* services to the emulator. Per-service override: `AWS_ENDPOINT_URL_S3`, `..._DYNAMODB`, etc.
- Credentials here are fake (`test`/`test`) — the emulator doesn't authenticate. Real AWS does, and that's Track T's entire subject.
- Precedence refresher: explicit flags/params → env vars → config files → defaults.

## 6. Volumes: why data vanishes (and how to keep it)
- Container writable layers die with the container (Phase 0, §1). A **named volume** (`-v dojo-data:/path`) lives outside any container's lifecycle.
- Emulators keep state in a data directory; mounting a volume there = persistence across restarts. `docker compose down -v` deletes volumes — that's the nuke option, used deliberately in the Phase 2 boss.

## 7. Bridge networks and DNS
- Containers on the same **user-defined bridge** resolve each other **by name** (`curl http://emulator:4566`). Default bridge doesn't do this — always create your own (`docker network create`).
- The rule that runs the rest of the course: **host → `localhost:4566`, container → `<service-name>:4566`**.

## Further reading (official, short)
- S3 basics, SQS visibility timeout, DynamoDB core components — search each in https://docs.aws.amazon.com/ (the Concepts pages, not API refs).
- LocalStack/emulator endpoint pattern — https://docs.localstack.cloud/aws/getting-started/installation/
