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
BENCHMARK_SYNTHESIS
EXPECTED_EFFECTS_RISKS_MITIGATIONS_BEFORE_BUILD
SINGLE_INITIAL_APPROVAL_THEN_CONTINUE
RECOVER_TRY_ALTERNATIVES_RESUME
ZERO_INCREMENTAL_COST_REQUIRED
FIVE_DISTINCT_ADVERSARIAL_ROUNDS
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
→ BENCHMARK SYNTHESIS
→ EXPECTED EFFECTS / RISKS / MITIGATIONS
→ ONE USER APPROVAL
→ SMALL TESTABLE SLICES
→ TOOL / RUNTIME EXECUTION
→ FIVE DISTINCT ADVERSARIAL ROUNDS
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

## 3. 벤치마킹과 재해석

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
rejected_alternatives: []
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

## 12. 정확히 5회의 적대적 검토

### `FIVE_DISTINCT_ADVERSARIAL_ROUNDS`

L1 이상 장기 작업의 최종 통합 검토는 **정확히 다섯 개의 서로 다른 공격면**으로 수행한다. 같은 질문을 다섯 번 반복하지 않는다.

### Round 1 — Intent / Assumptions / Scope

- 사용자 기획 의도를 편의상 재해석했는가
- 승인 범위를 무단 확대/축소했는가
- 큰 방향보다 세부 구현이 앞섰는가
- 숨은 가정이 있는가

### Round 2 — Canon / Ownership / Structure / Dependencies

- 같은 사실을 두 정본이 소유하는가
- Skill/Tool/Policy 역할이 겹치는가
- stale generated/derived view가 정본처럼 보이는가
- 참조·schema·consumer propagation이 누락됐는가

### Round 3 — Failure / Security / Concurrency / Recovery

- 실패 시 부분 상태가 남는가
- port/worktree/branch/path ownership이 충돌하는가
- retry가 중복 side effect를 만드는가
- credential/secret/raw reasoning이 새는가
- fail-closed 상태를 PASS로 오인하는가

### Round 4 — Player Value / Benchmark / Cost / Maintainability

- 실제 사용자/플레이어 가치가 있는가
- 성공사례를 표면 복제했는가
- 더 단순하고 검증된 대안이 있는가
- 장기 유지비가 효과를 초과하는가
- `ZERO_INCREMENTAL_COST_REQUIRED`를 깨는가

### Round 5 — Regression / Evidence / Completion / Freshness

- 변경 전 동작을 불필요하게 깨뜨렸는가
- exact-head가 아닌 과거 성공을 재사용했는가
- 테스트·runtime·Figma/tool evidence 상한을 과장했는가
- merge 후 main readback과 successor/reference update가 빠졌는가
- acceptance criterion 누락을 optional backlog로 숨겼는가

각 Round는 다음을 기록한다.

```yaml
attack_hypothesis:
evidence_checked: []
findings: []
severity: P0 | P1 | P2 | P3
resolution: FIXED | REJECTED_CRITIQUE | DEFERRED_OPTIONAL | BLOCKED
recheck:
unresolved: []
```

병합 전 `P0=0`, `P1=0`이어야 한다. P2/P3도 acceptance criterion을 막으면 수정한다.

## 13. PR·병합·postmerge

작업은 저장소가 허용한 작은 self-contained slice로 구현한다. 하나의 integration Goal 아래 여러 독립 테스트를 둘 수 있지만, 서로 무관한 제품 변경을 한 PR에 섞지 않는다.

병합 전:

- latest main 재조회
- open/recent PR semantic reconciliation
- actual changed paths 확인
- exact-head required checks
- unresolved review thread 0
- 다섯 Round P0/P1 0
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

- 현재 사용자가 이미 보유한 GPT Pro/Figma Pro 범위는 사용할 수 있다.
- 별도 pay-as-you-go API, credit, 추가 SaaS, 유료 marketplace, 신규 유료 runner/compute/storage는 자동 도입하지 않는다.
- 기존 구독 기능이라도 별도 metered billing으로 전환되면 차단한다.
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
