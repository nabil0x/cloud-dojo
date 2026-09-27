# Troubleshooting — error decoder

Find your symptom. Newbies live here; intermediates revisit monthly.

## Docker daemon & permissions
- **`Cannot connect to the Docker daemon`** → daemon isn't running. Desktop: start the app. Linux: `sudo systemctl start docker` (and `enable` it). After a kernel upgrade: **reboot**.
- **`permission denied` on `/var/run/docker.sock`** → not in the `docker` group: `sudo usermod -aG docker $USER`, then log out/in (or `newgrp docker`).
- **`docker: command not found`** → Docker isn't installed at all (Q0.1).

## Ports & lifecycle
- **`port is already allocated`** → something owns the host port. `docker ps` (another container?) or `lsof -i :PORT`. Pick a different host port.
- **Connection refused on `localhost:PORT`** → container not running, wrong host port, or app listens on `127.0.0.1` inside the container instead of `0.0.0.0`.
- **`docker rm` fails** → container is running: `docker stop` first (or `rm -f`).
- **Edit didn't take effect** → rebuilt without `--build`, or edited a file inside the container instead of the source. Compose: `docker compose up -d --build`.
- **Slow rebuilds** → `COPY . .` placed before dependency install; reorder slow-changing instructions first (Phase 0 §2).

## Container networking (the #1 confusion)
- **Works from laptop, fails from container** → you used `localhost` inside a container, where it means *that container*. Use the service/container **name** (`http://emulator:4566`).
- **Name doesn't resolve** → containers aren't on the same *user-defined* bridge (the default bridge has no DNS). `docker network create` + attach both.
- **Can't reach emulator from app in Compose** → `AWS_ENDPOINT_URL=http://emulator:4566`, not `localhost`. Deliberately break + fix this in Q2.3 until the error is familiar.

## Emulator: connection & config
- **`Could not connect to the endpoint URL`** → emulator isn't up (`docker ps`?), wrong port, or wrong host (`localhost` vs service name — see above).
- **Empty results (no buckets/queues)** → fresh emulator is empty by design, not broken. Run `bash shared/seed.sh`.
- **Data vanished after restart** → no volume mounted (Q1.4), or you ran `down -v`. Re-seed.
- **`NoSuchBucket` / `NoSuchKey`** → typo in name, wrong region endpoint, or resource lives in a different (real vs emulated) environment.

## AWS CLI & credentials
- **Forgot `--endpoint-url`** → call went to real AWS (or failed without creds). Export `AWS_ENDPOINT_URL` once (Q1.5).
- **`Unable to locate credentials`** → export the fake `test`/`test` pair + region, or check `aws configure list` for what's active.
- **`AccessDenied`** → on real AWS: genuinely missing permission (fix the policy — T.2). On emulator: unexpected; check you're hitting the emulator at all.
- **Wrong region behavior** → `AWS_DEFAULT_REGION` unset or mismatched; some errors only make sense per-region.

## Terraform
- **`plan` wants to destroy everything** → state file lost/moved, or you're in the wrong directory/workspace. Stop, find state, never `apply` a surprise plan.
- **Credentials validation errors on emulator** → missing `skip_*` flags or `endpoints` override in the provider block (Phase 6 skeleton has them).
- **Resource needs replacement** → you changed a force-new attribute (names, AZs); plan says `forces replacement` — read it or be surprised.
- **State lock stuck** → previous run died mid-apply; verify no apply is running, then `force-unlock` (carefully, once).

## Pipelines & ECS
- **Pipeline red** → read logs top-down; the first error is usually the only real one.
- **Task stops immediately** → check the CloudWatch log group first, then task role (pull image? write logs?) vs task-definition mistakes.
- **Can't reach Fargate task** → security group ingress, wrong port, or app bound to `127.0.0.1`.

## Billing panic (real AWS)
Breathe. Then, in order: Cost Explorer (what, since when?) → terminate/stop the resource → delete unattached EBS, snapshots, Elastic IPs → check NAT gateway hours → set the $1 budget + anomaly detection you skipped (T.4). The rogues' gallery: NAT Gateway, idle EIP, data transfer, EBS-on-stopped, public IPv4, log retention. Full list: Track T STUDY §4.
