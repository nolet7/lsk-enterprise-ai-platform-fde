import os, sqlite3, time, json, uuid
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from .model import infer
from .agents import AGENTS, run_agent

DB = os.getenv("DB_PATH", "/tmp/lsk-platform.db")
REQUESTS = Counter("lsk_requests_total", "Requests", ["operation","status"])
DURATION = Histogram("lsk_operation_seconds", "Operation duration", ["operation"])
app = FastAPI(title="LSK Enterprise AI Platform", version="0.1.0")
def conn():
    c = sqlite3.connect(DB, timeout=10)
    c.row_factory=sqlite3.Row
    return c
def init():
    Path(DB).parent.mkdir(parents=True, exist_ok=True)
    with conn() as c:
        c.executescript("""CREATE TABLE IF NOT EXISTS apps (id TEXT PRIMARY KEY, name TEXT, owner TEXT, kind TEXT);
        CREATE TABLE IF NOT EXISTS tickets (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, requester TEXT, category TEXT, detail TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS deployments (id TEXT PRIMARY KEY, tenant TEXT NOT NULL, app_id TEXT, requester TEXT, environment TEXT, status TEXT);
        CREATE TABLE IF NOT EXISTS audit (id TEXT PRIMARY KEY, event TEXT, detail TEXT);""")
        c.execute("INSERT OR IGNORE INTO apps VALUES ('crm','Commercial CRM','sales','legacy')")
        c.execute("INSERT OR IGNORE INTO apps VALUES ('procurement','Procurement Desk','finance','legacy')")
@app.on_event("startup")
def startup(): init()
class Ticket(BaseModel):
    requester:str
    category:str
    detail:str
class Deployment(BaseModel):
    app_id:str
    requester:str
    environment:str="dev"
class Chat(BaseModel):
    agent_id:str
    question:str
    tenant:str="demo"
def tenant_for(request: Request):\n    identity=getattr(request.state,"identity",None)\n    if identity:return identity["tenant"]\n    if os.getenv("REQUIRE_AUTH","false").lower()=="true":raise HTTPException(401,"Identity required")\n    return "demo"\ndef record(event,detail):
    with conn() as c: c.execute("INSERT INTO audit VALUES (?,?,?)",(str(uuid.uuid4()),event,json.dumps(detail)))
@app.get("/healthz")
def health():return {"status":"ok","mode":"poc"}
@app.get("/readyz")
def ready():return {"status":"ready"}
@app.get("/metrics")
def metrics():return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@app.get("/")
def portal():return FileResponse("/app/frontend/index.html")
@app.get("/api/apps")
def apps():
    with conn() as c:return [dict(x) for x in c.execute("SELECT * FROM apps")]
@app.get("/api/tickets")
def tickets():
    with conn() as c:return [dict(x) for x in c.execute("SELECT * FROM tickets ORDER BY rowid DESC")]
@app.post("/api/tickets")
def create_ticket(t:Ticket,request:Request):
    t_id=str(uuid.uuid4())
    with conn() as c:c.execute("INSERT INTO tickets VALUES (?,?,?,?,?,?)",(t_id,tenant_for(request),t.requester,t.category,t.detail,"open"))
    REQUESTS.labels("legacy_ticket","ok").inc()
    record("ticket_created",{"id":t_id})
    return {"id":t_id,"status":"open"}
@app.post("/api/deployments")
def deployment(d:Deployment,request:Request):
    if d.environment not in ("dev","test"):raise HTTPException(403,"POC only accepts dev/test")
    with conn() as c:
        if not c.execute("SELECT id FROM apps WHERE id=?",(d.app_id,)).fetchone():raise HTTPException(404,"Unknown app")
        d_id=str(uuid.uuid4())
        c.execute("INSERT INTO deployments VALUES (?,?,?,?,?,?)",(d_id,tenant_for(request),d.app_id,d.requester,d.environment,"requested"))
    record("deployment_requested",{"id":d_id})
    return {"id":d_id,"status":"requested","note":"No deployment executed; approval needed"}
@app.get("/api/deployments")
def deployments():
    with conn() as c:return [dict(x) for x in c.execute("SELECT * FROM deployments")]
@app.get("/api/agents")
def agents():return [{"id":k,**v} for k,v in AGENTS.items()]
@app.post("/api/agents/chat")
async def chat(q:Chat,request:Request):
    if q.agent_id not in AGENTS: raise HTTPException(404,"Unknown agent")
    start=time.monotonic()
    try:
        result=await run_agent(q.agent_id,q.question,tenant_for(request))
        REQUESTS.labels("ai_chat","ok").inc()
        record("agent_answer",{"agent":q.agent_id,"tenant":tenant_for(request),"trace_id":result["trace_id"]})
        return result
    except Exception:
        REQUESTS.labels("ai_chat","error").inc()
        raise
    finally:DURATION.labels("ai_chat").observe(time.monotonic()-start)
@app.get("/api/audit")
def audit():
    with conn() as c:return [dict(x) for x in c.execute("SELECT * FROM audit ORDER BY rowid DESC LIMIT 100")]

# Pilot modules are optional in POC; fail closed when REQUIRE_AUTH=true.
from middleware.identity import auth_gate
from observability.otel import instrument
app.middleware("http")(auth_gate)
instrument(app)
\n# Import read-only tool gateway after route declarations to avoid circular initialization.\nfrom . import mcp_gateway\n