# Setup on macOS

## 1. Install Docker Desktop
1. Download the right build: **Apple Silicon** (M1+) vs **Intel** — check  → About This Mac.
2. Start it, wait for the whale icon to stop animating, then:
```bash
docker run hello-world
```

## 2. Tune resources (important on 8 GB Macs)
Docker Desktop → Settings → Resources: give Docker **at least 4 GB RAM and 2 CPUs**.
Emulator + app + Lambda images on defaults will swap and crawl.

## 3. Course tooling
```bash
brew install awscli curl python3   # or: xcode-select --install, then pip
aws --version && python3 --version
```

## Pitfalls (Mac-specific)
- **Apple Silicon + old images**: if a container exits with `exec format error`, it's an amd64-only image. Prefer multi-arch tags; the course images are fine.
- **VirtioFS file sharing**: keep it on (default) — bind mounts into the emulator are near-native; legacy osxfs is 10x slower.
- **"Port already allocated" after sleep**: Docker Desktop sometimes keeps dead mappings; `docker ps -a` + `rm -f`, or Restart from the whale menu.
- **Battery + heat**: compose stacks + Lambda builds are heavy. Plug in, or do heavy phases in short sessions.
- **No admin rights?** Docker Desktop needs one install with admin; after that it's user-space. Otherwise use the Codespaces button (zero install).
