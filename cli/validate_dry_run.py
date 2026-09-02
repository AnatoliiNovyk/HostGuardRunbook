#!/usr/bin/env python3
"""HostGuardRunbook dry-run artifact validator (local only; never applies)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADER_KEYS = (
    "inventory_ref",
    "scope_stack",
    "leave_neighbors",
    "touches_foreign",
    "verdict",
)
F_IDS = ("F01", "F02", "F03", "F04", "F05", "F06")


def parse_wide_header(text: str) -> dict[str, str]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= {"-", " ", ":"} for c in cells):
            continue
        rows.append(cells)
        if len(rows) >= 2:
            break
    if len(rows) < 2:
        return {}
    keys, vals = rows[0], rows[1]
    return {k.strip("`"): v for k, v in zip(keys, vals)}


def parse_f_gate(text: str) -> dict[str, str]:
    results: dict[str, str] = {}
    in_gate = False
    for line in text.splitlines():
        if re.match(r"(?im)^##\s+Hard fail gate\b", line):
            in_gate = True
            continue
        if in_gate and re.match(r"(?im)^##\s+", line):
            break
        if not in_gate or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in F_IDS:
            results[cells[0]] = cells[2]
    return results


def f_result_pass(result: str) -> bool:
    return result.lower().startswith("pass")


def validate_dry_run(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    header = parse_wide_header(text)
    stops: list[str] = []
    for k in HEADER_KEYS:
        if k not in header or not header[k].strip():
            stops.append(f"META:missing_{k}")
    touches = re.sub(r"[*`]", "", header.get("touches_foreign", "")).strip().lower()
    if touches and touches != "no":
        stops.extend(["F06", "TOUCHES_FOREIGN"])
    verdict = re.sub(r"[*`]", "", header.get("verdict", "")).strip().lower()
    inv = header.get("inventory_ref", "")
    if inv and "runs/" not in inv:
        stops.append("F06")
    fgate = parse_f_gate(text)
    for fid in F_IDS:
        if fid not in fgate:
            stops.append(f"META:missing_{fid}")
        elif not f_result_pass(fgate[fid]):
            stops.append(fid)
    in_diff = False
    for line in text.splitlines():
        if re.match(r"(?im)^##\s+Diff rows\b", line):
            in_diff = True
            continue
        if in_diff and re.match(r"(?im)^##\s+", line):
            break
        if not in_diff or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 6:
            continue
        if cells[0].lower() in {"id"} or set(cells[0]) <= {"-"}:
            continue
        owner, action = cells[4].lower(), cells[5].lower()
        evidence = cells[6] if len(cells) > 6 else ""
        if owner == "foreign" and action not in {"none", "leave", "n/a"}:
            stops.append("TOUCHES_FOREIGN")
        if re.match(r"^R\d+", cells[0]) and not evidence.strip():
            stops.append("F06")
    if ("TOUCHES_FOREIGN" in stops or any(f in stops for f in F_IDS)) and verdict == "pass":
        stops.append("META:verdict_pass_but_gates_failed")
    return sorted(set(stops))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate HostGuardRunbook dry-run markdown (no host apply).")
    p.add_argument("path", type=Path)
    p.add_argument("--expect-stops", default="")
    args = p.parse_args(argv)
    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2
    stops = validate_dry_run(args.path)
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
        print("result: fail/blocked gates; no host apply performed")
        return 1
    print("result: dry-run gates clear (still does NOT apply on host)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
