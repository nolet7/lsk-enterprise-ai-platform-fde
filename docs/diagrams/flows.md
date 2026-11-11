# POC system architecture
```mermaid
flowchart LR
 U[Commercial user] --> P[Browser portal]
 P --> API[FastAPI commercial IT service]
 API --> DB[(SQLite legacy app registry / tickets / deployment requests)]
 API --> R[Agent registry + retrieval]
 R --> M[OpenAI-compatible hosted API or local model]
 M --> R --> API --> P
 API --> PM[Prometheus metrics endpoint]
```
Legacy path remains functional without model. POC identity is not trusted. Production path must add verified OIDC, per-tenant authorization, secrets and auditable boundaries.
