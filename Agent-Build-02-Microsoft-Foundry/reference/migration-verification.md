# Structure update verification — 30 October 2026

## Preservation

The pre-migration inventory contained 29,857 regular files, including ignored local state. Every file was found at its mapped destination after the move. 29,838 remained byte-identical; 19 changed through documentation extensions or reviewed path-reference updates. Existing dependency declarations and notebooks were preserved. The original tree was moved rather than reconstructed from Git because substantial existing content was untracked.

The nine original module READMEs remain within their updated documents under “Retained chapter material”. Four new module READMEs, the section overview, reference/depth documents and study-log instructions were added. No dated study results were created.

## Checks

- All local Markdown file targets within the Foundry section resolve. External URLs and heading anchors were not exhaustively validated.
- The two Python files with changed path references parse successfully; the setup shell script passes bash syntax checking. These checks do not execute the code.
- Cross-section references were updated where they used the old Foundry paths.
- No package installation, dependency upgrade, cloud deployment or runtime lab verification was performed.
- Existing working-tree changes were preserved; no commit or push was made.

## Remaining limitations

Moved virtual environments can contain former absolute paths and must not be assumed runnable; see [SDK compatibility](sdk-compatibility.md). Existing cross-stage/shared-environment dependencies are retained pending a separately authorised migration. Historical API/status claims in retained chapters are not re-certified by this update. Mastery remains unassessed and future implementation exercises remain learner-owned.
