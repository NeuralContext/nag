# Feature: Add portable test execution, metrics, and NAG configuration

Make the NAG workflow portable across repositories by separating NAG-wide guidance from repository-specific configuration, adding a canonical `$run-tests` skill for tiered test execution, incorporating a pytest test dashboard as an optional visualization, and making every NAG skill consume the same guidance and configuration contract.

This work targets three initial repository shapes:

| Repository shape | Required behavior |
| --- | --- |
| Python + Poetry + pytest markers | Run `fast` and `slow` marker suites; run `very_slow` only with user approval. |
| Node + npm + Vitest | Run configured npm/Vitest commands without assuming pytest-style markers. |
| Node + npm without Vitest | Run repository-defined npm test commands; do not require or install Vitest. |

The canonical test skill name is `$run-tests`. The canonical test tiers are `fast`, `slow`, and `very_slow`.

## Scope

### In scope

- Portable NAG bootstrap guidance in `AGENTS.md`, `.agents/NAG-AGENTS.md`, and `.agents/NAG-CONFIG.md`.
- A fully specified `.agents/skills/run-tests/SKILL.md` supporting the three test tiers and repository overrides.
- NAG metadata and a common preflight contract in every `.agents/skills/*/SKILL.md`.
- Updates to `$architect-and-orchestrate`, `$create-spec`, `$peer-review`, `$update-agent-guidance`, and other existing skills needed to consume the portable configuration.
- A vendored `$test-dashboard` skill based on `foomoon/test-dashboard`, treated as MIT-licensed per the project decision and accompanied by clear upstream provenance.
- README instructions for installing, configuring, validating, and using NAG in an existing repository.
- Static and scenario-based validation of the skill contracts.

### Out of scope

- Adding or replacing test frameworks in consuming repositories.
- Inventing marker semantics for Vitest or npm projects that do not already distinguish test tiers.
- Making the upstream pytest dashboard support JavaScript/TypeScript test suites.
- Implementing `$mermaid-visualizer` or any other visualization skill.
- Running `very_slow` tests without explicit user approval.
- Modifying the three target consumer repositories as part of this branch.

## Design Decisions

| Decision | Required design |
| --- | --- |
| Test skill name | Use `$run-tests` everywhere. Remove/rename the empty `$test-code` placeholder; do not keep two aliases. |
| Test tiers | Use `fast`, `slow`, and `very_slow`. Run `fast` before `slow`; ask the user before `very_slow`. |
| Guidance filenames | Use `.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md`; update every lowercase reference. |
| Precedence | Active `AGENTS.md` files override repository-specific NAG configuration; `.agents/NAG-CONFIG.md` overrides `.agents/NAG-AGENTS.md`; the active skill supplies the final skill-specific defaults. Non-overridable NAG safety/integrity rules remain higher priority than repository configuration. |
| Missing configuration | Never guess a destructive, networked, or expensive command. Report a missing tier as a validation gap, with the exact configuration entry needed. |
| Dashboard scope | `$test-dashboard` is an optional Python/pytest visualization. Its absence or inapplicability is disclosed, not treated as a `$run-tests` failure. |
| Dashboard import | Vendor the upstream dashboard under `.agents/skills/test-dashboard/`, treat it as MIT-licensed, pin the imported commit, and document provenance and local modifications. |
| Generated artifacts | Test/dashboard artifacts must use a repository-local ignored output path so they can be linked in the orchestrator's final table and do not write into a user's home directory. |
| Design-path overrides | Store the consuming repository's design-document path in `.agents/NAG-CONFIG.md`; `.agents/NAG-AGENTS.md` defines only the default and fallback behavior. |
| Feature artifacts | Group each independent feature in `.agents/specs/<feature-name>/` with paired `spec-vN.md` and `review-vN.md` files plus `change-summary.md`. Multiple feature directories may share one issue/branch. |
| Existing repositories | This repository is greenfield, so no backward-compatible lowercase guidance filenames or `$test-code` alias are required. Version-controlled examples and distribution artifacts must be updated consistently. |

## Configuration Contract

`.agents/NAG-CONFIG.md` is Markdown intended for agents, not a machine-parsed configuration format. It must contain explicit sections with copyable commands and must not contain fake commands that look executable.

Use this minimum structure:

```md
# NAG Repository Configuration

## Repository
- Design documentation: `docs/design/`
- Temporary artifacts: `tmp/`

## `$run-tests`

| Tier | Command | Configured |
| --- | --- | --- |
| `fast` | `<repository command>` | yes/no |
| `slow` | `<repository command>` | yes/no |
| `very_slow` | `<repository command>` | yes/no |

### Test conventions
- Framework: `<pytest | vitest | other>`
- Integration-test infrastructure and allowed mocks: `<repository guidance>`

## `$test-dashboard`
- Enabled: `<yes/no>`
- Output: `tmp/test-dashboard.html`
- Additional configuration: `<none or repository-specific instructions>`

## Skill-specific overrides
### `$skill-name`
<override, exclusion, or additional repository guidance>
```

The distributed template must explain that angle-bracket values are placeholders and must be resolved by `$update-agent-guidance` before the affected skill is considered configured.

## Tasks

### Task 1: Establish portable NAG guidance and filenames

1. Rename the branch's lowercase guidance files:
   - `.agents/nag-agents.md` -> `.agents/NAG-AGENTS.md`
   - `.agents/nag-config.md` -> `.agents/NAG-CONFIG.md`
2. Keep root `AGENTS.md` as the small bootstrap layer. It must:
   - direct agents to read `.agents/NAG-AGENTS.md` before repository work;
   - direct NAG skills to read `.agents/NAG-CONFIG.md` and their corresponding section;
   - explain the precedence contract without duplicating the full NAG guidance;
   - leave a clear location for repository-owned instructions.
3. Refactor `.agents/NAG-AGENTS.md` into reusable NAG-wide defaults:
   - remove nc-algorithm-specific Poetry, database, broker, service/worker, and greenfield assumptions;
   - define instruction precedence and identify non-overridable safety/integrity constraints explicitly;
   - define design-document discovery using the configured path, with `docs/design/` as the default;
   - if the configured/default design directory does not exist, continue with the repository's available maintained documentation and report the missing reference instead of failing on a nonexistent path;
   - define the shared NAG skill preflight and test-tier approval rule;
   - preserve concise code-quality, documentation, scope, and no-commit guidance where it is genuinely cross-repository.
4. Populate `.agents/NAG-CONFIG.md` with the configuration contract above and repository-specific examples for:
   - nc-algorithm/nc-db-style Poetry + pytest marker commands;
   - nc-ui-style npm commands without requiring Vitest;
   - npm + Vitest commands, with repository scripts preferred over direct executable invocation.
5. Update all tracked references and verify no stale lowercase filename remains:

   ```bash
   rg -n "nag-(agents|config)\.md" \
     AGENTS.md README.md .agents/NAG-AGENTS.md .agents/NAG-CONFIG.md .agents/skills
   ```

   This command must not search `.agents/specs/`, where migration instructions may intentionally name the old files.

### Task 2: Add the canonical `$run-tests` skill

1. Remove `.agents/skills/test-code/` and create `.agents/skills/run-tests/SKILL.md`.
2. Define `$run-tests` as an orchestration skill that reads commands from `.agents/NAG-CONFIG.md`; it must not install a framework or rewrite repository test configuration.
3. Specify command resolution in this order:

   ```text
   for tier in [fast, slow]:
       command = NAG_CONFIG.run_tests[tier]
       if command is configured:
           run command
           if it fails because sandbox/network access is restricted:
               request the minimum required approval and retry
           if it fails because tests fail:
               diagnose and fix only when the invoking task authorizes code changes
               otherwise report the failure
       else:
           report tier as not configured

   if very_slow is configured:
       ask user for approval before running
   else:
       report very_slow as not configured
   ```

4. Require each tier to run as a separate command so failures and elapsed time can be attributed correctly. Stop after a failing tier unless the skill's current task explicitly requires collecting all failures.
5. Require a concise result table:

   | Tier | Command | Status | Tests | Duration | Notes |
   | --- | --- | --- | ---: | ---: | --- |

   Use `pass`, `fail`, `not configured`, `not run`, or `declined` for status. Record counts/duration only when the runner output supplies them; do not fabricate metrics.
6. Preserve the integration-test rule as repository-specific configuration rather than hardcoded nc-algorithm guidance. NAG's generic default is to prefer real infrastructure in integration tests; mocks/exceptions must come from the active repository guidance.
7. Update every reference from `$test-code` or an obsolete test skill name to `$run-tests`:

   ```bash
   rg -n "\$(test-code|run-tests)|skills/(test-code|run-tests)" AGENTS.md README.md .agents
   ```

### Task 3: Add shared NAG metadata and skill preflight behavior

1. Update every discoverable `.agents/skills/*/SKILL.md` frontmatter to include:

   ```yaml
   metadata:
     nag: true
   ```

2. Add the following semantic preflight to every NAG skill, using concise wording appropriate to that skill:

   ```text
   1. Read all active AGENTS.md guidance.
   2. Read <repo-root>/.agents/NAG-AGENTS.md.
   3. Read <repo-root>/.agents/NAG-CONFIG.md.
   4. Apply the section for this skill, if present.
   5. If a required file/setting is missing, follow NAG-AGENTS fallback behavior and report the gap.
   ```

3. Do not copy the complete precedence or configuration rules into every skill. Keep the authoritative shared rules in `.agents/NAG-AGENTS.md` and link to them.
4. Audit each skill for hardcoded nc-algorithm assumptions and stale paths. Move legitimate repository-specific commands and exceptions into `.agents/NAG-CONFIG.md`; retain only portable behavior in the skill.
5. Specifically correct known stale references:
   - `$create-spec` must not require nonexistent `CLAUDE.md`, `docs/design/`, or nc-algorithm service/database conventions;
   - `$peer-review` must use one documented review-output path and must handle a configured/missing review-standards path;
   - `$create-change-summary` must not describe itself as nc-algorithm-only;
   - `$dead-code-cleanup` must remain explicitly Python/Poetry-specific and be treated as inapplicable, not broken, in non-Python repositories;
   - `$update-agent-guidance` must populate/resolve `.agents/NAG-CONFIG.md`, including Python-dependent skill applicability, rather than scattering repository-specific commands through every skill.
6. Apply the shared feature-directory contract to `$create-spec`, `$architect-and-orchestrate`, `$peer-review`, and `$create-change-summary`:
   - prefer an explicitly selected or user-named directory;
   - when no name is supplied, use a single uninitialized directory without reading completed feature contents; ask if multiple uninitialized directories exist;
   - when neither is supplied, propose a kebab-case name derived from the branch and requested work and wait for confirmation;
   - allow multiple feature directories with the same issue identifier on one branch;
   - pair `spec-vN.md` with `review-vN.md` and write `change-summary.md` in the same directory;
   - keep the selected directory explicit throughout the workflow rather than rediscovering it from the branch.
7. Make `$create-change-summary` safe on branches containing multiple feature directories:
   - use the selected feature's specs and reviews to identify the intended scope;
   - inspect the complete branch diff, but include only changes clearly attributable to the selected feature;
   - label shared changes as cross-feature and identify the other affected feature directories when known;
   - ask the user rather than guessing when a changed file or hunk cannot be attributed confidently;
   - state in `change-summary.md` that it is feature-scoped rather than a complete branch summary when other feature directories exist.
8. Keep the obsolete `.agents/skills/update-agent-guidance.tar` deleted and remove any remaining references to it. The source directory is the only supported form of this skill.
9. Validate frontmatter and preflight coverage across every skill:

   ```bash
   find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md -print
   rg --files-without-match "nag: true" .agents/skills/*/SKILL.md
   rg --files-without-match "NAG-AGENTS\.md" .agents/skills/*/SKILL.md
   rg --files-without-match "NAG-CONFIG\.md" .agents/skills/*/SKILL.md
   ```

### Task 4: Incorporate `$test-dashboard` as an optional visualization skill

1. Add `.agents/skills/test-dashboard/` from the reviewed upstream source at `https://github.com/foomoon/test-dashboard`, pinned to commit `7918df2e30b643d1d31f009abf43355fc8c3bc9d`, and record:
   - upstream URL;
   - imported commit SHA (`7918df2e30b643d1d31f009abf43355fc8c3bc9d`);
   - import date;
   - local modifications;
   - the project decision to treat the imported source as MIT-licensed, including the applicable MIT license notice;
   - upstream provenance.
2. Preserve the upstream deterministic Python implementation and its requirements (`pytest`, coverage/pytest-cov, and `radon`). Do not claim Node/Vitest support.
3. Adapt its `SKILL.md` to the common NAG metadata and preflight contract.
4. Define an explicit repository-local output interface:
   - add `--out PATH` to `export_test_dashboard_data.py` and default it to `<repo-root>/tmp/test-dashboard-data.json`;
   - continue using the generator's existing `--data PATH` and `--out PATH` arguments, but change its default HTML path from `~/.agent/diagrams/test-dashboard.html` to `<repo-root>/tmp/test-dashboard.html`;
   - create missing parent directories for configured outputs;
   - reject configured output paths that resolve outside the repository root;
   - have the skill resolve `.agents/NAG-CONFIG.md` and always pass both paths explicitly:

     ```bash
     <detected-python> scripts/export_test_dashboard_data.py \
       --out <repo-root>/tmp/test-dashboard-data.json
     <detected-python> scripts/generate_test_dashboard.py \
       --data <repo-root>/tmp/test-dashboard-data.json \
       --out <repo-root>/tmp/test-dashboard.html
     ```

5. Make test failure unambiguous:
   - `export_test_dashboard_data.py` must print the captured pytest output and exit nonzero when its instrumented pytest run fails;
   - it must not publish a new final JSON snapshot after a failed test run;
   - `$test-dashboard` must report `failed` and must not report an existing or partially generated dashboard as current;
   - successful JSON/HTML writes must replace their destination only after generation completes, so a partial write is never presented as a current artifact.
6. Make applicability explicit:

   ```text
   if NAG-CONFIG disables dashboard:
       status = inapplicable
   elif repository is not Python + pytest:
       status = inapplicable
   elif required dashboard dependencies are missing:
       status = unavailable; report exact dependencies
   else:
       generate dashboard and report output path
   ```

7. Do not automatically open a GUI application. Generate the artifact and provide a clickable path; opening it requires an explicit user request and any environment approval.
8. Keep generated data and HTML ignored unless the repository configuration explicitly requires versioning them. Do not hand-edit generated JSON/HTML.
9. Validate the vendored scripts in a temporary Python/pytest fixture when dependencies are available. The check must demonstrate that configured JSON and HTML outputs are created after a passing suite, paths outside the repository are rejected, and a failing suite exits nonzero without publishing a new final snapshot.

### Task 5: Integrate tests and visualizations into `$architect-and-orchestrate`

1. Update `.agents/skills/architect-and-orchestrate/SKILL.md` dependency discovery to use canonical names and applicability states.
2. In each implementation/review iteration:
   - run `$run-tests` after the preceding correctness, quality, fidelity, and coverage checks;
   - require `fast` and `slow` configured suites to pass;
   - never invoke `very_slow` without current user approval;
   - carry missing or inapplicable checks as visible validation gaps.
3. Complete all iterative specs, implementations, validation, and peer reviews before invoking `$test-dashboard` or any other visualization skill. Generate final visualizations only after the final peer review meets the review threshold.
4. If visualization generation identifies a required code or test change, resume the spec/implementation/validation/review loop. Regenerate visualizations only after the new final peer review passes; never treat a stale pre-fix visualization as final.
5. Completion requires the existing peer-review threshold plus passing configured `fast` and `slow` suites. A missing required tier is a disclosed validation gap and prevents an unconditional claim that all validation passed.
6. Present a final developer-review table with one row per artifact/result:

   | Output | Path or result | Status | Notes |
   | --- | --- | --- | --- |
   | Approved implementation spec(s) | `.agents/specs/<feature-name>/spec-vN.md` | ready | Include every iteration in order. |
   | Test results | `$run-tests` summary | pass/gap/fail | Link an artifact if one exists. |
   | Test dashboard | configured path | ready/inapplicable/unavailable | State why when no dashboard exists. |
   | Peer-review comments | `.agents/specs/<feature-name>/review-vN.md` | pass/fail | Pair each review with its spec version and include counts by severity. |
   | PR change summary | `.agents/specs/<feature-name>/change-summary.md` | ready/not requested | Do not invoke `$create-change-summary` unless requested. |

7. Keep artifact generation within authorization boundaries: generating the dashboard does not authorize opening it, and orchestration completion does not authorize committing or creating a PR.

### Task 6: Update installation and workflow documentation

1. Update `README.md` Getting Started instructions so adopters:
   - merge the small NAG bootstrap block into their root `AGENTS.md`;
   - copy/merge `.agents/NAG-AGENTS.md`, `.agents/NAG-CONFIG.md`, and `.agents/skills/`;
   - configure design-document and artifact paths;
   - configure `fast`, `slow`, and `very_slow` commands;
   - run `$update-agent-guidance` and resolve all placeholders before orchestration.
2. Update the workflow and skills table to use `$run-tests`, describe `$test-dashboard` as Python/pytest-only, and distinguish missing, disabled, inapplicable, and unconfigured skills.
3. Document the default `docs/design/` lookup and fallback when it does not exist.
4. Document the instruction/configuration precedence and the rule that consuming repositories own their test commands and infrastructure/mock policy.
5. Update filename casing and skill references throughout README examples.
6. Document feature-directory selection, multiple feature directories per branch, versioned spec/review pairing, and the frozen post-merge lifecycle. Do not create or reference a separate `history/` directory.

### Task 7: Validate the complete portable workflow

1. Run static consistency checks:

   ```bash
   git diff --check
   rg -n "nag-(agents|config)\.md|\$test-code|very_fast" AGENTS.md README.md .agents/NAG-AGENTS.md .agents/NAG-CONFIG.md .agents/skills
   rg --files-without-match "nag: true" .agents/skills/*/SKILL.md
   rg --files-without-match "NAG-AGENTS\.md" .agents/skills/*/SKILL.md
   rg --files-without-match "NAG-CONFIG\.md" .agents/skills/*/SKILL.md
   ```

   The stale-name searches must return no matches; the missing-metadata/preflight searches must return no skill files.
2. Review all Markdown links and every referenced local path. No mandatory instruction may point at an absent file without documented fallback behavior.
3. Exercise `$run-tests` reasoning against temporary fixture configurations for:
   - Poetry + pytest with all three marker commands;
   - npm + Vitest with explicit `fast` and `slow` scripts;
   - npm without Vitest using repository-provided test scripts;
   - missing `slow` configuration;
   - a declined `very_slow` run;
   - a failing `fast` suite.
4. Confirm each fixture yields the required status/result table and that no command is invented for an unconfigured tier.
5. If `$test-dashboard` is incorporated, execute its focused fixture validation from Task 4. Do not run a consuming repository's `very_slow` suite during implementation unless the user separately approves it.
6. Review the final branch diff for generated files, vendored provenance, stale distribution archives, and accidental home-directory paths. Do not commit.

## Acceptance Criteria

- [ ] `.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md` exist; lowercase variants and lowercase references do not.
- [ ] Root `AGENTS.md` is a concise bootstrap and clearly states instruction precedence.
- [ ] `.agents/NAG-CONFIG.md` defines repository-owned design paths, artifact paths, test-tier commands, integration-test policy, dashboard applicability, and skill-specific overrides.
- [ ] `.agents/skills/run-tests/SKILL.md` exists and `$test-code` does not.
- [ ] `$run-tests` uses only `fast`, `slow`, and `very_slow`, runs configured tiers separately, and asks before `very_slow`.
- [ ] `$run-tests` supports Poetry/pytest, npm/Vitest, and npm without Vitest through explicit repository commands without installing or assuming a framework.
- [ ] `$run-tests` reports command, status, available test counts, duration, and validation gaps without fabricating metrics.
- [ ] Every `.agents/skills/*/SKILL.md` contains valid `metadata.nag: true` frontmatter and the shared NAG preflight.
- [ ] Existing skills no longer hardcode nc-algorithm paths, architecture, test markers, infrastructure, or mock exceptions unless provided by repository configuration.
- [ ] Design-document discovery defaults to `docs/design/`, honors configuration, and degrades explicitly when the directory is absent.
- [ ] `$peer-review` has one consistent output path and portable review-standards discovery.
- [ ] `$create-spec`, `$architect-and-orchestrate`, `$peer-review`, and `$create-change-summary` consistently use `.agents/specs/<feature-name>/{spec-vN.md,review-vN.md,change-summary.md}` without assuming one feature per branch.
- [ ] `$create-change-summary` attributes only selected-feature changes, labels shared changes as cross-feature, and asks rather than guessing when attribution is ambiguous.
- [ ] Completed feature directories are documented as frozen, excluded from general context and audits, and readable only by explicit request or historical investigation.
- [ ] `$update-agent-guidance` resolves NAG configuration placeholders and skill applicability for the target repository.
- [ ] The obsolete `update-agent-guidance.tar` artifact and all references to it are removed.
- [ ] `$test-dashboard` is vendored from commit `7918df2e30b643d1d31f009abf43355fc8c3bc9d` under the project's MIT-license assumption and is labeled Python/pytest-only.
- [ ] Dashboard export and generation accept explicit repository-local output paths, write snapshots atomically, reject paths outside the repository, and exit/report failure without publishing a new snapshot when pytest fails.
- [ ] `$architect-and-orchestrate` runs configured `fast` and `slow` suites in each relevant iteration, gates `very_slow`, waits until the iterative peer-review loop is complete before generating final visualizations, and reports validation gaps honestly.
- [ ] The orchestrator's final output table includes specs, test results, dashboard status/path, peer-review results, and PR-summary status.
- [ ] README installation and workflow instructions use the final uppercase filenames, canonical skill names, configuration schema, and portability rules.
- [ ] Static checks and the Python/Node fixture scenarios in Task 7 pass.
- [ ] No changes are committed by the implementing agent.
