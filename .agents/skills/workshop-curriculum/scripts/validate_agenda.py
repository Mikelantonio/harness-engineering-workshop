#!/usr/bin/env python3
"""Validate a workshop agenda JSON (offline, stdlib only)."""
import argparse
import json
import sys
from pathlib import Path

KINDS = {"theory", "demo", "lab", "review", "break", "qa"}

def validate(data, expected=None, min_ratio=0.4):
    errors = []
    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        return ["'blocks' must be a non-empty list"], {}
    gross = net = lab = 0
    for index, block in enumerate(blocks, start=1):
        if not isinstance(block, dict):
            errors.append(f"Block {index}: must be an object")
            continue
        kind, duration = block.get("kind"), block.get("minutes")
        if kind not in KINDS:
            errors.append(f"Block {index}: invalid kind '{kind}'")
        if type(duration) is not int or duration <= 0:
            errors.append(f"Block {index}: 'minutes' must be a positive integer")
            continue
        gross += duration
        if kind != "break": net += duration
        if kind == "lab": lab += duration
    ratio = lab / net if net else 0
    if expected is not None and gross != expected:
        errors.append(f"Expected {expected} gross minutes, got {gross}")
    if ratio < min_ratio:
        errors.append(f"Practice ratio {ratio:.0%} below threshold {min_ratio:.0%}")
    return errors, {"gross_minutes": gross, "net_minutes": net, "lab_minutes": lab, "practice_ratio": round(ratio, 3)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agenda", type=Path)
    parser.add_argument("--expected-minutes", type=int)
    parser.add_argument("--minimum-practice-ratio", type=float, default=0.4)
    args = parser.parse_args()
    if not 0 <= args.minimum_practice_ratio <= 1:
        parser.error("--minimum-practice-ratio must be between 0 and 1")
    try:
        data = json.loads(args.agenda.read_text(encoding="utf-8"))
        errors, stats = validate(data, args.expected_minutes, args.minimum_practice_ratio)
    except (OSError, ValueError, AttributeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    for err in errors: print(f"ERROR: {err}", file=sys.stderr)
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
