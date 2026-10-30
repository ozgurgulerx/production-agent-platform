# Golden answers: identity for an agent on Foundry

Six questions a contract client architecture panel asks on identity, each with the points a three-minute spoken answer must contain. The skeletons are the grading rubric; the answers themselves are yours, recorded aloud and transcribed (checklist 7.1). Grade 0–4 per question: 4 = every point, in order, with one concrete example and one named failure; 2 = points present but no example; 0 = vocabulary only. Record the transcript path and score in the log below.

## 1. OIDC or SAML for the agent, and why?

Must say: OIDC is the authentication layer on OAuth 2.0 and is what you build for any new app; SAML appears only where an enterprise portal already uses it; neither issues the token the agent's tools accept; the agent's tool calls are OAuth access tokens with an audience, acquired separately; for an autonomous agent there is no user sign-in at all, the agent's own identity authenticates. Example: the bank's SAML portal embeds the assistant; the assistant's own registration uses OIDC with PKCE and requests `api://ticket-api/.default`. Failure: sending a SAML assertion or an ID token as the MCP bearer.

## 2. The CISO says no keys and no public endpoints. Show me.

Must say: every runtime hop is an identity (managed identity in Container Apps, agent identity for the agent, federated credential for CI, OIDC for people); keys disabled on OpenAI and Search; the one remaining secret and where it lives; private endpoints with public access disabled, APIM internal, Front Door with WAF as the only public face, Firewall egress allow-list; the component table row by row. Example: the Search query path, identity and network. Failure: `DefaultAzureCredential` in production, or a gateway check with a reachable backend behind it.

## 3. Whose identity calls the tool, and who approved that permission?

Must say: the agent's own Entra identity, created with the agent, no credential of its own, the blueprint holds it; Agent Service exchanges blueprint credential for an agent-identity token and then an audience-scoped token; the tool validates audience and reads `roles`; the permission is an app-role assignment an administrator granted to that identity, recorded in Entra; when the tool must act as the user, delegation and consent instead, and the audit log shows subject user, actor agent. Example: `Refunds.Execute` on the refund agent only. Failure: project managed identity in production.

## 4. How do you stop every agent in the project sharing one identity?

Must say: current Foundry provisions a blueprint and identity per agent; the shared project identity exists for legacy agents and prototypes; migration changes the identity and role assignments do not transfer, so plan the re-grant; separate identities give separate audit lines and separate permission sets; sponsor on each; blueprint-level actions for the kind. Example: triage agent denied `issue_refund` while the refund agent is permitted, same project. Failure: `azd` compatibility grant of `Foundry User` on the shared identity left in place in production.

## 5. What does the audit log show when the refund tool is called?

Must say: one correlation ID from sign-in to backend receipt; sign-in log for Ayşe with CA result; trace with agent `oid`, tool name, arguments hash, approval request; gateway log with validated `oid`, scope, policy outcome; server log with scope check, ticket entitlement, approval ID, operation key, outcome; backend receipt; no token, no secret, no raw customer content anywhere in it. Example: the ten-step walkthrough. Failure: the model's summary treated as the execution record.

## 6. Forty agents from three teams and a vendor in one tenant. How do you govern them?

Must say: every agent has an Entra identity with a sponsor; the registry (Agent 365) is the inventory; Conditional Access and permission revocation at blueprint level per kind of agent; access reviews on agent role assignments at service-account cadence; Purview for data risk, Defender for threat detection; switching one off is a blueprint action, not a code change; vendor agents get the same identity treatment or do not connect. Example: "disable all Sales Assistant agents." Failure: inventory by spreadsheet; vendor agent on a shared key.

## Log

| Date | Question | Transcript | Score | Gap |
|---|---|---|---|---|
| | | | | |
