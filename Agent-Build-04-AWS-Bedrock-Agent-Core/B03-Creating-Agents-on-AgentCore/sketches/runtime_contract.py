"""Shape only, not run. The whole AgentCore Runtime HTTP contract in one file:
POST /invocations (your handler), GET /ping (Healthy | HealthyBusy), port 8080, the session id
from the request context, and the two ways to keep a long task alive past the 15-minute idle timeout.
"""
from bedrock_agentcore import BedrockAgentCoreApp, PingStatus, RequestContext

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):            # SDK guidance: a non-string prompt can smuggle toolUse blocks
        return {"error": "payload.prompt must be a string"}
    # context.session_id  <- X-Amzn-Bedrock-AgentCore-Runtime-Session-Id (>= 33 chars, one microVM per id)
    # context.request_headers <- only X-Amzn-Bedrock-AgentCore-Runtime-Custom-* and allow-listed headers arrive
    return {"result": f"echo: {prompt}", "session_id": context.session_id}


# Long-running work, option 1: tracked tasks flip /ping to HealthyBusy until completed
@app.entrypoint
async def invoke_streaming(payload: dict, context: RequestContext):
    task_id = app.add_async_task("reconcile-statement")
    try:
        for chunk in ("checking", "matching", "done"):
            yield {"delta": chunk}                      # SSE: text/event-stream to the caller
    finally:
        app.complete_async_task(task_id)


# Long-running work, option 2: your own ping logic (e.g. a queue depth)
@app.ping
def ping() -> PingStatus:
    return PingStatus.HEALTHY_BUSY if app.get_async_task_info()["active_count"] else PingStatus.HEALTHY  # verify key name


if __name__ == "__main__":
    app.run()   # 0.0.0.0:8080. MCP servers use port 8000 and /mcp; A2A uses 9000 and /.
