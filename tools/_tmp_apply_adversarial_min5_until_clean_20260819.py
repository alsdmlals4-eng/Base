from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_exact(path: str, old: str, new: str) -> None:
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"MISSING_PATTERN {path}: {old[:120]!r}")
    if text.count(old) != 1:
        raise SystemExit(f"NON_UNIQUE_PATTERN {path}: count={text.count(old)} {old[:120]!r}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_exact(
    "AGENTS.md",
    "- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:** L1 이상에서 적대적 검토를 실행할 때는 고정 횟수나 quota로 종료하지 않는다. **전체 승인 범위 적대적 검토 → 충돌·누락·오류·위험 finding 검증 → 검증된 finding 개선·보완 → 실제 검증·회귀검사 → 개선된 상태 전체를 다시 공격**하는 완전한 개선 루프를 반복한다. 새로 검증되는 `MUST_FIX`·blocking finding·정본 충돌·acceptance failure가 하나라도 나오면 수정·검증 뒤 다시 전체 범위를 공격한다. 종료는 횟수가 아니라 **새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정의 회귀가 없으며, acceptance criteria·정본 신선도·증거 ceiling을 모두 만족하는 `CLEAN_REVIEW_EXIT`**으로만 판정한다. 동일 finding을 표현만 바꿔 반복 성과로 계수하지 않는다.",
    "- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:** L1 이상에서 적대적 검토를 실행하면 `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`를 적용한다. **전체 승인 범위 적대적 검토 → 충돌·누락·오류·위험 finding 검증 → 검증된 finding 개선·보완 → 실제 검증·회귀검사 → 개선된 상태 전체를 다시 공격**하는 완전한 개선 루프를 **최소 5회** 수행하며, 5회의 완전한 전체 개선 루프를 마치기 전에는 finding이 0이어도 `CLEAN_REVIEW_EXIT`로 종료하지 않는다. **5회 이후에도** 새로 검증되는 `MUST_FIX`·blocking finding·정본 충돌·acceptance failure가 하나라도 나오면 수정·검증 뒤 추가 전체 루프를 계속한다. 종료는 최소 5회를 충족한 뒤 **새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정의 회귀가 없으며, acceptance criteria·정본 신선도·증거 ceiling을 모두 만족하는 `CLEAN_REVIEW_EXIT`**으로만 판정한다. 5회는 최소 floor이지 최대치가 아니며, 횟수를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않는다."
)

replace_exact(
    "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
    "ADVERSARIAL_REVIEW_UNTIL_CLEAN\nPOSTMERGE_PROMOTION_AND_SUPERSESSION",
    "ADVERSARIAL_REVIEW_UNTIL_CLEAN\nFULL_LOOP_COUNT_MINIMUM: 5\nMINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5\nPOSTMERGE_PROMOTION_AND_SUPERSESSION"
)

replace_exact(
    "docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md",
    "→ ADVERSARIAL REVIEW UNTIL CLEAN\n→ LONG-TERM FIT CLOSURE",
    "→ AT LEAST 5 FULL ADVERSARIAL LOOPS, THEN UNTIL CLEAN\n→ LONG-TERM FIT CLOSURE"
)

old_exit = '''## 적대적 검토 종료 조건

`ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 숫자 quota가 아니다.

```text
FULL_SCOPE_REVIEW
→ validate findings
→ fix approved findings
→ verification/regression
→ RE-ATTACK improved whole state
→ repeat while any new valid error/conflict/omission/blocker appears
→ CLEAN_REVIEW_EXIT
```

`CLEAN_REVIEW_EXIT` 조건은 모두 필요하다.

- 새 유효 `MUST_FIX` 또는 blocking finding 0
- 정본/owner/consumer/reference 충돌 0
- acceptance criterion failure 0
- 기존 수정으로 생긴 회귀 0
- evidence ceiling 위반/미실행을 PASS로 과장한 항목 0
- 더 나은 대안 재탐색과 장기계획 적합성 재검사가 현재 증거에서 추가 변경을 요구하지 않음

한 회차가 깨끗해도 전체 범위를 다시 공격했을 때 새 finding이 나오면 종료하지 않는다. 반대로 깨끗한 상태에서 횟수를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않는다.
'''
new_exit = '''## 적대적 검토 종료 조건

`ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 **최소 5회 floor + 이후 clean-exit** 계약이다. `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`이며 5회는 최대 quota가 아니다.

```text
FULL_SCOPE_REVIEW #1
→ validate findings → fix approved findings → verification/regression → RE-ATTACK
→ FULL_SCOPE_REVIEW #2
→ FULL_SCOPE_REVIEW #3
→ FULL_SCOPE_REVIEW #4
→ FULL_SCOPE_REVIEW #5
→ if any new valid error/conflict/omission/blocker remains: continue #6..N
→ CLEAN_REVIEW_EXIT only after minimum 5 and verified zero-blocker re-attack
```

`CLEAN_REVIEW_EXIT` 조건은 모두 필요하다.

- 완전한 전체 개선 루프 5회 이상 완료
- 새 유효 `MUST_FIX` 또는 blocking finding 0
- 정본/owner/consumer/reference 충돌 0
- acceptance criterion failure 0
- 기존 수정으로 생긴 회귀 0
- evidence ceiling 위반/미실행을 PASS로 과장한 항목 0
- 더 나은 대안 재탐색과 장기계획 적합성 재검사가 현재 증거에서 추가 변경을 요구하지 않음

1~5회 중 한 회차가 깨끗해도 최소 floor를 충족하기 전에는 종료하지 않는다. **5회 이후에도** 전체 범위를 다시 공격했을 때 새 finding이 나오면 수정·검증 후 추가 전체 루프를 수행한다. 다만 횟수를 채우기 위해 가짜 finding이나 불필요한 변경을 만들지 않으며, full-scope 검토와 검증을 실제 수행했다면 finding/changes가 0인 clean loop도 유효한 회차다.
'''
replace_exact("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md", old_exit, new_exit)

old_section12 = '''## 12. 오류가 사라질 때까지의 전체 적대적 개선 루프

### `ADVERSARIAL_REVIEW_UNTIL_CLEAN`

적대적 검토를 실제로 실행할 때는 고정 횟수를 채우는 것이 아니라 다음 **전체 범위 개선 루프를 CLEAN_REVIEW_EXIT가 성립할 때까지** 반복한다.

```text
FULL_SCOPE_REVIEW
→ finding 검증
→ 개선/보완
→ 실제 검증/회귀
→ 개선된 전체 상태 RE-ATTACK
```

각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자산, 실패 복구, 보안, 동시성, 비용, 벤치마크, 장기 유지, 증거와 완료조건을 다시 본다. 회차 N 입력은 원칙적으로 회차 N-1의 검증된 출력 상태다.

각 회차에서 `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_REQUIRED`를 다시 확인한다. 5회차 뒤 P0/P1 또는 acceptance criterion을 막는 finding이 남으면 수정·검증 후 추가 전체 루프를 수행한다.

`NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니다.
'''
new_section12 = '''## 12. 최소 5회 후 오류가 사라질 때까지의 전체 적대적 개선 루프

### `ADVERSARIAL_REVIEW_UNTIL_CLEAN`

적대적 검토를 실제로 실행할 때는 다음 **전체 범위 개선 루프를 최소 5회 수행하고, 5회 이후에는 CLEAN_REVIEW_EXIT가 성립할 때까지** 반복한다.

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_SCOPE_REVIEW
→ finding 검증
→ 개선/보완
→ 실제 검증/회귀
→ 개선된 전체 상태 RE-ATTACK
→ repeat through loop 5 even when an earlier loop is clean
→ after loop 5, continue while any valid blocker exists
→ CLEAN_REVIEW_EXIT
```

각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자산, 실패 복구, 보안, 동시성, 비용, 벤치마크, 장기 유지, 증거와 완료조건을 다시 본다. 회차 N 입력은 원칙적으로 회차 N-1의 검증된 출력 상태다.

각 회차에서 `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_REQUIRED`를 다시 확인한다. **최소 5회의 완전한 전체 개선 루프**를 수행하기 전에는 `CLEAN_REVIEW_EXIT`를 선언하지 않는다. **5회 이후에도** P0/P1, `MUST_FIX`, 정본 충돌, acceptance criterion을 막는 finding 또는 회귀가 남으면 수정·검증 후 추가 전체 루프를 수행한다. 최대 회차 수는 고정하지 않는다.

finding이 없는 의무 회차에서도 전체 범위 attack·검증·대안·장기 적합성 재검사를 실제 수행하고 evidence를 남긴다. 횟수를 채우기 위한 가짜 finding이나 불필요한 변경은 금지한다.

`NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니다.
'''
replace_exact("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md", old_section12, new_section12)

replace_exact(
    "skills/running-adversarial-review-and-refinement/SKILL.md",
    "이 Skill을 L1 이상 작업물·PR·저장소 감사·병합 후 결과의 적대적 검토로 호출하면 **고정 횟수 없이 CLEAN_REVIEW_EXIT까지 전체 검토·개선 생명주기를 반복한다.** 관점 수나 loop 수를 성과로 계산하지 않는다. 앞 회차의 수정 결과와 새 증거 자체가 다음 회차의 공격 입력이다.",
    "이 Skill을 L1 이상 작업물·PR·저장소 감사·병합 후 결과의 적대적 검토로 호출하면 **최소 5회의 완전한 전체 개선 루프를 수행하고, 그 이후 CLEAN_REVIEW_EXIT까지 전체 검토·개선 생명주기를 반복한다.** `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`다. 5회는 종료 quota나 최대치가 아니라 최소 floor다. 앞 회차의 수정 결과와 새 증거 자체가 다음 회차의 공격 입력이다."
)

replace_exact(
    "skills/running-adversarial-review-and-refinement/SKILL.md",
    "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS\nFULL_SCOPE_REVIEW",
    "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS\nFULL_LOOP_COUNT_MINIMUM: 5\nMINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5\nFULL_SCOPE_REVIEW"
)

old_rules = '''종료 규칙:

1. 새 유효 `MUST_FIX`, P0/P1, acceptance blocker가 하나라도 나오면 수정·검증 뒤 다음 전체 회차를 수행한다.
2. 정본·consumer·reference·Schema drift, 정상 경로 회귀, evidence ceiling 위반이 발견되면 종료하지 않는다.
3. `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_RECHECK`에서 현재 승인 범위 안의 더 강한 개선이 확인되면 적용 후 다시 전체 검토한다.
4. `NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니며, 완료 조건에 필요한 증거가 없으면 clean exit가 아니다.
5. 동일 finding을 표현만 바꿔 반복 계수하거나, 횟수를 채우기 위해 가짜 finding/불필요한 변경을 만들지 않는다.
6. **전체 재공격 결과 새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정 회귀 0, acceptance criteria 충족, 정본/참조 신선도와 evidence ceiling이 모두 닫힐 때만 `CLEAN_REVIEW_EXIT`다.**
'''
new_rules = '''종료 규칙:

1. **1~5회는 의무 전체 루프다.** 최소 5회의 완전한 전체 개선 루프를 실제 수행하기 전에는 중간 회차 finding이 0이어도 `CLEAN_REVIEW_EXIT`를 선언하지 않는다.
2. 새 유효 `MUST_FIX`, P0/P1, acceptance blocker가 하나라도 나오면 수정·검증 뒤 다음 전체 회차를 수행한다.
3. 정본·consumer·reference·Schema drift, 정상 경로 회귀, evidence ceiling 위반이 발견되면 종료하지 않는다.
4. `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_RECHECK`에서 현재 승인 범위 안의 더 강한 개선이 확인되면 적용 후 다시 전체 검토한다.
5. `NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니며, 완료 조건에 필요한 증거가 없으면 clean exit가 아니다.
6. **5회 이후에도** 새로운 유효 오류·충돌·누락·blocking finding, 정본 충돌, acceptance failure 또는 회귀가 하나라도 나오면 수정·검증 후 6..N번째 전체 루프를 계속한다. 최대 회차 수는 고정하지 않는다.
7. 동일 finding을 표현만 바꿔 반복 계수하거나, 최소 횟수를 채우기 위해 가짜 finding/불필요한 변경을 만들지 않는다. full-scope attack·검증·대안·장기 적합성 재검사를 실제 수행했다면 finding과 changes가 0인 clean loop도 유효한 의무 회차다.
8. **최소 5회를 완료한 뒤 전체 재공격 결과 새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정 회귀 0, acceptance criteria 충족, 정본/참조 신선도와 evidence ceiling이 모두 닫힐 때만 `CLEAN_REVIEW_EXIT`다.**
'''
replace_exact("skills/running-adversarial-review-and-refinement/SKILL.md", old_rules, new_rules)

old_neutral = '''    def test_adversarial_review_repeats_until_verified_clean_exit(self) -> None:
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
new_neutral = '''    def test_adversarial_review_repeats_minimum_five_then_until_verified_clean_exit(self) -> None:
        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")
        for term in (
            "ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS",
            "FULL_LOOP_COUNT_MINIMUM: 5",
            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",
            "FULL_SCOPE_REVIEW",
            "FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK",
            "BETTER_ALTERNATIVE_SEARCH",
            "LONG_TERM_PLAN_FIT_RECHECK",
            "CLEAN_REVIEW_EXIT",
            "loop_index",
            "최소 5회의 완전한 전체 개선 루프",
            "5회 이후에도",
            "새로운 유효 오류·충돌·누락·blocking finding이 0",
            "이미 구현된 finding을 다시 수정하지 않는다",
        ):
            self.assertIn(term, adversarial)

        self.assertNotIn("FIVE_DISTINCT_ADVERSARIAL_ROUNDS", adversarial)
        self.assertNotIn("ROUND_1_INTENT_ASSUMPTIONS_SCOPE", adversarial)
'''
replace_exact("tests/test_neutral_adversarial_feature_lifecycle.py", old_neutral, new_neutral)

# Strengthen the focused Long-Horizon test so the global owners are also pinned.
long_test = ROOT / "tests/test_base_long_horizon_work_contract.py"
text = long_test.read_text(encoding="utf-8")
old = '''        for term in (\n            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",\n            "REQUIRED_WORK_REMAINING",'''
new = '''        for term in (\n            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",\n            "FULL_LOOP_COUNT_MINIMUM: 5",\n            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",\n            "REQUIRED_WORK_REMAINING",'''
if old not in text:
    raise SystemExit("MISSING_PATTERN tests/test_base_long_horizon_work_contract.py entrypoint terms")
text = text.replace(old, new, 1)
old = '''            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",\n            "POSTMERGE_PROMOTION_AND_SUPERSESSION",'''
new = '''            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",\n            "FULL_LOOP_COUNT_MINIMUM: 5",\n            "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5",\n            "POSTMERGE_PROMOTION_AND_SUPERSESSION",'''
if old not in text:
    raise SystemExit("MISSING_PATTERN tests/test_base_long_horizon_work_contract.py policy terms")
text = text.replace(old, new, 1)
long_test.write_text(text, encoding="utf-8")

log_path = ROOT / "skills/running-adversarial-review-and-refinement/LEARNING_LOG.md"
log = log_path.read_text(encoding="utf-8")
header = "# Running Adversarial Review and Refinement — Learning Log\n\n"
if not log.startswith(header):
    raise SystemExit("LEARNING_LOG_HEADER_MISMATCH")
entry = '''## 2026-08-19 — minimum five full loops plus verified clean exit is the active contract

- **Trigger:** 사용자가 최신 규칙으로 적대적 검토 루프를 **최소 5회 수행하고, 5회 이후에도 유효 오류가 남으면 오류 0이 될 때까지 계속**하도록 명시했다.
- **Finding:** 직전 `ADVERSARIAL_REVIEW_UNTIL_CLEAN`은 숫자 quota가 종료조건을 왜곡하는 문제를 해결했지만 최소 검토 깊이가 사라져 한두 번의 우연한 clean 결과로 충분히 깊게 공격하지 못할 수 있었다. 반대로 과거 fixed-five 계약은 5회를 최대 종료점처럼 오해할 여지가 있었다.
- **Decision:** 기존 Skill owner를 유지하고 `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`, `CLEAN_REVIEW_EXIT`를 함께 사용한다. 1~5회는 전체 승인 범위를 다시 공격하는 의무 loop이며 5회 전에는 종료하지 않는다. 5회 이후에는 새 유효 `MUST_FIX`/P0/P1/정본 충돌/acceptance failure/회귀가 하나라도 있으면 6..N회로 계속하고, post-minimum 전체 재공격에서 유효 blocking finding 0일 때만 종료한다.
- **Evidence:** PR #532에서 먼저 Long-Horizon regression을 바꿔 current production이 `FULL_LOOP_COUNT_MINIMUM: 5` 부재로 RED가 되는 것을 확인했다. production owner와 companion regression을 동기화한 뒤 focused/required CI로 GREEN을 요구한다.
- **Boundary:** 최소 5회는 가짜 finding이나 불필요한 변경을 만들라는 뜻이 아니다. full-scope attack·검증·대안·장기 적합성 재검사를 실제 수행하면 finding/changes가 0인 clean loop도 의무 회차로 인정한다. 5회는 최대치가 아니며 5회 이후 오류가 남으면 계속한다.
- **Next trigger:** 5회 미만 clean exit, 5회에서 강제 종료, loop를 lens/checklist 개수로 대체, 가짜 finding 생성, evidence ceiling 무시가 나타나면 즉시 재검토한다.

'''
log = header + entry + log[len(header):]
log = log.replace(
    "## 2026-08-19 — fixed loop counts are weaker than a verified clean-exit condition",
    "## 2026-08-19 — fixed loop counts are weaker than a verified clean-exit condition (SUPERSEDED LATER SAME DAY)",
    1,
)
log_path.write_text(log, encoding="utf-8")

Path(__file__).unlink()
print("ADVERSARIAL_MIN5_UNTIL_CLEAN_APPLIED")
