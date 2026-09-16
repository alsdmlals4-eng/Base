from __future__ import annotations

import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

from tools.periodic_source_scan_queue import (
    ISSUE_MARKER,
    ISSUE_TITLE,
    load_ledger,
    parse_iso_date,
    render_issue_body,
    select_due_sources,
    source_is_due,
)


ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "AGENTS.md"
CI_COST_POLICY = ROOT / "docs" / "CI_EXECUTION_COST_POLICY.md"
QUEUE_WORKFLOW = ROOT / ".github" / "workflows" / "periodic-source-scan-queue.yml"
EVIDENCE_WORKFLOW = ROOT / ".github" / "workflows" / "validate-evidence-knowledge.yml"
WATCHLIST = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md"
QUEUE_GUIDE = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_SCAN_QUEUE.md"
RADAR = ROOT / "docs" / "knowledge" / "game-development" / "NARRATIVE_WORLD_CHARACTER_SOURCE_RADAR.md"
TUTORIAL = ROOT / "docs" / "knowledge" / "game-development" / "TUTORIAL_AND_ONBOARDING_DESIGN_GUIDE.md"
CHECKPOINT = ROOT / "docs" / "knowledge" / "game-development" / "SOURCE_SCAN_CHECKPOINT_2026-08-14.md"
LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
CANDIDATE_LEDGER = ROOT / "docs" / "knowledge" / "game-development" / "PERIODIC_SOURCE_CANDIDATE_LEDGER.json"
SCAN_README = ROOT / "docs" / "knowledge" / "game-development" / "source-scans" / "README.md"


def source(
    source_id: str,
    cadence: str,
    last_scan: str | None,
    *,
    status: str = "ACTIVE",
) -> dict[str, object]:
    return {
        "source_id": source_id,
        "name": source_id.replace("-", " ").title(),
        "domains": ["FICTION_AND_INTERACTIVE_NARRATIVE"],
        "roles": ["PROFESSIONAL_PRACTICE"],
        "recommended_cadence": cadence,
        "scan_surfaces": ["recent articles", "linked originals"],
        "last_successful_scan_at": last_scan,
        "last_material_candidate_at": None,
        "last_base_contribution_at": None,
        "last_base_contribution_ref": None,
        "material_candidate_count_since_tracking_start": 0,
        "base_contribution_count_since_tracking_start": 0,
        "status": status,
    }


def payload(sources: list[dict[str, object]]) -> dict[str, object]:
    return {
        "schema_version": 1,
        "ledger_role": "periodic-source-operational-state",
        "tracking_started_at": "2026-08-11",
        "watchlist_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        "state_semantics": "test fixture",
        "sources": sources,
    }


class PeriodicSourceScanQueueTests(unittest.TestCase):
    def test_date_parser_accepts_null_and_strict_iso_date(self) -> None:
        self.assertIsNone(parse_iso_date(None))
        self.assertEqual(parse_iso_date("2026-08-14"), date(2026, 8, 14))
        for invalid in ("", "2026/08/14", "14-08-2026", 20260814, True):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    parse_iso_date(invalid)

    def test_due_policy_matches_daily_and_longer_watchlist_cadences(self) -> None:
        today = date(2026, 8, 14)
        cases = (
            ("daily-or-weekly", "2026-08-13", True),
            ("daily-or-weekly", "2026-08-14", False),
            ("weekly", "2026-08-07", True),
            ("weekly", "2026-08-08", False),
            ("monthly-or-on-demand", "2026-07-15", True),
            ("monthly-or-on-demand", "2026-07-16", False),
            ("quarterly-or-when-relevant", "2026-05-16", True),
            ("quarterly-or-when-relevant", "2026-05-17", False),
        )
        for cadence, last_scan, expected in cases:
            with self.subTest(cadence=cadence, last_scan=last_scan):
                self.assertEqual(
                    source_is_due(source("candidate", cadence, last_scan), today),
                    expected,
                )

    def test_null_scan_is_due_and_inactive_sources_are_excluded(self) -> None:
        today = date(2026, 8, 14)
        ledger = payload([
            source("never-scanned", "weekly", None),
            source("inactive", "weekly", None, status="RETIRED"),
        ])
        selected = select_due_sources(ledger, today)
        self.assertEqual([item["source_id"] for item in selected], ["never-scanned"])

    def test_due_source_order_prioritizes_never_scanned_then_most_overdue(self) -> None:
        today = date(2026, 8, 14)
        ledger = payload([
            source("daily-recent", "daily-or-weekly", "2026-08-13"),
            source("weekly-overdue", "weekly", "2026-08-01"),
            source("monthly-overdue", "monthly-or-on-demand", "2026-06-01"),
            source("never-b", "quarterly-or-when-relevant", None),
            source("never-a", "daily-or-weekly", None),
        ])
        selected = select_due_sources(ledger, today)
        self.assertEqual(
            [item["source_id"] for item in selected],
            ["never-a", "never-b", "monthly-overdue", "weekly-overdue", "daily-recent"],
        )

    def test_invalid_cadence_date_and_future_scan_fail_closed(self) -> None:
        today = date(2026, 8, 14)
        for item in (
            source("unknown", "hourly", None),
            source("bad-date", "weekly", "not-a-date"),
            source("future", "weekly", "2026-08-15"),
        ):
            with self.subTest(source_id=item["source_id"]):
                with self.assertRaises(ValueError):
                    source_is_due(item, today)

    def test_load_ledger_requires_schema_unique_ids_and_known_cadence(self) -> None:
        fixtures = (
            ({"schema_version": 2, "sources": []}, "schema_version"),
            (payload([source("duplicate", "weekly", None), source("duplicate", "weekly", None)]), "duplicate"),
            (payload([source("unknown", "hourly", None)]), "cadence"),
        )
        for data, expected_message in fixtures:
            with self.subTest(expected_message=expected_message):
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / "ledger.json"
                    path.write_text(json.dumps(data), encoding="utf-8")
                    with self.assertRaisesRegex(ValueError, expected_message):
                        load_ledger(path)

    def test_issue_body_is_deterministic_and_preserves_evidence_boundaries(self) -> None:
        today = date(2026, 8, 14)
        ledger = payload([
            source("daily-source", "daily-or-weekly", "2026-08-13"),
            source("monthly-source", "monthly-or-on-demand", "2026-07-01"),
            source("fresh-source", "weekly", "2026-08-13"),
        ])
        first = render_issue_body(ledger, today)
        self.assertEqual(first, render_issue_body(ledger, today))
        self.assertTrue(first.startswith(ISSUE_MARKER))
        self.assertEqual(ISSUE_TITLE, "[Periodic Source Scan Queue]")
        for required in (
            "UNVERIFIED_DISCOVERY", "2026-08-14", "daily-source", "monthly-source",
            "기존 Source의 새 글·수정 글 확인", "신규 Source 사이트 탐색",
            "original source backtrace", "published_or_updated_at",
            "current_base_owner", "current_project_consumer", "claim ceiling",
            "validation artifact", "rollback_or_discard_condition",
            "ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID",
            "Queue 완료 != Ledger scan 완료",
        ):
            self.assertIn(required, first)
        self.assertNotIn("fresh-source", first)

    def test_base_zero_incremental_cost_policy_is_always_on_and_uses_existing_cost_owner(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        self.assertTrue(CI_COST_POLICY.is_file())
        for required in (
            "ZERO_INCREMENTAL_COST_REQUIRED",
            "COST_GATE_BLOCKED",
            "pay-as-you-go",
            "separately metered",
            "docs/CI_EXECUTION_COST_POLICY.md",
        ):
            self.assertIn(required, agents)
        ci_policy = CI_COST_POLICY.read_text(encoding="utf-8")
        for required in ("REMOTE_CI", "LOCAL_FALLBACK", "비용"):
            self.assertIn(required, ci_policy)

    def test_workflow_runs_daily_as_zero_cost_queue_preparation_only(self) -> None:
        self.assertTrue(QUEUE_WORKFLOW.is_file())
        workflow = QUEUE_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            'cron: "0 18 * * *"', 'timezone: "Asia/Seoul"', "workflow_dispatch:",
            "issues: write", "tools/periodic_source_scan_queue.py",
            "periodic-source-scan-queue.md",
            "ZERO_INCREMENTAL_COST_QUEUE_PREP", "AWAITING_CHATGPT_REVIEW",
            "USER_DIRECTED_CHATGPT_REVIEW",
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
        ):
            self.assertIn(required, workflow)
        for forbidden in (
            "timeout-minutes", "pull_request_target", "git push origin HEAD:main",
            "git push --force", "--admin", "--auto",
            "BLOCKED_ACTIVE_PR_GUARD", "BLOCKED_ACTIVE_PR_GUARD_QUERY",
            "SOURCE_SCAN_BATCH_SIZE",
            "actions: write", "contents: write", "pull-requests: write",
            "automation/source-scan-", "gh run watch", "reviewThreads",
            "validation_level=full", "--squash", "--match-head-commit",
        ):
            self.assertNotIn(forbidden, workflow)

    def test_first_scan_sources_and_minimal_absorptions_are_connected(self) -> None:
        self.assertTrue(CHECKPOINT.is_file())
        radar = RADAR.read_text(encoding="utf-8")
        tutorial = TUTORIAL.read_text(encoding="utf-8")
        checkpoint = CHECKPOINT.read_text(encoding="utf-8")
        queue_guide = QUEUE_GUIDE.read_text(encoding="utf-8")
        for source_name in (
            "DiGRA Digital Library", "Game Studies", "MCLC Resource Center",
            "Library of Congress Web Cultures Web Archive", "Data & Society",
        ):
            self.assertIn(source_name, radar)
            self.assertIn(source_name, checkpoint)
        for required in (
            "story_holon_local_coherence", "shared_storyworld_contribution",
            "fragment_inference_burden", "optional_fragment_redundancy_and_recovery",
            "wuxia_xianxia_cultivation_boundary", "cosmology_and_technical_practice",
            "translation_and_cross_cultural_boundary",
            "platform_commercialization_and_governance_stage",
            "native_symbol_system_and_recontextualization",
        ):
            self.assertIn(required, radar)
        for required in (
            "prior_game_expertise", "expertise_measure", "novice_expert_segment",
            "expertise_by_onboarding_interaction",
        ):
            self.assertIn(required, tutorial)
        for required in (
            "UNVERIFIED_DISCOVERY", "Queue 완료 != scan 완료", "새 글·수정 글",
            "신규 Source 사이트", "Issue 갱신 != Ledger timestamp 갱신",
            "기존 owner", "자동 Canon", "자동 PR", "ZERO_INCREMENTAL_COST_REQUIRED",
            "AWAITING_CHATGPT_REVIEW",
        ):
            self.assertIn(required, queue_guide)

    def test_daily_analysis_records_and_pending_candidate_ledger_are_discoverable(self) -> None:
        self.assertTrue(CANDIDATE_LEDGER.is_file())
        self.assertTrue(SCAN_README.is_file())
        candidate_data = json.loads(CANDIDATE_LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(1, candidate_data["schema_version"])
        self.assertEqual("UNVERIFIED_DISCOVERY_ONLY", candidate_data["authority"])
        self.assertIsInstance(candidate_data["candidates"], list)
        scan_readme = SCAN_README.read_text(encoding="utf-8")
        for required in (
            "T6", "원출처", "claim ceiling", "counterevidence",
            "rollback", "article body", "immutable",
        ):
            self.assertIn(required.lower(), scan_readme.lower())

    def test_evidence_workflow_executes_and_archives_analysis_contract(self) -> None:
        workflow = EVIDENCE_WORKFLOW.read_text(encoding="utf-8")
        for required in (
            '"tools/periodic_source_scan_queue.py"',
            '"tools/periodic_source_analysis.py"',
            '"tests/test_periodic_source_scan_queue.py"',
            '"tests/test_periodic_source_analysis_auto_merge.py"',
            '\".github/workflows/periodic-source-scan-queue.yml\"',
            "docs/knowledge/game-development/PERIODIC_SOURCE_CANDIDATE_LEDGER.json",
            "docs/knowledge/game-development/source-scans/README.md",
            "tools/periodic_source_analysis.py",
            "tests/test_periodic_source_analysis_auto_merge.py",
        ):
            self.assertIn(required, workflow)

    def test_repository_ledger_remains_the_only_canonical_operational_state(self) -> None:
        self.assertTrue(LEDGER.is_file())
        watchlist = WATCHLIST.read_text(encoding="utf-8")
        queue_workflow = QUEUE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("고유 Source family 하나로 추적", watchlist)
        self.assertIn("PERIODIC_SOURCE_OPERATIONS_LEDGER.json", watchlist)
        self.assertIn("tools/periodic_source_scan_queue.py", queue_workflow)
        self.assertNotIn('echo "last_successful_scan_at', queue_workflow)


class YozmSourceScanIntegrationTests(unittest.TestCase):
    """Exercise the real queue consumer; profile checks are documentation contracts."""

    def yozm_source(self) -> dict[str, object]:
        rows = [row for row in load_ledger(LEDGER)["sources"] if row["source_id"] == "yozm-it"]
        self.assertEqual(1, len(rows), "register exactly one yozm-it Source family")
        return dict(rows[0])

    def yozm_profile(self) -> str:
        text = WATCHLIST.read_text(encoding="utf-8")
        heading = "### 3.7 요즘IT"
        self.assertTrue(heading in text, "missing 요즘IT discovery profile in the existing Watchlist owner")
        return text.split(heading, 1)[1].split("\n## 4.", 1)[0]

    def test_yozm_is_one_active_discovery_family_not_a_product_authority(self) -> None:
        row = self.yozm_source()
        self.assertEqual("ACTIVE", row["status"])
        self.assertEqual(["DISCOVERY_FEED"], row["roles"])
        self.assertTrue(
            {"PROMPT_AND_AGENT_WORKFLOW", "SKILL_AUTHORING_AND_EVOLUTION", "CODE_ENGINEERING"}
            .issubset(set(row["domains"]))
        )

    def test_yozm_registered_cadence_rechecks_after_one_day(self) -> None:
        row = self.yozm_source()
        self.assertEqual("daily-or-weekly", row["recommended_cadence"])
        row["last_successful_scan_at"] = "2026-08-30"
        self.assertFalse(source_is_due(row, date(2026, 8, 30)))
        self.assertTrue(source_is_due(row, date(2026, 8, 31)))
        row["status"] = "RETIRED"
        self.assertFalse(source_is_due(row, date(2026, 8, 31)))

    def test_yozm_real_queue_covers_both_topic_surfaces_without_writing_scan_state(self) -> None:
        original_bytes = LEDGER.read_bytes()
        row = self.yozm_source()
        row["last_successful_scan_at"] = None
        ledger = payload([row])
        before = json.dumps(ledger, ensure_ascii=False, sort_keys=True)
        body = render_issue_body(ledger, date(2026, 8, 31))
        self.assertEqual(1, body.count("| `yozm-it` |"))
        for required in (
            "https://yozm.wishket.com/", "오늘의 토픽", "주간 인기",
            "latest", "article body", "linked original sources",
            "PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md", "UNVERIFIED_DISCOVERY",
            "queue_writes_ledger_state: false", "queue_writes_project_canon: false",
        ):
            self.assertIn(required, body)
        self.assertEqual(before, json.dumps(ledger, ensure_ascii=False, sort_keys=True))
        self.assertEqual(original_bytes, LEDGER.read_bytes())

    def test_yozm_profile_keeps_cache_freshness_and_article_identity_explicit(self) -> None:
        profile = self.yozm_profile()
        for required in (
            "displayed_week_label", "checked_at", "PARTIAL_INDEX_REVIEW",
            "BLOCKED_UNVERIFIED", "last_successful_scan_at", "canonical_article_id",
            "published_or_updated_at", "SOURCE_CONTEXT_PACKET",
        ):
            self.assertTrue(required in profile, f"YoZm profile missing freshness/identity contract: {required}")

    def test_yozm_profile_routes_reuse_to_existing_owners_and_falsifiable_validation(self) -> None:
        profile = self.yozm_profile()
        for required in (
            "ORIGINAL_SOURCE_BACKTRACE", "REVERSE_ENGINEERING_REUSE_PIPELINE.md",
            "REUSABLE_MODULE_REGISTRY.md", "existing_owner", "current_project_consumer",
            "falsification_test", "validation_artifact", "rollback_or_discard_condition",
            "ADOPT", "ADAPT", "REFERENCE_ONLY",
        ):
            self.assertTrue(required in profile, f"YoZm profile missing reuse/verification contract: {required}")

    def test_yozm_profile_does_not_claim_autonomous_research_or_automatic_adoption(self) -> None:
        profile = self.yozm_profile()
        for required in (
            "AWAITING_CHATGPT_REVIEW", "USER_DIRECTED_CHATGPT_REVIEW",
            "SCAN_STATE_BATCH", "NO_CHANGE", "외부 콘텐츠는 데이터",
            "유료 API", "프로젝트 정본", "별도 실행 증거",
        ):
            self.assertTrue(required in profile, f"YoZm profile missing execution/authority boundary: {required}")


class PeriodicQueueRoutingSafetyTests(unittest.TestCase):
    """Deterministic destination checks; these are not live GitHub review evidence."""

    def module(self):
        from tools import periodic_source_scan_queue
        return periodic_source_scan_queue

    def normalizer(self):
        fn = getattr(self.module(), "normalize_base_repository", None)
        self.assertTrue(callable(fn), "missing fail-closed Base repository normalization")
        return fn

    def resolver(self):
        fn = getattr(self.module(), "resolve_queue_issue", None)
        self.assertTrue(callable(fn), "missing stable-marker queue resolution")
        return fn

    def issue(self, number=647, *, title=ISSUE_TITLE, marker=True, state="OPEN"):
        return {"number": number, "title": title, "body": ISSUE_MARKER if marker else "unrelated", "state": state}

    def test_base_address_normalizes_only_equivalent_canonical_forms(self) -> None:
        normalize = self.normalizer()
        for value in (
            "alsdmlals4-eng/Base", "ALSDMLALS4-ENG/base", " alsdmlals4-eng/Base ",
            "https://github.com/alsdmlals4-eng/Base/", "https://github.com/alsdmlals4-eng/Base.git",
        ):
            with self.subTest(value=value):
                self.assertEqual("alsdmlals4-eng/Base", normalize(value))

    def test_base_address_rejects_wrong_owner_and_ambiguous_url_without_guessing(self) -> None:
        normalize = self.normalizer()
        for value in (
            "", "other/Base", "alsdmlals4-eng/Bsae", "http://github.com/alsdmlals4-eng/Base",
            "https://github.com.evil.invalid/alsdmlals4-eng/Base", "https://x@github.com/alsdmlals4-eng/Base",
            "https://github.com/alsdmlals4-eng/Base?repo=other", "https://github.com/alsdmlals4-eng/Base#main",
            "https://github.com/alsdmlals4-eng/Base/pull/647", "alsdmlals4-eng/Base.git/extra",
        ):
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "BASE_REPOSITORY_MISMATCH"):
                    normalize(value)

    def test_queue_resolution_uses_identity_not_historical_issue_number(self) -> None:
        resolve = self.resolver()
        self.assertEqual(888, resolve([
            self.issue(334, state="CLOSED"),
            self.issue(777, title="Other work", marker=False), self.issue(888),
        ]))
        self.assertIsNone(resolve([]))

    def test_queue_resolution_blocks_duplicate_or_lookalike_issue(self) -> None:
        resolve = self.resolver()
        for rows in (
            [self.issue(647), self.issue(888)], [self.issue(marker=False)],
            [self.issue(title="Renamed source queue")], [self.issue(number=True)],
        ):
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(ValueError, "QUEUE_"):
                    resolve(rows)

    def test_queue_resolution_does_not_treat_truncated_or_malformed_listing_as_empty(self) -> None:
        resolve = self.resolver()
        for rows in (None, {}, ["bad"], [self.issue(i + 1, title="Other", marker=False) for i in range(100)]):
            with self.subTest(rows_type=type(rows).__name__):
                with self.assertRaisesRegex(ValueError, "QUEUE_"):
                    resolve(rows)

    def test_every_source_domain_gets_the_same_full_cycle_handoff_without_success_claims(self) -> None:
        domains = (
            "GAME_DEVELOPMENT", "CODE_ENGINEERING", "PROMPT_AND_AGENT_WORKFLOW",
            "SKILL_AUTHORING_AND_EVOLUTION", "FICTION_AND_INTERACTIVE_NARRATIVE", "YOUTUBE_AND_VIDEO_EDITING",
        )
        rows = [source(f"domain-{i}", "weekly", None) for i in range(len(domains))]
        for row, domain in zip(rows, domains):
            row["domains"] = [domain]
        ledger = payload(rows)
        before = json.dumps(ledger, sort_keys=True)
        body = render_issue_body(ledger, date(2026, 8, 31))
        for required in (
            "https://github.com/alsdmlals4-eng/Base", "1295870270", "SOURCE_REVIEW_FULL_CYCLE",
            "PERIODIC_SOURCE_SCAN_QUEUE.md", "REVERSE_ENGINEERING_REUSE_PIPELINE.md",
            "FULL_LOOP_COUNT_MINIMUM: 5", "FULL_LOOP_IS_NOT_A_REVIEW_LENS",
            "SOURCE_SCAN_AUTO_MERGE_GATE", "POSTMERGE_READBACK", "ACTUAL_SOURCE_REVIEW_RECEIPT",
            "review_execution: NOT_RUN", "merge_execution: NOT_RUN", "NO_CHANGE",
        ):
            self.assertIn(required, body)
        for row in rows:
            self.assertEqual(1, body.count(f"| `{row['source_id']}` |"))
        self.assertEqual(before, json.dumps(ledger, sort_keys=True))

    def test_queue_guide_uses_discovered_issue_and_explicit_external_scheduler_ceiling(self) -> None:
        text = QUEUE_GUIDE.read_text(encoding="utf-8")
        self.assertNotIn("Issue #334의 comment", text)
        for required in (
            ISSUE_MARKER, "SOURCE_REVIEW_FULL_CYCLE", "SCHEDULER_CONFIG_NOT_EXPOSED",
            "FULL_LOOP_COUNT_MINIMUM: 5", "POSTMERGE_READBACK", "reviewed_head_sha",
            "REVERSE_ENGINEERING_REUSE_PIPELINE.md", "REUSABLE_MODULE_REGISTRY.md",
            "연결된 GitHub", "독립 검토", "NO_CHANGE", "WORKSPACE",
        ):
            self.assertIn(required, text)

    def test_source_configuration_changes_refresh_the_existing_scheduled_queue(self) -> None:
        workflow = QUEUE_WORKFLOW.read_text(encoding="utf-8")
        for path in (
            "docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
            "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
        ):
            self.assertIn(f'"{path}"', workflow)


class PeriodicQueueRunnerSafetyTests(unittest.TestCase):
    """Execute the actual POSIX wrapper with only its remote gh boundary replaced."""

    def run_wrapper(self, *, repo="alsdmlals4-eng/Base", issues=None, repository_id=1295870270, github_repository="alsdmlals4-eng/Base", readback_mismatch=False, write_exit=0):
        import os
        import shutil
        import subprocess
        import sys
        if os.name != "posix" or not shutil.which("bash"):
            self.skipTest("POSIX queue wrapper is owned by the ubuntu-latest scheduler")
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "tools").mkdir()
            for name in ("periodic_source_scan_queue.py", "run_periodic_source_scan_queue.sh"):
                shutil.copy2(ROOT / "tools" / name, workspace / "tools" / name)
            ledger_path = workspace / "docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json"
            ledger_path.parent.mkdir(parents=True)
            ledger_path.write_text(json.dumps(payload([source("test", "weekly", None)])), encoding="utf-8")
            manifest = workspace / "docs/operations/BASE_PARTITION_MANIFEST.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(json.dumps({"contract_id": "BASE_PARTITION_OPERATING_MODEL_V1", "parts": []}), encoding="utf-8")
            bin_dir = workspace / "bin"
            bin_dir.mkdir()
            (bin_dir / "python").symlink_to(sys.executable)
            fake = bin_dir / "gh"
            fake.write_text('''#!/usr/bin/env python
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
with Path("gh-calls.jsonl").open("a") as log:
    log.write(json.dumps(args) + "\\n")
if args[:1] == ["api"]:
    print(os.environ["FIXTURE_REPOSITORY_ID"])
elif args[:2] == ["issue", "list"]:
    rows = json.loads(os.environ["FIXTURE_ISSUES"])
    if "--jq" in args:
        print("\\n".join(str(row["number"]) for row in rows))
    else:
        print(json.dumps(rows))
elif args[:2] in (["issue", "edit"], ["issue", "create"]):
    if os.environ["FIXTURE_WRITE_EXIT"] != "0":
        raise SystemExit(int(os.environ["FIXTURE_WRITE_EXIT"]))
    Path("published-body.txt").write_text(Path(args[args.index("--body-file") + 1]).read_text())
    print("https://github.com/alsdmlals4-eng/Base/issues/647")
elif args[:2] == ["issue", "view"]:
    body = Path("published-body.txt").read_text()
    if os.environ["FIXTURE_READBACK_MISMATCH"] == "1":
        body = "different body"
    print(json.dumps({"title": "[Periodic Source Scan Queue]", "body": body, "state": "OPEN"}))
else:
    raise SystemExit("unexpected gh call: " + repr(args))
''', encoding="utf-8")
            fake.chmod(0o755)
            env = dict(os.environ, PATH=str(bin_dir) + os.pathsep + os.environ.get("PATH", ""), GH_TOKEN="fixture-not-a-token", GH_REPO=repo,
                       GITHUB_REPOSITORY=github_repository, FIXTURE_REPOSITORY_ID=str(repository_id),
                       FIXTURE_ISSUES=json.dumps(issues or []), FIXTURE_READBACK_MISMATCH="1" if readback_mismatch else "0", FIXTURE_WRITE_EXIT=str(write_exit))
            (workspace / "source-analysis-status.json").write_text(json.dumps({"state": "AWAITING_CHATGPT_REVIEW", "stale": True}), encoding="utf-8")
            completed = subprocess.run(["bash", "tools/run_periodic_source_scan_queue.sh"], cwd=workspace, env=env, capture_output=True, text=True, timeout=20)
            log = workspace / "gh-calls.jsonl"
            calls = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            report = workspace / "queue-final.md"
            self.last_status = json.loads((workspace / "source-analysis-status.json").read_text(encoding="utf-8"))
            return completed, calls, report.read_text(encoding="utf-8") if report.exists() else ""

    def test_wrapper_rejects_wrong_repository_before_any_remote_call(self) -> None:
        run, calls, _ = self.run_wrapper(repo="someone-else/Base")
        self.assertNotEqual(0, run.returncode)
        self.assertEqual([], calls)

    def test_wrapper_rejects_repository_identity_drift_before_issue_write(self) -> None:
        for options in ({"repository_id": 1}, {"github_repository": "someone-else/Base"}):
            with self.subTest(options=options):
                run, calls, _ = self.run_wrapper(**options)
                self.assertNotEqual(0, run.returncode)
                self.assertFalse(any(call[:2] in (["issue", "edit"], ["issue", "create"]) for call in calls))

    def test_wrapper_blocks_duplicate_queue_instead_of_editing_the_first(self) -> None:
        rows = [{"number": n, "title": ISSUE_TITLE, "body": ISSUE_MARKER, "state": "OPEN"} for n in (647, 888)]
        run, calls, _ = self.run_wrapper(issues=rows)
        self.assertNotEqual(0, run.returncode)
        self.assertFalse(any(call[:2] in (["issue", "edit"], ["issue", "create"]) for call in calls))

    def test_wrapper_normalizes_url_and_publishes_full_cycle_pending_not_merge_success(self) -> None:
        rows = [{"number": 888, "title": ISSUE_TITLE, "body": ISSUE_MARKER, "state": "OPEN"}]
        run, calls, body = self.run_wrapper(repo="https://github.com/alsdmlals4-eng/Base/", issues=rows)
        self.assertEqual(0, run.returncode, run.stderr)
        writes = [call for call in calls if call[:2] == ["issue", "edit"]]
        self.assertEqual(1, len(writes))
        self.assertEqual("888", writes[0][2])
        self.assertEqual("alsdmlals4-eng/Base", writes[0][writes[0].index("--repo") + 1])
        self.assertIn("SOURCE_REVIEW_FULL_CYCLE", body)
        self.assertIn("AWAITING_CHATGPT_REVIEW", body)
        self.assertIn("merge_execution: NOT_RUN", body)


    def test_wrapper_requires_destination_readback_after_publication(self) -> None:
        rows = [{"number": 647, "title": ISSUE_TITLE, "body": ISSUE_MARKER, "state": "OPEN"}]
        run, calls, _ = self.run_wrapper(issues=rows, readback_mismatch=True)
        self.assertNotEqual(0, run.returncode)
        self.assertTrue(any(call[:2] == ["issue", "view"] for call in calls))
        self.assertNotIn("Source Queue prepared:", run.stdout)

    def test_wrapper_stops_on_remote_publication_failure(self) -> None:
        run, calls, _ = self.run_wrapper(write_exit=1)
        self.assertNotEqual(0, run.returncode)
        self.assertNotIn("Source Queue prepared:", run.stdout)

    def test_wrapper_creates_only_when_complete_listing_has_no_queue_and_reads_it_back(self) -> None:
        run, calls, body = self.run_wrapper(issues=[])
        self.assertEqual(0, run.returncode, run.stderr)
        self.assertEqual(1, sum(call[:2] == ["issue", "create"] for call in calls))
        self.assertEqual(1, sum(call[:2] == ["issue", "view"] for call in calls))
        self.assertIn("merge_execution: NOT_RUN", body)


    def test_failed_retry_cannot_leave_a_previous_success_receipt_current(self) -> None:
        run, _, _ = self.run_wrapper(write_exit=1)
        self.assertNotEqual(0, run.returncode)
        self.assertEqual("BLOCKED_QUEUE_PREPARATION", self.last_status["state"])
        self.assertEqual("NOT_RUN", self.last_status["review_execution"])
        self.assertEqual("NOT_RUN", self.last_status["merge_execution"])


if __name__ == "__main__":
    unittest.main()
