# Mandatory production blockers
1. Replace SQLite /tmp with durable tenant-scoped PostgreSQL and implement row-level isolation for all legacy resources, retrieval, audit and deployment endpoints.
2. Implement actual delegated OAuth/MCP tool adapters with scope enforcement and negative tests.
3. Configure admission signature verification, SBOM scans, pinned digest, workload identity, external secrets, private networking and a customer-approved egress policy.
4. Verify prompt injection defense, evaluation thresholds, model licensing, PII masking, deletion and retention.
5. Deploy full OTel collector, Loki, Tempo, Grafana, alert rules and approved log redaction.
6. Prove encrypted backups and successful restore, DR failover exercises, and rollback rehearsal.
7. Production does not proceed until signed customer security and change-management review.
