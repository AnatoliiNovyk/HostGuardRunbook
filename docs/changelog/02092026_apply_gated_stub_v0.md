# Changelog 02092026_apply_gated_stub_v0

## Як було
Три окремі CLI (`validate_inventory`, `validate_dry_run`, `validate_apply`) без єдиної точки входу. Ризик: оператор «пройшов» один гейт і випадково вважає apply дозволеним.

## Як стало
Додано `cli/apply_gated.py` + docs. Ланцюг викликає всі три валідатори; при будь-якому fail — `GATED FAIL`. При успіху всіх — усе одно друкує refuse host apply (stub). Fixture blocked suno-sb → apply HS03 → gated fail.

## Користь
Єдина команда «перевірити перед apply» без можливості мутувати хост.

## Самоперевірка
Локальний прогін fixture: inventory/dry-run ok, apply HS03 → exit 1; жодного SSH.
