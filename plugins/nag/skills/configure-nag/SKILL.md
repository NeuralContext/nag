---
name: configure-nag
description: Configure or update NAG guidance for a specific repository, validate it, and leave changes for user review.
metadata:
  nag: true
---

# Configure NAG

Configure or reconcile the plugin-delivered NAG guidance in the repository
where the agent is operating. This is the single idempotent entry point for
both an initial repository setup and later updates. Never copy, install, update,
or delete repository-local `.agents/skills/` content: NAG skills are
plugin-provided. Never stage, commit, push, create a pull request, or change
branches.

## Configuration preflight

1. Resolve the target with `git rev-parse --show-toplevel`, report that root,
   and ensure it is the current repository; do not accept another checkout as
   a source or target.
2. Read every active target `AGENTS.md` and `AGENTS.override.md` that applies.
   Missing `.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md` are expected for
   an unconfigured repository. Inventory either file when present, along with
   `AGENTS.md` and existing working-tree changes.
3. Prompt once whether to apply the recommended NAG presets. Name the only
   supported files—`.codex/config.toml` and `.codex/agents/implementer.toml`—
   and explain that acceptance authorizes a merge preserving unrelated local
   settings. If declined, do not fetch or modify either file.
4. Invoke `scripts/fetch_nag_resources.py` from this skill directory with a
   Python 3.8-or-newer interpreter, with `--include-codex` only when accepted.
   Locate an available Python 3 host command (for example `python3`, `python`,
   or Windows `py -3`) before invocation; if none is available, report the
   blocker before target writes. This script is the exclusive mechanism for
   canonical resource retrieval: do not construct URLs or use ad hoc network,
   Git, browser, or local-template fallbacks.
5. On a nonzero result, stop before target writes and report its diagnostics,
   script path, pinned commit `fcbc43b9af615cfdd564e84c127e41909be95575`, and
   the exact resource URL that failed. On success, capture its sole stdout
   absolute staging path, require that directory to exist, and read only staged
   resources. Remove exactly that returned directory after applying or
   abandoning merges.

The fetch script verifies every selected byte before returning its staging path.
Network denial, redirect/HTTP failure, missing content, malformed content, or
checksum failure is a blocker; never partially configure or use an unpinned
fallback.

## Classify and reconcile repository configuration

Classify the state after verified resources are available:

- If both `.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md` are absent,
  report `initial configuration`.
- Otherwise report `update`; if exactly one is present, also report the
  partial-configuration gap.

For the root `AGENTS.md`, preserve all repository-owned text. Create it when
absent. Extract the NAG workflow bootstrap from the verified staged
`AGENTS.md`, then insert it when absent surrounded by one stable
`<!-- NAG:START -->` / `<!-- NAG:END -->` pair. Update exactly one recognizable
canonical or prior NAG block in place; never duplicate it. If multiple
candidates or materially edited candidates exist, display the conflict and
obtain approval before editing. Re-scan after writing and prove exactly one
effective bootstrap block remains.

Create `.agents/` as needed. For an initial configuration, write the verified
canonical `.agents/NAG-AGENTS.md` and initialize `.agents/NAG-CONFIG.md` from
the verified template. On update, reconcile portable guidance with the
canonical version only when ownership is clear. Surface ambiguous local
divergence and ask before replacing it. Reconcile an existing configuration by
section/key: retain resolved repository paths, commands, policies, overrides,
enablement choices, and rationales. Never replace a resolved value with an
angle-bracket template placeholder. Replace live references to prior skill
names with `$configure-nag`; do not rewrite frozen feature history.

When NAG presets were accepted, do the following:
  - Merge the two verified supported preset files;
  - Retain unrelated TOML settings and agent definitions. If a conflict cannot be
  resolved safely, preserve the target value and report it. 
  - Review the .codex/config.toml file and identify filepaths in the [permissions.repo.filesystem.":workspace_roots"] section that do not currently exist. 
    - Prompt the user for permission to remove these filepaths from the .codex/config.toml file. Explain that:
      "The following filepaths are configured in the .codex/config.toml file but don't exist in your repository.
      Codex may erroneously create empty files if those paths aren't removed from the config. If you plan to create the folders soon, you
      may wish to leave the config. If not, I recommend removing them.
      
      Can I remove the filepaths from .codex/config.toml that don't exist in your repository? You can say 'yes','no', or specify the filepaths to 
      delete."
    - IF the user replies affirmatively, remove the filepaths from .codex/config that don't exist in the repository
    - IF the user replies negatively, don't remove any filepaths from .codex/config
    - IF the user replies with a list of filepaths, only remove those filepaths from .codex/config 

Do nothing in`.codex/` if the user declined the NAG preset prompt.

Repeated runs with unchanged inputs must not create formatting churn, reorder
unrelated content, or add another bootstrap block. Ask before ambiguous,
moderate-or-higher-risk, security-sensitive, or destructive changes.

## Terminal guidance audit

After the verified bootstrap and portable guidance are configured, read
`.agents/NAG-AGENTS.md` and `.agents/NAG-CONFIG.md` and perform this terminal
phase. Discover active guidance, plugin-visible NAG skill metadata and declared
requirements, language/package manifests, task scripts, CI, formatter/linter/
test configuration, and maintained documentation. Do not require or recreate
repository-local skills. Preserve multi-language components and their package
managers.

Resolve verified repository configuration for design-document, artifact,
review-standard, and ADR paths; separate `fast`, `slow`, and `very_slow` test
commands; test framework, integration infrastructure, and mock policy;
`$test-dashboard` applicability and repository-local outputs; every
language-dependent skill's enabled/inapplicable/unavailable decision and
rationale; and repository-specific overrides. Resolve affected angle-bracket
placeholders. Prefer existing Poetry, uv, npm, or equivalent scripts over
direct executables. Never require Vitest merely because npm exists or translate
required Python scripts. If Python availability cannot safely be established,
report the applicability decision as unresolved rather than deleting or
rewriting a skill. Missing test tiers remain explicitly unconfigured, and
`very_slow` never runs without current user approval.

Validate referenced paths, commands, environment variables, services,
workflows, and plugin prerequisites. Remove only demonstrably stale references;
retain intentional optional/external ones. Do not change application code to
satisfy guidance. Re-scan paths and placeholders, run safe lightweight checks,
and use read-only Git inspection such as `git status --short` and
`git diff --check`.

End with this report, leaving all changes unstaged and uncommitted:

## NAG configuration result

- Mode: initial configuration or update
- Target: resolved repository root
- Files added and modified
- Existing values preserved and conflicts requiring approval
- Pinned source commit and download verification result
- `.codex` preset choice: accepted or declined
- Applicability decisions and unresolved gaps/placeholders
- Validation commands and results
- Git state: changes are unstaged and uncommitted
- Next action: review the diff and commit it when satisfied
