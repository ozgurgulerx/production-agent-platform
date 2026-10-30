"""Put the custom model behind an on-demand custom model deployment and poll to Active. Writes FT_DEPLOYMENT_ARN.

Proves: a custom model ARN is not callable by itself; the deployment ARN is the modelId you pass to Converse or to
Strands BedrockModel. --cleanup deletes the deployment and then the custom model (storage is billed monthly).
"""
import sys
import time

from _common import need, session, write_env

NAME = "ticket-tone-nova2lite-ondemand"


def cleanup(br) -> None:
    for d in br.list_custom_model_deployments(nameContains=NAME).get("modelDeploymentSummaries", []):
        br.delete_custom_model_deployment(customModelDeploymentIdentifier=d["customModelDeploymentArn"])
        print("deleted deployment", d["customModelDeploymentArn"])
    model_arn = need("FT_CUSTOM_MODEL_ARN")
    time.sleep(20)                                   # deployment teardown before model delete
    br.delete_custom_model(modelIdentifier=model_arn)
    print("deleted custom model", model_arn)


def main() -> None:
    br = session().client("bedrock")
    if "--cleanup" in sys.argv:
        cleanup(br)
        return
    model_arn = need("FT_CUSTOM_MODEL_ARN")
    existing = [d for d in br.list_custom_model_deployments(nameContains=NAME).get("modelDeploymentSummaries", [])
                if d["modelArn"] == model_arn]
    arn = existing[0]["customModelDeploymentArn"] if existing else br.create_custom_model_deployment(
        modelDeploymentName=NAME, modelArn=model_arn, description="B06 ticket-tone eval deployment",
        tags=[{"key": "track", "value": "B06"}])["customModelDeploymentArn"]
    while (d := br.get_custom_model_deployment(customModelDeploymentIdentifier=arn))["status"] == "Creating":
        print("  Creating ..."); time.sleep(30)
    if d["status"] != "Active":
        raise SystemExit(d.get("failureMessage", d["status"]))
    write_env("FT_DEPLOYMENT_ARN", arn)
    print("Active:", arn, "\nnext: python compare_base_vs_tuned.py")


if __name__ == "__main__":
    main()
