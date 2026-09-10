---
name: peer-review-task
description: Run a scoped peer review of the implementation of a spec file focusing on the changes and impact from those changes as defined in the associated spec. Then create a peer review comments file at `.agents/specs/<spec-file-name>-pr.md` where <spec-file-name> is the name of the spec file you are reviewing against. Use when the user asks to "peer review", "review this branch", or "run the peer review" or when reviewing the output of an implemenation model. This skill references architecture guidance and documentation that should be considered when reviewing. This skill itself also contains specific guidance about review standards, severity definitions, package-boundary rules, and recurring defect patterns. STRICTLY read-only — it makes NO code changes and NO commits; it only produces the review file.
---

# Peer Review Task (nc-algorithm)

Perform a scoped peer review of recent changes on this branch and summarize the findings into the peer review comments file.
Resolution happens in a later skill, not here.

Everything needed to review is in this document or in the documents it references: the workflow (Steps 1–3) followed by the review
standards themselves — review philosophy, engineering standards, design goals, and the recurring
defect patterns that let a reviewer detect important classes of problems with the correct priorities.

The information in this skill should be complemented with the information in the documents / folders referenced herein.

**IMPORTANT CAVEAT**: If the user requests a peer review and specifies a tigher, smaller scope, do not expand the scope. In this case, only consider the parts of the spec that are related to the requested scope. When uncertain, err on the side of tightly scoping to the user's requested scope.

## Absolute constraints

- **DO NOT modify ANY application code.** Not a single line, not even an obvious fix.
- **DO NOT commit, stage, push, or run any mutating git command.**
- Your only writes are: the peer-review output markdown file.

If you notice something that begs to be fixed, you still do not fix it — you record it as a comment. Resolution is the job of the `resolve-review-issues` skill.

## Step 1 — Execute the peer review

Review the guidance in the [Review Standards](#review-standards) section, all of its descendant sections, and the documents it references 

Review the branch against this guidance, then write every finding to `tmp/xyz-peer-review-comments.md` where xyz is replaced with the issue number from the branch.
in this repository (create the `tmp/` folder if needed). In particular:

- First read the inputs named in **Always Review These Inputs**, plus this branch's task file
  (`.agents/specs/<branch>.md`) and the modules/tests adjacent to the change.
- Review against the **Review North Star** priorities
- Compare this branch against `main` (`git diff main...HEAD`, `git log --oneline main..HEAD`) and look
  for the recurring defect classes in **Common Review Findings To Reuse**.
- Honor **Scope Discipline**: prefer the smallest change that restores the intended architecture, and
  flag unrelated refactors or naming churn.
- Classify each finding `Critical`, `Major`, `Minor`, or `Trivial` per the severity interpretation in
  **Reviewer Posture**, grounded in a file path and a line or narrow location, with a fix direction.
- Work through **Review Checklist** before concluding.
- If no issues are found, say so and identify residual test gaps or risks.
- Scope your review to the changes in this branch and look for code or design issues introduced by this branch. This is not a comprehensive review of the entire codebase -- your comments should be scoped to the changes in the branch, issues / bugs introduced by the changes, or changes that significantly deviate from design guidance. 

Reviewing may read/run focused, read-only checks (e.g. `poetry run pytest -m ...` to confirm a claimed test passes) but must never modify code. Prefer running tests with 'fast' and 'slow' markers. Ask before running tests with 'very_slow' markers.

## Step 2 — Note the issues in the peer review comments file

1. Get the branch: `git branch --show-current`; open `tmp/xyz-peer-review-comments.md` where xyz is the issue number from the branch.
2. Write issues to the tmp/xyz-peer-review-comments.md file using the guidance outlined below
3. Include a summary in the file
4. Your tone should be technical and very concise where findings and/or fixes are obvious or trivial
5. For minor, major, and critical issues remain concise but provide more context and justification

## Step 3 — Confirm

Report to the user how many findings there were by severity and confirm that no code was changed and nothing was committed.

---

# Review Standards
Review and adhere to the standards in the [peer-review-standards.md document](../../../docs/peer-review-standards.md)