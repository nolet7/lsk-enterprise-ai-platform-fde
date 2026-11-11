import os, time
import httpx
from fastapi import HTTPException
from prometheus_client import Counter, Histogram
TOKENS=Counter("lsk_llm_tokens_total","Reported token consumption",["type","model"])
MODEL_LATENCY=Histogram("lsk_llm_seconds","Model latency",["model"])\nESTIMATED_COST=Counter("lsk_llm_estimated_cost_usd_total","Estimated inference cost (configured USD prices per 1M tokens)",["model"])
async def infer(messages):
    base=os.getenv("MODEL_BASE_URL","").rstrip("/")
    key=os.getenv("MODEL_API_KEY","")
    model=os.getenv("MODEL_NAME","")
    if not base or not model:
        raise HTTPException(503,"Real model not configured. Set MODEL_BASE_URL, MODEL_NAME and MODEL_API_KEY if required.")
    start=time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r=await client.post(base+"/chat/completions",headers={"Authorization":"Bearer "+(key or "local")},json={"model":model,"messages":messages,"temperature":0.1,"max_tokens":350})
            r.raise_for_status()
            data=r.json()
        usage=data.get("usage") or {}
        for kind,keyname in (("input","prompt_tokens"),("output","completion_tokens")): TOKENS.labels(kind,model).inc(usage.get(keyname,0))\n        # Explicit customer-configured prices, not a claim about current provider pricing.\n        input_price=float(os.getenv("MODEL_INPUT_USD_PER_M", "0"))\n        output_price=float(os.getenv("MODEL_OUTPUT_USD_PER_M", "0"))\n        if input_price or output_price:\n            cost=(usage.get("prompt_tokens",0)*input_price+usage.get("completion_tokens",0)*output_price)/1_000_000\n            ESTIMATED_COST.labels(model).inc(cost)
        return data["choices"][0]["message"]["content"],usage
    except (httpx.HTTPError,KeyError,IndexError,ValueError) as exc:
        raise HTTPException(502,"Model inference failed; check endpoint and provider credentials") from exc
    finally: MODEL_LATENCY.labels(model or "unset").observe(time.monotonic()-start)
