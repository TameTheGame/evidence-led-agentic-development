#!/usr/bin/env python3
"""Checks spec_lint.py against its fixtures. Dependency-free; needs git on PATH.

    python examples/sbox/tools/test_spec_lint.py

Each case commits fixtures/base.spec.md and the stand-in sources in fixtures/sources/ in a
throwaway git repository, replaces the spec with a variant, runs the lint, and checks the
exit code and output. It writes its own output as UTF-8, since a failing case prints the
lint's.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT = HERE / "spec_lint.py"
FIXTURES = HERE / "fixtures"

SOURCES = ["--sources", "UnitTests", "--sources", "tools"]
# Each check runs with a cp1252 stdout, as Windows gives a pipe, and its output is read as
# UTF-8, so a case with characters outside cp1252 fails unless the check writes UTF-8. UTF-8
# mode is off, as Python starts on Windows by default, so a text run decodes in the ANSI code
# page even where the runner sets PYTHONUTF8=1, which would hide the non-ASCII folder case.
PIPE = {"PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"}

CASES = [
    # (variant, extra arguments, expected exit, text that must appear, text that must not appear,
    # and the folder the repository sits in, if any)
    ("base.spec.md", SOURCES, 0, ["PASS", "no agreed requirement changed"],
     ["NEEDS OWNER", "NOT FOUND", "FAIL", "note"]),
    ("base.spec.md", [], 0, ["PASS", "note  check names not looked up"], ["NOT FOUND", "FAIL"]),
    ("agreed-sentence-changed.spec.md", SOURCES, 0,
     ["NEEDS OWNER: YARD-SIGHT-01", "sentence changed", "PASS"], ["FAIL"]),
    ("agreed-sentence-unicode.spec.md", SOURCES, 0,
     ["NEEDS OWNER: YARD-SIGHT-01", "at every spawn · ≥ 2 m →\"", "PASS"], ["FAIL", "\ufffd", "spawn · ?"]),
    ("draft-changed.spec.md", SOURCES, 0, ["PASS", "no agreed requirement changed"],
     ["NEEDS OWNER", "FAIL"]),
    ("check-not-written.spec.md", SOURCES, 0,
     ["NOT FOUND: YARD-ROUTE-01", "YARD_ROUTE_01_RouteIsClear", "1 check(s) not found", "PASS"],
     ["FAIL", "NOT FOUND: YARD-SIGHT-01", "NOT FOUND: YARD-DATA-01"]),
    # The repository under a folder with a non-ASCII name. A lint that reads Git's path in the
    # ANSI code page, as a text run does on Windows, skips the owner gate here.
    ("agreed-sentence-changed.spec.md", SOURCES, 0, ["NEEDS OWNER: YARD-SIGHT-01", "PASS"],
     ["owner gate and retired-ID check skipped", "FAIL"], "Übung ü"),
    ("bad-format.spec.md", SOURCES, 1,
     ["duplicate ID", "state \"approved\"", "rung \"vibes\"", "agreed requirement has no check",
      "spec/yard.spec.md:29: heading is not shaped"], []),
    ("bad-checks.spec.md", SOURCES, 1,
     ["Yard-1: ID is not shaped AREA-TOPIC-NN", "YARD-GATE-01: was retired at HEAD",
      "YARD-LOOK-01: owner-rung check \"YARD_LOOK_01_LooksLivedIn\" is not a card",
      "YARD-NET-01: card NET-1 is not defined"],
     ["YARD-FEEL-01:", "NOT FOUND"]),
]


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=Test Owner", "-c", "user.email=owner@example.invalid",
                    *args], cwd=repo, check=True, capture_output=True)


def run_case(variant: str, extra: list[str], folder: str = "") -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / folder
        shutil.copytree(FIXTURES / "sources", repo, dirs_exist_ok=True)
        (repo / "spec").mkdir()
        target = repo / "spec" / "yard.spec.md"
        shutil.copyfile(FIXTURES / "base.spec.md", target)
        git(repo, "init", "-q")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "Base spec")
        shutil.copyfile(FIXTURES / variant, target)
        result = subprocess.run([sys.executable, str(LINT), *extra], cwd=repo, capture_output=True,
                                text=True, encoding="utf-8", errors="replace",
                                env={**os.environ, **PIPE})
        return result.returncode, result.stdout + result.stderr


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # a failing case prints the lint's output
        stream.reconfigure(encoding="utf-8", errors="replace")
    failures = 0
    for variant, extra, code, present, absent, *where in CASES:
        folder = where[0] if where else ""
        got_code, output = run_case(variant, extra, folder)
        missing = [t for t in present if t not in output]
        unwanted = [t for t in absent if t in output]
        ok = got_code == code and not missing and not unwanted
        failures += not ok
        shown = f"{variant} {' '.join(extra)}".strip() + (f" in {folder}" if folder else "")
        print(f"{'PASS' if ok else 'FAIL'}  {shown}: exit {got_code}")
        if not ok:
            print(f"      expected exit {code}; missing {missing}; unexpected {unwanted}")
            print("      " + output.replace("\n", "\n      "))
    print(f"{'PASS' if not failures else 'FAIL'} - {len(CASES) - failures} of {len(CASES)} cases.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
