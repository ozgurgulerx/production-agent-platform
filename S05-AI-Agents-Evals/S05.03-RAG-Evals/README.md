# S05.03: RAG Evals

Status: **Planned** (scope only; built with S06).

Retrieval quality (recall@k, precision@k, MRR/nDCG against labelled relevant chunks), answer quality (faithfulness to retrieved evidence, correctness against gold answers, citation accuracy), and context cost (tokens of retrieved evidence per answer). Separate retrieval failures from generation failures: a wrong answer with the right chunks retrieved is a different bug from a wrong answer because the chunks were missing.

[Back to S05](../README.md)
