# MCP sandbox gateway
Implemented on pilot and production branches: POST /mcp, JSON-RPC 2.0 methods initialize, tools/list, tools/call; two allowlisted read-only tools. Uses the existing bearer OIDC middleware and requires the commercial-read realm role when identity is enabled. Tenant filtering occurs at SQL query time for ticket records.
**Scope:** demonstration subset only: no complete MCP Streamable HTTP session lifecycle, content negotiation, resources, OAuth protected resource metadata, token exchange, dynamic client registration or delegated vendor OAuth. Do not claim compatibility/security certification without a standard-conformance test and authorization-server integration.
Example (development only):
```bash
curl -fsS localhost:18743/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
curl -fsS localhost:18743/mcp -H 'Content-Type: application/json' -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"commercial.apps.list","arguments":{}}}'
```
Add Authorization: Bearer <signed access token> with tenant_id and commercial-read role when REQUIRE_AUTH=true.
