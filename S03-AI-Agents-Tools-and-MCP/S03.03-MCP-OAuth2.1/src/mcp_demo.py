"""Call an authenticated MCP tool, with human-only refund confirmation."""

import asyncio

from mcp import ClientSession, types
from mcp.client.streamable_http import streamablehttp_client

from auth import RESOURCE


def _known_confirmation(params: types.ElicitRequestParams) -> bool:
    if not isinstance(params, types.ElicitRequestFormParams) or params.mode != 'form':
        return False
    schema = params.requestedSchema
    properties = schema.get('properties', {})
    return (
        schema.get('type') == 'object'
        and isinstance(properties, dict)
        and set(properties) == {'confirm'}
        and isinstance(properties['confirm'], dict)
        and properties['confirm'].get('type') == 'boolean'
        and schema.get('required') == ['confirm']
    )


async def confirm_refund(context, params: types.ElicitRequestParams) -> types.ElicitResult:
    """Only terminal input can approve a supported confirmation form."""
    if not _known_confirmation(params):
        return types.ElicitResult(action='cancel')
    try:
        answer = await asyncio.to_thread(
            input, f'\n{params.message}\nType exactly YES to approve; anything else declines: '
        )
    except EOFError:
        return types.ElicitResult(action='cancel')
    if answer == 'YES':
        return types.ElicitResult(action='accept', content={'confirm': True})
    return types.ElicitResult(action='decline')


async def call_tool(access_token: str, name: str, arguments: dict) -> dict:
    """Send a token in the Authorization header and return the MCP result."""
    async with streamablehttp_client(
        RESOURCE, headers={'Authorization': f'Bearer {access_token}'},
    ) as (read, write, _):
        async with ClientSession(read, write, elicitation_callback=confirm_refund) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments=arguments)
            return result.model_dump(mode='json')
