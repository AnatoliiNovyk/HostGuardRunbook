# cli_validator_inventory_v0

## Purpose
Локальна перевірка `docs/runbook/runs/*.md` (checklist 01–16 + evidence) **без** apply на хост.

## Command
```bash
python3 cli/validate_inventory.py docs/runbook/runs/<file>.md
```

## Checks
- Mode mentions inventory-only
- Status complete
- Rows `01`–`16` present
- verdict ∈ pass|fail|skip
- evidence required unless skip

## Fixture
`docs/runbook/runs/20260902_169.58.250.236.md` → stops none.

## Non-goals
- Host apply / SSH / live rediscovery
