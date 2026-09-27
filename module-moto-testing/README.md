# Module M — Moto Testing (50 XP)

**Status:** 🔒 locked — unlocks after Phase 1. Small, sharp, standalone.
**Goal:** test AWS-touching Python code fast, offline, and free.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** your laptop. No emulator, no Docker needed (until M.3).

## Quests

### M.1 First mocked test (15 XP)
1. `pip install 'moto[s3]' pytest boto3`. Write a function that creates a bucket + uploads a file.
2. Test it with `@mock_aws`: create, upload, read back, assert bytes equal.
- **Done check:** paste `pytest -v` showing 1 passed + the test file (under 30 lines to count).

### M.2 Fixtures: DynamoDB + SQS (20 XP)
1. pytest fixture spinning up a table + queue per test; write tests for put/get and send/receive/delete.
2. Prove isolation: run the suite twice, everything green, no cross-test leakage.
- **Done check:** paste two consecutive `pytest` runs, both green.

### M.3 👹 Boss: server mode (15 XP, badge 🧪)
1. Run `motoserver/moto` in Docker (`-p 5000:5000`), point the *same* boto3 code at it via `endpoint_url`, run the suite unmocked against the server.
2. Write one paragraph: when to use decorator mode vs server mode.
- **Done check:** paste the green run against `http://localhost:5000` + your paragraph. Par: zero test-code changes besides the endpoint.

**Standing rule for this module:** mocks test *your* logic, not AWS. A green suite means your code is correct, not that AWS will behave — validate against the emulator/sandbox before trusting it (Phase 1 + Track T exist for exactly this).
