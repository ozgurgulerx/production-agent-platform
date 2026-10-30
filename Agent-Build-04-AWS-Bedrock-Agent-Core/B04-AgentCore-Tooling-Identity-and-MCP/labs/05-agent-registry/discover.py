"""Discover approved records the way another team would: `agent-registry` client search, then list by type.
Also shows the registry's MCP endpoint for run-time discovery when the response exposes one.

Proves: discovery is a separate, read-only surface from management. Run: python discover.py
"""

import json

from _common import control, need, session


def main() -> None:
    rid = need("TICKET_REGISTRY_ID")
    disc = session().client("agent-registry")
    r = disc.search_discoverable_registry_records(searchQuery="refund", registryIds=[rid], maxResults=10)
    print("search 'refund':", json.dumps(r.get("registryRecords", r), indent=1, default=str)[:1200])   # verify key

    cp = control()
    for kind in ("MCP", "A2A", "AGENT_SKILLS"):
        recs = cp.list_registry_records(registryId=rid, descriptorType=kind, status="APPROVED").get("registryRecords", [])
        print(kind, [(x.get("name"), x.get("status")) for x in recs])

    reg = cp.get_registry(registryId=rid)
    print("registry MCP endpoint:", reg.get("mcpEndpoint") or "(not in GetRegistry output on 1.43.118; see console)")   # verify


if __name__ == "__main__":
    main()
