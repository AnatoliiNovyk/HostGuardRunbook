# Changelog 02092026_ci_cli_smoke_v0

## Як було
CLI validators і `apply_gated` жили лише локально; регресія на main могла пройти непоміченою.

## Як стало
Додано `.github/workflows/cli-smoke.yml`: на push/PR ганяє fixture suno-sb —
inventory/dry-run stops none, apply `--expect-stops HS03`, `apply_gated` → `GATED FAIL` + exit 1.
Жодного SSH/host apply.

## Користь
Автоматичний smoke проти ламання гейтів перед freeze CLI v0 milestone.

## Самоперевірка
Локальний прогін тих самих команд: LOCAL_SMOKE_OK; workflow містить очікувані маркери.
