# First XP in 5 minutes

No reading ahead. Just this page, then Q0.1 is done.

## Minute 0–1: prove Docker works
```bash
docker run hello-world
```
See `Hello from Docker!`? Good. If not: [SETUP-WINDOWS](SETUP-WINDOWS.md) /
[SETUP-MAC](SETUP-MAC.md), or click **Open in GitHub Codespaces** in the README.

## Minute 1–3: start your first AWS emulator
```bash
docker run -d --name dojo-emu -p 4566:4566 ministackorg/ministack
curl -s http://localhost:4566/_ministack/health
```
A JSON blob answers. That blob is pretending to be Amazon. Congratulations.

## Minute 3–5: claim 10 XP
```bash
python3 shared/progress.py check Q0.1
python3 shared/progress.py status
```
Then open `dashboard.html` — your bar moved. Paste the `hello-world` output
wherever your group chats, and continue to
[Phase 0](../../phase-00-docker-foundations/README.md) Q0.2.

Stuck anywhere? [Troubleshooting](../learn/TROUBLESHOOTING.md) → symptom first, theory later.
