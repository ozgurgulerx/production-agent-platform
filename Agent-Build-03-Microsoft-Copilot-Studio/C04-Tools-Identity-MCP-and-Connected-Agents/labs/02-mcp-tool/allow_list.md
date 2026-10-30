# The per-tool allow-list (reading map D4)

1. Open the `tickets-none` MCP tool in the agent. "Allow all" is a single toggle; switch it **off**. Each of the four tools now has its own toggle, and tools the server adds later arrive **off**.
2. Leave `get_ticket`, `list_tickets`, `get_policy` on; turn `issue_refund` **off**. Save, publish.
3. Test: "Refund ticket 1042 forty pounds". Expected: the agent explains it cannot issue refunds; the activity map shows no `issue_refund` call and no plan step for it.
4. Turn `issue_refund` on. Save, publish. Same question: `issue_refund` returns `REFUNDED`; "Refund 400 pounds" returns `ESCALATE`.
5. Count: with "Allow all" on against a server that exposes 130 tools the agent exceeds **128** (D1); the wizard warns and the planner degrades. Keep servers small or split into child agents, each with its own 128.

Record the two transcripts side by side; that pair is the proof that tool exposure is a maker control, independent of instructions.
