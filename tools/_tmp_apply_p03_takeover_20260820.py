from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "e26684d80e1455e18188a557762c8b3e63099173"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def old(path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{OLD}:{path}"], cwd=ROOT, text=True, encoding="utf-8"
    )


# 1. These three P03 review surfaces were unchanged on current main relative to
# the original P03 baseline, so reapply the already-reviewed semantic delta.
for path in (
    "skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md",
    "skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md",
    "templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md",
):
    write(path, old(path))

# 2. Preserve current full-loop contract, add P03's fix-guided guard, and make
# the user's full-loop-not-review-lens correction explicit in the Skill itself.
adv_path = "skills/running-adversarial-review-and-refinement/SKILL.md"
adv = read(adv_path)
if "FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE" not in adv:
    anchor = "일반 작업은 `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`를 사용한다. 저장소 전체 감사는 `references/repository-wide-audit-protocol.md`, 세부 Finding·회귀 판정은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.\n"
    guard = """

### Finding validation evidence guard

`FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE: REQUIRED`

구체적 수정으로 재현 가능한 Finding은 같은 acceptance/evidence ceiling에서 baseline과 candidate를 비교해 비판 자체를 재검증한다. candidate가 원 실패를 줄이지 못하거나 새 회귀를 만들면 심각도와 채택 여부를 다시 판정한다. 순수 기획·미감처럼 동등한 실행 비교가 불가능한 문제에는 억지로 적용하지 않는다. 세부 기록은 `references/finding-and-regression-protocol.md`를 따른다. 실제 runtime/build/render PASS 권위는 해당 validation owner를 넘지 않는다.
"""
    if anchor not in adv:
        raise SystemExit("adversarial workflow anchor missing")
    adv = adv.replace(anchor, anchor + guard, 1)
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in adv:
    anchor = "MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5\n"
    if anchor not in adv:
        raise SystemExit("full loop token anchor missing")
    adv = adv.replace(anchor, anchor + "FULL_LOOP_IS_NOT_A_REVIEW_LENS\n", 1)
    marker = "한 전체 회차:\n"
    explanation = """
`FULL_LOOP_IS_NOT_A_REVIEW_LENS`: `Loop 1=scope`, `Loop 2=UX`, `Loop 3=CI`처럼 서로 다른 관점을 각각 한 번 검사한 것은 여러 full loop로 계수하지 않는다. Scope·UX·CI·security·cost·long-term 등 필요한 lens는 **각 counted loop 안에서** 전체 승인 범위를 다시 공격하기 위한 coverage로 사용한다. 회차별 대표 finding을 기록할 수는 있지만 대표 finding이 그 회차의 검토 범위를 뜻하지 않는다.

"""
    if marker not in adv:
        raise SystemExit("full loop explanation anchor missing")
    adv = adv.replace(marker, explanation + marker, 1)
write(adv_path, adv)

# 3. Reapply execution-surface-aware Git sync, then layer the current
# OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM rule so stale P03 semantics cannot revert it.
sync_path = "skills/synchronizing-local-and-github-state/SKILL.md"
sync = old(sync_path)
if "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM" not in sync:
    anchor = "`same goal`은 `same workstream`의 증거가 아니다. `different workstream`이면 사용자의 현재 명시 승인 없이 checkout/write/rebase/close/merge/selective-copy를 수행하지 않는다.\n"
    addition = """

### Open PR activity classification

`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`

`open/draft/ready` PR 상태만으로 다른 작업자가 현재 활동 중이라고 판정하지 않는다. 실제 보호는 사용자 지시, current session/automation owner, Resource Lock 등 current owner evidence가 있을 때만 적용한다. 사용자가 `CURRENT_COORDINATOR_CHAT`만 활성이라고 확인하면 unresolved open PR은 latest main과 Goal을 재검증해 coordinator takeover/finish/supersession 대상으로 분류할 수 있다. 실제 `ACTIVE_OTHER_WORKER`로 확인된 workstream만 mutation-protected다.
"""
    if anchor not in sync:
        raise SystemExit("sync open-pr anchor missing")
    sync = sync.replace(anchor, anchor + addition, 1)
write(sync_path, sync)

safe_path = "skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md"
safe = old(safe_path)
if "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM" not in safe:
    anchor = "- `HYBRID`: local과 connector 증거의 출처를 각각 구분한다.\n"
    addition = "- `OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`: open/draft/ready 상태는 owner evidence가 아니다. 실제 current owner evidence가 없고 사용자가 현재 coordinator만 활성이라고 확인했으면 열린 PR을 backlog로 분류해 최신 main에서 takeover/finish/supersession할 수 있다.\n"
    if anchor not in safe:
        raise SystemExit("safe-sync execution-surface anchor missing")
    safe = safe.replace(anchor, anchor + addition, 1)
write(safe_path, safe)

# 4. Reuse the old P03 focused regression, and add the new takeover checks to
# an already-executed adversarial regression suite so CI consumption is real.
quality_path = "tests/test_p03_adversarial_quality_contract.py"
write(quality_path, old(quality_path))

neutral_path = "tests/test_neutral_adversarial_feature_lifecycle.py"
neutral = read(neutral_path)
if "test_p03_current_main_evidence_bounded_takeover" not in neutral:
    marker = "    def test_socratic_review_lens_is_selective_evidence_first_and_meta_validated(self) -> None:\n"
    method = '''    def test_p03_current_main_evidence_bounded_takeover(self) -> None:\n        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")\n        finding = read("skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md")\n        audit = read("skills/running-adversarial-review-and-refinement/references/repository-wide-audit-protocol.md")\n        postmerge = read("templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md")\n        sync = read("skills/synchronizing-local-and-github-state/SKILL.md")\n        safe_sync = read("skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md")\n\n        for token in ("FIX_GUIDED_VERIFICATION_WHEN_EXECUTABLE", "FULL_LOOP_IS_NOT_A_REVIEW_LENS", "Loop 1=scope"):\n            self.assertIn(token, adversarial)\n        for text in (finding, audit, postmerge):\n            self.assertIn("CONFIGURED_PROJECT_WORKSPACE", text)\n        for text in (sync, safe_sync):\n            for token in ("execution_surface", "GITHUB_CONNECTOR_ONLY", "NOT_APPLICABLE_CONNECTOR_ONLY", "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM"):\n                self.assertIn(token, text)\n\n'''
    if marker not in neutral:
        raise SystemExit("neutral regression insertion anchor missing")
    neutral = neutral.replace(marker, method + marker, 1)
write(neutral_path, neutral)

# 5. Record the current-main takeover lesson without reusing the old invalid
# lens-separated loop count as current evidence.
p03_log = "docs/operations/base-partitions/learning/P03_LEARNING_LOG.md"
log = read(p03_log)
entry = """

### 2026-08-20 — Current-main P03 takeover after single-coordinator correction

```yaml
work_ref: "P03 coordinator takeover / PR #549; supersedes unfinished #537"
baseline_and_result: "current Base main c8de06cdd63ddcb9121d8321bf135eaea9e14f06 -> current-main selective P03 integration"
what_worked:
  - "Revalidated #537 as coordinator backlog instead of treating open PR state as another active worker."
  - "Reused only evidence-bounded P03 semantics on the latest main rather than merging the stale branch wholesale."
  - "Made FULL_LOOP_IS_NOT_A_REVIEW_LENS explicit in the P03 Skill so review lenses cannot be counted as separate full loops."
what_failed_or_was_rejected:
  - "The original #537 loop count is not reused because several entries described separate review lenses rather than repeated whole-lifecycle attacks."
  - "Blind old-branch merge was rejected because it could overwrite newer coordinator/open-PR policy."
reusable_lesson: "Open PR state and active ownership must be separated; takeover should selectively rehydrate unique semantic deltas onto current main and rerun current review evidence."
anti_pattern: "Counting scope/UX/CI as separate adversarial loops or treating stale branch bytes as current authority."
affected_rules_skills_modules:
  - "running-adversarial-review-and-refinement"
  - "synchronizing-local-and-github-state"
  - "Finding Validation / Git Sync & Isolation"
evidence:
  - "focused RED run 32272479838"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "current-owner-evidence takeover + selective current-main semantic rehydration"
source_followup_questions: []
revisit_condition: "Revisit if actual simultaneous workers become common or execution-surface evidence becomes machine-schema owned."
```
"""
if "Current-main P03 takeover after single-coordinator correction" not in log:
    log = log.rstrip() + entry
write(p03_log, log)

sync_log_path = "skills/synchronizing-local-and-github-state/LEARNING_LOG.md"
sync_log = read(sync_log_path)
entry2 = """

## 2026-08-20 — Open PR state is not execution-surface owner evidence

- **Status:** `PATTERN`
- An open/draft/ready PR is backlog metadata, not proof of another active worker.
- Protect mutation only when current owner evidence exists; otherwise a user-confirmed single coordinator may revalidate and take over stale backlog on latest main.
- Connector-only execution must still use `GITHUB_CONNECTOR_ONLY` / `NOT_APPLICABLE_CONNECTOR_ONLY` and never invent local evidence.
"""
if "Open PR state is not execution-surface owner evidence" not in sync_log:
    sync_log = sync_log.rstrip() + entry2
write(sync_log_path, sync_log)

print("P03_CURRENT_MAIN_TAKEOVER_APPLIED")
