# The custom-connector route (reading map D3)

Same server, declared as a Power Platform custom connector from `openapi.yaml`. The single extension `x-ms-agentic-protocol: mcp-streamable-1.0` on the POST operation tells Copilot Studio the connector is an MCP server.

## Import
Portal: Power Apps → Custom connectors → New custom connector → Import an OpenAPI file → `openapi.yaml` → set the host to your Container Apps FQDN → Security: pick API key or OAuth 2.0 to match the deployed mode → Create. CLI alternative: `paconn create --api-def openapi.yaml --api-prop apiProperties.json` (paconn needs its own Python environment; not in the shared venv).

## Use
Copilot Studio → Tools → Add a tool → search the connector name → the MCP tools appear under it. Allow-list and DLP behave exactly as for the wizard route, because the wizard also creates a connector.

## Why bother
Solution-aware ALM: the custom connector travels in the solution with connection references, while a wizard-created connector is created per environment. Certification: a custom connector is what you submit when you want the server in the public connector catalogue (D2).
