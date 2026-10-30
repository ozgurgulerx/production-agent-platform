"""Untested sketch. One SFT training line in each of the three shapes from README §3 (map G3).
Runnable: python jsonl_shapes.py   prints three JSONL lines. Proof lab: ../labs/01-sft-ticket-tone/.

Shape per map G3: {"systemInstruction":{"parts":[{"text":...}]}, "contents":[{"role":"user"|"model","parts":[...]}]};
optional "tools"; optional "fileData". The function-call part layout inside a "model" turn is the Gemini
Content layout; its exact field names are not in the map and are marked unverified below.
"""

import json

SYSTEM = "You are the UK card team's support assistant. Warm, brief, British English, no exclamation marks. Never invent amounts or dates."
Q = "Can I get £300 back on ticket 1042?"
A = "I can't approve that myself: refunds above £250 need a second approver. I've flagged it; you'll hear back within 4 business hours."

# 1. Plain contents: the style is in the model turn alone.
PLAIN = {
    "contents": [
        {"role": "user", "parts": [{"text": Q}]},
        {"role": "model", "parts": [{"text": A}]},
    ]
}

# 2. With systemInstruction: serve with the same instruction or you evaluate something you did not train.
WITH_SYSTEM = {
    "systemInstruction": {"parts": [{"text": SYSTEM}]},
    "contents": PLAIN["contents"],
}

# 3. With tools: the model turn calls get_ticket first, then answers in the new tone.
#    "tools" is optional per G3; functionCall/functionResponse part names unverified against the tuning page.
WITH_TOOLS = {
    "systemInstruction": {"parts": [{"text": SYSTEM}]},
    "tools": [
        {
            "functionDeclarations": [
                {
                    "name": "get_ticket",
                    "description": "Look up a support ticket",
                    "parameters": {
                        "type": "object",
                        "properties": {"ticket_id": {"type": "string"}},
                        "required": ["ticket_id"],
                    },
                }
            ]
        }
    ],
    "contents": [
        {"role": "user", "parts": [{"text": Q}]},
        {
            "role": "model",
            "parts": [
                {"functionCall": {"name": "get_ticket", "args": {"ticket_id": "1042"}}}
            ],
        },
        {
            "role": "user",
            "parts": [
                {
                    "functionResponse": {
                        "name": "get_ticket",
                        "response": {"status": "open", "amount_gbp": 120.0},
                    }
                }
            ],
        },
        {"role": "model", "parts": [{"text": A}]},
    ],
}

if __name__ == "__main__":
    for name, row in (
        ("plain", PLAIN),
        ("with systemInstruction", WITH_SYSTEM),
        ("with tools", WITH_TOOLS),
    ):
        print(f"# {name}")
        print(json.dumps(row, ensure_ascii=False))
    print(
        "# limits (map G2): 131,072 tokens per example, 1 GB per file, <=5,000 validation rows; start at 100 rows (G3)"
    )
