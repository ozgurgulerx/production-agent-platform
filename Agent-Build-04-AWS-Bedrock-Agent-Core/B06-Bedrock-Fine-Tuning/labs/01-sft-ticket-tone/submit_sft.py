"""Submit the SFT job on Nova 2 Lite and poll it to Completed. Writes FT_JOB_ARN and FT_CUSTOM_MODEL_ARN.

Proves: one create call; hyperparameters are a string map keyed per model family; validation metrics arrive with the
job. Cost is training tokens x epochs plus USD 1.95/model/month storage (reading map K9). Run after make_dataset.py and
customization_role.py.
"""
import os
import sys
import time

from _common import need, session, write_env

BASE = os.environ.get("BEDROCK_FT_BASE_MODEL_ID", "amazon.nova-2-lite-v1:0")
BUCKET, ROLE = need("CODE_BUCKET"), need("FT_ROLE_ARN")
JOB = f"ticket-tone-sft-{int(time.time())}"
MODEL_NAME = "ticket-tone-nova2lite"
HYPER = {"epochCount": "2", "learningRate": "0.00001", "batchSize": "1"}   # verify: key names on the Nova 2 Lite page


def main() -> None:
    br = session().client("bedrock")
    if "--status" in sys.argv:
        job_arn = need("FT_JOB_ARN")
    else:
        job_arn = br.create_model_customization_job(
            jobName=JOB, customModelName=MODEL_NAME, roleArn=ROLE, baseModelIdentifier=BASE,
            customizationType="FINE_TUNING",
            trainingDataConfig={"s3Uri": f"s3://{BUCKET}/finetune/train.jsonl"},
            validationDataConfig={"validators": [{"s3Uri": f"s3://{BUCKET}/finetune/valid.jsonl"}]},
            outputDataConfig={"s3Uri": f"s3://{BUCKET}/finetune/out/"},
            hyperParameters=HYPER,
            jobTags=[{"key": "track", "value": "B06"}], customModelTags=[{"key": "track", "value": "B06"}],
        )["jobArn"]
        write_env("FT_JOB_ARN", job_arn)
        print("submitted", JOB)
    while True:
        j = br.get_model_customization_job(jobIdentifier=job_arn)
        print(f"  {time.strftime('%H:%M:%S')} {j['status']} {j.get('statusDetails', '')}")
        if j["status"] in ("Completed", "Failed", "Stopped"):
            break
        time.sleep(60)
    if j["status"] != "Completed":
        raise SystemExit(j.get("failureMessage", j["status"]))
    print("training:", j.get("trainingMetrics"), "\nvalidation:", j.get("validationMetrics"))
    write_env("FT_CUSTOM_MODEL_ARN", j["outputModelArn"])
    print("next: python deploy_custom_model.py")


if __name__ == "__main__":
    main()
