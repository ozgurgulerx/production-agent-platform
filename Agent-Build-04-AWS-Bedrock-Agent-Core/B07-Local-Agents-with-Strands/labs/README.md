# B07 labs — local agents with Strands

No AWS needed for the local rows. Shared venv from [`../../labs-setup/`](../../labs-setup/) plus `pip install "strands-agents[ollama]"` (the `ollama` client is not in the pinned requirements on purpose; it is a B07-only dependency).

```
labs/
└── 01-local-ticket-agent/   B03's agent on Ollama or llama.cpp; the Runtime contract on 8080 without AWS; GGUF quant script
```

| Lab | Chapter section | Needs |
|---|---|---|
| 01 | §2 provider swap, §3 contract locally, §4 quantisation, §6 what you own | Ollama installed, one model pulled (~5 GB for `qwen3:8b`, ~13 GB for `gpt-oss:20b`) |
