# cli_validator_dry_run_v0

## Purpose
Локальна перевірка `docs/runbook/dry_runs/*.md` (F01–F06, `touches_foreign`) **без** apply на хост.

## Command
```bash
python3 cli/validate_dry_run.py docs/runbook/dry_runs/<file>.md
```

## Checks
- Header: inventory_ref, scope_stack, leave_neighbors, touches_foreign, verdict
- `touches_foreign` must be `no`
- Hard fail gate table must list F01–F06 with `pass…`
- Diff rows: `owner=foreign` лише з `action=none` (або еквівалент); evidence на R* rows
- inventory_ref path shape includes `runs/`

## Fixture
`docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md` → stops none, exit 0.

## Non-goals
- Host apply / SSH / docker mutate
