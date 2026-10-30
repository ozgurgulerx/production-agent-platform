"""REQUEST interceptor for the ticket Gateway: refuse `issue_refund` above £250 before the target is called, and
stamp a header. Event/response envelope follows the Gateway interceptor docs; field names marked verify."""

import json

LIMIT = 250.0


def handler(event, context):
    print(json.dumps(event)[:2000])
    mcp = event.get("mcp", {})                                         # verify: envelope key
    body = mcp.get("gatewayRequest", {}) if isinstance(mcp, dict) else {}
    params = body.get("params", {}) if isinstance(body, dict) else {}
    name = str(params.get("name", ""))
    args = params.get("arguments", {}) or {}
    if name.endswith("issue_refund") and float(args.get("amount", 0)) > LIMIT:
        return {"interceptorOutputVersion": "1.0",
                "mcp": {"transformedGatewayRequest": None,
                        "error": {"code": -32000, "message": f"interceptor: refunds above £{LIMIT:.0f} need a human"}}}   # verify
    body.setdefault("headers", {})["x-interceptor"] = "ticket-gateway"
    return {"interceptorOutputVersion": "1.0", "mcp": {"transformedGatewayRequest": body}}   # verify
