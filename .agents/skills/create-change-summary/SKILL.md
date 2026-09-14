---
name: create-change-summary
description: Create the merge-request change summary for a selected feature and save it as `.agents/specs/<feature-name>/change-summary.md`.
---

# Create Change Summary

Produce a reviewer-facing summary of what actually shipped for one selected feature.

## Step 1 — Select the feature directory

Prefer a feature directory or `spec-vN.md` path supplied by the user or current orchestration workflow. The selected directory must be `.agents/specs/<feature-name>/`.

Do not select by branch alone: a branch may contain multiple feature directories. If the active feature is ambiguous, stop and ask the user which directory to summarize.

## Step 2 — Create the summary

- Compare the branch against its base using `git diff`, `git log`, and `git diff --stat`, then scope the summary to the selected feature.
- Read the feature's `spec-vN.md` and `review-vN.md` files, but describe the actual diff rather than merely repeating intended work.
- Write a short overview plus 3–6 bullets covering the major changes.
- Call out startup, infrastructure, environment, dependency, and data-migration changes that affect reviewers or deployment.
- If actual changes diverge from the specs, describe what shipped and note the divergence.
- Save the result to `.agents/specs/<feature-name>/change-summary.md`. If it already exists, update it to reflect the current diff; do not append the summary to a spec.

## Step 3 — Confirm

Do NOT commit. Report the `change-summary.md` path and any material divergence, infrastructure action, or migration action the reviewer must not miss.
