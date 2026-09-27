# Phase 4 — EC2 + VPC + RDS (150 XP)

**Status:** 🔒 locked — unlocks after the Phase 2 boss.
**Goal:** launch real compute, network it correctly, attach a managed database — then tear it all down.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.
**Environment:** ⚠️ mostly **real sandbox** (Builder Center Sandbox / free-tier account). EC2/VPC/RDS don't emulate meaningfully — no real VMs, no real networking. Teardown discipline is part of every quest.

## Quests

### Q4.1 VPC anatomy (30 XP)
1. In the sandbox console, open the default VPC: identify 1 VPC, subnets, route tables, internet gateway.
2. Draw (paper counts): IGW → route table → public subnet → instance. Label where a *private* subnet would differ (NAT, no IGW route).
- **Done check:** paste the subnet + route-table listing (console screenshot description or CLI `describe-subnets` output).

### Q4.2 Launch EC2 + security groups (40 XP)
1. Launch a `t3.micro` (free-tier eligible) Amazon Linux instance with a key pair, in the default VPC.
2. Write a security group allowing SSH (port 22) **from your IP only** + HTTP (port 80) open; attach it.
3. SSH in, install something via user data or manually, serve a page on port 80.
- **Done check:** paste the `curl` of your instance's public IP returning your page + the SG inbound rules.

### Q4.3 AMIs, EBS, stop/start billing lesson (25 XP)
1. Stop the instance: prove it keeps its EBS volume (and keeps billing for it).
2. Create an AMI from it, terminate the original, launch a clone from the AMI.
- **Done check:** paste `describe-instances` showing the clone running + one sentence on what still bills while stopped.

### Q4.4 RDS Postgres, scoped access (30 XP)
1. Launch a `db.t3.micro` Postgres (free-tier eligible), **not publicly accessible**, in the default VPC.
2. Open the RDS security group to your EC2 security group only (SG-to-SG reference, never `0.0.0.0/0`).
3. Connect from the EC2 instance with `psql`, create a table, insert a row.
- **Done check:** paste the `SELECT` output + the RDS SG inbound rules.

### Q4.5 👹 Boss: nuke it + $0 proof (25 XP, badge 🏗️)
1. Terminate the EC2 instance(s), delete the RDS instance (skip final snapshot — it's practice data), release Elastic IPs, delete unattached volumes/snapshots.
2. Open Billing / Cost Explorer: prove $0 (or sandbox-clean) and list what *would* have billed had you left it (NAT? EBS? IPv4?).
- **Done check:** paste the resource-terminated confirmations + the billing screenshot description. Par: nothing left running.

**Standing rule for this phase:** no quest counts while anything from a previous quest is still running unattended. If you sleep, it sleeps terminated.
