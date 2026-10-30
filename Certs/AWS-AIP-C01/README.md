# AWS Certified Generative AI Developer – Professional (AIP-C01)

Professional-level. Exam guide read 25 Oct 2026 from the AWS Certification docs site (HTML version of the guide).

## Official links

| What | Link |
|---|---|
| Certification page | https://aws.amazon.com/certification/certified-generative-ai-developer-professional/ |
| Exam guide (HTML, domains linked per page) | https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html |
| In-scope services | https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/aip-01-in-scope-services.html |
| Out-of-scope services | https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/aip-01-out-of-scope-services.html |
| Technologies and concepts | https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-technologies-concepts.html |
| Skill Builder exam prep plan (exam-style questions, Official Practice Question Set, Official Pretest, Practice Exam) | https://skillbuilder.aws/category/exam-prep/generative-ai-developer-professional-AIP-C01 |
| Schedule | https://cp.certmetrics.com/amazon/en/schedule/schedule-exam |

Exam facts: 75 questions (65 scored + 10 unscored), 180 minutes, 300 USD, pass at 750/1000 scaled, compensatory scoring, Pearson VUE or online. Languages: English, Japanese, Korean, Simplified Chinese. Target candidate: 2+ years building production apps on AWS, 1 year hands-on GenAI. Out of scope: model development and training, advanced ML techniques, data and feature engineering.

## Blueprint

| # | Domain | Weight | File |
|---|---|---|---|
| 1 | Foundation Model Integration, Data Management, and Compliance | 31% | [01-fm-integration-data-compliance.md](01-fm-integration-data-compliance.md) |
| 2 | Implementation and Integration | 26% | [02-implementation-integration.md](02-implementation-integration.md) |
| 3 | AI Safety, Security, and Governance | 20% | [03-safety-security-governance.md](03-safety-security-governance.md) |
| 4 | Operational Efficiency and Optimization for GenAI Applications | 12% | [04-operations-optimization.md](04-operations-optimization.md) |
| 5 | Testing, Validation, and Troubleshooting | 11% | [05-testing-troubleshooting.md](05-testing-troubleshooting.md) |

Plus [progress.md](progress.md). Every skill statement in the guide ends with "(for example, by using …)" naming services; those service names are the exam's vocabulary, so the domain files keep them.

## Core documentation hubs

- Amazon Bedrock user guide https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html
- Bedrock AgentCore https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html
- Bedrock Knowledge Bases https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html
- Bedrock Guardrails https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html
- Bedrock Prompt Management and Flows https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-management.html · https://docs.aws.amazon.com/bedrock/latest/userguide/flows.html
- Bedrock model evaluation https://docs.aws.amazon.com/bedrock/latest/userguide/model-evaluation.html
- Strands Agents SDK https://strandsagents.com/latest/
- Agent Squad (multi-agent) https://github.com/awslabs/agent-squad
- SageMaker AI https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html
- OpenSearch Service vector search https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html
- Well-Architected Generative AI Lens https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html
- AWS Machine Learning Blog (GenAI category) https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/generative-ai/
- Amazon Bedrock samples https://github.com/aws-samples/amazon-bedrock-samples · AgentCore samples https://github.com/awslabs/amazon-bedrock-agentcore-samples

## Community (unofficial)

- Tutorials Dojo study path https://tutorialsdojo.com/aws-certified-generative-ai-developer-professional-study-path/
- KodeKloud study guide https://kodekloud.com/blog/the-complete-aws-certified-generative-ai-developer-professional-aip-c01-study-guide/

## Mapping to the Azure track

Same patterns, different names: Bedrock ≈ Foundry Models; AgentCore Runtime/Gateway/Identity/Memory ≈ Agent Service hosted agents, toolbox, agent identity, memory; Knowledge Bases ≈ Foundry IQ / AI Search; Guardrails ≈ Guardrails/Content Safety; Prompt Flows ≈ Agent Framework workflows. Reuse [S03](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/) and [S04](../../Agent-Build-01-Fundamentals/S04-Agentic-Workflows-and-Harnesses/) for the vendor-neutral parts.
