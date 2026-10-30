# Domain 2: Design for New Solutions (29%)

Verbatim from the SAP-C02 guide: https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain2.html

## Task 2.1: Design a deployment strategy to meet business requirements

Knowledge of: Infrastructure as code (CloudFormation) · CI/CD · Change management processes · Configuration management tools (Systems Manager)

- [ ] Determining an application or upgrade path for new services and features
- [ ] Selecting services to develop deployment strategies and implement appropriate rollback mechanisms
- [ ] Adopting managed services as needed to reduce infrastructure provisioning and patching overhead
- [ ] Making advanced technologies accessible by delegating complex development and deployment tasks to AWS
  - Know how to: CloudFormation StackSets, change sets, drift, custom resources, CDK; CodePipeline/CodeBuild/CodeDeploy deployment configs (in-place, blue/green, canary, linear) for EC2, Lambda, ECS; Elastic Beanstalk deployment policies; SSM Automation, Patch Manager, State Manager, Change Manager; App Runner, Proton.
  - Read: CloudFormation best practices https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html · StackSets https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html · CodeDeploy deployment types https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments.html · Systems Manager https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html · Deployment strategies (Prescriptive Guidance) https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/deployment-strategies.html

## Task 2.2: Design a solution to ensure business continuity

Knowledge of: AWS Global Infrastructure · AWS networking concepts (Route 53, routing methods) · RTOs and RPOs · Disaster recovery scenarios (backup and restore, pilot light, warm standby, multi-site) · Disaster recovery solutions on AWS

- [ ] Configuring disaster recovery solutions
- [ ] Configuring data and database replication
- [ ] Performing disaster recovery testing
- [ ] Architecting a backup solution that is automated, is cost-effective, and supports business continuity across multiple Availability Zones or AWS Regions
- [ ] Designing an architecture that provides application and infrastructure availability in the event of a disruption
- [ ] Using processes and components for centralized monitoring to proactively recover from system failures
  - Know how to: Route 53 failover with health checks, ARC readiness checks and routing controls, Aurora Global Database (managed failover, write forwarding), RDS cross-region read replicas, DynamoDB global tables, S3 CRR with RTC, EFS replication, FSx backups, Fault Injection Service for game days.
  - Read: DR whitepaper https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html · Aurora Global Database https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html · DynamoDB global tables https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html · Route 53 failover https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover.html · Fault Injection Service https://docs.aws.amazon.com/fis/latest/userguide/what-is.html · S3 replication https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html

## Task 2.3: Determine security controls based on requirements

Knowledge of: IAM · Route tables, security groups, network ACLs · Encryption options at rest and in transit · AWS service endpoints · Credential management services · AWS managed security services (Shield, WAF, GuardDuty, Security Hub)

- [ ] Specifying IAM users and IAM roles that adhere to the principle of least privilege access
- [ ] Specifying inbound and outbound network flows by using security group rules and network ACL rules
- [ ] Developing attack mitigation strategies for large-scale web applications
- [ ] Developing encryption strategies for data at rest and data in transit
- [ ] Specifying service endpoints for service integrations
- [ ] Developing strategies for patch management to remain compliant with organizational standards
  - Know how to: IAM policy evaluation logic, Access Analyzer policy generation, session policies; SG stateful vs NACL stateless; Shield Advanced + WAF + CloudFront + Route 53 for DDoS; Network Firewall; Secrets Manager rotation vs Parameter Store; ACM + ALB/CloudFront TLS, S3 bucket keys, EBS default encryption; Patch Manager baselines and maintenance windows; Inspector.
  - Read: Security pillar https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html · Policy evaluation logic https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html · DDoS resiliency best practices https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/welcome.html · WAF https://docs.aws.amazon.com/waf/latest/developerguide/what-is-aws-waf.html · Secrets Manager https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html · Patch Manager https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager.html · Network Firewall https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html

## Task 2.4: Design a strategy to meet reliability requirements

Knowledge of: AWS Global Infrastructure · AWS storage services and replication strategies (S3, RDS, ElastiCache) · Multi-AZ and multi-Region architectures · Auto scaling policies and events · Application integration (SNS, SQS, Step Functions) · Service quotas and limits

- [ ] Designing highly available application environments based on business requirements
- [ ] Using advanced techniques to design for failure and ensure seamless system recoverability
- [ ] Implementing loosely coupled dependencies
- [ ] Operating and maintaining high-availability architectures (for example, application failovers, database failovers)
- [ ] Using AWS managed services for high availability
- [ ] Implementing DNS routing policies (for example, Route 53 latency-based routing, geolocation routing, simple routing)
  - Know how to: Auto Scaling policies (target tracking, step, predictive, scheduled), lifecycle hooks, warm pools; SQS (standard vs FIFO, DLQ, visibility timeout), SNS fan-out, EventBridge, Step Functions standard vs express; RDS Multi-AZ instance vs cluster, ElastiCache Multi-AZ, Global Datastore; Route 53 routing policies incl. geoproximity and weighted; Service Quotas and quota monitoring; static stability and cell-based architecture.
  - Read: Reliability pillar https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html · Auto Scaling policies https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html · Route 53 routing policies https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html · SQS best practices https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-best-practices.html · RDS Multi-AZ https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html · Static stability (Builders' Library) https://aws.amazon.com/builders-library/static-stability-using-availability-zones/ · Service Quotas https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html

## Task 2.5: Design a solution to meet performance objectives

Knowledge of: Performance monitoring technologies · Storage options on AWS · Instance families and use cases · Purpose-built databases

- [ ] Designing large-scale application architectures for a variety of access patterns
- [ ] Designing an elastic architecture based on business objectives
- [ ] Applying design patterns to meet performance objectives with caching, buffering, and replicas
- [ ] Developing a process methodology for selecting purpose-built services for required tasks
- [ ] Designing a rightsizing strategy
  - Know how to: EBS volume types (gp3, io2 Block Express), EFS throughput modes, FSx (Windows, Lustre, NetApp ONTAP, OpenZFS), S3 performance (prefixes, Transfer Acceleration, Express One Zone); instance families (C/M/R/I/G/P, Graviton, Nitro); DynamoDB DAX, ElastiCache, CloudFront, Global Accelerator; purpose-built DB choice (Aurora, DynamoDB, DocumentDB, Neptune, Timestream, Keyspaces, MemoryDB, Redshift); CloudWatch, X-Ray, Compute Optimizer.
  - Read: Performance efficiency pillar https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html · Choosing an AWS database https://docs.aws.amazon.com/decision-guides/latest/databases-on-aws-how-to-choose/databases-on-aws-how-to-choose.html · Storage decision guide https://docs.aws.amazon.com/decision-guides/latest/storage-on-aws-how-to-choose/choosing-aws-storage-service.html · EBS volume types https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html · Instance types https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-types.html · Global Accelerator vs CloudFront https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html

## Task 2.6: Determine a cost optimization strategy to meet solution goals and objectives

Knowledge of: AWS cost and usage monitoring tools (Cost Explorer, Trusted Advisor, Pricing Calculator) · Pricing models (Reserved Instances, Savings Plans) · Storage tiering · Data transfer costs · AWS managed service offerings

- [ ] Identifying opportunities to select and rightsize infrastructure for cost-effective resources
- [ ] Identifying appropriate pricing models
- [ ] Performing data transfer modeling and selecting services to reduce data transfer costs
- [ ] Developing a strategy and implementing controls for expenditure and usage awareness
  - Know how to: S3 storage classes and Intelligent-Tiering, lifecycle rules, Glacier retrieval tiers; data transfer pricing (inter-AZ, inter-region, NAT Gateway vs gateway endpoints, CloudFront egress, Direct Connect egress); Spot with Auto Scaling mixed instances; Lambda vs Fargate vs EC2 break-even; Budgets and Cost Anomaly Detection.
  - Read: Cost optimization pillar https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html · S3 storage classes https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html · Data transfer costs overview https://aws.amazon.com/blogs/architecture/overview-of-data-transfer-costs-for-common-architectures/ · EC2 Spot best practices https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-best-practices.html · Budgets https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html
