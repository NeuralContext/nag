# Nag

Nag ([Neural Context](https://ncclassify.com) agent gating) captures [NeuralContext's](https://ncclassify.com) agent-based software development process, agent skills, tools, and documentation for agents and humans. The goal: agent-based development guided by deterministic metrics that focus on self-documenting, quality code and validated test coverage instead of reams of old specs.

It is open source, and anyone is welcome to use it. We welcome suggestions, questions, and contributions.

![Agent-based development workflow: define and approve the work; iterate between implementation and review using deterministic metrics as guardrails; give humans self-documenting code, high-level code and test visualizations, and small high-level documentation updates to review; then prepare for delivery.](assets/agent-based-development-workflow.png)

## Structure Overview

AI has exploded the world of software development (we mean this in a good way). Agents, skills, and terminal user interfaces (TUIs) have become super important if you want to keep up. But we still think humans are important too, so we're including goodies for them as well!

### Folder Structure

| Path | What's in it |
| --- | --- |
| [`.agents/skills/`](.agents/skills/) | Skills and other agent-specific instructions for AI. |
| `.agents/specs/` | Working specs created during development; added when needed. |
| [`.codex/`](.codex/) | Configuration for this repository that is also reusable in other repositories. |
| [`AGENTS.md`](AGENTS.md) | Shared repository guidance for coding agents. |
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

1. Copy `.agents/` and `.codex/` into the root of the target repository. If either folder already exists, merge the contents so you preserve the repo's existing skills and configuration.
2. Copy `AGENTS.md` if the target repo doesn't have one. Otherwise, merge the relevant guidance into its existing file.
3. Open Codex in the target repository and select a high-tier model for architecture and orchestration. Review the copied `.codex/` configuration, including the implementation model in `.codex/agents/implementer.toml`, for your environment.
4. Run `$update-agent-guidance` to align the guidance and skills with the target repository's language, tooling, and conventions.
5. Review the updated guidance and resolve any missing references before starting development.

> **NOTE:** This library is oriented toward Python, and some skills assume certain paths and conventions. `$update-agent-guidance` adapts the guidance to the target repo, including other languages; it may ask for input where a change needs a decision.

> **WORK IN PROGRESS:** Some skills in the process below aren't included yet. The [Skills](#skills) table marks them explicitly. Until they're added, use the target repo's existing validation commands and document any gaps in the spec.

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
      - Optionally include a desired filename and a brief description of the goal of the spec (or as much detail as you want)
2. **Architect + Developer:** 
   - Work together to define the scope and acceptance criteria
   - Architect  agent writes the initial spec in `.agents/specs/`
   - Developer answers questions and approves it before implementation.
3. **Developer:** Run `$architect-and-orchestrate` and point it to the approved spec.
4. **Architect:** Delegate the spec to an implementation agent.
5. **Implementer:** Implement the spec and validate it using the checks below. For each check, fix the issues and rerun it before moving on. Repeat affected checks after later fixes until all required checks pass.

   | Order | Skill | Purpose |
   | --- | --- | --- |
   | 1 | `$check-code-correctness` | Check that the code builds and satisfies correctness checks. |
   | 2 | `$check-code-quality` | Check code quality and maintainability. |
   | 3 | `$check-test-fidelity` | Check that tests reflect real use and infrastructure. |
   | 4 | `$check-test-coverage` | Check coverage of the required behavior. |
   | 5 | `$run-tests` | Run the required test suites. |
   | 6 | `$dead-code-cleanup` | Verify and remove unused Python code. |

6. **Implementer:** Prepare visualizations for developer review with `$test-dashboard` and `$mermaid-visualizer` when available.
7. **Architect:** Run `$peer-review` against the implementation and spec. Check the findings against the review threshold: no critical or major/high issues and at most three minor issues. Automated checks are repeatable; peer review still requires judgment.
8. **Architect + Implementer:** If the review doesn't meet the threshold, the architect writes a versioned follow-up spec and delegates the fixes. Repeat implementation, validation, visualization, and review. Bring material design decisions back to the developer.
9. **Architect:** Report the completed scope, validation results, final review counts, and any accepted minor issues. When ready to prepare the PR, the developer can request `$create-change-summary` to record what actually changed.

### Skills

“Who uses it” identifies who normally invokes the skill in this workflow; agents execute the instructions. “Missing” means there is no corresponding `SKILL.md` in this repository's `.agents/skills/` folder. Summaries for missing skills describe their intended role.

| Skill | Brief summary | Who uses it | Missing? |
| --- | --- | --- | --- |
| [`$update-agent-guidance`](.agents/skills/update-agent-guidance/SKILL.md) | Adapt agent guidance and skills to the target repo. | Developer | No |
| [`$create-spec`](.agents/skills/create-spec/SKILL.md) | Write an implementation spec with acceptance criteria. | Both | No |
| [`$architect-and-orchestrate`](.agents/skills/architect-and-orchestrate/SKILL.md) | Coordinate specs, delegated implementation, and review loops. | Developer | No |
| `$check-code-correctness` | Check builds and code correctness. | Agent | **Yes** |
| `$check-code-quality` | Check code quality and maintainability. | Agent | **Yes** |
| `$check-test-fidelity` | Check how well tests reflect real use. | Agent | **Yes** |
| `$check-test-coverage` | Check coverage of required behavior. | Agent | **Yes** |
| `$run-tests` | Run the required test suites. | Agent | **Yes** |
| [`$dead-code-cleanup`](.agents/skills/dead-code-cleanup/SKILL.md) | Find and safely remove unused Python code with Vulture. | Both | No |
| `$test-dashboard` | Visualize test results for developer review. | Agent | **Yes** |
| `$mermaid-visualizer` | Create diagrams for developer review. | Agent | **Yes** |
| [`$peer-review`](.agents/skills/peer-review/SKILL.md) | Review implementation against the spec and record findings. | Both | No |
| [`$create-change-summary`](.agents/skills/create-change-summary/SKILL.md) | Write a PR summary and append it to the task file. | Developer | No |
