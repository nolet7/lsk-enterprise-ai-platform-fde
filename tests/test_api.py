import os, tempfile
os.environ["DB_PATH"]=tempfile.mktemp(suffix=".db")
from fastapi.testclient import TestClient
from app.main import app
def test_legacy_and_registry():
    with TestClient(app) as c:
        assert c.get("/healthz").status_code==200
        assert len(c.get("/api/apps").json())==2
        assert c.post("/api/tickets",json={"requester":"test","category":"invoice","detail":"question"}).status_code==200
        assert len(c.get("/api/tickets").json())==1
        assert c.post("/api/deployments",json={"app_id":"crm","requester":"test","environment":"prod"}).status_code==403
        assert len(c.get("/api/agents").json())==2
def test_unconfigured_real_model_fails_closed():
    with TestClient(app) as c:
        os.environ.pop("MODEL_BASE_URL",None)
        r=c.post("/api/agents/chat",json={"agent_id":"support","question":"hi"})
        assert r.status_code==503
