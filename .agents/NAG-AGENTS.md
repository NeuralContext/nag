# NAG Agent Guidance

## Instruction precedence

Apply instructions in this order:

1. Platform safety, security, and permission restrictions.
2. Active `AGENTS.md` and `AGENTS.override.md` files.
3. Repository-specific `.agents/NAG-CONFIG.md` instructions.
4. The shared defaults in this file.
5. The active skill's skill-specific defaults.

Active repository guidance may override NAG defaults. It may not override a
requirement explicitly marked **NAG invariant**. If a conflict is ambiguous,
stop and ask the user.

## Shared skill preflight

Before using any NAG skill:

1. Find the repository root and read all active `AGENTS.md` guidance.
2. Read `<repo-root>/.agents/NAG-AGENTS.md`.
3. Read `<repo-root>/.agents/NAG-CONFIG.md`.
4. Apply the configuration section for the active skill, if present.
5. If a required file or setting is missing, use the fallbacks below and
   report the gap. Never invent a destructive, networked, or expensive command.

## Goals and Principles
1. Code is the primary source of documentation.
2. Deterministic checks and metrics provide guardrails for all agent-based development.
3. Orchestrate iterative development between higher-tier architect/orchestrator models and lower-tier implementation models.
4. Use high-level visualizations for developer review.

## Reference Material
If you are requested to "only" or "exclusively" or "just" review one or more artifacts, only review those. If you are not provided with explicit guidance on what to review before starting, review all of the files in the docs/design folder and adhere to all of the design, architecture, guidance, constraints, process, and goals outlined in those documents.

## Dev Environment
- Poetry is used to manage dependencies and execute scripts and run applications
- Run all poetry commands (e.g. compile, lint, tests) using the Poetry environment (e.g. `poetry run ...`) and do not use the system Python interpreter for repository validation.
- If `poetry run check` fails with numerous import errors, it's probably due to your sandbox environment. Run `poetry run check` outside your sandbox environment if this happens.

## Agent resources — `.agents/`

`.agents/` contains agent-facing material, shared by every coding agent:
- `.agents/specs/<feature-name>/` — one feature's versioned specs, peer reviews, and change summary. A branch may contain multiple feature directories.
- `.agents/skills/` — the skills both agents load, each self-contained. Codex reads this path natively; `.claude/skills` is a symlink to it so Claude Code sees the same files. Edit skills here only, never through the symlink's own path.
- `.agents/NAG-CONFIG.md` - repository-specific information for NAG skills. Read it before invoking a NAG skill and apply the corresponding section.

This file is the root instruction file; `CLAUDE.md` is a symlink to it.

## Repository context and design documents

Use the design-document path in `.agents/NAG-CONFIG.md`. If it is absent, use
`docs/design/`. Read maintained design documentation relevant to the requested
work unless the user gives a narrower scope.

If the configured/default directory does not exist, continue with maintained
documentation available elsewhere in the repository and report the missing
reference. An absent design directory is a gap, not a reason to fabricate
guidance or halt otherwise safe work.

Exclude generated/build/dependency directories and frozen feature histories
from general context. Read an excluded path only when the user selects it or a
workflow requires a specific file from it.

## Feature specification workspaces

Each independent feature uses `.agents/specs/<feature-name>/`:

```text
.agents/specs/<feature-name>/
├── spec-v1.md
├── review-v1.md
├── spec-v2.md
├── review-v2.md
└── change-summary.md
```

The active feature directory is established by the current workflow, not inferred from the branch alone:

1. Prefer a directory the user explicitly supplied.
2. If the user supplies a feature name, create `.agents/specs/<feature-name>/`.
3. Otherwise, list only the immediate children of `.agents/specs/` without reading their contents. If exactly one directory has no `spec-v1.md`, treat it as the user-created feature directory. If several qualify, ask the user which to use.
4. If no uninitialized directory exists, derive a kebab-case candidate such as `10-feature-description` from the branch and requested work, then ask the user to confirm or replace it before creating the directory.

Feature names should begin with the issue identifier when one is available. Different directories may share that identifier, for example `10-add-test-metrics`, `10-update-run-tests-skill`, and `10-move-to-plugin-folder-hierarchy`.

Keep the selected directory in context throughout `$create-spec`, `$architect-and-orchestrate`, `$peer-review`, and `$create-change-summary`. Do not switch directories based only on the current branch. If more than one directory could apply and the current workflow did not identify one, ask the user which to use.

Specs and reviews remain available throughout feature development and merge-request review. After merge, the directory is frozen historical context:

- do not update or maintain it;
- exclude it from general agent context and repository audits;
- read it only when explicitly requested or when investigating that feature's history.

A frozen feature directory may be deleted when the user requests cleanup.

## Nag Skill Identification and Configuration
- Nag skills are identified by the `metadata.nag` field in the skill's frontmatter YAML
    - All nag skills have the following in their frontmatter:
        ```YAML
        metadata:
            nag: true
        ```
- Repository specific instructions, exclusions, references, and overrides for NAG skills are found in `.agents/NAG-CONFIG.md`

## Test execution and artifacts

Use `$run-tests` after changing production code, production data inputs, or
tests. For tooling/documentation-only changes, follow the invoking task's
validation authorization or ask before running costly repository suites.

- Ask the user if `$run-tests` should be run when modifying non-production scripts or other code that doesn't impact production. It is okay to carry some broken tests forward if a larger feature is split across multiple specs and the user has specifically requested this.
- If `$run-tests` outputs errors, fix them before considering your task complete.
    - If the `$run-tests` errors are pre-existing or were not initiated on this branch, by the user, or by you, ask the user how to proceed.

The canonical tiers are `fast`, `slow`, and `very_slow`. Run configured `fast`
before configured `slow`, in separate commands. **NAG invariant:** never run
`very_slow` without explicit approval from the user in the current workflow.
Missing tier commands are visible validation gaps.

NAG's generic integration-test preference is real infrastructure. The active
repository owns all mock exceptions and infrastructure policy in
`.agents/NAG-CONFIG.md` or active `AGENTS.md` guidance.

Write generated NAG artifacts only to the configured repository-local artifact
path. **NAG invariant:** reject artifact destinations outside the repository
root. Do not open GUI applications without an explicit user request and any
required environment approval.

## Change and validation boundaries

- **NAG invariant:** do not commit, stage, push, create a PR, or change branches
  unless the user explicitly authorizes that action.
- Keep changes within the approved task and preserve unrelated user changes.
- Diagnose failures before editing. Fix them only when the task authorizes code
  changes; otherwise report them.
- Treat unavailable or inapplicable skills honestly. Do not install frameworks
  or dependencies without authorization.
- Prefer existing repository scripts and configuration over generic commands.
- Use recoverable operations and obtain approval for destructive, networked,
  expensive, or externally visible actions when required.

## Code and Comment Expectations
- Code should be self-documenting. Classes and functions should be focused, with concise but expalanatory names.
- There are several reasons to consider breaking something into one or more functions:
    - Code reuse--if the same or very similar code is / will be needed somewhere else, consider creating a function
    - Code readibility--instead of adding a comment, create a function whose name clarifies the intent (e.g. _record_exclusive_task_outcome).
- The following guidelines should be considered when determining if a new function should be added:
    - A function should be decomposed into smaller functions if it contains more than 50 lines of code (including comments)
    - A function should be elminiated if it contains less than 2 lines of code
    - If a new function will decrease readability or introduce complexity significantly consider using a class or other programming abstraction
    - If a large comment is needed to explain something, consider decomposing into a function or class where names and docstrings obviate the need for the comment
- Comments should be extremely concise and describe WHY something occurred. Do not document HOW something is done or WHAT something does in the comments.
    - Docstrings are a small exception in that they may give a very concise description of what an attribute contains, how a function should be used, or what a class represents. They should be concise and focus on aspects that are not self-evident from the name or structure of the code.
- Design trade-off and architecture decisions should not be recorded in comments. They should be recorded in the ADR of the feature spec.
- When adding new docstrings, they should generally be a single line. With rare exceptions they can extend to two lines, never more.
    - Existing docstrings in the code or longer docstrings modified by developers are fine and should not be modified unless you are specifically modifying that function/class/module/attribute. In that case, do not try to minimize the docstring to meet the guidelines.
- Inline comments should almost always be a single line with rare exceptions going to two lines.
- Comments should be minimal and infrequent. The code is authoritative and should be clean with naming standards that meet the following:
    - function names represent what the function does (e.g. clean, get_id, reserve_slot, etc.)
    - class names reflect what the class represents as a component or structure (e.g. ExclusiveTaskSlot, ClassificationGuide, Rule, etc.)
    - variable and field names reflect what the variable contains or represents. They typically do not indicate the type with the exception being cases where the type is integral to its purpose (disambiguation, etc)

## Documentation
The following section guides persistent documentation, not detailed, ephemeral specs used for feature development. Guidelines for feature specifications is found in the $create-spec skill
- Documentation should be minimal with a few high-level design documents
    - Should focus on the following:
        - High level goals and guidelines
        - Why high level capabilities / functionality exist
        - Why certain constraints have been imposed (focusing on problem domain / customer reasons)
        - Caveats, limitations, and goals that impose restrictions or caveats on the system or it's design
        - High level architectural guidelines
        - Architecture Decision Record for high level architectural decisions and impact
        - Important algorithms / Intellectual Property should be outlined in pseudocode / diagrams
    - Should NOT be comprehensive
    - Should NOT describe what the code does
    - Should NOT be considered as authoritative but should be considered as cooperative with the code
        - If significant discrepancies exist they should be resolved
        - The documentation is a high-level overview
        - The code is the self-documenting implementation.
    - Should focus on high-level concepts that cannot be pulled easily from the code
- Medium-fidelity specs are useful during feature develompent but should not be maintained or referred to after feature completion (merge complete)
- General rule: well-written code IS the documentation

## General Expectations
- Never commit code to the git repository unless you are requested to do so
- Do not make changes unless the task requires it or the prompt specifically requests it.
- Do not use intitiative to "fix things" or "improve things"
- When reviewing code or documents, if there are only trivial issues or minor documentation issues just say "Looks good to me.". 
- When reviewing code or documents, keep the review to the changes made or areas of code impacted by the change. Unless specifically told to do so, do not expand scope beyond this.
- When design tradeoffs are not clear in the documentation or a decision is made that isn't intuitive and may lead to peer review confustion, add a design decision row to the Architecture Decision Record in docs/design/architecture-decision-record.md

## Project State
- 
- This project is currently a greenfield project. Do not worry about database migrations or preserving legacy deployments.
    - The single caveat is that version controlled data used for testing, scripts, etc. must be migrated if breaking changes occur.
- If you see issues that would cause breakage if a legacy production deployment existed, add a note that you're not capturing these items as we're still in greenfield development.

## Communication Style
- Be professional
- Be concise
- Do not use filler phrases like "this is where it bites", "your instinct is right", "you are right to question", "which I should have flagged instead of", "Good challenge", etc.
    - Be direct. If you or I were wrong, just say "This was incorrect."
    - If there are options to consider, just say "Here are several options to consider."
