"""Minimal JSON-RPC MCP tool gateway for sandbox; not complete Streamable HTTP MCP."""
import uuid, json
from fastapi import Request, HTTPException
from pydantic import BaseModel
from .main import app, conn, tenant_for, record
class ToolCall(BaseModel):
    jsonrpc: str="2.0"
    id: str|int|None=None
    method: str
    params: dict={}
TOOLS=[
 {"name":"commercial.apps.list","description":"List public internal app registry entries; read-only","inputSchema":{"type":"object","properties":{},"additionalProperties":False}},
 {"name":"commercial.tickets.list","description":"List tickets belonging to verified caller tenant; read-only","inputSchema":{"type":"object","properties":{},"additionalProperties":False}}
]
@app.post("/mcp")
def mcp(request:Request, rpc:ToolCall):
    identity=getattr(request.state,"identity",None)
    if identity and "commercial-read" not in identity.get("roles",[]):
        raise HTTPException(403,"commercial-read role required")
    if rpc.jsonrpc!="2.0":raise HTTPException(400,"JSON-RPC 2.0 required")
    if rpc.method=="initialize":
        result={"protocolVersion":"2025-03-26","capabilities":{"tools":{}},"serverInfo":{"name":"lsk-commercial-sandbox","version":"0.1.0"}}
    elif rpc.method=="tools/list":
        result={"tools":TOOLS}
    elif rpc.method=="tools/call":
        name=rpc.params.get("name")
        if rpc.params.get("arguments",{})!={}:
            raise HTTPException(400,"Tool takes no arguments")
        with conn() as c:
            if name=="commercial.apps.list":
                data=[dict(row) for row in c.execute("SELECT id,name,owner,kind FROM apps")]
            elif name=="commercial.tickets.list":
                data=[dict(row) for row in c.execute("SELECT id,category,detail,status FROM tickets WHERE tenant=?",(tenant_for(request),))]
            else:raise HTTPException(404,"Tool not allowed")
        record("tool_call",{"tool":name,"trace_id":str(uuid.uuid4()),"tenant":tenant_for(request)})
        result={"content":[{"type":"text","text":json.dumps(data)}],"isError":False}
    else:raise HTTPException(404,"Unsupported MCP method")
    return {"jsonrpc":"2.0","id":rpc.id,"result":result}
