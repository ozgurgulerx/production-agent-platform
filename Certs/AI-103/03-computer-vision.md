# Domain 3: Implement computer vision solutions (10–15%)

Objectives verbatim from the 16 Apr 2026 outline. No repo coverage yet. The outline is generative-first: image/video generation, multimodal understanding, Content Understanding. Classic Image Analysis 4.0 is deprecated (retires 25 Sep 2028) and Custom Vision is not in scope.

## 3.1 Design and implement image- and video-generation solutions

- [ ] Implement a solution that generates images from text prompts and reference media
  - Know how to: deploy GPT-Image-2 class models (GA; dall-e-3 retired 4 Mar 2026), call the images API with prompt and reference images, size/quality/format parameters.
  - Read: Image generation models https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/dall-e (2026-04-17)
- [ ] Implement a solution that generates videos from text prompts and reference media
  - Know how to: Sora 2 (preview) job flow: create job, poll, download; limits on duration and resolution.
  - Read: Sora 2 video generation (preview) https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/video-generation (2026-03-18)
- [ ] Configure image-editing workflows, including inpainting, mask‑based edits, and prompt‑driven modifications
  - Know how to: edits endpoint with mask image, prompt-only edits, multi-image composition.
  - Read: same image generation page, "edit" section https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/dall-e
- [ ] Implement workflows to edit generated videos
  - Know how to: remix / extend operations on Sora 2 jobs where offered; otherwise re-generate with reference video.
  - Read: Sora 2 page https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/video-generation
- [ ] Select and apply appropriate generation and editing controls provided by the platform
  - Know how to: content filters on image models, watermark/C2PA provenance, output format, moderation level, limited-access registration.
  - Read: Responsible AI for Azure OpenAI https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/overview

## 3.2 Design and implement multimodal understanding workflows

- [ ] Build a solution that analyzes visual context by using multimodal models
  - Know how to: image input via Responses/Chat API (URL or base64), detail level, multiple images per turn.
  - Read: Vision-enabled chat models https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/gpt-with-vision (2026-07-29)
- [ ] Configure apps to produce concise or detailed captions for single or multiple images
  - Know how to: prompt a multimodal model for short vs long captions; Image Analysis 4.0 caption/dense captions as the legacy path (region limited, deprecated).
  - Read: Image captions (Image Analysis 4.0) https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/concept-describe-images-40
- [ ] Implement a solution that enables question‑answering grounded in visual evidence
  - Know how to: visual QA prompt with structured output; combine with Content Understanding field extraction for grounded fields.
  - Read: Vision chat how-to (above) · Content Understanding image overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/image/overview (2026-03-31)
- [ ] Configure generation of alt‑text and extended image descriptions aligned to accessibility guidelines
  - Know how to: WCAG 1.1.1 non-text content: short alt (≤ ~125 chars), long description when informative, decorative images empty alt.
  - Read: WCAG 2.2 Understanding 1.1.1 https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html · W3C alt decision tree https://www.w3.org/WAI/tutorials/images/decision-tree/
- [ ] Implement visual understanding by configuring Azure Content Understanding in Foundry Tools to extract visual characteristics
  - Know how to: create an image analyzer with a field schema, run analyze, read confidence and grounding.
  - Read: Content Understanding overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview (2026-09-15; GA API `2025-11-01`, preview `2026-06-01-preview`) · Image overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/image/overview · Quickstart REST/Python https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/quickstart/use-rest-api
- [ ] Implement video analysis workflows to process and interpret video segments
  - Know how to: Content Understanding video analyzer (preview): segmentation, per-segment fields, transcript; Video Indexer for insights at scale.
  - Read: Content Understanding video overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/video/overview (2026-03-23, preview) · Video Indexer overview https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-overview (2026-09-11)
- [ ] Configure single‑task and pro‑mode Content Understanding pipelines
  - Know how to: standard (single document/image, single analyzer) vs pro mode (multi-document reasoning, reference data); cost and latency difference.
  - Read: Content Understanding overview "modes" section https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview · Document overview (agentic mode preview) https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/document/overview (2026-08-04)
- [ ] Implement solutions that identify objects, components, or regions within images or video
  - Know how to: ask a multimodal model for bounding boxes via structured output; Image Analysis 4.0 object detection as legacy; Content Understanding region fields.
  - Read: Object detection (Image Analysis 4.0) https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/concept-object-detection-40 · Image Analysis overview (deprecation notice) https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-image-analysis

## 3.3 Implement responsible AI for multimodal content

- [ ] Implement filters to classify unsafe or disallowed visual content
  - Know how to: Content Safety image analysis (four harm categories, severity), multimodal text+image analysis, guardrails on image generation deployments.
  - Read: Content Safety image quickstart https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-image · Harm categories https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/harm-categories
- [ ] Detect and mitigate indirect prompt injection by using embedded text in images
  - Know how to: Prompt Shields for documents on OCR'd image text, spotlighting (preview), treat image text as untrusted data in the system prompt.
  - Read: Prompt Shields (Content Safety) https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection (2026-08-28) · Prompt Shields in Foundry https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/content-filter-prompt-shields · In repo: [S03.06 Client as trust boundary](../../Agent-Build-01-Fundamentals/S03-AI-Agents-Tools-and-MCP/S03.06-Client-as-Trust-Boundary/README.md)
- [ ] Enforce visual policy rules, such as applying watermarks, flagging prohibited symbols, upholding brand usage requirements, and detecting potentially inappropriate content
  - Know how to: Content Safety custom categories (preview) for brand/symbol rules, C2PA credentials on generated images, post-processing watermark step, protected-material detection.
  - Read: Content Safety overview (custom categories, protected material) https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview · Content credentials in Azure OpenAI https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/content-credentials
