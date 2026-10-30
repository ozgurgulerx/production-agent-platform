"""Proves: one Bedrock guardrail resource carries every policy type; a version freezes it.

Standard tier (multilingual, prompt-leakage) where the region supports it (needs a cross-Region guardrail
profile; --classic falls back). Content filters incl. PROMPT_ATTACK, denied topic 'financial advice', PII
anonymised, contextual grounding. Writes GUARDRAIL_ID / GUARDRAIL_VERSION to .env. --cleanup deletes.
"""
import sys
from _common import GUARDRAIL_ID, REGION, bedrock, write_env

NAME = "ticket-agent-guardrail"
br = bedrock()
if "--cleanup" in sys.argv:
    if GUARDRAIL_ID:
        br.delete_guardrail(guardrailIdentifier=GUARDRAIL_ID); print("deleted", GUARDRAIL_ID)
    sys.exit(0)

tier = {"tierName": "CLASSIC" if "--classic" in sys.argv else "STANDARD"}
kw = {}
if tier["tierName"] == "STANDARD":
    geo = "eu" if REGION.startswith("eu-") else "us"
    kw["crossRegionConfig"] = {"guardrailProfileIdentifier": f"{geo}.guardrail.v1:0"}   # verify profile id
r = br.create_guardrail(
    name=NAME, description="B05 lab 03: model-side guardrail for the ticket agent",
    contentPolicyConfig={"tierConfig": tier, "filtersConfig": [
        {"type": "PROMPT_ATTACK", "inputStrength": "HIGH", "outputStrength": "NONE"},
        {"type": "HATE", "inputStrength": "MEDIUM", "outputStrength": "MEDIUM"},
        {"type": "INSULTS", "inputStrength": "MEDIUM", "outputStrength": "MEDIUM"},
        {"type": "MISCONDUCT", "inputStrength": "MEDIUM", "outputStrength": "MEDIUM"}]},
    topicPolicyConfig={"tierConfig": tier, "topicsConfig": [{
        "name": "financial-advice", "type": "DENY",
        "definition": "Advice on investing, loans, credit products or what to do with refunded money.",
        "examples": ["Should I put the refund into crypto?", "Which savings account is best?"]}]},
    sensitiveInformationPolicyConfig={"piiEntitiesConfig": [
        {"type": "CREDIT_DEBIT_CARD_NUMBER", "action": "ANONYMIZE"},
        {"type": "EMAIL", "action": "ANONYMIZE"},
        {"type": "UK_NATIONAL_INSURANCE_NUMBER", "action": "BLOCK"}]},   # verify entity name
    contextualGroundingPolicyConfig={"tierConfig": tier, "filtersConfig": [
        {"type": "GROUNDING", "threshold": 0.7}, {"type": "RELEVANCE", "threshold": 0.7}]},
    blockedInputMessaging="I can only help with support tickets and refunds within policy.",
    blockedOutputsMessaging="That response was withheld by the support guardrail.",
    **kw,
)
gid = r["guardrailId"]; print("guardrail:", gid, "draft version:", r["version"])
v = br.create_guardrail_version(guardrailIdentifier=gid, description="v1 for B05 lab 03")
print("version:", v["version"])
write_env("GUARDRAIL_ID", gid); write_env("GUARDRAIL_VERSION", v["version"])
print("pricing: content filters/denied topics $0.15, PII and grounding $0.10 per 1K text units; both tiers same price")
