---
name: create-spec
description: Create an implementation-ready, versioned feature specification for an independent implementation agent. This should include sample code, interfaces, pseudocode for algorithms, and design guidance. Prefer using code and psuedocode to provide guidance rather than just natural language. Some natural language is okay. The goal is to provide a document with enough specificity that a lower tier agent will successfully implement the design in the repository.
metadata:
  nag: true
---

# Create Spec

Work with the user to define a change and write an implementation-ready spec.
Ask about unresolved product, security, or architectural decisions that would
materially affect the solution.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$create-spec` section. If a
required file or setting is missing, follow `NAG-AGENTS.md` fallback behavior
and report the gap.

If the `$create-spec` section of the NAG-CONFIG.md shows `Enabled: no`, skip this skill completely and alert the user.

## Select the feature directory

Each independent feature uses `<repo-root>/.agents/specs/<feature-name>/`, even when multiple features are developed on the same branch. The initial output is always `spec-v1.md` in that directory.

1. Prefer a feature directory the user explicitly supplied.
2. If the user supplies only a feature name, validate that it is kebab-case, normally begins with the issue identifier, and create `<repo-root>/.agents/specs/<feature-name>/`.
3. If the user supplies neither, list only the immediate children of `<repo-root>/.agents/specs/`; do not read completed feature contents during discovery:
   - if exactly one directory does not contain `spec-v1.md`, use it as the user-created feature directory;
   - if several directories do not contain `spec-v1.md`, stop and ask which one to use;
   - if none qualify, continue to the next step.
4. When no directory or name is available:
   - inspect `git branch --show-current` and the requested work;
   - derive a concise candidate such as `10-feature-description` with no more than six descriptive words after the issue identifier; the number prefix should align with the number prefix of the branch (the issue number in version control). 
   - stop and ask the user to accept the candidate or provide another name before creating the directory.
5. Do not treat the branch name as the entire feature identifier. Multiple valid feature directories could start with the same issue number / branch prefix (examples: `10-add-test-metrics`, `10-update-run-tests-skill`, and `10-move-to-plugin-folder-hierarchy`).
6. If `spec-v1.md` already exists, stop and ask whether to update it, use another feature directory, or abort. Never silently overwrite an existing spec.

## Gather context

Read user-provided requirements, relevant code/tests, maintained repository
documentation, and the configured design-document path (configured in `<repo-root>/.agents/NAG-CONFIG.md`). If that path (default
`docs/design/`) is absent, use other maintained documentation and report the
gap. Do not require `CLAUDE.md` or any repository-specific service, database,
worker, framework, marker, or mock convention unless active guidance supplies
it. Review `$peer-review` standards or its configured standards path when
available.

Do not include specs in the `<repo-root>/.agents/specs` folder unless they are in the same folder as the spec being created and are specifically related to this spec / feature.

## Write the spec

Create `spec-v1.md`, or the explicitly requested next `spec-vN.md`, containing:

- outcome, scope, exclusions, constraints, and assumptions;
- affected files/components and relevant interfaces;
- design decisions with code, pseudocode, tables, or diagrams;
- ordered implementation tasks;
- acceptance criteria and validation commands/skills;
- dependency availability, fallbacks, known gaps, and risks.

The document must include at least the following:
- **# Feature: <clear feature name>** with a real description (not a placeholder). For a bug branch, title it **# Bug Fix** and describe the bug — symptom, trigger, and the wrong behavior — instead.
- **## Tasks** — broken into numbered Tasks, each with detailed numbered Steps and concrete sub-steps/requirements. Reference real modules, classes, and search commands (e.g. `rg -n "..." nc-svc`) wherever possible, include pseudocode, example code, class definitions, procotols, etc. Prefer code snippets, psuedocode, tables, charts, and diagrams to natural language.
- **## Acceptance Criteria** — an explicit checklist derived from the conversation with the user, so completion can be verified later.

Ensure the spec respects repository-configured test tiers and infrastructure policy. The spec should define the implementation sufficiently that $run-tests and $dead-code-cleanup will pass.

Respect repository norms. Focus spec test coverage requirements on integration tests that minimize the use of mocks. 
**Spec requirements must align with the design principles and guidance on code and comments, documentation and design referenced in `<repo-root>/.agents/NAG-AGENTS.md`**

Do not commit. Report the selected directory, output path, and a concise scope
summary.
