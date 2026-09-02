# inventory_checklist_v1

## Purpose
Перевіряємий inventory перед будь-яким dry-run/apply на multi-tenant VPS (Coolify/Traefik на спільному IP).
UX №1: існуючий прод на тому ж хості — не чіпати чужі Host()/middleware/volume/БД.

## Verdict row format
`id | check | expected | observed | verdict (pass/fail/skip) | evidence`

- **fail** = чуже в diff apply або небезпечна зміна
- **skip** = N/A для стеку
- без **evidence** — не pass

## Checklist

| id | check | expected |
|----|--------|----------|
| 01 | Coolify apps: name, FQDN, status (running/exited), project | повний список зафіксовано |
| 02 | Traefik router rules / `Host(\`...\`)` + entrypoints | усі правила зібрані |
| 03 | Traefik middleware names | імена унікальні vs сусіди |
| 04 | TLS / ACME domains на хості | домени й серт. обліковані |
| 05 | Docker networks ↔ containers | мапа мереж є |
| 06 | Volumes: ім'я + хто mount | чужі volume позначені LEAVE |
| 07 | БД/сервіси (Postgres/Redis тощо) + host ports | свої vs чужі розділені |
| 08 | Published ports; хто слухає :80/:443 окрім Traefik | аномалії зазначені |
| 09 | CORS/auth на спільних роутах | політика зафіксована |
| 10 | Snapshot «до»: `docker ps -a`, Coolify apps, Traefik dynamic config paths | артефакти збережені |
| 11 | Middleware name uniqueness vs neighbor | немає clash (напр. не спільний `redirect-to-https`) |
| 12 | Host() у compose з backticks | `Host(\`domain\`)`; без backticks → ризик Traefik 503 |
| 13 | Coolify leftovers: exited apps з порожнім FQDN | лише inventory, не rm |
| 14 | Neighbor/CORE64 flag: uuid/stack/container | LEAVE |
| 15 | Volumes/functions path; не чужа БД | свій шлях; немає міграцій на чужу БД |
| 16 | CORS/auth: `/auth` reflect Origin (не `*`); OPTIONS smoke apex/www/evil | окремо від REST; smoke зафіксовано |

## Run artifacts
Прогони: `docs/runbook/runs/YYYYMMDD_<host>.md` (таблиця рядків у форматі вище).

## Status
v1 accepted — reference inventory-only run: docs/runbook/runs/20260902_169.58.250.236.md
