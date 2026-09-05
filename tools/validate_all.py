#!/usr/bin/env python3
"""Run every dependency-free ELAD Level-0 validator with this interpreter."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATORS = (
    "validate_blueprint.py",
    "validate_context_authority_v05.py",
    "validate_protocol_security_v05.py",
    "validate_adoption_v05.py",
    "validate_task_rigor_v05.py",
    "validate_release_bundle_v05.py",
    "validate_release.py",
)


def main() -> int:
    if sys.version_info < (3, 10):
        print("FAIL - Python 3.10 or newer is required.", file=sys.stderr)
        return 3

    for name in VALIDATORS:
        validator = ROOT / "tools" / name
        if not validator.is_file():
            print(f"FAIL - validator not found: {validator}", file=sys.stderr)
            return 2
        completed = subprocess.run([sys.executable, str(validator)], cwd=ROOT, check=False)
        if completed.returncode != 0:
            return completed.returncode

    print("PASS - all ELAD Level-0 validation slices passed; no authority granted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
