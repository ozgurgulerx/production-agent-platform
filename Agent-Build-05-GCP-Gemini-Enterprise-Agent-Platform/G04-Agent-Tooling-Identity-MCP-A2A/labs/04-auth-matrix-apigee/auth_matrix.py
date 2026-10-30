"""Run one ticket-agent per credential type against TICKET_MCP_URL (or --target) and print what happened.
Usage: python auth_matrix.py [--row ROW] [--target URL]. Status: scaffold only, functionality unverified."""
import argparse
import asyncio

from ticket_agent.agent import ROWS, TICKET_MCP_URL, make_agent


async def run_row(row: str, target: str) -> str:
    """Return 'ROW | status | principal seen | note'. Catch adk_request_credential for the OAUTH2/OIDC rows."""
    agent = make_agent(row, target)
    # TODO(learner): Runner(agent=agent, app_name="g04-lab04", session_service=InMemorySessionService(), auto_create_session=True)
    # run "What is the status of ticket 1002?"; on an adk_request_credential function call print auth_uri, input() the
    # redirect, send the FunctionResponse (sketches/consent_and_resume.py); capture the tool response or the error.
    return f"{row:<16} TODO(learner)"


async def main(rows: list[str], target: str) -> None:
    for row in rows:
        print(await run_row(row, target))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--row", choices=ROWS)
    ap.add_argument("--target", default=TICKET_MCP_URL)
    a = ap.parse_args()
    asyncio.run(main([a.row] if a.row else ROWS, a.target))
