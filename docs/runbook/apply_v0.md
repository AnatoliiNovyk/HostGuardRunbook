# apply_v0

## Purpose
Спека шару **apply** після успішного dry-run. Цей документ **не виконує** apply на хост — лише правила, гейти й формат артефакту.

## Preconditions (all required)
1. `inventory_ref` існує, усі обовʼязкові checks мають evidence
2. `dry_run_ref` існує, `verdict=pass`, `touches_foreign=no`
3. Жоден Hard Fail F01–F06 з `dry_run_v0` не спрацював → **HS01/HS02**
4. `scope_stack` збігається з dry-run (лише own)
5. Явний **human approve** у шапці apply-артефакту → **HS03**
6. Блок `post_check` прописаний у артефакті → **HS05** (відсутній → `blocked`)

Якщо будь-яка умова false → `verdict=blocked`, `apply=no`, steps порожні, **apply заборонено**.

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
| f_gate | `pass` \| `fail` — підсумок F01–F06 / preflight |
| apply | `yes` \| `no` — без approve або при F* / fail f_gate → **`apply=no`** |
| approve | `approver` + `timestamp` + `statement` (напр. «approve apply for scope_stack only») |
| verdict | pass / fail / blocked |

Без заповненого `approve` → **blocked**, `apply=no` (**HS03**).
`f_gate=fail` → `apply=no`.

### Step row
`id | step | command_or_action | owner(own/foreign) | rollback_id | status(pending/done/skipped/failed) | evidence`

- `rollback_id` обовʼязковий (**HS04**) — посилання на крок у блоці `rollback`
- `owner=foreign` у будь-якому step → **fail**, stop
- step без evidence після виконання → не done

### Blocks
- `preflight` — повторна перевірка F01–F06 + dry-run hash/ref → виставляє `f_gate`
- `steps` — лише own; порядок з dry-run `plan`; кожен рядок з `rollback_id`
- `rollback` — обовʼязковий stub **до** першого мутуючого step (копія/уточнення dry-run `rollback_stub`)
- `post_check` — **обовʼязковий блок** (**HS05**): мінімум re-inventory touches (Host/middleware/volumes/CORS smoke для scope); сусіди LEAVE незмінні. Відсутній блок → `blocked`, `apply=no`

## Hard stop
| id | condition | effect |
|----|-----------|--------|
| HS01 | F* / foreign у preconditions | blocked, `apply=no` |
| HS02 | dry-run не pass / `touches_foreign≠no` | blocked, `apply=no` |
| HS03 | approve відсутній | blocked, `apply=no` |
| HS04 | step без `rollback_id` | fail/blocked, stop |
| HS05 | блок `post_check` відсутній | blocked, `apply=no` |
| S01 | preflight F* fail mid-run | abort, no further steps |
| S02 | step would touch LEAVE / foreign | abort + run rollback |
| S03 | approve missing (runtime) | blocked |
| S04 | post_check показує зміну сусіда | fail + rollback |

## Explicit non-goals (v0)
- Реальний apply на будь-який хост з цього документа
- Авто-merge / авто-approve
- CI шар
- `rm` Coolify leftovers без окремого approve-артефакту

## Status
v0 — патч за ревʼю Shranz/Yezhi (`f_gate`/`apply`, `rollback_id`, HS05). Apply на хост ні.
