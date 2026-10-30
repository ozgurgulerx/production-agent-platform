# F07 capability builds — Search, document ingestion and RAG

## Build contract

Status: **planned; functionality unverified**. Build one capability at a time using the existing module and labs. Record environment/dependency versions, permitted assistance, positive and negative results, and trace/test evidence. The learner writes code and tests; these contracts do not supply hidden implementations. Verify dated API and availability claims before execution.

### Document and multimodal ingestion

- [ ] Build: Build PDF-to-layout/Markdown-to-chunks with stable source/page citations. Compare integrated vectorization with custom push ingestion; use Content Understanding analyzers and OCR/field extraction where applicable. Extend one pipeline to image/audio/video-derived content.
- [ ] Verify: Inject corrupt files, partial extraction and missing fields; inspect indexer errors and assert ingestion success before querying. Keep lineage and incremental delete semantics.

### Retrieval benchmark

- [ ] Build: Create a versioned labeled query set and compare vector-only, hybrid BM25/vector/RRF and semantic reranking. Configure filters and measure recall@k, groundedness, correctness, p95 and embedding cost using the same corpus.
- [ ] Verify: Include no-answer and ambiguous queries; report sample size and judge limits. Compare Foundry IQ/agentic retrieval with explicit Search index access rather than assuming they are interchangeable.

### Access, freshness and index lifecycle

- [ ] Build: Enforce document permissions before context construction; partition caches by access context. Implement permission revocation, source deletion, TTL/freshness and blue-green index replacement.
- [ ] Verify: Prove two-user denial before and after revocation; switch to a new index and roll back without dropping source citations. Test stale or unauthorized documents cannot return through cache.

### Advanced grounding and stores

- [ ] Build: Compare late interaction, RAPTOR and GraphRAG against the baseline with explicit build cost and measurable benefit. Explore Fabric/OneLake/Databricks/SQL grounding and Storage lifecycle/immutability through bounded integration exercises.
- [ ] Verify: Record grants, network boundary, incremental update behavior and failure handling; keep optional extensions separate from the minimum proven RAG path.

## Exact checklist targets

Each ID below is a distinct occurrence in the [full coverage matrix](../reference/production-build-coverage.md). Source wording is retained, including historical names and unfinished placeholders; it is not a fresh API guarantee. Compound items may require several small builds. Mark complete only after recording evidence.

- [ ] **CB068** — Foundry IQ
- [ ] **CB184** — Storage (documents, eval sets),
- [ ] **CB185** — Document Intelligence (ingestion),
- [ ] **CB199** — Ingestion: Document Intelligence layout model, chunking strategies (fixed, semantic, layout-aware, parent-child), integrated vectorisation vs custom pipeline, skillsets vs push API, incremental indexing, index versioning and blue/green reindex.
- [ ] **CB200** — Retrieval: hybrid (vector + BM25 + RRF), semantic ranker, filters and security trimming, query rewriting, multi-index federation, agentic retrieval / knowledge agents in AI Search, reranking with cross-encoders.
- [ ] **CB201** — Evaluation: groundedness, relevance, retrieval recall@k, answer correctness; building the golden set; Foundry evaluators vs promptfoo/RAGAS.
- [ ] **CB202** — Advanced: ColBERT-style late interaction, RAPTOR hierarchical summaries, GraphRAG (community summaries, entity graphs, when it beats vector RAG, cost), permission-aware RAG, freshness and TTL.
- [ ] **CB203** — Numbers to carry: index size vs tier, embedding cost per million tokens, p95 retrieval latency, recall uplift from hybrid vs vector-only on your own set.
- [ ] **CB204** — Ingestion: Document Intelligence layout model, chunking strategies (fixed, semantic, layout-aware, parent-child), integrated vectorisation vs custom pipeline, skillsets vs push API, incremental indexing, index versioning and blue/green reindex.
- [ ] **CB205** — Retrieval: hybrid (vector + BM25 + RRF), semantic ranker, filters and security trimming, query rewriting, multi-index federation, agentic retrieval / knowledge agents in AI Search, reranking with cross-encoders.
- [ ] **CB206** — Evaluation: groundedness, relevance, retrieval recall@k, answer correctness; building the golden set; Foundry evaluators vs promptfoo/RAGAS.
- [ ] **CB207** — Advanced: ColBERT-style late interaction, RAPTOR hierarchical summaries, GraphRAG (community summaries, entity graphs, when it beats vector RAG, cost), permission-aware RAG, freshness and TTL.
- [ ] **CB208** — Numbers to carry: index size vs tier, embedding cost per million tokens, p95 retrieval latency, recall uplift from hybrid vs vector-only on your own set.
- [ ] **CB209** — Document Intelligence custom models, Content Understanding, structured outputs with JSON schema, OCR fallbacks; GCS ad names document extraction/OCR.
- [ ] **CB210** — `SearchClient`, `SearchIndexClient`, `SearchIndexerClient`; index schema (fields, `SearchField` with `vector_search_dimensions` and profile), vector search config (HNSW/exhaustive KNN, vectorizers), semantic configuration, `search(search_text=..., vector_queries=[VectorizedQuery/VectorizableTextQuery], query_type="semantic", filter=..., select=..., top=...)`, hybrid scoring and RRF, `IndexDocumentsBatch` upload/merge, indexers + skillsets + integrated vectorisation, security filters (`search.in(groups, ...)`), scoring profiles, facets, agentic retrieval / knowledge agent APIs (check current preview name).
- [ ] **CB211** — Exercise: build an index with hybrid + semantic, ingest 200 chunks with embeddings, run vector-only vs hybrid vs hybrid+semantic on a 30-question golden set, compute recall@5, print the table. 60 minutes.
- [ ] **CB212** — `DocumentIntelligenceClient.begin_analyze_document("prebuilt-layout", ...)`, output formats (markdown for RAG), tables, paragraphs with roles, figures, page-aware chunking; custom extraction models; Content Understanding (newer) for multimodal. GCS ad: document extraction / OCR.
- [ ] **CB213** — Exercise: PDF → markdown → layout-aware chunks → index, with page citations preserved end to end.
- [ ] **CB214** — Microsoft Fabric (OneLake, Lakehouse, Data Agents, mirroring), Azure Databricks (Unity Catalog, Mosaic AI, Vector Search), Synapse legacy, Cosmos DB (vector search, change feed, session store), Azure SQL / PostgreSQL (pgvector), Purview (classification, lineage, DLP), Text-to-SQL patterns and their guardrails.
- [ ] **CB216** — Upload/download, SAS vs managed identity, lifecycle, immutability (WORM) for audit sets, event-driven ingestion with Event Grid on blob created.
- [ ] **CB217** — Fabric and Databricks hooks — Fabric REST/notebooks, OneLake shortcuts, Databricks SDK and Mosaic AI Vector Search, Unity Catalog grants; enough to read a client's grounding layer.

## Completion evidence

- [ ] Store the artifact path, reproducible command, observed outcome, limitations and next gap in the existing study log.
- [ ] Preserve current labs; link to shared concepts rather than importing another stage’s implementation.
- [ ] Do not label a sample, empty test collection or planned experiment as verified functionality.
