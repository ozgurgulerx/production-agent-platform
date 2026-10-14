# Repository instructions

## Explicit instructions only

Do only the work the user explicitly requests. Do not treat a discussion, suggestion, roadmap, or recommended next step as permission to implement it. If the requested action is unclear, explain the options and ask before changing anything.

If you identify useful work outside the explicit request, remind the user that they have not requested it and wait for an explicit instruction before doing it.

Do not create repository structures, folders, files, scaffolds, configuration, dependencies, fixtures, tooling, or CI by default. First explain what the user should create, where it belongs, why it is needed, and the commands they can run. Let the user do it. Create or change these items yourself only when the user explicitly asks you to perform that specific work.

Preserve the user's existing code. Do not replace it with empty scaffolds, move it, remove it, or restore another version unless explicitly instructed. Explain where existing code is before proposing a replacement or reorganisation.

## Learner ownership

Default to minimal, clear code snippets. Explain one concept at a time. Add extra filters, validation or abstractions only when requested.

This is a learning repository. The learner writes all functions, server adapters, and tests. Existing empty scaffolds are for the learner to fill in; this is not permission to create more scaffolds. Agents may explain contracts, review learner work, and diagnose errors when requested. Changes to documentation, fixtures, tooling, or CI also require an explicit instruction. Do not write or replace learner functions or tests unless the user expressly asks for that specific work. Do not provide hidden solutions, fabricated tests, placeholder passing tests, status claims, or xfails that make incomplete work look complete.

Stages must remain self-contained, with their own dependencies, lockfile, fixtures, source, and tests. Do not import another stage. Future roadmap stages get no folders until requested. Empty-test collection must be reported as “scaffold only—functionality unverified,” never as passing functionality. Once tests exist, run them and require at least 80% coverage. Report checks honestly.

## Documentation and verification

For vendor-specific tasks, check `documentation/` for relevant local reference material. This folder is local and git-ignored.

Keep tests and verification to the minimum appropriate for the requested change. Do not add tests, run broad suites, or repeat checks for unrelated work. A documentation-only change needs a small content or path check, not the Python test suite. Apply the coverage requirement above when verifying Python implementation work.

## Changes and Git

Commit or push only when explicitly requested. When publishing is requested, use main directly; do not create branches or pull requests unless the user asks. Preserve repository history and ignored local state. Review changes and checks before publishing. Agent-authored commits must say `[agent]` in the subject, using the conventional format such as `docs: [agent] clarify stage contracts`. Never attribute agent-authored work to the learner. Do not commit secrets, credentials, personal automation, or private local artifacts.

## Local application preferences

Never launch LibreOffice or invoke soffice. Open PowerPoint files only when asked, explicitly using Microsoft PowerPoint. When asked to open a webpage or HTML report on macOS, launch Safari explicitly unless the user chooses another browser.
