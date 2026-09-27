# T.5 — Secrets Manager: no hardcoded keys (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
Hardcoding passwords and keys into code or config is how secrets leak.
Secrets Manager stores those values centrally, encrypts them, and hands them to code at runtime with an IAM check on every read.
Your code never contains the value, and your repository never sees it.
In this quest you store a database password in Secrets Manager and read it back from a Lambda function, or from the CLI with a policy that allows it.
Then you rotate the secret once and prove the old value stops working while the function keeps reading the new one.
Rotation without downtime is the real skill here, not the storage. This runs on real AWS, never an emulator, because the IAM check is the whole point.

## Uses
- Keeping database credentials and API keys out of source control.
- Rotating secrets automatically without redeploying code.
- Auditing secret access through CloudTrail.
- Feeding application config to Lambda or containers at runtime.
- Reducing the blast radius when a key leaks, since rotation kills the old value.

## Key info
- Store a secret: `aws secretsmanager create-secret --name dojo/db --secret-string '{"password":"..."}'`
- Read it: `aws secretsmanager get-secret-value --secret-id dojo/db`
- Grant the reading role `secretsmanager:GetSecretValue` on the secret's ARN.
- Rotate: `aws secretsmanager rotate-secret --secret-id dojo/db`, or enable automatic rotation with a Lambda rotator.
- After rotation, the old value fails and the function still works with the new one.
- This is real AWS only. The emulator does not enforce the IAM read check that makes this meaningful.
- Retrieve the secret inside the handler at runtime, not at build time.
- Enable automatic rotation so the value changes on a schedule instead of on a bad day.

## Pitfalls
- Printing the secret value into logs or `out.json`, which defeats the point.
- Forgetting to grant `GetSecretValue`, so the function fails with `AccessDenied`.
- Caching the secret forever in memory and missing a rotation, which causes the outage rotation is supposed to prevent.

## Done check
paste the rotation output + the function's successful read post-rotation.

## Links
- Rotating secrets: https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html
- `get-secret-value` reference: https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/get-secret-value.html
- Secrets Manager best practices: https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html
