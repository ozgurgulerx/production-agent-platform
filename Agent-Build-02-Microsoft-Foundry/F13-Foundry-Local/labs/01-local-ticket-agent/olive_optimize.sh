#!/usr/bin/env bash
# Bring your own model: Hugging Face -> ONNX INT4 -> Foundry Local cache. Learn 2026-05-29 shape (`olive optimize`).
set -euo pipefail
MODEL="${1:-Qwen/Qwen2.5-0.5B-Instruct}"; OUT="models/qwen-int4"
pip install -q olive-ai transformers onnxruntime-genai
olive optimize --model_name_or_path "$MODEL" --trust_remote_code --output_path "$OUT" \
  --device cpu --provider CPUExecutionProvider --precision int4 --log_level 1
printf '{"Name": "qwen2.5-local:1"}\n' > "$OUT/model/inference_model.json" 2>/dev/null || printf '{"Name": "qwen2.5-local:1"}\n' > "$OUT/inference_model.json"
foundry cache cd models && foundry cache list
echo "Run it:  foundry run qwen2.5-local   (the Olive CLI changes; see github.com/microsoft/olive-recipes if flags drift)"
