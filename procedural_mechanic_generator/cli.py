"""CLI entry point for the mechanic generator."""

from __future__ import annotations

import argparse
import json
import sys

from .service import MechanicGeneratorService


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Procedural Game Mechanic Generator")
    parser.add_argument("--theme")
    parser.add_argument("--genre")
    parser.add_argument("--complexity")
    parser.add_argument("--mechanic-type", dest="mechanic_type")
    parser.add_argument("--constraints", nargs="*", default=[])
    parser.add_argument("--demo-mode", action="store_true")
    parser.add_argument("--debug", action="store_true")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    service = MechanicGeneratorService()
    result = service.generate(vars(args))
    payload = {"success": result.success, "output": result.output, "errors": result.errors, "logs": result.logs}
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
