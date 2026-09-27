# Self-check — Real-AWS Track (IAM, Billing & Observability) (no XP, honor system)

Score 7+ before the boss fight.

## 1. Why can't Track T be done on an emulator?
<details><summary>Show answer</summary>
Because emulators do not enforce IAM, do not bill, and do not quota. Moto leaves auth off; LocalStack is permissive unless you are on Pro with `ENFORCE_IAM=1`. The whole point of this track is to feel the enforcement and the money that emulators cannot reproduce.
</details>

## 2. One policy allows `s3:*`. Another policy denies `s3:GetObject`. What happens on `GetObject`?
<details><summary>Show answer</summary>
The call is denied. An explicit Deny always beats an Allow. This is why least privilege policies must be written carefully: an accidental deny in a broad policy silently breaks access no matter how many allows exist.
</details>

## 3. What happens to an API call that no policy allows?
<details><summary>Show answer</summary>
It is denied by implicit deny. Every call is checked, and if no policy allows it, the default is deny. There is no "unset means allowed" state. This is exactly the enforcement step emulators skip.
</details>

## 4. Why do humans get users but code gets roles?
<details><summary>Show answer</summary>
Users are people and should sign in with MFA, ideally no long-lived access keys. Roles are assumed by services and code, handing out temporary, auto-rotated credentials with nothing long-lived to leak. A Lambda execution role or EC2 instance profile is a role for this reason. Access keys on a human user are a smell.
</details>

## 5. What breaks if a role tries to read a `SecureString` parameter encrypted under a KMS key it cannot decrypt?
<details><summary>Show answer</summary>
The read fails with `AccessDenied`, even if the parameter-read permission is present, because KMS decrypt is a separate authorization. T.6 makes you grant decrypt to exactly one role and prove a different role is denied. Encryption by default, decrypt scoped narrowly.
</details>

## 6. What breaks if you hardcode a database password in your Lambda code instead of using Secrets Manager?
<details><summary>Show answer</summary>
The secret lives in the repo, the deployment package, and every environment it touches, and you cannot rotate it without a code change and redeploy. Secrets Manager stores it out of band and rotates it while code reads it at runtime. T.5 proves rotation works with zero downtime: the old value stops, the function keeps working.
</details>

## 7. Why is the NAT gateway called the number one surprise-bill killer?
<details><summary>Show answer</summary>
It charges roughly $0.045/hour plus a data fee, running 24/7, so an idle one is about $32+/month even with no traffic. It is the top of the rogues' gallery for learners: easy to create, easy to forget, hard to notice until the bill.
</details>

## 8. What breaks if CloudWatch Logs has no retention policy?
<details><summary>Show answer</summary>
logs accumulate forever, so ingestion and storage charges grow silently and never stop. Set a retention policy so old logs expire. Storage you never look at is still storage you pay for.
</details>

## 9. What does least privilege mean as a starting point, not a slogan?
<details><summary>Show answer</summary>
Start from nothing and add only the actions on only the resources needed. Never start from `*` and subtract. Policies live and die by ARN precision, so scope the Resource field tightly instead of granting a wildcard.
</details>

## 10. Which two safety nets should every real account have before anything else?
<details><summary>Show answer</summary>
A $1 budget with an alert (email the moment spend starts, plus Cost Anomaly Detection) and a CloudWatch billing alarm on estimated charges in us-east-1. Together they turn a silent bill into a message. Tag everything and delete after each session, because sandboxes auto-clean but real accounts do not.
</details>
