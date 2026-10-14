# R1 — Ticket functions as MCP tools (Day 1)

**FastMCP** is the server-building interface we use from the MCP Python SDK
(`mcp.server.fastmcp`). It exposes Python functions as tools through the Model
Context Protocol (MCP). The `@mcp.tool()` decorator registers a function, while
its type hints and docstring describe the tool's inputs, output, and purpose.
FastMCP handles MCP requests and responses; our functions still do the actual
work. It does not choose which tool to call—the client, or an AI model through
the client, makes that choice.

### What our FastMCP server actually does

Our server is a running Python process that lets an MCP client use our ticket
functions. In this project, it communicates over **stdio**: the client sends
protocol messages through the process's standard input and reads responses from
its standard output. We do not need to expose an HTTP endpoint for this setup.

1. **Advertises tools.** When the client asks for the tool list, the server returns
   the names, descriptions, and input schemas of our three registered tools.
2. **Receives a tool call.** For example, Inspector requests `get_ticket` with
   `{"ticket_id": "T-1001"}`. This is a structured request, not natural language.
3. **Validates and dispatches.** FastMCP checks the arguments against the tool's
   declared input types and calls the registered wrapper in `server.py`.
4. **Runs our existing logic.** The wrapper calls `functions.get_ticket("T-1001")`,
   which reads the JSON fixture and returns the matching ticket or a `not_found`
   dictionary.
5. **Returns an MCP response.** FastMCP packages the Python result into a protocol
   response and sends it back to the client.

```text
Inspector or an agent application's MCP client
    → get_ticket request with ticket_id="T-1001"
    → FastMCP tool wrapper in server.py
    → lookup logic in functions.py
    → result packaged as an MCP response
    → client receives the ticket or not_found result
```

The server does not interpret a user's question or decide whether a refund should
be issued. It exposes the operations we registered and executes the requested
one. With Inspector, we choose the call manually; with an agent, the model can
choose it and the agent application sends it through the MCP client.

From this folder, activate the shared root environment with `source ../.venv/bin/activate`. Run tests with `python -m pytest --cov=src --cov-report=term-missing --cov-fail-under=80`. See the root README for dependency installation.


We will now be exposing python functions as mcp tools via an mcp server.
The larger task is (imaginary scenario) building an ops agent for a financial company and initially will be focusing on the "refunds agent."

- [ ] write the functions as per their specs below
- [ ] test the functions with pytest 
- [ ] expose the functions with FastMCP as tools
- [ ] Use MCP Inspector to test the server



### What functions we will build...
**list_tickets** — the agent’s way to find tickets without knowing an id. Takes optional filters (status, customer, maybe a tag) and returns a compact list: id, subject, status, customer, created date — enough to pick one, not the whole record, because the model will read every returned token. An empty match returns an empty list, not an error.

**get_ticket** — one ticket in full by id: the summary fields plus the refund-relevant ones (amount disputed, refund status, which policy it references). An unknown id comes back as a clean “not found” error the model can act on, never a raised exception that kills the run. Customer card and NI fields are either absent from the data this tool reads or stripped here, so no later stage can leak them.

**get_policy** — one policy document by id, returned as text with its id and title, so the agent can quote it when it answers “which policy applies”. Unknown id → the same clean error shape as get_ticket.

Ok, once done - test the functions with tests/test_functions.py

### Testing stages

| Test level | Question it answers | How we will test |
| --- | --- | --- |
| 1. Python function tests (`functions.py`) | Does the ticket and policy lookup logic work? | Use `pytest` in `tests/test_functions.py` to call the functions directly and assert their results, including filters and missing IDs. |
| 2. Automated MCP server tests (`server.py`) | Does the server expose the right tools and execute calls correctly through MCP? | Use `pytest` in `tests/test_mcp_server.py` with an initialized MCP client session to check tool names, descriptions, input schemas, and calls to each tool. |
| 3. Manual MCP Inspector tests | Can we discover and call the tools through an interactive client? | Use Inspector to select tools, enter arguments, inspect returned results, and capture screenshots. |
| 4. LLM agent tests | Does the model choose the right tool and use its result correctly? | Use the OpenAI Agents SDK to connect an agent to our MCP server, give it natural-language tasks, and check its tool choices, arguments, and final answers. |

Stages 2 and 3 both test the MCP interface: pytest automates the checks, while
Inspector lets us perform them manually. Neither requires an LLM. The automated
server tests complement the function tests by checking the MCP connection and
tool definitions as well as the returned data.

#### LLM agent tests

**Build brief:** Write a simple local Python agent using the OpenAI Agents SDK.
The agent script and MCP server run on our machine; the language model runs
through the OpenAI API. Start with one question per run and display the final
answer in the terminal.

The agent should:

1. Read its API key from the environment, keeping it out of source code.
2. Connect to our existing MCP server over stdio, launching it from the R1 folder
   so its relative data paths work.
3. Make the server's three tools available to the model and instruct it to use
   them for ticket and policy facts, and report missing records honestly.
4. Accept a question, let the model choose and call the appropriate tool, and
   display the answer. Make the tool name, arguments, and returned result
   inspectable so we can check what happened.
5. Close the MCP connection when the run finishes.

**First checkpoint:** Ask “What is the status of ticket T-1001?” and observe a
`get_ticket` call followed by an answer grounded in its result. This first run is
a manual agent check; automated agent tests can follow once the connection works.

These tests check whether a model can use our tools to answer a user's question.
We will connect an agent built with the OpenAI Agents SDK to our MCP server over
stdio. Unlike Inspector and the automated MCP tests, the model chooses the tool
and its arguments from a natural-language task.

For example, ask: **“What is the status of ticket T-1001?”** Check that the agent
calls `get_ticket` with `ticket_id="T-1001"`, receives the ticket, and answers that
its status is **open**. Check the tool call as well as the final answer: a correct
answer alone could be a guess. The wording can vary, but the facts must match
the returned data.

Follow-up cases should ask for open tickets, request a policy, and reference an
unknown ticket. Check the selected tool, arguments, and whether the answer stays
grounded in the result, including reporting missing records without inventing them.
The basic agent is implemented in `src/llm_agent.py` and has completed one live
run. Automated agent tests and the follow-up cases above are still planned.
Live runs require an OpenAI API key and incur model usage costs.

#### Running the agent and reading server logs

From the R1 folder, with `OPENAI_API_KEY` exported, run:

```bash
../.venv/bin/python src/llm_agent.py
```

The script currently asks one fixed question: “What is the status of ticket
T-1001?” In the verified live run, the server logged these request types in order
(timestamps and file locations omitted here):

```text
INFO Processing request of type ListToolsRequest
INFO Processing request of type CallToolRequest
INFO Processing request of type ListToolsRequest
Ticket T-1001 is **open**.
```

**Server logs** are diagnostic messages written by the MCP server while it runs.
They describe activity; they are separate from the model's final answer.

| Output | Meaning |
| --- | --- |
| `INFO` | An informational message, not an error. |
| `ListToolsRequest` | The client asked which tools the server provides. This may happen more than once during a run. |
| `CallToolRequest` | The client requested execution of a tool. |
| `Ticket T-1001 is **open**.` | The agent's final answer, printed by `llm_agent.py`. |

With stdio transport, the server uses standard output for MCP protocol messages
and sends these logs to standard error. The terminal can display both streams.
Do not add ordinary `print()` debugging to `server.py`'s protocol output.

This run exited successfully and confirms that a tool call occurred and the
agent returned the correct ticket status. These basic logs do not show the tool
name, arguments, or returned data; inspecting those details is still needed to
verify the exact call rather than infer it from the answer.

====

### Test the server with MCP Inspector

MCP Inspector is a client for manually testing your MCP server. You select a tool
and supply its arguments; no AI model is involved. Inspector sends the request
through MCP, your server calls the Python function, and Inspector displays the result.

From the `r1-functions-to-mcp-tools` folder, launch Inspector with:

```bash
npx @modelcontextprotocol/inspector ../.venv/bin/python src/server.py
```

Keep that terminal running while testing. In the browser interface, connect to the
server if necessary and select **Tools**.

![MCP Inspector showing the three registered tools and the get_policy input form](docs/evidence/screenshots/mcp-inspector-tools.png)

The screenshot shows tool discovery: all three tools are listed, the selected
tool's docstring appears as its description, and its parameter becomes an input
field. It does not yet show a completed tool call.

#### Run the manual tests

Select a tool on the left, enter the inputs below, then click **Execute Tool**.
Compare the returned data with the expected result; a connected indicator alone
does not prove a tool works.

| Test | Tool | Inputs | Expected result |
| --- | --- | --- | --- |
| Existing ticket | `get_ticket` | `ticket_id`: `T-1001` | Ticket with ID `T-1001` and subject `Card declined twice` |
| Unknown ticket | `get_ticket` | `ticket_id`: `DOES-NOT-EXIST` | `{"error": "not_found", "id": "DOES-NOT-EXIST"}` |
| All tickets | `list_tickets` | Omit both filters | Eight ticket summaries |
| Open tickets | `list_tickets` | `status`: `open`; omit `customer_id` | Four tickets: `T-1001`, `T-1003`, `T-1006`, `T-1008` |
| Both filters | `list_tickets` | `status`: `open`; `customer_id`: `C-42` | Three tickets: `T-1001`, `T-1003`, `T-1008` |
| No matching tickets | `list_tickets` | `customer_id`: `DOES-NOT-EXIST`; omit `status` | An empty list |
| Existing policy | `get_policy` | `policy_id`: `POL-REFUND-01` | Policy titled `Refund window`, with its ID and text |
| Unknown policy | `get_policy` | `policy_id`: `DOES-NOT-EXIST` | `{"error": "not_found", "id": "DOES-NOT-EXIST"}` |

These expected results refer to the current JSON fixtures in `data/`.
For optional filters, omit the argument rather than sending an empty string.
If the form makes this unclear, enable **Edit as JSON** and use `{}` for all
tickets, or `{"status": "open"}` for open tickets.

The missing-ID result is an expected application response. The current functions
return an error dictionary normally, so Inspector may show a successful MCP call
alongside `"error": "not_found"`. Check the returned data, not just the success label.

If the tool list is blank or a request times out, the test has not passed. Try
disconnecting and reconnecting, and inspect the **Protocol** and **Console** panels
plus the launching terminal for errors.

After running the existing-ticket and unknown-ticket tests, save a screenshot of
each result under `docs/evidence/screenshots/`. These demonstrate tool execution;
the screenshot above demonstrates discovery. Stop Inspector with **Ctrl-C** in
the launching terminal when finished.

#### Captured test results

Existing ticket: `get_ticket` with `ticket_id="T-1001"` returns the ticket details.

![Inspector returning ticket T-1001](docs/evidence/screenshots/mcp-ticket-found.png)

Unknown ticket: `get_ticket` with `ticket_id="DOES-NOT-EXIST"` returns the expected
`not_found` dictionary.

![Inspector returning not_found for an unknown ticket](docs/evidence/screenshots/mcp-ticket-not-found.png)
