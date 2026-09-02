#!/usr/bin/env python3
"""HostGuardRunbook gated apply stub: chain validators, NEVER mutate a host."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CLI_DIR = Path(__file__).resolve().parent


def run_validator(script: str, artifact: Path, expect_stops: str = "") -> tuple[int, str]:
    cmd = [sys.executable, str(CLI_DIR / script), str(artifact)]
    if expect_stops:
        cmd.extend(["--expect-stops", expect_stops])
    p = subprocess.run(cmd, capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Gated apply stub: validate inventory→dry-run→apply, refuse host apply."
    )
    ap.add_argument("--inventory", type=Path, required=True, help="docs/runbook/runs/*.md")
    ap.add_argument("--dry-run", type=Path, required=True, help="docs/runbook/dry_runs/*.md")
    ap.add_argument("--apply", type=Path, required=True, help="docs/runbook/applies/*.md")
    ap.add_argument(
        "--apply-expect-stops",
        default="",
        help="Optional expected stops for apply artifact (e.g. HS03 for blocked fixture).",
    )
    args = ap.parse_args(argv)

    stages = [
        ("inventory", "validate_inventory.py", args.inventory, ""),
        ("dry-run", "validate_dry_run.py", args.dry_run, ""),
        ("apply", "validate_apply.py", args.apply, args.apply_expect_stops),
    ]

    print("=== HostGuardRunbook apply_gated (STUB — no host apply) ===")
    failed = False
    for name, script, path, expect in stages:
        if not path.is_file():
            print(f"[{name}] error: missing {path}")
            failed = True
            continue
        code, out = run_validator(script, path, expect)
        print(f"[{name}] exit={code}")
        for line in out.splitlines():
            print(f"  {line}")
        if code != 0:
            failed = True

    if failed:
        print("result: GATED FAIL — host apply refused")
        return 1

    print("result: gates clear locally — STILL refusing host apply (stub)")
    print("action: none (no SSH, no docker, no mutate)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
