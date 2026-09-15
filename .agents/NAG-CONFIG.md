# NAG Configuration

This is the configuration for the NAG repository itself. Consuming repositories should replace the examples below with their own commands and policies.

Angle-bracket values are placeholders, not executable commands. A skill that
depends on an unresolved placeholder is unconfigured until
`$install-nag` resolves it.

## Repository Structure

- Design documentation: `docs/design/`
- Temporary artifacts: `tmp/`
- Review standards: absent; use `$peer-review`'s embedded standards
- Architecture decision record: absent; report the gap when an ADR is required

## Skill Configurations

### `$run-tests`
- Enabled: no

| Tier | Command | Configured |
| --- | --- | --- |
| `fast` | `<repository fast-test command>` | no |
| `slow` | `<repository slow-test command>` | no |
| `very_slow` | `<repository very-slow-test command>` | no |

#### Test conventions

- Framework: absent
- Integration-test infrastructure and allowed mocks: prefer real infrastructure;
- Exceptions: none

### `$test-dashboard`

- Enabled: no
- Output: `tmp/test-dashboard.html`
- Data output: `tmp/test-dashboard-data.json`
- Additional configuration: Python + pytest only; requires `pytest`,
  `coverage` or `pytest-cov`, and `radon` in the detected project environment.

### `$dead-code-cleanup`
- Enabled: no
- Rationale: 
    - Inapplicable: this repository is not a Python/Poetry application and has no dead-code cleanup objective.

### `$peer-review`
- Enabled: yes
- Standards Document Location: N/A
- Additional Instructions:
    - Use the review standards embedded in the skill because the configured review
    standards path is absent. Write only to the selected feature's matching
    `review-vN.md`.

### `$install-nag`
- Enabled: yes
- Guidance:
    - Resolve all placeholders and explicitly record which language-dependent skills are applicable, disabled, inapplicable, or unavailable for the target repository.
