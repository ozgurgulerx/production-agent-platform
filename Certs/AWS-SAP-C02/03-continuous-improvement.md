# Domain 3: Continuous Improvement for Existing Solutions (25%)

Verbatim from the SAP-C02 guide: https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02-domain3.html

## Task 3.1: Determine a strategy to improve overall operational excellence

Knowledge of: Alerting and automatic remediation strategies · Disaster recovery planning · Monitoring and logging solutions (CloudWatch) · CI/CD pipelines and deployment strategies (blue/green, all-at-once, rolling) · Configuration management tools (Systems Manager)

- [ ] Determining the most appropriate logging and monitoring strategy
- [ ] Evaluating current deployment processes for improvement opportunities
- [ ] Prioritizing opportunities for automation within a solution stack
- [ ] Recommending the appropriate AWS solution to enable configuration management automation
- [ ] Engineering failure scenario activities to support and exercise an understanding of recovery actions
  - Know how to: CloudWatch alarms (composite, anomaly), Logs Insights, metric filters, Contributor Insights, Synthetics, Application Signals; EventBridge → SSM Automation / Lambda remediation; Config auto-remediation; OpsCenter and Incident Manager; CodeDeploy configs; SSM State Manager, Run Command, AppConfig; FIS experiments; Health Dashboard events.
  - Read: Operational excellence pillar https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html · CloudWatch alarms https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html · Config remediation https://docs.aws.amazon.com/config/latest/developerguide/remediation.html · Incident Manager https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html · Fault Injection Service https://docs.aws.amazon.com/fis/latest/userguide/what-is.html · Application Signals https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html

## Task 3.2: Determine a strategy to improve security

Knowledge of: Data retention, sensitivity, regulatory requirements · Automated monitoring and remediation (Config rules) · Secrets management (Systems Manager, Secrets Manager) · Principle of least privilege · Security-specific AWS solutions · Patching practices · Backup practices and methods

- [ ] Evaluating a strategy for the secure management of secrets and credentials
- [ ] Auditing an environment for least privilege access
- [ ] Reviewing implemented solutions to ensure security at every layer
- [ ] Reviewing comprehensive traceability of users and services
- [ ] Prioritizing automated responses to the detection of vulnerabilities
- [ ] Designing and implementing a patch and update process
- [ ] Designing and implementing a backup process
- [ ] Employing remediation techniques
  - Know how to: Access Analyzer unused access and external access findings, IAM last-accessed data, credential reports; Macie for S3 PII, S3 Object Lock and Glacier Vault Lock for retention; GuardDuty findings → EventBridge → Lambda/SSM; Security Hub automation rules; Inspector + Patch Manager; Backup vault lock and audit manager; Detective for investigation; Firewall Manager policies.
  - Read: IAM Access Analyzer https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html · GuardDuty https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html · Security Hub automation https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules.html · Macie https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html · S3 Object Lock https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html · Backup Audit Manager https://docs.aws.amazon.com/aws-backup/latest/devguide/aws-backup-audit-manager.html · Security incident response guide https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html

## Task 3.3: Determine a strategy to improve performance

Knowledge of: High-performing systems architectures (auto scaling, instance fleets, placement groups) · Global service offerings (Global Accelerator, CloudFront, edge computing) · Monitoring tool sets (CloudWatch) · SLAs and KPIs

- [ ] Translating business requirements to measurable metrics
- [ ] Testing potential remediation solutions and making recommendations
- [ ] Proposing opportunities for the adoption of new technologies and managed services
- [ ] Assessing solutions and applying rightsizing based on requirements
- [ ] Identifying and examining performance bottlenecks
  - Know how to: placement groups (cluster, spread, partition), EC2 Fleet / Spot Fleet, Auto Scaling mixed instances; CloudFront functions vs Lambda@Edge, origin shield, Global Accelerator; ElastiCache vs DAX; RDS Performance Insights, Enhanced Monitoring; X-Ray service maps; Compute Optimizer and Trusted Advisor performance checks; Graviton migration.
  - Read: Performance efficiency pillar https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html · Placement groups https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html · CloudFront edge functions https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/edge-functions.html · RDS Performance Insights https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html · X-Ray https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html

## Task 3.4: Determine a strategy to improve reliability

Knowledge of: AWS Global Infrastructure · Data replication methods · Scaling methodologies (load balancing, auto scaling) · High availability and resiliency · Disaster recovery methods and tools · Service quotas and limits

- [ ] Understanding application growth and usage trends
- [ ] Evaluating existing architecture to determine areas that are not sufficiently reliable
- [ ] Remediating single points of failure
- [ ] Enabling data replication, self-healing, and elastic features and services
  - Know how to: ELB types (ALB, NLB, GWLB) and cross-zone behaviour; Resilience Hub assessments; Auto Scaling health checks and instance refresh; RDS → Aurora Multi-AZ; ElastiCache cluster mode; SQS buffering; Route 53 ARC zonal shift and zonal autoshift; quota increases via Service Quotas and Trusted Advisor; Builders' Library patterns (shuffle sharding, cells).
  - Read: Resilience Hub https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html · ELB comparison https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/what-is-load-balancing.html · Zonal shift https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.html · Instance refresh https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-refresh.html · Builders' Library https://aws.amazon.com/builders-library/

## Task 3.5: Identify opportunities for cost optimizations

Knowledge of: Cost-conscious architecture choices (Spot Instances, scaling policies, rightsizing) · Price model adoptions (Reserved Instances, Savings Plans) · Networking and data transfer costs · Cost management, alerting, and reporting

- [ ] Analyzing usage reports to identify underutilized and overutilized resources
- [ ] Using AWS solutions to identify unused resources
- [ ] Designing billing alarms based on expected usage patterns
- [ ] Investigating AWS Cost and Usage Reports at a granular level
- [ ] Using tagging for cost allocation and reporting
  - Know how to: Cost Explorer rightsizing recommendations, Trusted Advisor cost checks (idle LB, unassociated EIP, low-utilisation EC2), Compute Optimizer, S3 Storage Lens, CUR in Athena/QuickSight, Budgets alerts and actions, Cost Anomaly Detection, tag policies in Organizations, Savings Plans utilisation and coverage reports.
  - Read: Cost Explorer rightsizing https://docs.aws.amazon.com/cost-management/latest/userguide/ce-rightsizing.html · Trusted Advisor https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html · Cost Anomaly Detection https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html · Tag policies https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html · Querying CUR with Athena https://docs.aws.amazon.com/cur/latest/userguide/cur-query-athena.html
