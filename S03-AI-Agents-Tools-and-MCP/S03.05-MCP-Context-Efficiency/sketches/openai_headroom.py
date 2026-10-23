"""Generation-headroom example on the OpenAI Responses API (untested).

Shows where the output cap and reasoning control go, how to detect
truncation, and which usage fields report cached and reasoning tokens.
Field names are as known for the SDK in mid-2026; check the pinned version.
"""

from openai import OpenAI
import tiktoken

client = OpenAI()
MODEL = "gpt-5.5"
WINDOW = 400_000                 # from the model card; not returned by the API
MAX_OUTPUT = 16_000              # the cap we pass; reasoning tokens count inside it
BUDGET = int(WINDOW * 0.75) - MAX_OUTPUT

# tiktoken has no public encoding for the newest models; this is an estimate,
# fine as a trigger, not as a hard limit.
enc = tiktoken.encoding_for_model("gpt-4o")


def count(messages, tools) -> int:
    text = "".join(m["content"] for m in messages) + str(tools)
    return len(enc.encode(text))


def call(messages, tools):
    assert count(messages, tools) <= BUDGET, "reduce input first (see context_budget.prepare)"
    resp = client.responses.create(
        model=MODEL,
        input=messages,
        tools=tools,
        max_output_tokens=MAX_OUTPUT,        # output cap: answer + reasoning
        reasoning={"effort": "medium"},      # reasoning control; levels, not a token number
    )
    if resp.status == "incomplete" and resp.incomplete_details.reason == "max_output_tokens":
        raise RuntimeError("truncated: treat like a timeout, not a result")
    u = resp.usage
    print(
        "input", u.input_tokens,
        "cached", u.input_tokens_details.cached_tokens,
        "output", u.output_tokens,
        "reasoning", u.output_tokens_details.reasoning_tokens,
    )
    return resp


# The same two settings in the OpenAI Agents SDK go through ModelSettings:
#
#   from agents import Agent, ModelSettings
#   agent = Agent(name="support", tools=[...],
#                 model_settings=ModelSettings(max_tokens=16_000,
#                                              reasoning={"effort": "medium"}))
#
# and RunResult exposes usage per run.
#
# Chat Completions equivalents: max_completion_tokens, reasoning_effort,
# truncation signalled by finish_reason == "length".
