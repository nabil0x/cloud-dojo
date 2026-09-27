# M.3 👹 Boss: server mode (15 XP)

**Phase:** Module M — Moto Testing

## Concept
Decorator mode runs the mock inside your Python process; server mode runs Moto as a real HTTP server that any SDK can reach through `endpoint_url`. Running the `motoserver/moto` image in Docker on port 5000 lets you point the same boto3 code at `http://localhost:5000` and run the suite unmocked.

The code barely changes: the endpoint is the only difference. This proves your tests survive swapping a mock for a network service, and it's how you decide which harness to use. Decorator mode is for speed in the inner loop; server mode is for realism when other languages or containers join in.

## Uses
- Let non-Python services and other containers hit the same mock server.
- Run a shared fake AWS for a whole integration test job.
- Compare decorator and server behavior on identical test code.
- Test client code written in any language that speaks AWS APIs.
- Move from fast unit tests to a more realistic CI harness without rewriting logic.

## Key info
- Run the server: `docker run -d -p 5000:5000 motoserver/moto`.
- Point boto3 at it: `boto3.client("s3", endpoint_url="http://localhost:5000", aws_access_key_id="test", aws_secret_access_key="test", region_name="us-east-1")`.
- Run the same suite against the server with zero test-code changes besides the endpoint.
- Decorator mode is in-process and fastest; server mode is over HTTP and more realistic.
- Decision rule: decorator for TDD, server mode in CI with multiple languages or containers.
- Even server mode doesn't prove AWS behavior; validate against the emulator or a sandbox first.
- Write one paragraph explaining the tradeoff for the done check.
- `docker logs <container>` shows the requests the Moto server received.
- Server mode speaks the AWS wire protocol, so any SDK or language can use it.
- Keep the endpoint in one config value so switching harnesses is a one-line change.

## Pitfalls
- Changing test logic along with the endpoint, which defeats the whole point of parity.
- Assuming server mode covers IAM enforcement, quotas, or real Lambda execution; it doesn't.
- Leaving the container running on port 5000 and colliding with other local services.

## Done check
paste the green run against `http://localhost:5000` + your paragraph. Par: zero test-code changes besides the endpoint.

## Links
- Moto server mode — https://docs.getmoto.org/en/latest/docs/server_mode.html
- Moto implementation coverage — https://github.com/getmoto/moto/blob/master/IMPLEMENTATION_COVERAGE.md
- motoserver/moto image — https://hub.docker.com/r/motoserver/moto
