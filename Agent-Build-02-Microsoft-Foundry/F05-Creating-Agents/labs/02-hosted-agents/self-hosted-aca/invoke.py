"""Call the self-hosted agent with a plain OpenAI client. Same wire format as a Foundry-hosted
agent; the only difference is the base URL (and whatever auth YOU put in front of it).
Usage: python invoke.py https://<fqdn>   |   python invoke.py http://localhost:8088
"""
import sys

from openai import OpenAI

base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8088"
client = OpenAI(base_url=base, api_key="not-used-by-this-host")
r1 = client.responses.create(input="Where do you run, and what is the status of ticket 8841?")
print(r1.output_text)
r2 = client.responses.create(input="Repeat the ticket id you just looked up.", previous_response_id=r1.id)
print(r2.output_text)
