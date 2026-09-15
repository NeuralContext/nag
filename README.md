# Nag

Nag ([Neural Context](https://ncclassify.com) agent gating) captures [NeuralContext's](https://ncclassify.com) agent-based software development process, agent skills, tools, and documentation for agents and humans. The goal: agent-based development guided by deterministic metrics that focus on self-documenting, quality code and validated test coverage instead of reams of old specs.

It is open source, and anyone is welcome to use it. We welcome suggestions, questions, and contributions.

![Agent-based development workflow: define and approve the work; iterate between implementation and review using deterministic metrics as guardrails; give humans self-documenting code, high-level code and test visualizations, and small high-level documentation updates to review; then prepare for delivery.](assets/agent-based-development-workflow.png)

## Structure Overview

AI has exploded the world of software development (we mean this in a good way). Agents, skills, and terminal user interfaces (TUIs) have become super important if you want to keep up. But we still think humans are important too, so we're including goodies for them as well!

### Folder Structure

| Path | What's in it |
| --- | --- |
| [NAG plugin skills](plugins/nag/skills/) | Reusable workflow skills provided to Codex by the `nag` plugin. |
| `.agents/specs/<feature-name>/` | A feature's versioned specs, peer reviews, and change summary. |
| [`.codex/`](.codex/) | Configuration for this repository that is also reusable in other repositories. |
| [`AGENTS.md`](AGENTS.md) | Small bootstrap that connects repository guidance to NAG. |
| [`.agents/NAG-AGENTS.md`](.agents/NAG-AGENTS.md) | Portable NAG-wide defaults and invariants. |
| [`.agents/NAG-CONFIG.md`](.agents/NAG-CONFIG.md) | Repository-owned paths, commands, policies, and overrides. |
| [`README.md`](README.md) | You are here. Bootstrapping and process information for bipeds with large organic neural networks. |

## Things That Matter (in order)

We're being pragmatic here, not idealistic. Plus, we're a start-up, so some things may matter more to us than they do to bigger fish. But we're also thinking long-term, and code quality has a huge impact on long-term viability.

1. Code Correctness (does it compile and do what it's supposed to do?)
2. Code Quality
   - Good architecture and adherence to the design
   - Self documenting
   - Intelligible by Agents and Humans
3. Test Quality
   - Fidelity (avoids mocks where possible)
   - Correctness (checks realistic behavior and corner cases)
   - Coverage (higher coverage where it matters most)
6. Money 
   - Token burn rate
   - Use model tiers efficiently
   - Improve developer + agent efficiency
7. Speed 
   - Time-to-build
   - Reduce cognitive overload / context creep for developers and agents

## Principles

This is how we achieve high-quality code at a reasonable speed and price.

1. Code is the primary source of documentation.
2. Deterministic checks and metrics provide guardrails for all agent-based development.
3. Orchestrate iterative development between higher-tier architect/orchestrator models and lower-tier implementation models.
4. Use high-level visualizations for developer review.

## Getting Started

### Adding to an Existing Repo

Prerequisite: the NAG plugin is installed and enabled.

1. Open the target repository with the appropriate agent/model.
2. Run `$install-nag`.
3. Approve network access to retrieve verified bootstrap and configuration
   inputs from public NAG commit `fcbc43b9af615cfdd564e84c127e41909be95575`.
4. Choose whether to apply the recommended `.codex` presets.
5. Resolve decisions or gaps reported by the skill.
6. Review the unstaged diff.
7. Commit the changes only when satisfied.

`$install-nag` is the single entry point for both initial setup and later
guidance/configuration reconciliation. Its deterministic fetch script retrieves
and verifies the commit-pinned public inputs before target files are changed;
NAG looks for design material at the configured path, defaulting to
`docs/design/`. When that directory does not exist, agents continue with other
maintained repository documentation and report the missing reference.

Instruction precedence is platform safety; active repository `AGENTS.md` and
`AGENTS.override.md`; `.agents/NAG-CONFIG.md`; `.agents/NAG-AGENTS.md`; then
skill-specific defaults. Rules explicitly marked as NAG safety/integrity
invariants cannot be relaxed by repository configuration.

Some skills are language-specific. `$test-dashboard` supports only Python +
pytest, and `$dead-code-cleanup` supports Python + Poetry. `$install-nag`
records them as applicable, disabled, inapplicable, or unavailable rather than
rewriting them for another ecosystem.

> **WORK IN PROGRESS:** Some skills in the process below aren't included yet.
> Discover actual skill files for every workflow run; do not rely on this table
> as a capability registry. Missing and unconfigured validations remain visible
> gaps.

## How to Use Nag (development process overview)

Initialize the repo using [Getting Started](#getting-started) before following this process.

### Terminology

- **Agent (Architect):** A high-tier model responsible for scoping, specs, orchestration, and review.
- **Agent (Implementer):** A low- or mid-tier model responsible for implementing the spec and validating the changes.
- **Skill:** Reusable instructions in a `SKILL.md` file, plus any supporting scripts or resources.
- **Developer:** You!

### Process

1. **Developer:** 
   - Create a branch with the issue number at the start (e.g. `134-fix-all-the-broken-stuff`)
   - Start Codex with a high-tier model (e.g. 5.6-sol or astra)
   - Run `$create-spec`.
      - Prefer creating `.agents/specs/<feature-name>/` first or supplying the name to the skill when you start it (e.g. `$create-spec 10-add-test-metrics`).
      - Use a kebab-case name such as `10-feature-description`, normally beginning with the issue identifier.
      - One branch may have multiple feature directories, such as `10-add-test-metrics`, `10-update-run-tests-skill`, and `10-move-to-plugin-folder-hierarchy`.
      - If no directory or name is supplied, `$create-spec` uses a single uninitialized directory the user already created. If there are several, it asks which one to use. If there are none, it proposes a name from the branch and requested work and asks for confirmation before creating it.
2. **Architec Agent + Developer:** 
   - Work together to define the scope and acceptance criteria
   - Architect agent writes `.agents/specs/<feature-name>/spec-v1.md`.
   - Developer answers questions and approves it before implementation.
3. **Developer:** Run `$architect-and-orchestrate` and point it to the approved spec.
4. **Architect Agent:** Delegate the spec to an implementation agent.
5. **Implementer Agent:** Implement the spec and validate it using the checks below. For each applicable check, fix implementation-caused issues and rerun it before moving on. Repeat affected checks after later fixes until all required checks pass. `$run-tests` reads commands from `.agents/NAG-CONFIG.md`, runs `fast` before `slow` as separate commands, and never runs `very_slow` without current developer approval.

   | Order | Skill | Purpose |
   | --- | --- | --- |
   | 1 | `$check-code-correctness` | Check that the code builds and satisfies correctness checks. |
   | 2 | `$check-code-quality` | Check code quality and maintainability. |
   | 3 | `$check-test-fidelity` | Check that tests reflect real use and infrastructure. |
   | 4 | `$check-test-coverage` | Check coverage of the required behavior. |
   | 5 | `$run-tests` | Run the required test suites. |
   | 6 | `$dead-code-cleanup` | Verify and remove unused Python code. |

6. **Architect Agent:** Run `$peer-review` against `spec-v1.md` and save its findings as `review-v1.md` in the same feature directory. Check the findings against the review threshold: no critical or major/high issues and at most three minor issues. Automated checks are repeatable; peer review still requires judgment.
7. **Architect Agent + Implementer Agent:** If the review doesn't meet the threshold, create `spec-v2.md`, delegate the fixes, and write the next review to `review-v2.md`. Continue pairing `spec-vN.md` with `review-vN.md` until the review threshold is met and implementation is complete. Bring material design decisions back to the developer.
8. **Implementer Agent:** After the iterative spec, implementation, validation, and peer-review loop is complete, prepare final visualizations for developer review. `$test-dashboard` is optional and Python/pytest-only; it writes configured repository-local ignored artifacts and does not open them automatically. If producing a visualization identifies a required code or test change, return to the iterative loop and regenerate visualizations only after the new final review passes.
9. **Architect Agent:** Report the completed scope, validation results, visualization artifacts, final review counts, and any accepted minor issues. When ready to prepare the PR, the developer can request `$create-change-summary` to write `<feature-directory>/change-summary.md`.

### Feature artifact lifecycle

Specs, reviews, and the change summary stay available in their feature directory throughout development and merge-request review. The selected feature directory—not the branch—is the workflow context, so a branch can carry several independent feature-spec sequences.

```text
.agents/specs/
└── 10-feature-description/
    ├── spec-v1.md
    ├── review-v1.md
    ├── spec-v2.md
    ├── review-v2.md
    └── change-summary.md
```

After merge, treat the directory as frozen historical context. Do not maintain it or include it in general agent context and repository audits. Read it only when explicitly requested or when investigating that feature's history. It may be deleted later at the user's request; do not move completed features into a separate `history/` directory.

### Skills

“Who uses it” identifies who normally invokes the skill. `Missing` means no
discoverable `SKILL.md`; `disabled` means repository configuration turns it off;
`inapplicable` means it does not support the repository shape; `unavailable`
means prerequisites are absent; and `unconfigured` means required repository
settings are unresolved.

| Skill | Brief summary | Who uses it | Missing? |
| --- | --- | --- | --- |
| [`$install-nag`](plugins/nag/skills/install-nag/SKILL.md) | Install or reconcile NAG guidance and configuration for the target repo. | Developer | No |
| [`$create-spec`](plugins/nag/skills/create-spec/SKILL.md) | Write an implementation spec with acceptance criteria. | Both | No |
| [`$architect-and-orchestrate`](plugins/nag/skills/architect-and-orchestrate/SKILL.md) | Coordinate specs, delegated implementation, and review loops. | Developer | No |
| `$check-code-correctness` | Check builds and code correctness. | Agent | **Yes** |
| `$check-code-quality` | Check code quality and maintainability. | Agent | **Yes** |
| `$check-test-fidelity` | Check how well tests reflect real use. | Agent | **Yes** |
| `$check-test-coverage` | Check coverage of required behavior. | Agent | **Yes** |
| [`$run-tests`](plugins/nag/skills/run-tests/SKILL.md) | Run repository-configured test tiers and report available metrics. | Agent | No |
| [`$dead-code-cleanup`](plugins/nag/skills/dead-code-cleanup/SKILL.md) | Find and safely remove unused Python code with Vulture. | Both | No |
| [`$test-dashboard`](plugins/nag/skills/test-dashboard/SKILL.md) | Generate an optional Python/pytest-only test dashboard. | Agent | No |
| `$mermaid-visualizer` | Create diagrams for developer review. | Agent | **Yes** |
| [`$peer-review`](plugins/nag/skills/peer-review/SKILL.md) | Review implementation against the spec and record findings. | Both | No |
| [`$create-change-summary`](plugins/nag/skills/create-change-summary/SKILL.md) | Write the feature's final `change-summary.md` for merge-request review. | Developer | No |
