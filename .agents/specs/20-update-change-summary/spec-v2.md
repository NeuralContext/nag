# Feature: Make the scope finder skill callable

This iteration fixes the three integration findings in `review-v1.md` for the approved scope finder. Preserve the existing helper behavior and the four-level priority order.

## Scope and decisions

- Change only `plugins/nag/skills/find-scope-directory/SKILL.md`, unless validation reveals a direct defect in the helper.
- The skill's public name is singular: `find-scope-directory`, matching its directory and references from calling skills.
- The skill must show a runnable command that invokes the Python file through an interpreter while setting the command working directory inside the target repository. The skill's own installation path supplies the script path; the command's working directory supplies Git context.
- Correct the preflight section name to `$find-scope-directory`.
- Keep the first three priority cases and their ordering unchanged. The helper remains a fourth-priority source of candidates for user verification.

## Tasks

### Task 1: Correct the skill metadata and instructions

1. Set the frontmatter `name` to `find-scope-directory`.
2. Replace the preflight's `$create-change-summary` configuration reference with `$find-scope-directory`.
3. Replace the bare `.py` invocation with a command form such as:

   ```text
   python3 <plugin-root>/skills/find-scope-directory/scripts/find_scope_directories.py
   ```

   State that the agent sets the command working directory to a directory inside the target repository. Use a repository configured Python interpreter when required by its guidance; the script uses only the standard library.
4. Keep the existing instruction to parse `folders` and ask the user to verify candidates.

### Task 2: Validate integration

1. Read the updated skill and confirm that its name matches caller references, the command is executable through an interpreter, the working directory instruction is clear, and the priority order remains unchanged.
2. Invoke the documented command form from inside this repository and confirm the helper emits a JSON `folders` list.
3. Rerun only checks affected by any further code change.

## Acceptance Criteria

- [ ] The skill declares `name: find-scope-directory`.
- [ ] The preflight references its own configuration section.
- [ ] The fourth priority includes an interpreter-based invocation with the command working directory inside the target repository.
- [ ] The first three priorities, their order, and candidate verification behavior remain intact.
- [ ] The helper's JSON output remains valid when invoked as documented.
- [ ] Unrelated existing edits are preserved.

## Validation and workflow gaps

- `$run-tests` remains disabled and its fast/slow tier commands are unconfigured; do not invent suite commands.
- `$dead-code-cleanup` and `$test-dashboard` are disabled/inapplicable in this repository.
- `$check-code-correctness`, `$check-code-quality`, `$check-test-fidelity`, `$check-test-coverage`, and `$mermaid-visualizer` are unavailable. Use focused manual checks for this instruction-only iteration.
- Run `$peer-review` against this spec and write `review-v2.md`.
