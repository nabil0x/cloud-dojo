# T.3 — Least privilege + MFA (25 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
Least privilege means granting only the actions on only the resources that are actually needed.
Instead of starting from a wildcard and subtracting, you start from nothing and add the single permission required.
In this quest you write a custom policy that allows exactly one action on one resource, then attach it to a user.
You also turn on multi-factor authentication, the second factor that protects sign-in even if a password leaks.
Real AWS enforces both: a tight policy really does block everything outside its scope, and MFA really does gate access.
This is the discipline emulators never taught you, because they allow almost everything by default.

## Uses
- Limiting the blast radius when a credential or application is compromised.
- Meeting compliance requirements that demand scoped access and MFA.
- Granting service accounts the minimum they need to run.
- Reviewing existing policies and trimming wildcards down to real needs.
- Building the habit of writing a denial test alongside every grant.

## Key info
- Custom policy: a JSON document with `Effect`, `Action`, and `Resource`. Example: allow `s3:GetObject` only on `arn:aws:s3:::dojo-bucket/*`.
- Attach it to a user or role, then test both the allowed action and a neighboring denied action.
- Enable MFA for the user and confirm the MFA status shows as enabled.
- The wildcard `*` in actions or resources is the enemy of least privilege.
- `aws:MultiFactorAuthPresent` can enforce MFA inside a policy for sensitive actions.
- This is real AWS only. The emulator does not enforce the policy you write.
- Use the IAM policy simulator to check a policy before you attach it to anyone.
- Grant the action, not the whole service: `s3:GetObject` is not `s3:*`.

## Pitfalls
- Using `"Resource": "*"` and calling it least privilege.
- Testing only the granted action and never confirming that something else is denied.
- Enabling MFA but never enrolling a device, so the user is locked out or left unprotected.

## Done check
paste the policy JSON + the MFA status line.

## Links
- Grant least privilege: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege
- MFA in IAM: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html
- IAM JSON policy reference: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html
