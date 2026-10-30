"""Create three records in the registry: an MCP record for the ticket Gateway (server descriptor + tool list), an A2A
record for the B03 A2A specialist (its agent card), and an AGENT_SKILLS record (a SKILL.md). Submit each for approval,
then approve them as the reviewer.

Proves: records are DRAFT → PENDING_APPROVAL → APPROVED; what is published is a descriptor, never a credential.
Run: python register_records.py
"""

import json
import os
from pathlib import Path

from _common import control, need

SKILL_MD = (Path(__file__).parent / "SKILL.md").read_text()


def submit_and_approve(cp, rid: str, rec_id: str) -> None:
    cp.submit_registry_record_for_approval(registryId=rid, recordId=rec_id)
    cp.update_registry_record_status(registryId=rid, recordId=rec_id, status="APPROVED", statusReason="lab reviewer")
    print("  approved", rec_id)


def main() -> None:
    cp, rid = control(), need("TICKET_REGISTRY_ID")

    mcp_rec = cp.create_registry_record(
        registryId=rid, name="ticket-gateway", descriptorType="MCP",
        description="Ticket tools for the UK card team (Gateway, Cognito JWT)",
        descriptors={"mcp": {
            "server": {"schemaVersion": "2025-06-18", "inlineContent": json.dumps({"name": "ticket-gateway", "url": need("TICKET_GATEWAY_URL"), "transport": "streamable-http"})},   # verify descriptor schema
            "tools": {"protocolVersion": "2025-06-18", "inlineContent": json.dumps([{"name": "tickets-lambda___issue_refund", "description": "Refund up to £250"}])},
        }},
        recordVersion="1.0.0",
    )
    print("MCP record", mcp_rec["recordArn"]); submit_and_approve(cp, rid, mcp_rec["recordArn"].split("/")[-1])

    card_url = os.environ.get("TICKET_A2A_CARD_URL")                   # written by B03 lab 03
    if card_url:
        a2a_rec = cp.create_registry_record(
            registryId=rid, name="refund-specialist", descriptorType="A2A",
            synchronizationType="URL", synchronizationConfiguration={"fromUrl": {"url": card_url,
                "credentialProviderConfigurations": [{"credentialProviderType": "IAM", "credentialProvider": {}}]}},   # verify
        )
        print("A2A record", a2a_rec["recordArn"]); submit_and_approve(cp, rid, a2a_rec["recordArn"].split("/")[-1])
    else:
        print("A2A record skipped: set TICKET_A2A_CARD_URL (B03 lab 03)")

    skill_rec = cp.create_registry_record(
        registryId=rid, name="refund-policy-skill", descriptorType="AGENT_SKILLS",
        descriptors={"agentSkills": {"skillMd": {"inlineContent": SKILL_MD}}},
        recordVersion="1.0.0",
    )
    print("skill record", skill_rec["recordArn"]); submit_and_approve(cp, rid, skill_rec["recordArn"].split("/")[-1])


if __name__ == "__main__":
    main()
