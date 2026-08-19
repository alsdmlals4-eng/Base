from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


# Preserve explicit completion token and the exact learning-report wording used by
# existing Base tests while keeping the new sequential coordinator semantics.
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
    write(path, text.rstrip() + "\n")

path = "tests/test_base_partition_contract.py"
text = read(path)
text = text.replace(
    'self.assertEqual("HYBRID_CONTROL_PLANE_END_TO_END_CAPABILITY_PARTITIONS", manifest["selected_strategy"])',
    'self.assertEqual("ONE_BASE_STABLE_PARTITIONS_SEQUENTIAL_COORDINATOR", manifest["selected_strategy"])',
)
text = text.replace(
    'self.assertIn("PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION", text)',
    'self.assertIn("SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS", text)',
)
old_name = "def test_operating_model_compares_four_real_strategies_and_records_revisit_conditions(self) -> None:"
new_name = "def test_operating_model_compares_real_execution_strategies_and_records_revisit_conditions(self) -> None:"
text = text.replace(old_name, new_name)
old_terms = '''        for term in ("A · 디렉터리 계층 분할", "B · 기능/도메인 분할", "C · Control Plane + End-to-End Capability Partition", "D · 동적 의존성 그래프 재클러스터링", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토 조건"):
            self.assertIn(term, text)'''
new_terms = '''        for term in ("A · 9개 별도 채팅 유지", "B · 한 coordinator 채팅", "C · Part 자체 제거", "BETTER_ALTERNATIVE_SEARCH", "LONG_TERM_PLAN_FIT_REQUIRED", "재검토"):
            self.assertIn(term, text)'''
if old_terms not in text:
    raise SystemExit("stale operating-model alternative expectation block missing")
text = text.replace(old_terms, new_terms, 1)
write(path, text)

print("STALE_COORDINATOR_TEST_EXPECTATIONS_PATCHED")
