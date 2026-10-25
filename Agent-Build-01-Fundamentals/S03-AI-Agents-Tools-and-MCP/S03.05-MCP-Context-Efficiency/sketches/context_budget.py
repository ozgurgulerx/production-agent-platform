"""Context-budget enforcement sketch for S03.05 (untested).

Enforces the generation-headroom rule before each model call:
measure input (including tool definitions), compare to a budget,
reduce in a fixed order, and refuse to send if pinned material alone
exceeds the budget. Replace the helper stubs with real implementations.
"""

WINDOW = 200_000          # from the model's documentation; not returned by the API
MAX_OUTPUT = 16_000       # passed as max_tokens / max_output_tokens
BUDGET = int(WINDOW * 0.75) - MAX_OUTPUT


class ContextOverBudget(Exception):
    pass


def count_tokens(messages, tools) -> int:
    """Exact: Anthropic messages.count_tokens; local: tiktoken for OpenAI models.
    Cheap trigger: previous usage.input_tokens plus what was appended since."""
    raise NotImplementedError


def mask_old_tool_results(messages, keep_last: int):
    """Replace bodies of tool results older than the last `keep_last` with a
    one-line reference, e.g. 'get_tickets(uk) -> 2,000 rows, artifact A-12'."""
    raise NotImplementedError


def drop_turns_outside_window(messages, keep_last: int):
    """Drop whole turns older than the last `keep_last`; pinned state is never dropped."""
    raise NotImplementedError


def summarise_old_turns(messages):
    """The one step that costs a model call. Keep references so facts can be re-fetched."""
    raise NotImplementedError


def prepare(messages, tools):
    if count_tokens(messages, tools) <= BUDGET:
        return messages
    messages = mask_old_tool_results(messages, keep_last=3)
    if count_tokens(messages, tools) <= BUDGET:
        return messages
    messages = drop_turns_outside_window(messages, keep_last=6)
    if count_tokens(messages, tools) <= BUDGET:
        return messages
    messages = summarise_old_turns(messages)
    if count_tokens(messages, tools) > BUDGET:
        raise ContextOverBudget("pinned material alone exceeds the budget: split the task")
    return messages
