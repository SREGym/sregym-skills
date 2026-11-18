#!/usr/bin/env python3
"""Locate the code, tests, and notes related to one SREGym fault."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Optional


REGISTRY_PATH = Path("sregym/conductor/problems/registry.py")
SEARCH_ROOTS = (
    "sregym/conductor/problems",
    "sregym/conductor/oracles",
    "sregym/generators/fault",
    "tests",
    "notes.mo/fault_docs",
    "notes.mo/fault_pr_reviews",
    "notes.mo/fault_testing",
)


def find_repository(start: Path) -> Optional[Path]:
    """Find a SREGym checkout at start or one of its parents."""
    start = start.expanduser().resolve()
    for candidate in (start, *start.parents):
        if (candidate / REGISTRY_PATH).is_file():
            return candidate
    return None


def branch_name(repo: Path) -> str:
    """Show branch information without requiring a Git checkout or Git itself."""
    if shutil.which("git") is None:
        return "<Git unavailable>"
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "<not a Git checkout>"
    return result.stdout.strip() or "<detached>"


def run(command: list[str], repo: Path) -> str:
    result = subprocess.run(
        command, cwd=repo, check=False, capture_output=True, text=True
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr.strip() or f"command failed: {command}")
    return result.stdout.rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "query", help="Fault identifier, class name, or distinctive term"
    )
    parser.add_argument(
        "--repo",
        type=Path,
        help="SREGym checkout root; default: find it from the working directory",
    )
    args = parser.parse_args()

    repo = (
        args.repo.expanduser().resolve()
        if args.repo is not None
        else find_repository(Path.cwd())
    )
    if repo is None:
        parser.error(
            "no SREGym checkout found from the working directory; select one with --repo"
        )
    if not (repo / REGISTRY_PATH).is_file():
        parser.error(f"not an SREGym checkout: {repo}")
    if shutil.which("rg") is None:
        parser.error("ripgrep (rg) is required but is not available on PATH")

    roots = [str(repo / item) for item in SEARCH_ROOTS if (repo / item).exists()]
    print(f"Repository: {repo}")
    print(f"Branch: {branch_name(repo)}")

    matching_files = run(["rg", "--files", *roots], repo).splitlines()
    normalized = args.query.lower().replace("-", "_")
    path_matches = sorted(
        path for path in matching_files if normalized in path.lower().replace("-", "_")
    )

    print("\nPath matches:")
    print("\n".join(path_matches) if path_matches else "<none>")

    content = run(
        ["rg", "-n", "-i", "--fixed-strings", "--", args.query, *roots],
        repo,
    )
    if not content and "-" in args.query:
        content = run(
            [
                "rg",
                "-n",
                "-i",
                "--fixed-strings",
                "--",
                args.query.replace("-", "_"),
                *roots,
            ],
            repo,
        )

    print("\nContent matches:")
    print(content or "<none>")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
