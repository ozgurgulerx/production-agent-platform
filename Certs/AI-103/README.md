# AI-103: Developing AI Apps and Agents on Azure

Credential: **Microsoft Certified: Azure AI Apps and Agents Developer Associate**. Replaces AI-102 (retired 30 Jun 2026 per third-party sources; not confirmed on Microsoft pages). Skills measured as of **16 Apr 2026**. Study guide page `ms.date` 2026-03-31, last updated 2026-10-15. Verified 25 Oct 2026.

## Official links

| What | Link |
|---|---|
| Study guide (blueprint) | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-103 |
| Certification page | https://learn.microsoft.com/en-us/credentials/certifications/azure-ai-apps-and-agents-developer-associate/ |
| Exam page (two ways to prepare) | https://learn.microsoft.com/en-us/credentials/certifications/exams/AI-103#two-ways-to-prepare |
| Practice assessment (AI Skills Navigator, sign-in required) | https://aiskillsnavigator.microsoft.com/credentials/cert-3fb198f57997226a824aa5f52a1a22af9a4597941b2288ed39371c7a9e6bd7c9 |
| Exam sandbox | https://aka.ms/examdemo |
| Instructor-led course AI-103T00 (4 days; learning paths listed there) | https://learn.microsoft.com/en-us/training/courses/ai-103t00 |
| Exam scoring and score reports | https://learn.microsoft.com/en-us/credentials/certifications/exam-scoring-reports |
| Renewal | https://learn.microsoft.com/en-us/credentials/certifications/renew-your-microsoft-certification |

Exam facts from the study guide: passing score 700. "Most questions cover features that are general availability (GA). The exam may contain questions on Preview features if those features are commonly used." Microsoft Learn is available during the exam (third-party reports say 120 minutes; verify on the exam page when booking).

## Blueprint

| # | Domain | Weight | File |
|---|---|---|---|
| 1 | Plan and manage an Azure AI solution | 25–30% | [01-plan-and-manage.md](01-plan-and-manage.md) |
| 2 | Implement generative AI and agentic solutions | 30–35% | [02-genai-and-agents.md](02-genai-and-agents.md) |
| 3 | Implement computer vision solutions | 10–15% | [03-computer-vision.md](03-computer-vision.md) |
| 4 | Implement text analysis solutions | 10–15% | [04-text-analysis.md](04-text-analysis.md) |
| 5 | Implement information extraction solutions | 10–15% | [05-information-extraction.md](05-information-extraction.md) |

Also: [00-exam-logistics.md](00-exam-logistics.md), [06-labs-and-practice.md](06-labs-and-practice.md), [progress.md](progress.md).

## Documentation hubs the study guide points to

- Foundry Tools (formerly Azure AI services) https://learn.microsoft.com/en-us/azure/ai-services/what-are-ai-services
- Microsoft Foundry https://learn.microsoft.com/en-us/azure/foundry/what-is-foundry
- Azure Vision https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview
- Azure AI Video Indexer https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-overview
- Azure Language https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview
- Azure Speech https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview
- Azure AI Search https://learn.microsoft.com/en-us/azure/search/search-what-is-azure-search
- Azure OpenAI in Foundry Models https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure
- Document Intelligence https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview
- Content Understanding https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview

## Naming to carry into the exam

The April 2026 outline says **Microsoft Foundry** (not Azure AI Foundry) and **Foundry Tools** (not Azure AI services). Pages still mix both. Old standalone services (Custom Vision, Language Studio, Image Analysis 4.0 model customisation) are deprecated or retiring and are not in the outline.

## How this folder maps to the repo

| Domain | Already covered in |
|---|---|
| 1 Plan and manage | [F01 Landing Zones](../../Agent-Build-02-Microsoft-Foundry/F02-Landing-Zones-and-Networking/README.md), [F02 SDKs and automated deployment](../../Agent-Build-02-Microsoft-Foundry/F04-Foundry-SDKs-and-Deployment/README.md), [F09 APIM designs](../../Agent-Build-02-Microsoft-Foundry/F09-APIM-AI-Gateway/README.md) |
| 2 GenAI and agents | [F03 Creating agents](../../Agent-Build-02-Microsoft-Foundry/F05-Creating-Agents/README.md), [F04 Agent tooling](../../Agent-Build-02-Microsoft-Foundry/F06-Agent-Tooling-MCP-and-Integration/README.md), [F05 Evals](../../Agent-Build-02-Microsoft-Foundry/F08-Evals-Tracing-and-Release/README.md), [S03 Tools and MCP](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/), [S04 Workflows and harnesses](../../Agent-Build-01-Fundamentals/S04-Agentic-Workflows-and-Harnesses/) |
| 5 Information extraction | [F08 Foundry IQ](../../Agent-Build-02-Microsoft-Foundry/F07-RAG-on-AI-Search/README.md) |
| Reading maps with dated page metadata | [Foundry agents reading map](../../Agent-Build-02-Microsoft-Foundry/reference/reading-map-foundry-agents-2026-10-25.md) |

Domains 3 and 4 (vision, speech, language) have no repo coverage yet; the domain files here are the only material.
