---
name: test-dashboard
description: Generate a deterministic repository-local HTML dashboard for a Python pytest suite after final validation and review.
metadata:
  nag: true
---

# Test Dashboard

Generate a self-contained pytest dashboard with Tests, CRAP Score, and Coverage
Matrix tabs. This skill supports Python + pytest only; it does not support Node,
Vitest, or other runners.

If the `$test-dashboard` section of the NAG-CONFIG.md shows `Enabled: no`, skip this skill completely and alert the user.

## NAG preflight and applicability

Read all active `AGENTS.md` guidance, `<repo-root>/.agents/NAG-AGENTS.md`, and
`<repo-root>/.agents/NAG-CONFIG.md`. Apply the `$test-dashboard` section. If a
required file or setting is missing, follow `NAG-AGENTS.md` fallback behavior
and report the gap.

```text
if NAG-CONFIG disables dashboard:
    status = inapplicable
elif repository is not Python + pytest:
    status = inapplicable
elif pytest, coverage/pytest-cov, or radon is missing:
    status = unavailable; report exact missing dependencies
else:
    generate dashboard and report configured output path
```

Do not install dependencies without approval. Use `scripts/_detect.py` to find
the repository, tests, sources, and Python environment. Verify its output on
first use; use `scripts/.dashboard_config.json` for detection overrides rather
than editing the detector.

## Generate the final snapshot

Resolve both data and HTML paths from `.agents/NAG-CONFIG.md`. They must be
inside the repository root. Run from the repository root using the Python path
reported by the detector:

```bash
<detected-python> .agents/skills/test-dashboard/scripts/export_test_dashboard_data.py \
  --out <repo-root>/tmp/test-dashboard-data.json
<detected-python> .agents/skills/test-dashboard/scripts/generate_test_dashboard.py \
  --data <repo-root>/tmp/test-dashboard-data.json \
  --out <repo-root>/tmp/test-dashboard.html
```

Always pass both paths explicitly even though the scripts provide the same
repository-local defaults. The export reruns pytest under coverage and may be
expensive. Use only after the orchestration loop's final validation and review;
if it exposes a required code/test change, mark the artifact stale and resume
that loop before regenerating it.

If pytest fails, report `failed`; no new JSON is published and an existing HTML
must not be described as current. Successful JSON and HTML writes are atomic.
Generated outputs remain ignored unless repository configuration explicitly
requires versioning. Never hand-edit them.

Do not automatically open the dashboard. Report total tests, suite status,
notable CRAP threshold changes when available, and a clickable repository-local
path. Opening a GUI requires explicit user request and environment approval.

## Provenance

See `PROVENANCE.md` and `LICENSE.md`. The deterministic implementation was
vendored from `foomoon/test-dashboard` at the pinned commit recorded there and
then locally adapted only as documented.
