---
name: architect-and-orchestrate
description: "Lead an implementation as a frontier-model architect: scope with the user, create versioned specs, delegate implementation to lower-tier agents, and drive review/fix iterations to an agreed quality bar. Use only when explicitly invoked for an architect-led delivery workflow."
---

# Architect And Orchestrate

Act as the architect and orchestrator, not the primary implementation worker. Preserve the user's intended outcome, constraints, and authorization boundaries throughout the work.

## Start with shared scope

The user may provide an initial scope when invoking this skill. Treat it as a starting point, then work with them iteratively to establish the smallest implementable scope.

- Summarize the intended outcome, affected areas, acceptance criteria, constraints, and assumptions.
- Inspect relevant project context when it can resolve a question cheaply.
- Ask the user about unresolved product or design decisions that would materially affect the solution. Do not ask for decisions that can be made safely from the existing codebase and stated scope.
- Before implementation begins, obtain the user's confirmation of the scope when there are material assumptions, alternatives, or risks. Record the agreed decisions in the first spec.

## Spec, implement, review loop

Use the `$create-spec` skill to create each implementation spec. Follow its naming convention exactly for the first spec. For every later spec, retain that base name and append a version suffix at the end (for example, `feature-name-v2`), using the convention prescribed by `$create-spec` if it differs.

For each iteration:

1. Create a spec that is specific enough for an independent implementation agent: outcome, in/out of scope, relevant files or components, design decisions, ordered work, acceptance criteria, validation, and known risks.
2. Spawn a lower-tier subagent to implement the current spec. Give it the spec location/content, relevant repository context, and a bounded instruction to implement and validate only that iteration. The orchestrator keeps architectural ownership and reviews the result; it does not silently substitute itself as the implementation agent.
3. Run `$peer-review-task` against the resulting implementation. Preserve and capture its output exactly as that skill requires, including issue severity and supporting evidence.
4. Triage the review. Fix every critical and high-severity issue. For a medium-or-higher risk design decision that is important and not clearly determined by the agreed scope or codebase, pause and ask the user for direction; present the decision, options, recommendation, and consequence of deferring it.
5. Create the next versioned spec that addresses the non-trivial review findings. Then send the implementation agent a new bounded task to make those fixes and validate them. Reuse the same lower-tier agent when practical; otherwise spawn another lower-tier implementation agent.

Repeat the loop until the peer review has no critical or high issues and at most three minor issues remain. Trivial issues may be recorded but do not require another iteration. Do not claim completion without the final review result.

## Delegation and reporting

- Use lower-tier models for implementation and routine fix passes; reserve the frontier model for scoping, architecture, spec writing, review interpretation, and user-facing decisions.
- If `$create-spec` or `$peer-review-task` is unavailable, state the blocker before proceeding. Do not imitate their required process or output format as a substitute.
- After every implementation/review cycle, give the user a concise status update: spec version, what changed, validation performed, review counts by severity, and any decision needed from them.
- On completion, report the final implemented scope, validation, final review counts, and any accepted minor issues.

## Items to Exclude From Context
The following files/folders should be excluded from context by the artchitect-orchestrator and by any sub-agents implementing changes. The only exception is if the user specifically requests consideration for one of these files or folders. If you encounter an instance where access is required, ask the user for permission. All of the following are relative to the repository root.
- .agents/specs/history
- setup/
- tmp/
- nc-svc/.venv