# M.1 — First mocked test (15 XP)

**Phase:** Module M — Moto Testing

## Concept
Moto is an in-process mock library that intercepts boto3 and botocore calls and serves them from memory. With the `@mock_aws` decorator, your AWS-touching code runs against a fake S3 with no network, no account, and millisecond speed.

You write a small function that creates a bucket and uploads a file, then test it by creating the bucket, uploading, reading the object back, and asserting the bytes match. The point is to test your logic fast and offline, not to prove that AWS will behave. Keep the AWS code behind thin functions so the test stays tiny.

## Uses
- Run a fast unit-test suite for AWS code on every save.
- Test S3 upload and download logic with no credentials or internet.
- Exercise error paths that are hard to trigger against real AWS.
- Keep CI cheap and deterministic with no cloud dependency.
- Catch regressions in your own glue code before integration tests.

## Key info
- Install the pieces: `pip install 'moto[s3]' pytest boto3`.
- Decorate the test function with `@mock_aws`.
- Inside the mock, `boto3.client("s3", region_name="us-east-1")` works with no real creds.
- Keep functions thin: create, upload, read, so tests stay short.
- Assert on behavior, for example "the object reads back with the same bytes", not on mock internals.
- The test file must be under 30 lines to count for this quest.
- A context-manager form exists too: `with mock_aws(): ...`.
- Coverage is per-operation; check your service before trusting it.
- `@mock_aws` covers S3, SQS, SNS, DynamoDB, and 160+ other services.
- Use `with mock_aws():` as a context manager when a decorator isn't convenient.
- Keep the AWS-touching function in its own module so the test imports it cleanly.

## Pitfalls
- Forgetting `@mock_aws`, so calls try real AWS and fail or hang on missing credentials.
- Testing mock internals instead of your own code's behavior, which breaks the moment you swap harnesses.
- Believing a green mock proves AWS will behave the same; it doesn't, which is exactly what M.3 addresses.

## Done check
paste `pytest -v` showing 1 passed + the test file (under 30 lines to count).

## Links
- Moto getting started — https://docs.getmoto.org/en/latest/docs/getting_started.html
- moto mock_aws API — https://docs.getmoto.org/en/latest/docs/moto_api.html
- pytest documentation — https://docs.pytest.org/en/stable/
