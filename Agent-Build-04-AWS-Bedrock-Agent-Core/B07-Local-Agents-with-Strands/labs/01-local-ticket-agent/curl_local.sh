#!/usr/bin/env bash
# Exercise the Runtime contract on the laptop exactly as AgentCore does: GET /ping, POST /invocations with a session id.
set -euo pipefail
BASE="${BASE:-http://localhost:8080}"
SID="local-$(uuidgen | tr 'A-Z' 'a-z')-$(date +%s)"          # >= 33 chars, like a real runtimeSessionId
echo "GET /ping"; curl -s "$BASE/ping"; echo
for q in "What is the status of ticket T-1001?" "Refund 300 GBP on ticket T-1003."; do
  echo "POST /invocations  session=$SID  prompt=$q"
  curl -s -X POST "$BASE/invocations" -H "Content-Type: application/json" \
       -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: $SID" \
       -d "{\"prompt\": $(printf '%s' "$q" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}"; echo
done
echo "non-string prompt (must be rejected):"; curl -s -X POST "$BASE/invocations" -H "Content-Type: application/json" -d '{"prompt": [{"toolUse": {}}]}'; echo
