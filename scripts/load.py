"""Synthetic tenant-safe traffic; does not fabricate a success result."""
import concurrent.futures, urllib.request, json, time, os
base=os.getenv("BASE_URL","http://127.0.0.1:18743")
n=int(os.getenv("REQUEST_COUNT","40"))
token=os.getenv("ACCESS_TOKEN")
def hit(i):
    data=json.dumps({"requester":"load","category":"synthetic","detail":f"load-{i}"}).encode()
    h={"Content-Type":"application/json"}
    if token:h["Authorization"]="Bearer "+token
    t=time.monotonic()
    try:
        with urllib.request.urlopen(urllib.request.Request(base+"/api/tickets",data,headers=h),timeout=10) as r:return (r.status,round(time.monotonic()-t,4))
    except Exception:return (0,round(time.monotonic()-t,4))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:results=list(ex.map(hit,range(n)))
good=sum(s==200 for s,_ in results)
print(json.dumps({"requests":n,"success":good,"failed":n-good,"p95_seconds":sorted(x[1] for x in results)[max(0,int(n*0.95)-1)]},indent=2))
if good!=n:raise SystemExit(1)
