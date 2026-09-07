"""Regression tests for the MCP evaluation contract, not live MCP behavior."""
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "skills/evaluating-godot-assets-and-plugins-before-creation/references/source-catalog.md"
HEADING = "## 8. MCP 기능 비교·흡수 사전점검"


class McpCapabilityAbsorptionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalog = CATALOG.read_text(encoding="utf-8")

    def section(self, heading: str = HEADING) -> str:
        self.assertIn(heading + "\n", self.catalog, f"Missing active section: {heading}")
        tail = self.catalog.split(heading + "\n", 1)[1]
        level = len(heading) - len(heading.lstrip("#"))
        return re.split(rf"(?m)^#{{1,{level}}} ", tail, maxsplit=1)[0]

    def require(self, heading: str, *phrases: str) -> str:
        body = self.section(heading)
        for phrase in phrases:
            with self.subTest(section=heading, phrase=phrase):
                self.assertIn(phrase, body)
        return body

    def test_existing_catalog_routes_mcp_work_before_design(self) -> None:
        intro = self.catalog.split("## 0.", 1)[0]
        self.assertIn("MCP 비교·흡수 작업은 8절", intro)
        self.require(HEADING, "inventory-current-environment", "새 Skill", "기존 작업 계약")

    def test_host_native_inventory_is_preferred_to_another_parser(self) -> None:
        self.require("### 8.1 현재 기능의 증거를 먼저 분리",
                     "codex mcp list", "/mcp", "MCP: List Servers",
                     "CODEX_HOME", "별도 인벤토리 CLI", "enabled_tools", "disabled_tools")

    def test_configuration_and_runtime_are_distinct_and_unknown_is_not_absent(self) -> None:
        self.require("### 8.1 현재 기능의 증거를 먼저 분리",
                     "설정 파일만으로 활성 상태를 확정하지 않는다",
                     "등록", "활성", "연결", "실제 작업 검증",
                     "UNVERIFIED", "기능 부재의 증거가 아니다",
                     "새 구현이 필요하다고 추론하지 않는다")

    def test_absorption_order_prefers_no_code_change(self) -> None:
        body = self.require("### 8.2 추가 위치와 대안 선택",
                            "ABSORB", "REFACTOR", "REUSE", "BUILD_NEW",
                            "MCP 코드 수정이 아니다", "현행 유지")
        match = re.search(r"```text\n(.*?)\n```", body, re.DOTALL)
        self.assertIsNotNone(match, "Decision order must be an explicit bounded flow")
        flow = match.group(1) if match else ""
        steps = ["현재 기능 재사용", "기존 설정·작업 절차·검증 보강",
                 "확인된 결함만 기존 구현에 제한 수정", "역할이 다른 기존 전문 도구 재사용",
                 "대안 부적합 증거가 있을 때만 최소 신규 제작"]
        positions = [flow.find(step) for step in steps]
        self.assertTrue(all(position >= 0 for position in positions), positions)
        self.assertEqual(positions, sorted(positions))

    def test_evidence_projection_reuses_existing_owner_not_new_registry(self) -> None:
        self.require("### 8.2 추가 위치와 대안 선택",
                     "기존 작업 계약", "새 중앙 Registry", "실제 consumer",
                     "exact version", "변경 대상 owner", "검증", "rollback",
                     "UNVERIFIED이면", "BUILD_NEW 근거로 바꾸지 않는다")

    def test_server_count_does_not_replace_effective_writer_boundary(self) -> None:
        self.require("### 8.3 다중 MCP와 Blender의 경계",
                     "서버 개수", "같은 대상의 persistent mutation authority",
                     "HiGodot", "HIGODOT_SINGLE_AUTHORITY_AND_SAFE_OPERATION.md",
                     "별도 역할", "권한 격리의 증거는 아니다", "범용 MCP")

    def test_blender_stage_cannot_silently_write_project_canon(self) -> None:
        self.require("### 8.3 다중 MCP와 Blender의 경계",
                     "복제본", "staging", "SHA-256", "실제 Godot consumer",
                     "승인 자산", "이미지 모델", "Godot 실행 증거",
                     "프로젝트 정본을 직접 덮어쓰지 않는다")

    def test_existing_adapter_owns_safety_and_trial_rules(self) -> None:
        self.require("### 8.3 다중 MCP와 Blender의 경계",
                     "EXTERNAL_AGENT_ADAPTER_CONTRACT.md", "텔레메트리",
                     "개인 설정 전체", "키·토큰", "자동 재실행하지 않는다",
                     "추가 비용", "A/B", "TRIAL_APPROVED", "ADOPTED_ACTIVE")

    def test_dated_version_comparison_does_not_migrate_project(self) -> None:
        self.require("### 8.4 2026-09-07 비교 근거와 적용 판정",
                     "v3.2.0", "42c44e4d02ca1836a0e1866361509d3a14d83b0c",
                     "v4", "자동 업데이트", "NOT_RUN",
                     "설치 상태의 증거가 아니다", "Tetris")

    def test_benchmark_dispositions_are_explicit_and_source_backed(self) -> None:
        body = self.require("### 8.4 2026-09-07 비교 근거와 적용 판정",
                            "ADOPT", "ADAPT", "REJECT",
                            "modelcontextprotocol.io", "developers.openai.com/codex/mcp",
                            "code.visualstudio.com", "github.com/ahujasid/blender-mcp",
                            "github.com/hi-godot/godot-ai")
        rows = [line for line in body.splitlines() if line.startswith("| ")]
        self.assertGreaterEqual(len(rows), 4)

    def test_acceptance_distinguishes_contract_runtime_and_human_evidence(self) -> None:
        self.require("### 8.5 검증과 종료",
                     "문서 계약 검사", "실제 MCP", "runtime PASS", "UX/Human",
                     "문서 반영", "프로젝트 채택", "사용자 개입", "실패 복구",
                     "자동으로 승격하지 않는다", "NOT_RUN", "롤백")

    def test_native_observation_does_not_authorize_settings_or_installation(self) -> None:
        self.require("### 8.1 현재 기능의 증거를 먼저 분리",
                     "읽기 범위", "추가·삭제·로그인·권한 변경", "자동 실행하지 않는다",
                     "다른 프로젝트", "현재 세션")


if __name__ == "__main__":
    unittest.main()
