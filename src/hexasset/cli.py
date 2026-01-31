from __future__ import annotations

import argparse
import os
import sys

from .core import find_matches, parse_hex_color


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Find matching colour assets by hex in an Xcode project."
    )
    parser.add_argument("hex", help="Hex colour: #RRGGBB, RRGGBB, or 0xRRGGBB")
    # Backwards-compatible with your script: optional positional path
    parser.add_argument(
        "project_dir",
        nargs="?",
        default=".",
        help="Path to scan (defaults to current directory)",
    )

    args = parser.parse_args()

    try:
        # Validate early so we return exit code 2 for bad input, same as your script
        parse_hex_color(args.hex)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    project_dir = os.path.abspath(args.project_dir)
    if not os.path.isdir(project_dir):
        print(f"error: project directory not found: {project_dir}", file=sys.stderr)
        return 2

    matches = find_matches(project_dir=project_dir, hex_value=args.hex)

    if not matches:
        print("NO_MATCH")
        return 1

    for m in matches:
        alpha_out = m.alpha if m.alpha is not None else "unknown"
        print(f"{m.name} alpha = {alpha_out}")

    return 0
