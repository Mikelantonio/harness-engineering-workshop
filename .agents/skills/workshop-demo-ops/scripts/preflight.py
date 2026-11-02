#!/usr/bin/env python3
"""Offline preflight for ADK workshop environments (no secrets printed)."""
import argparse
from importlib import metadata
import os
import platform
import sys


def status_line(name: str, ok: bool, detail: str) -> None:
    print(f"[{'OK' if ok else 'WARN'}] {name}: {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-key", action="store_true", help="Fail when GOOGLE_API_KEY is not in process environment")
    args = parser.parse_args()
    python_ok = sys.version_info >= (3, 10)
    status_line("Python", python_ok, platform.python_version())
    try:
        version = metadata.version("google-adk")
        pkg_ok = True
    except metadata.PackageNotFoundError:
        pkg_ok = False
        version = "not installed"
    status_line("google-adk package", pkg_ok, version)
    has_key = bool(os.environ.get("GOOGLE_API_KEY"))
    status_line("GOOGLE_API_KEY process env", has_key, "present (hidden)" if has_key else "not set")
    print("NOTE: This script does not parse .env files, call Gemini, verify quotas or test networking.")
    return 1 if not python_ok or not pkg_ok or (args.require_key and not has_key) else 0


if __name__ == "__main__":
    raise SystemExit(main())
