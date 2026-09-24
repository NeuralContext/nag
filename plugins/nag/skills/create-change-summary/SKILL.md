---
name: create-change-summary
description: Create a spec or branch scoped MR change summary
metadata:
  nag: true
---

# Create Change Summary

Produce a reviewer-facing summary of what actually changed for one spec or branc. This is portable and is not tied to a language or application.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$create-change-summary` section.
If a required file or setting is missing, follow `NAG-AGENTS.md` fallback
behavior and report the gap.

## Select and attribute the feature

Prefer a feature directory or spec path supplied by the user or orchestration
workflow. If the user did not provide specific guidance on scope location, use
the $find-scope-directory skill to determine the most likely scope specification(s).

Read the specs and reviews, if available, to establish intended scope.
Inspect the complete branch diff and log and include changes clearly
attributable to that spec(s). If a file or hunk cannot be attributed
confidently, ask the user instead of guessing. Label changes used by multiple
features as `cross-feature` and identify other affected feature directories
when known.

If no spec was provided do not ask for unattributable changes -- just assume they are all
a part of the requested change summary.

If a change appears unrelated to the spec(s) ask the user if it should be included.

## Create the summary

- Compare the branch against its base using `git diff`, `git log`, and `git diff --stat`, then scope the summary to the selected spec(s).
- Read the feature's `spec-vN.md` and `review-vN.md` files, but describe the actual diff rather than merely repeating intended work.
- Write a short overview plus 3–6 bullets covering the major changes.
- Call out startup, infrastructure, environment, dependency, and data-migration changes that affect reviewers or deployment.
- If actual changes diverge from the specs, describe what shipped and note the divergence.

## Write and confirm

Create the change summary in the the spec folder location if it was identified.
If no spec(s) location was identified, ask the user where the change summary
should be writtne. Write a short overview, three to six major-change bullets, 
validation/review results, divergences from the specs, and reviewer-relevant environment,
dependency, infrastructure, or migration changes. Describe the actual diff,
not just intended work.

When other feature directories exist on the branch, state that the document is
feature-scoped and is not a complete branch summary. Update an existing summary
only with user authorization. Do not commit. Report the path and material
divergences or actions reviewers must not miss.
