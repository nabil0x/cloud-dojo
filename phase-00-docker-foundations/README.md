# Phase 0 — Docker Foundations (100 XP)

**Status:** 🔒 locked — we start together when you say go.
**Goal:** run any container with confidence; explain image vs container in one sentence each.
**Study:** 📖 read `STUDY.md` in this folder before starting the quests.

## Quests

### Q0.1 Hello, Docker (10 XP)
1. Install Docker (Desktop or Engine).
2. Run `docker run hello-world`.
- **Done check:** paste the `Hello from Docker!` output.

### Q0.2 Run the emulator (15 XP)
1. Run `docker run -d --name dojo-emu -p 4566:4566 ministackorg/ministack`.
2. Run `docker ps` and `curl -s http://localhost:4566/_ministack/health`.
- **Done check:** paste the health JSON.

### Q0.3 Lifecycle: ports, logs, stop/rm (15 XP)
1. Run an `nginx` container on host port 8080.
2. Open `http://localhost:8080`, then inspect `docker logs`, `docker stop`, `docker rm`.
- **Done check:** `docker ps -a` showing it gone, plus one log line pasted.

### Q0.4 Your first Dockerfile (20 XP)
1. Create a folder with an `index.html` and a 3-line Dockerfile (`FROM nginx:alpine` + `COPY`).
2. `docker build -t dojo-site .` then run it on port 8081.
- **Done check:** paste `docker images | grep dojo-site` + the page title from `curl -s localhost:8081`.

### Q0.5 Layers and cache (20 XP)
1. Rebuild Q0.4 twice: once unchanged (all cache), once after editing one file.
2. Run `docker image history dojo-site`.
- **Done check:** paste the two build timings + which layer rebuilt.

### Q0.6 👹 Boss: custom port + name (20 XP, badge 🐳)
1. Stop/remove everything. Re-run the emulator as `--name <your-name>` on host port **4570**.
2. Prove it answers on 4570 and that 4566 is now empty.
- **Done check:** `curl` outputs for both ports + `docker ps --format '{{.Names}} {{.Ports}}'`.

**Break-it bonus (rule #4):** map the port backwards (`-p 80:4566` style confusion),
read the error, fix it, note what you learned in `PROGRESS.md`.
