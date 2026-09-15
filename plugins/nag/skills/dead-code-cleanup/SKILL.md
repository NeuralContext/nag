---
name: dead-code-cleanup
description: Find and safely remove unused Python code in a Poetry project with Vulture; report inapplicable in other repository shapes.
metadata:
  nag: true
---

# Dead Code Cleanup

Use Vulture to produce candidates, then remove only code verified unused. This skill is Python/Poetry-specific. It is `inapplicable`, not broken, when the repository is not a Python Poetry project.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$dead-code-cleanup` section. If a required file or setting is missing, follow `NAG-AGENTS.md` fallback behavior and report the gap. Stop with `inapplicable` when configuration or repository manifests show this skill does not apply.

If the `$dead-code-cleanup` section of the NAG-CONFIG.md shows `Enabled: no`, skip this skill completely and alert the user.
## Scan and verify

From the directory containing `pyproject.toml`, check
`poetry run vulture --version`. Use the existing Poetry environment; do not add Vulture or change dependency files without approval. Run Vulture against the configured source/test scope, excluding vendored, generated, migration, build, cache, and environment directories.

For every candidate, search direct and dynamic references, exports, entry
points, framework/plugin registration, serialization, templates, and config.
Preserve public APIs and uncertain candidates. Remove only tightly related,
verified dead code and its newly obsolete imports/tests/references.

Do not add arbitrary Vulture whitelist entries merely to make the report clean; use a documented whitelist only for verified intentional dynamic/public uses.

If Vulture is missing, prompt the user for permission to install unless the

## Validate and report

Rerun the same Vulture scope and repository-configured relevant checks through
Poetry. Report removed and retained candidates, evidence, exact commands and
results, and dependency/configuration gaps. Do not commit.
