from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def update(path: str, transform):
    p = ROOT / path
    text = p.read_text(encoding="utf-8")
    new = transform(text)
    if new == text:
        raise SystemExit(f"NO_CHANGE_OR_PATTERN_MISSING: {path}")
    p.write_text(new, encoding="utf-8")


def replace_required(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"REQUIRED_PATTERN_MISSING: {old[:120]}")
    return text.replace(old, new)


# 1) Global Base rule: terminate adversarial review by clean result, not a numeric quota.
def agents_transform(text: str) -> str:
    old = "- **`FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`:** L1 이상에서 적대적 검토를 실행할 때는 다섯 관점을 각각 한 번 보는 방식이 아니라, **전체 승인 범위에 대한 적대적 검토 → 충돌·누락·문제 발견 → 검증된 finding 개선·보완 → 실제 검증·회귀검사 → 개선된 상태 전체를 다시 적대적으로 공격**하는 완전한 개선 루프를 최소 5회 반복한다. 각 회차는 사용자 의도·정본·Skill/Tool/구조·실제 구현·데이터·테스트·실패복구·보안·동시성·비용·벤치마크·장기 유지·증거·완료조건을 전체적으로 다시 본다. 5회차 뒤에도 blocking finding이 남으면 횟수를 채웠다는 이유로 종료하지 않고 수정·검증 후 **추가 전체 루프**를 수행한다."
    new = "- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:** L1 이상에서 적대적 검토를 실행할 때는 고정 횟수나 quota로 종료하지 않는다. **전체 승인 범위 적대적 검토 → 충돌·누락·오류·위험 finding 검증 → 검증된 finding 개선·보완 → 실제 검증·회귀검사 → 개선된 상태 전체를 다시 공격**하는 완전한 개선 루프를 반복한다. 새로 검증되는 `MUST_FIX`·blocking finding·정본 충돌·acceptance failure가 하나라도 나오면 수정·검증 뒤 다시 전체 범위를 공격한다. 종료는 횟수가 아니라 **새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정의 회귀가 없으며, acceptance criteria·정본 신선도·증거 ceiling을 모두 만족하는 `CLEAN_REVIEW_EXIT`**으로만 판정한다. 동일 finding을 표현만 바꿔 반복 성과로 계수하지 않는다."
    text = replace_required(text, old, new)
    marker = "## 7. 완료 보고\n"
    if marker not in text:
        raise SystemExit("AGENTS completion report marker missing")
    block = """## 7. 완료 보고\n\n### 사용자 학습형 완료보고\n\nBase와 Base를 채택한 프로젝트의 L1 이상 완료보고는 단순히 `작업 완료 / 테스트 통과`로 끝내지 않는다. 사용자가 작업 구조를 학습하고 다음 결정을 더 정확히 내릴 수 있도록 다음을 사람용으로 먼저 설명한다.\n\n- 이 작업/파트가 전체 Base 또는 프로젝트에서 담당하는 역할\n- 가장 중요한 상위 규칙과 실제 작동 시점\n- 사용한 핵심 Skill·Skill Mode와 서로의 책임 차이\n- 핵심 모듈과 `입력 → 판단/처리 → 출력 → 소비자/검증` 연결\n- 유지한 것 / 개선한 것 / 흡수·통합한 것 / 제거·폐기한 것 / 의도적으로 추가하지 않은 것\n- 변경 전 → 변경 후 → 사용자/플레이어 관점 기대효과 → trade-off\n- 장기계획 적합성 및 재검토 조건\n- 실행·검증 증거, 미검증, 남은 위험\n\n파일명·테스트명만 나열하지 말고 **왜 존재하고 무엇과 연결되며 없어지면 무엇이 깨지는지**까지 설명한다. 프로젝트 고유 내용은 프로젝트 전용으로, 반복 가능한 공용 교훈은 Base 승격 후보로 분리한다.\n\n"""
    return text.replace(marker, block, 1)


# 2) Long-horizon lifecycle: GPT-first, visual-first PoC, clean-loop termination, legacy absorption/removal.
def long_transform(text: str) -> str:
    text = text.replace("FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS", "ADVERSARIAL_REVIEW_UNTIL_CLEAN")
    text = text.replace("→ FIVE FULL ADVERSARIAL IMPROVEMENT LOOPS", "→ ADVERSARIAL REVIEW UNTIL CLEAN")
    text = text.replace("five full adversarial improvement loops", "adversarial review until clean")
    text = text.replace("다섯 번의 전체 적대적 개선 루프", "오류가 사라질 때까지의 전체 적대적 개선 루프")
    text = text.replace("### `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`", "### `ADVERSARIAL_REVIEW_UNTIL_CLEAN`")
    text = text.replace("적대적 검토를 실제로 실행할 때는 다섯 관점을 한 번씩 보는 것이 아니라 다음 **전체 범위 개선 루프를 최소 5회** 반복한다.", "적대적 검토를 실제로 실행할 때는 고정 횟수를 채우는 것이 아니라 다음 **전체 범위 개선 루프를 CLEAN_REVIEW_EXIT가 성립할 때까지** 반복한다.")
    text = text.replace("각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자", "각 회차는 사용자 의도, 정본/owner, Skill/Tool, 실제 구현, 데이터/자")
    insertion = """
## GPT-first 기획·검수와 선택적 Codex 보조 계약

`GPT_FIRST_PLANNING_AND_REVIEW`가 기본이다. GPT는 프로젝트 GitHub와 Notion의 현재 정본을 읽고 기획·조사·벤치마킹·대안 비교·시스템/데이터 설계·UI/UX 흐름·시각 방향·검수·적대적 검토를 닫는다. Codex는 필수 후속 단계가 아니라 실제 코드/Scene/Resource/data 변경, 저장소 규모가 큰 기계적 점검, 로컬 실행·테스트 등 **실행 권위가 필요한 경우에만** `OPTIONAL_CODEX_EXECUTOR`로 호출한다.

```text
GPT planning/research/review
→ GitHub + Notion canon reconciliation
→ UI/UX/visual requirement gate
→ when visuals materially affect PoC: generate/curate candidate visuals
→ attach to exact Project in Notion + readback
→ user/GPT review and approval state
→ implementation-ready package
→ OPTIONAL_CODEX_EXECUTOR only when implementation/runtime work benefits from it
→ repository implementation/runtime evidence
→ GPT final adversarial review
→ GitHub/Notion sync + readback
```

`VISUALIZED_POC_BEFORE_DEMO_TEST`: 플레이 경험을 UI/UX와 화면 맥락 없이 판단하면 왜곡될 위험이 큰 게임 PoC/데모는 회색 박스만으로 최종 평가하지 않는다. 기획·검수 단계에서 필요한 화면·HUD·핵심 상태·아트 앵커 이미지를 만들거나 승인된 기존 이미지를 선택하고, 올바른 Project의 Notion Visual/Asset surface에 배치·readback한 뒤 이를 구현 패키지의 시각 입력으로 사용한다. 모든 PoC에 완성 아트를 강제하지 않으며, 이미지가 판단에 실질 영향을 주지 않는 순수 로직 PoC는 예외로 기록한다.

`LEGACY_ABSORB_VERIFY_REMOVE`: 더 이상 사용하지 않기로 확정된 Figma, 전용 로컬 시각 Tool/Hub, 외부 HTML 작업면, Google Sheets 등 구형 surface는 일상 검색·라우팅 대상에서 제거한다. 삭제 전 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`를 분류하고, `UNIQUE`한 규칙·데이터·증거·재사용 원리만 현재 Notion 또는 repository 정본으로 흡수한다. 목적지 readback과 참조 신선도 검증이 끝나면 원본과 활성 참조를 제거한다. `DUPLICATE/OBSOLETE`는 재검토를 반복하지 않는다. 법적·감사·rollback 때문에 보존이 필요한 최소 이력은 명시적 archive manifest만 남기고 기본 탐색에서 제외한다.

Google Sheets는 신규 입력을 받지 않는다. 남은 고유 자료는 Project relation을 확정해 Notion 사람용 정본 또는 repository structured/runtime owner로 이관하고, `MIGRATED_READBACK_VERIFIED`가 되면 활성 호환 surface 자체를 제거 대상으로 전환한다.

`PAID_PLAN_GATE`: 현재 승인된 유료 플랜은 `GPT_PRO` 하나다. Notion은 현재 사용 가능한 무료 범위를 기본으로 하며, 기능 제한이 실제 목표를 막고 무료/기존 대안보다 유료 Notion이 장기 총비용·정확성에서 우월하다는 근거가 있을 때만 `NOTION_PAID_PLAN_PROPOSAL`로 사용자 승인을 요청한다. 승인 전에는 결제·유료 기능 의존을 만들지 않는다.

## 적대적 검토 종료 조건

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
"""
    marker = "## 11. 비용 경계"
    if marker not in text:
        raise SystemExit("long horizon insertion marker missing")
    return text.replace(marker, insertion + "\n" + marker, 1)


# 3) Adversarial skill: replace fixed minimum section with clean-exit invariant.
def adversarial_transform(text: str) -> str:
    start = text.find("### Five full adversarial improvement loop invariant")
    end = text.find("### `POST_CHANGE_MONITOR_LOOP`")
    if start < 0 or end < 0 or end <= start:
        raise SystemExit("adversarial loop section bounds missing")
    section = """### Adversarial review until clean invariant

이 Skill을 L1 이상 작업물·PR·저장소 감사·병합 후 결과의 적대적 검토로 호출하면 **고정 횟수 없이 CLEAN_REVIEW_EXIT까지 전체 검토·개선 생명주기를 반복한다.** 관점 수나 loop 수를 성과로 계산하지 않는다. 앞 회차의 수정 결과와 새 증거 자체가 다음 회차의 공격 입력이다.

```text
ADVERSARIAL_REVIEW_UNTIL_CLEAN: REQUIRED_WHEN_REVIEW_RUNS
FULL_SCOPE_REVIEW
FIND → VALIDATE → REFINE → VERIFY → RE-ATTACK
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_RECHECK
CLEAN_REVIEW_EXIT
```

한 전체 회차:

```text
FULL_SCOPE_REVIEW
→ attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck / execution verification
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ decision-report
→ RE-ATTACK resulting state
```

각 회차는 사용자 의도·핵심 방향·정본/owner/routing·Skill/Tool/Module·실제 구현·데이터·자산·실패복구·보안·동시성·비용·벤치마크·장기 유지·증거·완료조건을 전체적으로 다시 본다.

각 loop evidence:

```yaml
loop_index: 1..N
input_state_or_head:
evidence_delta: []
full_scope_findings: []
validated_findings: []
changes_applied: []
verification: []
better_alternative_result:
long_term_fit:
unresolved: []
output_state_or_head:
clean_exit_candidate: true | false
```

종료 규칙:

1. 새 유효 `MUST_FIX`, P0/P1, acceptance blocker가 하나라도 나오면 수정·검증 뒤 다음 전체 회차를 수행한다.
2. 정본·consumer·reference·Schema drift, 정상 경로 회귀, evidence ceiling 위반이 발견되면 종료하지 않는다.
3. `BETTER_ALTERNATIVE_SEARCH`와 `LONG_TERM_PLAN_FIT_RECHECK`에서 현재 승인 범위 안의 더 강한 개선이 확인되면 적용 후 다시 전체 검토한다.
4. `NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니며, 완료 조건에 필요한 증거가 없으면 clean exit가 아니다.
5. 동일 finding을 표현만 바꿔 반복 계수하거나, 횟수를 채우기 위해 가짜 finding/불필요한 변경을 만들지 않는다.
6. **전체 재공격 결과 새로운 유효 오류·충돌·누락·blocking finding이 0이고, 기존 수정 회귀 0, acceptance criteria 충족, 정본/참조 신선도와 evidence ceiling이 모두 닫힐 때만 `CLEAN_REVIEW_EXIT`다.**

구현 전 PLAN에서는 수정 대상이 아직 없을 수 있으므로 공격·검증 결과를 계약 입력으로 사용한다. 실제 BUILD/수정 뒤에는 검증된 출력 상태를 다시 전체 공격한다. PR 병합 후에도 새 `main`을 입력으로 같은 clean-exit 규칙을 적용한다.

"""
    text = text[:start] + section + text[end:]
    text = text.replace("Google Sheets 동기화", "Notion/GitHub 동기화")
    text = text.replace("실제 구현·데이터·자산·Tool/Runtime·Figma/구조화 데이터 경계", "실제 구현·데이터·자산·Tool/Runtime·Notion/repository 권위 경계")
    return text


# 4) GPT/Codex canonical policy: GPT owns planning/review; Codex is optional executor.
def codex_transform(text: str) -> str:
    marker = "## 2. GPT 책임\n"
    if marker not in text:
        raise SystemExit("GPT responsibility marker missing")
    block = """## 1A. GPT-first / optional Codex executor\n\n`GPT_FIRST_PLANNING_AND_REVIEW`가 기본 운영이다. GPT는 기획·조사·벤치마킹·대안 비교·시스템/데이터 설계·UI/UX·시각 방향·Notion 사람용 정본 갱신·검수·최종 적대적 검토를 주 책임으로 가진다. **GPT 단계가 끝났다는 이유만으로 Codex를 의무 호출하지 않는다.**\n\n`OPTIONAL_CODEX_EXECUTOR`는 다음처럼 실제 구현/실행 권위의 이점이 명확할 때만 사용한다.\n\n- 코드·Scene·Resource·game data의 실제 저장소 수정\n- 대규모 저장소를 대상으로 한 기계적 일괄 점검/변환\n- 로컬 Godot 실행·테스트·빌드·성능 확인\n- GPT가 현재 세션에서 직접 수행할 수 없는 filesystem/runtime 작업\n\nCodex를 호출하는 경우에도 GPT 실행 명세보다 현재 GitHub·Notion·프로젝트 파일·runtime evidence가 우선하며, Codex는 시작 시 이를 다시 읽는다. 사용자가 PowerShell에서 직접 시작해야 한다면 기존 `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`에 따라 **launcher + 전체 작업 prompt를 한 번에 붙여넣을 수 있는 형태**를 우선 제공한다.\n\n기획·검수·문서/Notion 정리만으로 완료 가능한 작업, 또는 GPT가 현재 도구로 직접 안전하게 완료 가능한 작업에는 Codex를 추가하지 않는다.\n\n"""
    text = text.replace(marker, block + marker, 1)
    text = text.replace("- HTML·Python 기반 기획·검증·발행 도구\n", "")
    return text


# 5) Visual PoC policy: Notion visuals are implementation input before demo when material.
def visual_transform(text: str) -> str:
    marker = "## Repository handoff and runtime evidence\n"
    if marker not in text:
        raise SystemExit("visual handoff marker missing")
    block = """## Visualized PoC / demo readiness\n\n`VISUALIZED_POC_BEFORE_DEMO_TEST`를 기본으로 한다. UI/UX, 화면 구성, 정보 가독성, 아트 분위기가 플레이 판단에 실질 영향을 주는 PoC/데모는 기획·검수 단계에서 먼저 필요한 이미지/화면 candidate를 만들거나 승인된 기존 시각 자산을 선택한다. candidate는 정확한 Project의 Notion Visual/Asset record에 배치하고 destination readback을 거친 뒤 구현 입력으로 사용한다.\n\n```text\nplanning + UX/UI flow\n→ visual requirements\n→ generate/select candidate images\n→ Notion project placement + readback\n→ approval/rejection\n→ implementation package uses approved visual inputs\n→ PoC/demo implementation\n→ runtime UX/UI/play test\n```\n\n완성 아트를 모든 로직 PoC에 강제하지 않는다. 시각 요소가 현재 가설 검증에 영향을 주지 않으면 `VISUAL_NOT_MATERIAL_TO_THIS_POC`로 기록하고 생략할 수 있다. 반대로 화면/가독성/첫인상/상호작용 의미를 검증하는 데모를 회색 박스만으로 최종 판정하지 않는다.\n\n"""
    return text.replace(marker, block + marker, 1)


# 6) Sheets policy: one-time absorb, verified migration, then remove from active discovery.
def sheets_transform(text: str) -> str:
    text = text.replace("`COMPATIBILITY_ONLY`", "`MIGRATION_ONLY_UNTIL_REMOVAL`", 1)
    marker = "## Completion\n"
    if marker not in text:
        raise SystemExit("sheets completion marker missing")
    block = """## Removal after migration\n\nGoogle Sheets는 신규 계획·수정·승인 데이터를 받지 않는 `MIGRATION_ONLY_UNTIL_REMOVAL` source다. 각 legacy Sheet는 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다. `UNIQUE`만 올바른 Project의 Notion 사람용 owner 또는 repository structured/runtime owner로 이관하고 destination readback을 검증한다. `DUPLICATE / OBSOLETE`는 활성 자료로 재검토하지 않는다.\n\n모든 unique material이 `MIGRATED_READBACK_VERIFIED`이고 active consumer/reference가 0이면 해당 Sheet와 Sheet 전용 템플릿·라우팅·기본 검색 참조는 제거한다. 법적/감사/rollback에 꼭 필요한 최소 provenance만 archive manifest에 남길 수 있으며 기본 탐색에서 제외한다.\n\n"""
    return text.replace(marker, block + marker, 1)


# 7) Regression contracts.
def long_test_transform(text: str) -> str:
    text = text.replace("FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS", "ADVERSARIAL_REVIEW_UNTIL_CLEAN")
    insertion = '''\n    def test_gpt_first_visualized_poc_legacy_removal_and_clean_review_contract(self) -> None:\n        agents = read("AGENTS.md")\n        policy = read("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md")\n        codex = read("docs/GPT_CODEX_WORKFLOW_POLICY.md")\n        visual = read("docs/VISUAL_COLLABORATION_TOOL_POLICY.md")\n        sheets = read("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md")\n        adversarial = read("skills/running-adversarial-review-and-refinement/SKILL.md")\n        for token in (\n            "ADVERSARIAL_REVIEW_UNTIL_CLEAN",\n            "CLEAN_REVIEW_EXIT",\n            "GPT_FIRST_PLANNING_AND_REVIEW",\n            "OPTIONAL_CODEX_EXECUTOR",\n            "VISUALIZED_POC_BEFORE_DEMO_TEST",\n            "LEGACY_ABSORB_VERIFY_REMOVE",\n            "PAID_PLAN_GATE",\n        ):\n            self.assertIn(token, policy if token not in ("CLEAN_REVIEW_EXIT",) else policy + adversarial + agents)\n        self.assertIn("사용자 학습형 완료보고", agents)\n        self.assertIn("GPT_FIRST_PLANNING_AND_REVIEW", codex)\n        self.assertIn("OPTIONAL_CODEX_EXECUTOR", codex)\n        self.assertIn("VISUALIZED_POC_BEFORE_DEMO_TEST", visual)\n        self.assertIn("MIGRATION_ONLY_UNTIL_REMOVAL", sheets)\n        self.assertNotIn("FULL_LOOP_COUNT_MINIMUM: 5", adversarial)\n        self.assertNotIn("FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS", adversarial)\n        self.assertNotIn("최소 다섯 번", adversarial)\n'''
    marker = "\n\nif __name__ == \"__main__\":"
    if marker not in text:
        raise SystemExit("long test footer missing")
    return text.replace(marker, insertion + marker, 1)


def codex_test_transform(text: str) -> str:
    insertion = '''\n    def test_gpt_is_primary_and_codex_is_optional_executor(self) -> None:\n        policy = (ROOT / "docs/GPT_CODEX_WORKFLOW_POLICY.md").read_text(encoding="utf-8")\n        for term in (\n            "GPT_FIRST_PLANNING_AND_REVIEW",\n            "OPTIONAL_CODEX_EXECUTOR",\n            "GPT 단계가 끝났다는 이유만으로 Codex를 의무 호출하지 않는다",\n            "ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP",\n        ):\n            self.assertIn(term, policy)\n'''
    marker = "\n\nif __name__ == \"__main__\":"
    if marker not in text:
        raise SystemExit("codex test footer missing")
    return text.replace(marker, insertion + marker, 1)


update("AGENTS.md", agents_transform)
update("docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md", long_transform)
update("skills/running-adversarial-review-and-refinement/SKILL.md", adversarial_transform)
update("docs/GPT_CODEX_WORKFLOW_POLICY.md", codex_transform)
update("docs/VISUAL_COLLABORATION_TOOL_POLICY.md", visual_transform)
update("docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md", sheets_transform)
update("tests/test_base_long_horizon_work_contract.py", long_test_transform)
update("tests/test_gpt_codex_workflow_contract.py", codex_test_transform)

# Remove this temporary migration harness after it has applied the durable changes.
Path(__file__).unlink()
print("GPT_FIRST_POLICY_MIGRATION_APPLIED")
