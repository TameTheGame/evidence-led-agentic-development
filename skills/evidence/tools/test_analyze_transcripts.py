#!/usr/bin/env python3
"""Checks analyze_transcripts.py's summary on a Windows pipe. Dependency-free.

    python skills/evidence/tools/test_analyze_transcripts.py

Each case writes one made-up transcript to a temporary folder, runs the tool with a cp1252
stdout, as Windows pipes it, reads its output as UTF-8, and checks the exit code and
output. The transcripts hold characters outside cp1252: the "≠" the tool marks a failed run
with, a lint line that quotes "·", "≥" and "→", and an edited file's name. It writes its
own output as UTF-8, since a failing case prints the tool's.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "analyze_transcripts.py"
PIPE = {"PYTHONIOENCODING": "cp1252"}
LINT_LINE = "FAIL  spec/yard.spec.md: YARD-01 sentence · ≥ 2 m → has no check"
ODD_EDIT = "spec/yard_Ω.spec.md"


def transcript(failed_lint: bool = False, edit: str = "") -> list[dict]:
    events: list[dict] = [{"type": "system", "subtype": "init", "model": "test-model",
                           "skills": ["choosing-rigor"]}]
    if failed_lint:
        events += [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t1", "name": "Bash",
                 "input": {"command": "python tools/spec_lint.py"}}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t1", "is_error": True,
                 "content": f"{LINT_LINE}\n"}]}},
        ]
    if edit:
        events += [
            {"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": "t2", "name": "Edit", "input": {"file_path": edit}}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": "t2", "content": "edited"}]}},
        ]
    return events + [{"type": "result", "result": "done", "num_turns": 3}]


def json_reads_back(out: str) -> bool:
    try:
        runs = json.loads(out)
    except ValueError:
        return False
    return runs[0]["lint_runs"][0]["status"] == "exit≠0" and runs[0]["lint_runs"][0]["output"] == LINT_LINE


CASES = [
    # (name, transcript, arguments, exit code, text that must appear, text that must not)
    ("a run with no lint and no edit", transcript(), [], 0,
     ["== run  model=test-model  turns=3", "spec_lint: none", "edits: none"], ["Traceback"]),
    ("a failed lint run prints its mark and its last line", transcript(failed_lint=True), [], 0,
     [f"spec_lint: step 1 exit≠0: {LINT_LINE}"], ["Traceback", "\ufffd"]),
    ("an edited file's name comes back as itself", transcript(edit=ODD_EDIT), [], 0,
     [f"edits: {ODD_EDIT}"], ["Traceback", "\ufffd", "spec/yard_?"]),
    ("--json reads back with the same text", transcript(failed_lint=True), ["--json"], 0,
     ["\"lint_runs\""], ["Traceback"]),
]


def run_case(events: list[dict], args: list[str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        folder = Path(tmp) / "transcripts"
        folder.mkdir()
        lines = "\n".join(json.dumps(e) for e in events) + "\n"
        (folder / "run.jsonl").write_text(lines, encoding="utf-8")
        done = subprocess.run([sys.executable, str(TOOL), "--transcripts", str(folder), *args],
                              capture_output=True, env={**os.environ, **PIPE})
        return done.returncode, (done.stdout + done.stderr).decode("utf-8", errors="replace")


def main() -> int:
    for stream in (sys.stdout, sys.stderr):  # a failing case prints the tool's output
        stream.reconfigure(encoding="utf-8", errors="replace")
    failures = 0
    for name, events, args, want_code, must, must_not in CASES:
        code, out = run_case(events, args)
        problems = []
        if code != want_code:
            problems.append(f"exit {code}, expected {want_code}")
        problems += [f"missing {t!r}" for t in must if t not in out]
        problems += [f"unexpected {t!r}" for t in must_not if t in out]
        if "--json" in args and not json_reads_back(out):
            problems.append("the JSON doesn't read back with the lint's status and line")
        if problems:
            failures += 1
            print(f"FAIL  {name}: {'; '.join(problems)}\n{out}")
        else:
            print(f"PASS  {name}")
    print(f"{'FAIL' if failures else 'PASS'} - {len(CASES) - failures} of {len(CASES)} cases passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
