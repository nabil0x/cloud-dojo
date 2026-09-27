#!/bin/bash
# Fire extinguisher: targeted playground reset. Run from repo root:
#   bash shared/nuke.sh
# Removes ONLY dojo resources (never touches your other containers/images).
set -uo pipefail
cd "$(dirname "$0")/../phase-02-compose" 2>/dev/null && docker compose down -v 2>/dev/null || true
cd - >/dev/null
docker rm -f dojo-emu dojo-emulator dojo-app 2>/dev/null || true
docker volume rm dojo-data 2>/dev/null || true
echo "Nuked. Rebuild via the Phase 2 boss loop: compose up --build + seed."
