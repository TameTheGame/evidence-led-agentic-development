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
    # and options, if any: "folder" the repository sits in, "new" when the base commit lacks the
    # spec, "no_git" when the project isn't a repository)
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
     ["owner gate and retired-ID check skipped", "FAIL"], {"folder": "Übung ü"}),
    # With --owner-exit, a change that needs the owner has its own exit code.
    ("agreed-sentence-changed.spec.md", SOURCES + ["--owner-exit", "3"], 3,
     ["NEEDS OWNER: YARD-SIGHT-01", "PASS"], ["FAIL"]),
    ("base.spec.md", SOURCES + ["--owner-exit", "3"], 0, ["PASS"], ["NEEDS OWNER"]),
    # Only the owner retires a requirement, and a retired one stays to keep its ID taken.
    ("draft-retired.spec.md", SOURCES, 0,
     ["NEEDS OWNER: YARD-FEEL-01 - marked retired", "NEEDS OWNER: YARD-GATE-01 - retired requirement was removed",
      "2 change(s) need the owner"], ["FAIL", "no agreed requirement changed"]),
    ("check-without-id.spec.md", SOURCES, 0,
     ["NO ID: YARD-PATH-01", "1 check(s) don't name their requirement", "PASS"],
     ["FAIL", "NEEDS OWNER", "NO ID: YARD-DATA-01", "NO ID: YARD-SIGHT-01"]),
    # A spec the base lacks is compared as empty, so its agreed requirements are new.
    ("base.spec.md", SOURCES, 0,
     ["NEEDS OWNER: YARD-DATA-01 - marked agreed", "NEEDS OWNER: YARD-SIGHT-01 - marked agreed"],
     ["skipped", "no agreed requirement changed", "FAIL"], {"new": True}),
    # With nothing to compare against, the summary says so instead of "no agreed requirement
    # changed".
    ("agreed-sentence-changed.spec.md", SOURCES, 0,
     ["owner gate skipped for 1 spec file(s)", "PASS"], ["no agreed requirement changed"], {"no_git": True}),
    ("agreed-sentence-changed.spec.md", SOURCES + ["--base", "no-such-ref"], 0,
     ["no-such-ref is not a commit", "owner gate skipped for 1 spec file(s)"],
     ["no agreed requirement changed"]),
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


def run_case(variant: str, extra: list[str], options: dict) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / options.get("folder", "")
        shutil.copytree(FIXTURES / "sources", repo, dirs_exist_ok=True)
        (repo / "spec").mkdir()
        target = repo / "spec" / "yard.spec.md"
        if not options.get("new"):
            shutil.copyfile(FIXTURES / "base.spec.md", target)
        if not options.get("no_git"):
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
    for variant, extra, code, present, absent, *rest in CASES:
        options = rest[0] if rest else {}
        got_code, output = run_case(variant, extra, options)
        missing = [t for t in present if t not in output]
        unwanted = [t for t in absent if t in output]
        ok = got_code == code and not missing and not unwanted
        failures += not ok
        shown = f"{variant} {' '.join(extra)}".strip() + "".join(
            f" in {v}" if k == "folder" else f" ({k})" for k, v in options.items())
        print(f"{'PASS' if ok else 'FAIL'}  {shown}: exit {got_code}")
        if not ok:
            print(f"      expected exit {code}; missing {missing}; unexpected {unwanted}")
            print("      " + output.replace("\n", "\n      "))
    print(f"{'PASS' if not failures else 'FAIL'} - {len(CASES) - failures} of {len(CASES)} cases.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
