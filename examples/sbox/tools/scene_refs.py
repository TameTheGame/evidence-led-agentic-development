#!/usr/bin/env python3
"""Rung-0 check for clearing out files a project's scenes may use, such as old light,
navigation, or envmap bakes. Example only: each project owns its own copy.

    python tools/scene_refs.py FOLDER [--assets PATH]

FOLDER is the folder to clear out, such as Assets/scenes/outpost_scene_data/ddgi.
--assets is the project's assets root (default Assets); resource paths are relative to it.

It reads every .scene and .prefab file under the assets root and collects each string in
it. S&box writes a resource path lower-cased, with forward slashes and without a compiled
file's "_c" ending, while the file on disk keeps the casing it was written with and that
ending. So a reference and a file name are compared the way S&box normalizes a path:
lower case, forward slashes, no leading slash, and no trailing "_c".

It prints:
  - IN USE: each file under FOLDER that a scene or prefab references;
  - UNUSED: each file under FOLDER that none references; only these may go; and
  - MISSING: each reference into FOLDER that no file answers.

It deletes nothing. Run it before a clean-up and move or delete only UNUSED files. Run it
again afterwards: it must pass, with the same IN USE files.

Exit code 1 when a reference into FOLDER is MISSING, or when FOLDER isn't a folder under
the assets root. So it fails after a clean-up that took a file still in use.
Dependency-free; Python 3.10 or newer.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REFERRERS = ("*.scene", "*.prefab")
QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')


def normalize(path: str) -> str:
    """A path as S&box keys a resource: lower case, forward slashes, no leading slash, no
    trailing "_c"."""
    path = path.replace("\\", "/").lower().lstrip("/")
    return path[:-2] if path.endswith("_c") else path


def strings(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings(v)]
    return []


def references(assets: Path) -> dict[str, list[str]]:
    """Each normalized string in the scenes and prefabs, with the files it appears in."""
    found: dict[str, list[str]] = {}
    for pattern in REFERRERS:
        for path in sorted(assets.rglob(pattern)):
            text = path.read_text(encoding="utf-8", errors="replace")
            try:
                values = strings(json.loads(text))
            except json.JSONDecodeError:
                values = QUOTED.findall(text)
            for value in values:
                found.setdefault(normalize(value), []).append(path.relative_to(assets).as_posix())
    return found


def main(argv: list[str]) -> int:
    args = list(argv)
    assets = Path("Assets")
    if "--assets" in args:
        at = args.index("--assets")
        if at + 1 >= len(args):
            print("FAIL  --assets needs a path")
            return 1
        assets = Path(args[at + 1])
        del args[at:at + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return 1
    folder = Path(args[0])
    try:
        inside = folder.resolve().relative_to(assets.resolve())
    except ValueError:
        inside = None
    if inside is None or not folder.is_dir():
        print(f"FAIL  {folder} is not a folder under the assets root {assets}")
        return 1

    refs = references(assets)
    prefix = normalize(inside.as_posix()).rstrip("/") + "/"
    keys: set[str] = set()
    in_use: list[str] = []
    unused: list[str] = []
    for path in sorted(p for p in folder.rglob("*") if p.is_file()):
        key = normalize(path.resolve().relative_to(assets.resolve()).as_posix())
        keys.add(key)
        (in_use if key in refs else unused).append(path.as_posix())
    missing = sorted((ref, where) for ref, where in refs.items()
                     if ref.startswith(prefix) and ref not in keys)

    for path in in_use:
        print(f"IN USE   {path}")
    for path in unused:
        print(f"UNUSED   {path}")
    for ref, where in missing:
        print(f"MISSING  {ref} (in {', '.join(sorted(set(where)))})")
    summary = f"{len(in_use)} in use, {len(unused)} unused, {len(missing)} missing in {folder.as_posix()}"
    if missing:
        print(f"FAIL - {summary}: a scene or prefab references a file that isn't there.")
        return 1
    print(f"PASS - {summary}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
