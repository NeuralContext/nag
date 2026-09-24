"""Find specification directories matching the current branch issue number."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


def fail(message: str) -> int:
    """Write a concise error message and return a failing status."""
    print(f"error: {message}", file=sys.stderr)
    return 1


def git_output(arguments: list[str]) -> str:
    """Run Git and return its trimmed standard output."""
    result = subprocess.run(
        arguments,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def contains_markdown_file(directory: Path) -> bool:
    """Return whether a directory contains a Markdown file at any depth."""
    return any(
        path.is_file() and path.suffix.lower() == ".md"
        for path in directory.rglob("*")
    )


def matching_folders(repo_root: Path, issue_number: str) -> list[str]:
    """Return specification folders matching an issue number."""
    specs_directory = repo_root / ".agents" / "specs"
    try:
        children = list(specs_directory.iterdir())
    except FileNotFoundError:
        return []
    except OSError as error:
        raise RuntimeError(f"cannot read specs directory: {error}") from error

    name_pattern = re.compile(rf"^{re.escape(issue_number)}-")
    folders: list[str] = []
    for child in children:
        if not child.is_dir() or not name_pattern.match(child.name):
            continue
        try:
            if contains_markdown_file(child):
                folders.append(str(child))
        except OSError as error:
            raise RuntimeError(f"cannot read candidate directory {child}: {error}") from error
    return sorted(folders)


def main() -> int:
    """Print matching specification directories for the current Git branch."""
    if len(sys.argv) != 1:
        return fail("expected no arguments")

    try:
        repo_root = Path(git_output(["git", "rev-parse", "--show-toplevel"]))
        branch = git_output(["git", "-C", str(repo_root), "branch", "--show-current"])
    except (OSError, subprocess.CalledProcessError):
        return fail("working directory must be inside a Git repository")

    match = re.match(r"^(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*$", branch)
    if match is None:
        return fail("branch name must use <issue-number>-<kebab-case-name>")

    try:
        folders = matching_folders(repo_root, match.group(1))
    except RuntimeError as error:
        return fail(str(error))

    print(json.dumps({"folders": folders}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
