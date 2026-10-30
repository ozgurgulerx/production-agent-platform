"""Run the same workflow in-process (no hosting) and show the checkpointing that makes it resumable.
Usage: python run_local.py
"""
import asyncio
import os
import sys
from pathlib import Path

from agent_framework import FileCheckpointStorage
from dotenv import find_dotenv, load_dotenv

sys.path.insert(0, str(Path(__file__).parent / "src" / "ticket-workflow"))
load_dotenv(find_dotenv(usecwd=False) or find_dotenv(usecwd=True))  # .env at the track root (walks up)
os.environ.setdefault("AZURE_AI_MODEL_DEPLOYMENT_NAME", os.environ.get("FOUNDRY_MODEL", "gpt-5-mini"))

from main import build_workflow_agent  # noqa: E402


async def main() -> None:
    agent = build_workflow_agent()
    result = await agent.run("Hi, my card was charged twice for order 8841, £42.10 each. Please fix it, I need the money back.")
    print("=== customer reply ===\n", result.text)

    # Checkpoints: a workflow (not the agent wrapper) can persist each superstep and be resumed.
    storage = FileCheckpointStorage(storage_path=str(Path(__file__).parent / ".checkpoints"))
    print("checkpoint storage ready at", storage.storage_path if hasattr(storage, "storage_path") else ".checkpoints")
    print("Resume pattern: workflow.run(checkpoint_id=<id>, checkpoint_storage=storage, stream=True); see Agent Framework docs 'checkpoints'.")


asyncio.run(main())
