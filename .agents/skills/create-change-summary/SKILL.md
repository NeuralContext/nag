---
name: create-change-summary
description: Create a PR change summary for the current nc-algorithm branch, and append that summary to the bottom of the branch task file so it records a full history of everything that ACTUALLY changed. Use at the end of work, when the user asks to "create the change summary", "write the PR summary", or "finalize the task file". Produces tmp/PRSummary.md and updates .agents/specs/<branch>.md.
---

# Create Change Summary (nc-algorithm)

Produce the PR summary and fold it into the task file so the task file becomes a complete record of
what actually shipped on this branch.

## Step 1 — Create the PR summary

The summary goes into a PR description, so write it for a reviewer who has not seen the branch:

- Write a very short overview paragraph plus 3–6 bullet points outlining the major changes.
- **Call out startup, infrastructure, or environment changes** that would require a developer/reviewer to start or use the service differently (new/renamed settings in `.env` / `example.env` / `helm/nc-svc/values.yaml`, new Poetry deps, broker/queue changes, Docker/Helm changes, worker replica requirements, etc.).
- **If database changes occurred** (changes to objects saved via `nc_db`, new top-level persisted classes, schema-version bumps), explicitly note that the reviewer will need to **delete the old database**.
- Base everything on the real diff — compare this branch against `main`:
  ```bash
  git diff main...HEAD
  git log --oneline main..HEAD
  git diff --stat main...HEAD
  ```
- Save the result to `tmp/PRSummary.md` in this repository (create `tmp/` if needed).

## Step 2 — Append the summary to the task file

1. Get the branch: `git branch --show-current`; open `.agents/specs/<branch-name>.md`.
2. Append a **## Change Summary** section at the BOTTOM of the task file containing the same summary (overview, bullets, and the infra/DB notes).
3. This section is the task file's permanent record of everything that ACTUALLY changed on the branch — make sure it reflects the real diff, not the original intent. If the actual changes diverge from what earlier sections described, the Change Summary reflects reality. If this branch has a sister branch in another repo, note which changes are cross-repo so the two histories stay reconcilable.

## Step 3 — Confirm

Do NOT commit. Report the path to `tmp/PRSummary.md` and confirm the task file now ends with the Change Summary section. If DB changes were noted, restate the "delete the old database" callout so the user doesn't miss it.
