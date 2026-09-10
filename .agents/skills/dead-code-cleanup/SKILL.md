---
name: dead-code-cleanup
description: Find and safely remove unused Python code in a Poetry project with Vulture. Use when asked to identify or eliminate dead Python code; do not use for broad refactors without a dead-code objective.
---

# Dead Code Cleanup

Use Vulture to produce a candidate list, then remove only code that has been
verified unused. Vulture's findings are not proof: framework entry points,
plugin registration, reflection, serialization, dynamic imports, and public
library APIs commonly appear unused.

## Run Vulture through Poetry

Work from the directory containing `pyproject.toml`. First check whether the
project environment has Vulture:

```bash
poetry run vulture --version
```

If dependencies have not been installed, use the project's normal Poetry
installation command without changing dependency declarations. If Vulture is
not a project dependency, report that and ask before adding it (normally as a
development dependency); do not silently modify `pyproject.toml` or the lock
file.

Run an initial scan through Poetry and save the raw output outside the source
tree or in an ignored temporary location. Honor existing Vulture configuration
or excludes before adding flags. Start with the package and test directories,
not vendored, generated, migration, build, cache, or virtual-environment
directories. Treat Vulture's exit status as a reporting detail rather than a
reason to discard its output.

## Verify candidates before editing

For each candidate that might be removed:

1. Search the repository for direct references and string-based/dynamic uses.
2. Inspect package exports, CLI entry points, framework routes, task/plugin
   registration, model/serializer fields, templates, and configuration that
   could name it indirectly.
3. Preserve intentionally public APIs unless the task explicitly authorizes
   changing them. Keep uncertain candidates and explain why.
4. Group only tightly related, low-risk removals; avoid opportunistic cleanup.

Remove confirmed code together with imports, tests, comments, and references
made obsolete by that exact removal. Keep each change narrow and reviewable.
Do not add arbitrary Vulture whitelist entries merely to make the report clean;
use a documented whitelist only for verified intentional dynamic/public uses.

## Validate and report

Run the project's relevant test, lint, type-check, and formatting commands
where they are available, all through `poetry run`. At minimum, rerun Vulture
with the same scope and confirm that removed candidates no longer appear.
If validation fails, diagnose and fix only changes introduced by this cleanup;
otherwise restore the affected removal and report it as retained.

Summarize:

- confirmed code removed and why it was safe;
- candidates retained, with the reason or uncertainty;
- validation commands and results; and
- any Vulture installation/configuration change that still needs approval.
