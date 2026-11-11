# Identity, requests and model data boundaries
```mermaid
sequenceDiagram
 participant User
 participant IdP as Keycloak/Enterprise IdP
 participant API as Portal API
 participant DB as Tenant-filtered legacy DB
 participant Model as Hosted API or private model
 User->>IdP: OIDC sign-in
 IdP-->>User: Signed access token
 User->>API: Bearer JWT and support request
 API->>IdP: Fetch trusted JWKS
 API->>API: Verify issuer, audience, signature, expiry, tenant
 API->>DB: Tenant-filtered ticket lookup
 API->>Model: Approved synthetic/authorized context only
 Model-->>API: Completion with provider usage
 API-->>User: Grounded answer and source IDs
```
Hosted model call explicitly sends selected context outside customer's network. Private vLLM requires GPU node, model license, private service and checked network policies.
