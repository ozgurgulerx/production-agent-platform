# Foundry IQ as a Copilot Studio tool (shape, not a script)

There is no public REST or `pac` surface for adding a Foundry IQ tool on 25 Oct 2026; it is a portal action in the GitHub Copilot harness (J3). The shape below is what the portal asks for, written as YAML so the fields can be compared with the F08 connection and the B08 gateway target. Treat the key names as documentation, not as a file the platform reads.

```yaml
# verify: portal fields as of 2026-10-23 (J3); not an importable schema
tool:
  kind: foundry-iq-knowledge-base # one per agent
  display_name: Ticket policies (Foundry IQ)
  description: UK card team refund, card and escalation policies, effective 1 Jul 2026. Use for any policy question.
  knowledge_base:
    foundry_project_endpoint: https://<resource>.services.ai.azure.com/api/projects/<project>
    name: kb-ticket-policies # built by F08 lab 01
  authentication:
    mode: entra-signed-in-user # alternatives: api-key | service-principal | certificate (J3)
    # api-key and service-principal store the secret in the connection, not in the agent definition
  tuning: in Foundry, not here # retrievalReasoningEffort, outputMode, sources (F08 §3)
  trace: activity trace shows each retrieval and its citations
```

## Side by side

| Field                     | Copilot Studio tool (C08)                   | Foundry agent connection (F08)                                                            | AgentCore gateway target (B08)         |
| ------------------------- | ------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------- |
| Where the index lives     | Foundry IQ (Azure AI Search)                | Foundry IQ                                                                                | Bedrock Managed KB                     |
| Identity used to retrieve | signed-in user, API key, SPN or certificate | project managed identity (`ProjectManagedIdentity`, audience `https://search.azure.com/`) | gateway IAM role                       |
| Per-user trimming         | with Entra signed-in mode                   | `x-ms-query-source-authorization`                                                         | `userContext.userId` / JWT passthrough |
| Allowed operations        | retrieve only                               | `allowed_tools: ["knowledge_base_retrieve"]`                                              | `Retrieve`, `AgenticRetrieveStream`    |
| Reasoning depth           | set in Foundry (`retrievalReasoningEffort`) | same                                                                                      | `maxAgentIteration`                    |
| Governance point          | tool DLP/ACP (D3), Agent 365 trace          | APIM / Entra roles                                                                        | Cedar policy on the gateway            |

## What to say when asked "why not just upload the files?"

Three platforms, three indexes, three permission models, three ALM stories. One Foundry IQ knowledge base is tuned once, billed once, and each platform gets a tool whose only job is to call it with the right identity.
