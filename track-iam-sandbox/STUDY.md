# Track T — Study Guide: IAM, Billing & What Emulators Hide

This is the only track that runs on **real AWS**. Everything here is true
in a way emulator behavior is not.

## 1. The IAM model (learn this cold)
- **Principals**: users (people), roles (assumed by services/code, temporary credentials), groups (bundles of users — attach policies to groups, never to individual users).
- **Policies**: JSON documents listing `Effect` (Allow/Deny), `Action` (`s3:GetObject`), `Resource` (ARNs). Explicit **Deny always beats Allow**.
- **Evaluation**: every API call is checked. No policy allowing it → implicit deny. This enforcement is exactly what emulators skip (Moto: auth off; LocalStack: permissive unless Pro + `ENFORCE_IAM=1`).
- **Least privilege**: grant only the actions on only the resources needed. Start from nothing, add grants — never start from `*` and subtract.

## 2. Roles vs users (the distinction that matters most)
- Humans get **users** (+ MFA, no exceptions). Code/services get **roles** (Lambda execution role, EC2 instance profile) — temporary credentials, auto-rotated, no long-lived keys to leak.
- Access keys on a human user are a smell. If T.2 tempts you to create one, note why and prefer console/SSO sign-in.

## 3. ARNs, MFA, boundaries
- **ARN** (`arn:aws:s3:::dojo-bucket/*`): the precise address of anything. Policies live and die by ARN precision.
- **MFA**: second factor on sign-in; also enforceable *inside* policies (`aws:MultiFactorAuthPresent`) for sensitive actions.
- Know the words even before you need them: permission boundaries, SCPs (organization-level guardrails), policy simulator. You'll meet them the week least privilege gets hard.

## 4. Billing: the surprise-bill rogues' gallery
| Culprit | Why it bites learners |
|---|---|
| NAT Gateway | ~$0.045/hr + data fee, 24/7 — ~$32+/mo idle. #1 killer. |
| Idle Elastic IP | Charged when allocated but unattached. |
| Outbound data transfer | ~$0.09/GB after the free 1 GB. Inbound is free. |
| EBS on stopped EC2 | Stopped ≠ deleted; volumes keep billing. |
| Public IPv4 | Charged since Feb 2024, easy to overlook. |
| CloudWatch Logs | Ingestion + storage with no retention policy grows silently. |

## 5. Your safety net (do this in every account, first)
1. **$1 budget + alert** → email the moment spend starts.
2. **Billing alarm** via CloudWatch (us-east-1) on estimated charges.
3. **Cost Anomaly Detection** → automatic "this is unusual" emails.
4. Tag everything; **delete after each session**. Sandboxes auto-clean — real accounts don't.

## 6. Shared responsibility (one paragraph)
AWS secures *the cloud* (hardware, hypervisor, managed-service patching). You secure *what's in it* (your data, IAM, security groups, keys, app code). Every breach postmortem you've ever read is someone failing the second half.

## 7. Secrets, keys, and parameters (T.5–T.6)
- **Secrets Manager**: passwords/tokens with rotation built in. Code reads at runtime; humans (and repos) never see values. Rotation without downtime is the skill, not storage.
- **SSM Parameter Store**: config hierarchy (`/prod/db/host`); `SecureString` type encrypts values under a **KMS key**. Cheap, simple, enough for most config.
- **KMS + envelope encryption**: data keys encrypt data, master keys encrypt data keys. You mostly need the vocabulary (key policies vs IAM policies both gate access — either can deny) and the habit: encrypt by default, scope decrypt narrowly.

## 8. Observability that pages you (T.7)
- **Metrics** (numbers over time: errors, duration, throttles) → **alarms** (threshold + action) → **dashboards** (the wall of truth). Logs are for forensics (Logs Insights queries); metrics are for alerting.
- Alarm on symptoms that page a human (error rate, p99 latency), not on every wiggle. An alarm nobody trusts gets muted, then it's decoration.

## 9. API authorization (T.8)
- **JWT authorizer**: validates bearer tokens (Cognito, Auth0...) before Lambda runs — no code, no cost on rejects. **IAM authorizer**: SigV4-signed calls, AWS-native. **Lambda authorizer**: custom logic when neither fits.
- Throttling + quotas at the gateway protect everything behind it (including your Bedrock bill). Auth first, throttle second, validate third — that order.

## Further reading (official, short)
- IAM concepts + least privilege — https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Free Tier + billing alarms — https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/checklistforunwantedcharges.html
- Builder Center Sandbox (free, no card) — https://aws.amazon.com/about-aws/whats-new/2026/07/aws-builder-center-sandbox
