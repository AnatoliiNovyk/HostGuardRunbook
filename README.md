# HostGuardRunbook

inventory → dry-run → apply

**Slogan:** NeighborSafe — не зламай сусіда на спільному IP.

**UX №1:** існуючий прод на тому ж хості (Coolify/Traefik multi-tenant).

## Docs
- Checklist: [docs/runbook/inventory_checklist_v1.md](docs/runbook/inventory_checklist_v1.md)
- Reference run (inventory-only): [docs/runbook/runs/20260902_169.58.250.236.md](docs/runbook/runs/20260902_169.58.250.236.md)
- Dry-run spec: [docs/runbook/dry_run_v0.md](docs/runbook/dry_run_v0.md)
- Apply spec (gates only, no host mutation from the doc): [docs/runbook/apply_v0.md](docs/runbook/apply_v0.md)
- CLI validator: [docs/runbook/cli_validator_v0.md](docs/runbook/cli_validator_v0.md)
- Dry-run CLI: [docs/runbook/cli_validator_dry_run_v0.md](docs/runbook/cli_validator_dry_run_v0.md)

## CLI (local only)
```bash
python3 cli/validate_apply.py docs/runbook/applies/20260902_169.58.250.236_suno-sb.md --expect-stops HS03
python3 cli/validate_dry_run.py docs/runbook/dry_runs/20260902_169.58.250.236_suno-sb.md
```
Does **not** apply on any host.
