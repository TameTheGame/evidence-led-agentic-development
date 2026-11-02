#!/usr/bin/env python3
"""Checks check_metas.py against small throwaway Git repositories. Needs Git; otherwise
dependency-free.

    python examples/sbox/tools/test_check_metas.py

Each case builds a project in a temporary folder, stages its files with git add (the check
reads Git's index, so nothing is committed), changes it, runs the check from the project's
root, and checks the exit code and output. The project holds a scene, an image whose .meta
S&box wrote with a lower-cased name, a material, and files S&box writes no .meta for.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK = HERE / "check_metas.py"

SOURCES = [
    "Assets/scenes/yard.scene",
    "Assets/materials/sand.vmat",
    "Assets/materials/Sand_Color.png",
]
METAS = [
    "Assets/scenes/yard.scene.meta",
    "Assets/materials/sand.vmat.meta",
    "Assets/materials/sand_color.png.meta",
]
NO_META = [
    "Assets/scenes/yard.scene_d",
    "Assets/scenes/yard_scene_data/probe.vtex_c",
    "Assets/materials/README.md",
    "Assets/materials/make_sand.py",
    "Assets/empty/.gitkeep",
    "tools/build.ps1",
]


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def write(root: Path, *names: str) -> None:
    for name in names:
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text("{}\n", encoding="utf-8")


def build(root: Path) -> None:
    git(root, "init", "-q")
    write(root, *SOURCES, *METAS, *NO_META)
    git(root, "add", "-A")


def unstage(*names: str):
    return lambda root: git(root, "rm", "-q", "--cached", "--", *names)


def add(*names: str):
    def change(root: Path) -> None:
        write(root, *names)
        git(root, "add", "--", *names)
    return change


def untracked(*names: str):
    return lambda root: write(root, *names)


def assets_named(name: str):
    def change(root: Path) -> None:
        git(root, "mv", "Assets", name)
    return change


CASES = [
    # (name, change, arguments, expected exit, text that must appear, text that must not)
    ("every source has its .meta, one in another letter case", None, [], 0,
     ["PASS - 3 tracked file(s) under Assets, each with its .meta."], ["MISSING", "FAIL"]),
    ("files S&box writes no .meta for are left out", None, [], 0,
     ["PASS - 3 tracked"], ["yard.scene_d.meta", "probe.vtex_c.meta", "README.md.meta",
                            "make_sand.py.meta", ".gitkeep.meta", "build.ps1"]),
    ("a staged source and .meta count", add("Assets/sounds/wind.wav", "Assets/sounds/wind.wav.meta"),
     [], 0, ["PASS - 4 tracked file(s) under Assets"], ["MISSING"]),
    ("control: a source with no .meta", add("Assets/sounds/wind.wav"), [], 1,
     ["MISSING  Assets/sounds/wind.wav.meta", "FAIL - 1 of 4 tracked file(s) under Assets"],
     ["PASS"]),
    ("control: a source whose .meta isn't tracked",
     lambda root: (unstage("Assets/materials/sand.vmat.meta")(root),
                   untracked("Assets/materials/sand.vmat.meta")(root)), [], 1,
     ["MISSING  Assets/materials/sand.vmat.meta"], ["PASS"]),
    ("control: a .meta for another name",
     lambda root: (unstage("Assets/materials/sand_color.png.meta")(root),
                   add("Assets/materials/sand_colour.png.meta")(root)), [], 1,
     ["MISSING  Assets/materials/Sand_Color.png.meta"], ["PASS"]),
    ("control: a scene with no .meta", unstage("Assets/scenes/yard.scene.meta"), [], 1,
     ["MISSING  Assets/scenes/yard.scene.meta"], ["PASS"]),
    ("another assets folder with --assets", assets_named("Content"), ["--assets", "Content"], 0,
     ["PASS - 3 tracked file(s) under Content"], ["MISSING"]),
    ("not run: no tracked file under the assets folder", None, ["--assets", "Elsewhere"], 2,
     ["NOT RUN - Git tracks no file under Elsewhere"], ["PASS"]),
    ("not run: not a Git repository", "no-git", [], 2, ["NOT RUN - git ls-files failed"],
     ["PASS"]),
]


def run_case(change, args: list[str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "project"
        root.mkdir()
        env = dict(os.environ, GIT_CEILING_DIRECTORIES=str(Path(tmp)))
        if change == "no-git":
            write(root, *SOURCES)
        else:
            build(root)
            if change:
                change(root)
        done = subprocess.run([sys.executable, str(CHECK), *args], cwd=root, env=env,
                              capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr


def main() -> int:
    failures = 0
    for name, change, args, want_code, must, must_not in CASES:
        code, out = run_case(change, args)
        problems = []
        if code != want_code:
            problems.append(f"exit {code}, expected {want_code}")
        problems += [f"missing {t!r}" for t in must if t not in out]
        problems += [f"unexpected {t!r}" for t in must_not if t in out]
        if problems:
            failures += 1
            print(f"FAIL  {name}: {'; '.join(problems)}\n{out}")
        else:
            print(f"PASS  {name}")
    print(f"{'FAIL' if failures else 'PASS'} - {len(CASES) - failures} of {len(CASES)} cases passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
