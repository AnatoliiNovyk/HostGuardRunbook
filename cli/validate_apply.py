#!/usr/bin/env python3
"""HostGuardRunbook apply-artifact validator (local only; never SSHs or applies)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_HEADER = (
    "inventory_ref",
    "dry_run_ref",
    "scope_stack",
    "leave_neighbors",
    "touches_foreign",
    "f_gate",
    "apply",
    "approve",
    "verdict",
)


def parse_header_table(text: str) -> dict[str, str]:
    """Parse markdown table rows `| field | value |` after the first header separator."""
    fields: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        key, val = cells[0], cells[1]
        if key.lower() in {"field", "-------", "---"} or set(key) <= {"-", " "}:
            continue
        if key in REQUIRED_HEADER or key.replace("`", "") in REQUIRED_HEADER:
            fields[key.strip("`")] = val
    return fields


def has_post_check_section(text: str) -> bool:
    return bool(re.search(r"(?im)^##\s+post_check\b", text))


def approve_present(approve_val: str) -> bool:
    v = approve_val.lower()
    if not approve_val.strip():
        return False
    if "missing" in v or "відсутн" in v or "*(" in approve_val:
        return False
    if "hs03" in v and "missing" in v:
        return False
    return bool(re.search(r"[A-Za-zА-Яа-яІіЇїЄє0-9_]{2,}", approve_val)) and "missing" not in v


def validate_apply_artifact(path: Path) -> list[str]:
    """Return list of hard-stop ids that fire. Empty list => structurally OK for apply=yes path."""
    text = path.read_text(encoding="utf-8")
    header = parse_header_table(text)
    stops: list[str] = []

    missing = [k for k in REQUIRED_HEADER if k not in header]
    if missing:
        stops.append(f"META:missing_header_fields:{','.join(missing)}")

    touches = header.get("touches_foreign", "").strip().lower()
    if touches and touches not in {"no", "**no**"}:
        stops.append("HS02")

    f_gate = re.sub(r"[*`]", "", header.get("f_gate", "")).strip().lower()
    if f_gate == "fail":
        stops.append("HS01")

    apply_val = re.sub(r"[*`]", "", header.get("apply", "")).strip().lower()
    verdict = re.sub(r"[*`]", "", header.get("verdict", "")).strip().lower()
    approve_val = header.get("approve", "")

    if not approve_present(approve_val):
        stops.append("HS03")

    if not has_post_check_section(text):
        stops.append("HS05")

    step_header = None
    for line in text.splitlines():
        if "rollback_id" in line and line.strip().startswith("|") and "step" in line.lower():
            step_header = line
            break
    in_steps = False
    for line in text.splitlines():
        if re.match(r"(?im)^##\s+steps\b", line):
            in_steps = True
            continue
        if in_steps and re.match(r"(?im)^##\s+", line):
            break
        if in_steps and line.strip().startswith("|") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if cells and cells[0].lower() in {"id", "---"}:
                continue
            if "empty" in line.lower() or "blocked" in line.lower():
                continue
            if len(cells) >= 2 and cells[0] and not cells[0].startswith("*"):
                if re.match(r"^[A-Za-z]?\d+", cells[0]):
                    if step_header is None or "rollback_id" not in step_header:
                        stops.append("HS04")
                        break

    if "HS03" in stops:
        if apply_val not in {"no", "n"}:
            stops.append("META:apply_should_be_no_when_HS03")
        if verdict not in {"blocked", "block"}:
            stops.append("META:verdict_should_be_blocked_when_HS03")

    return sorted(set(stops))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Validate HostGuardRunbook apply markdown artifacts (no host apply).")
    p.add_argument("path", type=Path, help="Path to applies/*.md artifact")
    p.add_argument(
        "--expect-stops",
        default="",
        help="Comma-separated hard-stop ids that MUST fire (e.g. HS03). Empty = expect no stops.",
    )
    args = p.parse_args(argv)

    if not args.path.is_file():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 2

    stops = validate_apply_artifact(args.path)
    expect = {s.strip() for s in args.expect_stops.split(",") if s.strip()}

    print(f"file: {args.path}")
    print(f"stops: {', '.join(stops) if stops else '(none)'}")

    if expect:
        missing = expect - set(stops)
        extra = set(stops) - expect
        if missing or extra:
            if missing:
                print(f"error: expected stops not seen: {', '.join(sorted(missing))}", file=sys.stderr)
            if extra:
                print(f"error: unexpected stops: {', '.join(sorted(extra))}", file=sys.stderr)
            return 1
        print("ok: expected stops matched")
        return 0

    if stops:
        print("result: blocked/fail (see stops); no host apply performed")
        return 1

    print("result: gates clear (still does NOT apply on host)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
