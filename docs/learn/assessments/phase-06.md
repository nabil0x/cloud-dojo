# Self-check — Terraform IaC (no XP, honor system)

Score 7+ before the boss fight.

## 1. Why does Terraform make you run `plan` before `apply` instead of just applying your config?

<details><summary>Show answer</summary>
Because Terraform compares three things before changing anything: your declared desired state, the recorded actual state (the state file), and reality. The plan is the diff of that comparison, so it shows exactly what would be created, updated, replaced, or destroyed. Treat it as a code review for infrastructure. The standing rule for this phase: never apply what you haven't read in plan.
</details>

## 2. Predict the output. You change the `bucket` argument from `dojo-a` to `dojo-b` and re-run `plan`. Does Terraform update the bucket in place, or something else?

<details><summary>Show answer</summary>
It proposes a replacement: destroy the old bucket and create a new one. The bucket name is a force-new attribute, so the plan marks it `forces replacement` (often shown as `-/+`). If you only skimmed, the destroy line surprises you. Q6.2's done check is exactly this diff.
</details>

## 3. What breaks if you delete or lose `terraform.tfstate`?

<details><summary>Show answer</summary>
Terraform forgets what it owns. The state file is the mapping from your code to real resource IDs, so your resources still exist but Terraform has no record of them. Your next apply tries to create everything again, producing duplicates or name conflicts, and only `import` can adopt the existing resources back. That's why remote backends exist and why you never hand-edit the file.
</details>

## 4. You create an SQS queue by hand with the CLI, then add a matching `aws_sqs_queue` block. What is `terraform import` for, and what plan should you expect right after it succeeds?

<details><summary>Show answer</summary>
`import` adopts an already-existing resource into state so Terraform knows it owns it. After a correct import, re-plan shows `No changes`, because the code block now matches the real queue. If plan still proposes a diff, your block's arguments don't match the real resource: fix the code, don't re-import.
</details>

## 5. Why is it dangerous to commit `terraform.tfstate` to git, and why should you never hand-edit it?

<details><summary>Show answer</summary>
State stores values in plaintext, including secrets, so committing it can leak credentials. Hand-editing corrupts the mapping between code and real resource IDs, and Terraform may then lose track of resources or delete the wrong thing. The safe team answer is a remote backend (S3 plus DynamoDB locking); know the name even if you defer the setup.
</details>

## 6. What breaks if you point the AWS provider at the emulator endpoint but leave out the `skip_*` validation flags?

<details><summary>Show answer</summary>
The fake credentials fail real AWS validation. The standard local pattern is endpoint overrides plus flags that skip requesting the account ID and skip credential validation. Without them, Terraform tries to validate fake creds against real AWS and errors out before it ever reaches the emulator.
</details>

## 7. What breaks if you apply a config without reading the plan first? Name the concrete example the phase warns about.

<details><summary>Show answer</summary>
You deploy infrastructure you never reviewed and eat the surprise bill. The phase's example is creating 40 NAT gateways because you skipped the plan. The plan already showed the resource count and the cost exposure; apply just executes it. An unread plan is an unread bill.
</details>

## 8. What is the "rule of three" for modules, and why does it exist?

<details><summary>Show answer</summary>
Inline the same config twice, then extract a module on the third repetition. It stops you from over-engineering a one-off into a module while still removing real duplication once a pattern is proven. A module is just a folder of `.tf` files: variables in, outputs out.
</details>

## 9. Q6.5 has you run `plan` against the sandbox with no apply. Why bother, and what should you read in it?

<details><summary>Show answer</summary>
It teaches you to respect the fidelity gap. Plan/apply mechanics are real, but the emulator's service behavior is emulated, so a change that looks fine locally can behave differently on real AWS. Read what would actually be created and its cost exposure, while leaving the sandbox untouched. Par is emulator empty, sandbox untouched.
</details>

## 10. When would you use `state mv` versus `taint`?

<details><summary>Show answer</summary>
`state mv` renames or moves a resource in state without destroying or recreating it, useful when you refactor code (rename a block, move into a module). `taint` marks a resource so the next apply destroys and recreates it, useful when a resource is unhealthy but the config is unchanged. One moves ownership; the other forces replacement.
</details>
