# Register the webhook as the environment's protection provider

Reading map F12 (preview). Environment admin.

1. Expose the webhook on HTTPS: `az containerapp up --name ticket-protection --source . --ingress external --target-port 8089` from this folder, or for a lab session a dev tunnel: `devtunnel host -p 8089 --allow-anonymous` (anonymous only for the lab; production uses the FIC token).
2. Create an app registration for the webhook's audience and a **federated identity credential** that trusts the Copilot Studio issuer named on the Learn page (verify the exact issuer/subject in your tenant).
3. Power Platform admin centre → the environment → **Settings** → **Security** → *External security provider* (label verify): paste the endpoint URL, the audience app id; save.
4. Test from the published agent: "Refund T-1002 in full." The orchestrator plans `issue_refund(400)`, the hook returns `block`, the agent reports the reason.
5. Watch the webhook logs: every tool call in the environment now hits this endpoint, not only refunds; keep `decide()` O(1).

Failure mode to remember: a slow or down webhook is an **open** gate (default allow after 1 s). Alarm on your own error rate and latency, and keep the same rule on the tool's API as the second line.
