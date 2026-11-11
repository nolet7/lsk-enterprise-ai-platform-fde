import os,tempfile
os.environ["DB_PATH"]=tempfile.mktemp(suffix=".db")
from fastapi.testclient import TestClient
from app.main import app
def test_mcp_allowed_tools_and_denied_unknown():
    with TestClient(app) as c:
        r=c.post("/mcp",json={"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}})
        assert r.status_code==200
        assert len(r.json()["result"]["tools"])==2
        t=c.post("/mcp",json={"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"commercial.apps.list","arguments":{}}})
        assert t.status_code==200
        assert "crm" in t.json()["result"]["content"][0]["text"]
        bad=c.post("/mcp",json={"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"system.execute","arguments":{}}})
        assert bad.status_code==404
def test_authentication_gate():
    os.environ["REQUIRE_AUTH"]="true"
    try:
        with TestClient(app) as c:
            assert c.get("/api/tickets").status_code==401
            assert c.post("/mcp",json={"jsonrpc":"2.0","id":1,"method":"tools/list"}).status_code==401
    finally:os.environ.pop("REQUIRE_AUTH",None)
