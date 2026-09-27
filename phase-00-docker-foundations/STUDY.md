# Phase 0 — Study Guide: Docker Foundations

Read this before (or alongside) the quests. Quests prove you can do it;
this file makes sure you know *what you just did*.

## 1. Image vs container (the whole game in two sentences)
- An **image** is a frozen, read-only template: stacked filesystem layers + metadata (entrypoint, env, exposed ports).
- A **container** is a running instance of an image: the same layers plus one thin writable layer on top, plus an isolated process space (namespaces) and resource limits (cgroups).
- Deleting a container deletes its writable layer. The image is untouched. This is why containers are disposable and why data needs **volumes** (Phase 1).

## 2. Layers and the build cache
- Each Dockerfile instruction (`FROM`, `RUN`, `COPY`, ...) creates one layer, identified by a content hash.
- Rebuilds reuse every layer whose instruction *and inputs* are unchanged — that's the cache.
- Ordering rule: put slow-changing instructions first (`FROM`, dependency installs), fast-changing ones last (`COPY app code`). A one-line code edit should rebuild only the last layers.
- `docker image history <img>` shows each layer, its size, and the command that made it. Big layers early = slow iteration.

## 3. Dockerfile essentials (enough for this course)
| Instruction | Meaning |
|---|---|
| `FROM python:3.13-slim` | Base image. `tag` pins the version — `latest` moves under you, never use it for anything you keep. |
| `WORKDIR /app` | Working directory for everything after it (auto-created). |
| `COPY requirements.txt .` | Copy from build context (your folder) into the image. Order matters for cache. |
| `RUN pip install ...` | Executes at *build* time, baked into a layer. |
| `EXPOSE 8080` | Documentation + default metadata. It does **not** publish the port — `-p host:container` does that at *run* time. |
| `CMD ["python","app.py"]` | Default command at container start. Overridable: `docker run <img> <other-cmd>`. |

## 4. Ports: `-p HOST:CONTAINER`
- `-p 8080:80` = host port 8080 forwards to container port 80. Two containers can both listen on 80 internally as long as host ports differ.
- `localhost:PORT` from your laptop reaches the **host** side. From *inside another container*, `localhost` means that container itself — hence service names / bridge DNS (Phase 1, Q1.6).

## 5. Lifecycle commands you must be fluent in
`ps` (list) → `logs` (read) → `stop` (graceful SIGTERM) → `rm` (delete) → `ps -a` (confirm).
Dangling state to clean occasionally: `docker ps -a`, `docker images`, `docker volume ls`, `docker network ls`.

## 6. Common beginner traps
- Rebuilding the world on every code change → fix instruction order (see §2).
- Editing files *inside* a running container and expecting them to persist → they live in the writable layer; gone with `rm`.
- Port already allocated → something else owns the host port; `docker ps` to find it.
- `sudo docker ...` every time → you're not in the `docker` group (Q0.1 fixed this).

## Further reading (official, short)
- Docker concepts: images vs containers — https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/
- Build, tag, publish + layers — https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/
- Docker Curriculum (free, hands-on) — https://docker-curriculum.com/
