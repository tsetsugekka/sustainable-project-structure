#!/usr/bin/env python3
"""Check or regenerate explicitly marked README document indexes (standard library only)."""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote


START = re.compile(r'<!-- DOC_INDEX:START scopes="([^"\n]+)" -->')
END = "<!-- DOC_INDEX:END -->"
EXCLUDED_DIRS = {"archive", "history", "records", "temporary", "temp", "tmp", "node_modules", "__pycache__", "vendor", "dist", "build"}
EXCLUDED_FILES = {"task.md", "changelog.md", "agents.md", "claude.md", "moved_paths.md"}


def excluded(path: Path) -> bool:
    return any(part.startswith(".") or re.sub(r"^\d+_", "", part.lower()) in EXCLUDED_DIRS
               for part in path.parts[:-1]) or path.name.lower() in EXCLUDED_FILES


def title(path: Path) -> str:
    fenced = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        if not fenced and line.startswith("# "):
            return re.sub(r"\s+#+\s*$", "", line[2:].strip()).replace("[", r"\[").replace("]", r"\]")
    raise ValueError(f"missing H1: {path}")


def documents(root: Path) -> list[Path]:
    allowed = None
    if (root / ".git").exists():
        result = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"], capture_output=True, check=True)
        allowed = set(result.stdout.decode().split("\0"))
    paths = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        base = Path(directory)
        dirs[:] = [name for name in dirs if not (base / name).is_symlink()
                   and not excluded((base / name / "README.md").relative_to(root))
                   and not (base / name / ".git").exists()]
        for name in files:
            path = base / name
            relative = path.relative_to(root)
            if path.suffix.lower() == ".md" and not path.is_symlink() and not excluded(relative) and (allowed is None or relative.as_posix() in allowed):
                paths.append(path)
    return paths


def matches(path: PurePosixPath, scope: str) -> bool:
    # Segment matching keeps '*' local; '**' deliberately opts into recursion.
    parts = PurePosixPath(scope).parts
    def match(names: tuple[str, ...], patterns: tuple[str, ...]) -> bool:
        if not patterns:
            return not names
        if patterns[0] == "**":
            return match(names, patterns[1:]) or bool(names) and match(names[1:], patterns)
        return bool(names) and fnmatch.fnmatchcase(names[0], patterns[0]) and match(names[1:], patterns[1:])
    return match(path.parts, parts)


def render(root: Path, readme: Path, text: str, candidates: list[Path] | None = None) -> str:
    starts = list(START.finditer(text))
    if len(starts) != 1 or text.count("DOC_INDEX:START") != 1 or text.count(END) != 1:
        raise ValueError(f"invalid index markers: {readme}")
    start = starts[0]
    end = text.index(END)
    if end < start.end():
        raise ValueError(f"reversed index markers: {readme}")
    paths = set()
    for scope in start.group(1).split():
        if PurePosixPath(scope).is_absolute() or ".." in PurePosixPath(scope).parts:
            raise ValueError(f"scope must stay inside README directory: {scope}")
        for path in candidates if candidates is not None else documents(root):
            if not path.is_relative_to(readme.parent) or not matches(PurePosixPath(path.relative_to(readme.parent).as_posix()), scope):
                continue
            relative = path.relative_to(root)
            if path.is_file() and path.suffix.lower() == ".md" and path != readme and not excluded(relative):
                if not path.resolve().is_relative_to(root):
                    raise ValueError(f"index target outside project: {path}")
                paths.add(path)
    lines = [f"- [{title(path)}]({quote(path.relative_to(readme.parent).as_posix(), safe='/')})"
             for path in sorted(paths)]
    body = "\n\n" + "\n".join(lines) + "\n\n"
    return text[:start.end()] + body + text[end:]


def update(root: Path, write: bool = False) -> int:
    if not root.is_dir():
        raise ValueError(f"project root not found: {root}")
    pending = []
    count = 0
    candidates = documents(root)
    for readme in sorted(path for path in candidates if path.name == "README.md"):
        if excluded(readme.relative_to(root)):
            continue
        if not readme.resolve().is_relative_to(root):
            raise ValueError(f"README outside project: {readme}")
        text = readme.read_text(encoding="utf-8")
        if "DOC_INDEX:" not in text:
            continue
        count += 1
        result = render(root, readme, text, candidates)
        if result != text:
            pending.append((readme, result))
    if not count:
        raise ValueError("no DOC_INDEX markers found; reuse the project's existing index tool or configure README scopes")
    # Validate every marked file before writing any changes.
    for readme, result in pending:
        print(f"{'WRITE' if write else 'STALE'} {readme.relative_to(root)}")
        if write:
            readme.write_text(result, encoding="utf-8")
    return 0 if write or not pending else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        return update(args.root.expanduser().resolve(), args.write)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
