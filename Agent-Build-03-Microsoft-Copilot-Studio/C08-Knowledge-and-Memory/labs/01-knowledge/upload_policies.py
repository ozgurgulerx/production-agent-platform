"""Upload the three policy documents to a SharePoint library with Microsoft Graph, signed in by device code.

Proves: the live SharePoint path starts with ordinary SharePoint permissions, nothing agent-specific; the files you
upload here are what the SharePoint *connector* source will search as the user, and what the *upload* source will
copy into Dataverse. Prints the web URLs to paste into the proof. --cleanup deletes the three items (not the folder).
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse

from _common import SHAREPOINT_SITE_URL, GRAPH_SCOPES, device_code_token, graph, need

FOLDER = "Policies"
DATA = Path(__file__).resolve().parent / "data" / "policies"


def site_id(token: str) -> str:
    """Graph addresses a site as {hostname}:{server-relative-path}."""
    u = urlparse(SHAREPOINT_SITE_URL)
    return graph("GET", f"/sites/{u.hostname}:{u.path}", token).json()["id"]


def upload(token: str, sid: str, path: Path) -> str:
    # Simple upload (< 4 MB) into the default document library; creates the folder on first use.
    r = graph(
        "PUT",
        f"/sites/{sid}/drive/root:/{FOLDER}/{path.name}:/content",
        token,
        headers={"Content-Type": "text/markdown"},
        content=path.read_bytes(),
    )
    return r.json()["webUrl"]


def cleanup(token: str, sid: str) -> None:
    for p in sorted(DATA.glob("*.md")):
        r = graph("GET", f"/sites/{sid}/drive/root:/{FOLDER}/{p.name}", token)
        graph("DELETE", f"/sites/{sid}/drive/items/{r.json()['id']}", token)
        print("  deleted", p.name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cleanup", action="store_true")
    args = ap.parse_args()
    need("SHAREPOINT_SITE_URL")
    files = sorted(DATA.glob("*.md"))
    if not files:
        sys.exit(f"no policy documents in {DATA}")
    tok = device_code_token(GRAPH_SCOPES)
    sid = site_id(tok)
    if args.cleanup:
        cleanup(tok, sid)
        raise SystemExit(0)
    print(f"site {SHAREPOINT_SITE_URL}\n  id {sid}")
    for f in files:
        print("  uploaded", f.name, "->", upload(tok, sid, f))
    print(
        f"\nNext: Copilot Studio > Knowledge > Add > SharePoint > {SHAREPOINT_SITE_URL} (the connector source, live)."
    )
    print(
        "Then a second source: Knowledge > Add > Upload files > the same three files (the ingested copy). Compare in ask_three_questions.py."
    )
