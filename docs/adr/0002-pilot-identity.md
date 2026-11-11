# ADR 0002: OIDC access tokens not client headers
Use RS256 signed OIDC JWT verified against Keycloak JWKS, issuer, audience and expiry; derive tenant from a trusted mapped claim. Reject missing identity. Roles govern deployment requests.
Remaining gap: tenant row-level checks on all legacy endpoints, retrieval indexes, management plane and MCP tools. Audit and tests before production.
