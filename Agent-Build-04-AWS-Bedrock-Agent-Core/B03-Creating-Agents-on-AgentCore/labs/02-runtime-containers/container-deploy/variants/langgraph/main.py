"""Same HTTP contract, LangGraph loop. Proves the Runtime does not care which framework runs
inside the container: BedrockAgentCoreApp owns /invocations and /ping, the graph owns the loop.
Needs: pip install langgraph langchain-aws (not in the shared venv; container-only)."""
from bedrock_agentcore import BedrockAgentCoreApp, RequestContext

app = BedrockAgentCoreApp()
_graph = None


def graph():
    global _graph
    if _graph is None:
        from langchain_aws import ChatBedrockConverse
        from langgraph.prebuilt import create_react_agent

        def get_ticket(ticket_id: str) -> str:
            """Return one support ticket by id."""
            return {"T-1001": "Ayşe, charged twice for a coffee, 4.50 GBP"}.get(ticket_id, "no such ticket")

        _graph = create_react_agent(ChatBedrockConverse(model="global.anthropic.claude-haiku-5-5"), tools=[get_ticket],
                                    prompt="UK card-team ticket assistant. Refunds above 250 GBP need a human.")
    return _graph


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):
        return {"error": "payload.prompt must be a string"}
    out = graph().invoke({"messages": [("user", prompt)]}, config={"configurable": {"thread_id": context.session_id}})
    return {"result": out["messages"][-1].content}


if __name__ == "__main__":
    app.run()
