# Appendix — the Foundry declarative workflow (preview, retiring 1 December 2026)

`deploy_workflow.py` is the 2025 version of this demo: a `kind: workflow` YAML with `InvokeAzureAgent` steps deployed as a `WorkflowAgentDefinition`. Microsoft Learn (`agents/concepts/workflow`, updated 2026-10-19): *"Microsoft Foundry is retiring workflows on December 1, 2026. If you're looking to build new workflows, use Microsoft Agent Framework."* After that date the designer and in-portal runs stop; existing YAML keeps running only when deployed as a hosted agent.

Keep it for two reasons: it is the fastest way to show a reviewer what "declarative multi-agent" looked like, and the migration guidance is literally this folder: export the YAML (designer → YAML view), then rebuild the graph with `WorkflowBuilder` as `../src/ticket-workflow/main.py` does. Do not deploy it in new projects.
