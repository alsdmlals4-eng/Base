from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

clusters = manifest.pop("parallel_execution_groups", None)
if clusters is None:
    clusters = manifest.get("responsibility_clusters", [])
for cluster in clusters:
    cluster["cluster_id"] = cluster.pop("group_id", cluster.get("cluster_id"))
    cluster.pop("can_run_with_other_groups", None)
    cluster.pop("execution_role", None)
    cluster["purpose"] = "REFERENCE_AND_LEARNING_CLUSTER_ONLY"
manifest["responsibility_clusters"] = clusters

manifest["control_plane"]["change_protocol"] = [
    "Coordinator may fix validated cross-Part or CP0 findings directly with CROSS_PART_CHANGE semantic attribution",
    "Different Part ownership alone is not a write barrier",
    "Independent open/draft/ready workstreams remain read-only unless the user explicitly authorizes takeover",
    "CROSS_PART_CHANGE_REQUEST is reserved for real authority/evidence/active-workstream blockers",
    "Generated artifacts are rebuilt from authority rather than hand-edited",
    "Exact-head CI and post-merge GitHub/Notion readback are required",
]

parts = {part["part_id"]: part for part in manifest["parts"]}

def remove_path(pid: str, pattern: str) -> None:
    paths = parts[pid]["owned_write_paths"]
    while pattern in paths:
        paths.remove(pattern)


def add_path(pid: str, pattern: str) -> None:
    paths = parts[pid]["owned_write_paths"]
    if pattern not in paths:
        paths.append(pattern)

remove_path("P03", "templates/quality/**")
add_path("P03", "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md")
add_path("P02", "templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md")
add_path("P05", "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md")
add_path("P07", "templates/quality/PROJECT_CHANGE_VALIDATION.md")
add_path("P07", "templates/quality/REVIEW_EVIDENCE_RECORD.json")

manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Update contract tests to protect the new semantic owner map and reject stale parallel naming.
test_path = ROOT / "tests/test_sequential_part_coordinator_contract.py"
text = test_path.read_text(encoding="utf-8")
needle = "    def test_cross_part_request_is_only_for_real_coordination_blockers(self) -> None:\n"
insert = '''    def test_manifest_uses_reference_clusters_not_parallel_execution_groups(self) -> None:\n        manifest = self.load_manifest()\n        self.assertNotIn("parallel_execution_groups", manifest)\n        clusters = manifest["responsibility_clusters"]\n        self.assertEqual(3, len(clusters))\n        self.assertEqual({"G1_FOUNDATION", "G2_GAME_PRODUCTION", "G3_DELIVERY_AI_CONTENT"}, {row["cluster_id"] for row in clusters})\n        self.assertTrue(all(row["purpose"] == "REFERENCE_AND_LEARNING_CLUSTER_ONLY" for row in clusters))\n\n    def test_quality_templates_have_semantic_owners_instead_of_broad_p03_glob(self) -> None:\n        manifest = self.load_manifest()\n        p03 = next(p for p in manifest["parts"] if p["part_id"] == "P03")\n        self.assertNotIn("templates/quality/**", p03["owned_write_paths"])\n        expected = {\n            "templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md": "P02",\n            "templates/quality/GAME_UX_UI_REVIEW_CHECKLIST.md": "P05",\n            "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md": "P03",\n            "templates/quality/PROJECT_CHANGE_VALIDATION.md": "P07",\n            "templates/quality/REVIEW_EVIDENCE_RECORD.json": "P07",\n        }\n        for path, owner in expected.items():\n            result = self.run_scope("--coordinator", "--files", path)\n            self.assertEqual(0, result.returncode, result.stdout + result.stderr)\n            self.assertIn(f"SEMANTIC_OWNER:{owner}", result.stdout)\n\n    def test_control_plane_protocol_allows_direct_cross_part_fixes_but_protects_active_workstreams(self) -> None:\n        manifest = self.load_manifest()\n        protocol = "\\n".join(manifest["control_plane"]["change_protocol"])\n        self.assertIn("CROSS_PART_CHANGE", protocol)\n        self.assertIn("not a write barrier", protocol)\n        self.assertIn("open/draft/ready", protocol)\n        self.assertIn("CROSS_PART_CHANGE_REQUEST", protocol)\n\n'''
if "test_manifest_uses_reference_clusters_not_parallel_execution_groups" not in text:
    if needle not in text:
        raise SystemExit("sequential test insertion anchor missing")
    text = text.replace(needle, insert + needle, 1)
test_path.write_text(text, encoding="utf-8", newline="\n")

base_test = ROOT / "tests/test_base_partition_contract.py"
text = base_test.read_text(encoding="utf-8")
text = text.replace("def test_parallel_groups_and_integration_order_are_explicit", "def test_responsibility_clusters_and_integration_order_are_explicit")
text = text.replace('groups = manifest["parallel_execution_groups"]', 'groups = manifest["responsibility_clusters"]')
base_test.write_text(text, encoding="utf-8", newline="\n")

print("COORDINATOR_MANIFEST_SEMANTICS_HARDENED")
