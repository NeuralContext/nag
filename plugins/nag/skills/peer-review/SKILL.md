---
name: peer-review
description: Run a scoped read-only review against a selected `spec-vN.md` and write only its matching `review-vN.md`.
metadata:
  nag: true
---

# Peer Review

Review an implementation against one selected feature spec. Resolution belongs
to a later implementation iteration, not this read-only review.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$peer-review` section. If a
required file or setting is missing, follow `NAG-AGENTS.md` fallback behavior
and report the gap. Use the configured review-standards path when it exists;
otherwise use the portable standards below and disclose the missing reference.

If the `$peer-review` section of the NAG-CONFIG.md shows `Enabled: no`, skip this skill completely and alert the user.


## Absolute constraints

- Do not modify application, test, guidance, spec, or generated files.
- Do not commit, stage, push, change branches, or run mutating git commands.
- The matching peer-review Markdown file is the only permitted write.
- Honor a user-supplied narrower scope; do not broaden it.

## Select inputs and output

Prefer the exact `.agents/specs/<feature-name>/spec-vN.md` supplied by the user
or current orchestration workflow. If no spec(s) location was provided, use the 
`$find-scope-directory` skill to determine the most likely scope specification(s).

The only output is the selected spec's paired path:

```text
.agents/specs/<feature-name>/spec-vN.md
.agents/specs/<feature-name>/review-vN.md
```

If that review already exists, obtain approval before overwriting it. Keep the
selected feature directory explicit throughout.

## Review

Read the selected spec, relevant active guidance/design material, configured
review standards, and changed modules/tests attributable to the feature.
Inspect the complete committed, staged, unstaged, and untracked implementation
diff against the appropriate base. When the branch contains several features,
use the selected spec/reviews to scope attribution and ask rather than guessing.

Prioritize correctness, security, data integrity, regressions, architectural
compatibility, dependency boundaries, failure handling, and missing or
low-fidelity tests. Run only focused non-mutating checks using repository
commands from `$run-tests` configuration. Never run `very_slow` without current
user approval.

Classify findings as:

- `Critical`: immediate security/data-loss/system-wide failure risk.
- `Major`: blocking correctness, design, compatibility, or required-validation
  defect (`High` findings from another convention map to `Major`).
- `Minor`: localized non-blocking defect or maintainability/test gap.
- `Trivial`: optional polish with negligible risk.

Ground every finding in a narrow file location, evidence, consequence, and fix
direction. Flag unrelated scope. If there are no findings, say so and record
residual risks or validation gaps.

## Write and confirm

Write a concise summary and findings to the matching `review-vN.md`. Report
counts by severity, validation performed, residual gaps, and confirmation that
no other file changed and nothing was committed.
