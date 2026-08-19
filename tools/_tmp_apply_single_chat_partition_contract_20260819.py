from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    if start not in text or end not in text:
        raise SystemExit(f"missing section marker: {start!r} -> {end!r}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + replacement.rstrip() + "\n\n" + end + after


# 1) Machine Partition contract.
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["unassigned_path_policy"] = "READ_ONLY_UNLESS_COORDINATOR_AUTHORIZED_OR_ACTIVE_WORKSTREAM_TRANSFERRED"
manifest["execution_model"] = {
    "policy": "SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS",
    "chat": "CURRENT_COORDINATOR_CHAT",
    "part_order": [f"P{i:02d}" for i in range(1, 10)],
    "part_progression": "SEQUENTIAL_CHECKPOINTS",
    "partition_semantics": "FOCUS_AND_ATTRIBUTION_VIEW",
    "required_new_part_chats": 0,
    "cross_part_repair_policy": "PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION",
    "coordinator_can_repair_cross_part": True,
    "unrelated_active_workstreams": "READ_ONLY_UNLESS_EXPLICIT_TRANSFER",
    "cross_part_repair_conditions": [
        "Identify the semantic owner and affected consumers/tests before repair",
        "The target must not be owned by an unrelated open/draft/ready workstream unless ownership is explicitly transferred",
        "The repair must serve the current authorized Base goal or regression closure",
        "Update owner-correct companions and record changed-path attribution",
        "Preserve exact-head verification and rollback",
    ],
}
manifest["collaboration_isolation"] = {
    "worker_model": "SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS",
    "github": {
        "normal_full_base_maintenance": "ONE_COORDINATOR_BRANCH_PR",
        "part_paths": "ATTRIBUTION_AND_FOCUS_NOT_HARD_WRITE_BARRIER",
        "other_open_draft_ready_workstreams": "READ_ONLY_UNLESS_EXPLICIT_TRANSFER",
        "cross_part_repair": "ALLOWED_WHEN_CURRENT_GOAL_OWNER_CONSUMER_TEST_AND_ROLLBACK_ARE_CLEAR",
    },
    "notion": {
        "hub_url": "https://app.notion.com/p/3c11b237eb1c81748c9ce43831b4f55d?pvs=204",
        "coordinator_write": "ALLOWED_FOR_CURRENT_AUTHORIZED_BASE_MAINTENANCE",
        "shared_visual_url": "https://app.notion.com/p/3c11b237eb1c81a6b773ed6726171561?pvs=204",
        "part_pages": "SEQUENTIAL_FOCUS_AND_LEARNING_SURFACES",
        "project_home_contract": "SELF_CONTAINED_HUMAN_HOME",
    },
}
integration = manifest["integration"]
integration["worker_chat_count"] = 0
integration["total_new_gpt_chats_after_task_1"] = 0
integration["new_integration_chat_count"] = 0
integration["integration_chat"] = "CURRENT_COORDINATOR_CHAT"
integration["final_confirmation_chat"] = "CURRENT_COORDINATOR_CHAT"
integration["ordered_steps"] = [
    "Run P01..P09 sequential checkpoints in CURRENT_COORDINATOR_CHAT on the current authorized maintenance branch",
    "Re-pin latest completed main at material boundaries and before merge",
    "Record each Part focus, learning checkpoint, changed-path attribution, and unresolved findings",
    "Repair validated cross-Part/CP0 findings directly when semantic ownership is clear and no unrelated open/draft/ready workstream owns the target",
    "Use CROSS_PART_CHANGE_REQUEST only for unresolved, concurrently-owned, destructive, or separately-authorized changes",
    "Review P01..P09 sequential checkpoints and promotion candidates",
    "Rebuild generated artifacts after canonical-owner changes",
    "Reconcile self-contained Notion Base/Project Home views from verified facts",
    "Run repository-wide regression and required CI",
    "Run at least 5 complete full-scope adversarial improvement loops; review lenses do not count as loops",
    "Continue additional complete loops until CLEAN_REVIEW_EXIT",
    "Exact-head merge",
    "Post-merge main and Notion readback",
]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 2) Top-level Base authority.
agents_path = ROOT / "AGENTS.md"
agents = agents_path.read_text(encoding="utf-8")
anchor = "- **`ADVERSARIAL_REVIEW_UNTIL_CLEAN`:**"
pos = agents.find(anchor)
if pos < 0:
    raise SystemExit("AGENTS adversarial anchor missing")
line_end = agents.find("\n", pos)
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in agents:
    insert = (
        "\n- **`FULL_LOOP_IS_NOT_A_REVIEW_LENS`:** `FULL_LOOP_COUNT_MINIMUM: 5`는 서로 다른 5개 관점을 한 번씩 검사하라는 뜻이 아니다. "
        "`Loop 1=scope`, `Loop 2=UX`, `Loop 3=consumer`, `Loop 4=alternatives`, `Loop 5=CI`처럼 관점을 회차로 쪼갠 검사는 5회의 full loop로 계수하지 않는다. "
        "각 계수 회차는 현행·정본·범위 재확인 → material decision의 최소 3개 실질 대안/현행 비교 → 전체 attack → critique 검증 → 승인 finding 개선 → 실제 verify/regression → BETTER_ALTERNATIVE_SEARCH → LONG_TERM_PLAN_FIT_RECHECK → 개선된 전체 상태 재공격을 모두 수행해야 한다. "
        "회차 보고에서 가장 큰 finding을 강조할 수는 있지만 그것이 해당 회차의 유일한 검토 관점이어서는 안 된다.\n"
        "- **`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`:** Base 전면 유지보수/최적화에서 P01~P09는 별도 채팅·쓰기 장벽이 아니라 집중 검토·학습·변경 attribution 단위다. 기본은 한 `CURRENT_COORDINATOR_CHAT`에서 `P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09` 순차 checkpoint로 진행한다. "
        "`PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION`: 현재 승인 Goal에서 다른 Part/CP0의 유효 결함을 발견했고 semantic owner·consumer·test·rollback이 명확하면 같은 총괄 작업에서 직접 수정할 수 있다. 단, 다른 open/draft/ready PR·branch·worktree가 이미 그 경로/의미를 소유하면 최신 사용자 지시로 ownership이 이전되지 않는 한 read-only다.\n"
    )
    agents = agents[: line_end + 1] + insert + agents[line_end + 1 :]
agents_path.write_text(agents, encoding="utf-8")

# 3) Human operating model.
model_path = ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md"
model = model_path.read_text(encoding="utf-8")
model = model.replace(
    "Base 전체를 여러 GPT 채팅이 동시에 깊게 최적화하더라도 **정본·Skill·Module·Test·PR 소유권이 충돌하지 않도록** 책임 경계를 고정한다.",
    "Base 전체를 한 GPT 총괄 채팅이 P01~P09 책임 관점을 순차적으로 깊게 검토하더라도 **정본·Skill·Module·Test·PR 책임과 변경 이유가 흐려지지 않도록** 집중 경계를 고정한다.",
)
model = replace_between(
    model,
    "## 채팅·GitHub·Notion 충돌 격리\n",
    "## CP0 · Base Control Plane",
    """## 한 채팅 순차 실행과 실제 충돌 격리

`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
                         ↓
                    Whole-Base Integration
```

- Base 전면 유지보수/최적화는 **한 `CURRENT_COORDINATOR_CHAT`**에서 P01→P09를 순차 checkpoint로 진행한다. 새 Part별 채팅은 요구하지 않는다.
- Part는 전문 초점, Learning Log, Source Radar, changed-path attribution을 위한 안정된 책임 View다.
- `PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION`: 다른 Part라는 이유만으로 현재 발견한 유효 오류를 미루지 않는다.
- 현재 승인 Goal 안에서 semantic owner, 실제 consumer/test, 영향 범위, rollback이 명확하면 coordinator가 다른 Part/CP0 경로도 같은 작업에서 직접 수정할 수 있다.
- `CROSS_PART_CHANGE_REQUEST`는 이제 모든 cross-Part finding의 강제 경로가 아니다. unresolved, destructive, separate authorization 필요, 또는 다른 active owner와 충돌할 때 사용한다.
- **별도 진행 중 workstream 보호는 계속 강제한다.** 다른 open/draft/ready PR·branch·worktree가 같은 경로나 의미를 소유하면 explicit ownership transfer 전에는 read-only다.
- Notion Base Hub와 Part 페이지는 같은 coordinator가 현재 승인된 Base 작업 안에서 순차 갱신할 수 있다. 프로젝트 고유 자료는 정확한 Project relation에만 쓴다.
- GitHub는 structured/runtime truth, Notion은 self-contained human-facing projection이라는 권위 분리는 유지한다.

### 왜 9개 Part를 유지하는가

Part를 없애면 채팅 수는 줄지만 어떤 책임을 충분히 깊게 봤는지, 어떤 Skill/Module이 학습되었는지, Source Radar가 어느 영역을 보강해야 하는지 추적하기 어렵다. 따라서 **Part ID는 유지하되 채팅·쓰기 장벽은 제거**한다.

### 재검토 조건

한 채팅이 practical context를 반복적으로 초과하거나, 동시 인간/agent writer가 상시화되거나, cross-Part 변경량이 review 가능한 범위를 지속적으로 넘으면 다중 workstream 모델을 다시 Trade Study한다.
""",
)
model = replace_between(
    model,
    "## 병렬 실행\n",
    "## 파일 상태 모델",
    """## 순차 실행

과거 G1/G2/G3 병렬 묶음은 책임 관계를 이해하는 분석 그룹으로만 남기고, 기본 실행 권위는 아니다.

```text
CURRENT_COORDINATOR_CHAT
→ P01 Foundation/Planning checkpoint
→ P02 Skill/Canon/Legacy checkpoint
→ P03 Quality/Git checkpoint
→ P04 Game Design checkpoint
→ P05 Visual/UX checkpoint
→ P06 Godot/Runtime checkpoint
→ P07 Validation/Release checkpoint
→ P08 AI/Executor checkpoint
→ P09 Content/Narrative checkpoint
→ Whole-Base Integration
```

각 checkpoint는 최신 completed `main`, 진행 중 독립 PR, 정본/consumer/test를 다시 확인한다. cross-Part 수정이 필요하면 동일 coordinator가 owner-correct 변경으로 처리하되 active foreign workstream은 침범하지 않는다.
""",
)
model = replace_between(
    model,
    "## Integration\n",
    "## Rollback",
    """## Integration

별도 Integration 채팅은 없다. 같은 `CURRENT_COORDINATOR_CHAT`이 P01~P09 순차 checkpoint를 끝낸 뒤 다음을 수행한다.

1. latest completed `main`과 현재 branch exact head 확인
2. P01..P09 sequential checkpoints, Learning Logs, promotion candidates 재검토
3. 이미 직접 해결한 cross-Part finding과 남은 `CROSS_PART_CHANGE_REQUEST` 중복 제거
4. CP0/Registry/Documentation Map/generated surface를 canonical owner에서 한 번만 정리
5. self-contained Notion Base/Project Home 갱신·readback
6. 전체 Base 회귀검증과 Required CI
7. `FULL_LOOP_IS_NOT_A_REVIEW_LENS`를 적용한 최소 5회의 **완전한 전체 적대적 개선 loop**
8. 오류가 남으면 6..N회 계속
9. exact-head merge
10. post-merge main/Notion readback
""",
)
model_path.write_text(model, encoding="utf-8")

# 4) Sequential worker prompt (still named for compatibility).
worker_path = ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md"
worker_path.write_text("""# Base P01~P09 순차 최적화 — GPT 작업지시문

Base는 하나의 통합 시스템이며 이 채팅은 하나의 `CURRENT_COORDINATOR_CHAT`에서 P01~P09를 순차적으로 깊게 검토한다.

`PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION`
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`
`PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION`

## 0. 실행 순서

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09
```

각 Part는 별도 채팅이나 hard write barrier가 아니라 **전문 초점·Learning·Source·변경 attribution checkpoint**다. 각 checkpoint 시작 시 최신 completed `main`, `AGENTS.md`, Manifest, Context Pack, 관련 Skill/Module/Test, 같은 Goal의 열린·최근 PR을 다시 읽는다.

## 1. 수정 권한

- 현재 승인 Goal에서 발견한 유효 결함은 다른 Part/CP0라는 이유만으로 미루지 않는다.
- semantic owner, consumer/test, 영향 범위, rollback이 명확하면 같은 coordinator branch/PR에서 owner-correct하게 직접 수정할 수 있다.
- `CROSS_PART_CHANGE_REQUEST`는 unresolved, destructive, 별도 사용자 결정, 또는 concurrent ownership이 있을 때만 사용한다.
- **다른 open/draft/ready PR·branch·worktree가 같은 경로나 의미를 이미 소유하면 explicit ownership transfer 전에는 read-only다.** 그 active workstream 자체를 rebase/merge/close/rewrite하지 않는다.
- completed/merged `main` 변경은 정상적인 통합 입력이다.

## 2. GPT / Codex

GPT가 기본 작업자다. 현행조사·기획·최소 3개 실질 대안·벤치마킹·규칙/Skill/Module 검토·Notion/GitHub 대조·검수·적대적 검토를 GPT에서 닫는다.

`OPTIONAL_CODEX_EXECUTOR`는 실제 filesystem/code/Scene/Resource/data 변경, 대규모 기계 점검, 로컬 runtime/build test가 필요할 때만 사용한다.

## 3. 각 Part checkpoint

각 Pxx에서 최소 다음을 수행한다.

1. 역할·입력·출력·consumer·test 복원
2. 중요 규칙 3~10개와 canonical owner 확인
3. Skill/Mode를 `KEEP / IMPROVE / MERGE / ABSORB / SPLIT / RECLASSIFY / DEPRECATE / ARCHIVE / BLOCKED_UNVERIFIED`로 판정
4. Module의 cohesion/coupling/interface/canonical owner/독립검증성 확인
5. material decision에는 `MINIMUM_VIABLE_ALTERNATIVES: 3`
6. `BETTER_ALTERNATIVE_SEARCH`
7. `LONG_TERM_PLAN_FIT_REQUIRED` + revisit conditions
8. 관련 Source Radar/원출처 조사와 Learning Checkpoint
9. Notion human-facing 설명을 최신 verified fact로 갱신
10. 변경 attribution과 실제 Test/NOT_RUN 기록

## 4. Notion

Base Home과 Project Home은 `SELF_CONTAINED_HUMAN_HOME`을 따른다. 사용자가 핵심 이해를 위해 하위 페이지를 열 필요가 없어야 한다.

Base Home에는 중요 규칙, 모든 핵심 Skill/Mode의 목적·trigger·작동·출력·기대효과·Module/Test 연결, Module flow, P01~P09 책임/흐름/연결/효과, 현재 위험/다음 작업을 직접 설명한다.

Project Home에는 최소 `CURRENT_DIRECTION_STATUS`, `PLAYER_OR_USER_PROMISE`, `CORE_LOOP`, `MAJOR_SYSTEMS_AND_CONNECTIONS`, `UX_UI_AND_VISUAL_DIRECTION`, `IMPLEMENTATION_RUNTIME_EVIDENCE`, `IMPORTANT_DECISIONS`, `RISKS_BLOCKERS`, `NEXT_WORK`를 직접 설명한다. 모르는 내용은 `UNVERIFIED / NOT_DEFINED / IN_PROGRESS`로 둔다.

하위 페이지는 상세 evidence/data/editing surface이지 기본 이해를 위한 필수 navigation이 아니다.

## 5. Legacy / 비용

Figma, 신규 Google Sheets, external HTML workspace, 폐기 local visual Tool/Hub를 기본 surface로 부활시키지 않는다. `UNIQUE / DUPLICATE / OBSOLETE` 분류와 destination readback 후 lifecycle을 결정한다.

기본 유료 플랜은 `GPT_PRO`; 신규 유료 API/SaaS는 사용자 승인 전 도입하지 않는다.

## 6. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

**관점 하나만 검사한 것은 full loop로 계수하지 않는다.** 예를 들어 다음은 잘못된 계수다.

```text
Loop 1 = scope
Loop 2 = UX
Loop 3 = consumer
Loop 4 = alternatives
Loop 5 = CI
```

각 계수 회차는 전체 승인 상태에 대해 반드시 다음 완전한 lifecycle을 수행한다.

```text
현행·정본·범위 재확인
→ material decision의 최소 3개 실질 대안/현행 비교
→ ATTACK whole state
→ VALIDATE critique
→ FIX/REFINE approved findings
→ VERIFY / REGRESSION
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK resulting whole state
```

1~5회는 의무 full loop다. 5회 이후 새 유효 오류·충돌·누락·blocking finding·회귀·acceptance failure가 하나라도 있으면 6..N회 계속한다. 최대 횟수는 없다. 최소 5회 완료 뒤 새 blocker 0, 회귀 0, acceptance/정본/evidence 조건 충족일 때만 `CLEAN_REVIEW_EXIT`다.

## 7. 완료보고

Part별 checkpoint와 최종 전체 Integration 보고에서:

- Part/Module/Skill이 무엇인지
- 왜 필요한지와 언제 작동하는지
- BEFORE → AFTER → 기대효과 → trade-off
- 최소 3개 대안과 선택 이유
- 실제 Test / NOT_RUN / BLOCKED_UNVERIFIED
- Learning / Source 적용
- 다른 Part까지 직접 수정한 경우 semantic owner와 이유
- 보호한 active workstream
- revisit conditions

을 사용자 학습형으로 설명한다.
""", encoding="utf-8")

# 5) Integration prompt.
integration_path = ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md"
integration_path.write_text("""# Base P01~P09 순차 Integration — GPT 작업지시문

`PARTITION_IS_MAINTENANCE_AND_SPECIALIZATION_VIEW_NOT_RUNTIME_FRAGMENTATION`
`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`
`PART_BOUNDARY_IS_FOCUS_NOT_REPAIR_PROHIBITION`

`CURRENT_COORDINATOR_CHAT` 하나가 P01→P09 순차 checkpoint와 최종 ONE BASE Integration을 모두 책임진다.

```text
P01 → P02 → P03 → P04 → P05 → P06 → P07 → P08 → P09 → Whole-Base Integration
```

## 입력

- latest completed main exact SHA
- current coordinator branch/PR exact head
- Manifest + P01..P09 Context Packs/Learning Logs
- merged/completed Part evidence
- unresolved `CROSS_PART_CHANGE_REQUEST`
- same-goal open/draft/ready PR inventory
- Notion Base Home + affected Project Home

## Cross-Part 처리

다른 Part라는 이유만으로 유효 finding을 남겨두지 않는다. semantic owner, consumer/test, 영향 범위, rollback이 명확하고 별도 active workstream이 소유하지 않으면 coordinator가 직접 owner-correct 수정한다.

`CROSS_PART_CHANGE_REQUEST`는 unresolved, concurrent ownership, destructive change, 또는 별도 사용자 결정이 필요할 때만 유지한다.

다른 open/draft/ready PR·branch·worktree는 explicit ownership transfer 전까지 read-only다.

## Notion

Base/Project Home은 `SELF_CONTAINED_HUMAN_HOME`이어야 한다. 핵심 이해를 하위 페이지 navigation에 의존시키지 않는다. GitHub는 structured/runtime truth, Notion은 human-facing explanation/visual/learning projection이다.

## 검증

- Partition contract / changed-domain focused tests
- scope checker는 Part attribution과 전체 Integration diff 감사에 사용
- Base v9/global integrity
- canonical reference freshness
- generated artifacts
- Required CI
- unresolved review thread 0
- exact-head verification
- Notion destination readback

실행하지 않은 runtime/device/human/store evidence는 PASS가 아니다.

## 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
FULL_LOOP_IS_NOT_A_REVIEW_LENS
```

관점 하나만 검사한 것은 full loop로 계수하지 않는다. `Loop 1 = scope / Loop 2 = UX / Loop 3 = consumer / Loop 4 = alternatives / Loop 5 = CI` 같은 분할은 금지한다.

각 회차는 **전체 결과 상태**를 대상으로:

```text
현행·정본·범위
→ 최소 3개 실질 대안/현행 비교(해당 material decision)
→ attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck / execution verification
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK resulting state
```

를 모두 수행한다. 최소 5회 뒤에도 유효 blocker가 있으면 6..N회 계속한다. 새 valid blocker 0, regression 0, acceptance/정본/evidence 조건이 닫혀야 `CLEAN_REVIEW_EXIT`다.

## Merge / post-merge

`CLEAN_REVIEW_EXIT`, Required CI, unresolved thread 0, exact head를 확인한 뒤 merge한다. 새 `main`과 Notion Home을 다시 읽은 뒤에만 완료를 보고한다.
""", encoding="utf-8")

# 6) Self-contained project Home machine contract.
authority_path = ROOT / "docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json"
authority = json.loads(authority_path.read_text(encoding="utf-8"))
authority["project_home_contract"] = "SELF_CONTAINED_HUMAN_HOME"
authority["child_pages_optional_for_basic_understanding"] = True
authority["project_home_required_sections"] = [
    "CURRENT_DIRECTION_STATUS",
    "PLAYER_OR_USER_PROMISE",
    "CORE_LOOP",
    "MAJOR_SYSTEMS_AND_CONNECTIONS",
    "UX_UI_AND_VISUAL_DIRECTION",
    "IMPLEMENTATION_RUNTIME_EVIDENCE",
    "IMPORTANT_DECISIONS",
    "RISKS_BLOCKERS",
    "NEXT_WORK",
]
authority["unknown_fact_policy"] = "USE_UNVERIFIED_NOT_DEFINED_OR_IN_PROGRESS_NEVER_INVENT_CANON"
authority["child_page_role"] = "DEEP_EVIDENCE_DATA_AND_EDITING_NOT_REQUIRED_FOR_BASIC_UNDERSTANDING"
authority_path.write_text(json.dumps(authority, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# 7) Project OS owner.
project_os_path = ROOT / "skills/managing-game-project-operating-system/SKILL.md"
project_os = project_os_path.read_text(encoding="utf-8")
if "SELF_CONTAINED_HUMAN_HOME" not in project_os:
    marker = "## HiGodot provider adoption contract\n"
    if marker not in project_os:
        raise SystemExit("project OS insertion marker missing")
    section = """## Self-contained Project Home contract

`SELF_CONTAINED_HUMAN_HOME`

Project Notion Home은 사용자가 **하위 페이지를 열지 않아도** 현재 프로젝트를 읽고 다음 작업을 이해할 수 있는 기본 인간용 설명면이다. 하위 페이지/DB는 깊은 evidence·data·editing surface이며 기본 이해를 위한 필수 navigation이 아니다.

Home에 최소 다음을 직접 설명한다.

- `CURRENT_DIRECTION_STATUS`: 현재 단계, 최신 정본/동기화 상태
- `PLAYER_OR_USER_PROMISE`: 사용자가 무엇을 느끼거나 얻어야 하는가
- `CORE_LOOP`: 반복 행동·결정·보상/진행 흐름
- `MAJOR_SYSTEMS_AND_CONNECTIONS`: 주요 시스템과 상호작용
- `UX_UI_AND_VISUAL_DIRECTION`: 화면/정보/아트 방향과 현재 승인 상태
- `IMPLEMENTATION_RUNTIME_EVIDENCE`: 실제 구현·runtime/build/test 증거와 evidence ceiling
- `IMPORTANT_DECISIONS`: 현재 작업을 바꾸는 핵심 확정사항
- `RISKS_BLOCKERS`: 미검증·충돌·막힘
- `NEXT_WORK`: 다음 의미 있는 작업과 재검토 조건

신규/빈 프로젝트처럼 근거가 없으면 내용을 추정하지 않고 `UNVERIFIED`, `NOT_DEFINED`, `IN_PROGRESS`를 명시한다. Home의 요약이 구조화 데이터·코드·Scene·Test 의미를 바꾸면 Repository 정본과 동기화한 뒤 구현한다.

"""
    project_os = project_os.replace(marker, section + marker, 1)
project_os_path.write_text(project_os, encoding="utf-8")

# 8) Adjust the RED contract to respect the active P03 workstream: top-level AGENTS owns the correction now.
test_path = ROOT / "tests/test_base_partition_contract.py"
test = test_path.read_text(encoding="utf-8")
test = test.replace(
    'ADVERSARIAL_SKILL = ROOT / "skills" / "running-adversarial-review-and-refinement" / "SKILL.md"\n',
    'AGENTS = ROOT / "AGENTS.md"\n',
)
test = test.replace(
    '        adversarial = ADVERSARIAL_SKILL.read_text(encoding="utf-8")\n',
    '        adversarial = AGENTS.read_text(encoding="utf-8")\n',
)
test_path.write_text(test, encoding="utf-8")

print("SINGLE_CHAT_PARTITION_CONTRACT_APPLIED")
