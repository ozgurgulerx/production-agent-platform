# Domain 4: Implement text analysis solutions (10–15%)

Objectives verbatim from the 16 Apr 2026 outline. No repo coverage yet. Note the retirements: sentiment, summarization and other Azure Language legacy features retire 31 Mar 2029; Language Studio retires 20 Mar 2027. The outline pairs each task with "generative prompting and Foundry Tools", so know both paths.

## 4.1 Apply language model text analysis

- [ ] Implement solutions to extract entities, topics, summaries, and structured JSON outputs by using generative prompting and Foundry Tools
  - Know how to: structured outputs with a JSON schema on a GPT model; Azure Language NER, key phrases, summarization (extractive/abstractive, conversation) via SDK; when the prebuilt tool beats a prompt (cost, determinism, PII compliance).
  - Read: Structured outputs https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs (2026-08-24) · Azure Language overview https://learn.microsoft.com/en-us/azure/ai-services/language-service/overview (2026-07-21) · NER https://learn.microsoft.com/en-us/azure/ai-services/language-service/named-entity-recognition/overview · Summarization (retiring 2029) https://learn.microsoft.com/en-us/azure/ai-services/language-service/summarization/overview · Custom NER https://learn.microsoft.com/en-us/azure/ai-services/language-service/custom-named-entity-recognition/overview
- [ ] Configure detection of sentiment, tone, safety issues, and sensitive content
  - Know how to: sentiment and opinion mining (retiring 2029) vs prompting; PII detection and redaction (text, conversation, document PII); Content Safety text analysis and groundedness; blocklists.
  - Read: Sentiment analysis https://learn.microsoft.com/en-us/azure/ai-services/language-service/sentiment-opinion-mining/overview · PII detection https://learn.microsoft.com/en-us/azure/ai-services/language-service/personally-identifiable-information/overview · Content Safety text https://learn.microsoft.com/en-us/azure/ai-services/content-safety/quickstart-text · Groundedness detection https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness
- [ ] Build solutions that translate text by using Azure Translator in Foundry Tools or LLM‑powered translation flows
  - Know how to: Translator text API (GA release 2026-06-06), custom translator, document translation; LLM translation with glossary in prompt; when each fits.
  - Read: Translator overview https://learn.microsoft.com/en-us/azure/ai-services/translator/overview (2026-05-14) · Text translation https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/overview (2026-06-02) · Document translation https://learn.microsoft.com/en-us/azure/ai-services/translator/document-translation/overview
- [ ] Customize language model outputs for domain tasks, such as compliance summarization and domain extraction
  - Know how to: system prompt + few-shot + schema first; fine-tuning (SFT) when style/format must be learned; custom NER / custom text classification in Language; evaluation set before and after.
  - Read: Fine-tuning in Foundry https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/fine-tuning (2026-10-05) · Prompt engineering https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/prompt-engineering · Custom text classification https://learn.microsoft.com/en-us/azure/ai-services/language-service/custom-text-classification/overview · In repo: [F06 Fine-tuning](../../Agent-Build-02-Microsoft-Foundry/F12-Fine-Tuning-and-Model-Routing/README.md)

## 4.2 Implement speech solutions

- [ ] Implement workflows to convert speech to text and text to speech for agentic interactions
  - Know how to: Speech SDK STT (real-time, batch, fast transcription), TTS neural voices and SSML; Voice Live API for low-latency agent voice; voice prompt agent (preview) in Agent Service.
  - Read: Speech overview https://learn.microsoft.com/en-us/azure/ai-services/speech-service/overview (2026-10-02) · Speech to text https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-to-text · Text to speech https://learn.microsoft.com/en-us/azure/ai-services/speech-service/text-to-speech · Voice Live API https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live (2026-10-08) · Voice prompt agent quickstart (preview) https://learn.microsoft.com/en-us/azure/foundry/agents/quickstarts/prompt-voice-agent (2026-10-06)
- [ ] Integrate speech as an agent modality, including custom speech models
  - Know how to: custom speech (acoustic/language adaptation, pronunciation), custom neural voice (limited access), plugging a custom speech model into Voice Live.
  - Read: Custom speech overview https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-speech-overview (2026-02-25) · Custom neural voice https://learn.microsoft.com/en-us/azure/ai-services/speech-service/custom-neural-voice · Voice Live how-to https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live-how-to
- [ ] Enable multimodal reasoning from audio inputs
  - Know how to: send audio to gpt-realtime / audio-capable models through the Responses or Realtime API; when to transcribe first vs native audio.
  - Read: Realtime audio reference https://learn.microsoft.com/en-us/azure/ai-foundry/openai/realtime-audio-reference · Voice Live models table https://learn.microsoft.com/en-us/azure/ai-services/speech-service/voice-live
- [ ] Translate speech into other languages by using language models and Foundry Tools
  - Know how to: speech translation SDK (multi-target, live interpreter), Voice Live with translation, LLM translation after STT.
  - Read: Speech translation https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-translation (2026-02-25) · Translator overview https://learn.microsoft.com/en-us/azure/ai-services/translator/overview
