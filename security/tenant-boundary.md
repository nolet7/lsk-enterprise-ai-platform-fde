# Pilot security test matrix
- No bearer -> 401; expired/wrong issuer/wrong audience/bad signature -> 401.
- Missing tenant_id in signed access token -> 401.
- Client-submitted tenant different from claim -> tenant overwritten for agent calls. All downstream connectors must also derive tenant from verified principal.
- Missing platform-requester role -> deployment request denied 403.
- AI tools are read-only; no write action allowed.
- NOTE: legacy ticket/app queries and deployment list are NOT tenant scoped in this pilot; sensitive tenant data must NOT be loaded until row-level filtering, policies and tests are implemented.
- Metrics protected when REQUIRE_AUTH=true.
- Prompt injection suite must use benchmark and require manual review; source overlap alone does not prove quality/safety.
