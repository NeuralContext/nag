---
name: run-tests
description: Run repository-configured fast, slow, and approved very_slow test tiers and report available metrics without inventing commands.
metadata:
  nag: true
---

# Run Tests

Run the consuming repository's configured test commands. Do not install a test
framework, rewrite test configuration, translate commands between frameworks,
or infer pytest markers for npm projects.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$run-tests` section. If a
required setting is missing, follow `NAG-AGENTS.md` fallback behavior and report
the gap.

If the `$run-tests` section of the NAG-CONFIG.md shows `Enabled: no`, skip this skill completely and alert the user.

## Resolve and run tiers

Treat a command as configured only when its table row says `yes` and contains a
real, copyable repository command rather than an angle-bracket placeholder.
Repository npm scripts take precedence over direct runner invocation.

```text
for tier in [fast, slow]:
    command = NAG_CONFIG.run_tests[tier]
    if command is configured:
        run command as a separate process and record elapsed time
        if sandbox or network restrictions caused failure:
            request the minimum approval and retry
        if tests failed:
            fix only when the invoking task authorizes code changes
            otherwise report failure
        stop after failure unless the task explicitly requests all failures
    else:
        report tier as not configured

if very_slow is configured and the user specifically requested very_slow execution:
    run very_slow as a separate process and record elapsed time
else:
    report very_slow as not configured or not specifically requested
```

Run `fast` before `slow`. A missing `fast` does not license inventing a command;
continue to the separately configured `slow` tier. If `very_slow` approval is
declined, report `declined`. If it is configured but approval was not requested
or resolved, report `not run`. Approval from a prior workflow is not current.

Use the active repository's integration infrastructure and mock policy. NAG's
portable default prefers real infrastructure, but exceptions are repository
owned.

## Report

Print a concise table in tier order:

| Tier | Command | Status | Tests | Duration | Notes |
| --- | --- | --- | ---: | ---: | --- |
| `fast` | configured command or `—` | pass/fail/not configured/not run/declined | runner count or `—` | runner/observed duration or `—` | concise result or gap |

Use only `pass`, `fail`, `not configured`, `not run`, or `declined`. Record test
counts only when runner output supplies them. An observed command duration may
be recorded when measured; never fabricate runner metrics. For an unconfigured
tier, name the exact `.agents/NAG-CONFIG.md` row that must be populated.

If you are called by another skill (e.g. `$architect-and-orchestrate`) make the full test output available to the calling skill.
