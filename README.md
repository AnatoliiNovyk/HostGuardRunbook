# HostGuardRunbook

inventory → dry-run → apply

**Slogan:** NeighborSafe — не зламай сусіда на спільному IP.

**UX №1:** існуючий прод на тому ж хості (Coolify/Traefik multi-tenant).

## Milestone
- **CLI v0 frozen:** [docs/runbook/MILESTONE_CLI_v0.md](docs/runbook/MILESTONE_CLI_v0.md)

## Docs
- Checklist: [docs/runbook/inventory_checklist_v1.md](docs/runbook/inventory_checklist_v1.md)
- Reference run (inventory-only): [docs/runbook/runs/20260902_169.58.250.236.md](docs/runbook/runs/20260902_169.58.250.236.md)
- Dry-run spec: [docs/runbook/dry_run_v0.md](docs/runbook/dry_run_v0.md)
- Apply spec (gates only, no host mutation from the doc): [docs/runbook/apply_v0.md](docs/runbook/apply_v0.md)
- CLI validator: [docs/runbook/cli_validator_v0.md](docs/runbook/cli_validator_v0.md)
- Dry-run CLI: [docs/runbook/cli_validator_dry_run_v0.md](docs/runbook/cli_validator_dry_run_v0.md)
- Inventory CLI: [docs/runbook/cli_validator_inventory_v0.md](docs/runbook/cli_validator_inventory_v0.md)
- Gated apply stub: [docs/runbook/cli_validator_apply_gated_v0.md](docs/runbook/cli_validator_apply_gated_v0.md)

## CLI (local only)
```bash
python3 cli/validate_apply.py docs/runbook/applies/20260902_169.58.250.236_suno-sb.md --expect-stops HS03
python3 cli/validate_dry_run.py docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md
python3 cli/validate_inventory.py docs/runbook/runs/20260902_169.58.250.236.md
python3 cli/apply_gated.py \
  --inventory docs/runbook/runs/20260902_169.58.250.236.md \
  --dry-run docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md \
  --apply docs/runbook/applies/20260902_169.58.250.236_suno-sb.md
```
Does **not** apply on any host.

## CI
- Smoke: [docs/runbook/ci_cli_smoke_v0.md](docs/runbook/ci_cli_smoke_v0.md) (`.github/workflows/cli-smoke.yml`)
