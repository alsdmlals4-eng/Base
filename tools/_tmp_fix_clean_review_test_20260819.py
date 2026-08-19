from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "tests/test_base_long_horizon_work_contract.py"
text = p.read_text(encoding="utf-8")
pattern = re.compile(
    r"\n    def test_adversarial_review_owner_requires_five_full_improvement_loops_when_invoked\(self\) -> None:\n.*?(?=\n    def |\n\nif __name__ ==)",
    re.S,
)
replacement = '''
    def test_adversarial_review_owner_repeats_until_clean_exit(self) -> None:
        skill = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS",
            "FULL_SCOPE_REVIEW",
            "FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "CLEAN_REVIEW_EXIT",
            "새로운 유효 오류·충돌·누락·blocking finding이 0",
        ):
            self.assertIn(term, skill)
        self.assertNotIn("FULL_LOOP_COUNT_MINIMUM: 5", skill)
        self.assertNotIn("FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS", skill)
        self.assertNotIn("최소 다섯 번", skill)
'''
new, count = pattern.subn("\n" + replacement.lstrip("\n"), text, count=1)
if count != 1:
    raise SystemExit(f"EXPECTED_ONE_OLD_LOOP_TEST, got {count}")
p.write_text(new, encoding="utf-8")
Path(__file__).unlink()
print("CLEAN_REVIEW_TEST_REPLACED")
