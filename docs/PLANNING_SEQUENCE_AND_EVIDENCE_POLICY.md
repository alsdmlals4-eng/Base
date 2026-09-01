# 기획 작업순서·근거·데모 우선 정책

이 문서는 Base와 Base를 적용한 프로젝트에서 기획 작업을 어떤 순서로 묶고, 무엇을 먼저 비교하며, 어떤 근거로 승인하고, 새 정책·Template·Skill을 어디까지 전파 검증할지 정하는 공용 책임 원본이다.

프로젝트 기본 역할은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`와 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`, 승인 결정 동기화는 `docs/CONFIRMED_DECISION_SYNC_POLICY.md`, workspace 권위는 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`, 분야 횡단 게임개발 근거 허브는 `docs/knowledge/game-development/README.md`, 최신 외부 Source 후보와 주기 학습은 `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`, legacy 시각·asset·flow 자료는 `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`의 V4 exception/migration 경계에서만 읽고, legacy Sheet 이관·삭제는 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`와 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`, 데모 Gate는 `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`가 책임진다.

공통 조사 기록은 `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`, 성공·실패·혼합 사례는 `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`를 사용한다. Watchlist와 Source Queue는 조사 후보를 제공할 뿐 정본이나 학습 완료 증거가 아니며, 원출처 검토와 Evidence disposition 뒤에만 현재 결정에 사용한다.

## 1. 작업면과 정본

```text
REPOSITORY_PRIMARY_CANON
→ Markdown / JSON / game data / code / scene / resource / config / tests / approval and validation evidence

HUMAN_GDD_PDF_DERIVED_VIEW
→ exact source SHA / scope / evidence ceiling / person-facing snapshot

REPOSITORY_RUNTIME_TRUTH
→ actual build / runtime / evidence

V4_NOTION_EXCEPTION_ONLY / NO_NEW_NOTION_WRITE_BY_DEFAULT
→ explicit exception or legacy migration source only; never the default Project Home or active decision-sync owner

Google Sheets
→ `BASE_EXCLUDED` (Base repository)
→ `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` (legacy project sources only)
```

Google Sheets와 Notion은 새 기획·GDD·상태관리의 작업면이 아니다. 고유 미이관 정보가 실제로 남아 있는 migration scope에서만 unique / duplicate / obsolete를 분류해 repository-native owner로 옮기고 destination readback 뒤 active reference를 제거한다. V4 exception은 explicit user approval, owner, scope, measurable value, exit/revisit 조건이 있는 경우에만 적용한다.

Figma, 독립 HTML dashboard/catalog, project-management Tool Hub, QA Evidence Studio와 프로젝트 관리용 user-facing localhost apps도 새 기획 surface가 아니다. Project Home은 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`에 따라 핵심 방향·Core Loop·시스템·UX/Visual·구현·검증·blocker를 본문에서 직접 설명한다.

## 2. 내용 보존

- 문서·Skill·정책·Template에 줄 수·문자 수·페이지 수·분량 상한을 완료 조건으로 두지 않는다.
- 간결성보다 내용 보존, 실행 가능성, 책임 경계, 한 단계 발견성, 검증 가능성을 우선한다.
- Reference 분리는 축약을 위한 것이 아니라 책임 분리와 조건부 발견성을 위한 것이다.
- 기존 결정·예외·실패 조건·검증 절차가 손실되면 간소화가 아니라 회귀다.

## 3. 모든 L1 이상 작업의 선행 감사

```text
latest user request
→ project GitHub latest main
→ CURRENT_CONFIRMED_DECISIONS.md
→ relevant canonical owner
→ same-goal open/recent PR read-only reconciliation (`OPEN_PR_READ_ONLY_BY_DEFAULT`)
→ actual code / data / Scene / Resource / assets / tests
→ exact-SHA repository derived PDF and repository-native human view; V4 exception/legacy source only when its recorded scope applies
→ optional RETIRED_MIGRATION_ONLY Sheet only when migration is the current scope
→ Decision ID / Commit / repository/PDF readback / current stage comparison
→ duplicate / omission / conflict / stale reference / missing sync verdict
```

필수 판정:

- `DUPLICATE_WORK`: 같은 결과가 이미 정본·구현·PR에 존재.
- `DUPLICATE_QUESTION`: 유효한 기존 Decision을 다시 질문.
- `MISSING_CANON`: 승인 내용이 책임 원본에 승격되지 않음.
- `MISSING_CONSUMER`: 새 정책·Template·Skill을 읽어야 할 소비처 누락.
- `CANON_CONFLICT`: 현행 책임 원본끼리 결정 충돌.
- `IMPLEMENTATION_CONFLICT`: 정본과 실제 구현 불일치.
- `STALE_REFERENCE`: 구형 경로·ID·policy·retired surface 참조.
- `MISSING_SYNC`: repository structured owner와 required exact-SHA derived view의 동기화 누락, 또는 실제 V4 exception destination의 agreed scope readback 누락.
- `MIGRATION_PENDING`: legacy Sheet 등 폐기 surface의 고유 material 이관이 아직 완료되지 않음.
- `NO_CONFLICT`: 현재 범위 진행 가능.
- `BLOCKED_UNVERIFIED`: 필요한 권위·접근·증거 부족.

차단 Finding이 있으면 새 작업보다 복원·정리·재동기화를 먼저 수행한다.

## 4. 공통 8단계 작업 루프

```text
1. BASELINE_RECOVERY
→ 2. DUPLICATE_OMISSION_CONFLICT_AUDIT
→ 3. EVIDENCE_PACK
→ 4. APPROVAL_BUNDLE
→ 5. CANONICAL_UPDATE
→ 6. PROPAGATION_AUDIT
→ 7. VALIDATION
→ 8. GATE_CLOSE
```

### 4.1 BASELINE_RECOVERY

GitHub main, Decision, canonical owner, actual implementation, PR, repository의 exact-SHA 사람용 PDF/Markdown projection 상태를 복원한다. 명시적으로 승인·범위가 정해진 V4 Notion 예외 또는 migration scope일 때만 해당 surface와 legacy Sheet의 고유 material을 추가로 읽는다. 이미 확인 가능한 사실은 사용자에게 되묻지 않는다.

### 4.2 DUPLICATE_OMISSION_CONFLICT_AUDIT

같은 작업·질문을 문구만 바꿔 반복하지 않는다. retired Figma/Tool Hub/QA/HTML/Sheet/local surface가 current authority처럼 다시 노출되면 `STALE_REFERENCE`다.

### 4.3 EVIDENCE_PACK

중요 기획·방향성·제품 결정은 다음 세 층을 모두 검토한다.

1. `BENCHMARK_EVIDENCE`: 직접 경쟁작, 인접 장르, distinctive/innovative 사례, 실패·혼합 사례.
2. `PLAYER_RESPONSE_EVIDENCE`: 긍정·부정·혼합 리뷰, 커뮤니티, 플레이테스트, 행동 데이터.
3. `PROFESSIONAL_OFFICIAL_EVIDENCE`: 현업 발표·사후 분석·공식 플랫폼·엔진·접근성·운영 자료.

중요 게임 기획은 `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`와 `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`의 `CREATIVE_BENCHMARK_FRONTIER`, `ORIGINALITY_FUN_CREATIVITY_REVIEW`를 함께 적용한다. 재미는 실제 player evidence 전에는 hypothesis다.

필요 분야만 조사한다. 외부 Source 후보는 `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`에서 찾을 수 있지만, 후보 발견 자체를 Evidence나 canon promotion으로 취급하지 않는다. 가능한 한 원출처를 확인하고 현재 질문에 필요한 범위만 조사한다.

근거는 다음 tier를 구분한다.

```text
T1_PRIMARY_OFFICIAL
T2_PROFESSIONAL_PRACTICE
T3_PLAYER_BEHAVIOR
T4_PLAYER_SELF_REPORT
T5_SYNTHESIS
T6_AI_INFERENCE
```

AI 추론은 독립 권한이 없다. Evidence는 정본을 대체하지 않고 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 현재 프로젝트에 적용한다.

### 4.4 APPROVAL_BUNDLE

같은 플레이어 경험·시스템·정본·후속 구현에 영향을 주는 결정을 묶는다.

```yaml
Approval Bundle:
  bundle_id:
  discipline:
  current_decisions:
  duplicate_omission_conflict_result:
  evidence_pack_path:
  evidence_ids: []
  case_card_paths: []
  questions_and_options: []
  gpt_recommendation:
  approved_decisions: []
  dependencies: []
  affected_repository_owners: []
  affected_human_projection_or_v4_notion_exception: []
  migration_sources: []
  validation_gate:
```

기술 세부와 초기 수치는 `RECOMMENDED_DEFAULT`로 처리한다. 프로젝트 코어·중요 기획·방향성·정본 충돌만 `USER_DECISION_REQUIRED`로 올린다. 핵심 시스템 수치는 가능한 한 쉽게 변경 가능한 `BALANCE_BUDGET`/범위/상대값으로 먼저 잡고 최종값으로 과장하지 않는다.

### 4.5 CANONICAL_UPDATE

승인 Decision을 `CURRENT_CONFIRMED_DECISIONS.md`, 분야 repository owner, 필요한 Active Context·Issue·Plan과 exact-SHA 사람이 읽는 PDF/Markdown projection에 반영하고 readback한다. 명시적으로 승인·범위가 정해진 V4 Notion 예외만 해당 filtered surface에도 반영한다.

legacy Sheet는 migration input일 뿐 승인 결과의 정상 sync target이 아니다.

### 4.6 PROPAGATION_AUDIT

새 정책·Template·Skill·경로·ID를 추가하거나 바꾸면 파일 존재가 아니라 실제 소비를 검사한다.

- `AGENTS.md`, `START_HERE.md`, `README.md`.
- `OPERATING_MODEL`, GPT-first workflow, long-horizon, Work Mode, Documentation Map.
- Skill Registry, Legacy Alias, shared route.
- 프로젝트 설치 Template과 Project START_HERE / AI_WORKFLOW.
- `docs/knowledge/game-development/README.md`와 관련 분야 Skill/Reference/data contract.
- Evidence Pack, Case Card, benchmark source와 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`.
- reference freshness, regression, publication/generation, governance.
- exact-SHA repository human projection 또는 명시된 V4 Notion exception surface.
- tests / runtime evidence / postmerge readback.

retired Figma/Tool Hub/QA/Sheet/HTML/local app는 active consumer 목록에 넣지 않는다. 이관 작업에서는 migration/history source로만 기록한다.

### 4.7 VALIDATION

정본 비교, 정적 검사, runtime, 접근성, 성능, 플레이테스트, 반응 조사, AI Eval, 적대적 검토 중 현재 범위에 필요한 검증을 실제 실행한다.

적대적 검토는 최소 다음 실패 가정을 본다.

- 성공 사례의 표면 복사.
- 장르·팀 규모·플랫폼 과잉 일반화.
- 독창성 명목의 gimmick/복잡성 증가.
- 행동과 자기보고 혼동.
- AI 추론을 공식 사실로 사용.
- 접근성·성능·보안·라이선스·제작비 누락.
- 새 Skill·Guide·Template의 중복 책임.
- retired surface 재도입.
- 실행하지 않은 검증 완료 주장.

### 4.8 GATE_CLOSE

```text
APPROVED
CANON_UPDATED
HUMAN_PROJECTION_UPDATED | V4_NOTION_EXCEPTION_UPDATED | HUMAN_PROJECTION_NOT_APPLICABLE
CONSUMERS_UPDATED
IMPLEMENTED | IMPLEMENTATION_PENDING
VALIDATED | BLOCKED_UNVERIFIED
MIGRATION_COMPLETE | MIGRATION_NOT_APPLICABLE | MIGRATION_PENDING
```

## 5. GPT planning / Codex Godot product implementation boundary

기획·근거조사·대안 비교·UI/UX·아트 방향·시각 후보 검수·최종 판정은 `GPT_FIRST_PLANNING_AND_REVIEW`와 `GPT_PRIMARY_REVIEWER`가 기본이다. 프로젝트 작업은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 `PLAY_MEANINGFUL_WORK_SLICE`를 기본 작업 단위로 삼고, 실제 구현 전에 승인된 기획 의미와 실행 계약을 `PLANNING_CANON_BEFORE_HANDOFF`로 정본화한다.

실제 Godot 제품 구현이 남지 않은 계획은 GPT가 비코딩 결과와 정본 readback을 닫고 종료한다. 실제 Godot 제품 구현이 남아 있으면 GPT가 `PRE_HANDOFF_GPT_STOP`을 통과한 뒤 구현 방법을 더 세분화하지 않고 다음 current boundary를 따른다.

```text
PLAY_MEANINGFUL_WORK_SLICE
→ PLANNING_CANON_BEFORE_HANDOFF
→ PRE_HANDOFF_GPT_STOP
→ ACTUAL GODOT PRODUCT IMPLEMENTATION → Codex
→ READY_FOR_GPT_REVIEW
→ GPT final review
```

Codex는 모든 계획에 붙는 선택적 보조 실행자가 아니라 **실제 게임 프로젝트의 Godot 제품 구현 owner**다. 반대로 Base·Notion·기획·문서·Visual 같은 비제품 구현은 Codex로 넘기지 않는다. 사용자가 local implementation을 실행해야 할 때는 `docs/operations/POWERSHELL_FRESH_SHELL_EXECUTION_CONTRACT.md`의 location-first 한 블록을 사용한다.

```text
GPT_PRIMARY_IS_DECISION_OWNERSHIP_NOT_TEXT_ONLY
REASONING_EFFORT_IS_NOT_WORK_EVIDENCE
REQUIRED_TOOL_EXECUTION_IS_NOT_OPTIONAL_EXECUTOR_HANDOFF
```

GPT-primary는 답변 문장만 만드는 경로가 아니다. 추론 강도는 실제 조사·readback·Tool 실행·검증 증거가 아니며, 현재 세션이 필요한 browser/repository/connector/runtime Tool을 보유하면 직접 사용한다. Codex의 제품 구현 책임 경계와 별개로 필수 실행 evidence는 실제로 확보해야 한다.

## 6. 시각 checkpoint와 Demo-First

```text
PROJECT_VISUALIZATION_NEED_MAP
→ VISUALIZED_POC_BEFORE_DEMO_TEST
→ REPRESENTATIVE_UX_UI_STATE_REQUIRED_WHEN_VISUALS_MATTER
→ APPROVED_VISUAL_INPUTS_FEED_POC
→ DEMO_FIRST_VERTICAL_SLICE
→ DEMO_VALIDATION
```

이미지·UI·UX가 테스트 판단을 바꿀 수 있으면 대표 화면 상태를 GPT에서 기획·검수하고 repository의 exact-SHA visual manifest와 사람용 PDF/Markdown projection에 배치·readback·승인한 뒤 PoC/demo 입력으로 사용한다. 명시적으로 승인·범위가 정해진 V4 Notion 예외만 해당 Notion surface에 배치한다. 생성 성공/업로드 성공만으로 승인이나 runtime 적용을 주장하지 않는다.

별도 `CORE_POC`를 모든 프로젝트의 필수 독립 단계로 만들지 않는다. 가장 큰 기술 불확실성만 격리해야 하면 `TECHNICAL_SPIKE`를 사용한다. 시스템-only Spike는 알고리즘·데이터·호환성 질문을 푸는 내부 증거이고, 플레이어 경험 검증은 **shipping-intent UI/UX·art/image·audio·VFX·system/content가 연결된 release-near Vertical Slice**에서 수행한다.

## 7. 사람용 Project surface 순서

일반 게임 프로젝트의 사람이 보는 기본 발견 순서는 다음처럼 유지한다.

```text
Project Home
→ Project Control
→ Reference / Benchmark
→ Visual / Story Bible
→ Core System / confirmed human tables
→ Production / Handoff
```

프로젝트 특성상 Storyboard, Character, Faction, Clue, economy/tier/roster page가 필요하면 책임이 실제로 다를 때만 추가한다. Sheet tab 구조를 새로운 표준으로 유지하지 않는다.

## 8. 승인 후 닫힘

material approval은 다음 상태까지 같은 승인 단위로 닫는다.

```text
user approval
→ adversarial review (minimum five full loops for L1+ long-horizon scope, then clean exit)
→ repository structured update
→ exact-SHA human PDF/Markdown projection update/readback; V4 Notion exception update/readback only when expressly scoped
→ branch / commit / PR
→ exact-head required checks
→ merge
→ postmerge GitHub main readback
→ repository projection destination/status readback; V4 Notion exception readback only when applicable
→ incident/solution/lesson classification
→ learning-oriented completion report
```

이미지 파일도 implementation-bound approval이면 provenance, repository asset path, PR/merge, runtime consumption evidence를 구분해 확인한다. planning-only visual은 exact-SHA repository visual manifest/human projection readback을 닫되 runtime PASS로 승격하지 않는다. V4 Notion exception은 실제 적용됐을 때만 추가 readback한다.

## 9. 재검토 조건

다음 경우 기획 workflow를 재검토한다.

- Notion 무료/current capability가 반복적으로 material planning을 차단.
- project 규모·협업자 수 때문에 current Project relation model이 부족.
- GPT가 직접 안정적인 engine mutation/verification을 수행할 공식 surface가 생김.
- Codex 실행환경·비용·권한이 크게 변함.
- retired surface에서 아직 고유 material이 반복 발견됨.
- 창의성 benchmark frontier가 실제 프로젝트에서 선택 품질을 높이지 못하거나 조사비용만 크게 늘림.
