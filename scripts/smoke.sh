#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:18743}"
curl -fsS "$BASE/healthz"
curl -fsS "$BASE/api/apps"
curl -fsS -X POST "$BASE/api/tickets" -H 'Content-Type: application/json' -d '{"requester":"smoke","category":"support","detail":"status"}'
curl -fsS -X POST "$BASE/api/deployments" -H 'Content-Type: application/json' -d '{"app_id":"crm","requester":"smoke","environment":"dev"}'
curl -fsS "$BASE/metrics" | grep -q lsk_requests_total
if [[ "${CHECK_MODEL:-0}" == "1" ]]; then
 curl -fsS -X POST "$BASE/api/agents/chat" -H 'Content-Type: application/json' -d '{"agent_id":"support","question":"How do invoice disputes work?"}' | python -c 'import json,sys; d=json.load(sys.stdin); assert d["mode"]=="real_model" and d["answer"]'
fi
echo "smoke passed (model check=${CHECK_MODEL:-0})"
