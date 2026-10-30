"""Proves: StartPolicyGeneration turns a sentence into Cedar assets with automated-reasoning findings
(VALID | INVALID | NOT_TRANSLATABLE | ALLOW_ALL | ALLOW_NONE | DENY_ALL | DENY_NONE). A VALID asset can be attached
by reference as a LOG_ONLY policy. Try a bad sentence with --text "support agents may refund" to see ALLOW_ALL."""
import sys
import time

from _common import ENGINE_ID, control, gateway_arn, need

need("POLICY_ENGINE_ID", "TICKET_GATEWAY_ID")
DEFAULT = "Support agents may call issue_refund on TicketTools only when amount_gbp is at most 250."


def main() -> None:
    c = control()
    text = sys.argv[sys.argv.index("--text") + 1] if "--text" in sys.argv else DEFAULT
    gen = c.start_policy_generation(policyEngineId=ENGINE_ID, name="refund-rule-from-text",
                                    resource={"arn": gateway_arn()}, content={"rawText": text})
    gid = gen["policyGenerationId"]
    while gen.get("status") not in ("COMPLETED", "FAILED", "ACTIVE"):    # verify terminal status names
        time.sleep(5)
        gen = c.get_policy_generation(policyEngineId=ENGINE_ID, policyGenerationId=gid)
    print("generation", gid, gen["status"], gen.get("findings"))
    assets = c.list_policy_generation_assets(policyEngineId=ENGINE_ID, policyGenerationId=gid)
    valid_asset = None
    for a in assets.get("policyGenerationAssets", []):
        print("\nfragment:", a.get("rawTextFragment"))
        print(a.get("definition", {}).get("cedar", {}).get("statement", "").strip())
        for f in a.get("findings", []):
            print("  finding:", f["type"], "-", f.get("description"))
        if all(f["type"] == "VALID" for f in a.get("findings", [])) and a.get("findings"):
            valid_asset = a["policyGenerationAssetId"]
    if valid_asset and "--attach" in sys.argv:
        r = c.create_policy(policyEngineId=ENGINE_ID, name="refund-rule-generated",
                            definition={"policyGeneration": {"policyGenerationId": gid,
                                                             "policyGenerationAssetId": valid_asset}},
                            validationMode="FAIL_ON_ANY_FINDINGS", enforcementMode="LOG_ONLY")
        print("\nattached by reference:", r["policyId"], r["status"], "mode", r["enforcementMode"])


if __name__ == "__main__":
    main()
