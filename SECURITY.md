# Security Policy

This is a learning repo: the only "production" surface is the course content itself.

## Reporting a vulnerability
Do **not** open a public issue for secrets, credential leaks, or anything that could
bill someone's AWS account. Instead:
1. Open a [private security advisory](../../security/advisories/new), or
2. DM the maintainer with "SECURITY:" in the subject.

We aim to acknowledge within 48 hours.

## Scope
- In scope: leaked real credentials in course content, malicious links/commands in
  quests or scripts, workflows with excessive permissions.
- Out of scope: emulator fidelity bugs (file those as regular issues), theoretical
  hardening of intentionally simple teaching code.

## Learner safety rules (enforced in review)
- No real credentials anywhere in the repo (fake `test`/`test` only).
- No quest may leave billable resources running without a teardown step.
- Workflows run with minimum permissions (`contents: read` unless noted).
