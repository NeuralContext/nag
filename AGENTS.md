# Agent Guidance

## NAG workflow

Before performing repository work, read and follow
`.agents/NAG-AGENTS.md`.

When invoking a NAG skill, also read `.agents/NAG-CONFIG.md` and apply
the sections required by that skill.

Instruction precedence is: platform safety; active `AGENTS.md` and
`AGENTS.override.md`; `.agents/NAG-CONFIG.md`; `.agents/NAG-AGENTS.md`; then
the active skill's defaults. Requirements explicitly marked as NAG invariants
remain above repository configuration.

Repository-specific instructions in this file override NAG defaults
unless `.agents/NAG-AGENTS.md` explicitly identifies a requirement as
a non-overridable safety or integrity constraint.

## Repository-specific guidance

{{Additional guidance goes here}}
