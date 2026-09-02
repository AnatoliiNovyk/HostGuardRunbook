# Changelog 02092026_freeze_cli_v0

## Як було
CLI pipeline зібраний (docs → validators → gated stub → CI), але не було явного «замороженого» контракту milestone.

## Як стало
Додано `docs/runbook/MILESTONE_CLI_v0.md` (FROZEN): in-scope таблиця, smoke-контракт HS03/`GATED FAIL`, out-of-scope (host apply). Посилання в README.

## Користь
Фіксує CLI v0 як базу; наступні зміни — свідомий наступний milestone, не повзуча ерозія гейтів.

## Самоперевірка
Базується на змерджених PR #1–#9; host apply не додано.
