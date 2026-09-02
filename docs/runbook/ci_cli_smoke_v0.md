# ci_cli_smoke_v0

## Purpose
GitHub Actions smoke на fixtures (без хоста).

## Workflow
`.github/workflows/cli-smoke.yml` — push/PR → ubuntu + Python 3.12.

## Expectations
| step | expect |
|------|--------|
| validate_inventory | exit 0, stops none |
| validate_dry_run | exit 0, stops none |
| validate_apply | exit 0 with `--expect-stops HS03` |
| apply_gated | exit 1, output contains `GATED FAIL` |

## Non-goals
Host apply / SSH / docker mutate.
