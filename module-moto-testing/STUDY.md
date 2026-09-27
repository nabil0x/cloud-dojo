# Module M — Study Guide: Testing with Moto

Fast tests for code that touches AWS — and knowing what the tests *can't* prove.

## 1. What Moto is (and isn't)
- An **in-process mock library**: `@mock_aws` intercepts boto3/botocore calls and serves them from memory. No network, no account, millisecond tests.
- 165 services covered, but coverage = *API operations implemented*, not fidelity. S3/SQS/SNS/DynamoDB behave convincingly; IAM isn't enforced; Lambda doesn't really execute (needs Docker or stubs).
- Moto's own docs call LocalStack its "bigger brother" — mocks for unit speed, emulators for integration truth.

## 2. The test pattern (M.1–M.2)
- Decorator or context manager (`with mock_aws():`) or manual `.start()/.stop()` in fixtures. Fixture-per-test = isolation; module-scoped mocks = leakage roulette.
- Assert on *behavior* (object readable back, message received) not on mock internals. Tests should survive swapping mock → emulator → real (modulo endpoint).
- Keep AWS-touching code behind thin functions (create/upload/read) so tests stay small and the suite stays fast.

## 3. Server mode (M.3)
- `moto_server` / `motoserver/moto` image speaks the AWS wire protocol over HTTP — any SDK/language can hit it via `endpoint_url`. Same code, two harnesses: decorator for speed, server for realism.
- Decision rule: decorator for TDD inner loop; server mode in CI when other languages/containers join; emulator/sandbox before any claim about *AWS behavior*.

## 4. What mocks can't test (memorize this)
- IAM enforcement, eventual consistency, quotas/limits, networking, real Lambda execution, Terraform/CDK (no HTTP layer in decorator mode). Every green suite carries these blind spots — name them in the retro, don't discover them in production.

## Further reading (official, short)
- Moto getting started + server mode — https://docs.getmoto.org/en/latest/docs/getting_started.html
- Implementation coverage (check your service before trusting it) — https://github.com/getmoto/moto/blob/master/IMPLEMENTATION_COVERAGE.md
