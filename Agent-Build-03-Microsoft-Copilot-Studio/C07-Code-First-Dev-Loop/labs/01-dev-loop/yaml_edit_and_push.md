# Edit the YAML, pull, push, publish

Proves: `pull` is a three-way merge, `push` stops on conflict, `publish` is what new sessions see (C1, L1).

1. `cd ticket-agent && git checkout -b feat/refund-wording`.
2. Open the agent manifest or instructions file the clone produced (name recorded in `README.md` after your first clone; `# verify`). Change one sentence, for example "Refunds above 250 GBP require a human approval" to "Refunds above 250 GBP are routed to the UK card team for approval".
3. `pac copilot pull --path .` first. If a maker changed anything in the portal since the clone, you see it merged into your tree now, not as a surprise later.
4. `pac copilot push --path .` then `pac copilot publish --schemaName $AGENT_SCHEMA_NAME`.
5. In the portal, open a **new** test-pane session and ask "What happens with a 300 GBP refund?" The wording is new. An existing session keeps the old wording until you type "start over" or it idles out (L1).
6. Conflict rehearsal: edit the same instruction in the portal, then change it again in YAML and push. The push stops with a conflict message. Run `pull`, resolve, push again. This is the whole safety model; there is no force.
7. `git commit -am "refund wording" && git push origin feat/refund-wording`, open the PR. The PR, not the portal, is where the review happens.

Record in the proof checklist: the new-session answer, the old-session answer, and the exact conflict message text.
