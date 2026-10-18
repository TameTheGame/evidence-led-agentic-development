#!/usr/bin/env python3
"""Claude Code PreToolUse hook: run tools/check.py before a `git push`, and deny the push if
it fails. Wired in .claude/settings.json for the Bash and PowerShell tools.

It always exits 0 and denies through JSON on stdout, so the settings command can try
`py -3` (Windows) and fall back to `python3` (Linux, macOS) with `||`: a blocking exit
code would make that fallback run the hook a second time.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHECK = ROOT / "tools" / "check.py"

# `git push`, also after global options such as `git -C <dir> push` or `git -c k=v push`.
PUSH = re.compile(r"(?:^|[\s;&|(`'\"])git(?:\.exe)?(?:\s+(?:-[Cc]\s+\S+|--\S+|-\S+))*\s+push(?=$|[\s;&|)`'\"])")


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    command = (event.get("tool_input") or {}).get("command") or ""
    if not PUSH.search(command):
        return 0
    result = subprocess.run([sys.executable, str(CHECK)], cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace",
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if result.returncode == 0:
        return 0
    report = (result.stdout + result.stderr).strip()
    lines = report.splitlines()
    if len(lines) > 40:
        report = "\n".join(lines[:40] + [f"... and {len(lines) - 40} more lines"])
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Push blocked: tools/check.py failed. Fix the problems, "
                                    "commit, and push again. A private word must be removed from "
                                    "the file or reworded out of the commit message. A commit "
                                    "that credits an AI tool needs the right author and message "
                                    "before it is pushed; rewriting one that is already pushed "
                                    "needs the owner's yes.\n" + report,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
