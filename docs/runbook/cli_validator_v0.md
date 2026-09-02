# cli_validator_v0

## Purpose
Локальна перевірка markdown-артефактів HostGuardRunbook **без** SSH і **без** apply на хост.

## Command
```bash
python3 cli/validate_apply.py docs/runbook/applies/<file>.md
python3 cli/validate_apply.py docs/runbook/applies/<file>.md --expect-stops HS03
```

## Behavior
- Читає header table (`inventory_ref` … `verdict`)
- HS01: `f_gate=fail`
- HS02: `touches_foreign` не `no`
- HS03: `approve` missing
- HS04: step rows без колонки `rollback_id`
- HS05: немає секції `## post_check`
- Exit `0` якщо stops порожні або збіглись із `--expect-stops`; інакше `1`

## Non-goals
- Будь-який host mutation / docker / coolify apply
- Валідація dry-run/inventory (наступний інкремент)

## Fixture
Blocked example must yield HS03:
`docs/runbook/applies/20260902_169.58.250.236_suno-sb.md`
