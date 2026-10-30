"""Untested sketch. OAuth identity passthrough: consent is an output item; resume by previous_response_id."""
from openai.types.responses.response_input_param import McpApprovalResponse

def drive(openai, prompt: str):
    r = openai.responses.create(input=prompt, tool_choice="required")
    while True:
        consent = [i for i in r.output if i.type == "oauth_consent_request"]
        if consent:
            print("open and consent:", consent[0].consent_link)   # per tool, per project, per user; scopes need offline_access
            input("then press Enter")
            r = openai.responses.create(input=prompt, previous_response_id=r.id, tool_choice="required"); continue
        approvals = [i for i in r.output if i.type == "mcp_approval_request"]
        if approvals:
            r = openai.responses.create(previous_response_id=r.id, input=[McpApprovalResponse(
                type="mcp_approval_response", approve=True, approval_request_id=a.id) for a in approvals]); continue
        return r.output_text
