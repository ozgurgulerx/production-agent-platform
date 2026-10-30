"""Call the published ticket agent through Direct Line v3, the way a custom app or Copilot Agent Kit does.

Proves: the Mobile app channel's token endpoint hands out a short-lived Direct Line token without any Entra
app of your own (C10); the conversation is `POST conversations`, `POST activities`, `GET activities?watermark=`.
For an agent with Authenticate with Microsoft the first reply is a sign-in card; use `--no-auth` agents for this proof.
"""
import os
import time

import httpx

from _common import need

TOKEN_ENDPOINT = os.environ.get("DIRECTLINE_TOKEN_ENDPOINT", "")   # Channels > Mobile app > Token endpoint (copy from portal)
DL = "https://directline.botframework.com/v3/directline"


def main() -> None:
    if not TOKEN_ENDPOINT:
        need("DIRECTLINE_TOKEN_ENDPOINT")
    token = httpx.get(TOKEN_ENDPOINT, timeout=30).json()["token"]
    h = {"Authorization": f"Bearer {token}"}
    conv = httpx.post(f"{DL}/conversations", headers=h, timeout=30).json()
    cid = conv["conversationId"]
    print("conversation", cid)
    watermark = None
    for text in ["What does ticket T-2041 say?", "Refund 400 GBP on it."]:
        httpx.post(f"{DL}/conversations/{cid}/activities", headers=h, timeout=30,
                   json={"type": "message", "from": {"id": "lab-user"}, "text": text})
        print(f"\nyou: {text}")
        for _ in range(15):                                   # poll until the agent replies
            time.sleep(1.5)
            url = f"{DL}/conversations/{cid}/activities" + (f"?watermark={watermark}" if watermark else "")
            page = httpx.get(url, headers=h, timeout=30).json()
            watermark = page.get("watermark", watermark)
            replies = [a for a in page.get("activities", []) if a.get("from", {}).get("id") != "lab-user" and a.get("type") == "message"]
            if replies:
                for a in replies:
                    print("agent:", a.get("text"))
                break


if __name__ == "__main__":
    main()
