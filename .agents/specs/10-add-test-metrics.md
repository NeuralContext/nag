# Feature: Add test-metrics and generalize Nag skills
This feature adds test metrics, generalizes skills so they can easily be incorporated into existing repositories, and adds support for repository-specific skill overrides / guidance.

## Goals:
- Create a generic test-code skill that supports
    - Test markers (slow, fast, very_fast) and integrates fast and slow tests into the architext-and-orchestrate SIR loop.
    - Supports both Node+NPM+Vitest and Python+Pytest for executing tests
    - Supports using the .agents/nag-config.md to override specific test commands for other languages / tech stacks
    - Note this must support overrides that can make this work with the nc-ui (Node+NPM, no vitest yet), nc-algorithm(pytest w/ markers), and nc-db(pytest w/ markers) repositories
- Adds support for visualization skills to the architect-and-orchestrate skill as a final output immediately before task completion and update the architect-and-orchestrate skill to provdie the user a table of outputs to review (including the iterative specs, the pr comments, and the test dashboard)
- Incorporates the test-dashboard from https://github.com/foomoon/test-dashboard as the first visualization skill to be added to the architect-and-orchestrate skill
- Updates every skill in this repo to include the metadata for nag in the frontmatter yaml:
    ```yaml
    metadata:
        nag: true
    ```
- Create a .agents/nag-agents.md file for Nag specific agent instruction
- Create a .agents/nag-config.md file for Nag skill-specific overrides, exclusions, and repository-specific guidance.
- Updates the each Nag skill (each SKILL.md under .agents/skills folders) so it includes something like the following at the beginning of the skill:
    ```md
    Before executing this skill:
        1. Read the active AGENTS.md guidance.
        2. Read `<repo-root>/.agents/nag-agents.md`.
        3. Read `<repo-root>/.agents/nag-config.md`.
        4. Apply the section corresponding to this skill.
    ```
- Update the README.md so the getting started instructions clarify the process and key components:
    - Add the section from AGENTS.md into your repository's AGENTS.md at the top
    - Copy the nag-agents.md and nag-config.md files into you .agents folder and update with your repository-specific information.
    - Run update-agent-guidance to finalize
- Update the README.md file to include the default repository design guidance is at docs/design. This can be overridden in nag-agents.md
    - If specific skills reference docs/design, update them so they reference the design documentation folder specifiied in .agents/nag-agents.md
- Update the filenames for `.agents/nag-agents.md` and `.agents/nag-config.md` so the filenames are uppercase (not the extension) in keeping with AGENTS.md and SKILL.md. Update all references to any of these files so they are also uppercase.
