# Phase 6 — Terraform IaC (150 XP)

**Status:** 🔒 locked — unlocks after Phase 3.
**Goal:** version your infrastructure; `plan` before you `apply`, `destroy` when done.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** emulator first (free, fast), then one careful apply to the sandbox.
**Starter files:** `main.tf` skeleton (provider done, resources are TODOs) — the TODOs ARE the quests.

## Quests

### Q6.1 First config: provider + bucket (30 XP)
1. Install Terraform. Write `main.tf`: AWS provider with `endpoints` overridden to `http://localhost:4566` + fake creds, one `aws_s3_bucket`.
2. `terraform init`, `plan` (read every line), `apply`.
- **Done check:** paste the `plan` resource summary + `Apply complete! Resources: 1 added`.

### Q6.2 Variables + outputs (25 XP)
1. Parameterize the bucket name (`variable` + `terraform.tfvars`), output the bucket ARN.
2. Change the var, re-plan, observe the diff proposes replace (name change = new bucket).
- **Done check:** paste `terraform output` + the plan diff showing replacement.

### Q6.3 State: list, show, import (30 XP)
1. `terraform state list` + `state show` — read the JSON, find where the bucket ID lives.
2. Create a queue by hand (CLI), then `terraform import` it into a matching `aws_sqs_queue` block. Re-plan: expect zero changes.
- **Done check:** paste `state list` (both resources) + the empty `No changes` plan.

### Q6.4 Multi-resource apply (35 XP)
1. Add SNS topic + DynamoDB table (+ SQS subscription wiring) to the config. One `apply` builds the Phase 1 stack declaratively.
2. Break one attribute on purpose, watch plan catch it before anything deploys.
- **Done check:** paste `Apply complete! Resources: N added` + the caught plan diff.

### Q6.5 👹 Boss: destroy + clean proof (30 XP, badge 🧱)
1. `terraform destroy` (type `yes` by hand — feel it), verify via CLI that bucket/queue/topic/table are all gone.
2. Run one `plan` against the **sandbox** (no apply) for the same config; read what *would* be created and its cost exposure.
- **Done check:** paste `Destroy complete!` + the sandbox plan's resource count. Par: emulator empty, sandbox untouched.

**Standing rule for this phase:** never `apply` what you haven't read in `plan`. The day you skip reading is the day you create 40 NAT gateways.
