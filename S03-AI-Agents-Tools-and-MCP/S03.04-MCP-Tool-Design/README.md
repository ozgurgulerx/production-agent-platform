# MCP Tool Design

“How would you expose our systems to an agent?” is one of the most common architect questions. The weak answer is “wrap the APIs as tools”. The strong answer is “I’d start from what the agent needs to get done, build a small set of **intent-level tools** with precise descriptions, keep the deterministic logic in code, and measure wrong-tool rate before adding more.” The sections below turn that answer into concrete design decisions and evaluation checks.

## Designing the tool interface

**Intent-based tools address the workflow boundary, but good tool design also determines whether the agent can choose, call, and recover from a tool reliably.** These principles apply beyond MCP; MCP provides the interface for exposing them.

Think about seven dimensions:

| Dimension | Design question | Meeting example |
|---|---|---|
| **1. Scope** | Does the tool represent a coherent action without hiding decisions that require judgment? | `reschedule_meeting` moves a specified meeting; it shouldn’t quietly choose a different day. |
| **2. Discoverability** | Can the agent distinguish this tool from nearby alternatives? | Explain when to use `reschedule_meeting` versus `propose_meeting_times`, including their side effects. |
| **3. Input clarity** | Can the agent provide valid arguments without guessing? | Require an event ID, explicit time zone, and start time; avoid an ambiguous `date: "Tuesday"`. |
| **4. Output usefulness** | Does the result support the agent’s next decision? | Return the confirmed time, event ID, and notification status—not just `"success"`. |
| **5. Failure and recovery** | Can the agent tell what failed, what already happened, and what it can safely do next? | “Meeting updated; attendee notification failed” is very different from “Nothing changed.” |
| **6. Authority and side effects** | Are permissions enforced, consequences clear, and retries safe? | Check calendar access; prevent a retry from sending duplicate invitations. |
| **7. Evaluation** | Does this tool set improve actual task completion? | Measure wrong-tool choices, invalid arguments, unnecessary calls, and completed reschedules—not only whether each endpoint works. |

MCP directly supports parts of this through tool names and descriptions, input schemas, optional output schemas, structured results, and error reporting. The server and application must implement the underlying behavior. [MCP tools specification](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/server/tools.mdx)

**The easiest dimension to underestimate is recovery.** Bundling five operations into one tool reduces the agent’s orchestration burden, but those five operations can still fail halfway through. The tool must make that partial outcome visible.

For example, after a timeout, the agent needs to know: **“Did the meeting move, or should I retry?”** An intent-based name alone doesn’t answer that. Reliable tool design does.

### 1. Choose tools around user intent

Exposing every API endpoint without considering the agent’s tasks is an anti-pattern. An API wrapper can be a useful starting point; the problem is an uncurated interface, not the wrapper itself.
We need to move individual endpoints to intent-shaped tool sets.


Having more tools means the LLM would need to understand which to use when, and in what order. In that sense having a large set of overlapping tools makes the LLM’s job difficult.

- Ambiguous selection: Several tools appear suitable, with subtle differences buried in descriptions.
- Longer, fragile workflows: The agent must assemble many small operations; each step creates another opportunity for a mistake. We should avoid making the agent reconstruct predictable, complicated workflows dynamically in production and move such workflows to code. The agent chooses what to accomplish; code handles the predictable mechanics.
- Context cost & Attention overhead: More definitions compete with the user’s request and the evidence needed to solve it. Definitions included in a model request consume context; caching and deferred loading affect the actual cost. Keep the exposed set focused, keep results compact, and load tools on demand when the catalogue is large.

Consider the following example...

An API-shaped tool set might expose list_calendars, list_events, get_event, get_attendees, check_availability, patch_event, send_email, and dozens more. The agent must figure out which operations belong together, their order, and details such as whether changing the event already notifies attendees.

An intent-shaped tool set might expose find_meeting, find_available_times, and reschedule_meeting. These still need precise inputs and safeguards, but they put more of the workflow’s reliable mechanics into software.

**Keep judgment outside the bundled mechanics.** In the support-ticket domain, `issue_refund(ticket_id, amount)` should execute the specifically authorized refund after checking policy. It must not quietly choose a different amount, customer or ticket. The tool boundary should match a coherent user intention, with consequential choices visible before execution.

**Avoid the opposite extreme.** A giant `do_everything(action=...)` tool with unrelated modes hides different permissions, required inputs and failure semantics behind one name. Prefer separate `find_tickets`, `get_ticket` and `issue_refund` contracts. Consolidate predictable steps within one action, not all business actions into one dispatcher.

The calendar and document examples below are retained as cross-domain illustrations. The added contracts use support tickets to connect the principles to this repository.

### 2. Write clear descriptions and argument schemas

Next is **the description**, which is the most underrated part of a tool. The model normally receives the tool definition rather than its implementation. Names, descriptions and argument schemas are its primary calling interface; output schemas, annotations and previous results can provide additional information.

**Before and after.** Take a tool for searching a company's documents. These are interface sketches, not runnable implementations; the improved signature assumes imports of `Annotated` and `Literal` from `typing`, and `Field` from `pydantic`:

```python
@mcp.tool()
def search_documents(query: str, type: str = "") -> list[dict]:
    """Search documents."""
```

The model can't tell when to prefer this over other tools, what `query` should look like, or what values `type` accepts. It will guess, and some guesses will be wrong.

```python
@mcp.tool()
def search_documents(
    query: Annotated[str, Field(description="Keywords or a short phrase, e.g. 'parental leave policy'. Not a full question.")],
    doc_type: Annotated[Literal["policy", "contract", "report"] | None, Field(description="Restrict to one kind of document. Omit to search all.")] = None,
    max_results: Annotated[int, Field(description="1-10. Default 5.", ge=1, le=10)] = 5,
) -> list[dict]:
    """Find documents by keyword and return titles, ids and short excerpts.

    Use this when the user asks what the company says about a topic and you
    don't yet have a document id. Do not use it to read a document you already
    have the id for; use get_document for that. Returns at most max_results
    items, best match first, each with id, title, doc_type and a 200-character excerpt.
    """
```

**What the better version does**

1. **Says what it does and returns**, so the model knows what it will hold afterwards.
2. **Says when to use it, and when not to**, naming the neighbouring tool. This is what cuts wrong-tool calls between similar tools.
3. **Explains every argument and gives an example where useful**, so the model doesn't guess formats ("keywords, not a full question").
4. **Narrows values where possible.** `Literal[...]` expresses allowed values as an enum; `ge=1, le=10` expresses numeric bounds. These guide generation and enable validation, but do not guarantee valid model output. The server must validate every call, and valid syntax does not prove correct intent.
5. **Gives sensible defaults and marks optional arguments**, so the model doesn't invent values for things it doesn't need to set.

**Link to your code.** Your S03.02 docstrings, such as "Get the full details of the ticket by its id.", are the minimal form. They work with three distinct tools, but they would not hold up once similar tools appear. Upgrading them is a good first change in S03.04.

**Two practical points**

- Descriptions cost tokens too (the context-cost point). Be specific, not long. A short description of roughly 3–6 lines can be a useful starting point, not a rule; every sentence should prevent a particular mistake.
- You find out which sentences are needed by testing. When the eval shows the model picking the wrong tool for a question, the fix is usually one added sentence in a description ("not for X, use Y").

### 3. Design results, errors, and ambiguity handling

Next is **what the tool sends back**: its output, its errors, and what it does when the request is unclear. The model reads these results and decides its next step from them, so they should be understandable to a model while remaining structured enough for programmatic validation.

**1. Output: small, labelled, ready for the next decision**

A raw API response may contain far more than the task needs. A tool should return what the model needs to move on. Compare two results for a customer lookup:

```text
{"id": 4417, "n": "Reid", "a1": "...", "a2": "...", "c": 3, "ts": 1760860000, ...40 more fields}
```

```json
{"customer_id": "C-4417", "name": "Anna Reid", "company": "Orchard Ltd",
 "open_orders": 3, "last_contact": "2026-10-12"}
```

The second uses readable field names, only the fields that matter, and ids the model can pass to the next tool. If the result is a list, say when it's cut off (`"showing 5 of 23, narrow the search"`) so the model knows there is more.

**2. Errors: say what went wrong and what to try**

For the **2025-11-25 MCP revision**, malformed `CallToolRequest` envelopes and unknown tools are protocol errors. Tool-input validation failures (such as an out-of-range amount), API failures and business-rule failures are tool errors reported with `isError: true`. Clients should expose these results to the model so it can adjust. Distinguish the protocol contract from SDK exception handling: verify the actual result produced by the pinned FastMCP version, and expose safe, actionable messages rather than raw internal exceptions. [Error handling](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#error-handling)

- Weak: `"Error 404"`
- Better: `"No customer named 'Reed'. Closest matches: Anna Reid (C-4417), Tom Reed (C-0932). Call again with the customer_id."`

An error that includes the next step lets the model recover without guessing.

**3. Ambiguity: return the candidates and let the model or user choose**

If "Anna" matches two people, picking one silently is the worst option, because the call succeeds and the answer is wrong. Return both:

```json
{"status": "ambiguous", "matches": [
  {"customer_id": "C-4417", "name": "Anna Reid", "company": "Orchard Ltd"},
  {"customer_id": "C-0553", "name": "Anna Kaya", "company": "Fenwick plc"}],
 "hint": "Ask the user which one, or pass customer_id."}
```

**4. Schema-valid but wrong**

Some calls pass every check and are still wrong: the right type but the wrong meaning. For example, "next Friday" resolves to the wrong date, or a time is read in the wrong time zone. Nothing in the protocol flags this. The defence is to **echo your interpretation** in the result (`"interpreted as Fri 2026-10-23, Europe/London"`), so the model or the user can see and correct it. For actions with side effects, ask for confirmation first.

**Interview line:** "I design results for the model: compact and labelled, errors that say what to do next, candidates on ambiguity instead of guesses, and an echo of how I interpreted the input."

**Quick check:** a `find_tickets(customer="Smith")` call matches 40 tickets across 3 customers named Smith. In your own words, what should it return, and why not just return all 40?

**Example answer:** for `find_tickets(customer="Smith")` the tool should return a short, labelled list (the 3 Smiths with ids, plus a count or a recent few of each), not all 40 tickets. Returning everything costs context and invites misreading, and the model can ask for one customer's tickets by id next.

### 4. Enforce authority and make retries safe

This connects tool design to [S03.03’s authentication and authorization work](../S03.03-MCP-OAuth2.1/README.md): verify the access token, require the scope for the specific tool, and enforce team ownership, amount limits and available balance in server code. A tool description or hidden UI control is not an access-control boundary. Tool filters reduce what reaches the model; callers still need authorization when they invoke the server directly.

Bind confirmation to the exact ticket, amount, currency and action. A changed request needs a new decision; approval does not override policy. Recheck relevant state after confirmation because balances and credentials can change while the user considers the request.

**MCP annotations describe behavior; they do not implement it.** `readOnlyHint` describes whether a tool changes state, `destructiveHint` describes potentially destructive updates, and `idempotentHint` describes repeat-call behavior with the same arguments. `openWorldHint` describes interaction with an open rather than closed world. Treat these as metadata, not authorization or transactional guarantees; clients must treat annotations as untrusted unless they come from trusted servers. See the [versioned annotation definitions](https://modelcontextprotocol.io/specification/2025-11-25/schema#toolannotations).

**A retry contract needs stored state.** For a future consequential refund tool, accept a stable operation/idempotency key for one authorized intent. Store it durably with the caller or tenant, normalized arguments, execution state and result. Reusing the key with the same intent returns the recorded result; reusing it with different arguments is rejected. Coordinate concurrent duplicates atomically. Document the retention window. Deduplicate the downstream payment operation too: a local record alone cannot close the crash window between an external payment and recording its result.

This is a proposed design, **not a claim about the existing demo**. S03.03 currently uses a process-local simulated ledger that resets on restart; it is not a durable payment or idempotency implementation.

**Worked partial-failure example (proposed contract).** A refund is recorded but its notification fails. The result must distinguish those outcomes and name the safe recovery action:

```json
{
  "status": "partial_success",
  "operation_id": "OP-204",
  "ticket_id": "T-1003",
  "refund": {"status": "recorded", "refund_id": "RF-204", "amount": "25.00", "currency": "GBP"},
  "notification": {"status": "failed", "error_code": "temporary_unavailable"},
  "recovery": {
    "action": "retry_notification",
    "operation_id": "OP-204",
    "safe_to_repeat_refund": false
  }
}
```

The recovery action retries only the notification and must deduplicate delivery attempts. It must not issue another refund. A successful state change is not undone merely because the overall result is an error. Make partial outcomes visible in structured data and the human-readable summary, including when `isError` is true.

**A timeout is an unknown outcome, not evidence of failure.** If the client receives no result, it should query operation status or retry the same idempotency key under the documented contract. It must not generate a fresh key and blindly repeat the action. A response saying `retry_safe: true` is insufficient unless it identifies what can safely be retried and why.

### 5. Make the MCP result contract explicit

These wire-level notes target **MCP 2025-11-25**, matching the specification cited in this chapter. SDK behavior must be checked against the pinned version; these examples are proposed contracts, not implemented S03.04 tools.

- `outputSchema` defines a result contract; `structuredContent` carries its JSON object. Text inside `content` remains useful for explanation and compatibility. Validate result shape, and include a serialized text representation for older clients.
- A resource link can point to a large export instead of embedding it. Ensure the client can retrieve it with appropriate authorization; do not expose credentials or assume an inaccessible local path will work.
- MCP cursor pagination for `tools/list` paginates **tool definitions**. A `find_tickets` result needs its own documented page size, continuation token and truncation behavior.

Sources: [structured results and output schemas](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#structured-content), [resource links](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#resource-links), [listing tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools#listing-tools).

For example, this application result tells the caller that the ticket list is incomplete:

```json
{
  "customer_id": "C-4417",
  "tickets": [{"ticket_id": "T-1003", "status": "open", "summary": "Refund request"}],
  "returned_count": 1,
  "total_count": 23,
  "truncated": true,
  "next_cursor": "opaque-continuation-token"
}
```

Document a stable ordering and bind the cursor to the original filter and authorization context. If computing a total is expensive or unavailable, omit it rather than inventing one. The output schema should define required fields and permitted outcome variants, including ambiguity and partial completion. Schema validation checks shape; it cannot establish that the right customer was selected or that a refund actually happened.

### 6. Evaluate the tool design

Now the last piece of S03.04: **the eval, which is how you prove the design is better instead of asserting it.**

**Why it exists.** "Fewer, better tools work better" is a claim. Tool-count advice such as "12–20 tools" is an illustrative rule of thumb here, not a sourced recommendation or universal target; the useful set depends on the tasks and model. The eval is the evidence.

**The setup**

- **Three versions of the same server.** A: raw endpoint-shaped tools (say 40), B: those same tools with improved descriptions, and C: a curated set (say 8) with comparably clear descriptions. A versus B tests wording; B versus C tests the additional effect of consolidation. Keep backend behavior, data, permissions, prompts, model settings and budgets comparable. If schemas or output formats also change, report that as a bundled redesign rather than claiming to isolate tool count.
- **About 20 realistic questions.** Mix the types: simple one-step lookups, multi-step tasks, deliberately ambiguous ones ("Smith"), ones where the data doesn't exist, and traps that exploit near-duplicate tools.
- **A known right answer for each.** Record acceptable tools or tool sequences, the expected final answer, and required final state. Allow equivalent valid paths instead of requiring one exact trace.
- **Two model families.** A design that only works on one model is fragile. Running two tests whether the gain appears across those models; it does not establish universal generality.
- **Repeat each run several times.** Model output is nondeterministic, so one run proves little.

**Hold out cases and define scoring.** Use development questions to improve descriptions and keep separate, unseen questions for the final comparison. Twenty questions is an exploratory set, not a reliable population estimate. Report counts with percentages (for example, 17/20), per-case variation and repeat counts. Repeats of one question do not create new independent tasks. Pin model versions and report sampling settings and execution budgets.

Use deterministic checks for valid arguments, authorized actions, final backend state, duplicate effects and required confirmations. Use a model judge only where answer quality needs semantic assessment; give it a fixed rubric and calibrate a sample against human judgments. Do not let the judge substitute for checking whether the operation actually happened. Keep the model judge independent of which variant produced the answer where practical.

**What you measure**

| Metric | What it reveals |
|---|---|
| Task success rate | Did it reach the right answer? |
| Wrong-tool rate | The selection problem |
| Invalid or wrong arguments | The description and schema problem |
| Calls per task | Planning efficiency, compared at similar correctness and safety |
| Tokens per task | The context-cost problem |

Define wrong-tool rate as incorrect selections divided by tool calls, and also report tasks containing at least one wrong selection. Separate malformed arguments from schema-valid but semantically wrong arguments. Report latency and unauthorized or duplicate side effects alongside the five core metrics. Lower token or call counts are not improvements if they come from skipped confirmations or incomplete work.

Read the tool-call trace, not only the final answer. A model can reach the right answer by a wasteful or lucky path, and the trace is where the design differences show.

**What the result looks like.** A small table with three server variants by two models by the five metrics. Treat improvement in wrong-tool rate, calls and tokens as a hypothesis, not an expected verdict. Report honestly if it doesn't: with few tools or a strong model the gap can be small, and that finding is still useful, since it tells you where the ceiling sits for your case.

**Use it as a loop.** When a question fails, look at the trace and fix the cause: a vague description, a missing "not for X" sentence, an ambiguous output. Then rerun. Most of the improvement in tool design comes from this loop.

**Interview line:** "I don't trust tool design by taste. I build a small eval of realistic questions, compare raw tools, description-improved tools, and curated tools on two models, and compare success, wrong-tool rate, calls and tokens from the traces."

### 7. Apply the design on managed platforms

| Platform | Practical mapping | Design responsibility |
|---|---|---|
| Azure API Management | Expose selected operations from a managed REST API as MCP tools. | Select useful operations and improve contracts; enforce policy behind the interface. |
| Amazon Bedrock AgentCore Gateway | Create MCP access to targets described by OpenAPI or tool schemas. | Curate exposed capabilities and define safe behavior in the backend. |
| Microsoft Foundry | Use the MCP integration’s `allowed_tools` configuration where supported by the selected API/SDK. | Limit the model’s available catalogue; do not treat this as server-side authorization. |
| OpenAI Agents SDK | Use `tool_filter`, including `create_static_tool_filter(allowed_tool_names=[...])`. | Expose a task-appropriate subset while retaining backend access controls. |

A generated wrapper is a valid integration starting point. Evaluate whether it already fits the task before adding an orchestration layer. If it exposes too many overlapping operations, curate the catalogue or introduce coherent workflow tools. Filtering reduces selection burden but does not implement transactional recovery.

Platform references: [Azure API Management](https://learn.microsoft.com/en-us/azure/api-management/export-rest-mcp-server), [AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building.html), [Foundry MCP configuration](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol?view=foundry-classic), [Agents SDK filtering](https://openai.github.io/openai-agents-python/mcp/). Check the selected platform API version before copying configuration names.

## S03.04 in five lines

1. Tools are for a model, not a programmer, so don't just wrap the API.
2. One tool per task a person would name; fixed steps go inside it.
3. The description is the interface.
4. Results and errors are written for the model: compact, with candidates and next steps.
5. Prove it with an eval.

**Next: design exercise.** Pick a system you know, list its raw endpoints, then redesign into intent tools and write one full description.

## Further reading

- [MCP tools specification, 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/server/tools): the protocol contract used here.
- [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents): practical design and evaluation guidance, rather than a mandatory tool-count rule.

The worked examples and evaluation design above are teaching proposals. No comparison results or production guarantees are claimed for S03.04.
