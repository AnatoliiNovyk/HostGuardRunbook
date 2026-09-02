# apply_v0

## Purpose
Спека шару **apply** після успішного dry-run. Цей документ **не виконує** apply на хост — лише правила, гейти й формат артефакту.

## Preconditions (all required)
1. `inventory_ref` існує, усі обовʼязкові checks мають evidence
2. `dry_run_ref` існує, `verdict=pass`, `touches_foreign=no`
3. Жоден Hard Fail F01–F06 з `dry_run_v0` не спрацював
4. `scope_stack` збігається з dry-run (лише own)
5. Явний **human approve** у шапці apply-артефакту (див. нижче)

Якщо будь-яка умова false → `verdict=blocked`, steps порожні, **apply заборонено**.

## Artifact path
`docs/runbook/applies/YYYYMMDD_<host>_<stack>.md`

### Header
| field | meaning |
|-------|---------|
| inventory_ref | шлях до inventory run |
| dry_run_ref | шлях до dry_run артефакту |
| scope_stack | той самий own stack |
| leave_neighbors | LEAVE list (must match dry-run) |
| touches_foreign | must be **no** |
| approve | `approver` + `timestamp` + `statement` (напр. «approve apply for scope_stack only») |
| verdict | pass / fail / blocked |

Без заповненого `approve` → **blocked**.

### Step row
`id | step | command_or_action | owner(own/foreign) | status(pending/done/skipped/failed) | evidence`

- `owner=foreign` у будь-якому step → **fail**, stop
- step без evidence після виконання → не done

### Blocks
- `preflight` — повторна перевірка F01–F06 + dry-run hash/ref
- `steps` — лише own; порядок з dry-run `plan`
- `rollback` — обовʼязковий stub **до** першого мутуючого step (копія/уточнення dry-run `rollback_stub`)
- `post_check` — мінімум: re-inventory touches (Host/middleware/volumes/CORS smoke для scope); сусіди LEAVE незмінні

## Hard stop (during apply)
- S01: preflight F* fail → abort, no further steps
- S02: step would touch LEAVE / foreign → abort + run rollback
- S03: approve missing/expired policy (v0: missing only) → blocked
- S04: post_check показує зміну сусіда → fail + rollback

## Explicit non-goals (v0)
- Реальний apply на будь-який хост з цього документа
- Авто-merge / авто-approve
- CI шар
- `rm` Coolify leftovers без окремого approve-артефакту

## Status
v0 draft — чекає формат/правки від Shranz (applies/) і hard-stop від Yezhi; PR без виконання apply.
