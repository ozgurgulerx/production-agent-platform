# Domain 1: Design Solutions for Organizational Complexity (26%)

Verbatim from the SAP-C02 guide: https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain1.html

## Task 1.1: Architect network connectivity strategies

Knowledge of: AWS Global Infrastructure · AWS networking concepts (Amazon VPC, AWS Direct Connect, AWS VPN, transitive routing, AWS container services) · Hybrid DNS concepts (Route 53 Resolver, on-premises DNS integration) · Network segmentation (subnetting, IP addressing, connectivity among VPCs) · Network traffic monitoring

- [ ] Evaluating connectivity options for multiple VPCs
- [ ] Evaluating connectivity options for on-premises, co-location, and cloud integration
- [ ] Selecting AWS Regions and Availability Zones based on network and latency requirements
- [ ] Troubleshooting traffic flows by using AWS tools
- [ ] Using service endpoints for service integrations
  - Know how to: peering vs Transit Gateway vs PrivateLink vs Cloud WAN; Direct Connect (dedicated/hosted, DX Gateway, transit VIF, SiteLink, MACsec) vs Site-to-Site VPN (accelerated, ECMP); Route 53 Resolver inbound/outbound endpoints and forwarding rules; VPC Reachability Analyzer, Network Access Analyzer, flow logs, Traffic Mirroring; IPAM; gateway vs interface endpoints and endpoint policies.
  - Read: Multi-VPC network whitepaper https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html · Transit Gateway https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html · Direct Connect https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html · Hybrid DNS with Route 53 Resolver https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver.html · Reachability Analyzer https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html · PrivateLink https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html · Cloud WAN https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html

## Task 1.2: Prescribe security controls

Knowledge of: IAM and IAM Identity Center · Route tables, security groups, and network ACLs · Encryption keys and certificate management (AWS KMS, ACM) · AWS security, identity, and compliance tools (CloudTrail, IAM Access Analyzer, Security Hub, Amazon Inspector)

- [ ] Evaluating cross-account access management
- [ ] Integrating with third-party identity providers
- [ ] Deploying encryption strategies for data at rest and data in transit
- [ ] Developing a strategy for centralized security event notifications and auditing
  - Know how to: cross-account roles vs resource policies vs RAM; SCPs and RCPs; permission boundaries; Identity Center with external IdP (SAML/SCIM), Cognito for app users; KMS key policies, grants, multi-region keys, custom key stores; ACM public vs private CA; organisation trail, Security Hub delegated admin, GuardDuty, Detective, Inspector, Config aggregator.
  - Read: IAM best practices https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html · Cross-account access https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html · SCPs https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html · RCPs https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html · IAM Identity Center https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html · KMS concepts https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html · Security Hub https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html · Security Reference Architecture https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html

## Task 1.3: Design reliable and resilient architectures

Knowledge of: RTOs and RPOs · Disaster recovery strategies (AWS Elastic Disaster Recovery, pilot light, warm standby, multi-site) · Data backup and restoration

- [ ] Designing disaster recovery solutions based on RTO and RPO requirements
- [ ] Implementing architectures to automatically recover from failure
- [ ] Developing the optimal architecture by considering scale-up and scale-out options
- [ ] Designing an effective backup and restoration strategy
  - Know how to: the four DR strategies with cost/RTO/RPO ordering; Elastic Disaster Recovery (DRS) vs CloudEndure legacy; Route 53 health checks and ARC (Application Recovery Controller) routing controls and zonal shift; AWS Backup (policies, vault lock, cross-account/region copy); Aurora Global Database, DynamoDB global tables, S3 CRR/replication time control.
  - Read: DR whitepaper https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html · Elastic Disaster Recovery https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html · AWS Backup https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html · Application Recovery Controller https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route53-recovery.html · Reliability pillar https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html · Resilience Hub https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html

## Task 1.4: Design a multi-account AWS environment

Knowledge of: AWS Organizations and AWS Control Tower · Multi-account event notifications · AWS resource sharing across environments

- [ ] Evaluating the most appropriate account structure for organizational requirements
- [ ] Recommending a strategy for central logging and event notifications
- [ ] Developing a multi-account governance model
  - Know how to: OU design (security, infrastructure, workloads, sandbox, suspended), Control Tower landing zone, guardrails (preventive/detective/proactive), Account Factory for Terraform, delegated administrators, centralized CloudWatch Logs and CloudTrail Lake, EventBridge cross-account buses, RAM shared subnets/TGW, Service Catalog portfolios.
  - Read: Multi-account whitepaper https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html · Control Tower https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html · Organizations https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html · RAM https://docs.aws.amazon.com/ram/latest/userguide/what-is.html · EventBridge cross-account https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-cross-account.html · CloudTrail Lake https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html

## Task 1.5: Determine cost optimization and visibility strategies

Knowledge of: AWS cost and usage monitoring tools (Trusted Advisor, Pricing Calculator, Cost Explorer, Budgets) · AWS purchasing options (Reserved Instances, Savings Plans, Spot Instances) · AWS rightsizing visibility tools (Compute Optimizer, S3 Storage Lens)

- [ ] Monitoring cost and usage with AWS tools
- [ ] Developing an effective tagging strategy that maps costs to business units
- [ ] Understanding how purchasing options affect cost and performance
  - Know how to: Compute vs EC2 Instance vs SageMaker Savings Plans; RI types and sharing across the organisation; Spot interruption handling and capacity-optimized allocation; cost allocation tags and cost categories; CUR 2.0 to Athena; Budgets actions; Billing Conductor for chargeback.
  - Read: Cost optimization pillar https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html · Savings Plans https://docs.aws.amazon.com/savingsplans/latest/userguide/what-is-savings-plans.html · Cost allocation tags https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html · Compute Optimizer https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html · S3 Storage Lens https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage_lens.html · Cost and Usage Report https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html
