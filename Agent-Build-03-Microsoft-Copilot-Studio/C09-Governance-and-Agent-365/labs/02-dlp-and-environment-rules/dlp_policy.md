# Block the HTTP virtual connector, watch publish disable, unblock (F1, F2)

Every change here is reverted in the same session. Do this in the **lab environment only**; a policy scoped to all environments would disable publishing tenant-wide.

## Before
```bash
python dlp_check.py          # capture state 1: HTTP classification, no-auth-chat classification, ticket connector
```

## Change (Power Platform admin centre)
1. Policies → Data policies → New policy, name `ticket-agent-lab-policy`.
2. Prebuilt connectors: move **HTTP** to **Blocked**. Optional: add endpoint filtering instead (Allow `https://<apim>.azure-api.net/*`, Deny `*`), which is the production shape in `../../sketches/dlp_policy_shape.json`.
3. Move **Chat without Microsoft Entra ID authentication in Copilot Studio** to **Blocked**.
4. Custom connectors: put the ticket connector (and the MCP connector it created in C04 lab 02) in **Business**.
5. Scope: **Add multiple environments** → only the lab environment. Save.

Admin API alternative (verify path): `PUT https://api.bap.microsoft.com/providers/PowerPlatform.Governance/v2/policies/{id}?api-version=2016-11-01` with the sketch body; or PowerShell `New-DlpPolicy` / `Set-DlpPolicy` from `Microsoft.PowerApps.Administration.PowerShell`.

## Observe
```bash
python dlp_check.py          # state 2: HTTP=Blocked
```
Open the ticket agent in Copilot Studio. If it has a REST tool (C04 lab 03) or an HTTP request node, the **Publish** button is disabled with a DLP violation message; the tool is listed. If the agent only has the MCP tool on a Business connector, publish still works: the point of the exercise. Now move the MCP connector to Blocked and watch publish disable too (MCP rides a connector).

## Revert
Move HTTP back to Business (or delete `ticket-agent-lab-policy`), restore the MCP connector, save. `python dlp_check.py` shows state 3 equal to state 1. Publish is enabled again.

## Advanced Connector Policies (F2)
In Environment groups → your Production group → Rules → Advanced connector policies: pre-approve the ticket connector and its actions; switch on **ACP-only mode** (preview). Anything not listed is refused at design time. Record the group rule as part of the proof.
