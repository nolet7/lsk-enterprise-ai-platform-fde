# Observability wiring
Configure OTLP_EXPORTER_OTLP_ENDPOINT to an authenticated collector endpoint. Route traces to Tempo, redacted structured logs to Loki, metrics to Prometheus via approved scrape authentication. Do not emit raw prompts, tokens, API keys or customer documents. Grafana panels: model latency histogram, reported token counters, API success/fail, auth denial, saturation, cost estimation (needs verified price table), retrieval quality from eval artifacts and tool failure once real tools are added.
No Loki/Tempo/Grafana servers are bundled or verified in this pilot.
