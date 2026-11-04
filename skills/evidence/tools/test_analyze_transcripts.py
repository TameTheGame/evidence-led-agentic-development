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


def command(n: int, text: str, output: str, tool: str = "Bash") -> list[dict]:
    return [{"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": f"c{n}", "name": tool, "input": {"command": text}}]}},
            {"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"c{n}", "content": output}]}}]


def transcript(failed_lint: bool = False, edit: str = "", commands: list[list[dict]] = (),
               final: str = "done") -> list[dict]:
    events: list[dict] = [{"type": "system", "subtype": "init", "model": "test-model",
                           "skills": ["choosing-rigor"]}]
    for c in commands:
        events += c
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
    return events + [{"type": "result", "result": final, "num_turns": 3}]


# Reading the scripts is not running them; each of these starts one.
READS = [command(1, "cat tools/run_engine_tests.ps1", "param("),
         command(2, "Get-Content tools\\spec_lint.py", "import re", "PowerShell")]
RUNS = [command(1, "cd /c/work && powershell -NoProfile -File tools/run_engine_tests.ps1", "Tests: 3 passed"),
        command(2, "& .\\tools\\run_engine_tests.ps1 -Filter Name~OUT", "Tests: 2 passed", "PowerShell"),
        command(3, "py -3 tools\\spec_lint.py --sources UnitTests", "PASS - 4 requirements", "PowerShell")]
RUN = "SF-2"  # a run id whose prefix is its condition, so it must not reach the extract's text


def json_reads_back(out: str) -> bool:
    try:
        runs = json.loads(out)
    except ValueError:
        return False
    return runs[0]["lint_runs"][0]["status"] == "exit≠0" and runs[0]["lint_runs"][0]["output"] == LINT_LINE


CASES = [
    # (name, transcript, arguments, exit code, text that must appear, text that must not).
    # {tmp} in an argument or a final reply is the case's folder; a transcript of None writes
    # none; "--extracts" appends the run's extract to the output.
    ("a run with no lint and no edit", transcript(), [], 0,
     ["== run  model=test-model  turns=3", "spec_lint: none", "edits: none"], ["Traceback"]),
    ("a failed lint run prints its mark and its last line", transcript(failed_lint=True), [], 0,
     [f"spec_lint: step 1 exit≠0: {LINT_LINE}"], ["Traceback", "�"]),
    ("an edited file's name comes back as itself", transcript(edit=ODD_EDIT), [], 0,
     [f"edits: {ODD_EDIT}"], ["Traceback", "�", "spec/yard_?"]),
    ("--json reads back with the same text", transcript(failed_lint=True), ["--json"], 0,
     ["\"lint_runs\""], ["Traceback"]),
    ("reading a script is not a run", transcript(commands=READS), [], 0,
     ["spec_lint: none", "engine runs: none"], ["Traceback"]),
    ("each way of starting a script is a run", transcript(commands=RUNS), [], 0,
     ["engine runs: step 1 ok: Tests: 3 passed; step 2 ok: Tests: 2 passed",
      "spec_lint: step 3 ok: PASS - 4 requirements"], ["Traceback"]),
    ("a transcript cut off mid-line is read up to the cut", transcript() + ["{\"type\": \"assi"], [], 0,
     ["== run  model=test-model", "NOT JSON, skipped: transcript line(s) 3"], ["Traceback"]),
    ("a folder with no transcripts is an error", None, [], 2, ["no <run>.jsonl transcripts"], ["Traceback"]),
    ("a diff git can't give says why, and the final reply loses the run's folder",
     transcript(final=f"Edited {{tmp}}/runs/{RUN}/spec/outpost.spec.md."),
     ["--runs", "{tmp}/runs", "--extracts", "{tmp}/extracts"], 0,
     ["(diff unavailable: git rev-list failed", "Edited ./spec/outpost.spec.md."],
     ["Traceback", f"runs/{RUN}", "\nNone.\n"]),
]


def run_case(events: list | None, args: list[str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp).resolve()
        folder = root / "transcripts"
        folder.mkdir()
        (root / "runs" / RUN).mkdir(parents=True)  # a run folder that isn't a git repository
        name = RUN if "--runs" in args else "run"
        if events is not None:
            lines = "\n".join(e if isinstance(e, str) else json.dumps(e) for e in events) + "\n"
            (folder / f"{name}.jsonl").write_text(lines.replace("{tmp}", root.as_posix()), encoding="utf-8")
        args = [a.replace("{tmp}", str(root)) for a in args]
        done = subprocess.run([sys.executable, str(TOOL), "--transcripts", str(folder), *args],
                              capture_output=True, env={**os.environ, **PIPE})
        out = (done.stdout + done.stderr).decode("utf-8", errors="replace")
        extract = root / "extracts" / f"{name}.md"
        if "--extracts" in args and extract.exists():
            out += "\n" + extract.read_text(encoding="utf-8").split("\n", 1)[1]  # past "# Run <id>"
        return done.returncode, out


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
