# C07 labs — the code-first dev loop

No tenant runtime to install, because there is none. The lab needs `pac` (`dotnet tool install --global Microsoft.PowerApps.CLI.Tool`), a device-code `pac auth` profile for the dev environment (see [`../../labs-setup/00-setup/README.md`](../../labs-setup/00-setup/README.md)), Git, and the shared venv for the Agents SDK part.

```
labs/
└── 01-dev-loop/   clone the ticket agent as YAML, edit, pull, push, publish; pack + import in CI; the SDK agent locally with the Playground and a tunnel
```

| Lab | Chapter section | Needs |
|---|---|---|
| 01 | §2 YAML artefact, §3 loop, §4 SDK agent locally, §5 pac MCP server | pac profile on a dev environment; the C03 lab 01 agent published once; C03 lab 04 `sdk_agent/` for the local part |
