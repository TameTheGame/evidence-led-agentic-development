#!/usr/bin/env python3
"""Rung-0 check that every file Git tracks under a project's assets folder has the .meta
S&box writes for it, tracked beside it. Example only: each project owns its own copy.

    python tools/check_metas.py [--assets PATH]

Run it from the project's root, in its Git checkout. --assets is the project's assets
folder (default Assets).

The first editor that opens a project writes a .meta holding a new GUID beside every
source it mounts that has none, in every folder at once. A source committed without its
.meta leaves the next editor run's working tree changed, so a check that needs a clean tree
fails there, after a run, on a file it didn't build. This check finds the gap without S&box.
It reads Git's index (git ls-files, so a staged file counts) and fails each tracked file
under the assets folder with no tracked <file>.meta beside it. Names are compared in any
letter case, as Windows and S&box compare them.

It leaves out the files S&box writes no .meta for:
  - a .meta itself;
  - a compiled file ending in _c and a file ending in _d, such as a scene's .scene_d,
    which S&box keeps with their source (Asset.cs, RelatedFileExts and GetMetadataFile);
  - notes and scripts kept beside the sources: .md, .py and .gitkeep, which got no .meta
    on 26.10.27c. Change NO_META if your build or project differs.

It prints MISSING for each file with no .meta, then one PASS, FAIL or NOT RUN line.
Exit code 0 pass, 1 fail, 2 not run: Git failed, or it tracks no file under the assets
folder, so a run from the wrong folder can't pass.
Dependency-free; Python 3.10 or newer.
"""

from __future__ import annotations

import subprocess
import sys

NO_META = (".meta", ".md", ".py", ".gitkeep")
RELATED = ("_c", "_d")


def needs_meta(path: str) -> bool:
    """Whether S&box writes a .meta for this file."""
    lowered = path.lower()
    return not lowered.endswith(NO_META + RELATED)


def missing_metas(tracked: list[str]) -> list[str]:
    """The tracked files that need a .meta and have none tracked beside them, in any case."""
    names = {p.lower() for p in tracked}
    return [p for p in sorted(tracked) if needs_meta(p) and f"{p}.meta".lower() not in names]


def main(argv: list[str]) -> int:
    args = list(argv)
    assets = "Assets"
    if "--assets" in args:
        at = args.index("--assets")
        if at + 1 >= len(args):
            print("NOT RUN - --assets needs a path")
            return 2
        assets = args[at + 1]
        del args[at:at + 2]
    if args:
        print(__doc__)
        return 2
    try:
        done = subprocess.run(["git", "ls-files", "-z", "--", assets], capture_output=True)
    except OSError as error:
        print(f"NOT RUN - git could not start: {error}")
        return 2
    if done.returncode != 0:
        print(f"NOT RUN - git ls-files failed: {done.stderr.decode(errors='replace').strip()}")
        return 2
    tracked = [p for p in done.stdout.decode("utf-8", errors="replace").split("\0") if p]
    if not tracked:
        print(f"NOT RUN - Git tracks no file under {assets}; run it from the project's root")
        return 2
    missing = missing_metas(tracked)
    for path in missing:
        print(f"MISSING  {path}.meta")
    counted = sum(needs_meta(p) for p in tracked)
    if missing:
        print(f"FAIL - {len(missing)} of {counted} tracked file(s) under {assets} have no .meta "
              "beside them. Open the project in an editor so S&box writes them, and commit "
              "each with its file.")
        return 1
    print(f"PASS - {counted} tracked file(s) under {assets}, each with its .meta.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
