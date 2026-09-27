# Phase 4 — Study Guide: EC2 + VPC + RDS

Real compute, real networking, real databases — and real bills if you're careless.

## 1. EC2: renting computers
- **Instance families**: `t` (burstable, cheap, free-tier), `m` (balanced), `c` (compute), `r` (memory), `g/p` (GPU — training/inference), `inf/trn` (AI accelerators). Pick by bottleneck, not habit.
- **AMIs**: machine images — OS + preinstalled software. Launch → configure → snapshot as your own AMI for reproducible clones.
- **Key pairs**: SSH access. Lose the private key = locked out (no password fallback by default).
- **User data**: shell script that runs once at first boot — bootstrapping without clicking.
- **EBS**: network-attached disks. Persist independently of instances — which is exactly why stopped instances keep billing.

## 2. VPC: your private network
- **VPC** (region-scoped CIDR, e.g. `10.0.0.0/16`) → **subnets** (AZ-scoped slices) → **route tables** (where traffic goes) → **IGW** (public internet door) / **NAT gateway** (private subnets' way out, $$$).
- **Public subnet**: route to IGW. **Private subnet**: no IGW route; outbound via NAT. Databases live in private subnets. Always.
- New accounts get a **default VPC** — perfect for learning, never for production architecture discussions.

## 3. Security groups vs NACLs (know the difference cold)
- **Security groups**: stateful, attached to *resources* (instance, RDS). Allow-rules only; return traffic auto-allowed. Your primary firewall — scope SSH to your IP, DBs to app SGs.
- **NACLs**: stateless, attached to *subnets*. Allow + deny, both directions explicit. Second layer, rarely touched day-to-day.
- Classic outage: "my app can't reach the DB" → SG on the DB doesn't allow the app's SG. Check SGs before anything else.

## 4. RDS: Postgres without the ops
- Managed engine, automated backups, snapshots, Multi-AZ failover option. You still own: instance sizing, storage growth, SG scoping, credential rotation.
- **Never publicly accessible** for practice or production. Access path: your laptop → (SSH tunnel via EC2) → RDS, or app EC2 → RDS over SG-to-SG rules.
- Free-tier eligible: `db.t3.micro`, 20 GB storage, 12 months (older accounts) — verify current terms in your sandbox.

## 5. Billing awareness (replaces emulator comfort)
- Running EC2 bills per second; **stopped EBS, snapshots, Elastic IPs, and NAT gateways bill while you sleep**. The Q4.5 teardown exists because every engineer learns this once — preferably in a sandbox.
- Before launching anything: note its hourly rate. After deleting: verify in Cost Explorer. That loop is the habit.

## Further reading (official, short)
- EC2 instance types + AMIs + key pairs — https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/
- VPC concepts (subnets, route tables, IGW/NAT) — https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html
- RDS Postgres setup — https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.PostgreSQL.html
