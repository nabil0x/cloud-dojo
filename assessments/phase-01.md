# Self-check — Phase 1: First AWS Services (no XP, honor system)

Score 7+ before the boss fight.

**1. S3 has no folders. What is a "path" like `images/cat.jpg` actually stored as?**
<details><summary>Show answer</summary>
A single object whose key is the string `images/cat.jpg`. The `/` characters only make keys look hierarchical; they are not directories. A bucket is a flat key to value store.
</details>

**2. A consumer receives an SQS message, then crashes before deleting it. What happens next?**
<details><summary>Show answer</summary>
After the visibility timeout expires, the message becomes visible again and another consumer can receive it. This is at-least-once delivery, which is why your consumer must be idempotent.
</details>

**3. Why must you delete an SQS message only after processing succeeds?**
<details><summary>Show answer</summary>
Delete confirms the message was handled. If you delete first and processing then fails, the work is lost forever. Delete last, so a failure lets the message return and be retried.
</details>

**4. What problem does a dead-letter queue (DLQ) solve?**
<details><summary>Show answer</summary>
A message that cannot be processed keeps getting received and returned. After the maximum receives, the DLQ moves it aside for inspection instead of poisoning the queue forever.
</details>

**5. You publish to an SNS topic with no subscribers. Where does the message go?**
<details><summary>Show answer</summary>
Nowhere. SNS does not store messages. It broadcasts to subscriptions at publish time, so with no subscribers the message is dropped.
</details>

**6. Describe the SNS to SQS fan-out pattern and why you would use it.**
<details><summary>Show answer</summary>
One SNS topic has several SQS queues subscribed to it. A single publish is delivered to every subscribed queue, so multiple independent consumers each get their own copy of one event.
</details>

**7. What breaks if one DynamoDB partition key gets all the traffic?**
<details><summary>Show answer</summary>
You get a hot partition. The partition key decides which storage node owns the item, so one key taking all traffic overloads a single node while others sit idle, and throughput suffers. Spread traffic across many key values.
</details>

**8. Which read is cheap and which is expensive: `get-item`, `query`, `scan`? Why?**
<details><summary>Show answer</summary>
`get-item` is cheapest (one key lookup). `query` reads one partition, sorted, so it is efficient. `scan` reads the whole table, so it is expensive; fine for learning, alarming in production.
</details>

**9. What breaks if the emulator container restarts without a volume?**
<details><summary>Show answer</summary>
All state is gone, because the emulator kept its data in the container writable layer, which dies with the container. Buckets, queues, and tables vanish. Mount a named volume at the emulator data path to survive restarts.
</details>

**10. From inside a second container, you set `AWS_ENDPOINT_URL=http://localhost:4566`. Why does it fail, and what is the fix?**
<details><summary>Show answer</summary>
Inside that container, `localhost` means the container itself, not the emulator. There is nothing on 4566 there. Fix it by using the emulator's container name on the shared bridge network, for example `http://emulator:4566`.
</details>

**11. You exported `AWS_ENDPOINT_URL` but also pass `--endpoint-url` on one command. Which wins?**
<details><summary>Show answer</summary>
The explicit flag wins. Precedence runs explicit flags and parameters first, then environment variables, then config files, then defaults.
</details>

**12. The emulator accepts fake `test`/`test` credentials. Why does this not mean credentials are always irrelevant?**
<details><summary>Show answer</summary>
The emulator does not authenticate, so any credentials pass. Real AWS does authenticate and authorize, and that is the whole subject of the real-AWS track. Fake creds are a local convenience, not a general truth.
</details>
