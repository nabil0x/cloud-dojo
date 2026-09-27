# T.1 — Claim your sandbox (20 XP)

**Phase:** Track T — Real-AWS Parallel Track

## Concept
Track T is the only part of the dojo that runs on real AWS, never on an emulator.
Emulators fake the APIs but skip the things that actually shape cloud work: IAM enforcement, billing, and quotas.
To learn those safely you use a free sandbox, either the AWS Builder Center Sandbox (no account, no credit card) or a free Skill Builder lab.
The sandbox is a disposable AWS account with a time limit, so mistakes cost nothing and expire on their own.
Once inside, you open the console and locate IAM, S3, and the billing dashboard, the three places every later quest returns to.
This is your safe place to break things, and it is where the emulator's training wheels come off.

## Uses
- Learning AWS services hands-on without an account or a credit card.
- Practicing IAM and billing work with real enforcement and real guardrails.
- Running labs that expire and clean themselves up, so nothing lingers.
- Building console fluency that transfers directly to a real account.
- Testing a policy or an alarm and seeing the genuine consequence, not a simulation.

## Key info
- Start from the AWS Builder Center Sandbox or a free Skill Builder lab.
- The sandbox shows a time-remaining notice; that countdown is the environment's lifetime.
- From the console, find IAM (identity and access), S3 (storage), and the billing dashboard.
- Note the console home region, because region matters for many later quests.
- Everything here is real AWS, so IAM policies you write are actually enforced.
- Never run these quests on an emulator. The whole point is the behavior emulators skip.
- The sandbox has no billing risk, which makes it the ideal place to learn what a real bill looks like.
- Bookmark the console so you can jump back to IAM and Billing quickly on every quest.

## Pitfalls
- Treating the sandbox like your own account. When the timer ends, everything is gone.
- Skipping the billing view because it feels boring. It is the whole reason Track T exists.
- Working in the wrong region and losing track of resources. Always confirm the region shown in the console.

## Done check
paste the sandbox time-remaining notice + the console home region.

## Links
- AWS Builder Center Sandbox: https://aws.amazon.com/about-aws/whats-new/2026/07/aws-builder-center-sandbox
- Getting started with IAM: https://docs.aws.amazon.com/IAM/latest/UserGuide/getting-started.html
- AWS Management Console overview: https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/what-is.html
