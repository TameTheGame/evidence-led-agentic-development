#!/usr/bin/env python3
"""Checks spec_lint.py against its fixtures. Dependency-free; needs git on PATH.

    python examples/sbox/tools/test_spec_lint.py

Each case commits fixtures/base.spec.md in a throwaway git repository, replaces it with a
variant, runs the lint, and checks the exit code and output.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT = HERE / "spec_lint.py"
FIXTURES = HERE / "fixtures"

CASES = [
    # (variant, expected exit, text that must appear, text that must not appear)
    ("base.spec.md", 0, ["PASS", "no agreed requirement changed"], ["NEEDS OWNER", "FAIL"]),
    ("agreed-sentence-changed.spec.md", 0,
     ["NEEDS OWNER: YARD-SIGHT-01", "sentence changed", "PASS"], ["FAIL"]),
    ("draft-changed.spec.md", 0, ["PASS", "no agreed requirement changed"], ["NEEDS OWNER", "FAIL"]),
    ("bad-format.spec.md", 1,
     ["duplicate ID", "state \"approved\"", "rung \"vibes\"", "agreed requirement has no check"], []),
]


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=Test Owner", "-c", "user.email=owner@example.invalid",
                    *args], cwd=repo, check=True, capture_output=True)


def run_case(variant: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp)
        (repo / "spec").mkdir()
        target = repo / "spec" / "yard.spec.md"
        shutil.copyfile(FIXTURES / "base.spec.md", target)
        git(repo, "init", "-q")
        git(repo, "add", ".")
        git(repo, "commit", "-q", "-m", "Base spec")
        shutil.copyfile(FIXTURES / variant, target)
        result = subprocess.run([sys.executable, str(LINT)], cwd=repo, capture_output=True,
                                text=True, encoding="utf-8", errors="replace")
        return result.returncode, result.stdout + result.stderr


def main() -> int:
    failures = 0
    for variant, code, present, absent in CASES:
        got_code, output = run_case(variant)
        missing = [t for t in present if t not in output]
        unwanted = [t for t in absent if t in output]
        ok = got_code == code and not missing and not unwanted
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {variant}: exit {got_code}")
        if not ok:
            print(f"      expected exit {code}; missing {missing}; unexpected {unwanted}")
            print("      " + output.replace("\n", "\n      "))
    print(f"{'PASS' if not failures else 'FAIL'} — {len(CASES) - failures} of {len(CASES)} cases.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
