"""Run with: python3 -m unittest discover -s scripts -p 'test_*.py'."""

import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

import doc_index
import scaffold_project


class IndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.write("README.md", "# Project\n\nManual introduction.\n" + scaffold_project.index_marker("*.md */README.md docs/**/*.md") + "\nManual footer.\n")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def update(self, write=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return doc_index.update(self.root, write)

    def test_lifecycle_titles_and_manual_content(self):
        path = self.write("docs/start.md", "# Start\n")
        self.assertEqual(self.update(), 1)
        self.assertNotIn("[Start]", (self.root / "README.md").read_text())
        self.assertEqual(self.update(True), 0)
        first = (self.root / "README.md").read_text()
        self.assertIn("[Start](docs/start.md)", first)
        self.assertTrue(first.endswith("Manual footer.\n"))
        self.assertIn("Manual introduction.", first)
        self.assertEqual(self.update(), 0)
        self.update(True)
        self.assertEqual(first, (self.root / "README.md").read_text())
        path.write_text("# New title\n")
        self.assertEqual(self.update(), 1)
        path.rename(self.root / "docs/renamed.md")
        self.update(True)
        self.assertIn("[New title](docs/renamed.md)", (self.root / "README.md").read_text())
        (self.root / "docs/renamed.md").unlink()
        self.assertEqual(self.update(), 1)
        self.update(True)
        self.assertNotIn("New title", (self.root / "README.md").read_text())

    def test_short_lived_nested_and_symlink_exclusion(self):
        self.write("module/README.md", "# Module\n")
        for name in ("docs/history/a.md", "docs/records/a.md", "98_Archive/README.md", "99_Temporary/README.md", "docs/TASK.md", "docs/CHANGELOG.md", "module/docs/detail.md", "vendor/README.md"):
            self.write(name, "# Excluded\n")
        (self.root / "docs/link.md").symlink_to(self.root / "module/README.md")
        (self.root / "linked").symlink_to(self.root / "module", target_is_directory=True)
        self.update(True)
        result = (self.root / "README.md").read_text()
        self.assertIn("[Module](module/README.md)", result)
        self.assertNotIn("Excluded", result)
        self.assertNotIn("link", result)

    def test_invalid_markers_do_not_modify_any_file(self):
        self.write("docs/new.md", "# New\n")
        self.write("module/README.md", "# Module\n<!-- DOC_INDEX:END -->\n")
        before = (self.root / "README.md").read_bytes()
        with self.assertRaises(ValueError):
            self.update(True)
        self.assertEqual(before, (self.root / "README.md").read_bytes())
        for marker in (scaffold_project.index_marker("../*.md"), "<!-- DOC_INDEX:END -->\n<!-- DOC_INDEX:START scopes=\"*.md\" -->", scaffold_project.index_marker("*.md") * 2):
            with self.subTest(marker=marker):
                with self.assertRaises(ValueError):
                    doc_index.render(self.root, self.root / "README.md", marker)

    def test_git_ignored_and_nested_repository(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.write(".gitignore", "docs/ignored.md\n")
        self.write("docs/ignored.md", "# Ignored\n")
        self.write("docs/new.md", "# Included\n")
        self.write("nested/README.md", "# Nested\n")
        subprocess.run(["git", "init", "-q", str(self.root / "nested")], check=True)
        self.update(True)
        result = (self.root / "README.md").read_text()
        self.assertIn("Included", result)
        self.assertNotIn("Ignored", result)
        self.assertNotIn("Nested", result)

    def test_deleted_tracked_file_is_removed_from_index(self):
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        path = self.write("docs/tracked.md", "# Tracked document\n")
        subprocess.run(["git", "-C", str(self.root), "add", "docs/tracked.md"], check=True)
        self.update(True)
        self.assertIn("Tracked document", (self.root / "README.md").read_text())
        path.unlink()
        self.assertEqual(self.update(), 1)
        self.update(True)
        self.assertNotIn("Tracked document", (self.root / "README.md").read_text())

    def test_missing_h1_does_not_write(self):
        self.write("docs/valid.md", "# Valid document\n")
        self.write("docs/invalid.md", "Body without a heading.\n")
        before = (self.root / "README.md").read_bytes()
        with self.assertRaisesRegex(ValueError, "missing H1"):
            self.update(True)
        self.assertEqual(before, (self.root / "README.md").read_bytes())


class ScaffoldTests(unittest.TestCase):
    def test_profiles_are_self_contained_and_check_clean(self):
        for profile, tool in (("development", "91_ProjectTools/doc_index.py"), ("research", "90_ReusableAssets/tools/doc_index.py")):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory:
                args = scaffold_project.parser().parse_args(["init", "--root", directory, "--profile", profile, "--name", "Example", "--unit", "01_Example", "--apply"])
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(scaffold_project.init_project(args), 0)
                result = subprocess.run(["python3", str(Path(directory) / tool), "--root", directory], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                self.assertIn(f"python3 {tool} --write", (Path(directory) / "AGENTS.md").read_text())
                root_text = (Path(directory) / "README.md").read_text()
                self.assertIn("01_Example/README.md", root_text)
                self.assertNotIn("01_Example/docs/", root_text)

    def test_existing_project_preserves_files_and_uses_existing_tool(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Existing\n")
            args = scaffold_project.parser().parse_args(["init", "--root", directory, "--profile", "development", "--name", "Example", "--allow-existing", "--apply"])
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(scaffold_project.init_project(args), 0)
            self.assertEqual((root / "README.md").read_text(), "# Existing\n")
            self.assertFalse((root / "91_ProjectTools/doc_index.py").exists())
            self.assertNotIn("DOC_INDEX:", (root / "90_ProjectDocs/README.md").read_text())


if __name__ == "__main__":
    unittest.main()
