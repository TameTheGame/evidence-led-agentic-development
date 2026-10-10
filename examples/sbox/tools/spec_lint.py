#!/usr/bin/env python3
"""Rung-0 lint for a project's spec files. Example only: each project owns its own copy.

    python tools/spec_lint.py [SPEC ...] [--base REF]

With no SPEC arguments it checks spec/*.spec.md under the current folder.

Format checks fail the run (exit code 1):
  - every requirement ID is unique;
  - state is draft, agreed, or retired, and rung is static, engine, editor, session,
    or owner; and
  - every agreed requirement names a check.

Owner gate (reported, never blocks): each spec file is compared with the same file at a
git base (default HEAD). It prints "NEEDS OWNER: <ID>" when:
  - an agreed requirement's sentence, rung, or check changed;
  - an agreed requirement was removed or left the agreed state; or
  - a requirement is agreed now but was not agreed at the base.
Only the owner agrees, changes, or retires a requirement.

Dependency-free; Python 3.10 or newer. The owner gate needs git on PATH.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

STATES = ("draft", "agreed", "retired")
RUNGS = ("static", "engine", "editor", "session", "owner")
HEADING = re.compile(r"^###\s+([A-Za-z0-9][A-Za-z0-9_-]*)\s+(?:—|–|--?)\s+(.+?)\s*$")
SECTION = re.compile(r"^##\s+(.+?)\s*$")
FIELD = re.compile(r"^-\s+([a-z-]+):\s*(.*?)\s*$")


def parse(text: str) -> list[dict]:
    """Requirements under '## Requirements', with their line numbers and fields."""
    requirements: list[dict] = []
    section = ""
    current: dict | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        section_match = SECTION.match(line)
        if section_match and not line.startswith("###"):
            section = section_match.group(1).strip().lower()
            current = None
            continue
        if section != "requirements":
            continue
        heading = HEADING.match(line)
        if heading:
            current = {"id": heading.group(1), "sentence": " ".join(heading.group(2).split()),
                       "line": number, "fields": {}}
            requirements.append(current)
            continue
        if line.startswith("#"):
            current = None
            continue
        field = FIELD.match(line)
        if current is not None and field and field.group(1) not in current["fields"]:
            current["fields"][field.group(1)] = field.group(2)
    return requirements


def format_problems(path: str, requirements: list[dict], seen: dict[str, str]) -> list[str]:
    problems = []
    for req in requirements:
        where = f"{path}:{req['line']}: {req['id']}"
        if req["id"] in seen:
            problems.append(f"{where}: duplicate ID (first in {seen[req['id']]})")
        else:
            seen[req["id"]] = f"{path}:{req['line']}"
        state = req["fields"].get("state")
        rung = req["fields"].get("rung")
        if state is None:
            problems.append(f"{where}: missing state")
        elif state not in STATES:
            problems.append(f"{where}: state \"{state}\" is not one of {', '.join(STATES)}")
        if rung is None:
            problems.append(f"{where}: missing rung")
        elif rung not in RUNGS:
            problems.append(f"{where}: rung \"{rung}\" is not one of {', '.join(RUNGS)}")
        if state == "agreed" and not req["fields"].get("check"):
            problems.append(f"{where}: agreed requirement has no check")
    return problems


def base_text(path: Path, base: str) -> tuple[str | None, str | None]:
    """The file's content at the git base, or (None, reason) when unavailable."""
    try:
        top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path.parent,
                             capture_output=True, text=True, check=True).stdout.strip()
        rel = path.resolve().relative_to(Path(top).resolve()).as_posix()
        shown = subprocess.run(["git", "show", f"{base}:{rel}"], cwd=top,
                               capture_output=True, text=True, encoding="utf-8")
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        return None, f"not in a git repository ({error.__class__.__name__})"
    if shown.returncode != 0:
        return None, f"not present at {base}"
    return shown.stdout, None


def owner_gate(now: list[dict], before: list[dict]) -> list[str]:
    findings = []
    old = {r["id"]: r for r in before}
    new = {r["id"]: r for r in now}
    for rid, was in old.items():
        if was["fields"].get("state") != "agreed":
            continue
        if rid not in new:
            findings.append(f"NEEDS OWNER: {rid} — agreed requirement was removed")
            continue
        cur = new[rid]
        if cur["fields"].get("state") != "agreed":
            findings.append(f"NEEDS OWNER: {rid} — state changed from agreed to "
                            f"\"{cur['fields'].get('state')}\"")
        if cur["sentence"] != was["sentence"]:
            findings.append(f"NEEDS OWNER: {rid} — sentence changed: \"{was['sentence']}\" "
                            f"-> \"{cur['sentence']}\"")
        for key in ("rung", "check"):
            if cur["fields"].get(key) != was["fields"].get(key):
                findings.append(f"NEEDS OWNER: {rid} — {key} changed: "
                                f"\"{was['fields'].get(key)}\" -> \"{cur['fields'].get(key)}\"")
    for rid, cur in new.items():
        if cur["fields"].get("state") == "agreed" and old.get(rid, {}).get("fields", {}).get("state") != "agreed":
            findings.append(f"NEEDS OWNER: {rid} — marked agreed, but it was not agreed at the base")
    return findings


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(errors="replace")  # never crash on a console that can't show a character
    base = "HEAD"
    paths: list[str] = []
    args = iter(argv)
    for arg in args:
        if arg == "--base":
            base = next(args, "HEAD")
        elif arg in ("-h", "--help"):
            print(__doc__)
            return 0
        else:
            paths.append(arg)
    files = [Path(p) for p in paths] or sorted(Path("spec").glob("*.spec.md"))
    if not files:
        print("FAIL  no spec files found (looked for spec/*.spec.md)")
        return 1

    problems: list[str] = []
    findings: list[str] = []
    notes: list[str] = []
    seen: dict[str, str] = {}
    total = 0
    for path in files:
        if not path.is_file():
            problems.append(f"{path}: file not found")
            continue
        shown_path = path.as_posix()
        now = parse(path.read_text(encoding="utf-8"))
        total += len(now)
        problems += format_problems(shown_path, now, seen)
        before_text, reason = base_text(path, base)
        if before_text is None:
            notes.append(f"note  owner gate skipped for {shown_path}: {reason}")
        else:
            findings += owner_gate(now, parse(before_text))

    for line in notes + [f"FAIL  {p}" for p in problems] + findings:
        print(line)
    gate = f"{len(findings)} change(s) need the owner (reported, not blocking)" if findings \
        else f"no agreed requirement changed since {base}"
    if problems:
        print(f"FAIL — {len(problems)} format problem(s) in {total} requirements; {gate}.")
        return 1
    print(f"PASS — {total} requirements well formed; {gate}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
