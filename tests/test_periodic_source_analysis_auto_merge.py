from __future__ import annotations

import json
import unittest
from datetime import date

from tools.periodic_source_analysis import (
    ANALYSIS_SCHEMA,
    REVIEW_SCHEMA,
    AnalysisBlocked,
    build_context_request,
    build_research_request,
    build_review_request,
    collect_source_urls,
    deterministic_gate,
    extract_output_text,
    render_scan_markdown,
    update_candidate_ledger,
    update_operations_ledger,
    validate_analysis_packet,
    validate_review_packet,
)


RUN_DATE = date(2026, 8, 14)
ARTICLE_URL = "https://example.com/articles/current-study"
NEW_SOURCE_URL = "https://newsource.example.org/research"
SELECTED = [{
    "source_id": "godot",
    "name": "Godot Engine official docs / blog / releases",
    "domains": ["GAME_DEVELOPMENT", "CODE_ENGINEERING"],
    "roles": ["AUTHORITY_TARGET"],
    "recommended_cadence": "daily-or-weekly",
    "scan_surfaces": ["blog", "release pages"],
    "last_successful_scan_at": "2026-08-13",
    "status": "ACTIVE",
}]


def candidate(**overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "candidate_id": "candidate-1",
        "source_id": "godot",
        "title": "Current Godot research note",
        "original_url": ARTICLE_URL,
        "published_or_updated_at": "2026-08-13",
        "checked_at": "2026-08-14",
        "source_role": "AUTHORITY_TARGET",
        "evidence_tier": "T1_PRIMARY_OFFICIAL",
        "evidence_status": "VERIFIED_SOURCE",
        "source_fact": "The source documents a current product-specific behavior.",
        "context_conditions": ["Applies to the documented version only."],
        "scope": "Godot version-specific documentation",
        "sample_or_method": "Official release documentation",
        "platform_or_medium": "Godot Engine",
        "commercial_or_vendor_interest": "Official product documentation",
        "license_or_copying_notes": "Store a short paraphrase and URL only.",
        "base_overlap": "PARTIAL",
        "existing_owner": "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
        "decision_delta": "Add a bounded freshness check to an evidence record.",
        "smallest_change_candidate": "Generated evidence record only.",
        "disposition": "ADAPT",
        "work_disposition": "EVIDENCE_ONLY_UPDATE",
        "claim_ceiling": "Product documentation is not a universal engine rule.",
        "counterevidence": ["Other engine versions may differ."],
        "validation_artifact": "Recheck the exact release documentation before project use.",
        "rollback_or_discard_condition": "Discard when the version is no longer relevant.",
    }
    row.update(overrides)
    return row


def analysis_packet(**overrides: object) -> dict[str, object]:
    packet: dict[str, object] = {
        "run_date": "2026-08-14",
        "scanned_sources": ["godot"],
        "candidates": [candidate()],
        "new_source_candidates": [],
        "no_change_reason": "",
    }
    packet.update(overrides)
    return packet


def review_packet(**overrides: object) -> dict[str, object]:
    packet: dict[str, object] = {
        "run_date": "2026-08-14",
        "findings": [],
        "approved_candidate_ids": ["candidate-1"],
        "blocked_candidate_ids": [],
        "url_verification_passed": True,
        "claim_ceiling_passed": True,
        "protected_semantic_change": False,
        "result": "AUTO_MERGE_ELIGIBLE",
    }
    packet.update(overrides)
    return packet


def operations_ledger() -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "fixture",
        "sources": [{
            "source_id": "godot",
            "name": "Godot",
            "domains": ["GAME_DEVELOPMENT"],
            "roles": ["AUTHORITY_TARGET"],
            "recommended_cadence": "daily-or-weekly",
            "scan_surfaces": ["blog"],
            "last_successful_scan_at": "2026-08-12",
            "last_material_candidate_at": None,
            "last_base_contribution_at": "2026-08-01",
            "last_base_contribution_ref": "abc123",
            "material_candidate_count_since_tracking_start": 1,
            "base_contribution_count_since_tracking_start": 1,
            "status": "ACTIVE",
        }],
    }


class PeriodicSourceAnalysisAutoMergeTests(unittest.TestCase):
    def test_request_builders_use_web_grounding_strict_schemas_and_no_storage(self) -> None:
        self.assertFalse(ANALYSIS_SCHEMA["additionalProperties"])
        self.assertFalse(REVIEW_SCHEMA["additionalProperties"])
        research = build_research_request(SELECTED, RUN_DATE, model="gpt-5.6-terra")
        self.assertEqual([{"type": "web_search"}], research["tools"])
        self.assertIn("web_search_call.action.sources", research["include"])
        self.assertIs(False, research["store"])
        self.assertIn("untrusted data", json.dumps(research["input"]).lower())
        context = build_context_request("digest", {ARTICLE_URL}, SELECTED, RUN_DATE)
        review = build_review_request(analysis_packet(), {ARTICLE_URL}, RUN_DATE)
        for payload in (context, review):
            self.assertIs(False, payload["store"])
            self.assertNotIn("tools", payload)
            self.assertEqual("json_schema", payload["text"]["format"]["type"])
            self.assertIs(True, payload["text"]["format"]["strict"])

    def test_source_and_output_extraction_fail_closed(self) -> None:
        response = {"output": [
            {"type": "web_search_call", "action": {"sources": [
                {"url": ARTICLE_URL + "#section"}, {"url": NEW_SOURCE_URL}
            ]}},
            {"type": "message", "content": [{"type": "output_text", "text": "digest",
                "annotations": [{"type": "url_citation", "url": ARTICLE_URL}]}]},
        ]}
        self.assertEqual({ARTICLE_URL, NEW_SOURCE_URL}, collect_source_urls(response))
        self.assertEqual("digest", extract_output_text(response))
        with self.assertRaisesRegex(AnalysisBlocked, "BLOCKED_RESEARCH_SOURCES"):
            collect_source_urls({"output": []})
        with self.assertRaisesRegex(AnalysisBlocked, "BLOCKED_RESEARCH_SOURCES"):
            collect_source_urls({"output": [{"type": "web_search_call", "action": {
                "sources": [{"url": "http://unsafe.example"}]}}]})
        with self.assertRaisesRegex(AnalysisBlocked, "BLOCKED_MODEL_REFUSAL"):
            extract_output_text({"output": [{"type": "message", "content": [
                {"type": "refusal", "refusal": "no"}]}]})

    def test_context_packet_accepts_only_selected_ids_exact_urls_and_current_dates(self) -> None:
        valid = validate_analysis_packet(
            analysis_packet(), {ARTICLE_URL}, {"godot"}, RUN_DATE
        )
        self.assertEqual("candidate-1", valid["candidates"][0]["candidate_id"])
        invalid = (
            candidate(original_url="https://foreign.example/a"),
            candidate(source_id="steamworks"),
            candidate(checked_at="2026-08-13"),
            candidate(published_or_updated_at="2026-08-15"),
            candidate(evidence_tier="T0_MAGIC"),
            candidate(work_disposition="ARBITRARY_PATCH"),
            candidate(claim_ceiling=""),
            candidate(counterevidence=[]),
            candidate(validation_artifact=""),
            candidate(rollback_or_discard_condition=""),
        )
        for row in invalid:
            with self.subTest(row=row):
                with self.assertRaises(AnalysisBlocked):
                    validate_analysis_packet(
                        analysis_packet(candidates=[row]),
                        {ARTICLE_URL}, {"godot"}, RUN_DATE,
                    )
        with self.assertRaisesRegex(AnalysisBlocked, "BLOCKED_CONTEXT_SCHEMA"):
            validate_analysis_packet(
                analysis_packet(candidates=[], no_change_reason=""),
                {ARTICLE_URL}, {"godot"}, RUN_DATE,
            )

    def test_review_and_deterministic_gate_block_p0_p1_protected_or_high_risk_work(self) -> None:
        analysis = validate_analysis_packet(
            analysis_packet(), {ARTICLE_URL}, {"godot"}, RUN_DATE
        )
        review = validate_review_packet(review_packet(), {"candidate-1"}, RUN_DATE)
        self.assertEqual(["candidate-1"], deterministic_gate(analysis, review, {ARTICLE_URL}))
        finding = {
            "finding_id": "finding-1", "severity": "P1",
            "candidate_id": "candidate-1", "category": "OVERGENERALIZATION",
            "claim": "The claim exceeds the source.", "validated": True,
            "decision": "MUST_FIX",
        }
        failures = (
            review_packet(findings=[finding]),
            review_packet(protected_semantic_change=True),
            review_packet(result="AUTO_MERGE_BLOCKED"),
            review_packet(approved_candidate_ids=[]),
            review_packet(url_verification_passed=False),
            review_packet(claim_ceiling_passed=False),
        )
        for packet in failures:
            checked = validate_review_packet(packet, {"candidate-1"}, RUN_DATE)
            with self.assertRaises(AnalysisBlocked):
                deterministic_gate(analysis, checked, {ARTICLE_URL})
        high_risk = validate_analysis_packet(
            analysis_packet(candidates=[candidate(work_disposition="RULE_OR_BCP_CANDIDATE")]),
            {ARTICLE_URL}, {"godot"}, RUN_DATE,
        )
        with self.assertRaisesRegex(AnalysisBlocked, "BLOCKED_PROTECTED_SEMANTIC_CHANGE"):
            deterministic_gate(high_risk, review, {ARTICLE_URL})

    def test_renderer_and_ledgers_are_deterministic_bounded_and_truthful(self) -> None:
        new_site = {
            "candidate_id": "new-source-1", "name": "New Research Source",
            "domain": "GAME_DEVELOPMENT", "url": NEW_SOURCE_URL,
            "source_role": "PROFESSIONAL_PRACTICE",
            "reason": "Publishes directly relevant primary-linked research.",
        }
        analysis = analysis_packet(new_source_candidates=[new_site])
        markdown = render_scan_markdown(
            analysis, review_packet(), ["candidate-1"],
            model="gpt-5.6-terra", run_id="run-123",
        )
        self.assertIn(f"[Current Godot research note]({ARTICLE_URL})", markdown)
        self.assertIn(f"[New Research Source]({NEW_SOURCE_URL})", markdown)
        for token in ("T1_PRIMARY_OFFICIAL", "claim ceiling", "counterevidence",
                      "validation artifact", "rollback", "AUTO_MERGE_ELIGIBLE",
                      "UNVERIFIED_DISCOVERY"):
            self.assertIn(token.lower(), markdown.lower())
        candidate_ledger = {
            "schema_version": 1,
            "ledger_role": "periodic-unverified-source-candidates",
            "authority": "UNVERIFIED_DISCOVERY_ONLY",
            "candidates": [],
        }
        twice = update_candidate_ledger(
            update_candidate_ledger(candidate_ledger, [new_site], RUN_DATE),
            [new_site], RUN_DATE,
        )
        self.assertEqual(1, len(twice["candidates"]))
        self.assertEqual(2, twice["candidates"][0]["seen_count"])
        self.assertEqual("UNVERIFIED_DISCOVERY", twice["candidates"][0]["status"])
        updated = update_operations_ledger(
            operations_ledger(), {"godot"}, [candidate()], RUN_DATE
        )
        row = updated["sources"][0]
        self.assertEqual("2026-08-14", row["last_successful_scan_at"])
        self.assertEqual("2026-08-14", row["last_material_candidate_at"])
        self.assertEqual(2, row["material_candidate_count_since_tracking_start"])
        self.assertEqual("2026-08-01", row["last_base_contribution_at"])
        self.assertEqual("abc123", row["last_base_contribution_ref"])


if __name__ == "__main__":
    unittest.main()
