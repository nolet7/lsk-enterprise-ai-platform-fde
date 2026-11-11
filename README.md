# LSK Enterprise AI Platform — Forward Deployment Engineering

Fictional B2B commercial IT and digital services organization. **Legacy first:** existing application registry, support requests and deployment-approval requests. AI support and procurement RAG are layered onto those workflows using a configurable **real OpenAI-compatible chat model endpoint**; no fabricated inference fallback.

## Phase branches

- [main](https://github.com/nolet7/lsk-enterprise-ai-platform-fde/tree/main): immutable kickoff baseline.
- [poc](https://github.com/nolet7/lsk-enterprise-ai-platform-fde/tree/poc): browser portal, FastAPI legacy workflows, synthetic knowledge assistants, model adapter, Prometheus counters, Docker Compose, smoke and Python unit tests.
- [pilot](https://github.com/nolet7/lsk-enterprise-ai-platform-fde/tree/pilot): inherits POC; adds verified OIDC JWT gate, tenant-filtered tickets/deployments, read-only MCP JSON-RPC tool subset, performance/evaluation scripts and optional MLflow tracking, reference vLLM.
- [production](https://github.com/nolet7/lsk-enterprise-ai-platform-fde/tree/production): inherits pilot; adds Terraform GKE/VPC, Helm, Argo CD, alerting, SRE runbooks, FDE handover and security gates. **Reference only; no real GCP deployment has been performed.**

## Run the POC

```bash
git clone https://github.com/nolet7/lsk-enterprise-ai-platform-fde.git
cd lsk-enterprise-ai-platform-fde
git checkout poc
cp .env.example .env
# Edit .env for a REAL hosted or locally reachable OpenAI-compatible model
docker compose --env-file .env up --build -d
bash scripts/smoke.sh
CHECK_MODEL=1 bash scripts/smoke.sh
```

Open http://localhost:18743. For pilot/production use the respective branches and read docs/04-pilot-runbook.md and docs/05-production-install.md.

## Engineering status and hard gates

This is a demonstration repository, **not a certified enterprise platform**. GitHub commits prove upload, not execution. Model smoke test requires credentials and a reachable endpoint. GitHub CI status must be checked before claiming tests passed.

Pilot currently uses SQLite, synthetic corpus and no full delegated OAuth vendor integration, production database, cloud cost quota enforcement, Kubernetes GPU benchmark or fully instrumented OTel/Loki/Tempo/Grafana stack. The MCP endpoint is an allowlisted JSON-RPC subset, not a full conformance-tested Streamable HTTP implementation. The current production chart has an intentionally missing image digest and must not deploy without approved inputs.

The production security gate in [security/required-gates.md](https://github.com/nolet7/lsk-enterprise-ai-platform-fde/blob/production/security/required-gates.md) lists required engineering and customer validation before real tenant data or production operations.

**Data residency:** hosted model providers receive prompt context. For private inference, deploy a tested customer-hosted GPU model service with approved egress policy; CPU-only Ollama is a local development option.
