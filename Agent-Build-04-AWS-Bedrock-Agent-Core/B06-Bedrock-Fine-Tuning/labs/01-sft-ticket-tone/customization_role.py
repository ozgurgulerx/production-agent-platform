"""Create the IAM role a Bedrock customisation job assumes, scoped to the finetune/ prefix. Writes FT_ROLE_ARN.

Proves: the job runs under a Bedrock-trusted role (bedrock.amazonaws.com, pinned to this account) with read on the
training prefix and write on the output prefix, not under your SSO identity. --cleanup deletes it.
"""
import json
import sys

from _common import account_id, need, session, write_env

ROLE = "bedrock-ticket-tone-customization-role"
BUCKET = need("CODE_BUCKET")


def main() -> None:
    iam = session().client("iam")
    if "--cleanup" in sys.argv:
        iam.delete_role_policy(RoleName=ROLE, PolicyName="finetune-s3")
        iam.delete_role(RoleName=ROLE)
        print("deleted", ROLE)
        return
    acct = account_id()
    trust = {"Version": "2012-10-17", "Statement": [{
        "Effect": "Allow", "Principal": {"Service": "bedrock.amazonaws.com"}, "Action": "sts:AssumeRole",
        "Condition": {"StringEquals": {"aws:SourceAccount": acct},
                      "ArnLike": {"aws:SourceArn": f"arn:aws:bedrock:*:{acct}:model-customization-job/*"}}}]}
    policy = {"Version": "2012-10-17", "Statement": [
        {"Effect": "Allow", "Action": ["s3:GetObject", "s3:ListBucket"],
         "Resource": [f"arn:aws:s3:::{BUCKET}", f"arn:aws:s3:::{BUCKET}/finetune/*"]},
        {"Effect": "Allow", "Action": ["s3:PutObject"], "Resource": f"arn:aws:s3:::{BUCKET}/finetune/out/*"}]}
    try:
        arn = iam.create_role(RoleName=ROLE, AssumeRolePolicyDocument=json.dumps(trust),
                              Description="Bedrock model customisation for the ticket-tone lab")["Role"]["Arn"]
    except iam.exceptions.EntityAlreadyExistsException:
        arn = iam.get_role(RoleName=ROLE)["Role"]["Arn"]
        iam.update_assume_role_policy(RoleName=ROLE, PolicyDocument=json.dumps(trust))
    iam.put_role_policy(RoleName=ROLE, PolicyName="finetune-s3", PolicyDocument=json.dumps(policy))
    write_env("FT_ROLE_ARN", arn)


if __name__ == "__main__":
    main()
