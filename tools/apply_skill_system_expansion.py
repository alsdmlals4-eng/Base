from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def clean(text: str) -> str:
    return textwrap.dedent(text).strip() + "\n"


def write(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(clean(text), encoding="utf-8")


def append_once(relative: str, marker: str, text: str) -> None:
    path = ROOT / relative
    current = path.read_text(encoding="utf-8")
    if marker not in current:
        path.write_text(current.rstrip() + "\n\n" + clean(text), encoding="utf-8")


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    current = path.read_text(encoding="utf-8")
    if old not in current:
        raise RuntimeError(f"Anchor not found in {relative}: {old[:80]!r}")
    path.write_text(current.replace(old, new, 1), encoding="utf-8")


# ---------------------------------------------------------------------------
# Compact existing skills while preserving their unique contracts in references.
# ---------------------------------------------------------------------------

write(
    "skills/identifying-project-core/SKILL.md",
    r'''
    ---
    name: identifying-project-core
    description: Use when an existing project needs an evidence-based, read-only determination of which experiences, loops, systems, rules, directions, or technical foundations are identity-defining project core rather than replaceable content, MVP support, or implementation detail.
    ---

    # Identifying Project Core

    ## Purpose and boundary

    프로젝트 코어는 제거하거나 본질적으로 바꾸면 같은 프로젝트라고 보기 어려운 최소 정체성·경험·시스템 중심부다. 현재 구현, 높은 제작비, 중요해 보인다는 인상만으로 코어를 확정하지 않는다.

    기본 Work Mode는 `PLAN` 또는 `REVIEW`이며 **읽기 전용**이다. 새 코어의 제안·사용자 승인은 `establishing-project-core`, 실제 변경 검증은 `reviewing-and-validating-project-changes`가 책임진다.

    ## Skill Modes

    `inventory → extract-candidates → dependency-map → removal-and-change-test → classify → core-report`

    ## Required inputs

    ```yaml
    project_identity_and_goal:
    approved_design_and_decisions:
    actual_code_data_assets_tests:
    player_actions_choices_feedback:
    core_loop_and_major_systems:
    technical_dependencies:
    mvp_scope:
    conflicts_and_unknowns:
    ```

    근거가 없으면 `UNVERIFIED`, 일부만 확인되면 `PARTIAL`, 문서·승인·구현이 충돌하면 `CONFLICTED`다.

    ## Classification

    - `PROJECT_CORE`: 제거·본질 변경 시 프로젝트 정체성이 달라진다.
    - `CORE_SUPPORT`: 코어를 운영·이해·확장하지만 대체 가능하다.
    - `MVP_SUPPORT`: 핵심 가설 검증에는 필요하지만 정체성 코어는 아니다.
    - `CONTENT_VARIANT`: 코어 규칙을 표현하는 교체 가능한 콘텐츠다.
    - `PRESENTATION_SHELL`: UI·대사·스킨·연출 등 교체 가능한 외피다.
    - `TECHNICAL_FOUNDATION`: 여러 기능이 의존하는 기술 기반이며 제품 코어와 분리한다.
    - `CONFLICTED` / `UNVERIFIED`: 충돌 또는 근거 부족이다.

    세부 층·증거 우선순위·제거·대체·변경 질문은 `references/classification-and-tests.md`를 필요할 때만 읽는다.

    ## Output contract

    ```md
    ## 판정 상태
    ## 프로젝트 정체성 한 문장
    ## 기획·시스템·기술 코어
    ## 코어가 아닌 변경 가능 요소
    ## 코어 기능과 MVP 지원 기능
    ## 후보별 제거·대체·변경 테스트
    ## 의존 관계와 근거
    ## 충돌·미검증·변경 영향
    ## 다음 단계
    ```

    ## Quality gate

    - 기획·시스템·기술 코어를 구분한다.
    - 모든 후보에 실제 근거와 `removal-and-change-test`가 있다.
    - 코어가 아닌 요소도 명시해 보호 범위 팽창을 막는다.
    - 사용자 승인 없이 책임 원본을 수정하거나 확정하지 않는다.
    - 결과는 `IDENTIFIED / PARTIAL / CONFLICTED / UNVERIFIED` 중 하나다.

    ## Failure conditions

    기능 목록 전체를 코어로 만들거나, 기술 의존성을 제품 정체성과 혼동하거나, UI·분량·임시 구현을 불변 코어로 고정하거나, 코어와 `MVP_SUPPORT`를 혼동하면 실패다.

    Learning Log: `skills/SKILL_LEARNING_LOG.md`
    '''
)

write(
    "skills/identifying-project-core/references/classification-and-tests.md",
    r'''
    # 프로젝트 코어 상세 판정표

    ## 코어 층

    - 기획 코어: 핵심 행동·선택·감정·판타지·금지 방향.
    - 시스템 코어: 입력과 자원 → 핵심 행동 → 상태 변화 → 활용·보상 → 다음 행동의 중심 순환.
    - 기술 기반: 상태·저장·생성·판정·이벤트·공통 ID와 Schema. 기술 중심성이 곧 제품 정체성은 아니다.

    ## 증거 우선순위

    최신 사용자 승인 → 등록된 책임 원본 → 결정·현재 상태 → 실제 코드·데이터·자산·테스트 → 과거 문서·외부 설명.

    ## 제거·대체·변경 테스트

    1. 제거하면 핵심 행동과 플레이어 약속이 성립하는가?
    2. 다른 방식으로 대체해도 같은 경험인가?
    3. 축소하면 뾰족한 재미와 반복 동기가 유지되는가?
    4. 변경하면 장르·판타지·사용자 약속이 달라지는가?
    5. 다른 주요 시스템이 끊기거나 의미를 잃는가?
    6. 표현 외피나 콘텐츠 수량처럼 교체 가능한가?
    7. 구현 방식만 바뀌고 제품 의미는 유지되는가?

    ## Core와 MVP

    - `CORE`: 정체성과 핵심 경험에 필수.
    - `MVP_SUPPORT`: 정체성은 아니지만 핵심 가설을 실행·관찰하는 데 필수.
    - `BOTH`: 코어이며 현재 MVP에도 필요.
    - `LATER`: 코어도 아니고 현재 검증에도 불필요.
    '''
)

write(
    "skills/establishing-project-core/SKILL.md",
    r'''
    ---
    name: establishing-project-core
    description: Use in PLAN work when a new or changing project needs its identity-defining player promise, core actions, core loop, system anchors, invariants, changeable shell, and required technical foundations proposed, stress-tested, explicitly approved, and recorded as the project core contract.
    ---

    # Establishing Project Core

    ## Purpose and authority

    프로젝트 코어 확정은 앞으로 보호할 **최소 정체성 계약**을 정하는 일이다. AI는 후보를 제안하고 반례를 검사할 수 있지만, 사용자 승인 없이 `CORE_CONFIRMED`로 표시하지 않는다.

    기존 프로젝트의 사실 판정은 `identifying-project-core`, 컨셉·PoC 탐색은 `analyzing-and-refining-game-concepts`, 승인 계약의 문서화는 `managing-design-documents`가 책임진다.

    ## Skill Modes and state

    `propose → stress-test → confirm → lock`, 새 근거가 생기면 `reopen`한다.

    `CORE_SEED → CORE_PROPOSED → CORE_STRESS_TESTED → CORE_CONFIRMED | CORE_REVISE | CORE_REJECTED → CORE_RECORDED`

    `confirm`과 `lock`은 명시적 사용자 승인 없이는 실행하지 않는다.

    ## Required inputs

    ```yaml
    goal_problem_and_target_player:
    candidate_concept_and_player_promise:
    core_actions_choices_feedback:
    candidate_core_loop_and_systems:
    world_visual_tone_invariants:
    technical_foundations:
    constraints_and_capacity:
    mvp_poc_playtest_evidence:
    alternatives_and_rejected_directions:
    approval_authority:
    ```

    ## Protection boundary

    - `INVARIANT`: 바뀌면 프로젝트 정체성이 달라진다.
    - `CHANGEABLE`: 코어를 유지한 채 교체·조정할 수 있다.
    - `REQUIRES_REAPPROVAL`: 영향 분석과 사용자 재승인이 필요하다.
    - `OUT_OF_SCOPE`: 현재 코어 계약에 포함하지 않는다.

    세부 계약 필드·반례·상태 전이·재개 조건은 `references/core-contract-and-state.md`를 필요할 때만 읽는다.

    ## Workflow

    1. 정체성 한 문장, 핵심 행동·선택·피드백, 코어 루프와 중심 시스템을 제안한다.
    2. 제거·대체·실패·확장 반례로 최소성과 일관성을 공격한다.
    3. 코어 기능과 `MVP_SUPPORT`, 기술 코어와 대체 가능한 구현을 분리한다.
    4. 사용자 승인·수정·기각을 기록한다.
    5. 승인된 항목만 책임 원본·개발 게이트·검수 기준에 연결한다.

    ## Output contract

    ```md
    ## 상태와 사용자 승인 기록
    ## 프로젝트 정체성·대상 플레이어·핵심 약속
    ## 핵심 행동·선택·피드백과 코어 루프
    ## 중심 시스템·기술 기반
    ## INVARIANT·CHANGEABLE·REQUIRES_REAPPROVAL·OUT_OF_SCOPE
    ## 코어 기능과 MVP 지원 기능
    ## PoC·플레이테스트 근거와 실패 조건
    ## 제외 후보·미검증·재개 조건
    ## 책임 원본·게이트·검수 연결
    ```

    ## Quality gate

    코어를 기능 목록으로 팽창시키지 않고, 불변 조건과 변경 가능한 외피를 구분하며, 반례와 근거를 기록하고, **사용자 승인 없이** `CORE_CONFIRMED` 또는 `CORE_RECORDED`로 전환하지 않는다.

    Learning Log: `skills/SKILL_LEARNING_LOG.md`
    '''
)

write(
    "skills/establishing-project-core/references/core-contract-and-state.md",
    r'''
    # 코어 확정 상세 계약

    ## 계약 필드

    - 정체성: 한 문장 약속, 대상 플레이어, 차별 원리, 바뀌면 다른 프로젝트가 되는 경계.
    - 핵심 경험: 반복 행동·판단·선택·즉시 피드백·다음 행동 동기·감정과 판타지.
    - 시스템: 코어 루프, 시스템 입력·출력, 상태 변화, 결과 사용처, 콘텐츠 연결 인터페이스.
    - 기술: 반드시 보존할 데이터·호환성 계약과 대체 가능한 구현을 분리.

    ## 스트레스 테스트

    제거, 대체, 극단적 축소, 콘텐츠 확장, 기술 교체, 제작 제약, PoC 반증 상황에서도 정체성 계약이 성립하는지 확인한다.

    ## 재개 조건

    - 사용자가 방향 변경을 명시했다.
    - PoC·플레이테스트가 핵심 가설을 반복 반증했다.
    - 제작·기술·법적 제약으로 핵심 경험이 성립하지 않는다.
    - 구현과 코어가 장기간 충돌하거나 기존 코어 문장끼리 모순된다.

    재확정 전에는 기존 코어와 새 후보, 영향·마이그레이션·중단 기준을 분리한다.
    '''
)

write(
    "skills/running-adversarial-review-and-refinement/SKILL.md",
    r'''
    ---
    name: running-adversarial-review-and-refinement
    description: Use when a design, plan, document, code proposal, data change, UX flow, or other work product should be attacked as if it failed, its criticisms independently validated, only justified findings refined, and the revised result regression-checked without changing project core or adding unnecessary scope.
    ---

    # Running Adversarial Review and Refinement

    ## Purpose and separation

    적대적 검토는 승인 거부 증거를 찾는 공격 단계다. 그러나 **비판도 오류·취향·과잉 요구**일 수 있으므로 공격과 검증을 분리하고, 검증된 문제만 최소 수정한다.

    실제 diff·정적·런타임·접근성·성능 증거는 `reviewing-and-validating-project-changes`, 프로젝트 코어 판정·확정은 관련 코어 Skill이 책임진다.

    ## Workflow

    `attack → validate-critique → refine-approved-findings → regression-recheck → decision-report`

    기본 Work Mode는 `REVIEW → 필요한 경우 BUILD → REVIEW`다. 같은 수행자가 맡아도 단계별 입력과 출력을 섞지 않는다.

    ## Required inputs

    ```yaml
    work_product:
    approved_requirements_and_scope:
    project_core:
    canonical_sources_and_actual_diff:
    acceptance_criteria:
    protected_strengths_and_assets:
    constraints_and_validation_environment:
    change_authority:
    ```

    코어가 확정되지 않았다면 핵심 충돌은 `UNVERIFIED`로 둔다.

    ## Finding decisions

    - `MUST_FIX`: 완료·안전·정합성을 막는 검증된 결함.
    - `SHOULD_FIX`: 범위 안에서 가치가 크고 회귀 위험이 통제된다.
    - `DEFER`: 유효하지만 현재 범위·근거·비용상 보류한다.
    - `REJECT`: 취향, 중복, 잘못된 전제, 범위 밖 요구다.
    - `UNVERIFIED`: 증거가 부족하다.

    상세 공격 렌즈·판정표·회귀 프로토콜은 `references/finding-and-regression-protocol.md`를 필요할 때만 읽는다.

    ## Rules

    1. `attack`은 실패·모순·악용·누락·경계 조건을 최대한 찾는다.
    2. `validate-critique`는 사실성, 발생 가능성, 영향, 범위, 수정 비용을 재판정한다.
    3. `refine-approved-findings`는 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정한다.
    4. `regression-recheck`는 기존 장점·정상 경로·코어·범위와 새 결함을 다시 공격한다.
    5. `decision-report`는 반영·보류·기각·미검증과 남은 위험을 모두 기록한다.

    ## Output contract

    ```md
    ## 공격 관점과 실패 가정
    ## finding·근거·심각도
    ## MUST_FIX / SHOULD_FIX / DEFER / REJECT / UNVERIFIED
    ## 실제 반영한 최소 변경
    ## 보호한 코어·장점·범위
    ## regression-recheck 결과
    ## 남은 위험·미검증·다음 조건
    ```

    ## Quality gate

    `MUST_FIX`·`SHOULD_FIX` 외 항목을 몰래 반영하지 않고, 프로젝트 코어를 바꾸거나 기능을 팽창시키지 않으며, 수정 뒤 `regression-recheck`를 수행한다.

    Learning Log: `skills/SKILL_LEARNING_LOG.md`
    '''
)

write(
    "skills/running-adversarial-review-and-refinement/references/finding-and-regression-protocol.md",
    r'''
    # 적대적 finding·회귀 상세 프로토콜

    ## 공격 렌즈

    요구·범위, 사실·정본, 논리·모순, 사용자 경로, 실패·경계·악용, 데이터·호환성, 접근성·성능, 제작 비용, 유지보수성, 설명 가능성을 순서대로 공격한다.

    ## finding 검증

    각 지적에 재현 조건, 근거, 실제 영향, 발생 가능성, 현재 범위, 보호 대상, 최소 수정, 검증 방법을 붙인다. 해결책이 큰 경우 문제의 유효성과 구현 승인을 분리한다.

    ## 회귀 재검토

    - 원래 finding이 실제로 사라졌는가?
    - 정상 경로와 기존 장점이 유지되는가?
    - 프로젝트 코어·승인 범위·정본이 바뀌지 않았는가?
    - 새 중복·복잡성·접근성·성능·호환성 문제가 생기지 않았는가?
    - 실행하지 못한 검사는 `UNVERIFIED`로 남았는가?
    '''
)

write(
    "skills/evolving-project-discipline-skills/SKILL.md",
    r'''
    ---
    name: evolving-project-discipline-skills
    description: Use when creating, reviewing, consolidating, or improving project Foundation and discipline skills from actual work and validation evidence while keeping the Registry, entrypoints, tests, references, and human derivatives synchronized.
    ---

    # Evolving Project Discipline Skills

    ## Core principle

    **Consolidation-first**: 새 Skill을 만들기 전에 기존 Skill mode·reference 확장으로 해결 가능한지 확인한다. 독립 입력·산출물·품질 기준·도구·승인 경계가 있을 때만 분리한다.

    가지치기 자체는 `pruning-stale-and-nonfunctional-material`, 본문 압축은 `simplifying-skill-bodies`, 기능 보존 구조 변경은 `refactoring-with-contract-preservation`이 책임진다.

    ## Skill Modes

    `inventory → decide-boundary → create-or-integrate → register → verify → learn`

    ## Required inputs

    ```yaml
    skill_registry_and_entrypoints:
    existing_skills_references_scripts:
    legacy_aliases:
    learning_and_failure_evidence:
    actual_work_examples:
    validation_and_publication_paths:
    ```

    ## Boundary decision

    1. 기존 통합 Skill의 mode로 처리 가능한가?
    2. trigger·mode·reference 확장으로 해결 가능한가?
    3. 독립 입력·산출물·Quality Bar·검증·승인 경계가 있는가?
    4. 여러 작업에서 반복될 책임인가?

    세부 인벤토리·통합 전 보존표·Health Review는 `references/consolidation-and-health-review.md`를 필요할 때만 읽는다.

    ## Workflow

    1. Registry·실제 패키지·entrypoint·Learning Log를 대조한다.
    2. 중복, 과분할, 누락, 죽은 자료, 과도한 기본 로드를 판정한다.
    3. 고유 기능·입력·산출물·검증을 먼저 보존한다.
    4. Skill·mode·reference 중 가장 작은 책임 단위로 생성 또는 통합한다.
    5. `load_by_default=false`, trigger, use/do-not-use, Learning Log를 등록한다.
    6. `auditing-canonical-reference-freshness`와 `managing-game-project-operating-system` verify를 실행한다.

    ## Output contract

    ```md
    ## 통합 전·후 구조와 활성 Skill 수
    ## 유지·추가·통합·제거한 책임과 이유
    ## 고유 기능 보존표
    ## Registry·entrypoint·alias·reference·test 동기화
    ## 선택적 호출·콜드 스타트·Health Review
    ## 검증·미검증·Learning Log·다음 trigger
    ```

    ## Quality gate

    - 기존 mode 검토 없이 새 Skill을 추가하지 않는다.
    - 이름만 합치며 기능·검증·승인 경계를 잃지 않는다.
    - `LEGACY_SKILL_ALIASES.md`와 오래된 참조를 처리한다.
    - 전체 skills 폴더를 기본 로드하지 않는다.
    - 실제 결과 없이 지식 상태를 승격하지 않는다.

    Learning Log: `skills/SKILL_LEARNING_LOG.md`
    '''
)

write(
    "skills/evolving-project-discipline-skills/references/consolidation-and-health-review.md",
    r'''
    # Skill 통합·Health Review 상세표

    ## 인벤토리

    Skill, mode, 분야, trigger, 입력, 산출물, 검증, 고유 책임, 중복, 상태를 한 표에서 비교한다.

    ## 통합 전 보존

    고유 입력·산출물·실패 조건·검증, 프로젝트 전용 규칙과 실제 경로, 책임 원본·Issue·PR 참조, Learning Log, scripts·references·templates, 사람용 발행본을 추출한다.

    ## Health Review

    - Registry 경로·trigger·do-not-use와 실제 패키지의 1:1 일치.
    - 활성 Skill 수, 중복 mode, 과도한 Foundation 연쇄 호출.
    - Legacy alias, 오래된 ID·경로, 변경 전파 누락.
    - reference·script의 고아 파일과 깨진 링크.
    - entrypoint·사람용 Skill Map·Manifest 최신성.
    - Governance checker, 정본 최신성, 회귀 테스트와 GitHub Actions.
    - 새 채팅이 최소 Skill을 찾아 실행할 수 있는지.
    '''
)

write(
    "skills/analyzing-and-refining-game-concepts/SKILL.md",
    r'''
    ---
    name: analyzing-and-refining-game-concepts
    description: Use when defining or reworking a game's core concept, pointed fun, constraints, design coherence, Digital Dopamine Design, benchmark and player evidence, playtest or experiment design, PoC hypothesis, or production direction.
    ---

    # Analyzing and Refining Game Concepts

    ## Core principle

    기능을 늘리는 것이 아니라 플레이어가 반복할 **뾰족한 재미**와 핵심 선택을 선명하게 만들고, 외부 사례·사용자 반응·행동 증거·PoC로 가장 위험한 가설을 검증한다.

    프로젝트 코어의 사실 판정·승인은 코어 Skill, 11영역 Games User Research 구조의 설치·누락 감사는 `governing-game-user-research-coverage`, 문서 작성은 `managing-design-documents`가 책임진다.

    ## Modes and state

    `frame → constrain → sharpen → structure → benchmark-and-player-research → analyze → playtest-and-experiment → poc-contract → recalibrate → production-gate`

    `CONCEPT_SEED → CONSTRAINTS_CHECKED → POINTED_FUN_HYPOTHESIS → CONCEPT_STRUCTURED → POC_BUILD_AND_TEST → CONCEPT_RECALIBRATION → PRODUCTION_READY | REPEAT_POC | HOLD | STOP`

    ## Required inputs

    ```yaml
    current_idea_or_gdd:
    target_player_and_play_context:
    core_loop_and_game_elements:
    constraints_and_production_capacity:
    reference_games_and_player_evidence:
    telemetry_playtest_experiment_evidence:
    prototype_or_poc_results:
    risks_unknowns_and_decision_to_make:
    ```

    ## Analysis lenses

    - `SWOT`은 설명에서 끝내지 않고 `SO / WO / ST / WT` 행동으로 변환한다.
    - `MDA / DDE / DDD`, 3C, 루프, 동기, 차별화, 제작성을 교차 확인한다.
    - Base에서 `DDD`는 `Digital Dopamine Design`이며 첫 의미 있는 보상, 행동-피드백 지연, 보상 명료성·밀도, Micro→Session→Meta 사다리, 피로·인플레이션을 본다. 외부 동명 약어는 정의 확인 전 **임의 해석하지 않는다**.

    세부 컨셉·제약·뾰족한 재미·PoC 게이트는 `references/concept-evidence-and-gates.md`, 벤치마크·사용자 근거·플레이테스트·DDD 계약은 `references/benchmark-playtest-and-ddd.md`를 필요할 때만 읽는다.

    ## Workflow

    1. 대상 플레이어, 핵심 행동·선택, 감정·판타지, 차별 원리를 한 문장으로 고정한다.
    2. 플레이·제작·기술·콘텐츠·표현·시장 제약을 확인한다.
    3. 요소를 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 정렬한다.
    4. 결정을 바꿀 질문만 벤치마킹하고 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 결론낸다.
    5. 빌드·표본·과제·관찰·이벤트·퍼널·지표가 있는 플레이테스트·실험을 설계한다.
    6. 가장 위험한 가설을 최소 PoC로 검증하고 `KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST`를 결정한다.

    ## Output contract

    ```md
    ## 핵심 컨셉·대상 플레이어·뾰족한 재미
    ## 제약과 코어 정렬
    ## SWOT·MDA/DDE/DDD·루프·차별화 분석
    ## 벤치마크·사용자·행동 증거와 판정
    ## 플레이테스트·실험·PoC 계약
    ## 유지·수정·삭제·보류 결정
    ## Production gate·미검증·다음 검증
    ```

    ## Quality gate

    기능 복사, 리뷰 표본 편향, 자기보고와 행동 혼동, 여러 변수 동시 실험, PoC 범위 팽창, DDD의 무의미한 자극화, 결과를 본 뒤 성공 기준 변경을 금지한다.

    Learning Log: `skills/SKILL_LEARNING_LOG.md`
    '''
)

write(
    "skills/analyzing-and-refining-game-concepts/references/concept-evidence-and-gates.md",
    r'''
    # 컨셉·PoC 상세 계약

    ## 핵심 컨셉

    `[대상 플레이어]는 [핵심 행동과 선택]을 반복하며 [고유한 감정·판타지·성취]를 경험하고, [차별 원리] 때문에 다시 플레이한다.`

    ## 뾰족한 재미 확인

    직접 행동인가, 반복할수록 판단·숙련·표현이 깊어지는가, 성공·실패 피드백이 명확한가, 짧은 플레이로 설명 가능한가, 콘텐츠 양에 의존하지 않고 변주가 생기는가를 확인한다.

    ## PoC

    가설, 실패 조건, 최소 구현, 비교 기준, 관찰 행동, 성공·중단 기준, 다음 게이트를 사전에 고정한다. PoC는 전체 게임이나 Vertical Slice가 아니다.

    ## Production gate

    핵심 재미 증거, 제약 적합성, 반복 가치, 제작 가능성, 사용자 근거, 남은 치명 위험으로 `PRODUCTION_READY / REPEAT_POC / HOLD / STOP`을 판정한다.
    '''
)

write(
    "skills/analyzing-and-refining-game-concepts/references/benchmark-playtest-and-ddd.md",
    r'''
    # 벤치마크·플레이테스트·DDD 상세 계약

    ## 벤치마크와 사용자 근거

    공식 제품 사실, 플레이어 자기보고, 행동 이벤트·퍼널, 통제 실험, 해석을 분리한다. 플랫폼·언어·버전·플레이타임·표본 편향을 기록하고 기능 복사가 아니라 작동 원리와 실패 조건을 추출한다.

    ## 플레이테스트·실험

    빌드·버전, 대상 집단과 기존 노출, 과제·시간, 관찰 행동, 인터뷰·설문, 이벤트·퍼널, 통제군·변형, 1차 지표와 가드레일, 성공·중단 기준을 사전 선언한다.

    ## Digital Dopamine Design

    의미 있는 행동 뒤의 빠르고 이해 가능한 피드백을 설계한다. 첫 보상 시간, 입력-반응 지연, 보상 명료성·밀도, 기대→행동→획득→다음 목표, micro/session/meta 연결, 반복 피로와 인플레이션을 확인한다.
    '''
)

# ---------------------------------------------------------------------------
# New independent skills requested by the source material.
# ---------------------------------------------------------------------------

new_skill_files = {
"skills/refactoring-with-contract-preservation/SKILL.md": r'''
---
name: refactoring-with-contract-preservation
description: Use when code, documents, data structures, automation, or a skill system must be structurally improved by reducing duplication and complexity while preserving approved behavior, interfaces, data compatibility, outputs, and user-visible capabilities.
---

# Refactoring with Contract Preservation

## Core principle

리팩토링은 기능을 다시 설계하는 일이 아니라 **승인된 동작과 계약을 유지한 채 구조를 개선**하는 일이다. 기능 추가·삭제·정책 변경과 같은 PR에 섞지 않는다.

## Modes

`baseline-contract → smell-audit → refactor → regression-validate → report`

## Required inputs

```yaml
approved_behavior_and_scope:
public_interfaces_and_outputs:
data_schema_and_compatibility:
current_implementation:
baseline_tests_and_examples:
protected_paths_assets_and_decisions:
validation_environment:
```

## Workflow

1. 정상·실패·경계 동작, API·파일·Schema·출력·성능 기준을 baseline으로 고정한다.
2. 중복, 긴 함수·문서, 복잡한 조건, 강결합, 책임 혼합, 잘못된 추상화를 근거로 찾는다.
3. 가장 작은 단계로 이동·추출·이름 정리·중복 통합을 수행한다.
4. 단계마다 baseline과 실제 결과를 비교한다.
5. 구조 개선과 동작 변경을 diff·보고에서 분리한다.

상세 냄새·변환·증거표는 `references/refactoring-checklist.md`를 필요할 때만 읽는다.

## Output contract

```md
## 보존 계약과 baseline
## 발견한 구조 문제와 근거
## 수행한 리팩토링
## 기능·인터페이스·데이터 보존 증거
## 회귀·성능·호환성 결과
## 의도적 동작 변경 없음 또는 별도 변경 목록
## 남은 위험·미검증
```

## Quality gate

동작을 설명할 baseline이 없거나, 리팩토링 명목으로 기능·정책·Schema를 바꾸거나, 테스트를 삭제해 통과시키거나, 추상화와 파일 수만 늘리면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/refactoring-with-contract-preservation/references/refactoring-checklist.md": r'''
# 리팩토링 상세 체크리스트

## 코드·구조 냄새

중복, 지나치게 긴 단위, 깊은 조건, 숨은 상태, 순환 의존, 책임 혼합, 불명확한 이름, 사용되지 않는 추상화, 같은 사실의 다중 원본, 테스트하기 어려운 결합을 찾는다.

## 안전한 변환

함수·모듈 추출, 책임 이동, 조건 단순화, 데이터 흐름 명시, 중복 통합, 이름 개선, 인터페이스 어댑터, 단계적 마이그레이션을 작은 단위로 수행한다.

## 보존 증거

기존 테스트, characterization test, golden output, Schema·API 비교, 저장 호환성, 대표 사용자 흐름, 성능 baseline과 변경 후 결과를 연결한다.
''',
"skills/simplifying-skill-bodies/SKILL.md": r'''
---
name: simplifying-skill-bodies
description: Use when a SKILL.md or operating router has grown too large and must retain only always-needed routing and execution rules while moving conditional templates, examples, domain detail, and decision tables into linked references with verified progressive disclosure.
---

# Simplifying Skill Bodies

## Core principle

본문 간소화는 정보를 지우는 작업이 아니라 **항상 필요한 실행 계약만 본문에 남기고 조건부 세부사항을 필요할 때 읽는 reference로 이동**하는 작업이다.

## Modes

`inventory → classify-always-vs-conditional → extract-references → rewrite-router → validate-disclosure`

## Keep in SKILL.md

목적·호출/비호출 조건, 권한 경계, 필수 입력, mode·작업 순서, 출력 계약, 중단·품질 게이트, 조건별 reference 주소만 둔다.

## Move to references

긴 예시, 템플릿 전문, 분야별 체크리스트, 상세 판정표, 드문 예외, 벤치마크·도메인 규칙, 반복 설명을 이동한다.

세부 분류와 검증 기준은 `references/progressive-disclosure-rules.md`를 필요할 때만 읽는다.

## Workflow

1. 각 문단이 매 호출의 행동을 바꾸는지 판정한다.
2. 항상 필요한 규칙과 조건부 지식을 분리한다.
3. 조건부 지식을 의미 있는 전문 reference로 묶고 본문에 읽는 조건과 경로를 남긴다.
4. 중복 문장을 한 계약으로 압축한다.
5. 대표·변형·예외 요청에서 필요한 reference가 실제로 발견되고 기능이 보존되는지 검사한다.

## Output contract

```md
## 간소화 전·후 본문 크기
## 본문에 유지한 필수 계약
## 이동한 reference와 호출 조건
## 삭제·통합한 중복
## 기능 보존표
## 발견성·깨진 링크·회귀 결과
```

## Quality gate

본문을 목차만 남긴 빈 라우터로 만들거나, 중요 안전 규칙을 reference 깊숙이 숨기거나, 여러 문서를 한 거대 reference로 합치거나, 이동한 파일을 본문에서 연결하지 않으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/simplifying-skill-bodies/references/progressive-disclosure-rules.md": r'''
# 점진적 공개 규칙

- Always: 모든 호출에 필요한 목적·권한·입력·흐름·출력·게이트.
- Conditional: 특정 mode·도메인·도구에서만 필요한 판정표·예시·템플릿.
- Historical: 현재 행동을 바꾸지 않는 과거 설명은 Git 이력 또는 Learning Log.
- Duplicate: 다른 책임 원본과 같은 내용은 한 원본만 유지하고 참조.

검증 시 기본 요청은 본문만으로 시작 가능해야 하고, 특수 요청은 한 단계의 명시적 reference 경로로 세부 규칙을 찾을 수 있어야 한다.
''',
"skills/pruning-stale-and-nonfunctional-material/SKILL.md": r'''
---
name: pruning-stale-and-nonfunctional-material
description: Use when skills, documents, templates, references, tests, or generated artifacts contain duplicated, stale, dead, unreachable, obsolete, or behavior-neutral material that should be reduced without losing unique capabilities, evidence, compatibility, or approved history.
---

# Pruning Stale and Nonfunctional Material

## Core principle

가지치기는 파일 수를 줄이는 목표가 아니라 **행동을 바꾸지 않는 부피와 죽은 경로를 제거하면서 고유 기능·근거·호환성을 보존**하는 작업이다.

## Modes and decisions

`inventory → classify → preserve-unique → prune-approved → verify-no-loss`

`KEEP / MERGE / MOVE_TO_REFERENCE / COMPATIBILITY_STUB / ARCHIVE / DELETE / UNVERIFIED`

## Required inputs

```yaml
active_registry_and_entrypoints:
canonical_sources_and_consumers:
usage_references_and_generation_paths:
unique_capabilities_and_evidence:
compatibility_and_history_requirements:
approval_and_rollback:
```

상세 판정표는 `references/pruning-decision-matrix.md`를 필요할 때만 읽는다.

## Workflow

1. 중복, 도달 불가, 오래된 경로·ID, 보류·백업의 기본 읽기 혼입, 행동을 바꾸지 않는 문장을 찾는다.
2. 삭제 전에 고유 입력·산출물·검증·근거·소비자·호환성을 추출한다.
3. 병합·reference 이동·stub·archive·삭제 중 가장 안전한 처리를 선택한다.
4. 사용자 승인 또는 저장소 계약이 필요한 삭제는 보류한다.
5. 정본 최신성·깨진 링크·Registry·테스트·콜드 스타트·대표 기능을 재검증한다.

## Output contract

```md
## 후보와 사용·참조 근거
## KEEP·MERGE·MOVE·STUB·ARCHIVE·DELETE·UNVERIFIED 판정
## 보존한 고유 기능·근거·호환성
## 실제 제거·축소량
## 정본·링크·라우팅·회귀 결과
## 롤백과 남은 위험
```

## Quality gate

사용 흔적이 없다는 이유만으로 자동 삭제하거나, Git 이력을 활성 백업 파일로 복제하거나, 테스트·문서만 지워 결함을 숨기거나, 고유 기능을 병합 중 잃으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/pruning-stale-and-nonfunctional-material/references/pruning-decision-matrix.md": r'''
# 가지치기 판정표

- `KEEP`: 현재 행동·안전·발견성에 필요하다.
- `MERGE`: 같은 책임과 생명주기를 중복 표현한다.
- `MOVE_TO_REFERENCE`: 가끔 필요하지만 본문 상시 로드에는 불필요하다.
- `COMPATIBILITY_STUB`: 외부 소비자가 이전 경로를 계속 사용한다.
- `ARCHIVE`: 감사·법적·승인 이력은 필요하지만 활성 입력은 아니다.
- `DELETE`: 고유 기능·소비자·증거·호환성 가치가 없고 롤백 가능하다.
- `UNVERIFIED`: 사용·소비자·권한을 확인하지 못했다.

삭제 전에는 정본, 역참조, 생성기, CI, 배포·발행, 사용자 북마크·외부 링크, 저장 호환성을 확인한다.
''',
"skills/synchronizing-local-and-github-state/SKILL.md": r'''
---
name: synchronizing-local-and-github-state
description: Use when a local checkout and its GitHub branch must be compared, safely reconciled, refreshed, published, or verified as equivalent without overwriting uncommitted work, secrets, divergent history, or unreviewed changes.
---

# Synchronizing Local and GitHub State

## Core principle

동기화는 무조건 pull·commit·push하는 자동화가 아니다. 먼저 양쪽 상태와 권한을 판정하고, **clean + fast-forward + 승인된 변경**일 때만 자동 진행한다.

## Modes and states

`inspect → reconcile → refresh-local | publish-remote → verify-sync`

`SYNCED / DIRTY / LOCAL_AHEAD / REMOTE_AHEAD / DIVERGED / BLOCKED`

## Required inputs

```yaml
repository_and_remote:
local_branch_head_and_status:
remote_branch_head:
uncommitted_and_untracked_files:
upstream_and_branch_policy:
credentials_permissions_and_required_checks:
allowed_generated_files_and_secrets_policy:
```

안전한 명령·충돌 절차는 `references/safe-sync-protocol.md`를 필요할 때만 읽는다.

## Rules

- `DIRTY`: 커밋·stash·폐기 선택 없이 pull/rebase/reset하지 않는다.
- `REMOTE_AHEAD`: fast-forward 가능할 때만 자동 갱신한다.
- `LOCAL_AHEAD`: diff·검증·커밋 범위를 확인한 뒤 push·PR한다.
- `DIVERGED`: 자동 force push·hard reset을 금지하고 병합·rebase·새 branch 중 하나를 명시적으로 선택한다.
- 비밀·대용량 생성물·승인되지 않은 파일은 자동 커밋하지 않는다.

## Output contract

```md
## 로컬·원격 HEAD와 상태
## 차이 파일·커밋·미추적 항목
## 선택한 reconcile 방식과 이유
## 수행한 fetch/pull/commit/push/PR
## 검증·Required Checks·최종 동등성
## 충돌·권한·미검증·사용자 조치
```

## Quality gate

로컬 작업 유실, 무검토 자동 커밋, force push, 인증 실패 은폐, pull 성공을 기능 검증으로 오인하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md": r'''
# 안전한 Git 동기화 프로토콜

1. remote·upstream·현재 branch·HEAD·working tree·untracked를 기록한다.
2. fetch 후 merge-base와 ahead/behind를 판정한다.
3. clean fast-forward만 자동 pull한다.
4. 로컬 변경은 diff·검증·명시적 파일 범위로 commit한다.
5. 원격 변경은 보호 branch 정책과 Required Checks를 지킨다.
6. diverged history는 백업 branch를 만들고 선택한 전략을 기록한다.
7. 최종 local HEAD와 remote HEAD, tree diff, CI 상태를 대조한다.
''',
"skills/maintaining-long-running-task-continuity/SKILL.md": r'''
---
name: maintaining-long-running-task-continuity
description: Use when a large multi-step task may exceed one response, tool session, context window, or execution attempt and must remain resumable through evidence-backed checkpoints, partial deliverables, explicit next actions, and truthful completion states.
---

# Maintaining Long-Running Task Continuity

## Core principle

중단을 숨기거나 비동기 완료를 약속하지 않는다. 큰 작업을 검증 가능한 결과 단위로 나누고, 각 단위가 끝날 때 재개 가능한 checkpoint와 실제 산출물을 남긴다.

## Modes

`initialize → checkpoint → resume → partial-delivery → close`

## Checkpoint contract

```yaml
objective_and_scope:
completed_outcomes:
changed_or_created_artifacts:
validation_and_evidence:
current_state_and_blockers:
protected_decisions:
next_exact_action:
remaining_acceptance_criteria:
```

## Workflow

1. 작업을 독립 검증 가능한 결과와 선행 조건으로 나눈다.
2. 가장 위험하거나 가치 있는 결과부터 실제로 완성한다.
3. 2~3개 도구 묶음 또는 의미 있는 단계마다 상태·증거·다음 행동을 갱신한다.
4. 실행이 막히면 완료한 결과를 먼저 전달하고 미완료·원인·재개 지점을 분리한다.
5. 재개 시 과거 대화 전체가 아니라 최신 checkpoint와 책임 원본을 읽는다.

## Quality gate

진행 중을 완료로 표시하지 않고, 같은 질문을 반복하지 않으며, 시간 예측·백그라운드 작업을 약속하지 않고, checkpoint 없이 긴 조사만 계속하지 않는다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/governing-game-user-research-coverage/SKILL.md": r'''
---
name: governing-game-user-research-coverage
description: Use when a game project's design-document system must install, audit, plan, or synthesize complete Games User Research coverage across eleven required evidence domains without inventing findings or forcing irrelevant research activity.
---

# Governing Games User Research Coverage

## Core principle

기획 운영체계에는 11개 연구 영역의 **자리·책임·증거 상태**가 모두 있어야 한다. 모든 영역에서 즉시 조사를 강제하지는 않으며, 근거가 없으면 `NOT_STARTED`, 적용 불가면 이유가 있는 `NOT_APPLICABLE`로 표시한다.

## Modes

`install → audit → plan-evidence → synthesize → verify-coverage`

## Required 11 domains

1. 시장·장르 분석
2. 벤치마킹·경쟁 게임 비교
3. SWOT·포지셔닝
4. 사용자 조사
5. 플레이테스트
6. 튜토리얼 이해도
7. UX 문제 분석
8. 텔레메트리·퍼널
9. 밸런스 데이터
10. 가설·실험·결과
11. 개선안과 채택·미채택 근거

책임·필드·상태·최소 증거는 `references/eleven-domain-coverage.md`를 필요할 때만 읽는다.

## Boundary

이 Skill은 누락 없는 구조와 증거 계획을 관리한다. 실제 컨셉·벤치마크·플레이테스트 해석은 `analyzing-and-refining-game-concepts`, 문서 생성은 `managing-design-documents`, 실제 계측 구현과 변경 검증은 프로젝트 계약과 검증 Skill이 책임진다.

## Output contract

```md
## 11영역 coverage matrix
## 영역별 책임 원본·담당·상태
## 현재 근거·표본·버전·한계
## 누락·중복·충돌
## 다음 연구·계측·플레이테스트 우선순위
## 개선안·채택/미채택 근거 연결
```

## Quality gate

빈 섹션 존재를 완료로 보거나, 조사하지 않은 내용을 사실로 작성하거나, 모든 프로젝트에 같은 연구 방법·표본을 강제하거나, 사용자 자기보고와 행동 데이터를 혼동하면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/governing-game-user-research-coverage/references/eleven-domain-coverage.md": r'''
# Games User Research 11영역 계약

각 영역은 `owner / canonical_source / question / method / sample_or_version / evidence / status / finding / implication / decision / limitation / next_check`를 가진다.

상태는 `NOT_STARTED / PLANNED / IN_PROGRESS / EVIDENCE_COLLECTED / SYNTHESIZED / VERIFIED / NOT_APPLICABLE / BLOCKED`로 구분한다.

- 시장·장르: 시장 약속, 대상층, 가격·운영, 지역·플랫폼.
- 벤치마킹·경쟁: 비교 차원, 작동 원리, 실패 조건, 차별화.
- SWOT: S/W/O/T를 SO/WO/ST/WT 행동으로 연결.
- 사용자 조사: 대상 세그먼트, 질문, 표본, 편향.
- 플레이테스트: 빌드·과제·관찰·피드백.
- 튜토리얼: 첫 행동·이해·오입력·이탈.
- UX: 목표·막힘·정보 위계·접근성.
- 텔레메트리: 이벤트 정의, 퍼널, 버전, 누락 데이터.
- 밸런스: 분포, 승률·사용률, 경제 흐름, 이상치.
- 가설·실험: 사전 가설, 변형, 지표, 결과, 한계.
- 개선·결정: 채택·변형·제외·보류와 근거·재검토 조건.
''',
"skills/creating-user-learning-notes/SKILL.md": r'''
---
name: creating-user-learning-notes
description: Use when completed project work, AI collaboration, tools, mistakes, or decisions should be converted into concise user-facing study notes that explain concepts, reasons, examples, misconceptions, practice steps, and reusable lessons rather than operational instructions for an AI.
---

# Creating User Learning Notes

## Core principle

학습 노트는 AI 지침을 복사하는 문서가 아니라 사용자가 **왜 이런 구조가 필요한지 이해하고 스스로 판단·적용**하도록 돕는 설명 자료다.

## Modes

`capture → explain → connect → practice → update`

## Required inputs

```yaml
learning_goal_and_reader_level:
completed_work_or_case:
key_decisions_and_reasons:
failures_misconceptions_and_evidence:
terms_tools_and_references:
practice_or_next_application:
```

## Output contract

```md
## 이번에 배울 핵심
## 개념과 쉬운 정의
## 왜 필요한가
## 실제 작업 흐름과 역할 구분
## 좋은 예·나쁜 예
## 자주 하는 오해와 수정
## 직접 해볼 연습
## 확인 질문과 다음 학습
## 근거·출처·미확인
```

## Rules

- 확정 사실, 경험적 교훈, 가설을 구분한다.
- 특정 프로젝트 사례와 공용 원리를 분리한다.
- 전문 용어는 첫 사용에서 정의한다.
- 결과만 나열하지 않고 원인→판단→결과를 연결한다.
- 긴 작업 로그와 내부 지침 전문을 학습 노트로 복제하지 않는다.

## Quality gate

독자가 원문 대화 없이 이해하고, 배운 원리를 새로운 작업에 적용하며, 무엇이 검증됐고 무엇이 가설인지 구분할 수 있어야 한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/building-project-visual-dashboards/SKILL.md": r'''
---
name: building-project-visual-dashboards
description: Use when project concepts, loops, system relationships, MVP status, UX flows, evidence, risks, or next work need an editable visual dashboard while canonical decisions remain in registered GitHub documents and data sources.
---

# Building Project Visual Dashboards

## Core principle

대시보드는 복잡한 관계를 보고 토론하는 작업 공간이다. 확정 결정과 구현 상태의 정본을 대체하지 않으며, 원본 경로·갱신 시점·상태를 명시한다.

## Modes

`frame → map-sources → build → bind-status → validate`

## Default form

특별한 요구가 없으면 단일 HTML + CSS + 최소 JavaScript로 만들고 PC 가독성, 의미 있는 카드·표·화살표·상태 배지, 수정 위치 주석을 우선한다.

정보 구조·검수표는 `references/dashboard-information-architecture.md`를 필요할 때만 읽는다.

## Output contract

```md
## 대시보드 목적·독자·결정
## 탭·흐름·데이터 원본
## 편집·미리보기 동작
## 상태·위험·누락 표시
## 생성 파일과 실행 방법
## 정본 동기화·검증·미확인
```

## Quality gate

예쁜 장식보다 정보 위계와 행동을 우선하고, 수동 복사된 오래된 상태를 최신으로 표시하지 않으며, 모바일·접근성·보안 요구가 있으면 별도 검증한다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/building-project-visual-dashboards/references/dashboard-information-architecture.md": r'''
# 프로젝트 대시보드 정보 구조

권장 탭: 프로젝트 개요, 핵심 루프, 시스템 관계도, MVP 진행, UI/UX 흐름, 벤치마크·사용자 근거, 누락·위험, 최신 QA·이미지, 다음 작업.

각 카드에는 `status / owner / source / updated_at / evidence / next_action`을 둔다. 색은 상태·기능 구분에만 사용하며 색상만으로 의미를 전달하지 않는다.

편집 모드는 텍스트·상태 조정을 허용하고, 미리보기 모드는 실제 사용자 관점의 흐름을 보여 준다. 확정 변경은 등록된 책임 원본에 다시 기록한다.
''',
"skills/diagnosing-game-engine-runtime-failures/SKILL.md": r'''
---
name: diagnosing-game-engine-runtime-failures
description: Use when a Godot, Unity, or comparable game-engine project crashes, throws errors, loads incorrectly, loses signals or references, corrupts state, or behaves differently at runtime and needs evidence-based reproduction, isolation, minimal repair, and revalidation.
---

# Diagnosing Game Engine Runtime Failures

## Core principle

증상을 추측으로 고치지 않는다. 같은 조건에서 재현하고 로그·Scene·Node·Component·Signal·데이터·상태 흐름을 좁힌 뒤 가장 작은 수정으로 원인을 제거한다.

## Modes

`reproduce → isolate → form-hypotheses → fix-minimally → revalidate → prevent`

## Required inputs

```yaml
engine_version_platform_and_build:
reproduction_steps_expected_actual:
logs_stack_trace_and_screenshots:
scene_prefab_node_component_structure:
scripts_signals_events_and_data:
recent_diff_and_known_good_baseline:
validation_environment:
```

상세 런타임 체크리스트는 `references/runtime-debugging-checklist.md`를 필요할 때만 읽는다.

## Output contract

```md
## 재현 조건과 관찰 결과
## 가장 가능성 높은 원인과 반증
## 확인한 Scene·Node·Signal·Component·데이터
## 최소 수정과 영향 범위
## 정상·실패·경계·저장·플랫폼 재검증
## 재발 방지 테스트·문서·규칙
## 미검증·사용자 엔진 확인 항목
```

## Quality gate

재현 없이 대규모 수정하거나, 오류 메시지만 숨기거나, 엔진 버전·플랫폼·최근 diff를 무시하거나, 수정 후 원래 재현 절차와 인접 경로를 다시 확인하지 않으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
''',
"skills/diagnosing-game-engine-runtime-failures/references/runtime-debugging-checklist.md": r'''
# 게임 엔진 런타임 디버깅 체크리스트

- 재현: 엔진·플랫폼·Scene·입력·저장 데이터·빈도·최초 실패 프레임.
- 로그: 최초 원인 오류와 후속 연쇄 오류를 분리.
- 구조: 누락 Node/Component, 경로, prefab/scene override, lifecycle 순서.
- 연결: Signal·event 구독/해제, 중복 호출, null·destroyed reference.
- 데이터: ID·Schema·직렬화·마이그레이션·리소스 경로.
- 상태: 초기화, scene 전환, pause, async, 재진입, 저장/불러오기.
- 재검증: 원래 재현, 정상 경로, 경계, 저장 호환, export/build, 성능.
''',
}

for path, content in new_skill_files.items():
    write(path, content)

# ---------------------------------------------------------------------------
# Coverage sources and dedicated PR checks.
# ---------------------------------------------------------------------------

coverage = {
    "schema_version": 1,
    "coverage_role": "source-text-to-active-skill-responsibility-map",
    "responsibilities": [
        {"id": "local-github-sync", "skills": ["synchronizing-local-and-github-state"], "status": "COVERED"},
        {"id": "behavior-preserving-refactoring", "skills": ["refactoring-with-contract-preservation"], "status": "COVERED"},
        {"id": "long-running-task-continuity", "skills": ["maintaining-long-running-task-continuity"], "status": "COVERED"},
        {"id": "skill-body-simplification", "skills": ["simplifying-skill-bodies"], "status": "COVERED"},
        {"id": "stale-dead-material-pruning", "skills": ["pruning-stale-and-nonfunctional-material"], "status": "COVERED"},
        {"id": "games-user-research-eleven-domains", "skills": ["governing-game-user-research-coverage"], "status": "COVERED"},
        {"id": "user-learning-notes", "skills": ["creating-user-learning-notes"], "status": "COVERED"},
        {"id": "ambiguous-request-to-work-contract", "skills": ["managing-project-intake-and-work-contract"], "status": "COVERED_EXISTING"},
        {"id": "player-experience-and-core-concept", "skills": ["analyzing-and-refining-game-concepts", "identifying-project-core", "establishing-project-core"], "status": "COVERED_EXISTING"},
        {"id": "benchmarking-and-player-evidence", "skills": ["analyzing-and-refining-game-concepts", "governing-game-user-research-coverage"], "status": "COVERED_EXISTING"},
        {"id": "mvp-scope-and-poc", "skills": ["managing-project-intake-and-work-contract", "analyzing-and-refining-game-concepts"], "status": "COVERED_EXISTING"},
        {"id": "issue-goal-plan-contract", "skills": ["managing-project-intake-and-work-contract"], "status": "COVERED_EXISTING"},
        {"id": "project-memory-and-context-compaction", "skills": ["managing-design-documents", "maintaining-project-context-and-handoff"], "status": "COVERED_EXISTING"},
        {"id": "visual-dashboard", "skills": ["building-project-visual-dashboards"], "status": "COVERED"},
        {"id": "multi-role-adversarial-review", "skills": ["running-adversarial-review-and-refinement"], "status": "COVERED_EXISTING"},
        {"id": "change-test-and-completion-evidence", "skills": ["reviewing-and-validating-project-changes"], "status": "COVERED_EXISTING"},
        {"id": "game-engine-runtime-debugging", "skills": ["diagnosing-game-engine-runtime-failures"], "status": "COVERED"},
        {"id": "skill-compression-and-evolution", "skills": ["evolving-project-discipline-skills", "simplifying-skill-bodies", "pruning-stale-and-nonfunctional-material"], "status": "COVERED_EXISTING"},
    ],
}
write("skills/SKILL_COVERAGE.json", json.dumps(coverage, ensure_ascii=False, indent=2))

write(
    "docs/SKILL_COVERAGE_MAP.md",
    r'''
    # Source Text → Base Skill Coverage

    이 문서는 사용자가 제공한 학습 텍스트의 작업 책임을 활성 Skill에 매핑한다. 개념마다 파일을 만들지 않고 **독립 입력·산출물·권한·검증 경계**가 있을 때만 새 Skill로 분리한다. 기계 검증 원본은 `skills/SKILL_COVERAGE.json`이다.

    ## 새 독립 Skill

    | 책임 | Skill | 분리 이유 |
    |---|---|---|
    | 로컬·GitHub 상태 동기화 | `synchronizing-local-and-github-state` | Git 상태·권한·충돌·손실 방지 계약이 독립적임 |
    | 행동 보존 리팩토링 | `refactoring-with-contract-preservation` | baseline·호환성·회귀 증거가 필요함 |
    | 장기 작업 연속성 | `maintaining-long-running-task-continuity` | checkpoint·재개·부분 전달 상태가 독립적임 |
    | Skill 본문 간소화 | `simplifying-skill-bodies` | 점진적 공개와 reference 발견성 검증이 필요함 |
    | 죽은 자료 가지치기 | `pruning-stale-and-nonfunctional-material` | 역참조·고유 기능·삭제 승인·롤백이 필요함 |
    | Games User Research 11영역 | `governing-game-user-research-coverage` | 설치·coverage·증거 상태 감사가 독립적임 |
    | 사용자 학습 노트 | `creating-user-learning-notes` | 학습 독자·설명·연습 산출물이 운영 지침과 다름 |
    | 프로젝트 시각 대시보드 | `building-project-visual-dashboards` | 시각 작업 공간·원본 연결·상태 바인딩이 독립적임 |
    | 엔진 런타임 디버깅 | `diagnosing-game-engine-runtime-failures` | 재현·원인 격리·최소 수정·엔진 재검증이 독립적임 |

    ## 기존 Skill에 유지한 책임

    - 모호한 요청→실행 계약, Issue·Goal·Plan, 작업 분해: `managing-project-intake-and-work-contract`.
    - 플레이어 경험·벤치마킹·MVP·PoC·플레이테스트: `analyzing-and-refining-game-concepts`.
    - 프로젝트 코어 사실 판정과 승인 확정: `identifying-project-core`, `establishing-project-core`.
    - 문서 기억·정본·단계별 컨텍스트 압축: `managing-design-documents`, `maintaining-project-context-and-handoff`.
    - 다중 관점 공격·개선: `running-adversarial-review-and-refinement`.
    - 실제 diff·테스트·완료 증거: `reviewing-and-validating-project-changes`.
    - Skill 생성·통합·학습: `evolving-project-discipline-skills`.

    ## Base 자체 적용 순서

    ```text
    coverage inventory
    → pruning-stale-and-nonfunctional-material
    → simplifying-skill-bodies
    → refactoring-with-contract-preservation
    → running-adversarial-review-and-refinement
    → reviewing-and-validating-project-changes
    → auditing-canonical-reference-freshness
    → PR checks
    ```
    '''
)

write(
    "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md",
    r'''
    # Base Skill System Optimization Report

    ## Scope

    사용자가 제공한 1,201줄 학습 텍스트와 기존 활성 Skill 16개의 책임을 대조했다. 새 책임은 9개로 제한하고, 이미 존재하는 요청 명세화·벤치마킹·MVP·Issue/Goal·문서 기억·검증 책임은 중복 신설하지 않았다.

    ## Applied pruning

    - 프로젝트 코어·적대적 검토·Skill 진화·게임 컨셉 Skill의 반복 설명과 상세 판정표를 본문에서 제거했다.
    - 고유 규칙은 각 패키지의 `references/`로 이동하고 본문에서 읽는 조건을 연결했다.
    - 임시 동기화 Workflow와 적용 스크립트는 결과 커밋에서 자체 제거한다.

    ## Applied simplification

    수정한 SKILL.md는 목적·경계·mode·필수 입력·핵심 흐름·출력·품질 게이트 중심의 라우터로 재작성했다. 상세 예시·판정표·체크리스트는 조건부 reference로 분리했다.

    ## Applied refactoring

    - 코어 판정, 코어 확정, 적대적 검토의 권한 경계를 보존했다.
    - 분석 Skill의 컨셉·벤치마크·플레이테스트·DDD·PoC 기능을 유지하며 세부 계약을 모듈화했다.
    - Skill 진화는 생성·통합 오케스트레이션만 남기고 가지치기·간소화·리팩토링을 독립 Skill로 위임했다.

    ## No-loss controls

    - `skills/SKILL_COVERAGE.json`으로 원문 책임 18개를 활성 Skill에 매핑한다.
    - 전용 checker가 coverage 대상, Registry, 파일, front matter, 최소 계약, compact target을 검증한다.
    - 기존 구조·Registry·reference·정본 최신성 회귀 테스트와 PR Actions를 함께 실행한다.

    ## Expected result

    활성 Skill은 16개에서 25개로 증가하지만, 각 새 Skill은 독립 계약이 있는 책임만 담당한다. 기본 컨텍스트는 전체 로드하지 않으며 `load_by_default=false`와 trigger 기반 선택을 유지한다.
    '''
)

write(
    "tools/check_skill_system_coverage.py",
    r'''
    from __future__ import annotations

    import json
    import re
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]
    REGISTRY = ROOT / "skills/SKILL_REGISTRY.json"
    COVERAGE = ROOT / "skills/SKILL_COVERAGE.json"
    FRONT_NAME = re.compile(r"^name:\s*['\"]?([^'\"\n]+)", re.MULTILINE)

    COMPACT_TARGETS = {
        "identifying-project-core",
        "establishing-project-core",
        "running-adversarial-review-and-refinement",
        "evolving-project-discipline-skills",
        "analyzing-and-refining-game-concepts",
        "refactoring-with-contract-preservation",
        "simplifying-skill-bodies",
        "pruning-stale-and-nonfunctional-material",
        "synchronizing-local-and-github-state",
        "maintaining-long-running-task-continuity",
        "governing-game-user-research-coverage",
        "creating-user-learning-notes",
        "building-project-visual-dashboards",
        "diagnosing-game-engine-runtime-failures",
    }

    def validate() -> list[str]:
        errors: list[str] = []
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        coverage = json.loads(COVERAGE.read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}

        for responsibility in coverage["responsibilities"]:
            if not responsibility["skills"]:
                errors.append(f"No skill target: {responsibility['id']}")
            for skill_id in responsibility["skills"]:
                if skill_id not in by_id:
                    errors.append(f"Coverage target not active: {responsibility['id']} -> {skill_id}")

        for skill_id, item in by_id.items():
            path = ROOT / item["path"]
            if not path.is_file():
                errors.append(f"Missing skill file: {skill_id} -> {item['path']}")
                continue
            text = path.read_text(encoding="utf-8")
            match = FRONT_NAME.search(text)
            if not match or match.group(1).strip() != skill_id:
                errors.append(f"Front matter mismatch: {skill_id}")
            for required in ("##", "Output contract", "Quality gate", "Learning Log"):
                if required not in text:
                    errors.append(f"Missing compact contract token {required!r}: {skill_id}")
            if skill_id in COMPACT_TARGETS and len(text.splitlines()) > 150:
                errors.append(f"Compact SKILL.md exceeds 150 lines: {skill_id} ({len(text.splitlines())})")

        return errors

    def main() -> int:
        errors = validate()
        if errors:
            print("Skill system coverage check failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        print("Skill system coverage check passed")
        return 0

    if __name__ == "__main__":
        raise SystemExit(main())
    '''
)

write(
    "tests/test_skill_system_coverage.py",
    r'''
    from __future__ import annotations

    import importlib.util
    import json
    import unittest
    from pathlib import Path

    ROOT = Path(__file__).resolve().parents[1]

    spec = importlib.util.spec_from_file_location(
        "check_skill_system_coverage",
        ROOT / "tools/check_skill_system_coverage.py",
    )
    checker = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(checker)


    class SkillSystemCoverageTests(unittest.TestCase):
        def test_source_responsibilities_are_mapped_to_active_skills(self) -> None:
            self.assertEqual(checker.validate(), [])

        def test_requested_independent_skills_remain_distinct(self) -> None:
            registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
            ids = {item["skill_id"] for item in registry["skills"]}
            required = {
                "refactoring-with-contract-preservation",
                "simplifying-skill-bodies",
                "pruning-stale-and-nonfunctional-material",
                "synchronizing-local-and-github-state",
                "maintaining-long-running-task-continuity",
                "governing-game-user-research-coverage",
                "creating-user-learning-notes",
                "building-project-visual-dashboards",
                "diagnosing-game-engine-runtime-failures",
            }
            self.assertTrue(required.issubset(ids))

        def test_games_user_research_contract_has_exactly_eleven_domains(self) -> None:
            text = (ROOT / "skills/governing-game-user-research-coverage/SKILL.md").read_text(encoding="utf-8")
            numbered = [line for line in text.splitlines() if line[:1].isdigit() and ". " in line]
            self.assertEqual(len(numbered), 11)

        def test_optimization_report_and_machine_coverage_exist(self) -> None:
            self.assertTrue((ROOT / "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md").is_file())
            self.assertTrue((ROOT / "docs/SKILL_COVERAGE_MAP.md").is_file())
            self.assertTrue((ROOT / "skills/SKILL_COVERAGE.json").is_file())


    if __name__ == "__main__":
        unittest.main()
    '''
)

# ---------------------------------------------------------------------------
# Registry update.
# ---------------------------------------------------------------------------

registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
existing_ids = {item["skill_id"] for item in registry["skills"]}

new_entries = [
    {
        "skill_id": "refactoring-with-contract-preservation",
        "layer": "foundation",
        "discipline": "structure-maintenance",
        "path": "skills/refactoring-with-contract-preservation/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["refactor", "code-smell", "complexity-reduction", "duplicate-removal", "behavior-preservation", "structural-improvement"],
        "use_when": ["승인된 동작·인터페이스·데이터 호환성을 유지하면서 코드·문서·자동화·Skill 구조의 중복과 복잡성을 줄인다."],
        "do_not_use_when": ["기능·정책·Schema 변경이 주목적이거나 baseline과 회귀 검증 없이 구조를 바꾸려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["기능 회귀", "호환성 손실", "리팩토링과 기능 변경 혼합", "테스트 삭제로 통과", "불필요한 추상화"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "simplifying-skill-bodies",
        "layer": "foundation",
        "discipline": "skill-context-optimization",
        "path": "skills/simplifying-skill-bodies/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["skill-body-simplification", "progressive-disclosure", "context-reduction", "reference-extraction", "compact-skill"],
        "use_when": ["비대해진 SKILL.md에서 항상 필요한 실행 계약만 남기고 조건부 상세를 연결된 reference로 이동한다."],
        "do_not_use_when": ["단순 문장 교정이거나 안전 규칙·핵심 절차를 숨기는 축약을 하려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["기능 손실", "reference 발견 실패", "깨진 링크", "빈 라우터", "거대 reference 재생성"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "pruning-stale-and-nonfunctional-material",
        "layer": "foundation",
        "discipline": "repository-pruning",
        "path": "skills/pruning-stale-and-nonfunctional-material/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["pruning", "dead-material", "stale-content", "duplicate-content", "orphan-reference", "obsolete-artifact", "repository-bloat"],
        "use_when": ["중복·죽은 자료·오래된 경로·행동을 바꾸지 않는 문장을 고유 기능과 호환성을 보존하며 병합·이동·보관·삭제한다."],
        "do_not_use_when": ["사용·소비자·승인·롤백을 확인하지 못했거나 단순히 파일 수를 줄이려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["고유 기능 유실", "오삭제", "외부 링크 파손", "호환성 손실", "보류 자료 기본 읽기 혼입"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "synchronizing-local-and-github-state",
        "layer": "specialist",
        "discipline": "git-operations",
        "path": "skills/synchronizing-local-and-github-state/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["git-sync", "local-remote-drift", "pull", "push", "branch-divergence", "working-tree", "github-sync"],
        "use_when": ["로컬 checkout과 GitHub branch의 HEAD·diff·working tree·권한을 대조해 안전하게 refresh·publish·reconcile하고 최종 동등성을 검증한다."],
        "do_not_use_when": ["저장소와 무관한 작업이거나 dirty/diverged 상태를 자동 force·reset으로 덮으려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["로컬 변경 유실", "무검토 자동 커밋", "force push", "비밀 커밋", "동기화와 기능 검증 혼동"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "maintaining-long-running-task-continuity",
        "layer": "foundation",
        "discipline": "execution-continuity",
        "path": "skills/maintaining-long-running-task-continuity/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["long-running-task", "checkpoint", "resume-work", "partial-delivery", "context-limit", "tool-session-boundary"],
        "use_when": ["큰 다단계 작업을 검증 가능한 결과·checkpoint·부분 산출물·정확한 다음 행동으로 유지해 중단 후에도 재개 가능하게 한다."],
        "do_not_use_when": ["10초 이내 단순 작업이거나 백그라운드·미래 완료를 약속하려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["중간 결과 유실", "진행 중을 완료로 보고", "재개 지점 불명", "반복 질문", "비동기 완료 약속"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "governing-game-user-research-coverage",
        "layer": "specialist",
        "discipline": "games-user-research-governance",
        "path": "skills/governing-game-user-research-coverage/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["games-user-research", "research-coverage", "eleven-domains", "tutorial-comprehension", "ux-research", "telemetry", "balance-data", "research-evidence"],
        "use_when": ["게임 기획 운영체계에 시장·경쟁·SWOT·사용자·플레이테스트·튜토리얼·UX·텔레메트리·밸런스·가설·개선 결정 11영역을 설치·감사한다."],
        "do_not_use_when": ["단일 벤치마크 질문만 있거나 근거 없는 연구 결과를 채우려는 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["영역 누락", "빈 섹션을 완료로 판정", "자기보고와 행동 혼동", "표본·버전 누락", "채택 근거 단절"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "creating-user-learning-notes",
        "layer": "specialist",
        "discipline": "user-learning",
        "path": "skills/creating-user-learning-notes/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["learning-note", "study-note", "explain-workflow", "user-education", "concept-summary", "practice-exercise"],
        "use_when": ["완료한 작업·도구·실수·결정을 사용자가 이해하고 재사용할 수 있는 개념·이유·예시·오해·연습 중심 학습 노트로 변환한다."],
        "do_not_use_when": ["AI 실행 지침을 그대로 복사하거나 단순 작업 보고만 필요한 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["지침과 학습자료 혼동", "검증·가설 혼동", "프로젝트 사례의 공용화", "연습·적용 연결 부족"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "building-project-visual-dashboards",
        "layer": "specialist",
        "discipline": "project-visualization",
        "path": "skills/building-project-visual-dashboards/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["project-dashboard", "html-dashboard", "system-map", "mvp-board", "ux-flow", "visual-status"],
        "use_when": ["프로젝트 개요·루프·시스템 관계·MVP·UX·근거·위험·다음 작업을 정본에 연결된 편집 가능한 시각 대시보드로 만든다."],
        "do_not_use_when": ["확정 문서 정본을 대시보드로 대체하거나 단순 표 한 개면 충분한 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["정본과 상태 불일치", "장식 우선", "원본 경로 누락", "접근성 문제", "과도한 JavaScript"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
    {
        "skill_id": "diagnosing-game-engine-runtime-failures",
        "layer": "specialist",
        "discipline": "game-engine-debugging",
        "path": "skills/diagnosing-game-engine-runtime-failures/SKILL.md",
        "status": "ACTIVE",
        "load_by_default": False,
        "trigger_tags": ["godot-error", "unity-error", "runtime-failure", "scene-node-signal", "crash", "state-corruption", "engine-debugging"],
        "use_when": ["Godot·Unity 등 엔진의 오류·충돌·잘못된 로딩·연결·상태 동작을 재현하고 원인을 격리해 최소 수정 후 재검증한다."],
        "do_not_use_when": ["재현·로그·실행 환경 없이 구조 전체를 추측 수정하거나 일반 코드 리뷰만 필요한 경우다."],
        "learning_log": "skills/SKILL_LEARNING_LOG.md",
        "review_triggers": ["재현 없는 수정", "연쇄 오류를 원인으로 오인", "대규모 추측 변경", "엔진 버전 누락", "수정 후 재검증 누락"],
        "last_reviewed_at": "2026-07-22",
        "last_reviewed_commit": "d2ec3899aaf897d7713a30ae7667707764b7336b",
        "knowledge_state": "HYPOTHESIS",
    },
]

for entry in new_entries:
    if entry["skill_id"] not in existing_ids:
        registry["skills"].append(entry)

registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# ---------------------------------------------------------------------------
# Entrypoints, maps, change records, and tests.
# ---------------------------------------------------------------------------

readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
readme = readme.replace("활성 Registry 스킬은 중복 통합 뒤 **16개**입니다.", "활성 Registry 스킬은 책임 경계 재검토와 최적화 뒤 **25개**입니다.")
anchor = "| `evolving-project-discipline-skills` | 프로젝트 스킬 생성·통합·학습 |\n"
rows = (
    "| `pruning-stale-and-nonfunctional-material` | 중복·죽은 자료·오래된 경로의 무손실 가지치기 |\n"
    "| `simplifying-skill-bodies` | SKILL.md 핵심 계약 유지와 조건부 reference 분리 |\n"
    "| `refactoring-with-contract-preservation` | 기능·인터페이스·데이터 보존 리팩토링 |\n"
    "| `synchronizing-local-and-github-state` | 로컬·GitHub 상태의 안전한 비교·동기화 |\n"
    "| `maintaining-long-running-task-continuity` | 장기 작업 checkpoint·재개·부분 전달 |\n"
    "| `governing-game-user-research-coverage` | 게임 사용자 연구 11영역 설치·증거 coverage 감사 |\n"
    "| `creating-user-learning-notes` | 작업 교훈을 사용자 학습 노트로 변환 |\n"
    "| `building-project-visual-dashboards` | 정본 연결형 프로젝트 시각 대시보드 |\n"
    "| `diagnosing-game-engine-runtime-failures` | Godot·Unity 런타임 재현·원인 격리·최소 수정 |\n"
)
if rows not in readme:
    readme = readme.replace(anchor, anchor + rows)
readme_path.write_text(readme, encoding="utf-8")

append_once(
    "START_HERE.md",
    "### 구조 최적화·동기화·장기 작업",
    r'''
    ### 구조 최적화·동기화·장기 작업

    ```text
    불필요 자료 판정 → pruning-stale-and-nonfunctional-material
    조건부 상세 분리 → simplifying-skill-bodies
    동작 보존 구조 변경 → refactoring-with-contract-preservation
    실패 가정 재검토 → running-adversarial-review-and-refinement
    실제 변경 증거 → reviewing-and-validating-project-changes
    ```

    - 로컬·GitHub drift: `synchronizing-local-and-github-state`
    - 긴 작업 checkpoint·재개: `maintaining-long-running-task-continuity`
    - 게임 사용자 연구 11영역: `governing-game-user-research-coverage`
    - 사용자 학습 자료: `creating-user-learning-notes`
    - 프로젝트 HTML·상태 시각화: `building-project-visual-dashboards`
    - Godot·Unity 런타임 오류: `diagnosing-game-engine-runtime-failures`

    전체 원문 책임 매핑은 `docs/SKILL_COVERAGE_MAP.md`, 기계 검증은 `skills/SKILL_COVERAGE.json`을 사용한다.
    '''
)

append_once(
    "docs/OPERATING_MODEL.md",
    "## 구조 최적화·작업 지원 Skill",
    r'''
    ## 구조 최적화·작업 지원 Skill

    Base와 프로젝트 구조를 줄이거나 바꿀 때는 `pruning-stale-and-nonfunctional-material → simplifying-skill-bodies → refactoring-with-contract-preservation → running-adversarial-review-and-refinement → reviewing-and-validating-project-changes` 순서로 기능 보존과 회귀를 확인한다.

    Git 상태는 `synchronizing-local-and-github-state`, 긴 실행의 checkpoint는 `maintaining-long-running-task-continuity`, Games User Research 11영역은 `governing-game-user-research-coverage`, 학습 자료는 `creating-user-learning-notes`, 시각 작업 공간은 `building-project-visual-dashboards`, 엔진 런타임 오류는 `diagnosing-game-engine-runtime-failures`가 책임진다.

    책임 coverage 원본은 `skills/SKILL_COVERAGE.json`이며 사람용 설명은 `docs/SKILL_COVERAGE_MAP.md`다.
    '''
)

append_once(
    "docs/DOCUMENTATION_MAP.md",
    "## 구조 최적화·추가 전문 Skill",
    r'''
    ## 구조 최적화·추가 전문 Skill

    | 책임 | Skill | 주요 mode |
    |---|---|---|
    | 무손실 가지치기 | `pruning-stale-and-nonfunctional-material` | `inventory / classify / preserve-unique / prune-approved / verify-no-loss` |
    | 본문 간소화 | `simplifying-skill-bodies` | `inventory / extract-references / rewrite-router / validate-disclosure` |
    | 동작 보존 리팩토링 | `refactoring-with-contract-preservation` | `baseline-contract / smell-audit / refactor / regression-validate` |
    | 로컬·GitHub 동기화 | `synchronizing-local-and-github-state` | `inspect / reconcile / refresh-local / publish-remote / verify-sync` |
    | 장기 작업 연속성 | `maintaining-long-running-task-continuity` | `initialize / checkpoint / resume / partial-delivery / close` |
    | Games User Research 11영역 | `governing-game-user-research-coverage` | `install / audit / plan-evidence / synthesize / verify-coverage` |
    | 사용자 학습 노트 | `creating-user-learning-notes` | `capture / explain / connect / practice / update` |
    | 프로젝트 대시보드 | `building-project-visual-dashboards` | `frame / map-sources / build / bind-status / validate` |
    | 엔진 런타임 디버깅 | `diagnosing-game-engine-runtime-failures` | `reproduce / isolate / fix-minimally / revalidate / prevent` |

    원문 책임 누락 검증: `docs/SKILL_COVERAGE_MAP.md` → `skills/SKILL_COVERAGE.json` → `tools/check_skill_system_coverage.py`.
    '''
)

append_once(
    "templates/project-operations/AI_WORKFLOW.md",
    "## 구조 최적화·추가 지원 Skill",
    r'''
    ## 구조 최적화·추가 지원 Skill

    | 작업 | Skill |
    |---|---|
    | 중복·죽은 자료 가지치기 | `pruning-stale-and-nonfunctional-material` |
    | SKILL.md 점진적 공개 | `simplifying-skill-bodies` |
    | 기능 보존 리팩토링 | `refactoring-with-contract-preservation` |
    | 로컬·GitHub 동기화 | `synchronizing-local-and-github-state` |
    | 장기 작업 checkpoint | `maintaining-long-running-task-continuity` |
    | Games User Research 11영역 | `governing-game-user-research-coverage` |
    | 사용자 학습 노트 | `creating-user-learning-notes` |
    | 시각 대시보드 | `building-project-visual-dashboards` |
    | 엔진 런타임 오류 | `diagnosing-game-engine-runtime-failures` |
    '''
)

change_path = ROOT / "docs/CHANGELOG.md"
change = change_path.read_text(encoding="utf-8")
change_anchor = "## Unreleased - Base audit and operating-contract consistency\n\n"
change_bullets = (
    "- 제공된 학습 텍스트의 책임을 전수 매핑하고 9개 독립 Skill을 추가했으며, 중복 책임은 기존 통합 Skill에 유지했다.\n"
    "- 가지치기·본문 간소화·행동 보존 리팩토링 Skill을 분리하고 이를 Base의 코어·컨셉·적대적 검토·Skill 진화 본문에 실제 적용했다.\n"
    "- Games User Research 11영역, 로컬·GitHub 동기화, 장기 작업 연속성, 사용자 학습 노트, 프로젝트 대시보드, 엔진 런타임 디버깅 계약을 추가했다.\n"
    "- 원문 책임 coverage JSON·checker·회귀 테스트와 최적화 보고서를 추가했다.\n"
)
if change_bullets not in change:
    change = change.replace(change_anchor, change_anchor + change_bullets)
change_path.write_text(change, encoding="utf-8")

learning_path = ROOT / "skills/SKILL_LEARNING_LOG.md"
learning = learning_path.read_text(encoding="utf-8")
learning_anchor = "# Base Skill Learning Log\n\n"
learning_section = clean(r'''
## 2026-07-22 원문 책임 전수 매핑·Skill 구조 최적화

- 1,201줄 학습 텍스트의 책임을 `skills/SKILL_COVERAGE.json`에 전수 매핑했다.
- 가지치기·본문 간소화·행동 보존 리팩토링은 입력·산출물·삭제 권한·검증이 달라 독립 Skill로 분리했다.
- 동기화·장기 작업 연속성·Games User Research 11영역·학습 노트·시각 대시보드·엔진 디버깅도 기존 Skill로 흡수할 수 없는 독립 계약으로 판정했다.
- 요청 명세화·Issue/Goal·MVP·벤치마킹·문서 기억·검증은 기존 Skill에 이미 기능이 있어 중복 신설하지 않았다.
- 코어 판정·코어 확정·적대적 검토·컨셉 분석·Skill 진화 본문을 compact router로 리팩토링하고 상세 판정표를 reference로 이동했다.
- 전용 checker와 PR 회귀 테스트로 coverage, Registry, front matter, 파일 존재, 본문 최소 계약과 compact line budget을 검증한다.
- 현재 지식 상태: 실제 Base 적용은 `OBSERVATION`, 여러 프로젝트 반복 전까지 새 Skill 계약은 `HYPOTHESIS`.

''')
if "## 2026-07-22 원문 책임 전수 매핑·Skill 구조 최적화" not in learning:
    learning = learning.replace(learning_anchor, learning_anchor + learning_section)
learning_path.write_text(learning, encoding="utf-8")

# Update structural regression expectations.
structure_path = ROOT / "tests/test_game_project_operating_system_structure.py"
structure = structure_path.read_text(encoding="utf-8")
structure = structure.replace('self.assertEqual(len(registry["skills"]), 16)', 'self.assertEqual(len(registry["skills"]), 25)')
required_anchor = '            "skills/evolving-project-discipline-skills/SKILL.md",\n'
required_paths = (
    '            "skills/pruning-stale-and-nonfunctional-material/SKILL.md",\n'
    '            "skills/simplifying-skill-bodies/SKILL.md",\n'
    '            "skills/refactoring-with-contract-preservation/SKILL.md",\n'
    '            "skills/synchronizing-local-and-github-state/SKILL.md",\n'
    '            "skills/maintaining-long-running-task-continuity/SKILL.md",\n'
    '            "skills/governing-game-user-research-coverage/SKILL.md",\n'
    '            "skills/creating-user-learning-notes/SKILL.md",\n'
    '            "skills/building-project-visual-dashboards/SKILL.md",\n'
    '            "skills/diagnosing-game-engine-runtime-failures/SKILL.md",\n'
    '            "skills/SKILL_COVERAGE.json",\n'
    '            "docs/SKILL_COVERAGE_MAP.md",\n'
    '            "docs/SKILL_SYSTEM_OPTIMIZATION_REPORT.md",\n'
    '            "tools/check_skill_system_coverage.py",\n'
    '            "tests/test_skill_system_coverage.py",\n'
)
if required_paths not in structure:
    structure = structure.replace(required_anchor, required_anchor + required_paths)
structure_path.write_text(structure, encoding="utf-8")

# Remove the one-time generator and workflow from the resulting commit.
for relative in (
    "tools/apply_skill_system_expansion.py",
    ".github/workflows/agent-expand-and-optimize-skill-system.yml",
):
    path = ROOT / relative
    if path.exists():
        path.unlink()
