---
name: update-agent-guidance
description: Audit repository guidance and resolve portable NAG configuration, paths, commands, and skill applicability.
metadata:
  nag: true
---

# Update Agent Guidance

Align repository-owned guidance and `.agents/NAG-CONFIG.md` with the actual
repository without changing application code to satisfy instructions.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$update-agent-guidance` section.
If a required file or setting is missing, follow `NAG-AGENTS.md` fallback
behavior and report the gap.

## Discover sources of truth

Inventory applicable `AGENTS.md`, all `.agents/skills/*/SKILL.md` files and
their required local resources, language/package manifests, task scripts, CI,
formatter/linter/test configuration, and maintained documentation. Prefer
existing repository scripts and documented commands. Preserve multi-language
components and their package managers.

## Resolve NAG configuration

Populate `.agents/NAG-CONFIG.md` with verified values for:

- design documentation, artifact, review-standard, and ADR paths;
- separate `fast`, `slow`, and `very_slow` commands, marking missing tiers
  unconfigured rather than inventing commands;
- test framework, integration infrastructure, and allowed mocks;
- `$test-dashboard` enablement and repository-local data/HTML outputs;
- update each language-dependent skill's `Enabled` metadata to `yes` or `no` and state the reason if set to `no`.;
- repository-specific overrides that do not belong in portable skills.

Resolve all angle-bracket placeholders for affected skills. Prefer poetry, uv, npm or other framework scripts over direct test executables and never install or require Vitest merely because the repository uses npm. Never translate a required Python script into another language. If Python availability for an enabled Python-dependent skill cannot be established safely, report the unresolved applicability decision rather than deleting or silently rewriting the skill.

## Audit and approval boundary

Check every referenced path, command, environment variable, service, and
workflow. Remove demonstrably stale references while preserving external or
optional references that remain intentional. Keep repository-specific material
in configuration or active `AGENTS.md`, not copied across skills.

Ask before moderate-or-higher-risk workflow changes, security-sensitive
changes, or changes based on uncertain guidance. Apply low-risk verified
corrections within the user's request.

Rescan local paths and placeholders, run safe lightweight validations, and
report files changed, configuration resolved, applicability decisions, gaps,
and commands/results. Do not commit.
