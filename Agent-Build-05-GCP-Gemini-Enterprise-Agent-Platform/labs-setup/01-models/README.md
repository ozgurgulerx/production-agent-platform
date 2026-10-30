# 01-models — pick the models, prove the project can call them

No deployment step exists on this platform: Gemini models are called by id through the regional or multi-regional endpoint (map B10, A9). What you choose here is the region and the three model ids every lab reads from `.env`.

| `.env` key | Default | Used by | Why this one |
|---|---|---|---|
| `GEMINI_MODEL` | `gemini-3.5-flash` | every agent | the id the Agent Runtime quickstart uses (map C1); GA; available in `europe-west2` |
| `GEMINI_LITE_MODEL` | `gemini-3.5-flash-lite` | G05 judge, G06 tuning base | SFT-capable (map G1); cheapest judge |
| `GEMINI_EMBEDDING_MODEL` | `gemini-embedding-001` | G03 lab 04 memory, G08 | the platform embedding id |

Do not use the 2.5 family; it retired on 20 Oct 2026 (map B10). `gemini-4-argon` (GA 13 Oct 2026) is a drop-in upgrade once you have a baseline; G05 lab 02 compares the two.

## Run
```bash
source ../.venv/bin/activate
python smoke_test.py
```
Expected: three lines, one per model id, each with real text or a dimension count. A `404 NOT_FOUND` on a model id means that id is not served in `GOOGLE_CLOUD_LOCATION`; switch the region to `us-central1` or the multi-region `eu` endpoint and re-run.

## Staging bucket (needed from G03 lab 02)
```bash
gcloud storage buckets create gs://${GOOGLE_CLOUD_PROJECT}-agent-staging --location=${GOOGLE_CLOUD_LOCATION} --uniform-bucket-level-access
```
Put the `gs://` URI in `.env` as `AGENT_RUNTIME_STAGING_BUCKET`. The bucket and the agent must be in the same region (map C1).
