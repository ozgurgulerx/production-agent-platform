# Section 2: Using coding agents for application development (~17%)

Objectives verbatim from the exam guide PDF (Sep 2026). This section names Antigravity (Google's agentic IDE) and Claude Code on Google Cloud explicitly.

## 2.1 Using coding agents effectively

- [ ] Configuring coding agents with Model Context Protocol (MCP) servers, custom skills, and access to tools (e.g., Antigravity and Claude Code on Google Cloud)
- [ ] Using coding agents in secure sandboxes (e.g., Google Kubernetes Engine [GKE], Cloud Workstations, and Antigravity)
- [ ] Using coding agents to refactor source code, optimize execution runtimes, and patch application-layer vulnerabilities
  - Know how to: add an MCP server to Antigravity and to Claude Code (`claude mcp add`), write a skill, run the agent inside Cloud Workstations or a GKE sandbox (gVisor / Agent Sandbox), use Google Cloud MCP servers for GCP resources, Claude on Vertex AI as the Claude Code backend.
  - Read: Antigravity docs https://antigravity.google/docs · Claude Code on Vertex AI https://docs.claude.com/en/docs/claude-code/google-vertex-ai · Claude Code MCP https://docs.claude.com/en/docs/claude-code/mcp · Claude Code skills https://docs.claude.com/en/docs/claude-code/skills · Google Cloud MCP servers https://github.com/googleapis/genai-toolbox · Cloud Workstations https://cloud.google.com/workstations/docs · GKE Agent Sandbox https://cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods · Gemini CLI https://github.com/google-gemini/gemini-cli · In repo: [S03 MCP chapters](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/), [S04.09 Harness Engineering](../../Agent-Build-01-Fundamentals/S04-Agentic-Workflows-and-Harnesses/S04.09-Harness-Engineering/README.md).

## 2.2 Customizing coding agents for enterprise workflows

- [ ] Creating skills, plugins, extensions hooks, rules, and subagents using Antigravity
- [ ] Augmenting Antigravity with Agents CLI to build, scale, govern, and optimize deployed agents
  - Know how to: Antigravity rules files, hooks on tool calls, subagent definitions, plugin/extension packaging; Agents CLI commands to scaffold, deploy to Agent Runtime, register in Agent Registry, and run evaluations from the terminal; the Skill Registry.
  - Read: Antigravity docs https://antigravity.google/docs · Agent Platform docs (Agents CLI, Skill Registry) https://cloud.google.com/agent-platform/docs · Gemini CLI extensions https://geminicli.com/docs/extensions/ · Claude Code hooks (same concepts) https://docs.claude.com/en/docs/claude-code/hooks
