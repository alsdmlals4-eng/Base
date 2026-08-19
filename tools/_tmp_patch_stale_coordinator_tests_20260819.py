from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


# Preserve explicit completion/coordinator tokens and learning-report wording while
# keeping the new sequential coordinator semantics.
for path in (
    "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md",
    "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md",
):
    text = read(path)
    if "CLEAN_REVIEW_EXIT" not in text:
        text = text.rstrip() + (
            "\n\n## Clean exit token\n\n"
            "최소 5회의 진짜 full-scope loop 이후 유효 blocker와 회귀가 0이고 acceptance/정본/evidence 조건이 닫혀야만 "
            "`CLEAN_REVIEW_EXIT`를 선언한다.\n"
        )
    if path.endswith("OPTIMIZATION_PROMPT.md") and "사용자 학습형 완료보고" not in text:
        text = text.rstrip() + (
            "\n\n## 사용자 학습형 완료보고\n\n"
            "각 Part checkpoint는 규칙·Skill·Module·BEFORE→AFTER·검증·교훈·재검토 조건을 사람이 이해할 수 있게 설명한다.\n"
        )
    if path.endswith("INTEGRATION_PROMPT.md") and "CURRENT_COORDINATOR_CHAT" not in text:
        text = text.replace(
            "`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`\n",
            "`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`\n\n현재 이 동일 coordinator 채팅의 canonical 이름은 `CURRENT_COORDINATOR_CHAT`이다.\n",
            1,
        )
    write(path, text.rstrip() + "\n")

path = "tests/test_base_partition_contract.py"
text = read(path)
text = text.replace(
    'self.assertEqual("HYBRID_CONTROL_PLANE_END_TO_END_CAPABILITY_PARTITIONS", manifest["selected_strategy"])',
    'self.assertEqual("ONE_BASE_STABLE_PARTITIONS_SEQUENTIAL_COORDINATOR", manifest["selected_strategy"])',
)
text = text.replace(
    'self.assertEqual("INTEGRATION_ONLY", manifest["control_plane"]["write_authority"])',
    'self.assertEqual("COORDINATOR_OR_INTEGRATION", manifest["control_plane"]["write_authority"])',
)
text = text.replace(
    '        self.assertEqual(9, integration["worker_chat_count"])\n        self.assertEqual(9, integration["total_new_gpt_chats_after_task_1"])',
    '        self.assertEqual(0, integration["worker_chat_count"])\n        self.assertEqual(0, integration["total_new_gpt_chats_after_task_1"])',
)
text = text.replace(
    'self.assertIn("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", text)',
    'self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)',
)
text = text.replace(
    "def test_one_chat_one_part_notion_and_github_isolation(self) -> None:",
    "def test_single_coordinator_preserves_unique_notion_part_pages_and_semantic_attribution(self) -> None:",
)
text = text.replace(
    'self.assertEqual("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", isolation["worker_model"])',
    'self.assertEqual("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", isolation["worker_model"])',
)
text = text.replace(
    '        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["hub_write"])\n        self.assertEqual("INTEGRATION_ONLY", isolation["notion"]["shared_visual_write"])',
    '        self.assertEqual("COORDINATOR", isolation["notion"]["hub_write"])\n        self.assertEqual("COORDINATOR", isolation["notion"]["shared_visual_write"])',
)
text = text.replace(
    '            self.assertEqual("ONE_CHAT_END_TO_END", part["chat_ownership"])\n            self.assertEqual("OWN_PART_PAGE_ONLY", part["notion_write_authority"])',
    '            self.assertEqual("CURRENT_COORDINATOR_CHAT_SEQUENTIAL_CHECKPOINT", part["chat_ownership"])\n            self.assertEqual("COORDINATOR_CURRENT_OR_AFFECTED_PART", part["notion_write_authority"])',
)
text = text.replace(
    '        self.assertIn("ONE_GPT_CHAT_OWNS_ONE_PART_END_TO_END", worker)\n        self.assertIn("자기 `notion_page_url`만 직접 수정", worker)\n        self.assertIn("Base Hub", INTEGRATION_PROMPT.read_text(encoding="utf-8"))',
    '        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", worker)\n        self.assertIn("PART_OWNERSHIP_IS_SEMANTIC_RESPONSIBILITY_NOT_WRITE_BARRIER", worker)\n        self.assertIn("HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN", INTEGRATION_PROMPT.read_text(encoding="utf-8"))',
)
old_name = "def test_operating_model_compares_four_real_strategies_and_records_revisit_conditions(self) -> None:"
new_name = "def test_operating_model_compares_real_execution_strategies_and_records_revisit_conditions(self) -> None:"
text = text.replace(old_name, new_name)
old_terms = '''        for term in ("A · 디렉터리 계층 분할", "B · 기능/도메인 분할", "C · Control Plane + End-to-End Capability Partition", "D · 동적 의존성 그래프 재클러스터링", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토 조건"):
            self.assertIn(term, text)
        self.assertIn("새 GPT 채팅은 P01~P09의 9개", text)
        self.assertIn("CURRENT_COORDINATOR_CHAT", text)'''
new_terms = '''        for term in ("A · 9개 별도 채팅 유지", "B · 한 coordinator 채팅", "C · Part 자체 제거", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토"):
            self.assertIn(term, text)
        self.assertIn("새 Part 채팅을 9개 만들지 않는다", text)
        self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)'''
if old_terms not in text:
    # It may already have the first replacement from an earlier migration attempt.
    partial_old = '''        for term in ("A · 9개 별도 채팅 유지", "B · 한 coordinator 채팅", "C · Part 자체 제거", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토"):
            self.assertIn(term, text)
        self.assertIn("새 GPT 채팅은 P01~P09의 9개", text)
        self.assertIn("CURRENT_COORDINATOR_CHAT", text)'''
    if partial_old not in text:
        raise SystemExit("stale operating-model expectation block missing")
    text = text.replace(partial_old, new_terms, 1)
else:
    text = text.replace(old_terms, new_terms, 1)

text = text.replace(
    '        self.assertIn("--integration", text)\n        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)',
    '        self.assertIn("--integration", text)\n        self.assertIn("--coordinator", text)\n        self.assertIn("CONTROL_PLANE_WRITE_FORBIDDEN", text)\n        self.assertIn("CONTROL_PLANE_COORDINATOR_WRITE", text)\n        self.assertIn("SEMANTIC_OWNER:", text)',
)
text = text.replace(
    'self.assertEqual("READ_ONLY_UNLESS_INTEGRATION_ASSIGNMENT_OR_CROSS_PART_CHANGE_REQUEST", manifest["unassigned_path_policy"])',
    'self.assertEqual("COORDINATOR_REVIEW_WITH_SEMANTIC_OWNER_ATTRIBUTION", manifest["unassigned_path_policy"])',
)
write(path, text)

print("STALE_COORDINATOR_TEST_EXPECTATIONS_PATCHED")
