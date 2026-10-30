"""Shape only, not run. An A2A agent on AgentCore Runtime: Strands executor, agent card, port 9000.
The Runtime serves the card at .../invocations/.well-known/agent-card.json and forwards JSON-RPC.
"""
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from bedrock_agentcore.runtime.a2a import serve_a2a
from strands import Agent
from strands.multiagent.a2a import StrandsA2AExecutor


def make_agent(context_id: str) -> Agent:                 # one agent per A2A context (conversation)
    return Agent(name="refund_specialist", system_prompt="Refunds up to 250 GBP; escalate above.")


card = AgentCard(
    name="refund_specialist", description="Issues card refunds up to 250 GBP", version="1.0.0",
    url="https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/<urlencoded-arn>/invocations",
    capabilities=AgentCapabilities(streaming=False),
    default_input_modes=["text/plain"], default_output_modes=["text/plain"],
    skills=[AgentSkill(id="refund", name="refund", description="Refund a ticket amount", tags=["refund"])],
)

serve_a2a(StrandsA2AExecutor(agent_factory=make_agent), card)   # port from A2A_PORT env, default 9000

# Runtime side: create_agent_runtime(..., protocolConfiguration={"serverProtocol": "A2A"})
# Caller side: SigV4 or a JWT (customJWTAuthorizer) on every request; a2a-sdk A2ACardResolver + ClientFactory
# Governance side: front it with a Gateway HTTP target so Policy (Cedar) applies to agent-to-agent calls
