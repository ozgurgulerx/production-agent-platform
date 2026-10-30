# Compare two versions before you publish

Since December 2025 a test set can run against two agent versions side by side (reading map I2). The habit: edit, save (do not publish), run the set against the draft and the published version, read the diff, then publish.

1. Make the change (instructions, a knowledge source, a tool description).
2. Monitor → Evaluations → the set → **Run** → choose *Draft* and *Published* (or two named versions).
3. Read the per-case diff. Any refusal case that flipped from pass to fail blocks the publish.
4. From code: run `run_and_poll.py` twice with `agentVersion` set in the body (`# verify` the key on the API page) and diff the two `metricsResults` lists.

The one thing to resist: fixing a failing case by editing the case. The case is the policy; the agent is what changes.
