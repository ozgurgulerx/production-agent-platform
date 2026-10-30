# Three KQL queries over the environment-level export (reading map H2)

Spans land in the App Insights `dependencies` table following the OpenTelemetry GenAI semantic conventions. Names: `InvokeAgent`, `ExecuteTool`, `OutputMessages`. Attributes sit in `customDimensions`.

## 1. Tool calls by name and outcome, last 24 h
```kusto
dependencies
| where timestamp > ago(24h)
| where name == "ExecuteTool"
| extend tool = tostring(customDimensions["gen_ai.tool.name"]),
         ok   = success
| summarize calls = count(), failures = countif(ok == false) by tool
| order by calls desc
```

## 2. Every refund the agent attempted, with the amount it passed
```kusto
dependencies
| where name == "ExecuteTool"
| extend tool = tostring(customDimensions["gen_ai.tool.name"]),
         args = tostring(customDimensions["gen_ai.tool.call.arguments"])
| where tool == "issue_refund"
| extend amount = todouble(parse_json(args)["amount_gbp"])
| project timestamp, amount, conversation = tostring(customDimensions["gen_ai.conversation.id"]), result = tostring(customDimensions["gen_ai.tool.call.result"])
| order by amount desc
```
Any row above 250 is a policy breach the webhook (C05 §7) should have blocked.

## 3. One conversation end to end
```kusto
let conv = "<gen_ai.conversation.id>";
dependencies
| where tostring(customDimensions["gen_ai.conversation.id"]) == conv
| project timestamp, name, duration, model = tostring(customDimensions["gen_ai.request.model"]),
          tool = tostring(customDimensions["gen_ai.tool.name"]), operation_Id, id, operation_ParentId
| order by timestamp asc
```
Attribute names are the OTel GenAI ones quoted on the Learn page; the harness adds its own prefix for some (`# verify` the exact keys in your workspace with `dependencies | take 1 | project customDimensions`).
