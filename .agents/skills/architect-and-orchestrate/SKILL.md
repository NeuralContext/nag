---
name: architect-and-orchestrate
description: "Lead an implementation as a frontier-model architect: scope with the user, create versioned specs, delegate implementation to lower-tier agents, and drive review/fix iterations to an agreed quality bar. Use only when explicitly invoked for an architect-led delivery workflow."
---

# Architect And Orchestrate

Act as the architect and orchestrator, not the primary implementation worker. Preserve the user's intended outcome, constraints, and authorization boundaries throughout the work.

## Start with shared scope

Start from the approved spec supplied by the user when available; preserve its scope and approval rather than recreating it. Otherwise, work with the user to establish the smallest implementable scope and create the initial spec with `$create-spec` when available.

Confirm that repository setup is complete and the current branch starts with the issue number (for example, `134-fix-all-the-broken-stuff`), as described in the README process. Report missing prerequisites without silently changing branches or repository configuration.

- Summarize the intended outcome, affected areas, acceptance criteria, constraints, and assumptions.
- Inspect relevant project context when it can resolve a question cheaply.
- Ask the user about unresolved product or design decisions that would materially affect the solution. Do not ask for decisions that can be made safely from the existing codebase and stated scope.
- Obtain approval of the initial spec before implementation; existing approval in the conversation is sufficient. Bring material scope or design changes back to the user and record agreed decisions in the spec.

## Discover dependency skills

At the start of each invocation resolve the skills named below from `.agents/skills/<skill-name>/SKILL.md`, then from the environment's available skill catalog if no repository copy exists. Check the actual files each time; do not rely on a fixed availability list or the README's “Missing” column. This lets newly added skills participate without changes to this orchestrator.

Read each available skill fully before using it at its assigned stage, and give the implementer its resolved path and responsibility. Do not recursively invoke `$architect-and-orchestrate` as a dependency.

The following skill dependencies are required and should cause this skill to abort with an error if they are not present: `$create-spec` and `$peer-review`.

If other skill dependencies are missing, provide a warning to the user and continue without those skill dependencies.

An installed skill with a failed check or a missing prerequisite is not an absent skill: follow its instructions and report unresolved failures honestly.

If a skill dependency is present, you must use it within the spec, implement, review loop (step 3) below. You are not allowed to skip skill dependencies that are present.

## Spec, implement, review loop

Use `$create-spec` to create each new implementation spec. Follow its naming guidance exactly for the first spec. For every later spec, retain that base name and append a version suffix at the end (for example, `feature-name-v2.md`), using the convention prescribed by `$create-spec`. Preserve existing files and approved specs.

For each iteration:

1. Use the approved initial spec or create a follow-up spec that is specific enough for an independent implementation agent: outcome, in/out of scope, relevant files or components, design decisions, ordered work, acceptance criteria, validation, and known risks. Include dependency availability, fallback checks, and known validation gaps.
2. Spawn a lower-tier subagent to implement the current spec. Give it the spec location/content, relevant repository context, and a bounded instruction to implement and validate only that iteration. The orchestrator keeps architectural ownership and reviews the result; it does not silently substitute itself as the implementation agent.
3. Have the implementer execute the following validation skills in order when available. For each check, fix issues and rerun it before moving on. After later fixes, including dead-code removal, repeat affected checks until all required checks pass. Keep cleanup scoped to the implementation and impacted code.

   | Order | Skill | Purpose |
   | --- | --- | --- |
   | 1 | `$check-code-correctness` | Build and check code correctness. |
   | 2 | `$check-code-quality` | Check quality and maintainability. |
   | 3 | `$check-test-fidelity` | Verify tests reflect real use and infrastructure. |
   | 4 | `$check-test-coverage` | Check coverage of required behavior. |
   | 5 | `$run-tests` | Run required test suites. |
   | 6 | `$dead-code-cleanup` | Verify and remove unused code introduced by current changes or when the spec has a dead-code objective. |

4. Have the implementer prepare human-review visualizations with `$test-dashboard` and `$mermaid-visualizer` when available. Refresh affected visualizations in subsequent iterations.
5. Run `$peer-review` when available against the resulting implementation and current spec. Preserve and capture its output as that skill requires, including issue severity and supporting evidence. Automated checks do not replace review judgment.
6. Triage the review. Address every critical and major/high-severity issue through delegated fixes. For a medium-or-higher risk design decision that is important and not clearly determined by the agreed scope or codebase, pause and ask the user for direction; present the decision, options, recommendation, and consequence of deferring it.
7. If the review threshold is not met, create the next versioned spec addressing the non-trivial findings and delegate it. Reuse the same lower-tier agent when practical; otherwise spawn another lower-tier implementation agent. Repeat implementation, validation, visualization, and review.

Repeat the loop until the review has no critical or major/high issues and at most three minor issues remain. Treat `Major` and `High` as blocking severities. Trivial issues may be recorded but do not require another iteration. Do not claim completion without the final review result and required validation results; disclose any gaps from unavailable skills.

## Delegation and reporting

- Use lower-tier models for implementation and routine fix passes; reserve the frontier model for scoping, architecture, spec writing, review interpretation, and user-facing decisions.
- After every implementation/review cycle, give the user a concise status update: spec version, what changed, validation performed, review counts by severity, and any decision needed from them.
- On completion, report the final implemented scope, validation results, visualization artifacts, final review counts, accepted minor issues, and missing skills or unresolved validation gaps.
- When the user requests PR preparation through `$create-change-summary`, use it if available to record what actually changed. Existing authorization is sufficient; otherwise leave this as a user-requested handoff, as in the README process. Apply the same discovery and warning behavior if the skill is missing.

## Items to Exclude From Context
The following files/folders should be excluded from general context gathering by the architect-orchestrator and by any sub-agents implementing changes. Access specific files when explicitly requested by the user or required as inputs or outputs by an active dependency skill (for example, review or summary artifacts in `tmp/`); this does not authorize browsing the whole excluded directory. For other required access, ask the user for permission. All of the following are relative to the repository root.
- .agents/specs/history
- tmp/
- dist/
- node_modules/
