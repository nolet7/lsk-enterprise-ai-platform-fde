# Pilot install and acceptance
1. Start with validated POC, deploy Keycloak in customer's sandbox and configure realm, audience, tenant claim and requester role.
2. Set REQUIRE_AUTH=true, OIDC_ISSUER and OIDC_AUDIENCE; restart API. Example only: DO NOT expose without TLS and gateway.
3. Obtain genuine user access tokens through approved OIDC flow. Anonymous /api/apps MUST return 401.
4. Run authorization denial matrix in security/tenant-boundary.md; attach command outputs to evidence.
5. Run ACCESS_TOKEN=... python scripts/load.py and ACCESS_TOKEN=... python evals/benchmark.py with real inference configured.
6. Review citation quality and prompt injection outputs manually; store findings in customer evidence system, not in source control.
7. Gate: NO multi-tenant confidential datasets until application registry, tickets, deployment list, corpus retrieval and connector tools each enforce tenant row-level authorization. This implementation does not meet that gate.
