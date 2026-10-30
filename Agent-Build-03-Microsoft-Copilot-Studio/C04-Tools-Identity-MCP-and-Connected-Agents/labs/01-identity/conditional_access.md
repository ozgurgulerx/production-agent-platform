# Conditional Access on the agent identity (reading map E1, E3)

What exists: because publish attaches connector scopes to the agent's service principal, a Conditional Access policy can target those scopes with the usual conditions (device compliance, named locations, sign-in risk). The Entra Agent ID security controls need Agent 365 licensing (E3).

What does not exist yet: enforcement outside Teams. The page says CA on the agent identity "applies only in Teams" today. A policy that blocks the ticket agent from unmanaged devices does nothing for the demo website or a Direct-to-Engine app, where the end-user's own CA (on the user, not the agent) is what runs.

## Try it (portal, no script)
1. Entra → Protection → Conditional Access → New policy. Target: the agent's service principal (search by agent name) under "Target resources → cloud apps" if it appears; otherwise target the connector scope app (`Azure API Connections Runtime` or the connector's service principal). verify: which selector the tenant shows depends on the Agent ID rollout.
2. Grant: require compliant device.
3. Test in Teams from an unmanaged browser: the agent's tool call is blocked and the chat shows the sign-in / block card.
4. Test on the demo website: no change.

## What to write in the design review
"Conditional Access on the agent constrains Teams today; for web and API surfaces the controls are end-user auth mode, DLP on the connector, and the IP firewall (preview, web chat only, F10)."
