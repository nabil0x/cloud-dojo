# Phase 2 — Study Guide: Docker Compose

The ideas behind running the emulator + your app as one stack.

## 1. What Compose is (and isn't)
- A **declarative multi-container dev environment**: one YAML file describes services, networks, volumes, env — `docker compose up` builds the whole world, `down` removes it.
- It is not production orchestration (that's ECS/Kubernetes). Think of it as "my laptop's data center," version-controlled.

## 2. Compose file anatomy (our `compose.yaml`)
- **`services:`** each entry is one container role (`emulator`, `app`). Each gets DNS = its service name on the shared network Compose creates automatically.
- **`build: ./app`** vs **`image:`**: `build` compiles a Dockerfile locally; `image` pulls a registry image. Our stack uses both (app builds, emulator pulls).
- **`ports: ["8080:8080"]`** — same `HOST:CONTAINER` semantics as `docker run -p`.
- **`environment:`** injects env vars. Ours carries the whole emulator contract: `AWS_ENDPOINT_URL=http://emulator:4566` + fake creds + region.
- **`volumes:`** top-level declares named volumes (`dojo-data`); per-service entries mount them. `down -v` deletes them (the boss fight's weapon).
- **`depends_on:`** orders startup (emulator first). Note: it does *not* wait for readiness — that's why real stacks add healthchecks; ours keeps it simple and lets you observe the race.

## 3. Service DNS: the one rule
- Inside the Compose network, `http://emulator:4566` resolves to the emulator container. `http://localhost:4566` inside the app container means *the app itself*.
- Host↔container confusion is the #1 Compose debugging skill: always ask "localhost *from whose perspective?*"
- Q2.3 makes you break this deliberately so the error message becomes a friend, not a stranger.

## 4. The rebuild loop (daily driver)
1. Edit code → 2. `docker compose up -d --build` → 3. `docker compose logs -f app` → 4. `curl` the endpoint → 5. repeat.
- `--build` forces image rebuild; without it Compose reuses the old image and your edit "mysteriously" doesn't appear (classic trap).
- `logs -f <service>` scopes the firehose to one service.

## 5. Seed scripts: deterministic playgrounds
- `shared/seed.sh` creates the bucket/queue/table from the **host** (host → `localhost:4566`). Run it after every fresh `up` so quests start from a known state.
- Pattern to remember: infrastructure-as-script beats clicking around — this instinct becomes Terraform/CDK later.

## 6. Swapping emulators (one-line lesson)
- MiniStack ↔ LocalStack differ only in `image:` (+ auth token). Same port, same endpoint pattern, app untouched. Portability through uniform interfaces is the entire point of the exercise.

## Further reading (official, short)
- Compose overview + file reference — https://docs.docker.com/compose/
- Multi-container apps tutorial — https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/
