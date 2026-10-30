# Way 4 — Runtime on Instances (described, not run)

GA 6 Aug 2026 (B5). A **capacity provider** is EC2 capacity in your account (any instance family, including GPU) that AgentCore schedules Runtime sessions onto. Everything else stays the same: same artifact, same `/invocations` contract, same versions and endpoints, same `InvokeAgentRuntime`. What changes:

| | microVM (default) | Instances |
|---|---|---|
| Where it runs | AgentCore-managed microVM per session | your EC2 instances, AgentCore-managed scheduling |
| Max session lifetime | 8 h | 14 days (`lifecycleConfiguration.maxLifetime`) |
| GPU | no | yes |
| Billing | per-second vCPU/GB | EC2 price + ~12 % management fee (L4) |
| Volumes | session storage, S3 Files, EFS | plus `capacityProviderVolume` |

Shape (bedrock-agentcore-control, boto3 1.43.118):
```python
cp.create_capacity_provider(name="ticket-gpu", ...)            # instance type, subnets, scaling; fields not fetched on 25 Oct 2026, verify
cp.create_agent_runtime(
    agentRuntimeName="ticket_agent_gpu",
    agentRuntimeArtifact={"containerConfiguration": {"containerUri": IMAGE}},
    roleArn=ROLE_ARN,
    capacityProviderConfiguration={"capacityProviderArn": CAPACITY_PROVIDER_ARN},
    lifecycleConfiguration={"idleRuntimeSessionTimeout": 3600, "maxLifetime": 14 * 24 * 3600},
    filesystemConfigurations=[{"capacityProviderVolume": {"volumeName": "models", "mountPath": "/models"}}],
)
```
`ListAgentRuntimeVersionsByCapacityProvider` tells you which versions are placed on which provider.

When to pick it: local models or embeddings on GPU inside the agent, sessions that outlive 8 h (long research jobs with interactive shells), or a data-residency rule that wants the compute in your VPC on your instances. When not to: everything else; the microVM path has no capacity to manage.

**Interview line.** "Instances change where the microVM's work lands, not the contract. Same image, same endpoint, 14-day sessions and your own GPUs."
