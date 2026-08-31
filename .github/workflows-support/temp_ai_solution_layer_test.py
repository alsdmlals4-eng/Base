from __future__ import annotations

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def bounded_section(text: str, start: str, end: str) -> str:
    start_index = text.index(start)
    end_index = text.index(end, start_index)
    return text[start_index:end_index]


class AISolutionLayerSelectionContractTests(unittest.TestCase):
    def test_public_video_uses_existing_reader_owner_before_blocker(self) -> None:
        intake = read("skills/managing-project-intake-and-work-contract/SKILL.md")
        start = "PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER"
        end = "새 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층 요청"
        self.assertIn(start, intake)
        self.assertIn(end, intake)
        section = bounded_section(intake, start, end)
        for term in (
            "VIDEO_LINK_IS_NOT_UNREADABLE_UNTIL_DECLARED_READER_LADDER_EXHAUSTED",
            "RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER",
            "docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md",
            "tools/public_video_research_ingest.py",
            "source_ladder",
            "ASR_FALLBACK_REQUIRED",
            "BLOCKED_UNVERIFIED",
            "PROJECT_REUSE_OPPORTUNITY_SCAN",
            "TRANSCRIPT_READY_IS_NOT_FACT_OR_PROJECT_FIT_PASS",
        ):
            self.assertIn(term, section)
        self.assertLess(
            section.index("PRODUCTION_TOOL_WORKFLOW_MODULES.md"),
            section.index("BLOCKED_UNVERIFIED"),
        )

    def test_layer_map_separates_model_context_integration_orchestration_and_harness(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        start = "## AI solution layer selection contract"
        end = "## AI game-engine machine boundary contract"
        self.assertIn(start, capability)
        self.assertIn(end, capability)
        section = bounded_section(capability, start, end)
        for term in (
            "AI_SOLUTION_LAYER_SELECTION",
            "MODEL_AND_TRAINING_LAYER",
            "CONTEXT_AND_KNOWLEDGE_LAYER",
            "TOOL_AND_INTEGRATION_LAYER",
            "ORCHESTRATION_LAYER",
            "HARNESS_LAYER",
            "HORIZON_VOCABULARY",
            "DO_NOT_STACK_EVERY_LAYER_BY_DEFAULT",
        ):
            self.assertIn(term, section)

    def test_model_and_training_capabilities_do_not_replace_task_evidence(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        for term in (
            "MODEL_CAPABILITY_IS_NOT_APPLICATION_ARCHITECTURE",
            "MULTIMODAL_INPUT_IS_NOT_TASK_COMPETENCE",
            "RLHF_IS_POST_TRAINING_NOT_RUNTIME_CONTROL",
            "human demonstrations or preference comparisons",
            "reward-based post-training stages",
            "PROMPT_AND_CONTEXT_BEFORE_FINE_TUNING",
            "CURRENT_KNOWLEDGE_IS_NOT_FINE_TUNING_DEFAULT",
            "EVAL_BEFORE_LAYER_ESCALATION",
        ):
            self.assertIn(term, capability)

    def test_knowledge_storage_and_rag_preserve_provenance_and_truth_boundaries(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        for term in (
            "KNOWLEDGE_BASE_IS_STORAGE_NOT_RETRIEVAL_OR_TRUTH",
            "RAG_RETRIEVES_EVIDENCE_BUT_DOES_NOT_GUARANTEE_TRUTH",
            "authoritative source",
            "retrieval relevance",
            "source freshness",
            "provenance",
        ):
            self.assertIn(term, capability)

    def test_mcp_is_interoperability_not_agent_authority(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        for term in (
            "MCP_IS_INTEROPERABILITY_NOT_AGENT_AUTHORITY_OR_APPROVAL",
            "capability negotiation",
            "host authority",
            "MCP_CONNECTED_IS_NOT_BEHAVIOR_PASS",
        ):
            self.assertIn(term, capability)

    def test_predictable_process_prefers_workflow_before_agent(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        start = "DETERMINISTIC_WORKFLOW_BEFORE_OPEN_ENDED_AGENT"
        end = "HARNESS_IS_COMPOSED_CONTROL_AND_EVIDENCE_SYSTEM"
        self.assertIn(start, capability)
        self.assertIn(end, capability)
        section = bounded_section(capability, start, end)
        for term in (
            "fixed and testable path",
            "open-ended",
            "dynamic planning",
            "stopping condition",
            "environment readback",
        ):
            self.assertIn(term, section)

    def test_harness_components_require_load_bearing_evidence_and_pruning(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        for term in (
            "HARNESS_IS_COMPOSED_CONTROL_AND_EVIDENCE_SYSTEM",
            "HARNESS_COMPONENTS_REQUIRE_LOAD_BEARING_EVIDENCE",
            "HARNESS_ABLATION_AND_PRUNING",
            "MODEL_VS_HARNESS_IS_AN_EVAL_QUESTION",
            "BASE_ALREADY_COMPOSES_A_HARNESS_NO_NEW_FRAMEWORK",
            "exact model/tool version",
            "materially changes behavior",
            "component's value in doubt",
        ):
            self.assertIn(term, capability)

    def test_agi_and_asi_are_horizon_terms_not_operational_authority(self) -> None:
        capability = read("docs/CAPABILITY_COMPOSITION_MAP.md")
        for term in (
            "AGI_ASI_AWARENESS_ONLY",
            "AGI/ASI",
            "implementation feature",
            "schedule assumption",
            "approval",
            "NO_NEW_AI_GLOSSARY_OR_SKILL",
        ):
            self.assertIn(term, capability)


if __name__ == "__main__":
    unittest.main()
