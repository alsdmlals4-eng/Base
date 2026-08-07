from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/project_asset_vault.py"


def run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ProjectAssetVaultTests(unittest.TestCase):
    def test_init_creates_local_vault_and_gitignore(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = run_tool("init", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / ".asset-vault/library").is_dir())
            self.assertTrue((project / ".asset-vault/archive").is_dir())
            self.assertTrue((project / ".asset-vault/inbox").is_dir())
            self.assertIn(".asset-vault/", (project / ".gitignore").read_text(encoding="utf-8"))

    def test_sync_mirrors_current_library_and_removes_only_previously_managed_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            library = project / ".asset-vault/library"
            (library / "characters").mkdir(parents=True)
            (library / "characters/hero.png").write_bytes(b"hero-v1")
            first = run_tool("sync", "--project-root", str(project))
            self.assertEqual(first.returncode, 0, first.stderr)
            managed = project / "assets/_managed/characters/hero.png"
            self.assertEqual(managed.read_bytes(), b"hero-v1")

            unrelated = project / "assets/_managed/user-authored.txt"
            unrelated.write_text("keep", encoding="utf-8")
            (library / "characters/hero.png").unlink()
            second = run_tool("sync", "--project-root", str(project))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse(managed.exists())
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep")

    def test_manual_addition_becomes_managed_and_manifest_has_no_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            asset = project / ".asset-vault/library/ui/button.webp"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"button")
            result = run_tool("sync", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest_path = project / "assets/ASSET_VAULT_SYNC.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["authority"], "local-vault-filesystem")
            self.assertEqual(manifest["assets"][0]["source_key"], "ui/button.webp")
            self.assertEqual(manifest["assets"][0]["managed_path"], "assets/_managed/ui/button.webp")
            self.assertNotIn(str(project), manifest_path.read_text(encoding="utf-8"))

    def test_download_pull_imports_new_image_once_and_does_not_resurrect_deleted_vault_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as downloads_tmp:
            project = Path(tmp)
            downloads = Path(downloads_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)

            # Baseline existing files without importing them.
            old = downloads / "old.png"
            old.write_bytes(b"old")
            baseline = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertFalse(any((project / ".asset-vault/library/gpt-imports").rglob("old.png")))

            new = downloads / "generated.png"
            new.write_bytes(b"generated")
            pulled = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(pulled.returncode, 0, pulled.stderr)
            copies = list((project / ".asset-vault/library/gpt-imports").rglob("generated.png"))
            self.assertEqual(len(copies), 1)
            copies[0].unlink()

            # Same download source is already processed; sync must not resurrect it.
            again = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertFalse(any((project / ".asset-vault/library/gpt-imports").rglob("generated.png")))
            self.assertFalse(any((project / "assets/_managed").rglob("generated.png")))

    def test_pull_downloads_ignores_non_images_and_partial_downloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as downloads_tmp:
            project = Path(tmp)
            downloads = Path(downloads_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            # Baseline empty source, then add unsupported/partial files.
            self.assertEqual(run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads)).returncode, 0)
            (downloads / "notes.txt").write_text("x", encoding="utf-8")
            (downloads / "image.png.crdownload").write_bytes(b"partial")
            result = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(result.returncode, 0, result.stderr)
            imported = project / ".asset-vault/library/gpt-imports"
            self.assertFalse(imported.exists() and any(imported.rglob("*")))

    def test_sync_rejects_managed_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(tmp)
            outside = Path(outside_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            asset = project / ".asset-vault/library/ui/button.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"button")
            managed = project / "assets/_managed"
            managed.mkdir(parents=True)
            try:
                (managed / "ui").symlink_to(outside, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink unavailable: {error}")
            result = run_tool("sync", "--project-root", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((outside / "button.png").exists())

    def test_download_source_must_not_overlap_library_or_managed_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            library = project / ".asset-vault/library"
            result = run_tool("pull-downloads", "--project-root", str(project), "--source", str(library))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("overlaps", result.stderr)


if __name__ == "__main__":
    unittest.main()
