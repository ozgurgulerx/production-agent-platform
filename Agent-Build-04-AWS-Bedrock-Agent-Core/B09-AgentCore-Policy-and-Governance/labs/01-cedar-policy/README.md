# 01 — Cedar policy on the ticket gateway

Engine, attach in `LOG_ONLY`, two policies, exercise, flip to `ENFORCE`, then generate a policy from a sentence and look at the reasoning findings. The point is to feel the difference between a limit in a prompt and a limit the gateway applies before the Lambda runs.

## Prerequisites
B04 lab 03 gateway (`TICKET_GATEWAY_ID`, `TICKET_GATEWAY_URL`, target `TicketTools`) and B04 lab 01 Cognito pool (`COGNITO_CLIENT_ID`, `COGNITO_TEST_USERNAME`). Region with Policy GA (13 regions on 3 Mar 2026; us-east-1 and us-west-2 are safe). Caller permissions: `bedrock-agentcore:CreatePolicyEngine`, `CreatePolicy`, `UpdateGateway`, `StartPolicyGeneration`, `logs:FilterLogEvents`.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python 01_create_engine.py            # POLICY_ENGINE_ID / ARN into .env
python 02_attach_log_only.py          # gateway.policyEngineConfiguration = {arn, LOG_ONLY}
python 03_policies.py                 # read-all + refund-cap-250
python 04_exercise.py                 # three calls pass; 900 logged as would-deny
python 05_enforce.py                  # ENFORCE; 900 denied with reason
python 06_generate_from_nl.py         # findings; --attach to add the VALID asset as LOG_ONLY
python 06_generate_from_nl.py --text "support agents may refund"     # expect ALLOW_ALL
python 07_temporal_dogwood.py         # dry run until the grammar is verified
python 05_enforce.py --cleanup        # detach, delete policies, delete engine
```

## What each script proves
- **01** an engine is just a container; it has an ARN the gateway will reference.
- **02** `UpdateGateway` carries the whole gateway definition again; the only new field is `policyEngineConfiguration`.
- **03** one statement per policy; `FAIL_ON_ANY_FINDINGS` rejects a policy the reasoner dislikes; each policy has its own `enforcementMode`.
- **04** `LOG_ONLY` is safe to attach to production: nothing is refused, decisions are logged.
- **05** `ENFORCE` denies the 900 GBP refund and anything with no permit at all (deny by default).
- **06** generated Cedar comes with findings; a sentence without a bound yields `ALLOW_ALL`.
- **07** temporal rules exist (Dogwood) but their grammar is unverified here.

## Proof checklist
- [ ] `01` printed an engine id and `ACTIVE`
- [ ] `02` printed `policy: {'arn': ..., 'mode': 'LOG_ONLY'}`
- [ ] `03` listed `read-all ACTIVE` and `refund-cap-250 ACTIVE`
- [ ] `04` showed three `ok` lines and at least one decision-log line for the 900 call (log group name recorded here: ______)
- [ ] `05` showed `DENIED` for 900 with the policy name in the body
- [ ] `06` printed a `VALID` asset for the default sentence and `ALLOW_ALL` for the short one
- [ ] `07` outcome recorded (grammar from docs: ______)
- [ ] cleanup left `policyEngineConfiguration` empty on the gateway

## Unverified on 2026-10-25
Decision log group name; whether omitting `policyEngineConfiguration` in `UpdateGateway` detaches; `GetPolicyGeneration` terminal status names; Dogwood grammar and whether it uses the `definition.policy` slot; principal attribute path for Cognito groups.
