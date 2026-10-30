"""Untested sketch. OAuth user passthrough in ADK: consent is a function call named `adk_request_credential`,
answered with a FunctionResponse carrying the redirect (map D5)."""
from google.adk.auth import AuthConfig
from google.adk.tools import ToolContext
from google.genai import types


def refund_history(customer: str, tool_context: ToolContext) -> dict:
    """Tool side. Asks for the user's credential on first use, reads it on the retry."""
    creds = tool_context.get_auth_response(AUTH_CONFIG)          # None until the user has consented
    if creds is None:
        tool_context.request_credential(AUTH_CONFIG)            # ADK emits adk_request_credential {auth_uri}
        return {"status": "pending", "message": "waiting for user consent"}
    # TODO(learner): call the downstream API with creds; return {"status": "success", ...}
    return {"status": "success", "customer": customer}


AUTH_CONFIG: AuthConfig = None  # TODO(learner): AuthConfig(auth_scheme=OAuth2(...), raw_auth_credential=...)


async def drive(runner, session, prompt: str) -> str:
    """Client side. Loop until there is no pending credential request. Do not cache the token in state (D5)."""
    msg = types.Content(role="user", parts=[types.Part(text=prompt)])
    while True:
        pending = None
        async for event in runner.run_async(user_id=session.user_id, session_id=session.id, new_message=msg):
            for call in event.get_function_calls() or []:
                if call.name == "adk_request_credential":
                    pending = call
        if pending is None:
            return "final answer reached"      # TODO(learner): return the last text part
        auth_uri = pending.args["auth_config"]["exchanged_auth_credential"]["oauth2"]["auth_uri"]
        print("open and consent:", auth_uri)
        redirect = input("paste the full redirect URL: ")
        auth_config = dict(pending.args["auth_config"])
        auth_config["exchanged_auth_credential"]["oauth2"]["auth_response_uri"] = redirect
        auth_config["exchanged_auth_credential"]["oauth2"]["redirect_uri"] = "http://localhost:8000/callback"
        msg = types.Content(role="user", parts=[types.Part(function_response=types.FunctionResponse(
            id=pending.id, name="adk_request_credential", response=auth_config))])
        # ADK exchanges the code and retries the tool; get_auth_response now returns the credential
