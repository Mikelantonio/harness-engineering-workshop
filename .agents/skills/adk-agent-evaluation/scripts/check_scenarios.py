#!/usr/bin/env python3
"""Lint custom workshop scenario files; this is NOT an ADK native evaluator."""
import argparse
import json
from pathlib import Path

REQUIRED = {"id", "category", "input", "expected", "metric"}


def validate(data):
    errors = []
    scenarios = data.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        return ["scenarios must be a non-empty list"]
    seen = set()
    for n, item in enumerate(scenarios, 1):
        if not isinstance(item, dict):
            errors.append(f"{n}: scenario must be an object")
            continue
        for field in sorted(REQUIRED):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{n}: field '{field}' must be a non-empty string")
        sid = item.get("id")
        if isinstance(sid, str) and sid in seen:
            errors.append(f"{n}: duplicate ID '{sid}'")
        if isinstance(sid, str): seen.add(sid)
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    errors = validate(data)
    if errors:
        for error in errors: print("ERROR:", error)
        return 1
    print(f"OK: {len(data['scenarios'])} valid custom scenarios (schema lint only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
