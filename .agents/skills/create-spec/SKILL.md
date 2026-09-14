---
name: create-spec
description: Create a specification file that a lower-tier agent can use to implement a design. This should include sample code, interfaces, pseudocode for algorithms, and design guidance. Prefer using code and psuedocode to provide guidance rather than just natural language. Some natural language is okay. The goal is to provide a document with enough specificity that a lower tier agent will successfully implement the design in the repository.
---

# Create spec

Generate a specification file that a lower tier agent can use to implement a change. If you are uncertain, if something is unclear, if you see missing items, or if you have security or design concerns about the content, ask the user. Work with the user to create the spec.

## Step 1 — Establish the feature directory

Each independent feature uses `.agents/specs/<feature-name>/`, even when multiple features are developed on the same branch. The initial output is always `spec-v1.md` in that directory.

1. Prefer a feature directory the user explicitly supplied.
2. If the user supplies only a feature name, validate that it is kebab-case, normally begins with the issue identifier, and create `.agents/specs/<feature-name>/`.
3. If the user supplies neither, list only the immediate children of `.agents/specs/`; do not read completed feature contents during discovery:
   - if exactly one directory does not contain `spec-v1.md`, use it as the user-created feature directory;
   - if several directories do not contain `spec-v1.md`, stop and ask which one to use;
   - if none qualify, continue to the next step.
4. When no directory or name is available:
   - inspect `git branch --show-current` and the requested work;
   - derive a concise candidate such as `10-feature-description` with no more than six descriptive words after the issue identifier; the number prefix should align with the number prefix of the branch (the issue number in version control). 
   - stop and ask the user to accept the candidate or provide another name before creating the directory.
5. Do not treat the branch name as the entire feature identifier. Multiple valid feature directories could start with the same issue number / branch prefix (examples: `10-add-test-metrics`, `10-update-run-tests-skill`, and `10-move-to-plugin-folder-hierarchy`).
6. If `spec-v1.md` already exists, stop and ask whether to update it, use another feature directory, or abort. Never silently overwrite an existing spec.

## Step 2 — Gather context

- Read `AGENTS.md`, `CLAUDE.md`, and every file in `docs/design/` (e.g. `concurrency-design.md`, `data_interface_overview.md`, `detailed-overview.md`, `guidelines.md`, `integrations.md`) so the task file's guidelines match the project's real conventions and priorities (reliability, accuracy, performance, maintainability, extensibility).
- Skim the review standards in `.agents/skills/peer-review/SKILL.md` so the task file's plan avoids the recurring defect patterns reviewers look for (package-boundary violations, hidden dependency construction, non-atomic aggregate updates, stale worker runtime, service-owns-worker-state, missing provenance, test-marker drift).
- Draw on the **information provided in this terminal conversation** — everything the user has said about the feature, constraints, and intent — as the primary source for the task description.

## Step 3 — Write the spec

The document must include at least the following:

- **# Feature: <clear feature name>** with a real description (not a placeholder). For a bug branch, title it **# Bug Fix** and describe the bug — symptom, trigger, and the wrong behavior — instead.
- **## Tasks** — broken into numbered Tasks, each with detailed numbered Steps and concrete sub-steps/requirements. Reference real modules, classes, and search commands (e.g. `rg -n "..." nc-svc`) wherever possible, include pseudocode, example code, class definitions, procotols, etc. Prefer code snippets, psuedocode, tables, charts, and diagrams to natural language.
- **## Acceptance Criteria** — an explicit checklist derived from the conversation with the user, so completion can be verified later.

Respect nc-algorithm norms while writing the plan: keep the service thin (CPU-bound work in workers), inject dependencies rather than constructing them deep in modules, persist through `nc_db`/Postgres, keep every worker consistent on guide/model changes, and plan `pytest` coverage with correct markers (`integration`/`slow`/`svc`).

- Integration test rule: Use real infrastructure components (not mocks).
   - Exception: OpenAI calls (nc-svc/packages/ncse-trainer/ncse_trainer/ai) and embedding generation (nc-svc/packages/ncse-deep/ncse_deep) are the only infrastructure components that should always be mocked unless the actual results from those calls are vital to the test fidelity.

## Step 4 — Save and confirm

Write `.agents/specs/<feature-name>/spec-v1.md`. Do NOT commit. Report the path and selected feature directory to the user and give a one-line summary of the Tasks and Acceptance Criteria captured.
