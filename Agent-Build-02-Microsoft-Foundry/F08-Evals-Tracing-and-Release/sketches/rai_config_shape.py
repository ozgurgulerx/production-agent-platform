"""Untested sketch. Where a guardrail is attached, three ways. Full ARM IDs, never bare names, for the hosted agent."""
SUB, RG, ACCT = "<sub>", "<rg>", "<account>"
POLICY_ID = f"/subscriptions/{SUB}/resourceGroups/{RG}/providers/Microsoft.CognitiveServices/accounts/{ACCT}/raiPolicies/ticket-strict"

# 1. model deployment (Bicep/ARM): properties.raiPolicyName = "ticket-strict"   (bare name here)
# 2. hosted agent version (azure-ai-projects 2.7): HostedAgentDefinition(..., rai_config=RaiConfig(rai_policy_name=POLICY_ID))
#    omit rai_config -> NO guardrail; rai_config without name -> Microsoft.DefaultV2; wrong ID -> often fails OPEN
# 3. azure.yaml (azd):   policies: [{ type: rai_policy, raiPolicyName: <POLICY_ID> }]
# Test: send a known jailbreak from F05 lab 02's red-team set and expect a block, separately from /readiness.
