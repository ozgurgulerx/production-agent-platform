# Run the Agents SDK ticket agent locally, then connect it

No code here on purpose: the agent lives in [`../../../../C03-Creating-Agents-in-Copilot-Studio/labs/04-agents-sdk-connected/sdk_agent/`](../../../../C03-Creating-Agents-in-Copilot-Studio/labs/04-agents-sdk-connected/sdk_agent/). This page runs it on your laptop and wires it into Copilot Studio.

1. `source ../../../../labs-setup/.venv/bin/activate && cd ../../../../C03-Creating-Agents-in-Copilot-Studio/labs/04-agents-sdk-connected/sdk_agent && python app.py` → listens on `http://localhost:3978/api/messages` (port by convention; check `app.py`).
2. **Playground**: open the Microsoft 365 Agents Playground (Agents Toolkit), set the endpoint to that URL, send "status of ticket T-1001". You get a reply with no token involved (see `../../sketches/agents_playground_note.md`).
3. **Tunnel**: `devtunnel host -p 3978 --allow-anonymous` (or `ngrok http 3978`). Copy the HTTPS URL.
4. **Connected agent** (B5): Copilot Studio → the ticket agent → Agents → Add → *Microsoft 365 Agents SDK agent*; endpoint `https://<tunnel>/api/messages`; auth **none** for this lab. Describe when to hand off ("ticket status and history questions").
5. Ask the Copilot Studio agent "what is the status of ticket T-1001?" in the test pane; the handoff reaches your terminal (you see the request log) and the reply comes back through Copilot Studio.
6. Switch auth to **API key** in the dialog and add the matching check in `app.py`; repeat. The Playground never tested this; Copilot Studio does.

Proof: the terminal shows an inbound Activity from Copilot Studio with the tunnel host in the request, and the test pane shows your agent's text. Record the auth mode you ended with.
