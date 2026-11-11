# ADR 0001: hosted API vs self-hosted
Decision: OpenAI-compatible inference abstraction; hosted endpoint for fastest POC; optional customer-hosted vLLM for approved GPU pilot.
Hosted: lower setup cost, outbound confidential data requires provider review and contractual terms.
vLLM: GPU memory and operational staffing; budget depends on model context and concurrency. Example starting assessment: single NVIDIA GPU with >=24GB VRAM for a quantized 7B-8B model; test exact model compatibility and KV-cache concurrency. Larger models may need 48-80GB+ or tensor parallelism.
CPU demo: Ollama 1.5B; not vLLM production parity.
KServe only when multiple independently scaled models, rollout policies, and inference workload justify controller overhead. For a single vLLM deployment use plain Kubernetes Deployment and Service first.
