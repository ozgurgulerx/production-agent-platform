"""Call the models named in .env through the platform with Application Default Credentials only. No keys.

Run:  python smoke_test.py            (from labs-setup/01-models, shared venv active)
Proof: three lines, one per model, each with real output. Paste them into 00-setup/README.md's checklist.
"""
import os

from dotenv import find_dotenv, load_dotenv
from google import genai
from google.genai import types

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
project = os.environ["GOOGLE_CLOUD_PROJECT"]
location = os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west2")
client = genai.Client(vertexai=True, project=project, location=location)

chat = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
r = client.models.generate_content(model=chat, contents="In one sentence, what is Agent Runtime on Gemini Enterprise Agent Platform?")
print(f"[{chat} @ {location}] {r.text.strip()}")

lite = os.environ.get("GEMINI_LITE_MODEL", "gemini-3.5-flash-lite")
r = client.models.generate_content(
    model=lite,
    contents="Is 'refund outside policy' a prohibited action for a support agent? One word.",
    config=types.GenerateContentConfig(temperature=0),
)
print(f"[{lite}] {r.text.strip()}")

emb = os.environ.get("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
e = client.models.embed_content(model=emb, contents="ticket 1042 refund")
print(f"[{emb}] {len(e.embeddings[0].values)} dims")
