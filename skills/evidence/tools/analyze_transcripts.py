#!/usr/bin/env python3
"""Summarizes headless Claude Code transcripts from a skills test.

    python analyze_transcripts.py --transcripts DIR [--runs DIR] [--extracts DIR] [--json]

--transcripts  folder of <run>.jsonl files from `claude -p --output-format stream-json --verbose`
--runs         folder of <run>/ project folders; each may be a git repository whose first
               commit is the starting fixture, so the run's changes can be diffed
--extracts     write one Markdown extract per run (tool calls, final reply, spec changes),
               with personal and temporary paths replaced by placeholders
--json         print the per-run summary as JSON instead of text

Per run it records the skills listed at startup, Skill-tool invocations, direct reads of
SKILL.md files, spec_lint runs and their output, file edits, denied tool calls, and the
final reply. Dependency-free; Python 3.10 or newer; git is needed only for diffs.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

SKILLS = ("choosing-rigor", "matching-evidence-to-claims", "asking-the-owner")


def sanitize(text: str, run_root: Path | None) -> str:
    text = str(text).replace("\\", "/")
    if run_root is not None:
        root = run_root.resolve().as_posix()
        for form in {root, root.lower(), "/" + root[0].lower() + root[2:] if root[1:2] == ":" else root}:
            text = re.sub(re.escape(form) + "/?", "./", text, flags=re.IGNORECASE)
    # Windows and Git Bash forms of the same paths: C:/Users/<name>/... and /c/Users/<name>/...
    home = r"(?:[a-z]:|/[a-z])/users/[^/\s\"'`]+"
    text = re.sub(r"(?i)" + home + r"/appdata/local/temp/claude/[^/\s\"'`]+/[0-9a-f-]{36}/scratchpad",
                  "<session scratchpad>", text)
    text = re.sub(r"(?i)\$(?:env:)?temp/claude/[^/\s\"'`]+/[0-9a-f-]{36}/scratchpad", "<session scratchpad>", text)
    text = re.sub(r"(?i)" + home + r"/\.claude/projects/[^/\s\"'`]+", "<session memory dir>", text)
    text = re.sub(r"(?i)" + home, "<home>", text)
    text = re.sub(r"(?i)[a-z]--users-[^/\s\"'`]+", "<encoded dir>", text)  # folder names that embed a path
    text = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<id>", text)
    return text


def tool_text(content) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(c.get("text", "") for c in content or [] if isinstance(c, dict))


def summarize(path: Path, runs_dir: Path | None) -> dict:
    run = path.stem
    root = (runs_dir / run) if runs_dir else None
    info = {"run": run, "model": None, "skills_listed": [], "skill_calls": [], "skill_reads": [],
            "lint_runs": [], "edits": [], "denied": [], "steps": [], "final": "", "turns": None}
    calls: dict[str, dict] = {}
    first_edit = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("{"):
            continue
        event = json.loads(line)
        if event.get("type") == "system" and event.get("subtype") == "init":
            info["model"] = event.get("model")
            info["skills_listed"] = [s for s in SKILLS if s in (event.get("skills") or [])]
        elif event.get("type") == "result":
            info["final"] = event.get("result") or ""
            info["turns"] = event.get("num_turns")
        message = event.get("message") if isinstance(event.get("message"), dict) else {}
        for block in message.get("content", []) or []:
            if block.get("type") == "tool_use":
                name, args = block["name"], block.get("input", {})
                target = args.get("skill") or args.get("file_path") or args.get("command") or args.get("pattern") or ""
                step = {"n": len(info["steps"]) + 1, "tool": name, "target": sanitize(target, root), "status": "?"}
                info["steps"].append(step)
                calls[block["id"]] = step
                if name == "Skill":
                    info["skill_calls"].append({"skill": target, "step": step["n"], "before_first_edit": first_edit is None})
                elif name == "Read" and str(target).replace("\\", "/").endswith("SKILL.md"):
                    info["skill_reads"].append(Path(str(target).replace("\\", "/")).parent.name)
                elif name in ("Edit", "Write", "NotebookEdit"):
                    first_edit = first_edit or step["n"]
                    info["edits"].append(step["target"])
            elif block.get("type") == "tool_result" and block.get("tool_use_id") in calls:
                step = calls[block["tool_use_id"]]
                step["status"] = "denied" if block.get("is_error") else "ok"
                if step["tool"] in ("Bash", "PowerShell") and "spec_lint" in step["target"]:
                    output = sanitize(tool_text(block.get("content")), root)
                    info["lint_runs"].append({"step": step["n"], "status": step["status"], "output": output.strip()})
                if step["status"] == "denied":
                    info["denied"].append(step["tool"])
    info["changes"] = diff(root) if root is not None else ""
    return info


def diff(root: Path) -> str:
    try:
        first = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=root, capture_output=True,
                               text=True, check=True).stdout.split()[0]
        tracked = subprocess.run(["git", "diff", "--no-color", "-U0", first, "--", "."], cwd=root,
                                 capture_output=True, text=True, encoding="utf-8", check=True).stdout
        untracked = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=root,
                                   capture_output=True, text=True, check=True).stdout.split()
    except (OSError, subprocess.CalledProcessError, IndexError):
        return ""
    lines = [l for l in tracked.splitlines() if not l.startswith(("index ", "diff --git"))]
    lines += [f"(new untracked file: {u})" for u in untracked]
    return "\n".join(lines)


def extract(info: dict) -> str:
    out = [f"# Run {info['run']}", "", "## Tool calls, in order", ""]
    for step in info["steps"]:
        target = " ⏎ ".join(step["target"].splitlines())
        target = target if len(target) <= 160 else target[:157] + "..."
        flag = " (denied)" if step["status"] == "denied" else ""
        out.append(f"{step['n']}. `{step['tool']}` " + (f"`{target.replace('`', chr(39))}`" if target else "") + flag)
    if info["lint_runs"]:
        out += ["", "## spec_lint output", ""]
        for lint in info["lint_runs"]:
            out += [f"Step {lint['step']} ({lint['status']}):", "", "```text", lint["output"], "```", ""]
    out += ["", "## Final reply", "", sanitize(info["final"], None).strip(), "", "## Changes since the starting commit", ""]
    out += (["```diff", info["changes"], "```"] if info["changes"] else ["None."]) + [""]
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--transcripts", type=Path, required=True)
    parser.add_argument("--runs", type=Path)
    parser.add_argument("--extracts", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    infos = [summarize(p, args.runs) for p in sorted(args.transcripts.glob("*.jsonl"))]
    if args.extracts:
        args.extracts.mkdir(parents=True, exist_ok=True)
        for info in infos:
            (args.extracts / f"{info['run']}.md").write_text(extract(info), encoding="utf-8", newline="\n")
    if args.json:
        print(json.dumps([{k: v for k, v in i.items() if k != "steps"} for i in infos], indent=2))
        return
    for i in infos:
        calls = ", ".join(f"{c['skill']}@{c['step']}" + ("" if c["before_first_edit"] else " (after edit)")
                          for c in i["skill_calls"]) or "none"
        lints = "; ".join(f"step {l['step']} {l['status']}: " + (l["output"].splitlines() or [""])[-1][:80]
                          for l in i["lint_runs"]) or "none"
        print(f"== {i['run']}  model={i['model']}  turns={i['turns']}")
        print(f"   listed: {', '.join(i['skills_listed']) or 'NONE'}")
        print(f"   Skill calls: {calls}")
        print(f"   SKILL.md reads: {', '.join(i['skill_reads']) or 'none'}")
        print(f"   spec_lint: {lints}")
        print(f"   edits: {', '.join(i['edits']) or 'none'}   denied: {', '.join(i['denied']) or 'none'}")


if __name__ == "__main__":
    main()
