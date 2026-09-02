#!/usr/bin/env python3
"""HostGuardRunbook inventory run validator (local only; never applies)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_IDS = [f"{i:02d}" for i in range(1, 17)]


def parse_meta(text: str) -> dict[str, str]:
    meta = {}
    for line in text.splitlines():
        m = re.match(r"^-\s+\*?\*?([^:**]+)\*?\*?:\s*(.+)$", line.strip())
        if m:
            meta[m.group(1).strip().lower()] = m.group(2).strip()
    return meta


def parse_rows(text: str) -> dict[str, dict[str, str]]:
    """Parse checklist rows; observed/evidence may contain raw | characters."""
    rows: dict[str, dict[str, str]] = {}
    row_re = re.compile(
        r"^\|\s*(\d{2})\s*\|\s*([^|]*?)\|\s*([^|]*?)\|\s*(.*?)\|\s*(pass|fail|skip)\s*\|\s*(.*?)\s*\|?\s*$",
        re.I,
    )
    for line in text.splitlines():
        m = row_re.match(line.strip())
        if not m:
            continue
        rid, check, expected, observed, verdict, evidence = m.groups()
        rows[rid] = {
            "check": check.strip(),
            "expected": expected.strip(),
            "observed": observed.strip(),
            "verdict": verdict.lower().strip(),
            "evidence": evidence.strip(),
        }
    return rows


def validate_inventory(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    stops: list[str] = []
    meta = parse_meta(text)
    mode = meta.get("mode", "").lower()
    status = meta.get("status", "").lower()
    if "inventory" not in mode and "inventory-only" not in mode:
        if "inventory-only" not in text.lower():
            stops.append("META:mode_not_inventory_only")
    if "complete" not in status and "complete" not in text.lower():
        stops.append("META:status_not_complete")
    rows = parse_rows(text)
    for rid in REQUIRED_IDS:
        if rid not in rows:
            stops.append(f"META:missing_row_{rid}")
            continue
        v = rows[rid]["verdict"].strip("*` ")
        ev = rows[rid]["evidence"].strip()
        if v not in {"pass", "fail", "skip"}:
            stops.append(f"META:bad_verdict_{rid}")
        if v != "skip" and not ev:
            stops.append(f"META:no_evidence_{rid}")
    return sorted(set(stops))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate inventory run markdown (no host apply).")
    p.add_argument("path", type=Path)
    p.add_argument("--expect-stops", default="")
    args = p.parse_args(argv)
    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2
    stops = validate_inventory(args.path)
    expect = {s.strip() for s in args.expect_stops.split(",") if s.strip()}
    print(f"file: {args.path}")
    print(f"stops: {', '.join(stops) if stops else '(none)'}")
    if expect:
        missing, extra = expect - set(stops), set(stops) - expect
        if missing or extra:
            if missing:
                print(f"error: expected stops not seen: {', '.join(sorted(missing))}", file=sys.stderr)
            if extra:
                print(f"error: unexpected stops: {', '.join(sorted(extra))}", file=sys.stderr)
            return 1
        print("ok: expected stops matched")
        return 0
    if stops:
        print("result: inventory gates fail; no host apply performed")
        return 1
    print("result: inventory run OK (still does NOT apply on host)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
