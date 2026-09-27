# Self-check — Module M: Moto Testing (no XP, honor system)

Score 7+ before the boss fight.

**1. What is Moto, and what does `@mock_aws` actually do?**
<details><summary>Show answer</summary>
Moto is an in-process mock library. `@mock_aws` intercepts boto3 and botocore calls and serves them from memory. There is no network, no AWS account, and tests run in milliseconds.
</details>

**2. Moto covers 165 services. What does that coverage actually mean?**
<details><summary>Show answer</summary>
It means the API operations are implemented, not that behavior is faithful. S3, SQS, SNS, and DynamoDB behave convincingly; IAM is not enforced; Lambda does not really execute. Coverage is not fidelity.
</details>

**3. A test asserts against Moto internals instead of observable behavior. What breaks later?**
<details><summary>Show answer</summary>
The test is coupled to the mock, so it fails or misleads when you swap Moto for the emulator or real AWS. Assert on behavior instead: the object reads back, the message is received. Tests should survive swapping mock to emulator to real, modulo the endpoint.
</details>

**4. What is the classic isolation mistake with mocks, and its consequence?**
<details><summary>Show answer</summary>
Using a module-scoped mock instead of one per test. State leaks between tests, so a passing test can depend on what an earlier test created. Fixture-per-test gives isolation.
</details>

**5. Name at least four things a green Moto suite cannot prove.**
<details><summary>Show answer</summary>
IAM enforcement, eventual consistency, quotas and limits, networking, real Lambda execution, and Terraform or CDK behavior (no HTTP layer in decorator mode). Every green suite carries these blind spots.
</details>

**6. What breaks if you treat "all tests green" as proof AWS will behave the same way?**
<details><summary>Show answer</summary>
The mock only proves your logic is correct, not that AWS is faithful to it. Real AWS may enforce IAM, apply limits, or behave under eventual consistency in ways the mock never simulated. Validate against the emulator or a sandbox before trusting it.
</details>

**7. Server mode: how does the same boto3 code hit `motoserver/moto`?**
<details><summary>Show answer</summary>
Run the `motoserver/moto` image in Docker (for example `-p 5000:5000`) and point boto3 at it with `endpoint_url`. The server speaks the AWS wire protocol over HTTP, so no other test-code change is needed.
</details>

**8. When do you use decorator mode and when server mode?**
<details><summary>Show answer</summary>
Decorator mode for the fast TDD inner loop. Server mode in CI when other languages or containers join, or when you want a more realistic HTTP boundary. Use the emulator or a sandbox before any claim about real AWS behavior.
</details>

**9. Why should AWS-touching code live behind thin functions?**
<details><summary>Show answer</summary>
So tests stay small, fast, and focused on behavior. Thin create, upload, and read functions are easy to cover and easy to repoint at a different endpoint later.
</details>

**10. M.1: what three packages do you install, and why special-case the extra?**
<details><summary>Show answer</summary>
`moto[s3]`, `pytest`, and `boto3`. The `[s3]` extra pulls the dependencies Moto needs to mock S3 specifically, rather than installing every service's requirements.
</details>
