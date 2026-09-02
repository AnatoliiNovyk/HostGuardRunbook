# Changelog 02092026_validate_inventory_v0

## Як було
CLI покривав лише `validate_apply` (HS01–HS05) і `validate_dry_run` (F01–F06). Inventory run (`docs/runbook/runs/*.md`) не мав локального машинного гейту: можна було помилково вважати run повним без рядків 01–16 або без evidence.

## Як стало
Додано `cli/validate_inventory.py` + `docs/runbook/cli_validator_inventory_v0.md` + посилання в README.
Перевіряє: mode inventory-only, status complete, рядки 01–16, verdict ∈ pass|fail|skip, evidence обовʼязковий якщо не skip. Парсер толерує `|` всередині observed/evidence (як у fixture suno-sb).
Смок: `docs/runbook/runs/20260902_169.58.250.236.md` → `stops: (none)`, exit 0.

## Користь / що лікує
Закриває дірку pipeline inventory→dry-run→apply на стороні inventory: артефакт run тепер валідується локально без SSH і без apply на хост.

## Самоперевірка
- Хост не чіпали.
- Fixture з main прогнано локально до push.
- PR лише код+docs validators.
