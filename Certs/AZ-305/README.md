# AZ-305: Designing Microsoft Azure Infrastructure Solutions

Credential: **Microsoft Certified: Azure Solutions Architect Expert**. Prerequisite certification: Azure Administrator Associate (AZ-104). Skills measured as of **17 Apr 2026**. Passing score 700. Verified 25 Oct 2026.

## Official links

| What | Link |
|---|---|
| Study guide (blueprint) | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-305 |
| Certification page | https://learn.microsoft.com/en-us/credentials/certifications/azure-solutions-architect/ |
| Exam page | https://learn.microsoft.com/en-us/credentials/certifications/exams/az-305 |
| Free practice assessment | https://learn.microsoft.com/en-us/credentials/certifications/exams/az-305/practice/assessment?assessment-type=practice&assessmentId=15 |
| Exam sandbox | https://aka.ms/examdemo |
| Learning path: Architect infrastructure operations in Azure | https://learn.microsoft.com/en-us/training/paths/architect-infrastructure-operations/ |
| Course AZ-305T00 | https://learn.microsoft.com/en-us/training/courses/az-305t00 |
| Exam Readiness Zone (AZ-305 episodes) | https://learn.microsoft.com/en-us/shows/exam-readiness-zone/?terms=AZ-305 |
| Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/ |
| Browse Azure architectures | https://learn.microsoft.com/en-us/azure/architecture/browse/ |

## Blueprint

| # | Domain | Weight | File |
|---|---|---|---|
| 1 | Design identity, governance, and monitoring solutions | 25–30% | [01-identity-governance-monitoring.md](01-identity-governance-monitoring.md) |
| 2 | Design data storage solutions | 20–25% | [02-data-storage.md](02-data-storage.md) |
| 3 | Design business continuity solutions | 15–20% | [03-business-continuity.md](03-business-continuity.md) |
| 4 | Design infrastructure solutions | 30–35% | [04-infrastructure.md](04-infrastructure.md) |

Plus [progress.md](progress.md).

## Frameworks every answer leans on

- Azure Well-Architected Framework https://learn.microsoft.com/en-us/azure/well-architected/
- Cloud Adoption Framework https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/
- Azure landing zones https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/
- Choose a compute service https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/compute-decision-tree
- Choose a data store https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-overview
- Choose a messaging service https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging
- Choose a load balancer https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview

## Exam style

Case studies plus "recommend a solution" items. Each question names constraints (cost, RTO/RPO, residency, minimal admin effort). The answer is the cheapest managed service that meets every stated constraint. Practise reading for the word that eliminates options.

In repo: [F01 Landing Zones](../../Agent-Build-02-Microsoft-Foundry/F02-Landing-Zones-and-Networking/README.md) is an AI-specific instance of the governance and network design here.
