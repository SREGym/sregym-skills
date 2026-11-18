"""Portable context discovery and read-only CLI checks."""

import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/sregym-fault-engineering/scripts/collect_fault_context.py"
)
SPEC = importlib.util.spec_from_file_location("collect_fault_context", SCRIPT)
CONTEXT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTEXT)


class ContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.repo = self.root / "SREGym checkout with spaces"
        self.registry = self.repo / "sregym/conductor/problems/registry.py"
        self.registry.parent.mkdir(parents=True)
        self.registry.write_text(
            "node_conntrack_exhaustion_hotel_reservation = None\n", encoding="utf-8"
        )
        self.fault = self.registry.parent / "node_conntrack_exhaustion.py"
        self.fault.write_text(
            "fault = 'node_conntrack_exhaustion_hotel_reservation'\n", encoding="utf-8"
        )
        self.outside = self.root / "outside"
        self.outside.mkdir()

    def cli(self, *arguments, cwd=None, environment=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=self.outside if cwd is None else cwd,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

    def snapshot(self):
        return {
            path.relative_to(self.repo): path.read_bytes()
            for path in self.repo.rglob("*")
            if path.is_file()
        }

    def test_find_repository_at_root(self):
        self.assertEqual(CONTEXT.find_repository(self.repo), self.repo)

    def test_find_repository_from_nested_directory(self):
        self.assertEqual(CONTEXT.find_repository(self.registry.parent), self.repo)

    def test_find_repository_outside_checkout(self):
        self.assertIsNone(CONTEXT.find_repository(self.outside))

    def test_no_checkout_reports_how_to_select_one(self):
        result = self.cli("conntrack")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--repo", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_explicit_invalid_checkout_does_not_fall_back_to_cwd(self):
        result = self.cli("conntrack", "--repo", str(self.outside), cwd=self.repo)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not an SREGym checkout", result.stderr)

    def test_missing_ripgrep_reports_dependency(self):
        environment = dict(os.environ, PATH="")
        result = self.cli(
            "conntrack", "--repo", str(self.repo), environment=environment
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("ripgrep", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_git_is_optional(self):
        with patch.object(CONTEXT.shutil, "which", return_value=None):
            self.assertEqual(CONTEXT.branch_name(self.repo), "<Git unavailable>")

    @unittest.skipUnless(shutil.which("git"), "Git is not installed")
    def test_source_archive_is_accepted_without_git_metadata(self):
        self.assertEqual(CONTEXT.branch_name(self.repo), "<not a Git checkout>")

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is not installed")
    def test_explicit_checkout_and_search_leave_files_unchanged(self):
        before = self.snapshot()
        result = self.cli("node_conntrack_exhaustion", "--repo", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.fault), result.stdout)
        self.assertIn("registry.py:1:", result.stdout)
        self.assertEqual(self.snapshot(), before)

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is not installed")
    def test_cli_discovers_checkout_from_nested_directory(self):
        result = self.cli("conntrack", cwd=self.registry.parent)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(self.repo), result.stdout)

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is not installed")
    def test_hyphenated_query_falls_back_to_underscore(self):
        result = self.cli("node-conntrack-exhaustion", "--repo", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("registry.py:1:", result.stdout)

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is not installed")
    def test_query_that_starts_with_dash_is_not_an_rg_option(self):
        self.fault.write_text("value = '--unexpected-query'\n", encoding="utf-8")
        result = self.cli("--repo", str(self.repo), "--", "--unexpected-query")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--unexpected-query", result.stdout)

    @unittest.skipUnless(shutil.which("rg"), "ripgrep is not installed")
    def test_query_without_matches_is_not_an_error(self):
        result = self.cli("no_such_fault", "--repo", str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("<none>"), 2)


if __name__ == "__main__":
    unittest.main()
