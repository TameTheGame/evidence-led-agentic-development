#!/usr/bin/env python3
"""ELAD repository checks: a skill lint, a relative-link check, and a private-word check.

Dependency-free; Python 3.10 or newer, and git for the private-word check. Run from anywhere:

    python tools/check.py

Exit code 0 means every check passed. It proves the repository's skills and links are
well formed and that no listed private word appears in it, nothing more.

The private-word check fails when a tracked text file, a tracked file name, or a commit
message contains a word or phrase whose fingerprint is in tools/private-words.sha256. The
readable list is kept outside the repository; to regenerate the fingerprints from it:

    python tools/check.py --hash-words <list> > tools/private-words.sha256
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent

# Where skills may live: skills/<name>/SKILL.md and examples/<target>/skills/<name>/SKILL.md.
SKILL_GLOBS = ("skills/*/SKILL.md", "examples/*/skills/*/SKILL.md")
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv"}

INLINE_LINK = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*(<[^>]*>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
FENCE = re.compile(r"^\s{0,3}(```|~~~)")
INLINE_CODE = re.compile(r"`+[^`]*`+")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")

PRIVATE_WORDS = ROOT / "tools" / "private-words.sha256"
WORD = re.compile(r"[a-z0-9]+")
MAX_PHRASE_WORDS = 3
FINGERPRINT = re.compile(r"^[0-9a-f]{64}$")
# Prefixed so the fingerprints don't match generic SHA-256 lookup tables.
FINGERPRINT_PREFIX = b"elad-private-word:"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def markdown_files() -> list[Path]:
    files = []
    for path in sorted(ROOT.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return files


# --- Skill lint -------------------------------------------------------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str] | None, str, str | None]:
    """Return (fields, body, error). Supports single-line `key: value` fields only."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text, "missing YAML frontmatter (first line must be ---)"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, text, "frontmatter is not closed with ---"
    fields: dict[str, str] = {}
    for number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            return None, text, f"line {number}: expected `key: value`"
        key, value = match.group(1), match.group(2).strip()
        if key in fields:
            return None, text, f"line {number}: duplicate key `{key}`"
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = value
    return fields, "\n".join(lines[end + 1:]), None


def check_skills() -> tuple[list[str], int]:
    problems: list[str] = []
    expected = {path for pattern in SKILL_GLOBS for path in ROOT.glob(pattern)}
    for path in sorted(ROOT.rglob("SKILL.md")):
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path not in expected:
            problems.append(f"{rel(path)}: SKILL.md outside skills/<name>/ or examples/<target>/skills/<name>/")
    for path in sorted(expected):
        where = rel(path)
        fields, body, error = parse_frontmatter(path.read_text(encoding="utf-8"))
        if error:
            problems.append(f"{where}: {error}")
            continue
        keys = set(fields)
        if keys != {"name", "description"}:
            extra = sorted(keys - {"name", "description"})
            missing = sorted({"name", "description"} - keys)
            detail = "; ".join(filter(None, [
                f"missing {', '.join(missing)}" if missing else "",
                f"unexpected {', '.join(extra)}" if extra else "",
            ]))
            problems.append(f"{where}: frontmatter must have exactly name and description ({detail})")
        name = fields.get("name", "")
        folder = path.parent.name
        if name and name != folder:
            problems.append(f"{where}: name `{name}` does not match folder `{folder}`")
        if name and (len(name) > MAX_NAME or not SKILL_NAME.match(name)):
            problems.append(f"{where}: name must be lowercase words joined by hyphens, at most {MAX_NAME} characters")
        description = fields.get("description", "")
        if description and not description.startswith("Use when"):
            problems.append(f"{where}: description must start with \"Use when\"")
        if len(description) > MAX_DESCRIPTION:
            problems.append(f"{where}: description is {len(description)} characters; the limit is {MAX_DESCRIPTION}")
        if not body.strip():
            problems.append(f"{where}: body is empty")
    return problems, len(expected)


# --- Link check -------------------------------------------------------------------------

def slugify(heading: str) -> str:
    """GitHub-style heading anchor."""
    text = INLINE_CODE.sub(lambda m: m.group(0).strip("`"), heading)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links keep their text
    text = re.sub(r"<[^>]+>", "", text)  # inline HTML
    text = text.strip().lower()
    kept = []
    for char in text:
        if char in (" ", "-", "_") or unicodedata.category(char)[0] in ("L", "N"):
            kept.append(char)
    return "".join(kept).replace(" ", "-")


def anchors(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        seen: dict[str, int] = {}
        result: set[str] = set()
        in_fence = False
        for line in path.read_text(encoding="utf-8").splitlines():
            if FENCE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING.match(line)
            if not match:
                continue
            slug = slugify(match.group(1))
            count = seen.get(slug, 0)
            result.add(slug if count == 0 else f"{slug}-{count}")
            seen[slug] = count + 1
        cache[path] = result
    return cache[path]


def links_in(path: Path):
    """Yield (line number, target) for every inline or reference link outside code.

    Link text may wrap across lines, so the search runs over the whole file with fenced
    blocks and inline code blanked out (keeping line breaks, so line numbers stay right).
    """
    kept = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            kept.append("")
        else:
            kept.append("" if in_fence else line)
    text = INLINE_CODE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), "\n".join(kept))
    for match in INLINE_LINK.finditer(text):
        yield text.count("\n", 0, match.start()) + 1, match.group(1)
    for number, line in enumerate(text.split("\n"), start=1):
        reference = REFERENCE_LINK.match(line)
        if reference:
            yield number, reference.group(1)


def check_links(files: list[Path]) -> tuple[list[str], int]:
    problems: list[str] = []
    cache: dict[Path, set[str]] = {}
    checked = 0
    for path in files:
        for number, raw in links_in(path):
            target = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
            if not target or SCHEME.match(target) or target.startswith("//"):
                continue
            checked += 1
            where = f"{rel(path)}:{number}"
            file_part, _, anchor = target.partition("#")
            file_part = unquote(file_part)
            if file_part:
                base = ROOT if file_part.startswith("/") else path.parent
                resolved = (base / file_part.lstrip("/")).resolve()
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    problems.append(f"{where}: link leaves the repository: {target}")
                    continue
                if not resolved.exists():
                    problems.append(f"{where}: broken link: {target}")
                    continue
            else:
                resolved = path
            if anchor:
                if resolved.is_file() and resolved.suffix.lower() == ".md":
                    if unquote(anchor).lower() not in anchors(resolved, cache):
                        problems.append(f"{where}: no heading for anchor #{anchor} in {rel(resolved)}")
    return problems, checked


# --- Private-word check -----------------------------------------------------------------

def words(text: str) -> list[str]:
    """Lowercase ASCII letter-and-digit runs; everything else separates words."""
    return WORD.findall(text.lower())


def fingerprint(phrase: str) -> str:
    return hashlib.sha256(FINGERPRINT_PREFIX + phrase.encode("ascii")).hexdigest()


def load_fingerprints() -> tuple[set[str], str | None]:
    where = rel(PRIVATE_WORDS)
    if not PRIVATE_WORDS.is_file():
        return set(), f"{where}: missing"
    found: set[str] = set()
    for number, line in enumerate(PRIVATE_WORDS.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not FINGERPRINT.match(line):
            return set(), f"{where}:{number}: expected a lowercase SHA-256 hex digest"
        found.add(line)
    if not found:
        return set(), f"{where}: no fingerprints"
    return found, None


class PrivateWords:
    """Finds every run of one to three words whose fingerprint is listed."""

    def __init__(self, fingerprints: set[str]):
        self.fingerprints = fingerprints
        self.known: dict[str, bool] = {}

    def is_private(self, phrase: str) -> bool:
        if phrase not in self.known:
            self.known[phrase] = fingerprint(phrase) in self.fingerprints
        return self.known[phrase]

    def lines(self, text: str) -> list[int]:
        """Line numbers on which a private word or phrase starts."""
        lowered = text.lower()
        matches = list(WORD.finditer(lowered))
        tokens = [match.group() for match in matches]
        found = []
        for start in range(len(tokens)):
            for count in range(1, MAX_PHRASE_WORDS + 1):
                if start + count > len(tokens):
                    break
                if self.is_private(" ".join(tokens[start:start + count])):
                    found.append(lowered.count("\n", 0, matches[start].start()) + 1)
                    break
        return sorted(set(found))


def git_output(*args: str) -> str | None:
    try:
        result = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True)
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", errors="replace")


def check_private_words() -> tuple[list[str], str]:
    fingerprints, error = load_fingerprints()
    if error:
        return [error], ""
    listed = git_output("ls-files", "-z")
    if listed is None:
        return ["private-word check needs a git checkout of this repository"], ""
    matcher = PrivateWords(fingerprints)
    problems: list[str] = []
    paths = [path for path in listed.split("\0") if path]
    for path in paths:
        if matcher.lines(path):
            problems.append(f"{path}: file name contains a private word")
        file = ROOT / path
        if not file.is_file():
            continue
        data = file.read_bytes()
        if b"\0" in data:
            continue  # binary
        for number in matcher.lines(data.decode("utf-8", errors="replace")):
            problems.append(f"{path}:{number}: contains a private word")
    log = git_output("log", "--format=%H%x00%B%x1e", "HEAD")
    commits = [entry.strip("\n") for entry in (log or "").split("\x1e") if entry.strip("\n")]
    for entry in commits:
        commit, _, message = entry.partition("\0")
        for number in matcher.lines(message):
            problems.append(f"commit {commit[:7]}: message line {number} contains a private word")
    return problems, f"no private words in {len(paths)} tracked files, their names, or {len(commits)} commit messages"


def hash_words(source: Path) -> int:
    """Print the fingerprint file for a readable list: one word or phrase per line, # comments."""
    fingerprints = set()
    for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), start=1):
        phrase = words(line.partition("#")[0])
        if not phrase:
            continue
        if len(phrase) > MAX_PHRASE_WORDS:
            print(f"{source}:{number}: more than {MAX_PHRASE_WORDS} words", file=sys.stderr)
            return 1
        fingerprints.add(fingerprint(" ".join(phrase)))
    print("# Fingerprints of words that must not appear in this repository, read by tools/check.py.")
    print("# Each is the SHA-256 of a prefix and one to three lowercase words; see check.py.")
    print("# The readable list is kept outside the repository.")
    for value in sorted(fingerprints):
        print(value)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ELAD repository checks.")
    parser.add_argument("--hash-words", type=Path, metavar="LIST",
                        help="print the fingerprint file for a readable word list, then exit")
    options = parser.parse_args()
    if options.hash_words:
        return hash_words(options.hash_words)

    skill_problems, skill_count = check_skills()
    files = markdown_files()
    link_problems, link_count = check_links(files)
    word_problems, word_summary = check_private_words()
    problems = skill_problems + link_problems + word_problems
    for problem in problems:
        print(f"FAIL  {problem}")
    if problems:
        print(f"FAIL — {len(problems)} problem(s).")
        return 1
    print(f"PASS — {skill_count} skills linted; {link_count} relative links in {len(files)} Markdown files resolve; "
          f"{word_summary}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
