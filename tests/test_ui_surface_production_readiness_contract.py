"""Regressions for UI preproduction instructions, not game/runtime verification."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
REF_DIR = ROOT / "skills/auditing-and-refining-ui-art/references"
OWNER = REF_DIR / "ui-surface-production-readiness.md"
ADAPTER = REF_DIR / "project-adapter-contract.md"

# Whole statements are checked so a token alone cannot satisfy the boundary.
BOUNDARIES = (
    "APPROVED_SCOPE_IS_THE_DENOMINATOR: required planned surfaces remain gaps even when no scene exists.",
    "PLANNED_CONSUMER_IS_NOT_RUNTIME: a specified future consumer permits preparation, not an implementation claim.",
    "PIXEL_READ_REQUIRED: filenames, manifests and hashes alone do not prove that image contents were inspected.",
    "NO_NEW_IMAGE_IS_NOT_NO_DESIGN: a reused/native skin still needs composition, states and readability review.",
    "GENERATED_CANDIDATE_IS_NOT_USER_APPROVED: final asset and Blueprint approval remain separate user decisions.",
    "CAPTURE_IS_NOT_ACTION_PROOF: screenshots do not prove clicks, persistence, timing, audio or recovery.",
    "VISUAL_RUNTIME_CLAIM_REQUIRES_CAPTURE: a visual runtime completion claim needs a retained in-game capture.",
    "PINNED_CONTRACT_PRESERVED: newer Base content is adopted explicitly, never by silently replacing a project lock.",
    "OPEN_OTHER_PR_IS_READ_ONLY: no takeover, rebase, absorption, closure or merge of another workstream.",
    "PROJECT_CANON_WINS: reference-game features never authorize new project scope or overwrite approved identity.",
    "FLOW_MAP_IS_TEXT_NATIVE: navigation maps stay editable text, tables or Mermaid, not generated artwork.",
    "IMAGE_ART_USES_IMAGE_MODEL: native controls do not replace required authored border, illustration or icon art.",
    "REVIEW_SELF_IS_NOT_INDEPENDENT: five author rechecks are not a separate independent review.",
    "ADOPTION_IS_NOT_RUNTIME: routing/document tests never become Godot, device, Human or release PASS.",
)


def contract_errors(text):
    return [statement for statement in BOUNDARIES if statement not in text]


class UiSurfaceProductionReadinessContract(unittest.TestCase):
    def text(self):
        self.assertTrue(OWNER.is_file(), "missing executable-workflow reference")
        return OWNER.read_text(encoding="utf-8")

    def test_existing_adapter_routes_to_owner(self):
        text = ADAPTER.read_text(encoding="utf-8")
        self.assertIn("[ui-surface-production-readiness.md](ui-surface-production-readiness.md)", text)
        self.assertIn("UI_SURFACE_PRODUCTION_READINESS", text)
        self.assertIn("source commit", text)

    def test_boundaries_have_direction_not_only_tokens(self):
        self.assertEqual(contract_errors(self.text()), [])

    def test_each_removed_boundary_is_rejected(self):
        text = self.text()
        for statement in BOUNDARIES:
            with self.subTest(statement=statement):
                self.assertIn(statement, contract_errors(text.replace(statement, "")))

    def test_each_reversed_boundary_is_rejected(self):
        text = self.text()
        for statement in BOUNDARIES:
            with self.subTest(statement=statement):
                marker = statement.split(":", 1)[0]
                reversed_text = text.replace(statement, marker + ": opposite behavior is allowed.")
                self.assertIn(statement, contract_errors(reversed_text))

    def test_required_modules_are_individually_routable(self):
        text = self.text()
        for identifier in ("UI-FLOW", "UI-SKIN", "UI-ACTION", "UI-REFERENCE", "UI-IMAGE", "UI-EVIDENCE"):
            with self.subTest(identifier=identifier):
                self.assertRegex(text, rf"(?m)^## {identifier} ")

    def test_full_journey_and_nested_surfaces(self):
        text = self.text()
        for key in ("page_id", "tab_id", "parent_surface", "return_target", "focus_restore", "scroll_restore", "cold_start", "save_reload"):
            self.assertIn(key, text)

    def test_system_and_dialogue_skin_decomposition(self):
        text = self.text()
        for key in ("dialogue_frame", "system_panel", "nameplate", "choice_row", "continue_indicator", "history_panel", "confirmation_modal", "tab_header", "tooltip", "scrollbar"):
            self.assertIn(key, text)

    def test_actual_nine_slice_and_layer_contract(self):
        text = self.text()
        for key in ("StyleBoxTexture", "NinePatchRect", "texture_margin", "content_margin", "region_rect", "mouse_filter", "alpha", "text_safe_area", "PanelContainer", "TabContainer"):
            self.assertIn(key, text)

    def test_menu_actions_have_recovery_contract(self):
        text = self.text()
        for key in ("new_game", "continue", "archive", "settings", "exit", "corrupt", "double", "rollback"):
            self.assertIn(key, text)

    def test_reference_observation_and_implementation_are_separate(self):
        text = self.text()
        for key in ("OBSERVED_BEHAVIOR", "SOURCE_VERIFIED", "IMPLEMENTATION_HYPOTHESIS", "ADOPT", "ADAPT", "REJECT", "source_version", "reference_method"):
            self.assertIn(key, text)

    def test_readiness_is_multiaxis(self):
        text = self.text()
        for key in ("SPECIFIED", "ASSET_READY", "IMPLEMENTED", "MACHINE_VERIFIED", "RUNTIME_VERIFIED", "USER_APPROVED", "unknown", "NOT_APPLICABLE"):
            self.assertIn(key, text)

    def test_receipt_has_run_identity_and_binary_readback(self):
        text = self.text()
        for key in ("source_commit", "build_or_run_id", "scene", "state", "viewport", "renderer", "capture_path", "sha256", "diagnostics", "evidence_ceiling", "NOT_RUN"):
            self.assertIn(key, text)

    def test_work_codex_pipeline_keeps_approval_and_runtime_separate(self):
        text = self.text()
        for key in ("Work", "Codex", "Blueprint", "final approval", "cold-start", "post-merge"):
            self.assertIn(key, text)

    def test_no_new_services_or_parallel_canon(self):
        text = self.text()
        for phrase in ("not a second canon", "No new paid service", "No mandatory new schema", "existing owner"):
            self.assertIn(phrase, text)
        self.assertNotIn("sandbox:/", text)

    def test_primary_sources_recorded(self):
        text = self.text()
        for url in ("https://www.renpy.org/doc/html/gui.html", "https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html", "https://docs.godotengine.org/en/stable/classes/class_tabcontainer.html", "https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html"):
            self.assertIn(url, text)


if __name__ == "__main__":
    unittest.main()
