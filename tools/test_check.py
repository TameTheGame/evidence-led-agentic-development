#!/usr/bin/env python3
"""Checks check.py's private-word check and both push hooks. Dependency-free; needs git on PATH.

    python tools/test_check.py

Each case copies check.py and the hooks into a throwaway git repository, lists made-up
private words, plants them (or not), and checks the exit code and output.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "tools" / "check.py"
HOOK = ROOT / ".claude" / "hooks" / "check_before_push.py"
GIT_HOOK = ROOT / ".githooks" / "pre-push"

# Made-up words only. Never put a real private word in this file.
WORDS = "zorblat\nGlass-Heron Cove   # a three-word phrase\n"
CLEAN = "# Notes\n\nThe zorblatty heron flew past the cove.\n"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-c", "user.name=Test Owner", "-c", "user.email=owner@example.invalid",
                    *args], cwd=repo, check=True, capture_output=True)


def run(args: list[str], cwd: Path, stdin: str = "") -> tuple[int, str]:
    result = subprocess.run([sys.executable, *args], cwd=cwd, input=stdin, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    return result.returncode, result.stdout + result.stderr


def make_repo(tmp: Path, files: dict[str, str], message: str = "Add notes",
              fingerprints: bool = True) -> Path:
    repo = tmp / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / ".claude" / "hooks").mkdir(parents=True)
    (repo / ".githooks").mkdir()
    shutil.copy2(GIT_HOOK, repo / ".githooks" / "pre-push")
    shutil.copyfile(CHECK, repo / "tools" / "check.py")
    shutil.copyfile(HOOK, repo / ".claude" / "hooks" / "check_before_push.py")
    if fingerprints:
        words = tmp / "words.txt"
        words.write_text(WORDS, encoding="utf-8")
        code, output = run([str(repo / "tools" / "check.py"), "--hash-words", str(words)], repo)
        assert code == 0, output
        (repo / "tools" / "private-words.sha256").write_text(output, encoding="utf-8")
    for name, text in files.items():
        (repo / name).write_text(text, encoding="utf-8")
    git(repo, "init", "-q")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", message)
    return repo


def check_case(files: dict[str, str], message: str = "Add notes", fingerprints: bool = True,
               untracked: dict[str, str] | None = None) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(Path(tmp), files, message, fingerprints)
        for name, text in (untracked or {}).items():
            (repo / name).write_text(text, encoding="utf-8")
        return run([str(repo / "tools" / "check.py")], repo)


def hook_case(files: dict[str, str], command: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(Path(tmp), files)
        event = json.dumps({"hook_event_name": "PreToolUse", "tool_name": "Bash",
                            "tool_input": {"command": command}})
        return run([str(repo / ".claude" / "hooks" / "check_before_push.py")], repo, event)


def git_push_case(files: dict[str, str], message: str = "Add notes") -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        repo = make_repo(Path(tmp), files, message)
        remote = Path(tmp) / "remote.git"
        git(repo, "init", "-q", "--bare", str(remote))
        git(repo, "config", "core.hooksPath", ".githooks")
        result = subprocess.run(["git", "push", str(remote), "HEAD:refs/heads/probe"], cwd=repo,
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
        pushed = subprocess.run(["git", "--git-dir", str(remote), "for-each-ref"],
                                capture_output=True, text=True).stdout
        return result.returncode, result.stdout + result.stderr + ("pushed" if pushed.strip() else "not pushed")


PLANTED = {"notes.md": "# Notes\n\nWe met at GLASS heron-cove.\n"}

CASES = [
    # (name, run, expected exit, text that must appear, text that must not appear)
    ("clean repository passes", lambda: check_case({"notes.md": CLEAN}),
     0, ["PASS", "no private words in"], ["FAIL"]),
    ("planted line fails", lambda: check_case(PLANTED),
     1, ["FAIL  notes.md:3: contains a private word"], ["PASS"]),
    ("phrase across a line break fails", lambda: check_case({"notes.md": "Glass heron\ncove\n"}),
     1, ["FAIL  notes.md:1: contains a private word"], ["PASS"]),
    ("planted file name fails", lambda: check_case({"zorblat-plan.md": CLEAN}),
     1, ["FAIL  zorblat-plan.md: file name contains a private word"], ["PASS"]),
    ("planted commit message fails", lambda: check_case({"notes.md": CLEAN}, "Tidy the ZORBLAT notes"),
     1, ["message line 1 contains a private word"], ["PASS"]),
    ("untracked file is ignored", lambda: check_case({"notes.md": CLEAN}, untracked={"zorblat.md": "zorblat"}),
     0, ["PASS"], ["FAIL"]),
    ("missing fingerprint file fails", lambda: check_case({"notes.md": CLEAN}, fingerprints=False),
     1, ["FAIL  tools/private-words.sha256: missing"], ["PASS"]),
    ("hook denies a push from a failing repository", lambda: hook_case(PLANTED, "git push -u origin main"),
     0, ['"permissionDecision": "deny"', "notes.md:3"], []),
    ("hook sees a push after global options", lambda: hook_case(PLANTED, "cd x && git -C . push origin HEAD"),
     0, ['"permissionDecision": "deny"'], []),
    ("hook allows a push from a clean repository", lambda: hook_case({"notes.md": CLEAN}, "git push"),
     0, [], ["deny"]),
    ("hook ignores other commands", lambda: hook_case(PLANTED, 'git commit -m "push it" && git log'),
     0, [], ["deny"]),
    ("git hook stops a push from a failing repository", lambda: git_push_case({"notes.md": CLEAN}, "Tidy the ZORBLAT notes"),
     1, ["message line 1 contains a private word", "not pushed"], []),
    ("git hook lets a clean push through", lambda: git_push_case({"notes.md": CLEAN}),
     0, ["PASS", "pushed"], ["FAIL", "not pushed"]),
]


def main() -> int:
    failures = 0
    for name, case, code, present, absent in CASES:
        got_code, output = case()
        missing = [t for t in present if t not in output]
        unwanted = [t for t in absent if t in output]
        ok = got_code == code and not missing and not unwanted
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if not ok:
            print(f"      exit {got_code} (expected {code}); missing {missing}; unwanted {unwanted}")
            print("      " + output.replace("\n", "\n      "))
    print(f"{'FAIL' if failures else 'PASS'} — {len(CASES) - failures} of {len(CASES)} cases passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
