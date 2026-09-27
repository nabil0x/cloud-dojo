#!/bin/bash
# Playground health check. Run: bash shared/check.sh
set -u
pass=0; fail=0
ok()   { echo "PASS: $1"; pass=$((pass+1)); }
bad()  { echo "FAIL: $1"; fail=$((fail+1)); }

command -v docker >/dev/null && ok "docker installed ($(docker --version))" || bad "docker not found"
docker info >/dev/null 2>&1 && ok "docker daemon running" || bad "docker daemon not reachable"
command -v aws >/dev/null && ok "aws cli installed ($(aws --version 2>&1 | head -c 60))" || bad "aws cli not found"
command -v curl >/dev/null && ok "curl installed" || bad "curl not found"

if curl -sf -m 3 http://localhost:4566/_ministack/health >/dev/null 2>&1; then
  ok "emulator responding (ministack health)"
elif curl -sf -m 3 http://localhost:4566/_localstack/health >/dev/null 2>&1; then
  ok "emulator responding (localstack health)"
else
  bad "nothing on http://localhost:4566 (emulator not running — expected before Phase 1)"
fi

echo "---"
echo "$pass passed, $fail failed"
