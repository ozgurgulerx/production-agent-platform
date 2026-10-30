# 00 — Setup: tenant, licences, admin, app registration, pac, venv

The user has a tenant with admin rights, so this track can run as it is written. This page is what the tenant and the laptop need before session 1.

## 1. Tenant and licences
- **Copilot Studio capacity**: a prepaid pack (25,000 Copilot Credits per month) or pay-as-you-go through an Azure billing policy. The maker licence is free, the tenant needs credits (reading map K5). GitHub Copilot harness agents need a Microsoft 365 Copilot licence on the maker, or usage-based credits (K5, A5).
- **A Managed Environment** for the labs. Environment-level telemetry (H2), environment group rules (F2) and CMK (F9) only work there. UK data residency: region United Kingdom, Dataverse URL ends `crm11.dynamics.com`.
- **Admin roles**: Power Platform administrator for PPAC, DLP and quarantine; Global or AI administrator for Agent 365 registry actions; Purview roles for audit search. C09 says per lab which one it needs.
- **Tenant switches to check before C04/C06**: external models enabled in PPAC and provider terms accepted in the M365 admin centre (K3); cross-geo generative AI allowed or not (C11); publishing of generative agents not turned off tenant-wide (C11).

## 2. Laptop tooling
```bash
brew install dotnet                                   # .NET SDK for the pac tool
dotnet tool install --global Microsoft.PowerApps.CLI.Tool
pac --version
pac auth create --deviceCode                          # interactive; stores a profile, no secret
pac auth list && pac env who                          # confirm the environment
code --install-extension microsoft-IsvExpTools.powerplatform-vscode   # Power Platform tools; the Copilot Studio extension id: verify in the Marketplace
```
The Copilot Studio VS Code extension (GA Jan 2026, C2) is installed from the Marketplace; it clones the agent as YAML next to the `pac copilot clone` output.

## 3. App registration for device-code sign-in
Create one **public client** app registration in Entra (no secret):
- Authentication → "Allow public client flows" = Yes; redirect `http://localhost` (mobile and desktop platform).
- API permissions (delegated): **Power Platform API** `CopilotStudio.Copilots.Invoke` (Direct-to-Engine, C8); `CopilotStudio.AdminActions.Invoke` (quarantine, F5; admin only); **Dynamics CRM** `user_impersonation` (Dataverse Web API); **Microsoft Graph** `Application.Read.All` (C04 lab 01 reads the agent's service principal), `Sites.ReadWrite.All` (C08 uploads policy files), `AuditLog.Read.All` (C09 lab 03).
- Grant admin consent once.
- Put the application (client) id in `.env` as `CLIENT_ID`. Every `_common.py` uses `msal.PublicClientApplication` with a per-lab token cache; nothing else is stored.
If the Power Platform API does not appear in the permission picker, register it first (`pac admin` or PowerShell `New-MgServicePrincipal -AppId 8578e004-a5c6-46e7-913e-12f58912df43`; the app id of "Power Platform API" is the documented one as of 2026, verify).

## 4. Python environment
```bash
bash scripts/bootstrap_venv.sh
source ../.venv/bin/activate
```
Pinned on 25 Oct 2026: `microsoft-agents-copilotstudio-client` 1.9.0, `microsoft-agents-hosting-aiohttp` 1.9.0, `microsoft-agents-authentication-msal` 1.9.0, `msal` 1.39.0, `mcp` 2.3.0.

## 5. Verify
```bash
bash scripts/verify.sh
```
Checks `.env`, `pac` and its auth profile, the venv imports, a device-code token for the Power Platform API (first run prompts), and a Dataverse `WhoAmI`.

## Proof checklist
- [ ] `verify.sh` prints `OK`
- [ ] `pac env who` shows the Managed Environment and the UK region
- [ ] The app registration shows admin consent for all delegated scopes in §3
- [ ] PPAC → Licensing → Copilot Studio shows the credits pool and the environment
