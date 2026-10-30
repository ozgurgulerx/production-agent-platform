"""Proves: the one-time account step every AgentCore evaluation depends on.

Switches the X-Ray trace segment destination to CloudWatch Logs (= Transaction Search) and sets the
indexing rule to 1% (free tier). Idempotent: prints the current state first and exits if already set.
"""
import sys
from _common import session

xray = session().client("xray")
current = xray.get_trace_segment_destination()
print("destination:", current.get("Destination"), "status:", current.get("Status"))
if current.get("Destination") == "CloudWatchLogs" and "--force" not in sys.argv:
    rules = xray.get_indexing_rules().get("IndexingRules", [])
    print("indexing rules:", [(r.get("Name"), r.get("Rule")) for r in rules])
    print("already enabled; nothing to do")
    sys.exit(0)

xray.update_trace_segment_destination(Destination="CloudWatchLogs")
print("destination -> CloudWatchLogs (takes a few minutes to become ACTIVE)")
pct = float(sys.argv[sys.argv.index("--sample") + 1]) if "--sample" in sys.argv else 1.0
xray.update_indexing_rule(Name="Default", Rule={"Probabilistic": {"DesiredSamplingPercentage": pct}})  # verify rule name
print(f"indexing rule Default -> {pct}% (1% is free; higher is billed)")
print("console: CloudWatch -> Settings -> Transaction Search; then GenAI Observability -> Bedrock AgentCore")
