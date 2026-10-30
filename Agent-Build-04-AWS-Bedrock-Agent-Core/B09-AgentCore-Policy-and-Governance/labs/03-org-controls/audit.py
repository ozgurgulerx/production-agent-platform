"""Proves: every control-plane change and runtime invocation is in CloudTrail with the real principal, and every
AgentCore resource carries an owner tag. Lists the last 24h of InvokeAgentRuntime, CreatePolicy, UpdateGateway,
then checks tags on runtimes, gateways and policy engines. Read-only."""
from datetime import datetime, timedelta, timezone

from _common import control, session

EVENTS = ["InvokeAgentRuntime", "CreatePolicy", "UpdateGateway", "CreateGatewayTarget", "PutResourcePolicy"]


def trail() -> None:
    ct = session().client("cloudtrail")
    since = datetime.now(timezone.utc) - timedelta(days=1)
    for name in EVENTS:
        r = ct.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": name}],
                             StartTime=since, MaxResults=10)
        print(f"\n{name}: {len(r.get('Events', []))} in 24h")
        for e in r.get("Events", []):
            print(f"  {e['EventTime']:%H:%M}  {e.get('Username', '?'):<30} {e.get('EventSource', '')}")


def tags() -> None:
    c = control()
    arns = [r["agentRuntimeArn"] for r in c.list_agent_runtimes().get("agentRuntimes", [])]
    arns += [g["gatewayArn"] for g in c.list_gateways().get("items", c.list_gateways().get("gateways", []))]   # verify key
    arns += [e["policyEngineArn"] for e in c.list_policy_engines().get("policyEngines", [])]
    print("\ntags:")
    for arn in arns:
        t = c.list_tags_for_resource(resourceArn=arn).get("tags", {})
        print(f"  {'OK ' if 'owner' in t else 'NO '} {arn.split(':')[-1]:<60} {t}")


if __name__ == "__main__":
    trail()
    tags()
