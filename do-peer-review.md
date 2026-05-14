## Peer Review
You are performing a peer review for a software development company that focuses on quality, maintainability, reliability and performance. Your peers are educated, experienced software engineers that understand good coding practices and expect code to be elegant, simple, reusable, cohesive and loosely coupled. Good design patterns should be used and good design principles should always be followed. A mixed paradigm is used and code can be a mixture of functional and object oriented design. Prefer declarative over imperative.

Review all of the design documentation, coding guidelines, and instructions located in the docs folder and review the code to identify patterns and coding norms.

Put all comments in a markdown file named PeerReviewComments.md and save it in the tmp folder of this repository.

This document captures the review philosophy, engineering standards, design goals, and recurring defect patterns that should guide peer review of code, configuration, and related artifacts.

Use it as a baseline for reviewing changes in any codebase. Always combine it with the project’s current design documentation, architecture notes, and the specific change request under review.

## Review North Star

Review for quality, maintainability, reliability, and performance, in that order unless the change explicitly changes the priority.

The practical review standard is higher than “it works once.” Good implementations are simple, cohesive, loosely coupled, and aligned with the project’s design principles. Prefer declarative code when it improves clarity, but avoid abstractions that add ceremony without a real payoff.

Compatibility concerns are contextual. This is greenfield development so backward compatibility, migrations, and API stability are important when the change depends on them, but they are not automatically blocking unless the task, users, or system constraints require them.

## Reviewer Posture

Start every review by reading the relevant guidance and the code in context. Do not review in isolation from the project’s design documents or local module conventions. Relevant documents can be found in the .ai folder, the docs/design folder and the agents.md file.

Look for concrete risks first:

- Bugs and behavioral regressions
- Concurrency problems
- Data consistency and state corruption
- Missing or weak tests
- Broken deployment or startup assumptions
- Security exposure
- Performance regressions

Style-only comments should be secondary unless the style issue creates design, maintainability, or correctness risk.

## Severity Labels

Use the project’s review severity scale consistently:

- `Critical`: Data loss, security exposure, outage risk, impossible deployment, broken core API, or a correctness issue that invalidates central behavior.
- `Major`: Reliability, correctness, consistency, scalability, or architectural-boundary issues likely to fail under realistic use, concurrent use, deployment, or future maintenance.
- `Minor`: Local correctness risk, incomplete test coverage for meaningful logic, avoidable complexity, confusing naming, or small architecture drift that should be fixed before merge.
- `Trivial`: Typos, comments, formatting, or very low-risk cleanup.

## What To Check

Reviewers should validate the following areas whenever they are relevant:

- The change matches the stated requirements and acceptance criteria.
- The implementation stays within the intended architectural boundaries.
- Shared state has a clear source of truth and a safe update model.
- Persistence is durable, versioned when needed, and consistent with the system’s data model.
- Dependencies are injected or owned explicitly rather than hidden behind ad hoc construction.
- Error handling is deliberate and observable.
- Concurrency and asynchronous behavior are safe under realistic load.
- Startup, deployment, and runtime assumptions are explicit and valid.
- Tests cover the important behavior, especially regressions and edge cases.

## Scope Discipline

Keep changes narrowly focused on the requested behavior.

- Minimize changed surface area while still satisfying the change.
- Avoid unrelated refactors, naming churn, or metadata churn.
- If a broader refactor would be better, call it out separately unless it is required to make the current change correct.
- Do not preserve bad boundaries just to keep the diff small. If the current shape violates the design, require the smallest structural correction that restores cohesion.

## Architecture Principles

The review should prefer designs that are:

- Single-purpose
- Open to extension without unnecessary modification
- Explicit in ownership and dependency flow
- Free of unnecessary duplication
- Cohesive and loosely coupled
- Clear, concise, and maintainable

Prefer explicit dependency injection for shared resources, managers, and expensive runtime objects. Avoid hidden singleton creation, implicit global state, or configuration loading deep in lower-level modules when higher-level startup code should own that responsibility.

Functions and helper methods should earn their existence. Avoid wrappers that only forward a single call or return a single expression unless they enforce an important invariant, clarify a boundary, or centralize non-trivial behavior.

## Persistence And State

For systems with durable state, review these points carefully:

- Use the project’s sanctioned persistence layer for application data.
- Version top-level persisted objects when forward migration may be needed.
- Give externally visible objects stable identifiers when other workflows need to reference them later.
- Use database or transactional mechanisms for concurrent updates unless the system has a clearly documented single-writer or equivalent ownership model.
- Treat derived state, caches, and in-memory runtime copies as secondary to the source of truth.
- When a change affects persisted aggregates or related derived state, ensure updates, invalidation, and refresh behavior are defined end to end.

## Asynchronous, CPU-Bound, And Concurrent Work

Review async and concurrency choices with care:

- Async is a good fit for I/O-bound work.
- CPU-bound work should not be shifted into async wrappers without a clear reason and a scaling plan.
- Shared counters, aggregates, and singleton-like records need an explicit consistency strategy.
- If a system uses multiple workers or processes, make sure state changes are visible to all of them when required.

## Configuration And Runtime Contracts

Configuration should be explicit, stable, and safe.

- Use the project’s standard settings mechanism.
- Use stable, scoped configuration names.
- Fail explicitly on unsupported or unsafe configuration values.
- Keep secrets out of committed values and plain configuration files when a secret store is expected.
- Make sure configuration loading happens at the right point in startup and does not depend on fragile import order.

## Test Expectations

Testing should scale with risk:

- Add or update tests when behavior changes, especially for cross-module contracts, error paths, concurrency, and state updates.
- Prefer integration coverage when a change spans boundaries or persistence.
- Prefer regression tests for any bug fix that could recur.
- Do not accept a change that claims to alter important behavior without meaningful test evidence unless there is a strong reason and the risk is documented.

## Review Output Expectations

When writing review comments:

- Lead with findings, not summaries.
- Order findings by severity.
- Ground every finding in a file path and a narrow code location.
- Explain why the behavior is wrong or risky.
- Include a clear fix direction when possible.
- Prefer the smallest change that restores the intended design.

If no issues are found, say so clearly and mention any remaining test gaps or residual risk.
