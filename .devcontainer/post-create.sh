#!/usr/bin/env bash
# Waits for the inner Docker daemon (DinD is flaky on first boot).
set -euo pipefail
echo "Waiting for the inner Docker daemon..."
for _ in $(seq 1 30); do
  if docker info >/dev/null 2>&1; then
    echo "Docker ready: $(docker --version)"
    docker compose version
    echo "Next: bash shared/check.sh"
    exit 0
  fi
  sleep 2
done
echo "Docker daemon not ready after 60s" >&2
exit 1
