# T.2 — IAM users, groups, policies (30 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
IAM decides who can do what on real AWS, and unlike an emulator it actually says no.
You model people as users, organize them with groups, and grant permissions by attaching policies to the group rather than to each user.
A policy is a JSON document that lists an effect (Allow or Deny), actions, and resources.
To prove the model, you create a group with one managed policy, add a user, sign in as that user, and confirm an allowed call works.
Then you detach the policy and confirm the same call fails with `AccessDenied`.
That two-sided proof, allowed then denied, is the whole quest. Seeing the denial is what teaches you IAM is real here.

## Uses
- Onboarding teammates with the right access and nothing more.
- Centralizing permissions in groups so users inherit access cleanly.
- Auditing who can touch which resources through attached policies.
- Reproducing least-privilege mistakes and their fixes on real infrastructure.
- Understanding the exact error a service hits when a permission is missing.

## Key info
- Create a group: `aws iam create-group --group-name dojo-readers`
- Create a user: `aws iam create-user --user-name dojo-alice`
- Add to group: `aws iam add-user-to-group --group-name dojo-readers --user-name dojo-alice`
- Attach a managed policy: `aws iam attach-group-policy --group-name dojo-readers --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess`
- Prove access, then `detach-group-policy` and prove it fails with `AccessDenied`.
- Explicit Deny always beats Allow, and a missing permission is an implicit deny.
- This is real AWS only. The emulator does not evaluate policies, so nothing here would fail there.

## Pitfalls
- Attaching policies to individual users instead of groups, which does not scale and hides why access exists.
- Creating long-lived access keys for a human user. Prefer console or SSO sign-in and give keys to roles, not people.
- Removing the policy but testing with an old cached session, so the denial does not appear immediately.

## Done check
paste the allowed call output AND the explicit `AccessDenied` error. Both halves count.

## Links
- IAM best practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- IAM policies and permissions: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html
- IAM policy evaluation logic: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
