# Self-check — CI/CD + ECS (no XP, honor system)

Score 7+ before the boss fight.

## 1. What's the difference between CI and CD here, and what does a red CI run mean?

<details><summary>Show answer</summary>
CI means every push builds and tests in a clean room; a red run means "don't merge," not "works on my machine." CD means every green main-branch build ships (or stages for approval). The pipeline itself is code: triggers, jobs, steps.
</details>

## 2. Why tag images with the commit SHA instead of a moving `:latest`?

<details><summary>Show answer</summary>
Artifacts must be immutable. A git-SHA tag points at exactly one build, so you always know what's running and rollback means redeploying the previous SHA. `:latest` moves under your feet, so two deploys can quietly run different code and rollback has no target. Never use a moving tag for deploys.
</details>

## 3. A workflow fails halfway through. Where do you look first, and why?

<details><summary>Show answer</summary>
Read the failed logs top-down. The first error is usually the only real one; everything after it is fallout from the first failure. Fixing the last line first wastes a run, because the actual cause is higher up.
</details>

## 4. Name four items from the production image checklist and what each one buys you.

<details><summary>Show answer</summary>
Pinned base tag (`python:3.13-slim`): reproducible builds, no surprise base changes. Non-root `USER`: least privilege inside the container. `.dockerignore`: keeps `.git` and secrets out and shrinks the build context. `HEALTHCHECK`: the orchestrator can tell dead from alive. Multi-stage builds (the advanced one): ship only runtime, so smaller image, faster deploys, smaller attack surface.
</details>

## 5. Why prefer OIDC role assumption over long-lived access keys in Actions, and what breaks if a key leaks?

<details><summary>Show answer</summary>
OIDC means no long-lived secrets stored in GitHub to leak. A leaked access key is standing access until someone rotates it, and it can be abused from anywhere. OIDC trades the secret for a short-lived token the pipeline assumes per run.
</details>

## 6. ECS vocabulary: cluster, task definition, service, task. Which one is versioned and immutable?

<details><summary>Show answer</summary>
Cluster is a logical pool; task definition is the image plus CPU/RAM plus env plus log config; service keeps a desired count of tasks running; a task is one running container set. The task definition is the versioned, immutable revision. When you change anything about the container, you register a new revision.
</details>

## 7. What breaks if you put your app's AWS permissions on the execution role, or omit the execution role's permissions?

<details><summary>Show answer</summary>
Task role is what the container may call; execution role is what ECS needs to pull images and write logs. If the execution role lacks ECR or CloudWatch permissions, the task can't start or its logs never appear. Putting app permissions on the execution role blurs that IAM separation and hands the ECS agent more than it needs.
</details>

## 8. A Fargate task dies immediately and no logs show in the console's green dots. Where do you start, and why?

<details><summary>Show answer</summary>
Start in the CloudWatch log group. Logs go there by default via the `awslogs` driver, and debugging a dead task begins in the log group, not the console's status indicators. If the execution role can't write logs, there's nothing to debug, which is itself the clue.
</details>

## 9. What breaks if you forget the Q7.5 teardown? Contrast `desiredCount: 0` with a full delete.

<details><summary>Show answer</summary>
A forgotten Fargate service is a subscription you didn't sign up for: it bills per vCPU/GB-second while tasks run, and ALBs, ECR storage, and NAT add up too. `desiredCount: 0` stops task billing while keeping the config, useful mid-project. A full delete at phase end removes everything. Par is $0 left behind.
</details>

## 10. Why does every deploy have to go through the pipeline in this phase?

<details><summary>Show answer</summary>
Because a laptop `docker push` or a console-click deploy bypasses the build and test gate, so nothing guarantees the running artifact matches the repo. The pipeline is the only thing that makes "ships itself" true and repeatable. Deploys done by hand don't count.
</details>
