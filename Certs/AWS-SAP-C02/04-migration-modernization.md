# Domain 4: Accelerate Workload Migration and Modernization (20%)

Verbatim from the SAP-C02 guide: https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain4.html

## Task 4.1: Select existing workloads and processes for potential migration

Knowledge of: Migration assessment and tracking tools (Migration Hub) · Portfolio assessment · Asset planning · Prioritization and migration of workloads (wave planning)

- [ ] Completing an application migration assessment
- [ ] Evaluating applications according to the seven common migration strategies (7Rs)
- [ ] Evaluating total cost of ownership (TCO)
  - Know how to: the 7 Rs (rehost, replatform, repurchase, refactor/re-architect, relocate, retain, retire); Migration Evaluator (TSO Logic) for business case; Application Discovery Service (agentless collector vs agent); Migration Hub strategy recommendations, wave planning and Journeys; Cloud Adoption Framework for AWS.
  - Read: Large migration guide (7 Rs) https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/ · Migration Evaluator https://aws.amazon.com/migration-evaluator/ · Application Discovery Service https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html · Migration Hub https://docs.aws.amazon.com/migrationhub/latest/ug/whatishub.html · Migration Hub Strategy Recommendations https://docs.aws.amazon.com/migrationhub-strategy/latest/userguide/what-is-mhub-strategy.html · AWS CAF https://docs.aws.amazon.com/whitepapers/latest/overview-aws-cloud-adoption-framework/welcome.html

## Task 4.2: Determine the optimal migration approach for existing workloads

Knowledge of: Data migration options and tools (DataSync, Transfer Family, Snow Family, S3 Transfer Acceleration) · Application migration tools (Application Discovery Service, Application Migration Service) · AWS networking services and DNS (Direct Connect, Site-to-Site VPN, Route 53) · Identity services (IAM Identity Center, Directory Service) · Database migration tools (DMS, SCT) · Governance tools (Control Tower, Organizations)

- [ ] Selecting the appropriate database transfer mechanism
- [ ] Selecting the appropriate application transfer mechanism
- [ ] Selecting the appropriate data transfer service and migration strategy
- [ ] Applying the appropriate security methods to migration tools
- [ ] Selecting the appropriate governance model
  - Know how to: DMS (full load + CDC, serverless, homogeneous vs heterogeneous with SCT, Fleet Advisor), native tools (backup/restore, Aurora snapshot import, pg_dump); MGN (agent-based replication, launch templates, post-launch actions) vs VM Import; DataSync (agent, NFS/SMB/HDFS/object), Transfer Family (SFTP/FTPS/AS2), Snowball Edge / Snowcone, Storage Gateway for hybrid; bandwidth maths for transfer choice; Directory Service (Managed AD, AD Connector), Identity Center during migration.
  - Read: DMS https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html · SCT https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Welcome.html · Application Migration Service https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html · DataSync https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html · Snow Family https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html · Transfer Family https://docs.aws.amazon.com/transfer/latest/userguide/what-is-aws-transfer-family.html · Directory Service https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html

## Task 4.3: Determine a new architecture for existing workloads

Knowledge of: Compute services (EC2, Elastic Beanstalk) · Containers (ECS, EKS, Fargate, ECR) · AWS storage services (EBS, EFS, FSx, S3, Storage Gateway Volume Gateway) · Databases (DynamoDB, OpenSearch Service, RDS, self-managed databases on EC2)

- [ ] Selecting the appropriate compute platform
- [ ] Selecting the appropriate container hosting platform
- [ ] Selecting the appropriate storage service
- [ ] Selecting the appropriate database platform
  - Know how to: EC2 vs Beanstalk vs ECS/EKS (EC2 vs Fargate launch) vs App Runner vs Lambda; EKS Anywhere / ECS Anywhere / Outposts for hybrid; EFS vs FSx for Windows (SMB, AD) vs FSx ONTAP (multi-protocol) vs FSx Lustre; Storage Gateway types (S3 File, FSx File, Volume cached/stored, Tape); RDS vs self-managed on EC2 triggers (unsupported engine features, OS access); App2Container.
  - Read: Compute decision guide https://docs.aws.amazon.com/decision-guides/latest/compute-on-aws-how-to-choose/compute-on-aws-how-to-choose.html · Containers decision guide https://docs.aws.amazon.com/decision-guides/latest/containers-on-aws-how-to-choose/choosing-aws-container-service.html · FSx overview https://docs.aws.amazon.com/fsx/ · Storage Gateway https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html · App2Container https://docs.aws.amazon.com/app2container/latest/UserGuide/what-is-a2c.html · Databases decision guide https://docs.aws.amazon.com/decision-guides/latest/databases-on-aws-how-to-choose/databases-on-aws-how-to-choose.html

## Task 4.4: Determine opportunities for modernization and enhancements

Knowledge of: Serverless compute offerings (Lambda) · Containers (ECS, EKS, Fargate) · AWS storage services (S3, EFS) · Purpose-built databases (DynamoDB, Aurora Serverless, ElastiCache) · Integration services (SQS, SNS, EventBridge, Step Functions)

- [ ] Identifying opportunities to decouple application components
- [ ] Identifying opportunities for serverless solutions
- [ ] Selecting the appropriate service for containers
- [ ] Identifying opportunities for purpose-built databases
- [ ] Selecting the appropriate application integration service
  - Know how to: strangler fig and anti-corruption layer with API Gateway; event-driven decoupling (EventBridge pipes, SQS, SNS); Step Functions vs SWF vs Airflow (MWAA); Aurora Serverless v2 and Babelfish (SQL Server → PostgreSQL); DynamoDB single-table design; Lambda limits (15 min, 10 GB, concurrency) that rule it out; Fargate vs EC2 launch type for ECS; MQ for legacy JMS/AMQP.
  - Read: Strangler fig pattern https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/strangler-fig.html · Modernization guides https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-decomposing-monoliths/ · EventBridge https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html · Step Functions https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html · Aurora Serverless v2 https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html · Babelfish https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/babelfish.html · Lambda quotas https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html

## Emerging topics (SAP-C02, unscored pretest items)

"Design security and responsible AI controls" — skills in:
- Implementing content filtering and regulatory compliance controls for generative AI services (for example, by using Amazon Bedrock Guardrails).
- Implementing access controls for generative and agentic AI applications (for example, by using AgentCore Identity).
- Designing human oversight workflows that include approval mechanisms for AI operations (for example, by using AWS Step Functions).

Covered in depth in [../AWS-AIP-C01/03-safety-security-governance.md](../AWS-AIP-C01/03-safety-security-governance.md). Expect these to be scored in SAP-C03.
