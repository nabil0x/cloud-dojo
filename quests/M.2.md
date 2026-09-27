# M.2 — Fixtures: DynamoDB + SQS (20 XP)

**Phase:** Module M — Moto Testing

## Concept
A pytest fixture sets up and tears down state around each test. Pair it with `@mock_aws` and you get a fresh DynamoDB table and SQS queue per test, so tests can't leak state into one another.

Fixture-per-test isolation is what makes a suite reliable when you run it twice in a row. You write tests for put and get on DynamoDB and send, receive, and delete on SQS, then prove isolation by running the whole suite twice green. If state leaked, the second run would fail.

## Uses
- Guarantee each test starts from a known, empty table and queue.
- Run tests in any order without hidden dependencies.
- Parallelize a suite without cross-test interference.
- Reuse the same setup across many tests with one fixture.
- Keep integration-style tests fast by mocking both services in-process.

## Key info
- Define setup with `@pytest.fixture`; create the table and queue, then `yield` the client.
- Scope fixtures to the function for isolation; module or session scope invites leakage.
- DynamoDB test: `put_item` then `get_item`, and assert the value round-trips.
- SQS test: `send_message`, `receive_message`, then `delete_message`, and assert the body.
- `@mock_aws` can decorate the test or wrap the body in `with mock_aws():`.
- Run `pytest` twice in a row; both runs must be green.
- Keep resource creation inside the fixture, never at import time.
- Handle an empty receive explicitly, since a message hides after the first read.
- `pytest -v` shows each test name and its pass or fail clearly.
- A fixture can create several resources before yielding; the mock resets per test.
- Assert exact bytes and message bodies, not just that a call returned something.

## Pitfalls
- Module- or session-scoped mocks keep state alive between tests and hide real bugs.
- Creating resources once outside the fixture makes test order affect the result.
- Forgetting to delete an SQS message after receiving it leaves it hidden, not gone, so the next read surprises you.

## Done check
paste two consecutive `pytest` runs, both green.

## Links
- Moto pytest fixtures — https://docs.getmoto.org/en/latest/docs/getting_started.html
- pytest fixtures reference — https://docs.pytest.org/en/stable/how-to/fixtures.html
- moto mock_aws API — https://docs.getmoto.org/en/latest/docs/moto_api.html
