# Upstream provenance

- Upstream: `https://github.com/foomoon/test-dashboard`
- Imported commit: `7918df2e30b643d1d31f009abf43355fc8c3bc9d`
- Import date: 2026-09-14
- Imported source: upstream `SKILL.md` and all five Python files under
  `scripts/`; the upstream README was reviewed but not retained because its
  installation and home-directory output instructions conflict with NAG's
  repository-local contract.
- Project licensing decision: treat the imported source as MIT-licensed under
  the notice in `LICENSE.md`. The pinned upstream tree did not include a
  separate license file; this repository records the project's explicit
  licensing decision rather than claiming additional upstream metadata.

## Local modifications

- Replaced upstream `SKILL.md` with the NAG metadata, shared preflight,
  applicability, repository-local output, failure, and no-GUI contracts.
- Replaced upstream installation/output documentation with this repository's
  NAG usage documentation.
- Added explicit `--out` support and an atomic repository-local JSON default to
  `export_test_dashboard_data.py`.
- Changed the generator's HTML default to the repository-local `tmp/` path and
  made its writes atomic.
- Added shared validation that rejects output paths outside the detected
  repository root and creates output parent directories.
- Made a failed instrumented pytest run print captured output, exit nonzero,
  and leave any previous final JSON snapshot untouched.
