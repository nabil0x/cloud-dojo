# Track T — Real-AWS Parallel Track (100 XP)

**Status:** 🔒 locked — runs alongside Phase 1 onward, real AWS only.
**Why this exists:** emulators don't enforce IAM, don't bill, and don't quota.
Everything here happens in a **free sandbox** (Builder Center Sandbox or
Skill Builder labs) — never in your main account, never on an emulator.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.

## Quests

### T.1 Claim your sandbox (20 XP)
1. Open the AWS Builder Center Sandbox (no account, no credit card) or a free Skill Builder lab.
2. Open the console, find IAM, S3, and the billing dashboard.
- **Done check:** paste the sandbox time-remaining notice + the console home region.

### T.2 IAM users, groups, policies (30 XP)
1. Create a group, a user, attach one managed policy to the group.
2. Sign in as the user and prove access works — then remove the policy and prove it fails.
- **Done check:** paste the allowed call output AND the explicit `AccessDenied` error. Both halves count.

### T.3 Least privilege + MFA (25 XP)
1. Write a custom policy allowing exactly one action on one resource.
2. Enable MFA on the user.
- **Done check:** paste the policy JSON + the MFA status line.

### T.4 Budgets and alarms (25 XP, badge 🛡️)
1. Create a $1 budget with an alert, enable Cost Anomaly Detection.
2. List the top surprise-bill culprits from memory: NAT Gateway, idle Elastic IP,
   outbound data transfer, EBS on stopped instances, public IPv4, CloudWatch logs without retention.
- **Done check:** paste the budget confirmation + your own one-line explanation of each culprit.

### T.5 Secrets Manager: no hardcoded keys (25 XP)
1. Store a database password in Secrets Manager; read it from a Lambda function (or CLI with the right policy).
2. Rotate it once; prove the old value stops working and the function still works.
- **Done check:** paste the rotation output + the function's successful read post-rotation.

### T.6 KMS + SSM Parameter Store (25 XP)
1. Create a KMS key; store a config value as a `SecureString` in Parameter Store encrypted under it.
2. Grant decrypt to exactly one role; prove a different role gets denied.
- **Done check:** paste the allowed read + the `AccessDenied` from the wrong role. This is real IAM enforcement — emulator can't do this.

### T.7 CloudWatch observability (25 XP)
1. Build a dashboard: Lambda errors + invocations + duration for your Phase 5/8 function.
2. Write one Logs Insights query (e.g. slowest invocations), create an alarm on error-rate that notifies you.
- **Done check:** paste the Insights query + results + the alarm configuration.

### T.8 API Gateway authorizer (25 XP, badge 🔐)
1. Put a JWT (or IAM) authorizer on an HTTP API in front of a Lambda.
2. Prove both paths: valid token → 200 with answer; missing/invalid token → 401/403.
- **Done check:** paste both `curl` outputs. This gate is what Q8.3 will reuse.

## Standing rule
If a quest can be done on an emulator, it doesn't belong here.
This track is where you learn what the emulator was hiding from you.
