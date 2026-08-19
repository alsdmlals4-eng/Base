from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

skill_path = ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md"
skill = skill_path.read_text(encoding="utf-8")
needle = "5. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다."
replacement = needle + "\n- 이미 구현된 finding을 다시 수정하지 않는다. 입력 상태가 바뀌지 않은 이미 구현·검증 finding은 재수정하지 않으며, 새 증거·회귀·정본 변화가 있을 때만 재개방한다."
if needle not in skill:
    raise SystemExit("SKILL_RULE_INSERTION_POINT_MISSING")
skill = skill.replace(needle, replacement, 1)
skill_path.write_text(skill, encoding="utf-8")

test_path = ROOT / "tests/test_neutral_adversarial_feature_lifecycle.py"
test = test_path.read_text(encoding="utf-8")
pattern = re.compile(
    r"\n    def test_adversarial_review_repeats_full_improvement_loop_at_least_five_times_when_run\(self\) -> None:\n.*?(?=\n    def test_socratic_review_lens_is_selective_evidence_first_and_meta_validated)",
    re.S,
)
new_test = '''
    def test_adversarial_review_repeats_until_verified_clean_exit(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS",
            "FULL_SCOPE_REVIEW",
            "FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "CLEAN_REVIEW_EXIT",
            "loop_index",
            "앞 회차의 수정 결과",
            "새로운 유효 오류·충돌·누락·blocking finding이 0",
            "이미 구현된 finding을 다시 수정하지 않는다",
        ):
            self.assertIn(term, adversarial)

        self.assertNotIn("FULL_LOOP_COUNT_MINIMUM: 5", adversarial)
        self.assertNotIn("FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS", adversarial)
        self.assertNotIn("FIVE_DISTINCT_ADVERSARIAL_ROUNDS", adversarial)
        self.assertNotIn("ROUND_1_INTENT_ASSUMPTIONS_SCOPE", adversarial)
'''
new, count = pattern.subn("\n" + new_test.lstrip("\n"), test, count=1)
if count != 1:
    raise SystemExit(f"EXPECTED_ONE_NEUTRAL_LOOP_TEST, got {count}")
test_path.write_text(new, encoding="utf-8")

Path(__file__).unlink()
print("NEUTRAL_CLEAN_REVIEW_CONTRACT_FIXED")
