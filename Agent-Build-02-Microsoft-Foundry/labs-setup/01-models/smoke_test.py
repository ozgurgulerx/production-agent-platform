"""Call every deployment named in .env with Entra auth only. No keys.

Run:  python smoke_test.py            (from labs-setup/01-models, shared venv active)
"""
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(usecwd=True))  # .env at the track root (walks up)
account = os.environ["FOUNDRY_ACCOUNT_NAME"]
token = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")
client = OpenAI(base_url=f"https://{account}.openai.azure.com/openai/v1/", api_key=token)

chat = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")
r = client.responses.create(model=chat, input="In one sentence, what is a deployment type in Foundry?")
print(f"[{chat}] {r.output_text.strip()}")

reasoning = os.environ.get("FOUNDRY_REASONING_MODEL", chat)
r = client.responses.create(model=reasoning, reasoning={"effort": "low"}, input="Is 'refund outside policy' a prohibited action for a support agent? One word.")
print(f"[{reasoning} reasoning=low] {r.output_text.strip()}")

emb = os.environ.get("FOUNDRY_EMBEDDING_MODEL", "text-embedding-3-small")
e = client.embeddings.create(model=emb, input="ticket 1042 refund")
print(f"[{emb}] {len(e.data[0].embedding)} dims")

voice = os.environ.get("FOUNDRY_VOICE_MODEL", "gpt-realtime")
print(f"[{voice}] realtime: exercised in F03 lab 01 way 3, not here")
