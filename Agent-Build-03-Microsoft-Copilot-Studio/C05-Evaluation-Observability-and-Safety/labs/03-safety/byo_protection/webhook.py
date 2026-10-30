"""Bring-your-own-protection webhook: block issue_refund above 250 GBP before the tool runs.

Proves: a deterministic business rule can sit at the tool boundary of a Copilot Studio agent (reading map F12,
preview). The platform calls this endpoint before every tool invocation, waits ≤ 1 s and ALLOWS on timeout, so the
decision stays local and fast. Auth: the platform presents an Entra token issued through a federated identity
credential; validate issuer/audience in production (left as a TODO here, marked verify). Envelope keys are marked
verify until the first real call; the handler tolerates missing fields.
"""
import logging
import os
import time

from fastapi import FastAPI, Request

LIMIT_GBP = float(os.environ.get("REFUND_LIMIT_GBP", "250"))
log = logging.getLogger("byo-protection")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
app = FastAPI(title="ticket-agent protection")


def decide(body: dict) -> dict:
    tool = body.get("tool") or {}
    name = (tool.get("name") or body.get("toolName") or "").split("___")[-1]      # verify: envelope key names
    args = tool.get("arguments") or body.get("arguments") or {}
    if name == "issue_refund":
        try:
            amount = float(args.get("amount_gbp", args.get("amount", 0)))
        except (TypeError, ValueError):
            return {"decision": "block", "reason": "refund amount missing or not a number"}
        if amount > LIMIT_GBP:
            return {"decision": "block", "reason": f"refund of {amount:g} GBP exceeds the {LIMIT_GBP:g} GBP limit; route to the UK card team"}
    return {"decision": "allow"}


@app.post("/protect")
async def protect(req: Request) -> dict:
    t0 = time.perf_counter()
    try:
        body = await req.json()
    except Exception:  # noqa: BLE001
        body = {}
    # TODO verify: validate the bearer token (issuer https://login.microsoftonline.com/<tenant>/v2.0, audience = this app)
    result = decide(body)
    log.info("%s %s -> %s (%.0f ms)", (body.get("tool") or {}).get("name"), (body.get("tool") or {}).get("arguments"),
             result["decision"], (time.perf_counter() - t0) * 1000)
    return result


@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "limit_gbp": LIMIT_GBP}
