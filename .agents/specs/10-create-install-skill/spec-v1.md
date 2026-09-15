# Feature: Create the plugin-delivered `$install-nag` skill

Rename `$update-agent-guidance` to `$install-nag` and expand it into the
developer-facing entry point for installing or updating NAG repository guidance.
The skill must bootstrap the target repository, reconcile an existing NAG
installation safely, and then perform all current `$update-agent-guidance`
auditing and configuration work as the terminal phase of the workflow. It must
leave every change unstaged and uncommitted for the user to review and commit.

## Outcome

A developer with the NAG plugin enabled can run `$install-nag` from a target
repository. The skill installs or updates the repository-owned NAG bootstrap and
configuration, adapts them to the actual repository, validates the result, and
reports the resulting working-tree changes and unresolved gaps. The skill never
copies skills into the repository and never commits on the user's behalf.

## Scope

- Rename `.agents/skills/update-agent-guidance/` to
  `.agents/skills/install-nag/` and rename the skill in its frontmatter and
  instructions.
- Add `.agents/skills/install-nag/scripts/fetch-nag-resources.sh` as the only
  supported mechanism for downloading and verifying pinned NAG resources.
- Make `$install-nag` work for both a repository without NAG guidance and a
  repository with an existing NAG installation.
- Update the new `$install-nag` skill so it does the following when executed:
  - Merge the NAG bootstrap block into the target root `AGENTS.md` without
    discarding repository-owned instructions.
  - Create or update `.agents/NAG-AGENTS.md` and create or reconcile
    `.agents/NAG-CONFIG.md` using verified canonical files fetched from the
    commit-pinned public NAG repository.
  - Preserve repository ownership of `AGENTS.md` additions and resolved
    `.agents/NAG-CONFIG.md` values.
  - Update maintained documentation and live configuration references from `$update-agent-guidance` to `$install-nag`.
  - Leave all changes unstaged and uncommitted for user review.
  - Prompt the user whether they would like the items in the `.codex/` folder
    updated with NAG presets (recommended).
  - Fetch initial authoritative copies of `.agents/NAG-CONFIG.md`,
    `.agents/NAG-AGENTS.md`, and the `AGENTS.md` NAG bootstrap from the public
    NAG GitHub repository at `https://github.com/NeuralContext/nag`.
    - Use a reviewed full commit hash and verify downloaded content as described
      below.
- `$install-nag` should include every existing `$update-agent-guidance` capability as the final audit,
  configuration-resolution, validation, and reporting phase.


## Exclusions

- Do not design or implement the plugin, plugin manifest, marketplace entry,
  plugin installation flow, or plugin release/versioning mechanism. The NAG
  plugin and all NAG skills are assumed to be available before invocation.
- Do not copy, install, update, or delete `.agents/skills/` in the target
  repository. Skills are provided by the plugin.
- Plugin installation makes the repository-copying instructions for skills and agent configuration obsolete.
- Do not stage, commit, push, create a pull request, or change branches.
- Do not modify application code merely to make generated guidance valid.
- Do not rewrite frozen feature history under `.agents/specs/` to replace old
  `$update-agent-guidance` references. Historical specs remain unchanged.

## Constraints and assumptions

- The plugin is the authoritative source for `$install-nag` and all other NAG
  skills. A reviewed, full Git commit hash in the public
  `NeuralContext/nag` repository is the authoritative source revision for the
  repository bootstrap/configuration files and optional `.codex/` presets used
  when the skill executes.
- The implementation must record one immutable, full commit hash rather than a
  branch, tag, abbreviated hash, or dynamically discovered latest revision.
  The pinned commit is
  `fcbc43b9af615cfdd564e84c127e41909be95575`.
- Fetching pinned public files is expected runtime behavior, but it remains
  subject to the agent host's network permission/approval controls. If access
  is denied or unavailable, fail before modifying target files and report the
  exact URLs that could not be retrieved.
- A commit-addressed URL provides version pinning but does not itself verify the
  returned bytes. Record expected checksums for every fetched file and verify
  all downloads in a temporary directory before applying any target changes.
- `$install-nag` normally targets the repository/worktree in which the agent is
  operating. It must resolve and report the target repository root before
  writing files; it must not accept an unrelated source checkout or copy skills
  between repositories.
- A missing `.agents/NAG-AGENTS.md` or `.agents/NAG-CONFIG.md` is expected during
  a first installation and must not cause the normal NAG preflight to fail.
- Platform safety and active target-repository `AGENTS.md`/
  `AGENTS.override.md` instructions remain authoritative. NAG invariants cannot
  be weakened by installation or repository configuration.
- Existing user changes may be present. The implementation must inspect and
  preserve unrelated changes and must not use destructive Git commands.
- Repository-specific values belong in `.agents/NAG-CONFIG.md` or the target's
  active `AGENTS.md`; portable guidance must remain repository-agnostic.
- Angle-bracket values are unresolved placeholders. An affected capability is
  unconfigured until `$install-nag` resolves the value from repository evidence.
- Moderate-or-higher-risk, security-sensitive, ambiguous, or destructive
  changes require user approval before they are applied. Low-risk, verified
  guidance/configuration changes are within the skill's normal authority.
- NAG's configured `fast`, `slow`, and `very_slow` test-tier rules continue to
  apply. `$install-nag` must never run `very_slow` without explicit approval in
  the current workflow.

## Implementation changes in this repository

| File/component | Required change |
| --- | --- |
| `.agents/skills/update-agent-guidance/SKILL.md` | Move to `.agents/skills/install-nag/SKILL.md`; replace the old skill identity and expand the workflow. |
| `.agents/skills/install-nag/scripts/fetch-nag-resources.sh` | Add an executable, deterministic downloader that owns the pinned commit, exact URLs, checksums, staging, verification, and failure cleanup. |
| `.agents/NAG-CONFIG.md` | Rename the skill configuration section and references to `$install-nag`; preserve the current guidance intent. |
| `README.md` | Replace the manual existing-repository copy procedure with the plugin assumption and `$install-nag` workflow; rename skill references and table entry. |
| `docs/design/overview.md` | Describe `$install-nag` as the repository bootstrap and reconciliation entry point. |
| Live non-historical references found by `rg` | Rename applicable references; do not alter frozen `.agents/specs/` history. |

These are the changes the implementation agent makes while implementing this
spec. It must not execute `$install-nag` against an unrelated repository as
part of implementation.

## Target files affected when `$install-nag` executes

| Target file/component | Runtime behavior |
| --- | --- |
| `AGENTS.md` | Merge or update only the NAG bootstrap block while preserving repository-owned guidance. |
| `.agents/NAG-AGENTS.md` | Initialize or update portable guidance from the verified, commit-pinned public source. |
| `.agents/NAG-CONFIG.md` | Initialize from the verified, commit-pinned public source, then reconcile it to the target repository. Preserve resolved repository-owned values on updates. |
| `.codex/config.toml` | Only after the user accepts the recommended `.codex` update; merge applicable NAG presets without discarding unrelated local settings. |
| `.codex/agents/implementer.toml` | Only after the user accepts the recommended `.codex` update; create or reconcile the NAG implementer preset without replacing unrelated agents. |
| Target documentation/guidance containing live `$update-agent-guidance` references | Rename applicable live references to `$install-nag`; do not rewrite frozen feature history. |

The pinned source may contain other `.codex/` files in the future. This feature
does not authorize installing an open-ended directory. The skill must name the
supported preset files explicitly and require a later reviewed skill change to
expand that set.

The implementation agent must discover the complete live reference set before
editing:

```bash
rg -n "update-agent-guidance|Update Agent Guidance" \
  README.md docs .agents .codex \
  --glob '!.agents/specs/**'
```

## Design decisions

### 1. One public install-and-update entry point

`$install-nag` is idempotent and selects its mode from target state; users do
not choose between separate install and update skills.

```text
target repository resolved
        |
        v
inspect AGENTS.md, NAG-AGENTS.md, and NAG-CONFIG.md
        |
        +-- required NAG files absent ------> fresh installation
        |
        `-- required NAG files present -----> update/reconciliation
                                                |
                                                v
                              terminal guidance audit and validation
                                                |
                                                v
                                unstaged diff for user review
```

Mode affects how missing files are interpreted, not the final quality bar. Both
modes finish with the same repository discovery, configuration resolution,
placeholder scan, safe validation, and report.

### 2. Explicit ownership and merge policy

| Target content | Ownership | Required behavior |
| --- | --- | --- |
| Root `AGENTS.md` outside the NAG bootstrap block | Repository | Preserve except for separately justified low-risk corrections requested by the user. |
| Root `AGENTS.md` NAG bootstrap block | NAG | Extract from the verified, commit-pinned public `AGENTS.md`; insert when absent, update in place when identifiable, and never duplicate it. |
| `.agents/NAG-AGENTS.md` portable defaults/invariants | NAG | Fetch from the verified, commit-pinned public source and reconcile to that canonical version. Surface ambiguous local divergence before replacement. |
| `.agents/NAG-CONFIG.md` | Repository | Initialize from the verified, commit-pinned public template; merge/reconcile on update and preserve verified repository values and overrides. Never blindly replace it. |
| `.agents/skills/` | Plugin | Do not create, copy, update, or delete repository-local skills. |
| Supported `.codex/` preset files | Shared | Offer a recommended opt-in update, then merge only supported NAG preset values while preserving unrelated target settings. Do nothing if declined. |

The root bootstrap must be small and recognizable. Prefer stable marker comments
around the pinned public block so later runs can update it deterministically,
provided the resulting `AGENTS.md` remains valid guidance. For example:

```markdown
<!-- NAG:START -->
## NAG workflow

Before performing repository work, read and follow
`.agents/NAG-AGENTS.md`.

When invoking a NAG skill, also read `.agents/NAG-CONFIG.md` and apply
the sections required by that skill.
<!-- NAG:END -->
```

The canonical block may contain the complete precedence wording from the
repository template. The implementation must use one canonical form and make a
second run produce no additional edit.

### 3. Commit-pinned, verified remote source

Create `.agents/skills/install-nag/scripts/fetch-nag-resources.sh`. The script,
not free-form skill instructions, owns the immutable source manifest, URL
construction, network transfer, checksum verification, staging lifecycle, and
machine-readable success/failure contract. `$install-nag` must invoke this
script every time it needs canonical resources and must not independently
construct URLs, download files, or decide whether integrity checks can be
skipped.

The script must hard-code this reviewed manifest with no runtime override:

```yaml
repository: https://github.com/NeuralContext/nag
raw_repository: https://raw.githubusercontent.com/NeuralContext/nag
commit: fcbc43b9af615cfdd564e84c127e41909be95575
files:
  - source: AGENTS.md
    purpose: extract-nag-bootstrap
    sha256: 2c82fbaa129fbb4a486797e4971fd89fc0bc2497578093529627cb960a32b88e
  - source: .agents/NAG-AGENTS.md
    target: .agents/NAG-AGENTS.md
    sha256: 233a48a54f9ebdf91e3e62c5f4356c47e5d93042ae87e90a50930e4db8fd0237
  - source: .agents/NAG-CONFIG.md
    target: .agents/NAG-CONFIG.md
    sha256: 21a0386b40f21bde39306db7c82e2cd81d1c4c8f8bba3d8bc0b86c69b0600a5e
  - source: .codex/config.toml
    target: .codex/config.toml
    optional_group: codex-presets
    sha256: 17f559bed7055b75f6561870c1df642f43fffad66c0e1401b2a9ced6adeb8c97
  - source: .codex/agents/implementer.toml
    target: .codex/agents/implementer.toml
    optional_group: codex-presets
    sha256: 3ec363539088722648b3880776efd2b58537308087bef8607809f10718f65bda
```

Use only URLs with the exact form:

```text
https://raw.githubusercontent.com/NeuralContext/nag/fcbc43b9af615cfdd564e84c127e41909be95575/{PATH}
```

The script interface is:

```text
fetch-nag-resources.sh [--include-codex]

stdout on success: one absolute path to the verified staging directory
stderr: diagnostics only
exit 0: every selected resource was downloaded and verified
exit 2: invalid arguments or missing required local command
exit 3: network/HTTP/redirect failure
exit 4: checksum or downloaded-file validation failure
```

The script must require only Bash plus explicitly checked common commands such
as `curl`, `sha256sum`, `mktemp`, and `rm`. It must check dependencies before
network access and report missing commands without attempting package
installation. Do not accept a commit, repository, raw base URL, checksum, or
output directory from environment variables or command-line arguments.

The runtime algorithm must fail closed and remain deterministic:

```pseudo
PINNED_COMMIT = "fcbc43b9af615cfdd564e84c127e41909be95575"
manifest = hard_coded_manifest()
assert manifest.commit == PINNED_COMMIT
check_required_commands()

staging_dir = mktemp_directory()
register_failure_cleanup(staging_dir)

selected = required_files(manifest)
if argument_present("--include-codex"):
    selected += codex_files(manifest)

for file in selected:
    destination = safe_join(staging_dir, file.source)
    create_parent_directories(destination)
    curl(
        fail_on_http_error = true,
        https_only = true,
        exact_pinned_url = file.source,
        destination = destination,
    )
    require(sha256(destination) == file.sha256)

validate_expected_paths_and_basic_markdown_toml_shapes(staging_dir, selected)
disable_failure_cleanup()
print_absolute_path_only(staging_dir)
exit(0)
```

Partial downloads exist only inside the script-created staging directory. On
any nonzero exit or signal, remove that exact staging directory and print no
stdout path. On success, retain it for `$install-nag`; the skill must remove the
exact returned directory after applying or abandoning merges. A transport
staging directory is ephemeral input, not a generated NAG artifact.

Do not execute downloaded content, fetch a branch/tag/`HEAD`, accept a checksum
mismatch, or fall back to an unpinned/local template. Clean up temporary files
after success or failure. The script must never write `AGENTS.md`, `.agents/`,
or `.codex/` in the target repository. The skill begins target inspection and
merge work only after the script returns exit `0` and a valid staging path.

### 4. Install-aware preflight

The current preflight assumes the NAG files already exist. `$install-nag` must
instead use this ordering:

```text
1. Resolve the target repository root.
2. Read all active target AGENTS.md and AGENTS.override.md files that apply.
3. Inventory existing .agents/NAG-AGENTS.md and .agents/NAG-CONFIG.md if present.
4. Ask whether to update supported `.codex/` presets, presenting yes as the
   recommended choice and making clear which files may change.
5. Invoke `scripts/fetch-nag-resources.sh`, adding `--include-codex` only when
   the user accepted the preset update. Do not reproduce its download logic in
   skill prose or ad hoc commands.
6. Require script exit `0`, capture its single stdout staging path, and verify
   that the returned directory exists before reading staged resources.
7. Classify fresh install versus update and identify conflicts.
8. Ask before any ambiguous or moderate-or-higher-risk merge.
9. Write approved bootstrap/guidance/configuration and optional preset changes.
10. Remove the exact verified staging directory.
11. Re-read the installed NAG guidance and configuration.
12. Run the terminal repository-guidance audit.
```

Absence of NAG files in steps 2-3 is installation state, not a configuration
gap. A denied/failed fetch, missing file at the pinned commit, unexpected
redirect, checksum mismatch, or invalid downloaded file is a blocker: report it
and do not partially install or fabricate portable guidance.

### 5. Existing guidance-update behavior is the terminal phase

After bootstrap/update writes, `$install-nag` must retain and execute all
behavior currently specified by `$update-agent-guidance`:

```text
discover sources of truth
  -> inventory active guidance and plugin-provided skill requirements
  -> inspect language/package manifests, scripts, CI, formatter/linter/test
     configuration, and maintained documentation
  -> preserve multi-language components and their package managers

resolve NAG configuration
  -> design-document, artifact, review-standard, and ADR paths
  -> separate fast, slow, and very_slow commands
  -> framework, integration infrastructure, and allowed-mock policy
  -> test-dashboard applicability and repository-local outputs
  -> each language-dependent skill's Enabled: yes/no decision and rationale
  -> repository-specific overrides
  -> all affected angle-bracket placeholders

audit and validate
  -> verify every referenced path, command, environment variable, service,
     workflow, and plugin-provided skill prerequisite
  -> remove only demonstrably stale references
  -> preserve intentional external/optional references
  -> rescan paths and placeholders
  -> run safe lightweight validations
  -> report changes, decisions, gaps, and command results
```

The renamed skill must preserve these existing constraints:

- Prefer existing Poetry, uv, npm, or other framework scripts over direct test
  executables.
- Never install or require Vitest merely because a repository uses npm.
- Never translate a required Python script into another language.
- If Python availability for a Python-dependent skill cannot be established
  safely, report an unresolved applicability decision rather than deleting or
  rewriting the skill.
- Missing test-tier commands remain explicitly unconfigured; never invent an
  executable example.
- Do not change application code to satisfy guidance.

Because skills are plugin-provided, inventory the plugin-visible NAG skills and
their declared requirements through available skill metadata/resources. Do not
require repository-local `.agents/skills/*/SKILL.md` files and do not install
them when absent.

### 6. User-owned completion

The final action is a report, not a commit. The report must make review easy:

```markdown
## NAG installation result

- Mode: fresh install | update
- Target: <resolved repository root>
- Files added: ...
- Files modified: ...
- Existing values preserved: ...
- Pinned source commit: ...
- Download verification: ...
- `.codex` preset choice: accepted | declined
- Applicability decisions: ...
- Unresolved gaps/placeholders: ...
- Validation commands and results: ...
- Git state: changes are unstaged and uncommitted
- Next action: review the diff and commit it when satisfied
```

The skill may use read-only Git inspection such as `git status --short` and
`git diff --check`. It must not execute `git add`, `git commit`, `git push`,
branch-changing commands, or pull-request creation commands.

## Tasks

### Task 1: Rename the skill and all maintained references

1. Move the source skill directory:
   - Move `.agents/skills/update-agent-guidance/SKILL.md` to
     `.agents/skills/install-nag/SKILL.md`.
   - Remove the now-empty `update-agent-guidance` directory.
   - Do not leave an alias skill or compatibility shim unless the user expands
     the scope later.
2. Update skill identity:
   - Set frontmatter `name: install-nag`.
   - Keep `metadata.nag: true`.
   - Change the description to state that the skill installs or updates NAG
     repository guidance, reconciles configuration, validates it, and leaves
     changes for user review.
   - Change the heading to `# Install NAG`.
3. Update live references found with `rg`:
   - Rename the `.agents/NAG-CONFIG.md` section heading to
     `### $install-nag` (with the skill name formatted as inline code).
   - Replace explanatory references in `.agents/NAG-CONFIG.md`, `README.md`,
     and `docs/design/overview.md`.
   - Update the README skill table link to
     `.agents/skills/install-nag/SKILL.md`.
   - Do not edit prior feature specs merely to rename historical references.
4. Verify no maintained, non-historical `$update-agent-guidance` reference
   remains and no new repository-local skill-copy instruction remains.

### Task 2: Define installation and update behavior

1. Replace the old preflight with the install-aware preflight in this spec.
2. Direct the skill to resolve and disclose the target repository root before
   making changes.
3. Create
   `.agents/skills/install-nag/scripts/fetch-nag-resources.sh` with the exact
   constants, resource paths, and checksums in Design Decision 3:
   - Hard-code commit `fcbc43b9af615cfdd564e84c127e41909be95575`.
   - Do not expose source, commit, checksum, or output-location overrides.
   - Support no argument for required resources and exactly
     `--include-codex` for required plus optional preset resources.
   - Check Bash runtime dependencies without installing them.
   - Use HTTPS-only `curl`, do not follow redirects, and require HTTP `200`.
   - Download to a script-created temporary directory without touching target
     repository files.
   - Verify SHA-256 and basic expected file shape for every selected resource.
   - On failure or signal, delete only the exact script-created staging
     directory, emit diagnostics on stderr, print no stdout path, and return the
     documented nonzero code.
   - On success, print only the absolute verified staging path and leave that
     directory for the caller to consume and remove.
4. Update `SKILL.md` to use the script as the exclusive resource-fetch path:
   - Never reproduce downloads with ad hoc agent-authored `curl`, Git, browser,
     or other commands.
   - Interpret a nonzero script exit as a blocker before target writes.
   - Capture the successful stdout path, read resources only under that path,
     and remove exactly that path after merges or abandonment.
   - Report the script path, pinned commit, and verification result.
5. Prompt once for the optional `.codex` preset group before invoking the script:
   - Recommend accepting the presets.
   - Identify `.codex/config.toml` and
     `.codex/agents/implementer.toml` before the user decides.
   - If declined, invoke the script without `--include-codex` and do not modify
     optional preset files.
   - If accepted, invoke it with `--include-codex` and merge the verified files
     without discarding unrelated target configuration or agent definitions.
6. Define deterministic state classification:

   ```pseudo
   existing = inspect(AGENTS.md, NAG_AGENTS.md, NAG_CONFIG.md)

   if NAG_AGENTS.md is absent and NAG_CONFIG.md is absent:
       mode = FRESH_INSTALL
   else:
       mode = UPDATE

   if only one required NAG file exists:
       record partial_installation_gap()
       mode = UPDATE
   ```

7. Specify safe bootstrap merging:
   - Create root `AGENTS.md` if absent.
   - Insert the canonical NAG block if absent while retaining existing content.
   - Replace exactly one recognized prior/canonical NAG block during an update.
   - If multiple or materially edited candidate blocks exist, show the conflict
     and ask before changing them.
   - Rescan to prove exactly one effective bootstrap block remains.
8. Specify NAG guidance/configuration handling:
   - Create missing `.agents/` parents as necessary.
   - Render the verified canonical `.agents/NAG-AGENTS.md` on a fresh install.
   - Reconcile portable guidance on update; do not silently discard ambiguous
     target modifications.
   - Initialize `.agents/NAG-CONFIG.md` from the verified canonical public
     template when absent.
   - Merge an existing configuration by section/key, retaining verified paths,
     commands, policies, overrides, enablement choices, and rationales.
   - Do not overwrite a resolved repository value with a template placeholder.
9. Make repeated execution idempotent: after a successful run with no target
   repository changes, another run must not alter files solely due to formatting,
   ordering, duplicate bootstrap insertion, or template defaults.

### Task 3: Append the complete repository-guidance reconciliation phase

1. Preserve the current skill's `Discover sources of truth` responsibilities,
   adapting skill discovery to the plugin rather than `.agents/skills/`.
2. Preserve every item under the current `Resolve NAG configuration` section.
3. Rename configuration and prose references from
   `$update-agent-guidance` to `$install-nag`.
4. Perform repository discovery only after the verified bootstrap and canonical
   portable guidance are present, so the terminal phase evaluates the installed
   result.
5. Keep repository-specific information out of portable skill instructions and
   `.agents/NAG-AGENTS.md`; place it in `.agents/NAG-CONFIG.md` or active target
   guidance.
6. Preserve approval boundaries and do not mutate application code.
7. End with the placeholder/path rescan, safe lightweight validation, and the
   structured installation report defined above.

### Task 4: Update README installation and skill documentation

1. Rewrite `README.md`'s `Adding to an Existing Repo` section around the plugin
   workflow:

   ```text
   Prerequisite: the NAG plugin is installed/enabled.
   1. Open the target repository with the appropriate agent/model.
   2. Run $install-nag.
   3. Approve network access required to retrieve the commit-pinned public
      bootstrap/configuration files.
   4. Choose whether to apply the recommended .codex presets.
   5. Resolve any decisions or gaps reported by the skill.
   6. Review the unstaged diff.
   7. Commit the changes only when satisfied.
   ```

2. Remove instructions to copy `.agents/skills/` or manually copy `.codex/`, and
   remove the manual instruction to run `$update-agent-guidance` after copying
   files. Distinguish that `$install-nag` can offer a recommended, explicit
   `.codex` preset update when it executes.
3. Explain succinctly that `$install-nag` supports both initial setup and later
   reconciliation/update runs.
4. Update the language-dependent-skill explanation to name `$install-nag` as
   the skill that records applicability.
5. Update the skills table name, link, and summary.
6. Document that initial bootstrap/configuration inputs are fetched from a
   the fixed commit
   `fcbc43b9af615cfdd564e84c127e41909be95575` in the public NAG GitHub
   repository by the skill's deterministic fetch script and verified before
   target writes. Do not imply that a branch or latest release is used or that
   the agent assembles its own download commands.
7. Keep the process overview focused on repository use; do not document plugin
   packaging or installation mechanics in this feature.

### Task 5: Update design documentation

1. In `docs/design/overview.md`, replace the bootstrap reference to
   `$update-agent-guidance` with `$install-nag`.
2. State at a high level that the plugin supplies skills while repository-owned
   configuration keeps commands, paths, and policies local to each repository.
3. State that canonical initial repository guidance/configuration comes from a
   verified, commit-pinned public NAG source. Keep checksum and merge mechanics
   in the skill/spec rather than the design overview.
4. Do not add implementation-level copying or merge algorithms to the design
   overview.
5. The configured ADR path is absent. If implementation reveals a material
   architectural decision beyond those explicitly settled in this spec, report
   the ADR gap and ask the user before creating a new ADR location.

### Task 6: Validate the renamed skill and documentation

1. Confirm the skill layout and frontmatter:

   ```bash
   test -f .agents/skills/install-nag/SKILL.md
   test ! -e .agents/skills/update-agent-guidance
   test -x .agents/skills/install-nag/scripts/fetch-nag-resources.sh
   bash -n .agents/skills/install-nag/scripts/fetch-nag-resources.sh
   rg -n '^name: install-nag$|^metadata:|^[[:space:]]+nag: true$' \
     .agents/skills/install-nag/SKILL.md
   ```

2. Search for stale maintained references while excluding frozen feature
   history:

   ```bash
   rg -n "update-agent-guidance|Update Agent Guidance" \
     README.md docs .agents/NAG-AGENTS.md .agents/NAG-CONFIG.md \
     .agents/skills .codex
   ```

   Expected result: no live reference. References inside prior
   `.agents/specs/<other-feature>/` directories are allowed and must remain
   unchanged.
3. Search for obsolete repository-copy instructions:

   ```bash
   rg -n "copy.*\.agents/skills|copy.*\.codex" README.md docs \
     .agents/skills/install-nag/SKILL.md
   ```

   Expected result: no instruction for `$install-nag` users to copy those
   directories manually. The skill's recommended opt-in `.codex` preset merge
   is allowed and must not be described as plugin installation.
4. Validate the deterministic fetch script:
   - The repository is exactly `https://github.com/NeuralContext/nag`.
   - The commit is exactly
     `fcbc43b9af615cfdd564e84c127e41909be95575`; no branch, tag,
     abbreviated hash, placeholder, override, or runtime latest-version lookup
     is accepted.
   - Each required and optional source path has the exact SHA-256 checksum from
     Design Decision 3.
   - Exact commit-pinned raw URLs are publicly retrievable during implementation.
   - Downloaded bytes match the recorded checksums.
   - The script is the only fetch mechanism described by `SKILL.md`.
   - The script emits only the verified absolute staging path on stdout after
     the complete selected set passes and never writes target files.
5. Execute focused script validation with any required network approval:
   - Run without arguments and verify that only the three required resources
     exist under the returned staging directory.
   - Run with `--include-codex` and verify that all five resources exist.
   - Independently hash every staged file and compare it to Design Decision 3.
   - Verify an unsupported argument exits `2`, emits no staging path, and does
     not leave a staging directory.
   - Remove only the exact successful staging directories after inspection.
6. Review the skill instructions and script for these runtime scenarios:

   | Scenario | Expected result |
   | --- | --- |
   | Required download fails or checksum differs | Abort with no target writes. |
   | Fresh target, `.codex` accepted | Install guidance/configuration and merge both supported presets. |
   | Fresh target, `.codex` declined | Install guidance/configuration; do not fetch or modify `.codex`. |
   | Existing customized `NAG-CONFIG.md` | Preserve verified repository values while updating structure/references. |
   | Existing unrelated `AGENTS.md` content | Preserve it and leave exactly one NAG bootstrap block. |
   | Second run with unchanged inputs | Produce no avoidable diff. |

7. Verify Markdown links and all paths named by the modified documentation.
8. Run lightweight repository checks:

   ```bash
   git diff --check
   git status --short
   ```

9. Do not invoke `$run-tests`; it is disabled for this skill/script/documentation
   repository change and no configured test commands exist.
10. Do not invoke `$dead-code-cleanup`; it is configured as disabled and
   inapplicable to this non-Python/Poetry repository.
11. Inspect the final diff and confirm no application code, historical feature
   specs, `.agents/skills/` other than the rename, or `.codex/` files were
   changed unexpectedly.
12. Report validation results and explicitly state that the implementation
   remains unstaged and uncommitted for the user to review and commit.

## Acceptance Criteria

- [ ] `.agents/skills/update-agent-guidance/` is renamed to
  `.agents/skills/install-nag/`, and its frontmatter name is `install-nag` with
  `metadata.nag: true`.
- [ ] `$install-nag` is documented as the single idempotent entry point for both
  fresh NAG repository setup and later NAG guidance/configuration updates.
- [ ] The skill assumes all NAG skills are plugin-provided and does not copy,
  install, update, or remove repository-local `.agents/skills/` content.
- [ ] The implementation adds executable
  `.agents/skills/install-nag/scripts/fetch-nag-resources.sh`, and `SKILL.md`
  requires this script as the exclusive resource-fetch mechanism on every run.
- [ ] The script hard-codes
  `fcbc43b9af615cfdd564e84c127e41909be95575` and the exact HTTPS source paths
  for `AGENTS.md`, `.agents/NAG-AGENTS.md`, `.agents/NAG-CONFIG.md`,
  `.codex/config.toml`, and `.codex/agents/implementer.toml`; it accepts no
  source, commit, checksum, destination, branch, tag, `HEAD`, or latest-version
  override.
- [ ] Every fetched file has the exact SHA-256 checksum specified in Design
  Decision 3, and the script requires all selected downloads and file-shape
  checks to pass before returning a staging path.
- [ ] The script never writes target repository files, prints only one verified
  absolute staging path on successful stdout, cleans its exact staging directory
  on failure, and returns documented deterministic exit codes.
- [ ] Network denial/failure, an unexpected redirect, missing pinned content,
  invalid file shape, or checksum mismatch aborts without a partial install.
- [ ] The skill prompts whether to update the two supported `.codex` preset
  files, recommends acceptance, names the affected files, changes nothing in
  `.codex/` when declined, and preserves unrelated settings when accepted.
- [ ] The skill resolves the target repository root and reads active existing
  repository guidance before writing changes.
- [ ] Fresh installation creates/merges the root `AGENTS.md` NAG bootstrap and
  initializes `.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md` from verified,
  commit-pinned public resources.
- [ ] Update mode updates one identifiable NAG bootstrap without duplication,
  reconciles portable NAG guidance, and preserves verified repository-owned
  configuration and unrelated `AGENTS.md` content.
- [ ] Missing or partial prior installation is handled as install/update state,
  while inaccessible or unverifiable pinned resources are reported as a blocker
  rather than fabricated or replaced with an unpinned fallback.
- [ ] Ambiguous local modifications, moderate-or-higher-risk changes,
  security-sensitive changes, and destructive changes require user approval.
- [ ] A second successful run against unchanged repository state produces no
  formatting churn, duplicate bootstrap, or other avoidable diff.
- [ ] The final phase preserves every existing `$update-agent-guidance`
  capability: source discovery, manifest/script/CI/documentation audit,
  NAG configuration resolution, language-dependent skill applicability,
  placeholder resolution, reference validation, lightweight checks, and gap
  reporting.
- [ ] Missing test commands remain unconfigured, repository commands are never
  invented, and application code is not changed to satisfy guidance.
- [ ] `README.md`, `.agents/NAG-CONFIG.md`, and `docs/design/overview.md` use
  `$install-nag`; the README skill table links to the renamed skill.
- [ ] README installation guidance assumes an already available plugin and
  directs the user to run `$install-nag`, permit the pinned fetch, choose whether
  to update recommended `.codex` presets, resolve reported decisions, review the
  unstaged diff, and commit only when satisfied.
- [ ] Maintained live references to `$update-agent-guidance` are removed without
  rewriting frozen feature-spec history.
- [ ] `$install-nag` never stages, commits, pushes, changes branches, or creates
  a pull request; its terminal report explicitly says changes are unstaged and
  uncommitted and that review/commit belong to the user.
- [ ] `git diff --check` passes, paths and Markdown links in changed files are
  valid, and the final diff contains only the intended skill, configuration,
  README, and design-document changes.

## Dependencies, fallbacks, gaps, and risks

- **Pinned public source:** Commit
  `fcbc43b9af615cfdd564e84c127e41909be95575` is intentionally fixed and
  predates this rename. Fetched live `$update-agent-guidance` references are
  expected inputs to the terminal reconciliation phase, which must convert them
  to `$install-nag`. Updating the pinned source later requires a reviewed script
  change with new checksums.
- **Supply-chain verification:** A commit in a URL provides immutability of the
  requested name, not independent verification of returned bytes. Recorded
  checksums and fail-before-write behavior are required. This does not eliminate
  compromise of the reviewed source before pinning; commit selection remains a
  release-review responsibility.
- **Network availability:** Initial installation and source-based updates need
  network permission. There is no unpinned, cached, plugin-template, or branch
  fallback. Report the exact failure and leave the target unchanged.
- **Runtime dependencies:** The script depends on Bash, `curl`, `sha256sum`,
  `mktemp`, and basic filesystem commands. Missing dependencies make the fetch
  unavailable; the skill reports them and does not install packages or replace
  the deterministic script with improvised commands.
- **Optional `.codex` merge:** TOML and agent presets may contain target-specific
  settings. Acceptance authorizes a merge, not wholesale replacement. If a
  conflict cannot be resolved safely, preserve the target value and report it.
- **Merge ambiguity:** Existing repositories may have copied and edited NAG
  guidance without markers or provenance. The skill must prefer disclosure and
  user approval over silent replacement when ownership cannot be established.
- **Configuration preservation:** A naive template replacement could erase real
  repository commands or policies. Section/key reconciliation and the rule
  against replacing resolved values with placeholders are required safeguards.
- **Plugin skill discovery:** The exact runtime interface for enumerating other
  plugin-delivered skills may differ by agent host. Use the host's available
  skill metadata/resources; if unavailable, report the applicability audit gap
  without recreating repository-local skill copies.
- **No configured automated suite:** `$run-tests` is disabled in this repository.
  Validation is therefore structural, reference-based, Markdown/link-oriented,
  and diff-based unless repository configuration changes before implementation.
- **Review standards:** No external review-standard path or ADR path is
  configured. `$peer-review` must use its embedded standards, and material new
  architecture decisions must be reported rather than written to an invented
  ADR location.
