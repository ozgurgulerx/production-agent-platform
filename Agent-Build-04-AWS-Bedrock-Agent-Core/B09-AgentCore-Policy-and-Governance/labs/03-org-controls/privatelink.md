# Network isolation for AgentCore — described, not run

Facts dated 2026-10-25 from the release notes (A3) and FAQ. Nothing here is executed by a lab; the shapes are the ones the labs would use.

## What exists
- **Control-plane PrivateLink** for Gateway, Runtime, Memory and tools (Mar 2026): interface endpoints for `bedrock-agentcore-control` so `CreateAgentRuntime` and friends never leave the VPC. Pair with `aws:VpceOrgID` in IAM to refuse calls from endpoints outside your organisation.
- **Runtime and Memory VPC mode** (Sep 2025): `networkConfiguration.networkMode = "VPC"` with `networkModeConfig.subnets`, `securityGroups`, `requireServiceS3Endpoint` (shape in `CreateAgentRuntime`). The microVM gets an ENI in your subnet; egress follows your route tables.
- **VPC egress for Identity, Gateway and Runtime** (Apr 2026): OAuth providers and gateway targets inside your network, reached without a public path.
- **Private CA for VPC Lattice targets** (Oct 2026): gateway targets behind Lattice with your own certificate chain.
- **Private authorizer endpoints**: `customJWTAuthorizer.privateEndpoint` (self-managed Lattice resource or managed VPC resource) for an IdP discovery URL that is not public.

## The ticket agent, isolated
```
VPC 10.0.0.0/16
  private subnets (2 AZs)
    Runtime ENIs (VPC mode)  -> SG allows 443 to gateway endpoint, IdP, Bedrock endpoint
    Interface endpoints: bedrock-runtime, bedrock-agentcore-control, logs, xray, ecr.api, ecr.dkr, sts
    S3 gateway endpoint (requireServiceS3Endpoint = true for code deploy and session storage)
  no IGW, no NAT
Gateway: authorizer discoveryUrl via privateEndpoint; targets = Lambda in VPC + Lattice service with private CA
```

## Fields to set
| Object | Field | Value |
|---|---|---|
| Runtime | `networkConfiguration.networkMode` | `VPC` |
| Runtime | `networkModeConfig.subnets / securityGroups / requireServiceS3Endpoint` | two private subnets, one SG, `true` |
| Gateway authorizer | `customJWTAuthorizer.privateEndpoint.managedVpcResource` | `vpcIdentifier`, `subnetIds`, `securityGroupIds` |
| IAM | `Condition: {"StringEquals": {"aws:VpceOrgID": "o-xxxx"}}` | on control-plane allow statements |

## What it does not do
A VPC placement does not authorise anything. The Cedar policy (lab 01) and IAM (this lab) still decide; the network only decides who can get a packet to the door.
