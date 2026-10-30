"""Create the Agent Search data store and the RAG Engine corpus for the ticket policies, and write the paths to .env.

Run:   python provision_kb.py            (shared venv active, .env filled, PDFs already in POLICY_DOCS_BUCKET)
       python provision_kb.py --delete
Proof: two lines AGENT_SEARCH_DATASTORE=... and RAG_CORPUS=..., then an import operation name.

Map: H9 (data store vocabulary), H11 (RAG Engine regions and vector DBs), B9 (data store path form), I8 (Terraform equivalents).
The client method names are NOT in the reading map; each TODO says what to look up. Do not guess them into "working" code.
"""
import os
import sys

from dotenv import find_dotenv, load_dotenv, set_key

ENV_PATH = find_dotenv(usecwd=True)
load_dotenv(ENV_PATH)

PROJECT = os.environ["GOOGLE_CLOUD_PROJECT"]
BUCKET = os.environ["POLICY_DOCS_BUCKET"]
RAG_LOCATION = os.environ.get("RAG_ENGINE_LOCATION", "europe-west3")   # GA region on 2026-10-22 (H11); europe-west2 is not listed
DATA_STORE_ID = "ticket-policies"
CORPUS_DISPLAY_NAME = "ticket-policies-corpus"


def create_data_store() -> str:
    """Return the full data store path projects/P/locations/global/collections/default_collection/dataStores/ID (B9).

    Vertical GENERIC, solution type SOLUTION_TYPE_SEARCH, source Cloud Storage (H9). Get-or-create by id.
    """
    # TODO(learner): use google.cloud.discoveryengine (DataStoreService) to create or fetch the data store.
    #   Look up the create call and the long-running operation it returns in the Discovery Engine reference.
    raise NotImplementedError


def import_documents(data_store_path: str) -> str:
    """Import gs://BUCKET/*.pdf into the data store; return the operation name."""
    # TODO(learner): DocumentService import from a GCS source (H9 lists Cloud Storage as a source). Unstructured content.
    raise NotImplementedError


def create_search_app(data_store_path: str) -> str:
    """Create a search app (engine) on the data store so the console and answer API work (H9 app types)."""
    # TODO(learner): EngineService create with solution type search. Terraform equivalent: google_discovery_engine_search_engine (I8).
    raise NotImplementedError


def create_corpus() -> str:
    """Return projects/P/locations/RAG_LOCATION/ragCorpora/ID. RagManagedDb, GEMINI_EMBEDDING_MODEL (H11)."""
    # TODO(learner): RAG Engine create-corpus call in google-cloud-aiplatform 2.6.0, then import files from BUCKET.
    raise NotImplementedError


def delete_all() -> None:
    # TODO(learner): delete corpus, search app, data store (in that order).
    raise NotImplementedError


def main() -> None:
    if "--delete" in sys.argv:
        delete_all()
        print("deleted")
        return
    ds = create_data_store()
    op = import_documents(ds)
    create_search_app(ds)
    corpus = create_corpus()
    set_key(ENV_PATH, "AGENT_SEARCH_DATASTORE", ds)
    set_key(ENV_PATH, "RAG_CORPUS", corpus)
    print(f"AGENT_SEARCH_DATASTORE={ds}")
    print(f"RAG_CORPUS={corpus}")
    print(f"import operation: {op}")


if __name__ == "__main__":
    main()
