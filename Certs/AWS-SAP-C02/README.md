# AWS Certified Solutions Architect – Professional (SAP-C02 → SAP-C03)

**Version warning (verified 25 Oct 2026).** The certification page says: "This exam is being updated. Registration for the updated version (SAP-C03) opens October 27, 2026. The last day to take the current exam (SAP-C02) is November 16, 2026." The SAP-C03 guide was not yet published on 25 Oct (the `solutions-architect-professional-03` docs URL returned 404). Unless you sit before 16 Nov 2026, you will take **SAP-C03**. The SAP-C02 outline below is the baseline; re-check the certification page on or after 27 Oct and record the C03 deltas in [sap-c03-delta.md](sap-c03-delta.md). The SAP-C02 "emerging topics" (unscored) already preview the direction: Bedrock Guardrails, AgentCore Identity, Step Functions human approval.

## Official links

| What | Link |
|---|---|
| Certification page (watch for SAP-C03 guide) | https://aws.amazon.com/certification/certified-solutions-architect-professional/ |
| SAP-C02 exam guide (HTML) | https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html |
| In-scope services | https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/sap-02-in-scope-services.html |
| Out-of-scope services | https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/sap-02-out-of-scope-services.html |
| Skill Builder exam prep (SAP-C02) | https://skillbuilder.aws/category/exam-prep/solutions-architect-professional-SAP-C02 |
| Schedule | https://cp.certmetrics.com/amazon/en/schedule/schedule-exam |

Exam facts: 75 questions (65 scored + 10 unscored), 180 minutes, 300 USD, pass 750/1000 scaled, compensatory. Languages: English, Japanese, Korean, Portuguese (Brazil), Simplified Chinese, Spanish (Latin America). Validity 3 years. Out of scope: frontend mobile development, 12-factor methodology, OS internals.

## Blueprint (SAP-C02)

| # | Domain | Weight | File |
|---|---|---|---|
| 1 | Design Solutions for Organizational Complexity | 26% | [01-organizational-complexity.md](01-organizational-complexity.md) |
| 2 | Design for New Solutions | 29% | [02-new-solutions.md](02-new-solutions.md) |
| 3 | Continuous Improvement for Existing Solutions | 25% | [03-continuous-improvement.md](03-continuous-improvement.md) |
| 4 | Accelerate Workload Migration and Modernization | 20% | [04-migration-modernization.md](04-migration-modernization.md) |

Plus [sap-c03-delta.md](sap-c03-delta.md) and [progress.md](progress.md).

## Reference material every domain uses

- AWS Well-Architected Framework https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html (six pillars; read the Reliability and Cost pillars end to end)
- AWS Architecture Center https://aws.amazon.com/architecture/
- AWS Prescriptive Guidance https://docs.aws.amazon.com/prescriptive-guidance/
- Disaster Recovery of Workloads on AWS whitepaper https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html
- Organizing Your AWS Environment Using Multiple Accounts https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html
- Building a Scalable and Secure Multi-VPC AWS Network Infrastructure https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/welcome.html
- AWS Security Reference Architecture https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html
- AWS Migration whitepaper (7 Rs) https://docs.aws.amazon.com/prescriptive-guidance/latest/large-migration-guide/
- AWS Architecture Blog https://aws.amazon.com/blogs/architecture/ · This is My Architecture videos https://aws.amazon.com/architecture/this-is-my-architecture/
- Service FAQs (read for the in-scope list): https://aws.amazon.com/faqs/

## Community (unofficial)

- Tutorials Dojo SAP study path https://tutorialsdojo.com/aws-certified-solutions-architect-professional-exam-guide-study-path-sap-c01-sap-c02/
- Adrian Cantrill SAP-C02 course https://learn.cantrill.io/p/aws-certified-solutions-architect-professional
- Stephane Maarek (Udemy) SAP-C02 https://www.udemy.com/course/aws-solutions-architect-professional/
- Packt SAP-C02 exam guide (Sard, Wadia) ISBN 9781801815079

## Mapping to the Azure track

Same architect questions as AZ-305 with AWS names: Organizations/Control Tower ≈ management groups/landing zones; Transit Gateway ≈ vWAN/hub-spoke; Route 53 routing ≈ Traffic Manager; Elastic Disaster Recovery ≈ Site Recovery; Migration Hub + MGN + DMS ≈ Azure Migrate + DMS. Study the two side by side; the decision logic transfers.
