"""Pilot identity gate. Only validated issuer-signed JWTs; user-provided tenant ignored."""
import os, json
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, Request
from starlette.responses import JSONResponse
from prometheus_client import Counter
DENIED=Counter("lsk_authorization_denied_total","Denied actions",["reason"])
PUBLIC={"/healthz","/readyz"}
async def auth_gate(request:Request,call_next):
    if os.getenv("REQUIRE_AUTH","false").lower()!="true" or request.url.path in PUBLIC:
        return await call_next(request)
    token=request.headers.get("Authorization","")
    if not token.startswith("Bearer "):
        DENIED.labels("no_bearer").inc()
        return JSONResponse({"detail":"Bearer token required"},status_code=401)
    try:
        issuer=os.environ["OIDC_ISSUER"].rstrip("/")
        audience=os.environ["OIDC_AUDIENCE"]
        jwks=PyJWKClient(issuer+"/protocol/openid-connect/certs",cache_jwk_set=True,lifespan=300)
        key=jwks.get_signing_key_from_jwt(token[7:]).key
        claims=jwt.decode(token[7:],key,algorithms=["RS256"],issuer=issuer,audience=audience,options={"require":["exp","iss","aud","sub"]})
        tenant=claims.get("tenant_id")
        if not isinstance(tenant,str) or not tenant or len(tenant)>80:
            raise ValueError("No trusted tenant claim")
        request.state.identity={"subject":claims["sub"],"tenant":tenant,"roles":claims.get("realm_access",{}).get("roles",[])}
    except Exception:
        DENIED.labels("invalid_token").inc()
        return JSONResponse({"detail":"Invalid identity or tenant"},status_code=401)
    # All handlers must derive tenant from request.state.identity, never client JSON.\n    if request.url.path.startswith("/api/deployments") and request.method=="POST" and "platform-requester" not in request.state.identity["roles"]:
        DENIED.labels("missing_role").inc()
        return JSONResponse({"detail":"platform-requester role required"},status_code=403)
    return await call_next(request)
