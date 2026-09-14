---
name: create-change-summary
description: Create a feature-scoped merge-request change summary at `.agents/specs/<feature-name>/change-summary.md`.
metadata:
  nag: true
---

# Create Change Summary

Produce a reviewer-facing summary of what actually changed for one selected
feature. This is portable and is not tied to a language or application.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$create-change-summary` section.
If a required file or setting is missing, follow `NAG-AGENTS.md` fallback
behavior and report the gap.

## Select and attribute the feature

Prefer a feature directory or spec path supplied by the user or orchestration
workflow. Otherwise follow the shared feature-directory selection contract.
Never select by branch alone.

Read the selected feature's specs and reviews to establish intended scope.
Inspect the complete branch diff and log, but include only changes clearly
attributable to that feature. If a file or hunk cannot be attributed
confidently, ask the user instead of guessing. Label changes used by multiple
features as `cross-feature` and identify other affected feature directories
when known.

## Create the summary

- Compare the branch against its base using `git diff`, `git log`, and `git diff --stat`, then scope the summary to the selected feature.
- Read the feature's `spec-vN.md` and `review-vN.md` files, but describe the actual diff rather than merely repeating intended work.
- Write a short overview plus 3–6 bullets covering the major changes.
- Call out startup, infrastructure, environment, dependency, and data-migration changes that affect reviewers or deployment.
- If actual changes diverge from the specs, describe what shipped and note the divergence.

## Write and confirm

Write `.agents/specs/<feature-name>/change-summary.md` with a short overview,
three to six major-change bullets, validation/review results, divergences from
the specs, and reviewer-relevant environment, dependency, infrastructure, or
migration changes. Describe the actual diff, not just intended work.

When other feature directories exist on the branch, state that the document is
feature-scoped and is not a complete branch summary. Update an existing summary
only with user authorization. Do not commit. Report the path and material
divergences or actions reviewers must not miss.
