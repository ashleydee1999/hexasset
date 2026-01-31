from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Optional


# Accept: #RRGGBB, RRGGBB, 0xRRGGBB
HEX_RE = re.compile(r"^(?:#|0x)?([0-9a-fA-F]{6})$")


@dataclass(frozen=True)
class Match:
    name: str
    alpha: Optional[str]


def parse_hex_color(hex_str: str) -> dict[str, str]:
    m = HEX_RE.match(hex_str.strip())
    if not m:
        raise ValueError("hex must be in the form #RRGGBB, RRGGBB, or 0xRRGGBB")

    hex_val = m.group(1).upper()
    return {
        "red": f"0x{hex_val[0:2]}",
        "green": f"0x{hex_val[2:4]}",
        "blue": f"0x{hex_val[4:6]}",
    }


def matching_alpha(contents_path: str, target: dict[str, str]) -> Optional[str]:
    try:
        with open(contents_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None

    colors = data.get("colors")
    if not colors:
        return None

    for color in colors:
        comps = color.get("color", {}).get("components", {})
        if not comps:
            continue
        if all(comps.get(k) == v for k, v in target.items()):
            return comps.get("alpha")

    return None


def is_within_xcassets(path: str) -> bool:
    parts = os.path.normpath(path).split(os.sep)
    return any(p.endswith(".xcassets") for p in parts)


def find_matches(project_dir: str, hex_value: str) -> list[Match]:
    target = parse_hex_color(hex_value)

    matches: list[Match] = []

    # Keep it snappy. These folders commonly exist and are never relevant.
    skip_dirs = {
        ".git",
        "DerivedData",
        "Pods",
        "Carthage",
        ".build",
        "build",
        "node_modules",
    }

    for dirpath, dirnames, filenames in os.walk(project_dir):
        # Prevent descending into junk
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]

        if not dirpath.endswith(".colorset"):
            continue
        if "Contents.json" not in filenames:
            continue
        if not is_within_xcassets(dirpath):
            continue

        contents_path = os.path.join(dirpath, "Contents.json")
        alpha = matching_alpha(contents_path, target)
        if alpha is not None:
            colorset_name = os.path.basename(os.path.dirname(contents_path))
            if colorset_name.endswith(".colorset"):
                colorset_name = colorset_name[:-9]
            matches.append(Match(name=colorset_name, alpha=alpha))

    # Deterministic ordering so output is stable between runs
    matches.sort(key=lambda m: (m.name.lower(), m.alpha or ""))

    return matches