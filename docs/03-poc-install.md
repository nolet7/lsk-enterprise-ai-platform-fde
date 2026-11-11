# POC installation and reproduction
Prereqs: Docker with Compose; or Python 3.12. No GCP account needed. Ports: 18743.
1. Copy .env.example to .env. Set MODEL_BASE_URL and MODEL_NAME to a real OpenAI-compatible endpoint; set MODEL_API_KEY when applicable. Do not commit .env.
2. Run `docker compose --env-file .env up --build -d`.
3. Browse http://localhost:18743 ; confirm apps list; create legacy support ticket; request dev deployment; ask AI.
4. Run `bash scripts/smoke.sh` then `CHECK_MODEL=1 bash scripts/smoke.sh` to exercise actual model inference.
5. Run `docker compose logs -f platform`; `curl localhost:18743/metrics`.
6. Unit tests: `python -m venv .venv && . .venv/bin/activate && pip install -r tests/requirements.txt && PYTHONPATH=backend pytest -q`.
CPU local option: install Ollama on host, run `ollama pull qwen2.5:1.5b`, then `ollama serve`. Docker may reach `http://host.docker.internal:11434/v1` on Docker Desktop; ensure Ollama binds an address reachable from Docker. Set MODEL_NAME=qwen2.5:1.5b. A CPU-only 1.5B model is slower and lower quality.
Hosted model API means prompts and snippets leave the network boundary. Never use confidential production data without approval.
POC deliberately has NO authentication, tenant enforcement, delegated tools, or durable database. It is not production safe.
