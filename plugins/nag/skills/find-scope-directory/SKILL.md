---
name: find-scope-directory
description: Find where specifications for the current feature are located
metadata:
  nag: true
---

# Find Scope Directories

Used by Nag skills to find specifications related to the current feature development.

## NAG preflight

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$find-scope-directory` section.
If a required file or setting is missing, follow `NAG-AGENTS.md` fallback
behavior and report the gap.

## Find candidates

Use the following prioritized list to select a scope location and return it to
the calling skill:

Ordered Scope Location Preferences:
1. A specification identified directly by the user
2. A group of iterative specifications colocated within a folder specified by the user
3. A group of folders specified by the user where each folder contains one or more specifications
4. All changes on the current branch with zero or more optional specifications potentially
  identified by folder / spec name prefixed with the same number as the branch.

When the first three priorities do not apply, set the command working directory
to the root directory inside the target repository and run:

```bash
python3 <plugin-root>/skills/find-scope-directory/scripts/find_scope_directories.py
```

Use a repository-configured Python interpreter when required by repository
guidance. Parse the JSON `folders` list as possible locations, then ask the
user to verify the intended scope location.

Ask the user to verify the location unless it was already specified by the user.
