# AI-103 labs, learning paths and practice

## Official

- **Course AI-103T00** (4 days) https://learn.microsoft.com/en-us/training/courses/ai-103t00 — learning paths it bundles (IDs from the course page): `develop-generative-ai-apps`, `develop-ai-agents-azure`, `develop-language-solutions-azure-ai`, `extract-insights-visual-data-azure`. Browse them at https://learn.microsoft.com/en-us/training/browse/?terms=AI-103
- **Practice assessment** (AI Skills Navigator): https://aiskillsnavigator.microsoft.com/credentials/cert-3fb198f57997226a824aa5f52a1a22af9a4597941b2288ed39371c7a9e6bd7c9
- **Exam sandbox**: https://aka.ms/examdemo
- **Exam Readiness Zone videos**: https://learn.microsoft.com/en-us/shows/exam-readiness-zone/?terms=AI-103 (check whether AI-103 episodes exist; AI-102 ones still apply to Foundry Tools topics)
- **Foundry samples** (official): https://github.com/microsoft-foundry/foundry-samples
- **Content Understanding toolkit**: https://github.com/Azure/content-understanding-toolkit
- **Foundry devblog** (what's new, GA announcements): https://devblogs.microsoft.com/foundry/
- **What's new in Foundry**: https://learn.microsoft.com/en-us/azure/foundry/whats-new-foundry

The MicrosoftLearning lab repo for AI-103 was not found on 25 Oct 2026 (`mslearn-ai-103` and `mslearn-ai-apps-agents` both 404). The AI-102 labs still exist and cover the Foundry Tools half: https://github.com/MicrosoftLearning/mslearn-ai-services

## Community (unofficial, check against the official outline)

- tpriyadata, 500+ scenario questions, Python SDK code https://github.com/tpriyadata/microsoft-ai-103-study-guide
- Howard Ginsburg community study guide https://howardginsburg.github.io/MicrosoftStudyGuides/AI-103.html
- GetHandsOn cheat sheet (commercial) https://gethandson.ai/blog/ai-103-study-guide-azure-ai-foundry
- sifatnotes https://github.com/sifatnotes/Microsoft-AI-103-Study-Guide-Azure-AI-Apps-and-Agents-Developer-Associate
- emmaRose2525 https://github.com/emmaRose2525/Microsoft-AI-103-Azure-AI-Apps-and-Agents-Study-Guide

## Hands-on checklist (things to have actually done before sitting)

- [ ] Standard agent setup with BYO VNet, private endpoints, and a hosted agent deployed via azd
- [ ] Prompt agent with file search + AI Search tool + MCP tool, traced in App Insights, evaluated with agent evaluators
- [ ] A2A call between two Foundry agents with agent identity auth
- [ ] Agent Framework workflow with human-in-the-loop checkpoint, hosted as one hosted agent
- [ ] Model router deployment and a cost/quality comparison run
- [ ] Image generation + edit with mask; one Sora 2 job
- [ ] Content Understanding custom analyzer (document) and one image analyzer; feed markdown into an AI Search index with integrated vectorization
- [ ] Voice Live or voice prompt agent round trip; one custom speech model
- [ ] Translator text API and document translation
- [ ] Content Safety: Prompt Shields on image-embedded text, custom category, groundedness detection
- [ ] Quota increase request and APIM token-limit policy in front of a deployment
