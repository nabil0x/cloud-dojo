# Phase 6 — Study Guide: Terraform IaC

Click-ops doesn't scale and doesn't review. Code does both.

## 1. The model: desired state + plan + apply
- You declare **desired state** (HCL blocks: `resource`, `variable`, `output`). Terraform compares it to **actual state** (the state file) and to reality, then shows a **plan** (create/update/replace/destroy).
- Golden loop: write → `plan` (read it!) → `apply` → verify → commit. The plan is a code review for infrastructure — treat it like one.
- **State file** (`terraform.tfstate`): the mapping of your code to real resource IDs. Lose it and Terraform forgets what it owns (hence `import`). Never hand-edit it; never commit secrets in it (it stores them in plaintext — backends + sensitive outputs exist for a reason).

## 2. HCL essentials
- `provider "aws" { region, endpoints { s3 = "http://localhost:4566" ... } }` — the emulator trick: same config, different endpoint. This is how one codebase targets both playground and sandbox.
- `resource "aws_s3_bucket" "dojo" { bucket = var.name }` — type + local name + arguments.
- `variable` (+ `terraform.tfvars` values) in, `output` (ARNs, endpoints) out. Modules consume variables and expose outputs — that's the whole composition model.
- Changing a **force-new** attribute (like a bucket name) destroys + recreates. The plan tells you (`forces replacement`) — read it or be surprised.

## 3. State operations you must know
- `state list` / `state show` — inspect. `import <addr> <id>` — adopt hand-made resources. `state mv` — rename without destroy. `taint` — force recreation next apply.
- Remote backends (S3 + DynamoDB locking) are the team answer to "whose laptop holds state" — know the name, defer the setup until you have a team.

## 4. Modules (the 80/20)
- A module is just a folder of `.tf` files with variables in and outputs out. Registry modules exist for VPCs etc. — prefer reviewed modules over hand-rolled networking once you're past learning.
- Rule of three: inline twice, module on the third repetition.

## 5. Emulator + Terraform specifically
- Provider endpoint overrides + `skip_*` validation flags (skip requesting account ID, skip credential validation) are the standard local pattern — the fake creds fail real AWS validation otherwise.
- Fidelity caveat carries over from Phase 1: plan/apply mechanics are real, service behavior is emulated. The sandbox `plan` in Q6.5 (no apply) teaches you to respect the difference.

## Further reading (official, short)
- Terraform language + CLI workflow — https://developer.hashicorp.com/terraform/docs
- AWS provider + local testing patterns — https://registry.terraform.io/providers/hashicorp/aws/latest/docs
