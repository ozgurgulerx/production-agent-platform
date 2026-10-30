"""Shape only, not run. The one line that differs between cloud and local for a Strands agent.
Everything below `build_agent` is identical to B03 lab 01; only `make_model` changes."""
import os

from strands import Agent
from strands.models import BedrockModel
from strands.models.llamacpp import LlamaCppModel


def make_model(provider: str):
    if provider == "bedrock":                                   # SigV4, guardrails, service tier: the cloud arguments
        return BedrockModel(model_id=os.environ.get("BEDROCK_MODEL_ID", "global.anthropic.claude-haiku-5-5"),
                            guardrail_id=os.environ.get("GUARDRAIL_ID"), guardrail_version=os.environ.get("GUARDRAIL_VERSION"))
    if provider == "ollama":                                    # needs: pip install "strands-agents[ollama]"
        from strands.models.ollama import OllamaModel           # import inside so the module loads without the extra
        return OllamaModel(host="http://localhost:11434", model_id="qwen3:8b", keep_alive="5m")   # no guardrail argument exists
    if provider == "llamacpp":                                  # llama-server --jinja -m model.gguf --port 8080
        return LlamaCppModel(base_url="http://localhost:8080", model_id="default")
    raise ValueError(provider)


def build_agent(provider: str, tools: list) -> Agent:
    return Agent(model=make_model(provider), tools=tools,
                 system_prompt="UK card team support assistant. Refunds above 250 GBP need a human.")
