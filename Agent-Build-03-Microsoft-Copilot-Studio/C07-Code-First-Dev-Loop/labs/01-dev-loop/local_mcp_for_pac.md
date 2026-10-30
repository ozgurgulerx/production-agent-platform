# pac as a local MCP server for coding agents

`pac copilot mcp --run` starts a local MCP server that exposes pac copilot commands as tools (C1; transport and port not stated on the reference page, `# verify`).

1. In one terminal: `pac copilot mcp --run`.
2. Register it in your coding agent's MCP config (Claude Code: `claude mcp add pac-copilot -- pac copilot mcp --run`; VS Code / GitHub Copilot: `.vscode/mcp.json` with the same command). `# verify` the exact invocation against the pac output.
3. Ask the coding agent: "pull the latest changes for ticket-agent and list the topics that changed". Watch it call the pull tool and read the diff.
4. Do **not** give this profile publish rights on test or prod. `pac auth create --deviceCode --name dev-only` scoped to the dev environment, select it before starting the MCP server.

What this proves: the authoring loop is scriptable end to end by an agent. What it does not change: `publish` and `pac solution import` stay in CI under a federated credential (see `ci_pipeline.yml`), and the Agent 365 audit shows who or what published (E8, F6).
