# MILESTONE_CLI_v0 — FROZEN

**Status:** frozen 2026-09-02 (Tipo4ki: Shranz / Yezhi / Anatolii / Petru44o)
**Slogan:** NeighborSafe
**Hard rule:** host apply = **ні** (stub only)

## In scope (frozen)
| Layer | Artifact |
|-------|----------|
| Spec inventory | `docs/runbook/inventory_checklist_v1.md` |
| Fixture inventory | `docs/runbook/runs/20260902_169.58.250.236.md` |
| Spec dry-run | `docs/runbook/dry_run_v0.md` (F01–F06) |
| Fixture dry-run | `docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md` |
| Spec apply | `docs/runbook/apply_v0.md` (HS01–HS05) |
| Fixture apply (blocked) | `docs/runbook/applies/20260902_169.58.250.236_suno-sb.md` (HS03) |
| CLI | `cli/validate_inventory.py`, `cli/validate_dry_run.py`, `cli/validate_apply.py`, `cli/apply_gated.py` |
| CI | `.github/workflows/cli-smoke.yml` |

## Contract (smoke)
1. `validate_inventory` → stops none, exit 0
2. `validate_dry_run` → stops none, exit 0
3. `validate_apply --expect-stops HS03` → exit 0
4. `apply_gated` on same trio → `GATED FAIL`, exit 1

## Explicitly out of scope
- SSH / docker mutate / real host apply
- Live rediscovery на проді
- Apply executor (навіть після approve — окремий milestone)

## Next (not this freeze)
Тільки після окремого рішення команди: executor з human approve + rollback, або новий fixture.
