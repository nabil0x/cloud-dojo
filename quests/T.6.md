# T.6 — KMS + SSM Parameter Store (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
Not every value is a secret, but plenty of config still deserves encryption.
KMS manages customer master keys, and SSM Parameter Store holds configuration values in a hierarchy, with a `SecureString` type that encrypts the value under a KMS key.
In this quest you create a KMS key, store a config value as a `SecureString` encrypted under it, and grant decrypt to exactly one role.
Then you prove a different role gets denied.
Both the key policy and IAM policies can gate access, and either can deny.
This is real IAM enforcement. The emulator allows the read for everyone; real AWS does not, which is why this quest lives only on real AWS.

## Uses
- Storing environment config like database hosts and feature flags without hardcoding.
- Encrypting configuration values under a key you control.
- Scoping decryption so only one service can read a sensitive parameter.
- Centralizing config for many services in one hierarchy.
- Rotating a key or revoking decrypt access to cut off a compromised service.

## Key info
- Create a key: `aws kms create-key`, and note the key ID and ARN.
- Store config: `aws ssm put-parameter --name /dojo/db/host --value db.internal --type SecureString --key-id <key-id>`
- Read it back: `aws ssm get-parameter --name /dojo/db/host --with-decryption`
- Grant the one allowed role `kms:Decrypt` on the key ARN, plus `ssm:GetParameter`.
- Prove a second role without the grant receives `AccessDenied`.
- Parameter Store hierarchy uses paths like `/prod/db/host`; `SecureString` is the encrypted type.
- Envelope encryption is the mental model: a KMS data key encrypts the value, and the master key protects the data key.
- Grant decrypt per key ARN, so one role cannot read another team's parameters.

## Pitfalls
- Storing a `SecureString` but only granting `ssm:GetParameter` without `kms:Decrypt`, so reads fail.
- Granting decrypt to a wildcard principal, which erases the point of a single-role scope.
- Confusing `String` with `SecureString` and accidentally storing plaintext.

## Done check
paste the allowed read + the `AccessDenied` from the wrong role. This is real IAM enforcement — emulator can't do this.

## Links
- KMS overview: https://docs.aws.amazon.com/kms/latest/developerguide/overview.html
- Parameter Store: https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html
- KMS key policies: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
