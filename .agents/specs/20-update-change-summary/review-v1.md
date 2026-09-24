# Peer review: spec-v1

## Summary

The helper implements Git-root discovery, issue-prefix matching, Markdown filtering, and deterministic JSON output. The implementer reported focused success and error-path checks passing in temporary Git repositories. The skill integration has two blocking issues. No production code, guidance, or test files were changed during this review.

## Findings

### Major 1: Skill name does not match callers

- Location: `plugins/nag/skills/find-scope-directory/SKILL.md:2`
- Evidence: frontmatter declares `name: find-scope-directories`, while the directory is `find-scope-directory` and both `create-change-summary` and `peer-review` refer to `$find-scope-directory`.
- Consequence: skill discovery or invocation by the referenced name can fail, so the helper may never be called through the intended workflow.
- Direction: declare `name: find-scope-directory` and keep caller references aligned.

### Major 2: Skill does not give an executable command

- Location: `plugins/nag/skills/find-scope-directory/SKILL.md:31-33`
- Evidence: the instruction says to run a `.py` path without an interpreter. The file has mode `664` and no shebang.
- Consequence: attempting to execute the documented path directly fails with permission or executable-format errors.
- Direction: instruct the agent to invoke the helper with an available Python interpreter and explicitly set command working directory inside the target repository.

### Minor 1: Preflight references another skill's configuration

- Location: `plugins/nag/skills/find-scope-directory/SKILL.md:13`
- Evidence: its preflight says to apply the `$create-change-summary` section of `NAG-CONFIG.md`.
- Consequence: future configuration for this skill could be ignored or unrelated change-summary settings could be applied.
- Direction: reference `$find-scope-directory` instead.

## Validation and gaps

- Implementer reported passing focused checks for root and nested invocation, exact numeric prefix, recursive case-insensitive Markdown detection, invalid branch, outside-Git invocation, missing specs, and extra arguments.
- `stat` confirms the helper mode is `664`; read-only source inspection confirms the invocation and name findings.
- `$run-tests` is disabled with fast and slow tiers unconfigured in `.agents/NAG-CONFIG.md`; no repository suite was run.
- `$dead-code-cleanup` and `$test-dashboard` are disabled/inapplicable by configuration. Code correctness, code quality, test fidelity, test coverage, and Mermaid visualization skills are unavailable.
- `git diff --check` reports trailing whitespace in an unrelated pre-existing edit to `plugins/nag/skills/peer-review/SKILL.md`; this review did not alter that file.

Counts: Critical 0, Major 2, Minor 1, Trivial 0. The review threshold is not met.
