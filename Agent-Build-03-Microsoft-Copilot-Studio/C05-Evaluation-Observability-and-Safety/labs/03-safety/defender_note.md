# Defender security for AI and the first-party provider

Reading map F12, F14. Defender is a provider on the same pre-tool-call hook your webhook uses, with threat intelligence behind it. Enable it from Defender → **Security for AI** and the Power Platform admin centre **Threat detection** page; it requires Agent 365 licensing (GA 1 May 2026, F15). Detections use the observability stream Copilot Studio emits automatically to Agent 365 (E8). Your webhook and Defender can coexist: Defender for threats, your webhook for business rules.
