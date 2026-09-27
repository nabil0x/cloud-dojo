# Cloud Dojo Glossary — jargon decoder

One line each. If a quest uses a word you don't know, it lives here.

## Docker
- **Image** — frozen read-only template; stacked layers + metadata.
- **Container** — a running instance of an image + one thin writable layer.
- **Layer** — one filesystem diff from one Dockerfile instruction; content-hashed, cached.
- **Build context** — the folder you hand to `docker build` (`.`); everything `COPY` can see.
- **Tag** — mutable pointer to an image (`myapp:v1`); `latest` moves, digests don't.
- **Digest** — immutable `sha256:…` identity of exact image bytes.
- **Volume** — storage outside any container's lifecycle; survives `rm`.
- **Bind mount** — a host path mounted into a container (vs managed named volumes).
- **Bridge network** — virtual LAN where containers resolve each other by name.
- **Port publishing** — `-p HOST:CONTAINER`; the only way in from the host.
- **Compose** — one YAML file describing a multi-container dev environment.
- **Registry** — image store (Docker Hub, ECR, GHCR); `push`/`pull` move images.
- **HEALTHCHECK** — orchestrator probe distinguishing dead from alive.
- **Multi-stage build** — build deps in one stage, ship only runtime in the final image.

## AWS core
- **Region / AZ** — region = geography (`us-east-1`); AZ = isolated datacenter inside it.
- **ARN** — precise address of anything (`arn:aws:s3:::bucket/key`); policies live by ARNs.
- **S3 bucket/object** — globally-unique bucket holding key→bytes objects; no real folders.
- **SQS** — message queue; visibility timeout + DLQ are the two ideas that matter.
- **SNS** — pub/sub fan-out; one publish, many subscribers; stores nothing.
- **DynamoDB** — serverless NoSQL; partition key picks the node, `query` ≠ `scan`.
- **Lambda** — event-driven functions; handler + execution role + 15-minute limit.
- **ECR** — private container registry; repos hold SHA-tagged images.
- **ECS / Fargate** — cluster → task definition → service → task; Fargate = no hosts to manage.
- **EC2** — rented VMs; families (`t` cheap, `g`/`p` GPU); AMIs are launch templates.
- **EBS** — network disks that outlive instances (and keep billing after stop).
- **RDS** — managed relational DBs; never publicly accessible.
- **API Gateway** — HTTPS front door: auth, throttling, CORS in front of Lambda.
- **CloudWatch** — metrics (alert on these) + logs (debug with these) + alarms + dashboards.
- **Bedrock** — foundation models as an API; pay per 1k tokens; Knowledge Bases = managed RAG.
- **SageMaker** — training jobs, notebooks, endpoints; endpoints bill while they exist.

## Networking
- **VPC** — your private region-scoped network (CIDR like `10.0.0.0/16`).
- **Subnet** — AZ-scoped slice; public = route to IGW, private = via NAT or nothing.
- **Route table** — where a subnet's packets go; `0.0.0.0/0 → IGW` means public.
- **IGW / NAT** — internet door (free-ish) vs private-subnet way out (~$32+/mo idle).
- **Security group** — stateful resource firewall, allow-rules only; check these first when unreachable.
- **NACL** — stateless subnet firewall; second layer, rarely touched daily.

## IAM & security
- **IAM** — who can do what; users (people) vs roles (code, temporary creds) vs groups.
- **Policy** — JSON of Effect/Action/Resource; explicit Deny always wins.
- **Least privilege** — start from nothing, add grants; never start from `*`.
- **MFA** — second factor; also enforceable inside policies.
- **KMS** — master keys; envelope encryption (keys encrypt keys).
- **Secrets Manager / SSM Parameter Store** — runtime secrets + config; never hardcode either.
- **OIDC** — CI pipelines assuming AWS roles without stored keys.

## IaC & delivery
- **Terraform** — desired-state declarations; `plan` is a code review, `apply` executes.
- **State file** — maps your code to real resource IDs; lose it, lose ownership.
- **Module** — folder of `.tf` with variables in, outputs out.
- **CI/CD** — every push builds+tests (CI); green main ships itself (CD).
- **Artifact** — immutable build output (SHA-tagged image); rollback = redeploy old SHA.

## Concepts
- **Idempotency** — safe to retry; SQS delivers at-least-once, so consumers must be.
- **Eventual consistency** — reads may lag writes; design for it (IAM propagation, S3 listings).
- **Cold start** — first-invocation latency; small images + lean deps fight it.
- **Drift** — reality changed outside your IaC; `plan` reveals it.
- **Blast radius** — how much breaks when one thing does; least privilege shrinks it.
