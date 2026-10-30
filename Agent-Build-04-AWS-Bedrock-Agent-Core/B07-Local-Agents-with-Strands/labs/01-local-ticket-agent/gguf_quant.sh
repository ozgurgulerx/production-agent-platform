#!/usr/bin/env bash
# Bring your own quantised model: Hugging Face -> GGUF F16 -> Q4_K_M -> Ollama. The Olive analogue on this side (F07 §5).
# Described, not run. llama.cpp flags move; check `llama-quantize --help`.
set -euo pipefail
MODEL="${1:-Qwen/Qwen3-8B}"; NAME="$(basename "$MODEL" | tr 'A-Z' 'a-z')"; OUT="models/$NAME"
mkdir -p "$OUT"
pip install -q huggingface_hub
hf download "$MODEL" --local-dir "$OUT/hf"                                  # full-precision safetensors; keep these for Custom Model Import (K7)
python "$(brew --prefix llama.cpp)/share/llama.cpp/convert_hf_to_gguf.py" "$OUT/hf" --outtype f16 --outfile "$OUT/$NAME-f16.gguf"   # verify script path
llama-quantize "$OUT/$NAME-f16.gguf" "$OUT/$NAME-q4_k_m.gguf" Q4_K_M       # per-block scales; ~0.56 bytes/weight
printf 'FROM %s\nPARAMETER temperature 0.2\n' "$OUT/$NAME-q4_k_m.gguf" > "$OUT/Modelfile"
ollama create "$NAME-local" -f "$OUT/Modelfile" && ollama list | grep "$NAME-local"
echo "Run it:  python local_ticket_agent.py --provider ollama --model $NAME-local   then re-run the B05 lab 02 cases before trusting it"
