# dry_run_v0

## Purpose
Поверх `inventory_checklist_v1`: згенерувати **план змін лише для власного стеку** і перевірити, що diff **не чіпає** чужі Host()/middleware/volume/БД (LEAVE). Без apply на хост.

## Artifact path (Shranz)
`docs/runbook/dry_runs/YYYYMMDD_<host>_<stack>.md`

### Header
`inventory_ref` | `scope_stack` | `leave_neighbors` | `touches_foreign` (must be **no**) | `verdict`

### Diff row
`id | resource | before | after | owner(own/foreign) | action(add/change/remove/none) | evidence`

### Blocks
- `plan` — лише `owner=own`
- `rollback_stub` — зворотні кроки

Без evidence або `owner=foreign` → **fail**, apply заборонено.

## Inputs
- Заповнений inventory run: `docs/runbook/runs/YYYYMMDD_<host>.md` (усі id з verdict+evidence)
- Scope: список «своїх» ресурсів (Coolify app ids / compose project / domains), явно не LEAVE

## Hard fail (suno-proven; before plan)
Будь-який F* → `verdict=fail`, **plan порожній**, apply заборонено.

- **F01** middleware: reuse/rename на чуже імʼя (напр. `redirect-to-https` сусіда) → fail
- **F02** Host: diff змінює Host() сусіда АБО знімає backticks у своєму правилі → fail
- **F03** volumes/DB: plan чіпає LEAVE (`u1u6…` / CORE64) або міграції на чужу БД → fail
- **F04** CORS `/auth`: `ACAO *` або credentials+`*` або знято reflect apex/www → fail
- **F05** leftovers: `rm` exited Coolify apps у plan без окремого approve → fail
- **F06** meta: немає `inventory_ref` або diff-рядок без evidence / `owner=foreign` → fail; `touches_foreign` must be `no`

## Rules (after hard-fail gate)
1. Diff лише: свої routers/middleware/services/volumes/env
2. Host() у плані тільки з backticks: `Host(\`domain\`)`
3. Нові middleware names не колізять з існуючими на хості (inventory 03/11)
4. Aggregate pass лише якщо всі diff-рядки own+evidence і жоден F* не спрацював

## Explicit non-goals (v0)
- Apply / restart / cert renew на хості
- CI шар
- Авто-видалення leftovers без окремого approve

## Status
v0 — формат Shranz + Hard Fail Yezhi вшиті; наступне: PR у HostGuardRunbook. Apply досі ні.
