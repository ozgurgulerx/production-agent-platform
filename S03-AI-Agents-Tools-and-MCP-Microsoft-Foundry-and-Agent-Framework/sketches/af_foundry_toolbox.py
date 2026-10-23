"""Agent Framework consuming a Foundry toolbox.

The toolbox is one governed MCP endpoint (`/toolboxes/{name}/mcp` serves the
default version). `FoundryToolbox` attaches it; `as_skills_provider()` turns the
toolbox's `skill://` resources into skills. `require_approval` arrives as
`_meta.tool_configuration` and the consuming runtime must enforce it.

Names from Agent Framework and Foundry pages crawled on 23 Oct 2026 (reading
map F7, C1, C3). Untested; the integration is beta.
"""

from __future__ import annotations

from typing import Any

TOOLBOX_URL = "https://my-project.services.ai.azure.com/api/projects/p1/toolboxes/support/mcp"


def build(client: Any, credential: Any) -> Any:
    from agent_framework.foundry import FoundryToolbox  # noqa: WPS433

    toolbox = FoundryToolbox(url=TOOLBOX_URL, credential=credential)
    return client.as_agent(
        name="support",
        instructions="Use tool_search before calling; prefer get_policy over guessing.",
        tools=[toolbox],
        context_providers=[toolbox.as_skills_provider()],
    )
