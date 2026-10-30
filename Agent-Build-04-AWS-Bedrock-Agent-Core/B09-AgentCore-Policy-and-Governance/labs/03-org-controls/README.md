# 03 — Account and organisation controls

The non-Cedar half of governance: the execution role shape, a resource policy for a partner account, the SCPs you ask the platform team for, a CloudTrail and tag audit, and the PrivateLink picture. Everything prints by default; `--apply` creates, `--cleanup` removes.

## Run
```bash
source ../../../labs-setup/.venv/bin/activate
python execution_role.py                      # print trust + permissions; --apply to create ticket-agent-runtime-role
python resource_policy_runtime.py --partner 210987654321      # print; --apply to put it on TICKET_AGENT_RUNTIME_ARN
python audit.py                               # CloudTrail last 24h + tag check
cat scp/*.json                                # hand to the org admin
cat privatelink.md
```

## Proof checklist
- [ ] `execution_role.py --apply` created the role; `aws iam get-role` shows the `SourceArn` condition
- [ ] a runtime created with that role (B03 lab 01) still invokes the model (allow-list is right)
- [ ] `resource_policy_runtime.py --apply` succeeded and `get_resource_policy` returned it
- [ ] `audit.py` lists at least one `InvokeAgentRuntime` with a human or role principal, and every resource shows `OK`
- [ ] SCP JSON validated with `aws organizations create-policy --dry-run` equivalent (policy simulator) by the org admin

## Unverified on 2026-10-25
Runtime-endpoint ARN form in the resource policy; the `bedrock-agentcore:RuntimeAuthorizerType` condition key spelling; `list_gateways` response key (`items` vs `gateways`).
