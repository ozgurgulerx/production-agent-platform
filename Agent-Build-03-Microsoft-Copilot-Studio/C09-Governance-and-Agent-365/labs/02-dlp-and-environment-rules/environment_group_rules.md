# Environment group rules for this lab (F2, F3)

Create two groups if they do not exist: **Makers** and **Production**. Both need Managed Environments. Set the rules from [`../../sketches/environment_group_rules.md`](../../sketches/environment_group_rules.md).

Do, in order:
1. Power Platform admin centre → Environment groups → New group `cs-track-makers`; add the lab environment.
2. Rules → **Agent sharing**: Viewer to security groups only, cap 50; **Transcript access**: makers; **Preview models**: allowed.
3. Open the ticket agent → Share: "Everyone in the tenant" is no longer offered. Screenshot.
4. New group `cs-track-production` (empty for now) with ACP-only mode, external models off, transcripts admins only, cross-geo off.
5. Default environment routing: switch on so new makers get a routed developer environment in `cs-track-makers`.

Revert: remove the lab environment from the group (rules stop applying) or leave it, since the rules are the recommended state.

Why it matters beyond governance: environment-level OpenTelemetry export to App Insights (C05 lab 02, H2) and customer-managed keys (F9) only exist for Managed Environments.
