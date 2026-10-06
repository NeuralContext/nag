# Feature: Fetch NAG initialization presets from templates

Update `$configure-nag` to retrieve reusable Codex presets from
`templates/.codex/` in the public NAG repository, and pin all initialization
resources to commit `ba3bfe15408d523db5df467d72601493b294368e` with matching
SHA-256 checksums. Consuming repositories continue to receive presets in
`.codex/`; the source repository's active Codex configuration is no longer the
preset source.

## Outcome and Scope

- Change `plugins/nag/skills/configure-nag/scripts/fetch_nag_resources.py`:
  update `PINNED_COMMIT`, every resource checksum, and the two preset source paths.
- Change `plugins/nag/skills/configure-nag/SKILL.md`: synchronize the documented
  pin and explicitly map verified staged templates to consuming-repository files.
- Update the `.codex` row in `README.md` and add a `templates/.codex/` row so
  installation documentation distinguishes active repository settings from presets.
- Preserve optional `--include-codex`, checksum verification, fail-closed
  behavior, cleanup, prompts, repository-value preservation, and idempotent merges.

Exclusions: no changes to preset contents, active `.codex` configuration,
repository-owned `.agents` guidance, other skills, dependency installation,
symlink resolution, network fallback, or the configuration merge algorithm.
Do not run `$configure-nag` against this repository as part of implementation.
Leave changes unstaged and uncommitted; do not change branches.

## Context and Interfaces

The fetcher stores each resource as `(resource_path, expected_checksum,
resource_kind)`. `download_resource()` uses the same path both to construct the
commit-pinned raw URL and to stage verified bytes. Retain this interface:

```python
url = f"{RAW_REPOSITORY}/{PINNED_COMMIT}/{resource_path}"
destination = staging_directory / resource_path
```

The CLI remains `fetch_nag_resources.py [--include-codex]`. Success writes only
the absolute staging directory to stdout. Without the flag, fetch three required
Markdown files; with it, fetch those files and two preset TOML files. Existing
exit codes and stderr diagnostics remain unchanged.

### Verified resources

All five paths were verified as regular Git blobs (`100644`) in the requested
commit. SHA-256 values below were calculated from exact `git show` output,
without decoding, newline conversion, or reserialization.

| Source and staged path | Kind | SHA-256 |
| --- | --- | --- |
| `AGENTS.md` | `markdown` | `2c82fbaa129fbb4a486797e4971fd89fc0bc2497578093529627cb960a32b88e` |
| `.agents/NAG-AGENTS.md` | `markdown` | `35ed17b28541617cfc4d06815c0d9ca70cbceeb2fb3c3b1c1694f5bb56e5505a` |
| `.agents/NAG-CONFIG.md` | `markdown` | `c63c28a561946bf55d75574ba8c1df9c11d73c6c9bf86571e62aa9b62a6650cf` |
| `templates/.codex/config.toml` | `toml` | `210eab80c20e41b50bd1efcbd4ba96365ad460de5f8bd154bfbecb99aaf9da61` |
| `templates/.codex/agents/implementer.toml` | `toml` | `bd8178a4d1168395f5ae966ce82ac667ccbb6120dc18ef2a50ac0030dc57f0b8` |

### Preset merge mapping

| Read from returned staging directory | Merge into target repository |
| --- | --- |
| `templates/.codex/config.toml` | `.codex/config.toml` |
| `templates/.codex/agents/implementer.toml` | `.codex/agents/implementer.toml` |

Do not create `templates/` in consuming repositories. When presets are declined,
neither template is fetched and no target `.codex` file is modified.

## Design Decisions

| Decision | Reason |
| --- | --- |
| Preserve the three-field resource tuple and stage source paths verbatim. | Changing the two constants and the skill's explicit merge mapping is sufficient; no fetcher refactor is needed. |
| Pin to `ba3bfe15408d523db5df467d72601493b294368e`. | This user-selected commit contains actual preset TOML files. The previously proposed commit's implementer template was a symlink blob. |
| Use byte-level hashes for all five resources. | The new pin changes portable guidance as well as preset sources; stale hashes would block retrieval. The `AGENTS.md` checksum happens to remain unchanged. |

The configured persistent ADR path is absent. This table records the decisions
for this feature; do not introduce an unrelated persistent ADR document.

## Tasks

### Task 1: Update the pinned resource manifest

1. Inspect the current constants and consumers:
   ```shell
   rg -n 'PINNED_COMMIT|REQUIRED_RESOURCES|CODEX_RESOURCES|resource_path' plugins/nag/skills/configure-nag/scripts/fetch_nag_resources.py
   ```
2. Set `PINNED_COMMIT` to `ba3bfe15408d523db5df467d72601493b294368e`.
3. Populate `REQUIRED_RESOURCES` and `CODEX_RESOURCES` from the verified table.
   Preserve order and resource kinds. In particular:
   ```python
   CODEX_RESOURCES = (
       ("templates/.codex/config.toml", "210eab80c20e41b50bd1efcbd4ba96365ad460de5f8bd154bfbecb99aaf9da61", "toml"),
       ("templates/.codex/agents/implementer.toml", "bd8178a4d1168395f5ae966ce82ac667ccbb6120dc18ef2a50ac0030dc57f0b8", "toml"),
   )
   ```
4. Keep `download_resource()`, `main()`, argument handling, and verification
   semantics unchanged. Do not follow symlinks or retrieve the old `.codex` URLs.

### Task 2: Align configuration instructions and maintained documentation

1. In `plugins/nag/skills/configure-nag/SKILL.md`, replace the old documented
   commit with the new pin, including the failure-report instructions.
2. In the accepted-presets merge instructions, explicitly name each staged
   template and corresponding target from the mapping table. The preset prompt
   must continue to describe the target `.codex` files.
3. Preserve instructions for declined presets, conflict reporting, unrelated
   settings, nonexistent configured paths, and staging-directory cleanup.
4. In `README.md`'s folder table, describe `.codex/` as this repository's active
   configuration and `templates/.codex/` as reusable presets fetched by
   `$configure-nag`. Avoid broader documentation changes.

### Task 3: Validate the manifest and source-to-target contract

1. Verify the pin and source blobs without network access:
   ```shell
   git ls-tree -r ba3bfe15408d523db5df467d72601493b294368e -- AGENTS.md .agents/NAG-AGENTS.md .agents/NAG-CONFIG.md templates/.codex
   ```
   Require mode `100644` for every selected resource. Recalculate each SHA-256
   using the following pattern, with shell pipe failure propagation enabled:
   ```shell
   set -o pipefail
   git show ba3bfe15408d523db5df467d72601493b294368e:templates/.codex/agents/implementer.toml | sha256sum
   ```
2. Use a temporary offline Python harness under repository-local `tmp/` to load
   the actual fetcher and compare its complete manifest against the verified
   table. Obtain fixture bytes from `git show <pin>:<source_path>`, not working
   tree files. Exercise `download_resource()` with a recording opener serving
   those exact bytes:
   ```text
   for resource in required + optional:
       opener serves the exact committed bytes with HTTP status 200
       download_resource(opener, temporary_stage, resource)
       assert requested URL == RAW_REPOSITORY + '/' + pin + '/' + source_path
       assert staged bytes == committed bytes
   assert no request URL ends with pin + '/.codex/config.toml'
   assert no request URL ends with pin + '/.codex/agents/implementer.toml'
   corrupt one byte of a fixture
   assert download_resource raises FetchError with exit_code == 4
   assert the corrupt resource was not written
   assert fail_if_invalid_arguments([]) is False
   assert fail_if_invalid_arguments(['--include-codex']) is True
   ```
   This focused harness uses real committed resource bytes; its recording
   transport avoids network cost. No persistent test framework or new dependency
   is required. Put temporary validation artifacts only in `tmp/` and clean up
   artifacts created by the harness.
3. Read the final skill mapping to confirm staged `templates/.codex` files are
   merged into target `.codex` files, and declined presets still bypass them.
4. Check the scoped diff:
   ```shell
   rg -n 'fcbc43b9af615cfdd564e84c127e41909be95575|ba3bfe15408d523db5df467d72601493b294368e|templates/\.codex' plugins/nag/skills/configure-nag README.md
   git diff --check
   git diff -- plugins/nag/skills/configure-nag README.md
   git status --short
   ```
   The old pin must have no remaining occurrence within the configure skill.
   Preserve unrelated user files and changes.

## Acceptance Criteria

- [ ] The fetcher and skill documentation use only the approved new pin.
- [ ] All five manifest SHA-256 values match the exact committed resource bytes.
- [ ] Optional presets are fetched exclusively from `templates/.codex/`.
- [ ] Both selected preset sources are regular TOML files at the pin.
- [ ] Presets stage under `templates/.codex/` and merge into consuming `.codex/`.
- [ ] Declining presets fetches only the three required Markdown resources.
- [ ] Checksum mismatch still prevents writing the offending resource; existing
      failure cleanup, redirect rejection, and CLI output contracts are preserved.
- [ ] Configuration prompts, merge preservation, and idempotency remain intact.
- [ ] README accurately distinguishes active settings from reusable presets.
- [ ] Offline validation succeeds and `git diff --check` reports no errors.
- [ ] No application/configuration reconciliation is performed in this checkout;
      changes remain unstaged and uncommitted.

## Dependencies, Gaps, and Risks

- The requested Git commit is available locally; source modes and hashes were
  verified during specification. Public raw URL availability is not yet verified.
  An optional live fetch requires applicable network approval; it is not needed
  for this spec's offline validation. No fallback to another pin or local source
  is permitted during actual configuration.
- The fetcher requires a Python 3.8+ host interpreter and only the standard
  library. This repository is not a Poetry application; its configuration marks
  `$run-tests`, `$dead-code-cleanup`, and `$test-dashboard` disabled. Do not invent
  fast/slow commands or install dependencies. No `very_slow` execution is authorized.
- There is no `$create-spec` configuration section, so skill defaults apply.
  `docs/design/overview.md` supplies design guidance; peer-review standards use
  the embedded skill defaults because no standards document is configured.
- The main regression risk is reading the old staged `.codex` path after the
  manifest moves to `templates/.codex`; the explicit merge mapping addresses it.
  Upgrading the pin also changes downloaded shared guidance, whose existing
  repository-ownership reconciliation rules must continue to apply.
