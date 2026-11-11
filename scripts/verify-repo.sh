#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q backend/app middleware observability
PYTHONPATH=backend pytest -q tests
if command -v helm >/dev/null 2>&1; then
  helm lint helm/lsk-platform --set image.digest=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
  helm template lsk helm/lsk-platform --set image.digest=sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa >/dev/null
fi
if command -v terraform >/dev/null 2>&1; then
  terraform -chdir=terraform/gcp fmt -check
  terraform -chdir=terraform/gcp init -backend=false
  terraform -chdir=terraform/gcp validate
fi
