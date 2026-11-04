#!/usr/bin/env python3
"""Rung-0 lint for a project's spec files. Example only: each project owns its own copy.

    python tools/spec_lint.py [SPEC ...] [--base REF] [--sources PATH ...] [--owner-exit N]

With no SPEC arguments it checks spec/*.spec.md under the current folder. --sources names
the folders (or files) that hold the project's tests and check scripts; give it once per
path.

Exit code: 0 pass, 1 a format problem. With --owner-exit N, a run with no format problem
exits N when a change needs the owner or the owner gate was skipped, so a suite that judges
the lint by its exit code can tell those apart from a pass. Print the output whatever the
exit code: NEEDS OWNER, NOT FOUND and NO ID lines don't fail the run.

Format checks fail the run (exit code 1):
  - every "###" heading under "## Requirements" is shaped "### <ID> — <sentence>", since
    one that isn't would drop out of every other check;
  - every requirement ID is unique and shaped AREA-TOPIC-NN;
  - an ID retired at the git base is not reused;
  - state is draft, agreed, or retired, and rung is static, engine, editor, session,
    or owner;
  - every agreed requirement names a check;
  - an owner-rung check is a card, written "card <CARD-ID>"; and
  - every card a check names is defined under "## Cards" in the same spec.

Check lookup (reported, never blocks): each agreed requirement's machine check must exist
in the --sources. The check's first word is its name, such as a test name or a script
name. A source file has that name when its file name, without the extension, matches it
(case, "-" and "_" don't matter) or its text contains the name as a whole word. The lint
prints "NOT FOUND: <ID>" for a name no source has. It doesn't block, because a check is
written after the owner agrees its requirement. Without --sources it skips the lookup and
says so.

ID check (reported, never blocks): a machine check, one that isn't a card, must name its
requirement's ID, with "-" or "_", such as OUT_SPAWN_01_... or lint-layout OUT-DATA-01, so
its result can be traced to it. The lint prints "NO ID: <ID>" for one that doesn't.

Owner gate (reported, never blocks): each spec file is compared with the same file at a
git base (default HEAD). A spec file the base doesn't have is compared as empty. It prints
"NEEDS OWNER: <ID>" when:
  - an agreed requirement's sentence, rung, or check changed;
  - an agreed requirement was removed or left the agreed state;
  - a requirement is agreed now but was not agreed at the base;
  - a requirement is retired now but was not retired at the base; or
  - a retired requirement was removed.
Only the owner agrees, changes, or retires a requirement. Pass --base the last commit the
owner has seen, such as the commit the task started from, or in CI the point the branch
left the main branch: once a change is committed, HEAD holds it and the gate reports
nothing. When there's no base to compare with, the summary says the gate was skipped.

It writes its output as UTF-8 on any console or pipe, so read it as UTF-8. On Windows,
Python would otherwise give a pipe the ANSI code page, such as cp1252, and a character
outside it would come out as "?" or as a byte a UTF-8 reader can't read.

Dependency-free; Python 3.10 or newer. The owner gate and the retired-ID check need git on
PATH.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

STATES = ("draft", "agreed", "retired")
RUNGS = ("static", "engine", "editor", "session", "owner")
ID_SHAPE = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*)+-[0-9]{2,}$")
HEADING = re.compile(r"^###\s+([A-Za-z0-9][A-Za-z0-9_-]*)\s+(?:—|–|--?)\s+(.+?)\s*$")
REQUIREMENT_LEVEL = re.compile(r"^###(?!#)")
CARD_HEADING = re.compile(r"^###\s+([A-Za-z0-9][A-Za-z0-9_-]*)(?:\s|$)")
SECTION = re.compile(r"^##\s+(.+?)\s*$")
FIELD = re.compile(r"^-\s+([a-z-]+):\s*(.*?)\s*$")
CARD_CHECK = re.compile(r"^card\s+(\S+)", re.IGNORECASE)
SKIP_DIRS = {".git", "bin", "obj", "node_modules", "__pycache__"}
MAX_SOURCE_BYTES = 2_000_000


def parse(text: str) -> tuple[list[dict], set[str], list[int]]:
    """Requirements under '## Requirements', with line numbers and fields, the card IDs
    under '## Cards', and the lines of '###' headings under '## Requirements' that aren't
    shaped as a requirement, which would otherwise drop out of every check unseen."""
    requirements: list[dict] = []
    cards: set[str] = set()
    unread: list[int] = []
    section = ""
    current: dict | None = None
    for number, line in enumerate(text.splitlines(), start=1):
        section_match = SECTION.match(line)
        if section_match and not line.startswith("###"):
            section = section_match.group(1).strip().lower()
            current = None
            continue
        if section == "cards":
            card = CARD_HEADING.match(line)
            if card:
                cards.add(card.group(1))
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
            if REQUIREMENT_LEVEL.match(line):
                unread.append(number)
            current = None
            continue
        field = FIELD.match(line)
        if current is not None and field and field.group(1) not in current["fields"]:
            current["fields"][field.group(1)] = field.group(2)
    return requirements, cards, unread


def format_problems(path: str, requirements: list[dict], cards: set[str],
                    seen: dict[str, str]) -> list[str]:
    problems = []
    for req in requirements:
        where = f"{path}:{req['line']}: {req['id']}"
        if req["id"] in seen:
            problems.append(f"{where}: duplicate ID (first in {seen[req['id']]})")
        else:
            seen[req["id"]] = f"{path}:{req['line']}"
        if not ID_SHAPE.match(req["id"]):
            problems.append(f"{where}: ID is not shaped AREA-TOPIC-NN")
        state = req["fields"].get("state")
        rung = req["fields"].get("rung")
        check = req["fields"].get("check", "")
        if state is None:
            problems.append(f"{where}: missing state")
        elif state not in STATES:
            problems.append(f"{where}: state \"{state}\" is not one of {', '.join(STATES)}")
        if rung is None:
            problems.append(f"{where}: missing rung")
        elif rung not in RUNGS:
            problems.append(f"{where}: rung \"{rung}\" is not one of {', '.join(RUNGS)}")
        if state == "agreed" and not check:
            problems.append(f"{where}: agreed requirement has no check")
        if not check:
            continue
        card = CARD_CHECK.match(check)
        if rung == "owner" and not card:
            problems.append(f"{where}: owner-rung check \"{check}\" is not a card")
        if card and card.group(1) not in cards:
            problems.append(f"{where}: card {card.group(1)} is not defined under \"## Cards\"")
    return problems


def retired_reused(path: str, now: list[dict], before: list[dict], base: str) -> list[str]:
    retired = {r["id"] for r in before if r["fields"].get("state") == "retired"}
    return [f"{path}:{r['line']}: {r['id']}: was retired at {base}; a retired ID is never reused"
            for r in now if r["id"] in retired and r["fields"].get("state") != "retired"]


def source_files(roots: list[Path]) -> list[Path]:
    own = Path(__file__).resolve()
    files: list[Path] = []
    for root in roots:
        candidates = [root] if root.is_file() else sorted(root.rglob("*"))
        for path in candidates:
            if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
                continue
            if path.resolve() != own and path.stat().st_size <= MAX_SOURCE_BYTES:
                files.append(path)
    return files


def stem_key(name: str) -> str:
    return name.lower().replace("_", "-")


def missing_checks(requirements: list[dict], files: list[Path], texts: dict[Path, str]) -> list[str]:
    stems = {stem_key(path.name.split(".")[0]) for path in files}
    findings = []
    for req in requirements:
        check = req["fields"].get("check", "")
        if req["fields"].get("state") != "agreed" or not check or CARD_CHECK.match(check):
            continue
        name = check.split()[0]
        if stem_key(name) in stems:
            continue
        word = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(name)}(?![A-Za-z0-9_-])")
        if not any(word.search(read_text(path, texts)) for path in files):
            findings.append(f"NOT FOUND: {req['id']} - no source has a check named \"{name}\"")
    return findings


def read_text(path: Path, texts: dict[Path, str]) -> str:
    """The file's text, read once per run."""
    if path not in texts:
        try:
            texts[path] = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            texts[path] = ""
    return texts[path]


def base_text(path: Path, base: str) -> tuple[str | None, str | None]:
    """The file's content at the git base, "" when the base predates the file, or
    (None, reason) when there is no base to compare with."""
    try:
        # Decoded as Python decodes file names, since a text run would read Git's UTF-8 in
        # the ANSI code page on Windows and miss the repository under a non-ASCII folder.
        top = os.fsdecode(subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path.parent,
                                         capture_output=True, check=True).stdout).strip()
        rel = path.resolve().relative_to(Path(top).resolve()).as_posix()
        known = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"],
                               cwd=top, capture_output=True)
        shown = subprocess.run(["git", "show", f"{base}:{rel}"], cwd=top,
                               capture_output=True, text=True, encoding="utf-8")
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        return None, f"not in a git repository ({error.__class__.__name__})"
    if known.returncode != 0:
        return None, f"{base} is not a commit in this repository"
    if shown.returncode != 0:
        return "", None  # a spec new since the base: every agreed requirement in it is new
    return shown.stdout, None


def owner_gate(now: list[dict], before: list[dict]) -> list[str]:
    findings = []
    old = {r["id"]: r for r in before}
    new = {r["id"]: r for r in now}
    for rid, was in old.items():
        if was["fields"].get("state") == "retired" and rid not in new:
            findings.append(f"NEEDS OWNER: {rid} - retired requirement was removed, so nothing "
                            "keeps its ID from being reused")
        if was["fields"].get("state") != "agreed":
            continue
        if rid not in new:
            findings.append(f"NEEDS OWNER: {rid} - agreed requirement was removed")
            continue
        cur = new[rid]
        if cur["fields"].get("state") != "agreed":
            findings.append(f"NEEDS OWNER: {rid} - state changed from agreed to "
                            f"\"{cur['fields'].get('state')}\"")
        if cur["sentence"] != was["sentence"]:
            findings.append(f"NEEDS OWNER: {rid} - sentence changed: \"{was['sentence']}\" "
                            f"-> \"{cur['sentence']}\"")
        for key in ("rung", "check"):
            if cur["fields"].get(key) != was["fields"].get(key):
                findings.append(f"NEEDS OWNER: {rid} - {key} changed: "
                                f"\"{was['fields'].get(key)}\" -> \"{cur['fields'].get(key)}\"")
    for rid, cur in new.items():
        state, was = cur["fields"].get("state"), old.get(rid, {}).get("fields", {}).get("state")
        if state == "agreed" and was != "agreed":
            findings.append(f"NEEDS OWNER: {rid} - marked agreed, but it was not agreed at the base")
        # Only the owner retires a requirement. One retired from agreed is reported above.
        if state == "retired" and was not in ("retired", "agreed"):
            findings.append(f"NEEDS OWNER: {rid} - marked retired, but it was not retired at the base")
    return findings


def missing_ids(requirements: list[dict]) -> list[str]:
    """Machine checks that don't name their requirement, so a result can't be traced to it."""
    findings = []
    for req in requirements:
        check = req["fields"].get("check", "")
        if not check or CARD_CHECK.match(check):
            continue
        rid = req["id"].lower()
        if rid not in check.lower() and rid.replace("-", "_") not in check.lower():
            findings.append(f"NO ID: {req['id']} - check \"{check}\" doesn't name the requirement")
    return findings


def main(argv: list[str]) -> int:
    for stream in (sys.stdout, sys.stderr):  # UTF-8 on any pipe; see the docstring
        stream.reconfigure(encoding="utf-8", errors="replace")
    base = "HEAD"
    owner_exit = 0
    paths: list[str] = []
    roots: list[Path] = []
    args = iter(argv)
    for arg in args:
        if arg == "--base":
            base = next(args, "HEAD")
        elif arg == "--sources":
            roots.append(Path(next(args, ".")))
        elif arg == "--owner-exit":
            code = next(args, "")
            if not code.isdigit() or int(code) in (0, 1):
                print("FAIL  --owner-exit needs an exit code other than 0 and 1, such as 3")
                return 1
            owner_exit = int(code)
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
    texts: dict[Path, str] = {}
    sources = source_files([r for r in roots if r.exists()])
    problems += [f"{r}: source path not found" for r in roots if not r.exists()]
    if not roots:
        notes.append("note  check names not looked up: pass --sources for the test and script folders")
    total = 0
    skipped = 0
    for path in files:
        if not path.is_file():
            problems.append(f"{path}: file not found")
            continue
        shown_path = path.as_posix()
        now, cards, unread = parse(path.read_text(encoding="utf-8"))
        total += len(now)
        problems += [f"{shown_path}:{n}: heading is not shaped \"### <ID> — <sentence>\", so no "
                     "check reads it as a requirement" for n in unread]
        problems += format_problems(shown_path, now, cards, seen)
        if roots:
            findings += missing_checks(now, sources, texts)
        findings += missing_ids(now)
        before_text, reason = base_text(path, base)
        if before_text is None:
            skipped += 1
            notes.append(f"note  owner gate and retired-ID check skipped for {shown_path}: {reason}")
        else:
            before, _, _ = parse(before_text)
            problems += retired_reused(shown_path, now, before, base)
            findings += owner_gate(now, before)

    for line in notes + [f"FAIL  {p}" for p in problems] + findings:
        print(line)
    owner = [f for f in findings if f.startswith("NEEDS OWNER")]
    parts = []
    if skipped:  # never "no agreed requirement changed" for a spec nothing compared
        parts.append(f"owner gate skipped for {skipped} spec file(s)")
    if owner:
        parts.append(f"{len(owner)} change(s) need the owner (reported, not blocking)")
    elif skipped < len(files):
        parts.append(f"no agreed requirement changed since {base}" + (" in the others" if skipped else ""))
    for mark, what in (("NOT FOUND", "check(s) not found"), ("NO ID", "check(s) don't name their requirement")):
        count = sum(f.startswith(mark) for f in findings)
        if count:
            parts.append(f"{count} {what} (reported, not blocking)")
    summary = "; ".join(parts)
    if problems:
        print(f"FAIL - {len(problems)} format problem(s) in {total} requirements; {summary}.")
        return 1
    print(f"PASS - {total} requirements well formed; {summary}.")
    return owner_exit if owner_exit and (owner or skipped) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
