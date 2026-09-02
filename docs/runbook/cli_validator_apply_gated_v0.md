# cli_validator_apply_gated_v0

## Purpose
Оркестратор `inventory → dry-run → apply` validators. Навіть якщо всі гейти чисті — **відмовляє** у host apply (stub).

## Command
```bash
python3 cli/apply_gated.py \
  --inventory docs/runbook/runs/20260902_169.58.250.236.md \
  --dry-run docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md \
  --apply docs/runbook/applies/20260902_169.58.250.236_suno-sb.md
```

## Fixture (blocked apply)
suno-sb apply має HS03 → stage apply exit≠0 → `GATED FAIL — host apply refused`.

## Non-goals
SSH, docker mutate, real apply — суворо заборонено.
