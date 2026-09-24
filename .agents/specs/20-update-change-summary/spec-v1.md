# Feature: Find possible scope directories from the branch issue number

Add a Python helper for the `find-scope-directory` skill's fourth priority: when the user has not identified a specification or folder, suggest possible specification directories from the current branch's issue number. The agent runs the helper from anywhere inside the target repository. The helper discovers that repository's root through Git and returns candidates; the agent applies the skill's priority order and confirms scope with the user.

## Scope and decisions

- Implement `plugins/nag/skills/find-scope-directory/scripts/find_scope_directories.py`. The existing empty `find_scope_location.py` stub may be removed as part of this task.
- The helper takes no path argument. It uses the command's working directory to discover the repository root with Git, then uses that root for branch discovery and the `.agents/specs` search. The script file's own location does not determine the repository being searched.
- Add a concise invocation instruction to `plugins/nag/skills/find-scope-directory/SKILL.md` for the fourth priority. It tells the agent to run the helper with a command working directory inside the target repository and to treat its JSON output as possible locations requiring user verification. Preserve the existing priority order.
- Branch names must begin with a numeric issue identifier followed by a hyphen and a kebab-case suffix, for example `20-update-change-summary`. The identifier is the initial contiguous digits before the first hyphen.
- A matching candidate directory starts with the same digits followed by a hyphen, so issue `20` matches `20-add-feature`, but not `200-other-feature` or `20other-feature`.
- Markdown files are files with a case-insensitive `.md` suffix anywhere below the candidate directory. Hidden and nested paths are included.
- Output is one JSON object with a `folders` array containing absolute matching folder paths, sorted lexicographically. No candidates, including a missing `.agents/specs` directory, produce `{"folders": []}`.
- A working directory outside a Git repository, Git failures, a branch name without a numeric prefix, and an unreadable specs directory must produce a concise error on stderr and a nonzero exit status; stdout remains reserved for JSON.
- No third-party dependencies.

## Out of scope

- Changing the `find-scope-directory` skill's priority order or the separately edited `create-change-summary` and `peer-review` skills.
- Choosing or confirming a scope with the user; this helper only returns candidates.
- Scanning the Git history, staged changes, or diff contents.

## Tasks

### Task 1: Implement the command line helper

1. In `plugins/nag/skills/find-scope-directory/scripts/find_scope_directories.py`, define a `main()` entry point with no required arguments.
2. Discover the repository root with `git rev-parse --show-toplevel` from the command's working directory. Read the branch with `git -C <discovered-root> branch --show-current` using `subprocess.run(..., check=True, capture_output=True, text=True)`.
3. Validate and extract the numeric prefix:

   ```python
   match = re.match(r"^(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*$", branch)
   if match is None:
       fail("branch name must use <issue-number>-<kebab-case-name>")
   issue_number = match.group(1)
   ```

4. Set `specs_dir = repo_root / ".agents" / "specs"`. Examine only its immediate child directories. Keep children whose names match `^<issue_number>-` (escape the prefix when building a regular expression), and retain each only if a recursive search finds at least one regular file with suffix `.md` case-insensitively.
5. Sort the returned paths and emit valid JSON to stdout:

   ```json
   {"folders": ["/path/to/repo/.agents/specs/20-example"]}
   ```

6. Handle expected OS and Git errors without a traceback; return nonzero and explain the problem on stderr.

### Task 2: Connect the helper to the skill

1. In `plugins/nag/skills/find-scope-directory/SKILL.md`, add the command to invoke `scripts/find_scope_directories.py` from inside the target repository when the first three priority cases do not apply.
2. Tell the agent to parse the returned `folders` list as candidates and ask the user to verify the intended scope location, consistent with the skill's existing priority order.

### Task 3: Validate behavior

1. Run the helper on branch `20-update-change-summary` from the repository root with no arguments and confirm valid JSON is emitted.
2. Exercise success and failure cases using temporary directories and a temporary Git repository where needed: invocation from a nested directory, invocation from outside a repository, exact issue prefix, prefix collision, Markdown file at root or nested, no Markdown file, missing `.agents/specs`, and invalid branch.
3. Keep temporary fixtures outside the repository or clean them up after the check.

## Acceptance Criteria

- [ ] `find_scope_directories.py` takes no path argument, discovers the repository root from the command's working directory, and reads the branch from that repository.
- [ ] The `find-scope-directory` skill invokes the helper for its fourth priority from inside the target repository and uses its output as candidates for user verification.
- [ ] It extracts only a numeric issue prefix from a valid kebab-case branch name and rejects invalid branch names.
- [ ] It searches immediate child directories of `<repo-root>/.agents/specs` and matches the issue prefix only at the beginning followed by a hyphen.
- [ ] It includes a candidate only when it contains at least one `.md` file recursively, case-insensitively.
- [ ] It emits a deterministic JSON object with an absolute-path `folders` list, including an empty list when there are no matches or the specs directory is absent.
- [ ] Errors go to stderr with a nonzero status and do not corrupt stdout JSON.
- [ ] The existing uncommitted edits to `plugins/nag/skills/create-change-summary/SKILL.md` and `plugins/nag/skills/peer-review/SKILL.md` are preserved.

## Validation and workflow gaps

- `$check-code-correctness`, `$check-code-quality`, `$check-test-fidelity`, `$check-test-coverage`, and `$mermaid-visualizer` were not found in the installed NAG skill directory or available local copy; report them as unavailable.
- `$run-tests` is disabled and has no configured fast or slow commands in `.agents/NAG-CONFIG.md`; do not invent suite commands.
- `$dead-code-cleanup` is configured disabled/inapplicable because this is not a Python/Poetry application and has no cleanup objective.
- `$test-dashboard` is disabled by configuration; do not generate it.
- `$peer-review` is enabled and must review the implementation against this spec.
- There is no `docs/design/architecture-decision-record.md`; Git root discovery and absolute-path output are recorded here because this small helper has no material architecture decision requiring an ADR.
