import asyncio
import sys

from agents import Agent, Runner
from agents.mcp import MCPServerStdio


async def main():
    # Start the MCP server. Run this script from the S03.02 folder.
    async with MCPServerStdio(
        params={
            "command": sys.executable,
            "args": ["src/server.py"],
        },
    ) as ticket_server:
        # Give the model access to our MCP tools.
        agent = Agent(
            name="Support assistant",
            model="gpt-5.6-luna",
            instructions=(
                "Answer ticket and policy questions using the available tools. "
                "Do not invent details. If a record is missing, say so."
            ),
            mcp_servers=[ticket_server],
        )

        # Ask a question; the runner handles model requests and tool calls.
        result = await Runner.run(
            agent,
            "What is the status of ticket T-1001?",
        )
        print(result.final_output)


# Start the program when this file is run directly.
if __name__ == "__main__":
    asyncio.run(main())
