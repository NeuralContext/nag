---
name: update-agent-guidance
description: Audit and update repository AGENTS.md and .agents/skills so their guidance, references, and language-specific commands match the current codebase.
---

# Update Agent Guidance

Bring `AGENTS.md` and every skill below `.agents/skills/` into alignment with the repository without expanding their scope or changing application code just to satisfy an instruction.

## Discover the repository and its conventions

1. Find the repository root and read every applicable `AGENTS.md` file before making any edits. Treat those files as guidance to audit as well as instructions to follow.
2. Inventory every `AGENTS.md` in scope and every `SKILL.md` below `.agents/skills/`, including resources each skill links to. Treat each skill directory as a unit.
3. Establish the repository's current sources of truth:
   - language and package manifests (for example `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `.sln`, `pom.xml`, or `build.gradle`);
   - task scripts, CI workflows, formatter/linter/test configuration, and documented developer commands;
   - maintained repository documentation, especially top-level docs and docs nearest to the affected component.

Do not infer tooling from a skill's old command. Prefer existing project scripts or documented commands, then the language's configured standard tools. Preserve intentionally multi-language repositories and scope a command to the component it serves.

## Review and update each skill

For `AGENTS.md` and each skill:

1. Check every path, command, script name, configuration file, environment variable, service name, and named workflow it references. Remove or replace references that are demonstrably stale. Do not remove a reference merely because it is external, optional, or unavailable in the current shell.
2. Add a short link or path to repository documentation only when it gives a user of that skill necessary, maintained guidance. Use the most specific existing documentation; do not create documentation or duplicate its contents just to add a link.
3. Update language-specific commands to commands actually supported by the component. Examples: a JavaScript/TypeScript project may use `npm run lint` and `npm test`; a Rust project may use `cargo fmt --check`, `cargo clippy`, and `cargo test`. Preserve project package-manager choices and existing CI commands rather than substituting generic equivalents.
4. Keep instructions concise, preserve user-facing behavior and approval boundaries, and avoid unrelated edits. Do not add placeholders, speculative commands, or references to files that do not exist.

## Approval gate

Before applying a proposed change, ask the user for explicit permission and wait if any change:

- has a moderate or higher risk of breaking behavior, workflows, or developer tooling;
- introduces, changes, or could expose a security risk; or
- is based on guidance whose logic or fit with the repository is uncertain.

Explain the affected guidance, the reason for the change, and the specific risk or uncertainty. Continue with low-risk, well-supported corrections without interruption, but leave gated changes unapplied until the user authorizes them.

## Python-script exception

If a skill specifically invokes, depends on, or instructs the user to run a Python script:

1. Do not translate or replace that script with another language, even if the repository's primary language is not Python.
2. Ask the user whether Python is available in the environment where the skill will run, and wait for the answer before changing that skill's Python-dependent behavior.
3. If Python is available, retain the script and update only its valid paths, invocation details, and relevant documentation links.
4. If Python is not available, disable the skill without deleting it: rename its entrypoint from `SKILL.md` to `SKILL.md.disabled`, add a brief reason and re-enable condition at the top of that file, and report the change. Do not attempt a replacement implementation.

## Verify and report

After editing, re-scan the updated skills for broken local paths and obsolete commands. Run the repository's relevant lightweight validation commands when they are known and safe; otherwise state what could not be verified. Summarize the skills changed, stale references removed or replaced, documentation linked, any language-tool changes, and any skills disabled pending Python availability.
