# F06 capability builds — MCP, tools and durable integration

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Toolbox and MCP consumption

- [ ] Build: Create a toolbox with a controlled MCP endpoint and attach it to a test agent. Compare the user-curated toolbox with the Microsoft Foundry MCP Server for platform operations. Configure approvals and explicit degraded behavior.
- [ ] Verify: Test denied approval, unavailable server and malicious tool-result text; inspect whether any side effect occurred rather than only the final response.

### MCP server authorization

- [ ] Build: Write a small MCP service with schema-bound tools/resources/prompts and supported HTTP transport. Validate resource audience and tool authorization using maintained auth components; evaluate API Center/APIM and Functions/Container Apps hosting.
- [ ] Verify: Show unauthenticated, wrong-audience, insufficient-scope and allowed calls; no bearer-token forwarding to an unrelated downstream resource. Reuse F03 identity design.

### Durable business action

- [ ] Build: Implement one Service Bus or event-driven tool path with correlation, stable idempotency key, operation ledger and a durable human-approval step. Bind approval to actor/action/arguments/expiry.
- [ ] Verify: Replay duplicates concurrently; interrupt after side effect before acknowledgment; test expired approval, timeout and poison messages. Demonstrate one recorded effect and a reconciliation path for unknown outcomes.

### Integration boundaries

- [ ] Build: Compare queue vs event vs synchronous REST, A2A cards/handoff, OpenAPI contracts and enterprise connectors. Choose one bounded Logic Apps/Functions/Graph/enterprise API boundary for the scenario.
- [ ] Verify: Test schema mismatch, downstream throttling and partial failure. Record retry ownership, compensation and which side validates authorization.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB081** — Foundry Toolbox - Microsoft's managed way to assemble an MCP tool server [link](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/toolbox-overview)
- [ ] **CB082** — Foundry MCP Server - agents to use Foundry services
- [ ] **CB083** — Connect an external MCP server, e.g. Microsoft Learn.
- [ ] **CB084** — Configure MCP tool approvals; handle approval requests.
- [ ] **CB085** — Handle unavailable optional MCP tools with explicit degraded behavior.
- [ ] **CB086** — Validate MCP tool safety controls beyond model content filters.
- [ ] **CB087** — Hosting MCP servers (Container Apps, Functions remote MCP), API Center as MCP registry, APIM in front of MCP (auth, rate limit), Foundry Agent Service MCP tool, Copilot Studio MCP connectors; auth per S27; tool design quality (S03.04).
- [ ] **CB088** — `FastMCP` server with tools/resources/prompts, streamable HTTP transport, OAuth 2.1 with Entra as authorisation server (protected resource metadata, audience/scope validation, no passthrough), hosting on Container Apps or Functions remote MCP, registering in API Center, fronting with APIM; MCP client from Agent Framework and Foundry Agent Service. Carries your S03.03 / S27 work.
- [ ] **CB089** — Azure Functions remote MCP and Logic Apps agent loops — awareness of the no-code/low-code agent surfaces clients will ask about.
- [ ] **CB109** — MCP server auth on Azure: Entra as authorisation server, protected-resource metadata, scopes per tool, audience validation, no token passthrough (ties to S03.03 / S27).
- [ ] **CB115** — MCP server auth on Azure: Entra as authorisation server, protected-resource metadata, scopes per tool, audience validation, no token passthrough (ties to S03.03 / S27).
- [ ] **CB179** — Service Bus / Event Grid for async tool execution,
- [ ] **CB180** — Azure Functions / Durable Functions for long-running or human-approval steps,
- [ ] **CB186** — Service Bus (queues, topics, sessions, dead-letter, scheduled messages) vs Event Grid (push, event-driven fan-out, CloudEvents) vs Event Hubs (streaming); when each.
- [ ] **CB187** — Async tool execution: request/response over queues, correlation IDs, outbox pattern, idempotency keys, exactly-once myths, saga / compensation for multi-step agent actions, human-approval step as a durable wait (Durable Functions, Logic Apps), replay and poison handling.
- [ ] **CB188** — API design: APIM products/subscriptions, versioning, OpenAPI as tool schema, backend pools, policy expressions, GraphQL where relevant.
- [ ] **CB189** — Enterprise integration: Logic Apps connectors, Dataverse, SAP (OData / BTP), ServiceNow, Salesforce; Microsoft Graph for M365 data (Access Computer Consulting ad).
- [ ] **CB194** — Temporal / Durable Functions / Logic Apps for long-running agent workflows (Uniting People ad names Temporal).
- [ ] **CB195** — Service Bus sender/receiver, sessions, dead-letter handling, peek-lock and completion, scheduled messages; Event Grid publish/subscribe with CloudEvents; Azure Functions Python v2 model with triggers (HTTP, Service Bus, timer), Durable Functions orchestrations with `wait_for_external_event` for human approval. This is the event-driven answer Cognizant asks for, in code.
- [ ] **CB196** — Exercise: tool execution over Service Bus with idempotency key in Cosmos and a Durable Functions approval step.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
