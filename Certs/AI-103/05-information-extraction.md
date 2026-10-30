# Domain 5: Implement information extraction solutions (10–15%)

Objectives verbatim from the 16 Apr 2026 outline. In repo: [F08 Foundry IQ](../../Agent-Build-02-Microsoft-Foundry/F07-RAG-on-AI-Search/README.md) covers knowledge bases and agentic retrieval.

## 5.1 Build retrieval and grounding pipelines

- [ ] Ingest and index content, such as documents, images, audio, and video
  - Know how to: indexer + data source + skillset for blobs; integrated vectorization; multimodal (image verbalization or multimodal embeddings); audio/video via Content Understanding or Video Indexer first, then index the output.
  - Read: Integrated vectorization https://learn.microsoft.com/en-us/azure/search/search-how-to-integrated-vectorization (2026-06-08) · Multimodal search https://learn.microsoft.com/en-us/azure/search/multimodal-search-overview (2026-04-20) · Content Understanding + AI Search RAG tutorial https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/tutorial/build-rag-solution (2026-03-31) · Sample https://github.com/Azure-Samples/azure-ai-search-with-content-understanding-python
- [ ] Configure semantic search, hybrid search, and vector search for grounding
  - Know how to: vector profiles (HNSW, compression), hybrid query with RRF, semantic ranker and captions/answers, query rewrite (preview), filters; agentic retrieval knowledge bases and knowledge sources.
  - Read: Vector search https://learn.microsoft.com/en-us/azure/search/vector-search-overview · Hybrid search https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview · Semantic ranking https://learn.microsoft.com/en-us/azure/search/semantic-search-overview (2026-08-05) · Agentic retrieval https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview (2026-09-16) · Create knowledge base https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base
- [ ] Implement enrichment by using custom or built-in skills for text, images, and layout
  - Know how to: built-in skills (OCR, image analysis, entity recognition, split, embedding, document layout), custom web API skill contract, knowledge store projections, enrichment cache.
  - Read: AI enrichment https://learn.microsoft.com/en-us/azure/search/cognitive-search-concept-intro (2026-06-08) · Skills reference https://learn.microsoft.com/en-us/azure/search/cognitive-search-predefined-skills (2026-06-25) · Custom skill interface https://learn.microsoft.com/en-us/azure/search/cognitive-search-custom-skill-interface (2026-07-28) · Document Layout skill https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-document-intelligence-layout
- [ ] Configure RAG ingestion flow, including documents and using optical character recognition (OCR)
  - Know how to: OCR skill vs Document Intelligence Read/Layout vs Content Understanding markdown output; chunking strategy (Text Split skill, layout-aware); when to use the Read OCR edition (legacy OCR v3.2 not recommended).
  - Read: OCR overview https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/overview-ocr · Document Intelligence Layout https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout (2026-05-01, v4.0 GA) · Chunking in RAG https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents
- [ ] Connect retrieval pipelines directly to workflows and agent tools
  - Know how to: AI Search tool on an agent, Foundry IQ knowledge base as a toolbox tool, file search vector stores, MCP server in front of a search index.
  - Read: AI Search tool https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/ai-search (2026-10-08) · What is Foundry IQ https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq · In repo: F08, F04.

## 5.2 Extract content from documents

- [ ] Extract information by using multimodal pipelines that combine OCR, layout analysis, and field extraction
  - Know how to: Document Intelligence v4.0 (Read, Layout, prebuilt and custom extraction models) vs Content Understanding analyzers; confidence, bounding regions, tables, selection marks.
  - Read: Document Intelligence overview https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/overview (2026-09-08; v3.0 retiring 2029) · Layout model https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/layout · Content Understanding document overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/document/overview (2026-08-04)
- [ ] Produce clean, grounded representations to use with agents and RAG by using Content Understanding
  - Know how to: analyzer returns markdown plus fields with source grounding; feed markdown to chunker; keep `source` spans for citations.
  - Read: Content Understanding overview https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/overview · RAG tutorial https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/tutorial/build-rag-solution
- [ ] Implement analyzers for generating structured or markdown outputs for downstream reasoning by using Content Understanding
  - Know how to: prebuilt analyzers (invoice, receipt, layout) vs custom analyzer with field schema (extract / generate / classify methods), standard vs pro mode, API version choice (GA `2025-11-01`).
  - Read: Prebuilt analyzers https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/prebuilt-analyzers (2026-01-29) · Quickstart REST/Python https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/quickstart/use-rest-api · Content Understanding toolkit (schemas) https://github.com/Azure/content-understanding-toolkit
