# Defender security for AI agents (F14, F12, F13)

- Needs Agent 365 licensing since 1 Jul 2026. Enable from Defender → Settings → Security for AI, and PPAC → Threat detection.
- Detections use the observability Copilot Studio auto-emits (E8): prompt injection, data exfiltration patterns, anomalous tool calls (`ExecuteToolByGateway` when the Tooling Gateway is in place).
- Copilot Studio's own runtime defences stay on regardless: UPIA / XPIA protection by default, content moderation (default High), and the **bring-your-own-protection** webhook before every tool call (F12; C05 lab 03 builds it for the refund cap).
- The **protection status** column (Protected / Needs review / Unknown) in the security view (F13) is the per-agent summary across authentication, policies and moderation; it is the field an auditor reads after the inventory.

Do: raise a test alert by sending the XPIA payload from C05 lab 03 through a channel; find it in Defender incidents; quarantine from lab 01 as the response; release.
