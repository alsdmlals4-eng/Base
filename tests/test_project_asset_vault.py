from __future__ import annotations

import json
import os
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
    def test_init_creates_local_vault_and_ignores_vault_and_godot_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            result = run_tool("init", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((project / ".asset-vault/library").is_dir())
            self.assertTrue((project / ".asset-vault/archive").is_dir())
            self.assertTrue((project / ".asset-vault/inbox").is_dir())
            gitignore = (project / ".gitignore").read_text(encoding="utf-8")
            self.assertIn(".asset-vault/", gitignore)
            self.assertIn("assets/_vault_local/", gitignore)

    def test_v2_contract_docs_route_local_candidates_to_explicit_promotion(self) -> None:
        config = json.loads(
            (ROOT / "templates/project-operations/PROJECT_ASSET_VAULT.json").read_text(encoding="utf-8")
        )
        self.assertEqual(config["schema_version"], 2)
        self.assertEqual(config["workspace_root"], "assets/_vault_local")
        self.assertEqual(config["sync_manifest"], ".asset-vault/sync.json")
        self.assertEqual(config["promotion_root"], "assets")
        self.assertNotIn("managed_root", config)

        policy = (ROOT / "docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md").read_text(encoding="utf-8")
        for token in (
            "assets/_vault_local/",
            "PROJECT_ASSET_APPROVED",
            "promote",
            "Global Asset Manager",
            "REUSE/TRIAL",
            ".gdignore",
            "VAULT_LOCAL_STATE_UNVERIFIED",
        ):
            self.assertIn(token, policy)

        documentation_map = (ROOT / "docs/DOCUMENTATION_MAP.md").read_text(encoding="utf-8")
        self.assertIn("docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md", documentation_map)

        image_policy = (ROOT / "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md", image_policy)
        self.assertIn("assets/_vault_local/", image_policy)
        self.assertIn("promote", image_policy)

        image_plan = (ROOT / "templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md").read_text(encoding="utf-8")
        for token in ("vault_source_key", "promotion_target", "promoted_path"):
            self.assertIn(token, image_plan)

        asset_manifest = (ROOT / "templates/project-operations/ASSET_MANIFEST.yml").read_text(encoding="utf-8")
        self.assertIn('workspace_root: "assets/_vault_local"', asset_manifest)
        self.assertIn('sync_manifest: ".asset-vault/sync.json"', asset_manifest)
        self.assertIn('promotion_root: "assets"', asset_manifest)

    def test_sync_mirrors_library_to_local_godot_workspace_and_removes_only_previous_copies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            library = project / ".asset-vault/library"
            (library / "characters").mkdir(parents=True)
            (library / "characters/hero.png").write_bytes(b"hero-v1")
            first = run_tool("sync", "--project-root", str(project))
            self.assertEqual(first.returncode, 0, first.stderr)
            workspace_asset = project / "assets/_vault_local/characters/hero.png"
            self.assertEqual(workspace_asset.read_bytes(), b"hero-v1")

            unrelated = project / "assets/_vault_local/user-authored.txt"
            unrelated.write_text("keep", encoding="utf-8")
            (library / "characters/hero.png").unlink()
            second = run_tool("sync", "--project-root", str(project))
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertFalse(workspace_asset.exists())
            self.assertEqual(unrelated.read_text(encoding="utf-8"), "keep")

    def test_sync_manifest_is_local_only_and_contains_no_absolute_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            asset = project / ".asset-vault/library/ui/button.webp"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"button")
            result = run_tool("sync", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest_path = project / ".asset-vault/sync.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["authority"], "local-vault-filesystem")
            self.assertEqual(manifest["assets"][0]["source_key"], "ui/button.webp")
            self.assertEqual(manifest["assets"][0]["workspace_path"], "assets/_vault_local/ui/button.webp")
            self.assertNotIn(str(project), manifest_path.read_text(encoding="utf-8"))
            self.assertFalse((project / "assets/ASSET_VAULT_SYNC.json").exists())

    def test_manual_deletion_tombstones_content_and_removes_local_workspace_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            asset = project / ".asset-vault/library/ui/button.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"button")
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)
            asset.unlink()
            result = run_tool("sync", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            state = json.loads((project / ".asset-vault/state.json").read_text(encoding="utf-8"))
            self.assertTrue(state["rejected_hashes"])
            self.assertFalse((project / "assets/_vault_local/ui/button.png").exists())

    def test_download_same_content_with_new_event_does_not_resurrect_deleted_vault_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as downloads_tmp:
            project = Path(tmp)
            downloads = Path(downloads_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            self.assertEqual(
                run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads)).returncode,
                0,
            )
            generated = downloads / "generated.png"
            generated.write_bytes(b"generated")
            pulled = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(pulled.returncode, 0, pulled.stderr)
            copies = list((project / ".asset-vault/library/gpt-imports").rglob("generated.png"))
            self.assertEqual(len(copies), 1)

            copies[0].unlink()
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)

            renamed = downloads / "generated-renamed.png"
            generated.rename(renamed)
            os.utime(renamed, None)
            again = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertIn("rejected=1", again.stdout)
            self.assertFalse(any((project / ".asset-vault/library/gpt-imports").rglob("generated-renamed.png")))
            self.assertFalse(any((project / "assets/_vault_local").rglob("generated-renamed.png")))

    def test_manual_readdition_is_explicit_and_clears_tombstone(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            original = project / ".asset-vault/library/ui/button.png"
            original.parent.mkdir(parents=True)
            original.write_bytes(b"button")
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)
            original.unlink()
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)
            state_before = json.loads((project / ".asset-vault/state.json").read_text(encoding="utf-8"))
            rejected_hash = state_before["rejected_hashes"][0]

            restored = project / ".asset-vault/library/restored/button.png"
            restored.parent.mkdir(parents=True)
            restored.write_bytes(b"button")
            result = run_tool("sync", "--project-root", str(project))
            self.assertEqual(result.returncode, 0, result.stderr)
            state_after = json.loads((project / ".asset-vault/state.json").read_text(encoding="utf-8"))
            self.assertNotIn(rejected_hash, state_after["rejected_hashes"])
            self.assertEqual((project / "assets/_vault_local/restored/button.png").read_bytes(), b"button")

    def test_promote_is_explicit_and_promoted_asset_survives_vault_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            source = project / ".asset-vault/library/ui/button.png"
            source.parent.mkdir(parents=True)
            source.write_bytes(b"button")
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)
            promoted = project / "assets/approved/ui/button.png"
            self.assertFalse(promoted.exists())

            result = run_tool(
                "promote",
                "--project-root",
                str(project),
                "--source-key",
                "ui/button.png",
                "--target",
                "approved/ui/button.png",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(promoted.read_bytes(), b"button")

            source.unlink()
            self.assertEqual(run_tool("sync", "--project-root", str(project)).returncode, 0)
            self.assertEqual(promoted.read_bytes(), b"button")

    def test_check_rejects_scene_reference_to_local_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            scene = project / "scenes/main.tscn"
            scene.parent.mkdir(parents=True)
            scene.write_text(
                '[gd_scene load_steps=2 format=3]\n[ext_resource path="res://assets/_vault_local/ui/button.png" type="Texture2D" id="1"]\n',
                encoding="utf-8",
            )
            result = run_tool("check", "--project-root", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("local-only workspace", result.stderr)
            self.assertIn("scenes/main.tscn", result.stderr)

    def test_check_rejects_untracked_scene_reference_inside_git_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=project, check=True)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            scene = project / "scenes/new_untracked_scene.tscn"
            scene.parent.mkdir(parents=True)
            scene.write_text(
                '[gd_scene load_steps=2 format=3]\n[ext_resource path="res://assets/_vault_local/ui/button.png" type="Texture2D" id="1"]\n',
                encoding="utf-8",
            )
            result = run_tool("check", "--project-root", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("new_untracked_scene.tscn", result.stderr)

    def test_pull_downloads_ignores_non_images_and_partial_downloads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as downloads_tmp:
            project = Path(tmp)
            downloads = Path(downloads_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            self.assertEqual(
                run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads)).returncode,
                0,
            )
            (downloads / "notes.txt").write_text("x", encoding="utf-8")
            (downloads / "image.png.crdownload").write_bytes(b"partial")
            result = run_tool("pull-downloads", "--project-root", str(project), "--source", str(downloads))
            self.assertEqual(result.returncode, 0, result.stderr)
            imported = project / ".asset-vault/library/gpt-imports"
            self.assertFalse(imported.exists() and any(imported.rglob("*")))

    def test_sync_rejects_workspace_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            project = Path(tmp)
            outside = Path(outside_tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            asset = project / ".asset-vault/library/ui/button.png"
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b"button")
            workspace = project / "assets/_vault_local"
            workspace.mkdir(parents=True, exist_ok=True)
            try:
                (workspace / "ui").symlink_to(outside, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"symlink unavailable: {error}")
            result = run_tool("sync", "--project-root", str(project))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((outside / "button.png").exists())

    def test_download_source_must_not_overlap_library_or_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            self.assertEqual(run_tool("init", "--project-root", str(project)).returncode, 0)
            library = project / ".asset-vault/library"
            result = run_tool("pull-downloads", "--project-root", str(project), "--source", str(library))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("overlaps", result.stderr)


if __name__ == "__main__":
    unittest.main()
