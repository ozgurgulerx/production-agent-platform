# 00-setup — tooling, scripts, proof checklist

## Tooling on this machine (checked 25 Oct 2026)
| Tool | Need | Install |
|---|---|---|
| `gcloud` | ≥ 584 | present |
| Python | 3.11+ (3.13 preferred) | `brew install python@3.13` |
| Terraform | ≥ 1.5 for G01/G02 IaC | `brew install terraform` (not installed today) |
| MCP Toolbox | 1.15.0 for G04 lab 03 | `brew install mcp-toolbox` |
| Ollama | any, for G07 | present |
| Gemini CLI | 0.65 for G04 lab 02 client test | present |

## Scripts
| Script | Does |
|---|---|
| `scripts/bootstrap_venv.sh` | creates `labs-setup/.venv`, installs `requirements.txt` |
| `scripts/enable_apis.sh` | enables the 14 APIs the labs need (map I6 plus Discovery Engine, Run, Secret Manager, Model Armor) |
| `scripts/verify.sh` | prints `OK` or the first thing that is wrong |

## Identity: who runs the labs
Local scripts use **your** Application Default Credentials (`gcloud auth application-default login`). Deployed agents use **Agent Identity** when `identity_type=AGENT_IDENTITY` is set, otherwise a service account (map C5). Grant yourself, once:
```bash
P=$GOOGLE_CLOUD_PROJECT; ME=$(gcloud config get-value account)
for r in roles/aiplatform.user roles/aiplatform.agentContextEditor roles/aiplatform.agentDefaultAccess roles/storage.admin roles/iam.serviceAccountUser roles/run.admin roles/secretmanager.admin roles/discoveryengine.admin; do
  gcloud projects add-iam-policy-binding $P --member="user:$ME" --role="$r" --condition=None >/dev/null
done
```
The Agent Runtime service agent `service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com` is created on first deploy and needs `roles/artifactregistry.reader` for custom images (map I6, I8).

## Proof checklist (tick with real output, not intent)
- [ ] `bash scripts/bootstrap_venv.sh` ends with `Ready: .venv (Python 3.1x)`
- [ ] `gcloud auth application-default print-access-token` prints a token
- [ ] `bash scripts/enable_apis.sh` ends with `Done.`
- [ ] `bash scripts/verify.sh` prints `OK`
- [ ] `python ../01-models/smoke_test.py` prints three model lines
- [ ] `.env` has `AGENT_RUNTIME_STAGING_BUCKET` and the bucket exists in the same region

Status on 25 Oct 2026: scaffold only, functionality unverified. On this machine ADC was missing and no AI APIs were enabled, so the first run will exercise every step above.
