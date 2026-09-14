---
name: create-spec
description: Create a specification file that a lower-tier agent can use to implement a design. This should include sample code, interfaces, pseudocode for algorithms, and design guidance. Prefer using code and psuedocode to provide guidance rather than just natural language. Some natural language is okay. The goal is to provide a document with enough specificity that a lower tier agent will successfully implement the design in the repository.
---

# Create spec

Generate a specification file that a lower tier agent can use to implement a change. If you are uncertain, if something is unclear, if you see missing items, or if you have security or design concerns about the content, ask the user. Work with the user to create the spec.

## Step 1 — Establish a Filename for the Spec
The filename must use kebab-case and must be a Markdown file with an 'md' extension.
1. Preferred Approach
   - If the user provides a filename use it
   - If the user does not provide a filename but a concise filename can reasonably be extracted by what the text they've provided, use this name and prompt to ensure the user accepts the name
2. Secondary Approach
   - If the user does not provide sufficient information to determine a filename, use the branch information:
      - Get the current branch name:
         ```bash
         git branch --show-current
         ```
      - Create a filename that includes the first section of the branch name (typically the issue number) and a kebab-case description of the task composed of no more than 6 words based on the branch name.
         - Example: `.agents/specs/123-fix-concurrency-bugs.md`
3. If a file already exists at the path, STOP and ask the user whether to overwrite, append, provide a new filename or abort. Never silently clobber an existing spec file.

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

Write the file. Do NOT commit. Report the path back to the user and give a one-line summary of the Tasks and Acceptance Criteria captured.