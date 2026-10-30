# The same loop in the VS Code extension

GA January 2026 (C2). Install "Microsoft Copilot Studio" from the Marketplace, sign in with the same account as your pac profile.

1. **Clone** from the extension's agent list, or open the `ticket-agent/` folder you already cloned; the extension recognises the layout.
2. Edit a topic YAML: IntelliSense offers node types and properties; an invalid node is underlined before you push. This is the check a coding agent editing raw YAML does not get.
3. **Sync** view shows drift between the portal and your tree (the same three-way state `pac copilot pull` uses).
4. **Apply** pushes with a diff preview; **Publish** is a separate command, as in pac.
5. Everything is still files in Git: commit and open the PR from the same window.

Note for §5 of the chapter: the extension page pitches this workflow for GitHub Copilot and Claude Code. If you let a coding agent edit here, keep it on a dev environment profile and keep Publish behind CI.
