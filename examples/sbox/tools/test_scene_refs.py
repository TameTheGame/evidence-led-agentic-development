#!/usr/bin/env python3
"""Checks scene_refs.py against a small throwaway project. Dependency-free.

    python examples/sbox/tools/test_scene_refs.py

Each case builds the project in a temporary folder, changes it, runs the check, and checks
the exit code and output. The project's scene references its newest light bake the way
S&box writes it, lower-cased and without "_c"; the files keep their capitals and "_c".
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECK = HERE / "scene_refs.py"

DATA = "Assets/scenes/yard_scene_data/ddgi"
OLD = f"{DATA}/Yard_Irradiance_1f2e_0a0a.vtex_c"
NEW = f"{DATA}/Yard_Irradiance_1f2e_0b0b.vtex_c"
NAV = f"{DATA}/Yard_Distance_1f2e_0b0b.vtex_c"


def build(root: Path) -> None:
    for name in (OLD, NEW, NAV):
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_bytes(b"")
    scene = {"GameObjects": [{"Name": "Yard", "Components": [{
        "__type": "Sandbox.IndirectLightVolume",
        "IrradianceTexture": "scenes/yard_scene_data/ddgi/yard_irradiance_1f2e_0b0b.vtex",
        "Material": "materials/dev/reflectivity_30.vmat"}]}]}
    (root / "Assets/scenes/yard.scene").write_text(json.dumps(scene), encoding="utf-8")
    prefab = {"RootObject": {"Components": [{
        "DistanceTexture": "/Scenes/Yard_Scene_Data/DDGI/Yard_Distance_1f2e_0b0b.vtex_c"}]}}
    (root / "Assets/prefabs").mkdir(parents=True)
    (root / "Assets/prefabs/lamp.prefab").write_text(json.dumps(prefab), encoding="utf-8")


def delete(*names: str):
    return lambda root: [(root / n).unlink() for n in names]


CASES = [
    # (name, change, folder argument, expected exit, text that must appear, text that must not)
    ("before a clean-up", None, DATA, 0,
     [f"IN USE   {NEW}", f"IN USE   {NAV}", f"UNUSED   {OLD}", "PASS - 2 in use, 1 unused, 0 missing"],
     ["MISSING", f"UNUSED   {NEW}", f"UNUSED   {NAV}"]),
    ("after deleting the unused bake", delete(OLD), DATA, 0,
     ["PASS - 2 in use, 0 unused, 0 missing"], ["MISSING", "UNUSED"]),
    ("control: after deleting the bake in use", delete(NEW), DATA, 1,
     ["MISSING  scenes/yard_scene_data/ddgi/yard_irradiance_1f2e_0b0b.vtex (in scenes/yard.scene)",
      "FAIL - 1 in use, 1 unused, 1 missing"], ["PASS"]),
    ("control: after deleting a file a prefab uses", delete(NAV), DATA, 1,
     ["MISSING  scenes/yard_scene_data/ddgi/yard_distance_1f2e_0b0b.vtex (in prefabs/lamp.prefab)"],
     ["PASS"]),
    ("a folder outside the assets root", None, "elsewhere", 1, ["is not a folder under"], ["PASS"]),
]


def run_case(change, folder: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        build(root)
        if change:
            change(root)
        done = subprocess.run([sys.executable, str(CHECK), folder], cwd=root,
                              capture_output=True, text=True)
        return done.returncode, done.stdout + done.stderr


def main() -> int:
    failures = 0
    for name, change, folder, want_code, must, must_not in CASES:
        code, out = run_case(change, folder)
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
