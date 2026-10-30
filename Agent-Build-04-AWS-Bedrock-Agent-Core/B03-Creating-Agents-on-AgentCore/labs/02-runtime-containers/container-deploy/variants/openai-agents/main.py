"""Same HTTP contract, OpenAI Agents SDK loop talking to Bedrock through the OpenAI-compatible
`bedrock-mantle` endpoint (L3). Proves the contract is framework-neutral. Container-only deps:
pip install openai-agents. Auth to Mantle is SigV4 via the IAM role; verify the base URL for
your region before building."""
import asyncio
import os

from bedrock_agentcore import BedrockAgentCoreApp, RequestContext

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload: dict, context: RequestContext) -> dict:
    prompt = payload.get("prompt")
    if not isinstance(prompt, str):
        return {"error": "payload.prompt must be a string"}
    from agents import Agent, Runner, function_tool

    @function_tool
    def get_ticket(ticket_id: str) -> str:
        """Return one support ticket by id."""
        return {"T-1001": "Ayşe, charged twice for a coffee, 4.50 GBP"}.get(ticket_id, "no such ticket")

    agent = Agent(name="ticket", instructions="UK card-team ticket assistant.", tools=[get_ticket],
                  model=os.environ.get("OPENAI_MODEL", "openai.gpt-oss-120b-1:0"))  # verify: Mantle model id spelling
    result = asyncio.run(Runner.run(agent, prompt))
    return {"result": result.final_output, "session_id": context.session_id}


if __name__ == "__main__":
    app.run()
