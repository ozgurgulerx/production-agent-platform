# MCP Tool Design 

“How would you expose our systems to an agent?” is one of the most common architect questions. The weak answer is “wrap the APIs as tools”. The strong answer is “I’d start from what the agent needs to get done, build a small set of **intent-level tools** with precise descriptions, keep the deterministic logic in code, and measure wrong-tool rate before adding more.” Each clause of that answer maps to one of the four decisions above.

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

Exposing each API endpoint as an MCP tool is an anti-pattern. 
We need to move individual endpoints to intent-shaped tool sets.


Having more agents means the LLM would need to understand which to use when, and in what order. In that sense having a large set of tool makes LLMs job difficult. 

- Ambiguous selection: Several tools appear suitable, with subtle differences buried in descriptions.
- Longer, fragile workflows: The agent must assemble many small operations; each step creates another opportunity for a mistake. We should avoid making the agent reconstruct predictable, complicated workflows dynamically in production and move such workflows to code. The agent chooses what to accomplish; code handles the predictable mechanics.
- Context cost & Attention overhead: More definitions compete with the user’s request and the evidence needed to solve it. Every tool definition is paid for on every turn in both tokens and attention, so I keep the set small, keep results compact, and load tools on demand if the catalogue has to be large.”

Consider the following example...

An API-shaped tool set might expose list_calendars, list_events, get_event, get_attendees, check_availability, patch_event, send_email, and dozens more. The agent must figure out which operations belong together, their order, and details such as whether changing the event already notifies attendees.

An intent-shaped tool set might expose find_meeting, find_available_times, and reschedule_meeting. These still need precise inputs and safeguards, but they put more of the workflow’s reliable mechanics into software.

### 2. Write clear descriptions and argument schemas

Next is **the description**, which is the most underrated part of a tool. The model never sees your code. The name, the description and the argument schema are the only thing it knows about the tool, so they are the tool's real interface.

**Before and after.** Take a tool for searching a company's documents:

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
3. **Explains every argument with an example**, so the model doesn't guess formats ("keywords, not a full question").
4. **Narrows values where possible.** `Literal[...]` becomes an enum in the schema, so the model can only pick valid values. Limits like `ge=1, le=10` do the same for numbers.
5. **Gives sensible defaults and marks optional arguments**, so the model doesn't invent values for things it doesn't need to set.

**Link to your code.** Your S03.02 docstrings, such as "Get the full details of the ticket by its id.", are the minimal form. They work with three distinct tools, but they would not hold up once similar tools appear. Upgrading them is a good first change in S03.04.

**Two practical points**

- Descriptions cost tokens too (the context-cost point). Be specific, not long. A good description is 3–6 lines, and every sentence should prevent a particular mistake.
- You find out which sentences are needed by testing. When the eval shows the model picking the wrong tool for a question, the fix is usually one added sentence in a description ("not for X, use Y").

### 3. Design results, errors, and ambiguity handling

Next is **what the tool sends back**: its output, its errors, and what it does when the request is unclear. The model reads these results and decides its next step from them, so they are written for a model, not for a program.

**1. Output: small, labelled, ready for the next decision**

An API returns everything it has. A tool returns what the model needs to move on. Compare two results for a customer lookup:

```text
{"id": 4417, "n": "Reid", "a1": "...", "a2": "...", "c": 3, "ts": 1760860000, ...40 more fields}
```

```json
{"customer_id": "C-4417", "name": "Anna Reid", "company": "Orchard Ltd",
 "open_orders": 3, "last_contact": "2026-10-12"}
```

The second uses readable field names, only the fields that matter, and ids the model can pass to the next tool. If the result is a list, say when it's cut off (`"showing 5 of 23, narrow the search"`) so the model knows there is more.

**2. Errors: say what went wrong and what to try**

MCP separates two kinds of error. A malformed request is a protocol error. A tool that ran but couldn't do the job returns a normal result with `isError: true`, and the model sees this and can adjust. In FastMCP, an exception raised inside a tool is reported this way. So write the message for the model:

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

### 4. Evaluate the tool design

Now the last piece of S03.04: **the eval, which is how you prove the design is better instead of asserting it.**

**Why it exists.** "Fewer, better tools work better" is a claim. Tool-count advice like "12–20 tools" is a heuristic, not a law, and it depends on your domain and your model. The eval is the evidence.

**The setup**

- **Two versions of the same server.** One with the raw, endpoint-shaped tools (say 40) and one with the curated set (say 8). The backend and the data are identical. Only the tool surface differs, so any difference in results comes from the design.
- **About 20 realistic questions.** Mix the types: simple one-step lookups, multi-step tasks, deliberately ambiguous ones ("Smith"), ones where the data doesn't exist, and traps that exploit near-duplicate tools.
- **A known right answer for each.** Record the expected tool or tool sequence and the expected final answer.
- **Two model families.** A design that only works on one model is fragile. Running two shows whether the gain is general.
- **Repeat each run several times.** Model output is nondeterministic, so one run proves little.

**What you measure**

| Metric | What it reveals |
|---|---|
| Task success rate | Did it reach the right answer? |
| Wrong-tool rate | The selection problem |
| Invalid or wrong arguments | The description and schema problem |
| Calls per task | The planning problem (fewer is better) |
| Tokens per task | The context-cost problem |

Read the tool-call trace, not only the final answer. A model can reach the right answer by a wasteful or lucky path, and the trace is where the design differences show.

**What the result looks like.** A small table with two servers by two models by the five metrics. Expect the curated server to win on wrong-tool rate, calls and tokens. Report honestly if it doesn't: with few tools or a strong model the gap can be small, and that finding is still useful, since it tells you where the ceiling sits for your case.

**Use it as a loop.** When a question fails, look at the trace and fix the cause: a vague description, a missing "not for X" sentence, an ambiguous output. Then rerun. Most of the improvement in tool design comes from this loop.

**Interview line:** "I don't trust tool design by taste. I build a small eval of realistic questions, run the endpoint-shaped and the curated server on two models, and compare success, wrong-tool rate, calls and tokens from the traces."

## S03.04 in five lines

1. Tools are for a model, not a programmer, so don't just wrap the API.
2. One tool per task a person would name; fixed steps go inside it.
3. The description is the interface.
4. Results and errors are written for the model: compact, with candidates and next steps.
5. Prove it with an eval.

**Next: design exercise.** Pick a system you know, list its raw endpoints, then redesign into intent tools and write one full description.
