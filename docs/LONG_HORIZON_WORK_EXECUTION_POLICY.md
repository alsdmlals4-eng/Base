# Base 장기 작업 실행 정책

이 문서는 Base와 Base를 채택한 프로젝트에서 **시간보다 기획 의도·정확성·복원성·검증 가능성을 우선하는 장기 작업**의 공용 생명주기를 정의한다.

이 정책은 새 Skill이나 새 Work Mode가 아니다. 기존 책임자를 한 흐름으로 조합한다.

- 요청·승인·연속작업: `managing-project-intake-and-work-contract`
- 프로젝트 운영체계: `managing-game-project-operating-system`
- 적대적 검토: `running-adversarial-review-and-refinement`
- Git/PR 동시작업 조정: `synchronizing-local-and-github-state`
- 정본·참조 신선도: `auditing-canonical-reference-freshness`
- 구형 자료·대체·Archive: `governing-legacy-retention-and-archives`
- 공용화 제안·교훈 환류: `managing-base-change-proposals`

`AGENTS.md`의 권한·안전 규칙, `docs/WORK_MODE_AND_SKILL_ROUTING.md`의 Work Mode, `docs/PLANNING_FIRST_GRILL_ME_BATCH_POLICY.md`의 사용자 결정 Gate를 대체하지 않는다.

## 1. Machine contract

```text
DIRECTION_FIRST
CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY
MINIMUM_VIABLE_ALTERNATIVES: 3
BENCHMARK_SYNTHESIS
BETTER_ALTERNATIVE_SEARCH
LONG_TERM_PLAN_FIT_REQUIRED
EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD
SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
RECOVER_TRY_ALTERNATIVES_RESUME
INDEPENDENT_WORKSTREAM_ISOLATION
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
ZERO_INCREMENTAL_COST_REQUIRED
CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO
PAID_PLAN_COUNT: 2
FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS
POSTMERGE_PROMOTION_AND_SUPERSESSION
CORE_LOOP_DUMMY_BALANCE_BUILD_TEST
BALANCE_BUDGET
WORLD_STORYLINE_FIT_REQUIRED
REUSABLE_SYSTEM_EXTRACTION
FIGMA_DEFAULT_VISUAL_WORKSPACE
REPO_NATIVE_STRUCTURED_DATA
GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE
EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE
TOOL_HUB: REQUIRED_WHEN_RELEVANT
LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT
REQUIRED_WORK_REMAINING: 0
```

위 표기는 테스트·라우팅을 위한 안정 계약 이름이며, 실제 판정은 아래 세부 규칙과 현재 저장소 증거를 함께 사용한다.

## 2. 장기 작업 기본 흐름

```text
RESEARCH
→ CURRENT STATE / OPEN PR RECONCILIATION
→ DIRECTION / INTENT
→ >= 3 VIABLE ALTERNATIVES
→ BENCHMARK SYNTHESIS
→ TRADE STUDY
→ PROVISIONAL BEST OPTION
→ EXPECTED EFFECTS / RISKS / MITIGATIONS
→ ONE USER APPROVAL
→ SMALL TESTABLE SLICES
→ TOOL / RUNTIME EXECUTION
→ FIVE FULL ADVERSARIAL IMPROVEMENT LOOPS
→ LONG-TERM FIT CLOSURE
→ EXACT-HEAD PR GATE
→ MERGE
→ POSTMERGE READBACK
→ LESSON PROMOTION / SUPERSESSION
→ REQUIRED WORK REMAINING = 0
```

### `DIRECTION_FIRST`

1. 현재 사용자 목표, 플레이어 가치, 성공 조건, 비목표를 먼저 복원한다.
2. 최신 `main`, 같은 Goal의 열린·최근 병합 PR, 정본, 실제 구현, 테스트, 실패 사례를 대조한다.
3. 세부 수치나 구현 편의가 큰 방향을 역으로 결정하지 못하게 한다.
4. 방향을 바꾸는 선택은 Grill Me로 사용자와 닫고, 방향을 보존하는 가역적 세부값은 GPT 권장 기본값으로 진행한다.

작업 시간이 길어져도 방향·제약·정본·검증이 누락되는 것보다 낫다. 반대로 “꼼꼼함”을 이유로 불필요한 문서·Skill·승인 Gate를 늘리지 않는다.

## 3. 벤치마킹·현행 조사·대안 비교

### `CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY`

L1 이상 중요한 설계·구현·정책 결정은 한 가지 해법을 먼저 선택한 뒤 벤치마킹으로 정당화하지 않는다. **현행 조사 → 최소 3개 실질 대안 탐색 → 벤치마킹 → 동일 기준 비교 → 임시 권장안 → 전체 적대적 개선 루프 → 장기 최선안** 순서를 기본으로 한다.

```text
current-state evidence
→ >= 3 materially distinct viable alternatives
→ benchmark + industry practice + success/failure cases
→ common trade criteria
→ provisional recommendation
→ better-alternative search
→ five full adversarial improvement loops
→ long-term-plan-fit closure
→ long-term recommendation
```

- **현행 조사**는 최신 `main`, 실제 구현, 현재 정본, 열린·최근 병합 PR, 테스트·실패 증거, Tool/Runtime 상태와 비용 제약을 읽고 시작한다.
- **`MINIMUM_VIABLE_ALTERNATIVES: 3`**: L1 이상 중요한 결정은 현재 Goal에서 실제로 실행 가능한 materially distinct 대안을 **최소 3개** 확보한다. 현행 유지/재사용/흡수/최소 수정/구조 개선/신규 구축 중 해당되는 전략을 넓게 탐색한다.
- 세 후보는 숫자를 채우기 위한 허수 대안이어서는 안 된다. 차이가 이름뿐이거나 실질적으로 같은 구현이면 하나의 대안으로 계산한다.
- 처음에 세 후보가 보이지 않으면 조사 범위와 추상화 수준을 넓혀 `현행 유지`, `기존 것 재사용·흡수`, `구조 개선`, `신규 구축`, `외부 검증된 해법 채택` 등 전략적으로 다른 경로를 찾는다. 조사 뒤에도 구조적으로 세 실질 후보를 만들 수 없는 특수 제약이면 기준을 조용히 낮추지 말고 제한 사유와 탈락 증거를 기록해 `BLOCKED_UNVERIFIED` 또는 적절한 Decision Gate로 보낸다.
- 벤치마킹·현업 조사·성공사례·실패사례는 한 사례를 모방하는 것이 아니라 작동 원리와 실패 조건을 추출한다.
- 비교 기준은 작업 성격에 맞게 고르되 최소한 사용자/플레이어 가치, 정확성·기획 충실도, 위험, 수명주기 비용, 유지보수성, 되돌리기 난이도, 재사용·모듈성, 증거 강도, 현재 무료/구독 범위 적합성을 본다.
- **`BETTER_ALTERNATIVE_SEARCH`**: 최초 임시 권장안을 고른 뒤에도 새 테스트·실패·적대적 finding·환경 변화가 생기면 더 나은 방안이 나타났는지 다시 찾는다. 기존 결론을 방어하는 것이 목표가 아니다.
- 더 나은 기술적 대안이 승인된 방향·범위 안에 있으면 근거와 함께 채택할 수 있다. 프로젝트 코어·플레이어 경험·중요 스토리 의미·비용·승인 범위를 바꾸면 `USER_DECISION_REQUIRED`로 올린다.
- **`LONG_TERM_PLAN_FIT_REQUIRED`**: 최종 선택은 현재 작업만 통과하면 되는 것이 아니라 장기계획에 맞아야 한다. 최소한 수명주기 비용, 유지보수성, 되돌리기, 재사용/모듈화, 향후 Base 업데이트·정본 신선도, 사용자/플레이어 가치, 증거 강도, 현재 비용 경계를 재확인한다.
- 단기 구현량이 작다는 이유만으로 장기 부채가 큰 안을 선택하지 않고, “장기적”이라는 명분으로 현재 Goal 밖의 과잉 플랫폼·Skill·도구를 만들지도 않는다.
- 최종 권장안은 왜 최소 3개 후보보다 **장기적으로 최선**인지, 어떤 조건에서 재검토해야 하는지와 함께 기록한다.

### `BENCHMARK_SYNTHESIS`

벤치마킹은 한 성공사례를 모방하는 절차가 아니다. 시스템·게임·실무사례·실패사례를 여러 개 비교하고 각각의 **작동 원리**를 분리한다.

각 후보는 다음 중 하나로 판정한다.

```text
ADOPT / ADAPT / REJECT
```

- `ADOPT`: 현재 목표·비용·권위·기술 환경에 그대로 맞는다.
- `ADAPT`: 장점의 원리를 가져오되 프로젝트 세계관·핵심 경험·기술 경계에 맞게 재해석한다.
- `REJECT`: 인기·성공 여부와 무관하게 현재 프로젝트에는 비용·복잡도·권위·플레이어 가치가 맞지 않는다.

최소 비교 축:

- 사용자/플레이어에게 생기는 실제 가치
- 학습 비용과 조작 복잡도
- 제작·유지보수 비용
- 실패·복구 가능성
- 데이터·정본·도구 권위
- 모듈 재사용 가능성
- 무료/기존 구독 범위 실행 가능성

외부 근거는 요구사항 정본이 아니며, Base에서 동일한 성과 수치를 재현했다고 주장하려면 별도 실행 증거가 필요하다.

## 4. 구현 전 효과·문제·보완 Gate

### `EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD`

L1 이상 BUILD 전에 최소한 다음을 명시한다.

```yaml
expected_effects: []
likely_problems: []
mitigations: []
considered_alternatives: []
rejected_alternatives: []
provisional_best_option:
long_term_fit:
revisit_conditions: []
rollback: []
acceptance_criteria: []
verification_plan: []
```

장기적으로 더 강한 방안이 명확하면 당장의 구현량이 적다는 이유만으로 약한 임시안을 선택하지 않는다. 반대로 장기 효율을 명분으로 현재 목표와 무관한 플랫폼·프레임워크·Skill을 과잉 구축하지 않는다.

## 5. 승인 후 연속 실행

### `SINGLE_INITIAL_APPROVAL_THEN_CONTINUE`

완전한 작업 계약을 사용자에게 한 번 승인받은 뒤에는 같은 승인 범위의 다음 행위로 이동할 때 routine approval을 반복하지 않는다.

다음은 같은 승인 범위에서 계속 진행한다.

- 구현 세부 선택
- 테스트 추가·재실행
- 실패 원인 진단과 가역적 최소 수정
- PR 생성·exact-head 검사·리뷰 finding 반영
- 적대적 검토와 회귀 검사
- 저장소 정책이 허용하는 병합
- postmerge readback
- 승인 범위의 교훈 승격·대체 표시

다음은 다시 사용자 결정을 요구한다.

- 핵심 게임 방향·플레이어 경험·스토리 의미 변경
- 승인된 범위 확대 또는 다른 Goal 생성
- 파괴적 데이터 migration/삭제
- 새 결제·별도 과금·유료 API
- 계정·보안 권한 확대
- 서로 다른 유효한 결과 중 사용자 선호가 필요한 선택

`[연속작업] 진행해`가 명시된 경우 세부 recovery와 Global Progress Queue는 기존 `continuous-work-execution.md`를 따른다.

## 6. 오류·중단 복구

### `RECOVER_TRY_ALTERNATIVES_RESUME`

실패를 발견하면 같은 명령을 맹목적으로 반복하지 않는다.

```text
failure / interruption
→ side effect 가능성 판정
→ authoritative state readback
→ root-cause hypothesis
→ safe route A
→ 필요 시 safe route B/C
→ rollback / partial-state containment
→ completed work 보존
→ incomplete work만 resume
→ regression recheck
```

예:

- GitHub CLI 부재 → 연결된 GitHub connector가 같은 권한을 제공하면 connector 사용
- 한 테스트 경로의 환경 실패 → 같은 acceptance criterion을 증명하는 권위 있는 대체 실행 경로 탐색
- transient Actions failure → exact head·job·log를 재조회하고 실제 코드 실패와 runner/tooling 실패를 분리
- 로컬 도구 port 충돌 → 소유권을 확인한 별도 port/instance 사용, 임의 프로세스 종료 금지

새로운 증거가 생기지 않는 무한 retry는 금지한다.

## 6.5 독립 Workstream 격리

### `INDEPENDENT_WORKSTREAM_ISOLATION`

기본 규칙은 다음과 같다.

```text
OTHER_CHAT_BRANCH_PATH_PR: DO_NOT_TOUCH_BY_DEFAULT
EXPLICIT_USER_ABSORPTION_AUTHORIZATION: REQUIRED_FOR_EXCEPTION
```

- 다른 채팅, 다른 독립 Goal, 다른 프로젝트가 소유한 branch·worktree·path·PR은 같은 저장소에 있더라도 현재 작업의 수정 대상으로 간주하지 않는다.
- 현재 작업은 자기 전용 branch/worktree/path/port/Resource Lock을 사용하고, 다른 workstream의 dirty state나 미완성 RED/Draft를 정리한다는 이유로 임의 수정·강제 병합·force update하지 않는다.
- 같은 Goal의 선행 PR이라도 먼저 `REUSE / ABSORB / SUPERSEDE / KEEP_SEPARATE` 판정을 하고 실제 material delta만 통합한다. stale whole branch를 현재 main 위에 그대로 얹지 않는다.
- 예외는 사용자가 현재 작업에 대해 **명시적으로 흡수·통합을 승인한 경우**다. 이때도 unrelated PR은 범위 밖으로 보존할 수 있으며, 흡수한 PR은 successor·superseded 근거와 replacement pointer를 남긴다.
- 다른 workstream과 소유권이 불명확하면 수정부터 하지 말고 authoritative state를 재조회해 충돌을 fail closed로 처리한다.

이 규칙은 병렬 작업의 독립성을 보호하기 위한 기본값이며, 사용자의 최신 명시 지시가 특정 workstream 흡수를 허용하면 그 승인 범위 안에서만 예외가 적용된다.

## 7. Skill·도구 과잉 방지

Skill Registry의 hard ceiling은 채워야 하는 목표치가 아니다. 세부 sparse routing은 `docs/knowledge/ai/SKILL_ROUTING_PRECISION_GUIDE.md`를 따른다.

기능적으로 같은 책임은 다음 순서로 처리한다.

```text
REUSE → ABSORB → MERGE → ARCHIVE → BUILD_NEW
```

새 Skill·시스템·도구·plugin은 **독립 입력·산출물·권한·failure semantics·검증 경계**가 실제로 필요할 때만 만든다.

## 8. 게임 작업 공용 계약

### `CORE_LOOP_DUMMY_BALANCE_BUILD_TEST`

게임 기획·구현에서는 문서 완성 자체가 목적이 아니다. 플레이 가능한 핵심 경험을 증명하도록 다음 순서를 기본으로 한다.

```text
PLAYER PROMISE
→ CORE LOOP
→ CORE SYSTEMS
→ WORLD / STORYLINE FIT
→ REUSABLE MODULE BOUNDARIES
→ DUMMY BALANCE BUDGET
→ PLAYABLE BUILD
→ DETERMINISTIC / RUNTIME TEST
→ EVIDENCE-BASED TUNING
```

### 8.1 핵심 시스템

- 플레이어가 반복해서 하는 행동, 선택, 위험, 보상, 진행을 먼저 고정한다.
- 핵심 재미와 직접 연결되지 않는 미니 시스템은 핵심 루프 검증을 방해하지 않는 순서로 둔다.
- 핵심 시스템과 독립성이 높은 미니 시스템은 다른 프로젝트에서도 쓸 수 있도록 입력·출력·상태·설정 경계를 분리한다.

### 8.2 `BALANCE_BUDGET`

초기 밸런스는 여러 곳에 magic number를 박는 방식이 아니라 **예산과 파라미터**로 설계한다.

예:

```yaml
budget_id: MARTIAL_ART_BUDGET
power_budget: 100
allocation:
  damage: 0
  control: 0
  mobility: 0
  defense: 0
  utility: 0
constraints: []
tuning_evidence: []
```

- `100` 같은 예시 수치는 프로젝트 확정값이 아니다.
- 실제 필드는 프로젝트 특성에 맞게 정의한다.
- 초기값은 `DETAILED_NUMERIC_DEFAULT`로 가역적이어야 한다.
- 데이터는 가능한 한 repo-native 설정으로 외부화해 테스트·비교·롤백하기 쉽게 만든다.
- 밸런스의 실제 적합성은 빌드/시뮬레이션/플레이테스트 증거 전에는 `NOT_RUN` 또는 해당 증거 상한으로 남긴다.

### 8.3 `WORLD_STORYLINE_FIT_REQUIRED`

핵심 스토리라인은 시스템과 따로 작성하지 않는다.

- 세계관이 플레이어의 반복 행동을 왜 하게 만드는지 설명해야 한다.
- 주요 갈등과 진행은 코어루프의 선택·보상·실패와 연결한다.
- 설정상 멋있지만 실제 게임 행동과 무관한 콘텐츠는 핵심 범위와 분리한다.
- 서사 프로젝트는 해당 프로젝트의 정본/서사 Skill을 사용하며 Base가 프로젝트 고유 세계관 정본을 소유하지 않는다.

### 8.4 `REUSABLE_SYSTEM_EXTRACTION`

모듈화는 코드 복사를 쉽게 만드는 것이 아니라 계약을 안정시키는 작업이다.

재사용 후보는 최소한 다음을 가져야 한다.

- 명시적 입력·출력
- 프로젝트 고유 데이터와 공용 로직의 분리
- 설정 가능한 budget/parameter
- 실패/복구 semantics
- 최소 fixture/test
- 프로젝트별 adapter 또는 data injection boundary

한 프로젝트의 세계관·고유 수치·정본을 공용 모듈에 박아 넣지 않는다.

## 9. Figma·Google Sheets·구조화 데이터 전환

### `FIGMA_DEFAULT_VISUAL_WORKSPACE`

새 프로젝트와 새 기획 작업의 **시각 협업 기본 작업면**은 프로젝트별 Figma다.

Figma가 소유하기 적합한 것:

- 방향 무드와 승인 레퍼런스
- 화면·컴포넌트·상태·프로토타입
- 이미지/시각 자료의 구조화·레이어화·재사용 분류
- WIP / Approved / Rejected / Final 시각 상태
- 구현에 pin한 visual handoff view

Figma는 게임 규칙·런타임 데이터·테스트 결과의 정본이 아니며, Figma readback 없이 업로드/동기화를 성공으로 주장하지 않는다.

### `REPO_NATIVE_STRUCTURED_DATA`

다음은 Figma로 옮겨 두 번째 정본을 만들지 않는다.

- 밸런스 수치
- 경제/확률
- schema
- runtime configuration
- save/state data contract
- 테스트용 fixture

프로젝트 기술에 맞는 JSON, CSV, Godot Resource 등 **repo-native structured source**를 정본으로 사용한다. 사람용 시각 요약은 Figma에서 해당 정본의 ID/Commit을 참조할 수 있다.

### `GOOGLE_SHEETS_LEGACY_MIGRATION_SOURCE`

기존 구성된 Google Sheets는 즉시 삭제하지 않는다. 전환 기간에는 **legacy compatibility + migration/proposal source**다.

```text
existing Sheet audit
→ Sheet-only proposal 보존
→ GitHub canon reconciliation
→ visual/human-facing content → Figma
→ structured runtime/balance data → repo-native source
→ Figma/repo readback
→ replacement pointer
→ active workflow removal
→ [대체됨] / SUPERSEDED / read-only archive
```

다음 조건 전에는 migration 완료를 주장하지 않는다.

- 고유 내용 손실 여부 확인
- `PROPOSED_SHEET_CHANGE` reconciliation
- 새 GitHub/Figma 위치 readback
- Decision/Commit/Artifact 연결
- rollback/reference path 보존

영구 삭제는 별도의 destructive operation이며 사용자 명시 승인 없이는 수행하지 않는다.

## 10. Tool Hub·외부 HTML 카탈로그·Figma

### `TOOL_HUB: REQUIRED_WHEN_RELEVANT`

로컬 도구 실행·상태·project binding·health·child lifetime이 작업 범위에 있으면 Tool Hub의 실제 registry/runtime/test를 사용한다. 카드가 보인다는 사실만으로 실행 가능 또는 검증 완료를 주장하지 않는다.

상태는 최소한 다음처럼 분리한다.

```text
AVAILABLE
VERIFIED
DEGRADED
BLOCKED_PLATFORM
BLOCKED_UNVERIFIED
NOT_RUN
```

### `EXTERNAL_HTML_TOOL_CATALOG: DERIVED_DISCOVERY_SURFACE`

외부 HTML 도구 카탈로그는 발견성과 안내를 위한 파생 surface다. 정확한 소유 파일/URL/생성 경로가 확인되지 않았다면 Tool Hub 자체나 실행 권위로 추정하지 않는다.

- 실행 권위: Tool Hub/실제 tool owner
- 등록 권위: 해당 Registry/manifest
- 발견 UI: HTML catalog
- runtime 증거: health/process/request/receipt/test

카탈로그와 실제 Registry가 다르면 카탈로그를 최신화하거나 `STALE_DERIVED_VIEW`로 표시한다. 카탈로그 표시는 실행 증거가 아니다.

## 11. Loop Engineering

### `LOOP_ENGINEERING: REQUIRED_WHEN_RELEVANT`

반복 Agent 실행·implementation package·Resource Lock·worktree 격리·Builder/Critic·project test·PR handoff·postmerge closure가 범위에 있으면 Loop Engineering 계약을 사용한다.

현재 구현 상태는 설명 문서의 과거 스냅샷보다 **machine-readable current checkpoint**를 우선한다.

- current operational checkpoint: `docs/operations/UNIVERSAL_LOOP_CROSS_PROJECT_ACCEPTANCE.json`
- foundation/history: `docs/LOOP_ENGINEERING_A2_RUNTIME.md`

`WAITING_INTEGRATION`은 merge 증거가 아니다. `FAKE`와 `REAL`, repository CI와 사용자 PC runtime, provider transport와 제품 변경 권위를 구분한다.

## 12. 최소 5회의 전체 적대적 개선 루프

### `FIVE_FULL_ADVERSARIAL_IMPROVEMENT_LOOPS`

L1 이상 작업에서 적대적 검토를 실행하면 **전체 적대적 검토 생명주기를 최소 5회 반복**한다. 다섯 개의 서로 다른 관점이나 공격면을 하나씩 수행하는 방식이 아니다. 각 회차는 전체 승인 범위를 처음부터 다시 검토하며, 앞 회차의 수정 결과 자체도 새 공격 대상이다.

한 회차의 필수 흐름:

```text
FULL_SCOPE_REVIEW
→ FIND
→ VALIDATE_CRITIQUE
→ REFINE_APPROVED_FINDINGS
→ VERIFY / REGRESSION_RECHECK
→ BETTER_ALTERNATIVE_SEARCH
→ LONG_TERM_PLAN_FIT_RECHECK
→ RE-ATTACK RESULTING STATE
```

각 회차의 `FULL_SCOPE_REVIEW`는 작업 성격에 적용되는 다음 전체 축을 함께 다시 본다.

- 사용자 의도·기획 방향·승인 범위·숨은 가정
- 정본·owner·Skill routing·중복·stale·schema·consumer·dependency
- 실제 구현·데이터·자산·Tool/Runtime·Figma/구조화 데이터 경계
- 실패 복구·부분 상태·branch/worktree/path/port·보안·secret·rollback
- 사용자/플레이어 가치·벤치마킹·비용·수명주기 유지보수·모듈화
- 정상 경로 회귀·evidence ceiling·exact-head·freshness·완료조건

이 축들은 **매 회차 전부 확인하는 checklist**이며, 각각을 별도 회차로 계산하지 않는다.

각 회차는 최소 다음을 기록한다.

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
```

규칙:

1. `FULL_LOOP_COUNT_MINIMUM: 5`. L1 이상에서 이 Skill을 적대적 검토로 실제 호출했다면 1~5회 전체 루프를 순서대로 닫는다. L0 단순 작업에 quota를 채우기 위해 Skill을 억지 호출하지 않는다.
2. finding을 나열만 하고 개선하지 않은 상태는, 개선 권한과 증거가 있는 경우 해당 회차 완료가 아니다. `MUST_FIX`와 승인된 `SHOULD_FIX`는 분야 owner에서 개선·보완하고 실제 검증을 거쳐야 한다.
3. 회차 N의 입력은 원칙적으로 회차 N-1의 **검증된 출력 상태**다. 앞 회차의 수정 결과가 새 충돌·누락을 만들었는지 다시 공격한다.
4. 각 회차에서 새 증거가 생기면 `BETTER_ALTERNATIVE_SEARCH`를 다시 실행한다. 최소 3개 후보를 처음 비교했다는 이유로 이후 더 나은 경로 탐색을 멈추지 않는다.
5. 각 회차에서 `LONG_TERM_PLAN_FIT_RECHECK`를 수행해 선택안이 장기계획·유지비·재사용·Base 변화·비용 경계에 계속 적합한지 확인한다.
6. **5회차**에서도 전체 범위를 처음부터 다시 본다. 5회차 뒤 P0/P1 또는 acceptance criterion을 막는 finding이 남으면 횟수를 채웠다는 이유로 종료하지 않는다. finding을 수정·검증한 뒤 **추가 전체 루프**를 수행해 개선된 상태를 다시 공격한다.
7. 새 더 나은 대안이 핵심 방향·승인 범위를 바꾸면 몰래 전환하지 않고 `USER_DECISION_REQUIRED`로 분리한다. 기술적으로 단일하며 기존 방향 안의 개선이면 승인된 연속작업 범위에서 반영할 수 있다.
8. `NOT_RUN`, `BLOCKED_UNVERIFIED`, `CANCELLED`는 PASS가 아니다. 실행 증거가 없으면 회차의 해당 항목은 미검증으로 남긴다.

## 13. PR·병합·postmerge

작업은 저장소가 허용한 작은 self-contained slice로 구현한다. 하나의 integration Goal 아래 여러 독립 테스트를 둘 수 있지만, 서로 무관한 제품 변경을 한 PR에 섞지 않는다.

병합 전:

- latest main 재조회
- open/recent PR semantic reconciliation
- actual changed paths 확인
- exact-head required checks
- unresolved review thread 0
- 최소 5회의 **전체 적대적 개선 루프** evidence와 각 회차 개선·검증 연결
- 최종 검증된 상태에서 `P0=0`, `P1=0`
- `LONG_TERM_PLAN_FIT_REQUIRED` 최종 재판정
- `NOT_RUN`/`BLOCKED_*` 과장 없음
- rollback 확인

병합 후:

### `POSTMERGE_PROMOTION_AND_SUPERSESSION`

```text
merged main SHA readback
→ changed canon readback
→ generated/derived consumers readback
→ postmerge regression evidence
→ incident / solution / lesson classification
→ reusable lesson promotion
→ old owner / doc / PR supersession
→ remaining-work calculation
```

- 대체된 문서·PR·기록은 `[대체됨]`, `SUPERSEDED`, archive manifest, replacement pointer 등 현재 구조가 사용하는 방법으로 오인 방지한다.
- 과거 증거는 삭제하지 않고 provenance를 보존한다.
- 프로젝트에서 발견된 공용 교훈은 Base 제안/학습 surface로 환류한다.

## 14. 완료와 남은 작업 0

`REQUIRED_WORK_REMAINING: 0`은 **현재 승인된 work contract의 acceptance criteria**에 대한 종료 조건이다. 미래 아이디어 전체를 0으로 만들라는 뜻이 아니다.

최종 보고는 반드시 세 축을 분리한다.

```yaml
required_work_remaining: 0 | N
external_blockers: []
optional_backlog: []
```

- acceptance criterion이 미충족이면 required work를 0으로 쓰지 않는다.
- 현재 세션 외 사용자 PC/기기/외부 계정 검증이 필요하면 external blocker로 남긴다.
- 장기 개선 아이디어는 optional backlog로 분리해 현재 완료를 불필요하게 막지 않는다.

## 15. 비용 경계

### `ZERO_INCREMENTAL_COST_REQUIRED`

기본 실행은 추가 결제 없는 경로만 사용한다.

```text
CURRENT_PAID_PLANS: GPT_PRO, FIGMA_PRO
PAID_PLAN_COUNT: 2
```

- 현재 사용 가능한 유료 플랜은 **GPT Pro와 Figma Pro 정확히 두 개**다.
- 두 플랜 안에서 이미 포함된 기능은 사용할 수 있지만, 별도 API·credit·metered billing·marketplace·runner·compute·storage·추가 SaaS 과금으로 넘어가면 허용 범위 밖이다.
- GPT Pro/Figma Pro 외의 새로운 유료 AI/API/SaaS/상위 플랜/유료 add-on을 도입·실행·결제하려면 **새 사용자 승인**이 필요하다.
- 별도 pay-as-you-go API, credit, 추가 SaaS, 유료 marketplace, 신규 유료 runner/compute/storage는 자동 도입하지 않는다.
- 비용 상태가 불명확하면 결제·live paid call을 실행하지 않고 `COST_GATE_BLOCKED`로 둔다.

## 16. Base 업데이트에 대한 신선도

Base는 주기적으로 변하므로 지시문이나 프로젝트가 특정 Skill 수·PR 번호·고정 문구를 영구 참조하지 않게 한다.

작업 시작 시 최소한 다음을 다시 찾는다.

```text
latest main SHA
→ START_HERE / AGENTS
→ DOCUMENTATION_MAP
→ SKILL_REGISTRY
→ same-goal open/recent PRs
→ current tool registries
→ current Loop checkpoint
→ project-local adopted Base pin / adapter
```

파생 문서와 설명이 machine checkpoint/Registry/actual code와 다르면 **현재 구현을 추정하지 말고 freshness finding**으로 처리한다.