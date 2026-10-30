"""Untested sketch. The six connection auth types as data; the tool only names the connection.
Runnable: ../labs/04-mcp-auth-apim/mcp_auth_matrix.py."""
AUTH_TYPES = {  # azd --auth-type : (principal the server sees, carries user?)
    "none": ("anonymous", False), "custom-keys": ("stored header", False),
    "project-managed-identity": ("project MI, shared", False), "agentic-identity": ("this agent's Entra identity", False),
    "user-entra-token": ("the user (same tenant)", True), "oauth2": ("the user after consent", True)}
# azd ai connection create <name> --kind remote-tool --target <url> --auth-type <type> [--audience <downstream app id>]
from azure.ai.projects.models import MCPTool
tool = MCPTool(server_label="ticketing", server_url="https://apim.example/mcp", require_approval="always", project_connection_id="<connection-name>")
