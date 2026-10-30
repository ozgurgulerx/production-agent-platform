"""Way 3 — Voice prompt agent (preview). Same create_version surface, kind=voice.

A voice agent is a prompt agent whose definition carries the realtime model and audio
config. Its endpoint is live when version 1 exists. You talk to it over a realtime
WebSocket (Voice Live) rather than POST /responses. `azd ai agent invoke` cannot do voice.

Requires: a `gpt-realtime` deployment (FOUNDRY_VOICE_MODEL), access to the voice preview,
and `pip install "azure-ai-projects[voice]"` (already in requirements via extras? no: run it once).

Run:  python 03-voice-prompt-agent.py
Proof: version created, a text-in / text-out realtime turn, conversation listed, agent deleted.
"""
import os

from azure.ai.projects.models import (
    AgentKind,
    VoiceAgentAudioConfig,
    VoiceAgentAudioOutputConfig,
    VoiceAgentDefinition,
    VoiceModelType,
    VoiceOutputModality,
    VoiceType,
)

from _common import SUPPORT_INSTRUCTIONS, delete_agent, get_or_create, project_client

AGENT_NAME = "ticket-agent-voice"
VOICE_MODEL = os.environ.get("FOUNDRY_VOICE_MODEL", "gpt-realtime")

# allow_preview=True is required for voice definitions through .agents
project = project_client(allow_preview=True)

definition = VoiceAgentDefinition(
    model_type=VoiceModelType.MANAGED,          # service-hosted realtime model; SELF_DEPLOYED = your deployment name
    model=VOICE_MODEL,
    instructions=SUPPORT_INSTRUCTIONS + " Keep spoken replies under two sentences.",
    audio=VoiceAgentAudioConfig(
        output=VoiceAgentAudioOutputConfig(voice="en-GB-SoniaNeural", voice_type=VoiceType.AZURE_STANDARD)
    ),
    output_modalities=[VoiceOutputModality.AUDIO],
    store=True,                                  # keep transcript + audio (60-day retention)
)
agent = get_or_create(project, AGENT_NAME, definition)
print("voice agents in project:", [a.name for a in project.agents.list(kind=AgentKind.VOICE)])

# Realtime session: text in, read the transcript events back. Audio is PCM16 mono 24 kHz.
with project.beta.voice_agents.realtime.connect(agent_name=AGENT_NAME) as conn:
    first = conn.recv(timeout=45)
    conversation_id = getattr(getattr(first, "session", None), "conversation_id", None) or getattr(first, "conversation_id", None)
    print("session event:", first.type, "conversation:", conversation_id)
    conn.conversation.item.create(
        item={"type": "message", "role": "user", "content": [{"type": "input_text", "text": "My card was charged twice. What should I do?"}]}
    )
    conn.response.create()
    transcript = []
    while True:
        event = conn.recv(timeout=45)
        if event.type == "response.output_audio_transcript.delta":
            transcript.append(event.delta)
        elif event.type in ("response.done", "error"):
            break
    print("agent said:", "".join(transcript) or f"(no transcript; last event {event.type})")

if conversation_id:
    items = list(project.beta.voice_agents.conversations.list_items(AGENT_NAME, conversation_id, order="asc"))
    print(f"stored conversation {conversation_id}: {len(items)} item(s)")

delete_agent(project, AGENT_NAME)
