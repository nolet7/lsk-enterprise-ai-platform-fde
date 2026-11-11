#!/usr/bin/env bash
set -euo pipefail
NS="${NAMESPACE:-lsk-ai}"
kubectl get namespace "$NS"
kubectl -n "$NS" get deployment,service,hpa,pdb,networkpolicy
kubectl -n "$NS" rollout status deployment/lsk --timeout=180s
kubectl -n "$NS" get pods -o wide
echo "Kubernetes checks done. Restore, authorization, network egress, signed image and load testing require separate evidence."
