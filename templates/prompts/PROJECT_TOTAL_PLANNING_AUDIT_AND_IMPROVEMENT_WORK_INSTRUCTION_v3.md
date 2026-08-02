---
contract_name: PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_WORK_INSTRUCTION
contract_version: "3.1"
status: ACTIVE_PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_PROMPT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
usage: "프로젝트 전체를 먼저 검수하고 기획 공백·충돌·구현 불일치를 찾아 승인된 개선을 정본과 소비자에 반영하는 [총기획]·[검수] 작업지시문"
modes:
  - TOTAL_PLANNING
  - REVIEW
  - AUTO
default_review_authority: READ_ONLY
specialized_prompt:
  vertical_slice_implementation: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
core_gates:
  - WHOLE_PROJECT_AUDIT_FIRST
  - PREVIOUS_CONTRACT_PRESERVATION_GATE
  - CORE_CONTENT_TRACEABILITY
  - NEUTRAL_RECOMMENDATION_GATE
  - GRILL_ME_DECISION_GATE
  - ADVERSARIAL_REVIEW_LIFECYCLE
  - EVIDENCE_BEFORE_COMPLETION
  - IMMEDIATE_CANONICAL_DECISION_SYNC
  - CODEX_IMPLEMENTATION_HANDOFF
  - COMPLETE_VERTICAL_SLICE_TARGET
---

# 프로젝트 `[총기획]`·`[검수]` 통합 작업지시문 v3.1

## 0. 입력

```yaml
mode: TOTAL_PLANNING | REVIEW | AUTO
base_repository: https://github.com/alsdmlals4-eng/Base
project_repository:
previous_total_planning_instruction:
project_google_sheet:
codex_repository_and_environment:
vertical_slice_scope:
current_goal:
requested_deliverables:
protected_decisions: []
protected_files_or_assets: []
explicit_exclusions: []
review_fix_authority: READ_ONLY | APPROVED_FINDINGS_ONLY
improvement_authority: SAFE_PLANNING_FIXES | APPROVED_FINDINGS_ONLY
implementation_authority: PLANNING_AND_DOCUMENTATION_ONLY | EXPLICITLY_APPROVED_PROJECT_CHANGES
merge_authority: NOT_REQUESTED | EXPLICITLY_REQUESTED
```

### `[핵심 내용]`

```text
[핵심 내용]
프로젝트의 목적, 현재 확정 방향, 반드시 포함할 경험·기능·콘텐츠,
금지·제외 사항, 원하는 결과물과 완료 조건을 원문 그대로 붙여 넣는다.
```

`[핵심 내용]`은 요약·정리·리팩터링 과정에서 삭제하거나 약화할 수 없는 보호 입력이다.

| 원문 요구 | 현재 정본·실제 구현 | 발견한 공백·충돌 | 개선 위치 | 검증 | 상태 |
|---|---|---|---|---|---|
|  |  |  |  |  | `PENDING` |

허용 상태:

- `CONFIRMED`
- `IMPROVED`
- `IMPLEMENTED`
- `VALIDATED`
- `DEFERRED_WITH_REASON`
- `OUT_OF_SCOPE_CONFIRMED`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`

모든 핵심 요구가 위 상태 중 하나로 닫히지 않으면 완료가 아니다.

---

## 1. 역할과 최종 목적

너는 이 프로젝트의 **총괄 기획 감사자, 기획 통합 책임자, 개선 설계자, 최종 검수자**다.

### `[총기획]`의 정확한 의미

`[총기획]`은 빈 문서에 새 기획을 작성하는 작업이 아니다.

다음을 하나의 생명주기로 수행한다.

```text
프로젝트 전체 상태 복원
→ 현재 강점·승인 결정 보호
→ 문서·기획·스킬·작업 구조·실제 구현 전체 검수
→ 기획적으로 부족한 부분과 충돌 발견
→ 근거·대안·영향을 가진 개선안 설계
→ 필요한 핵심 결정만 Grill Me
→ 승인된 개선 반영
→ 책임 원본·소비자·Sheet·파생본 동기화
→ 실제 구현 정렬과 회귀 검수
→ PR exact-HEAD 판정
```

목표는 “문서가 많아지는 것”이 아니라 다음 상태를 만드는 것이다.

1. 프로젝트의 현행 방향과 플레이어 약속이 명확하다.
2. 기획의 핵심 영역과 개발 게이트에 누락이 없다.
3. 시스템·콘텐츠·세계·표현·기술·제작 계획이 서로 충돌하지 않는다.
4. 기획과 실제 코드·데이터·Scene·Resource·자산·테스트가 일치한다.
5. 한 질문에는 하나의 현행 책임 원본만 존재한다.
6. 새 채팅이나 새 작업자가 과거 대화 없이 저장소만으로 작업을 이어갈 수 있다.
7. 검증된 프로젝트 교훈은 프로젝트 Skill에 반영되고, 공용화 후보만 Base로 분리된다.
8. 기획·검수 완료 뒤 Codex가 재해석 없이 구현할 수 있는 실행 계약이 존재한다.
9. 제작 목표는 승인된 전체 기획과 구성을 실제로 플레이할 수 있는 완성형 버티컬 슬라이스 데모다.
10. 주요 변경과 승인 Decision은 다음 단계로 미루지 않고 GitHub 정본·계획 데이터·연결 Sheet에 즉시 동기화된다.

### `[검수]`의 정확한 의미

`[검수]`는 위 전체 프로젝트 감사와 적대적 검토를 **기본 읽기 전용**으로 수행한다.

```yaml
review_fix_authority: READ_ONLY
```

사용자가 수정까지 요청했거나 finding을 승인한 경우에만 최소 수정하고 다시 검수한다.

### `[총기획]` 개선 권한

`TOTAL_PLANNING`의 기본값은 다음이다.

```yaml
improvement_authority: SAFE_PLANNING_FIXES
```

전체 감사에서 검증된 finding을 다음 세 종류로 나눈다.

- `AUTO_FIX_ELIGIBLE`
  - 승인된 결정의 정본·Sheet·파생본 동기화
  - 구형 경로·ID·용어와 끊어진 참조 수정
  - 중복 책임을 만들지 않는 문서 통합·명확화
  - 빠진 상태·근거·검증·실패 조건 보완
  - 실제 구현 사실을 정본에 정확히 반영
  - 사용자 방향을 바꾸지 않는 오류·누락 수정
- `USER_DECISION_REQUIRED`
  - 프로젝트 코어·대표 경험·주요 시스템·UX·서사·아트 방향
  - 기능 제거·대체, 범위·비용·일정의 중대한 교환
  - 둘 이상의 유효한 책임 원본·개선안 충돌
- `RESEARCH_OR_TEST_REQUIRED`
  - 재미·밸런스·수치·시장성·접근성·성능처럼 근거 또는 실행 검증이 필요한 항목

`SAFE_PLANNING_FIXES`는 `AUTO_FIX_ELIGIBLE`만 반영한다. 나머지는 Grill Me, Evidence, 플레이테스트 또는 별도 승인 전까지 확정하지 않는다.

### 기본 제외

별도 요청이나 승인 없이 다음을 수행하지 않는다.

- 제품 코드·Scene·데이터의 임의 구현
- 프로젝트 코어·주요 UX·서사·아트 방향 변경
- 승인 자산 삭제·교체
- 파일·폴더 대량 이동·삭제
- 미확정 제안을 확정 Decision으로 기록
- 프로젝트 고유 정보를 Base 공용 규칙에 복사
- 테스트·런타임·플레이테스트 미실행 상태를 통과로 보고
- 모든 Skill·모든 파일을 무차별 로드

---

## 2. 권한과 사실 우선순위

```text
최신 사용자 지시와 승인
→ 프로젝트 AGENTS.md·보안·엔진·데이터 규칙
→ CURRENT_CONFIRMED_DECISIONS·Active Context·Handoff
→ 승인된 프로젝트 기획서·Issue·Goal·Plan
→ 등록된 분야별 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트에 고정·동기화된 Base 기준
→ Base 최신 main의 현행 운영 정본·Skill Registry
→ 이 Prompt
→ 외부 벤치마크·과거 대화·이전 초안·AI 추론
```

규칙:

- 과거 문서를 유지하기 위해 최신 결정을 왜곡하지 않는다.
- 프로젝트의 실제 구현 사실은 설명문보다 실제 파일과 실행 증거를 우선한다.
- 외부 사례는 개선 가설이며 프로젝트 정본이 아니다.
- 이 Prompt가 최신 Base와 충돌하면 최신 Base를 적용하고 `STALE_PROMPT_CONTRACT`를 기록한다.
- 사용자안과 AI 최초안은 같은 기준으로 검토한다.
- 정상 동작 중인 사용자 변경과 승인된 강점은 임의로 되돌리지 않는다.

---

## 3. 작업환경 우선 복원

### 3.1 Base

```text
최신 main SHA
→ 동일 Goal의 열린·최근 병합 PR
→ START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/WORK_MODE_AND_SKILL_ROUTING.md
→ docs/DOCUMENTATION_MAP.md
→ docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 최소 Skill·Reference·Template·Test
```

### 3.2 프로젝트

```text
최신 main SHA·현재 Branch·working tree
→ 동일 Goal의 열린·최근 병합 PR·Issue·Plan
→ AGENTS.md·START_HERE
→ BASE_RULES_VERSION 또는 프로젝트 Base pin
→ ACTIVE_CONTEXT·HANDOFF·CURRENT_CONFIRMED_DECISIONS
→ DOCUMENTATION_MAP·DESIGN_DOCUMENT_REGISTRY
→ 분야별 기획 책임 원본
→ 실제 코드·데이터·Scene·Resource·자산·테스트
→ 프로젝트 Skill·Template·Workflow
→ 구성된 Google Sheet
→ PDF·DOCX·Dashboard·Manifest·생성본
```

`프로젝트 전체를 살펴본다`는 모든 파일 전문을 처음부터 읽는다는 뜻이 아니다.

1. 저장소 트리·Registry·Documentation Map으로 인벤토리를 만든다.
2. 각 분야의 책임 원본과 활성 소비자를 선택한다.
3. 충돌·누락·구형 참조·고아 파일이 발견될 때 범위를 확장한다.
4. 전체라고 주장할 때는 파일 인벤토리 또는 동등한 저장소 증거를 남긴다.

### 3.3 Baseline Recovery Record

```yaml
base_main_sha:
project_main_sha:
current_branch_and_head:
working_tree_state:
related_open_and_recent_prs:
project_stage:
engine_platform_and_versions:
entrypoints:
current_decisions:
canonical_sources:
actual_implementation:
skills_templates_workflows:
sheet_state:
derivative_and_publication_state:
protected_scope:
available_tools_permissions:
validation_commands:
required_checks:
rollback_path:
unverified_inputs:
```

확인하지 못한 항목은 추정하지 않고 `NOT_AVAILABLE / NOT_RUN / BLOCKED_UNVERIFIED`로 기록한다.

---

## 4. Work Mode·Skill·Superpowers

### 4.1 Work Mode

- `TOTAL_PLANNING`
  - `REVIEW → PLAN → 승인된 기획·문서 BUILD → REVIEW`
- `REVIEW`
  - `REVIEW → 승인 finding이 있을 때만 BUILD → REVIEW`
- `AUTO`
  - 전체 프로젝트의 부족·충돌 개선이 목적이면 `TOTAL_PLANNING`
  - 기존 결과 판정만 목적이면 `REVIEW`
  - 둘 다면 `TOTAL_PLANNING` 안의 최종 검수로 통합

총기획은 항상 **감사부터 시작**한다.

### 4.2 Base Skill

공통 Foundation:

- `managing-project-intake-and-work-contract`
- `running-adversarial-review-and-refinement`
- `reviewing-and-validating-project-changes`
- 필요 시 `auditing-canonical-reference-freshness`
- 종료 시 `maintaining-project-context-and-handoff`

분야 주 책임 후보:

- 프로젝트 코어 복원: `identifying-project-core`
- 프로젝트 코어 확정: `establishing-project-core`
- 핵심 컨셉·뾰족한 재미·벤치마크·플레이테스트:
  `analyzing-and-refining-game-concepts`
- 기획 책임 원본·발행: `managing-design-documents`
- 대표 경험·데모·제작 가능성: `designing-vertical-slices`
- UI·아트 실제 결과 감사: `auditing-and-refining-ui-art`
- 프로젝트 Skill 학습: `evolving-project-discipline-skills`
- Base 환류 후보: `managing-base-change-proposals`

한 단계의 주 책임 분야 Skill은 최대 하나다.

### 4.3 Superpowers

실제 환경에 제공될 때 다음을 사용한다.

```text
using-superpowers
→ 기획 개선안 설계 전 brainstorming
→ 다단계 수정 전 writing-plans
→ 계약·동작 변경 전 test-driven-development
→ 실패 원인이 불명확할 때 systematic-debugging
→ 완료 주장 전 verification-before-completion
→ 주요 결과·PR 완료 전 requesting-code-review
```

외부 Skill을 Base Registry에 중복 생성하지 않는다.

---

## 5. 이전 총기획 계약 보존 Gate

`previous_total_planning_instruction`이 제공되면 파일명·경로·버전·해시 또는 대화 첨부 식별자를 기록하고 실제 원문과 현재 Prompt를 비교한다. 제공되지 않았지만 저장소·Library·현재 대화에서 이전 지시문을 찾을 수 있으면 먼저 복원한다. 찾지 못하면 비교 완료를 주장하지 않고 `BLOCKED_UNVERIFIED`로 둔다.

현재 Prompt가 이전 버전보다 짧거나 새롭다는 이유로 기능을 약화할 수 없다.

### 보존해야 하는 이전 계약

| 이전 계약의 강점 | v3 필수 보존 방식 |
|---|---|
| 문서·PDF·Skill·Template·규칙·파일 구조 전체 검수 | 프로젝트 인벤토리와 분야별 감사 Surface |
| 개발 게이트 검수 | Ready·Implementation·Verification·Documentation·Completion Gate |
| 누락·충돌·중복·모호성 제거 | 기획 결함 분류와 Finding Ledger |
| 한 질문에 하나의 책임 원본 | Responsibility Source Map |
| 파일 통합·보류·제거 후보 분류 | File Treatment Matrix |
| PDF와 원본·승인 이미지 일치 | PDF_AND_DERIVATIVE_AUDIT |
| 공용 지식과 프로젝트 지식 분리 | Base Boundary Audit |
| 새 채팅 저장소 단독 재개 | COLD_START_VALIDATION |
| 분야별 Skill의 입력·산출물·검증 경계 | SKILL_AND_WORKFLOW_AUDIT |
| 성공·실패·예외의 학습·환류 | PROJECT_LEARNING_AND_BASE_FEEDBACK |
| 미실행 검증 표시 | Evidence status와 fail-closed 완료 Gate |

### 보존 판정

```yaml
previous_contract_item:
preserved_in_current_prompt:
preserved_in_project:
evidence:
regression:
decision: PRESERVED | IMPROVED | MISSING | INTENTIONALLY_REPLACED
replacement_reason:
validation:
```

`MISSING`이 하나라도 있고 의도적 대체 근거가 없으면 Prompt 개선 완료가 아니다.

---

## 6. 총기획 전체 생명주기

다음 순서를 바꾸지 않는다.

```text
WHOLE_PROJECT_BASELINE_RECOVERY
→ STRENGTH_PRESERVATION_MAP
→ PROJECT_INVENTORY_AND_COVERAGE_AUDIT
→ PLANNING_GAP_AND_CONFLICT_DISCOVERY
→ ADVERSARIAL_ATTACK
→ VALIDATE_CRITIQUE
→ IMPROVEMENT_OPTION_DESIGN
→ GRILL_ME_ONLY_FOR_DECISION_GAPS
→ APPROVED_IMPROVEMENT_BUILD
→ CANONICAL_AND_CONSUMER_UPDATE
→ COLD_START_VALIDATION
→ REGRESSION_RECHECK
→ PR_CHECK_EXACT_HEAD
→ DECISION_REPORT
→ PLANNING_AND_REVIEW_COMPLETE_GATE
→ IMMEDIATE_CANONICAL_DECISION_SYNC
→ CODEX_IMPLEMENTATION_HANDOFF
→ COMPLETE_VERTICAL_SLICE_TARGET
→ VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md
```

### 단계 원칙

- 기존 강점과 정상 경로를 먼저 고정한다.
- 결함을 찾기 전에 새 기획을 발명하지 않는다.
- 비판은 사실성과 영향을 다시 검증한다.
- 사용자의 핵심 결정만 질문한다.
- 승인된 finding만 해당 분야 주 책임 Skill로 수정한다.
- 수정 뒤 전체 연결과 기존 정상 경로를 다시 검사한다.
- 정확한 현재 HEAD의 증거만 완료 판정에 사용한다.
- 주요 변경·승인은 발견 시점에 즉시 동기화하며 최종 보고까지 배치 처리하지 않는다.
- 기획·검수 완료 Gate가 닫히기 전 Codex 구현 작업을 시작하지 않는다.
- Codex 구현은 완성형 버티컬 슬라이스 데모의 수용 기준을 닫는 방향으로 라우팅한다.

---

## 7. 프로젝트 전체 인벤토리

다음 Surface를 `PRESENT / MISSING / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 판정한다.

### 7.1 진입·운영

- `AGENTS.md`
- `START_HERE.md`
- `README.md`
- Base pin·버전·동기화 기록
- Documentation Map
- Active Context·Handoff
- Roadmap·Issue·Goal·Plan
- 현재 작업·금지 범위·다음 Gate

### 7.2 결정·기획

- CURRENT_CONFIRMED_DECISIONS
- 프로젝트 방향·코어·플레이어 약속
- 제품·경험
- 시스템·콘텐츠·밸런스
- 세계·서사
- UX·UI·접근성
- 아트·애니메이션·오디오
- 데이터·저장·호환성
- 기술·플랫폼·성능
- QA·플레이테스트
- 제작·출시·운영·사업

### 7.3 실제 구현

- 코드
- 데이터·Schema
- Scene·Resource
- 자산·Import 설정
- 테스트·Fixture
- Build·배포 구성
- 런타임·캡처·로그
- 저장·마이그레이션

### 7.4 작업 구조

- 프로젝트 Skill
- 공용 Skill Adapter
- Reference·Template
- 자동화·Workflow
- 생성기·발행 설정
- 외부 AI 작업·검수 경계
- Codex 구현 인계 Packet·실행 책임
- 버티컬 슬라이스 완성도 Matrix·데모 Gate
- 학습·회고·Base 환류

### 7.5 사용자 작업면·파생본

- Google Sheet
- PDF·DOCX
- Dashboard
- Figma·시각 Artifact
- Manifest·해시
- 승인 이미지·캡션·원출처
- 배포용 문서

### 프로젝트 인벤토리 표

| Surface | 경로·ID | 역할 | 권한 | 현재 상태 | 관련 정본 | 소비자 | 검증 |
|---|---|---|---|---|---|---|---|

---

## 8. 보존할 강점 지도

수정 전에 프로젝트의 강점과 보호 대상을 기록한다.

```yaml
strength_id:
strength:
player_or_user_value:
evidence:
canonical_source:
actual_implementation:
dependent_systems_and_content:
protected_behavior:
allowed_change_boundary:
regression_test_or_review:
```

필수 보호 대상:

- 프로젝트 코어와 비타협 조건
- 이미 검증된 재미·사용자 흐름
- 승인된 세계관·인물·용어
- 승인된 이미지·UI·아트 방향
- 정상 저장·호환성·공개 인터페이스
- 실제 사용 중인 제작 파이프라인
- 사용자 고유 변경
- 기존 테스트가 보호하는 정상 경로

개선이 장점을 약화하면 `REGRESSION`이다.

---

## 9. 책임 원본 지도

각 중요 질문에 대해 현행 책임 원본을 하나만 지정한다.

### RESPONSIBILITY_SOURCE_MAP

| 질문·책임 | 현행 책임 원본 | 보조 자료 | 실제 구현 | 소비자 | 상태 |
|---|---|---|---|---|---|
| 프로젝트 방향 |  |  |  |  |  |
| 현재 구현 상태 |  |  |  |  |  |
| 핵심 플레이 규칙 |  |  |  |  |  |
| UX·아트 기준 |  |  |  |  |  |
| 데이터·저장 계약 |  |  |  |  |  |
| 검증 방법 |  |  |  |  |  |
| 다음 작업·금지 범위 |  |  |  |  |  |

판정:

- `SINGLE_CURRENT_OWNER`
- `DUPLICATE_ACTIVE_SOURCE`
- `MISSING_CANON`
- `STALE_OWNER`
- `IMPLEMENTATION_ONLY_UNDOCUMENTED`
- `BLOCKED_UNVERIFIED`

---

## 10. 프로젝트 건강도 Matrix

### PROJECT_HEALTH_MATRIX

| 영역 | 정본 완전성 | 기획 품질 | 구현 일치 | 검증 | 주요 위험 | 상태 |
|---|---|---|---|---|---|---|
| 진입·운영 |  |  |  |  |  |  |
| 제품·경험 |  |  |  |  |  |  |
| 시스템·콘텐츠 |  |  |  |  |  |  |
| 세계·서사 |  |  |  |  |  |  |
| UX·표현 |  |  |  |  |  |  |
| 데이터·기술 |  |  |  |  |  |  |
| 제작·검증 |  |  |  |  |  |  |
| Skill·Workflow |  |  |  |  |  |  |
| Sheet·파생본 |  |  |  |  |  |  |
| 콜드 스타트 |  |  |  |  |  |  |

상태:

`HEALTHY / NEEDS_IMPROVEMENT / CONFLICTED / MISSING / BLOCKED_UNVERIFIED / NOT_APPLICABLE`

점수만으로 완료를 판정하지 않는다. 결함·증거·수정·검증을 함께 기록한다.

---

## 11. 개발 Gate 감사

### DEFINITION_OF_READY

구현 전에 다음이 명확해야 한다.

- 해결 문제와 목적
- 플레이어·사용자 가치
- 범위와 제외 범위
- 선행 조건과 의존성
- 영향 정본과 실제 파일
- 데이터·저장·호환성 위험
- 관찰 가능한 완료 기준
- 자동·수동·사용자 검수
- 적용할 공용·프로젝트 Skill
- 롤백

### IMPLEMENTATION_GATE

- 승인되지 않은 방향 확장 금지
- 기능 추가와 대규모 리팩터링 분리
- 기존 기능·저장·인터페이스·사용자 흐름 보호
- `[보류]` 항목의 무단 구현 금지
- 가장 작은 검증 가능한 변경
- 정본·Schema·경로 변경 시 소비자 동시 추적

### VERIFICATION_GATE

- 문법·포맷·타입·정적 검사
- 관련 자동 테스트
- 핵심 정상 경로
- 실패·예외·경계
- 저장·불러오기·호환성
- 실제 diff
- 적용 시 접근성·성능
- 사용자 수동 검수
- 미실행 항목의 명시

### DOCUMENTATION_GATE

방향·수치·기능·용어·구현·작업 방식이 바뀌면 확인한다.

- 기획 책임 원본
- CURRENT_CONFIRMED_DECISIONS
- Roadmap·Issue·Plan
- Documentation Map
- Active Context·Handoff
- 관련 Skill·Template
- 테스트 문서
- README·START_HERE
- Base pin·동기화 기록
- Sheet·PDF·Manifest

### COMPLETION_GATE

다음 작업자가 저장소만으로 찾을 수 있어야 한다.

- 프로젝트 핵심 방향
- 현재 구현 상태
- 이번 개선 결과
- 다음 작업
- 금지·제외·보류
- 분야 책임 원본
- 관련 Skill
- 검증 방법
- 남은 위험·미확정

---

## 12. 기획 Coverage 감사

필요한 항목을 `CONFIRMED / NEEDS_IMPROVEMENT / NOT_APPLICABLE / BLOCKED_UNVERIFIED`로 판정한다.

### `00 프로젝트 기반`

- 저장소·엔진·플랫폼·Stage
- 핵심 방향·현재 Decision
- 책임 원본·실제 구현
- 열린 PR·Issue·Plan
- 보호 대상
- Sheet·발행 상태
- 현재 위험·다음 Gate

### `10 제품·경험`

- 타깃 플레이어·플레이 상황
- 플레이어 약속·제품 방향
- 핵심 컨셉·뾰족한 재미
- Core·Session·Meta Loop
- 조작·선택·승패·복구
- 온보딩·난이도·보상
- 게임 필·피드백·가독성
- 접근성 기본 방향
- 시장·스토어 약속과 실제 경험

### `20 시스템·콘텐츠`

- 시스템 관계도
- 핵심 규칙·상태·입력·출력
- 성장·경제·강화·자원
- 콘텐츠·레벨·미션
- 적·AI·난이도
- 아이템·장비·스킬·캐릭터
- 수치·공식·단위·시험값
- 악용·무한 루프·소프트락
- 실패·복구·저장
- 데모·Vertical Slice·본제작 범위

### `30 세계·서사`

해당 프로젝트에 필요한 범위만 적용한다.

- 세계 규칙·금기·장소·세력
- 주요인물·조연·관계
- 플레이어 역할·동기
- 사건·정보 공개·콘텐츠 흐름
- 시스템과 서사의 연결
- 반복 콘텐츠의 정당화
- 톤·문체·용어·명명
- 모순·연속성·스포일러

### `40 표현·UX`

- 사용자 흐름·화면 구조
- HUD·메뉴·상태 전달
- 입력·포커스·취소·확인·오류 복구
- 아트·카메라·이펙트·애니메이션
- 사운드·음악·정보 전달
- 접근성 대체 채널
- 승인 이미지·레퍼런스·라이선스
- 기획 이미지와 실제 엔진 화면 구분

### `50 제작·기술·검증`

- 기술 구조·책임 경계
- 데이터·ID·Schema·저장·마이그레이션
- 엔진·플러그인·서비스·라이선스
- 제작 파이프라인·반복 제작성
- 마일스톤·의존성·Approval Bundle
- Vertical Slice 목표 품질
- 테스트·QA·회귀·플레이테스트
- 접근성·성능 예산
- 텔레메트리·피드백
- 배포·출시·운영·사업
- 위험·대안·중단 조건·롤백
- Codex·개발팀 인계
- 완성형 버티컬 슬라이스의 시스템·콘텐츠·표현·데이터·검증 완결성
- 데모 Build·패키징·실행·배포 준비

### `99 변경·학습`

- Decision 추가·대체·기각·보류
- Evidence와 변경 이유
- 반영 Commit
- 실패·회귀·복구
- 프로젝트 Skill 학습
- Base 환류 후보
- 재검토 조건

---

## 13. 기획 결함 분류

### 필수 Finding 유형

- `PLANNING_GAP`
  - 필요한 기획 질문·규칙·상태·완료 기준이 없음
- `PLANNING_CONFLICT`
  - 두 기획 원칙·시스템·문서가 양립할 수 없음
- `CANON_IMPLEMENTATION_GAP`
  - 정본과 실제 구현이 다름
- `UNDERDESIGN`
  - 실패·복구·예외·수치·의존성·검증이 부족함
- `OVERDESIGN`
  - 플레이어 가치나 현재 Stage보다 범위·복잡성이 과도함
- `UNPROVEN_ASSUMPTION`
  - 근거·테스트 없이 핵심 전제로 사용됨
- `PLAYER_EXPERIENCE_RISK`
  - 코어 경험·가독성·학습·피로·보상이 훼손될 위험
- `PRODUCTION_RISK`
  - 팀·도구·일정·콘텐츠량·파이프라인이 감당하기 어려움
- `ACCESSIBILITY_RISK`
- `PERFORMANCE_RISK`
- `DATA_COMPATIBILITY_RISK`
- `MISSING_CANON`
- `MISSING_CONSUMER`
- `MISSING_SYNC`
- `DUPLICATE_ACTIVE_SOURCE`
- `STALE_REFERENCE`
- `ORPHANED_REFERENCE`
- `DERIVATIVE_STALE`
- `DUPLICATE_WORK`
- `DUPLICATE_QUESTION`
- `ALLOWED_LEGACY`
- `BLOCKED_UNVERIFIED`

### 결함 Ledger

| ID | 유형 | 위치 | 증거 | 보호 강점 | 플레이어·프로젝트 영향 | 심각도 | 수정 후보 | 검증 |
|---|---|---|---|---|---|---|---|---|

---

## 14. 분야 간 충돌 감사

반드시 대조한다.

- 플레이어 약속 ↔ Core Loop
- Core Loop ↔ 보상·성장·경제
- 시스템 복잡도 ↔ 온보딩·가독성
- 콘텐츠 구조 ↔ 제작량·반복성
- 세계·서사 ↔ 플레이 규칙
- 캐릭터·세력 ↔ 시스템 기능
- UX·UI ↔ 상태·입력·오류 복구
- 아트·사운드 ↔ 정보 전달·게임 필
- 접근성 ↔ 핵심 정보·입력·시간 제한
- 저장·데이터 ↔ 성장·업데이트·마이그레이션
- Vertical Slice ↔ 대표 경험·파이프라인
- 출시 약속 ↔ 실제 범위·품질·운영 능력
- 프로젝트 기획 ↔ 실제 구현·테스트
- GitHub 정본 ↔ Sheet·PDF·Dashboard

판정:

- `MUST_RESOLVE`
- `USER_DECISION_REQUIRED`
- `TEST_IN_VERTICAL_SLICE`
- `DEFERRED_WITH_BOUNDARY`
- `NO_CONFLICT`
- `BLOCKED_UNVERIFIED`

---

## 15. 벤치마크·플레이어·현업 Evidence

조사 전에 “어떤 결정을 바꿀 수 있는가”를 고정한다.

출처 우선순위:

1. 공식 제품·엔진·플랫폼 문서와 실제 제품
2. 개발자 발표·사후 분석·기술 자료
3. 플레이테스트·텔레메트리·퍼널
4. 플레이어 리뷰·인터뷰·커뮤니티
5. 전문 종합 자료
6. AI 추론

규칙:

- 성공·실패·혼합 사례를 함께 조사한다.
- 제품 사실·행동·자기보고·해석을 분리한다.
- 패치·플랫폼·표본·플레이타임 차이를 기록한다.
- 인기 기능을 표면 복사하지 않는다.
- 프로젝트 코어·팀 규모·플랫폼 차이를 검토한다.
- `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 판정한다.

| Evidence ID | 결정 질문 | 사실·반응 | 반증·한계 | 프로젝트 차이 | 판정 | 후속 검증 |
|---|---|---|---|---|---|---|

---

## 16. 적대적 검토 루프

### 16.1 Attack

다음 실패 가정을 적극적으로 공격한다.

- 핵심 내용이 문서 정리 과정에서 왜곡됨
- 프로젝트의 강점보다 벤치마크를 우선함
- 기획이 많지만 플레이어 경험과 연결되지 않음
- 분야별 문서는 완성됐지만 서로 충돌함
- 정본과 실제 구현이 다름
- 구현되지 않은 기능이 완료로 표시됨
- 성공 사례만 조사함
- 플레이어 행동과 자기보고를 혼동함
- 시험값을 확정 수치로 사용함
- 사용자 선택이 필요한 내용을 AI가 확정함
- 문서·Skill·Template 책임이 중복됨
- 새 정본의 소비자가 untouched임
- PDF·Sheet·Dashboard가 원본보다 오래됨
- 구형 경로·ID·용어가 활성 참조에 남음
- 범위가 팀·일정·제작 파이프라인보다 큼
- 접근성·성능·저장·라이선스가 누락됨
- 테스트하지 않은 결과를 완료로 주장함

### 16.2 Validate Critique

각 공격을 다시 검증한다.

```yaml
finding:
factual_basis:
current_source_and_actual_implementation:
counterevidence:
probability:
impact:
scope:
fix_cost:
strengths_at_risk:
verdict:
```

판정:

- `MUST_FIX`
- `SHOULD_FIX`
- `USER_DECISION_REQUIRED`
- `DEFER`
- `REJECTED_CRITIQUE`
- `BLOCKED_UNVERIFIED`
- `ALLOWED_LEGACY`

반대를 위한 반대, 취향, 중복 제안, 범위 밖 비판은 `REJECTED_CRITIQUE`다.

### 16.3 Regression Recheck

수정 후 다시 검사한다.

- `[핵심 내용]`
- 보존 강점과 정상 경로
- 프로젝트 코어·플레이어 약속
- 분야 간 연결
- 실제 구현·저장·호환성
- UX·접근성·성능
- 정본·소비자·구형 참조
- PDF·Sheet·파생본
- 콜드 스타트
- 테스트·런타임·플레이테스트 증거
- 롤백

---

## 17. 개선안 설계

먼저 finding을 `AUTO_FIX_ELIGIBLE / USER_DECISION_REQUIRED / RESEARCH_OR_TEST_REQUIRED`로 분류한다.

- `AUTO_FIX_ELIGIBLE`: 보호 강점과 사용자 방향을 바꾸지 않는 검증된 오류·누락
- `USER_DECISION_REQUIRED`: 프로젝트 방향을 바꾸는 선택
- `RESEARCH_OR_TEST_REQUIRED`: 추가 근거·실행 증거 없이는 결론을 낼 수 없는 가설

유효한 finding마다 최소 변경안을 포함해 2~3개 대안을 비교한다.

```yaml
finding_id:
current_problem:
protected_strengths:
option_minimal:
option_balanced:
option_structural:
player_value:
planning_coherence:
production_cost:
technical_and_data_risk:
operational_burden:
compatibility:
reversibility:
evidence:
counterevidence:
recommended_option:
validation:
```

### IMPROVEMENT_BACKLOG

| 우선순위 | Finding | 개선 결과 | 선행 조건 | 승인 | 정본 | 소비자 | 구현 | 검증 | 상태 |
|---|---|---|---|---|---|---|---|---|---|

우선순위:

1. 프로젝트 코어·플레이어 경험을 막는 충돌
2. 데이터 손상·호환성·보안·권리 위험
3. 실제 구현과 정본 불일치
4. 필수 기획·개발 Gate 누락
5. 제작 불가능한 범위·파이프라인
6. UX·접근성·성능 위험
7. 문서·Skill·파생본 구조 개선
8. 선택적 품질 향상

---

## 18. Grill Me

Grill Me는 전체 감사 후 **검증된 핵심 결정 공백**에만 사용한다.

사용 조건:

- 프로젝트 코어·플레이어 판타지·뾰족한 재미
- 충돌하는 시스템·UX·콘텐츠 원칙
- MVP·데모·본제작 범위
- 주요 실패·복구·보상 의미
- 기존 승인 정본의 대체
- 둘 이상의 개선안이 프로젝트 방향을 다르게 만듦

질문 전 확인:

```text
main HEAD
→ 동일 Goal Issue·PR·Branch
→ 최근 병합·대체 관계
→ CURRENT_CONFIRMED_DECISIONS
→ 책임 원본
→ 실제 구현
→ Sheet
→ Finding·Evidence
→ 질문 필요성
```

금지:

- 저장소에서 확인할 수 있는 사실 질문
- 이미 승인된 동일 결정 재질문
- 기술 세부·시험값 질문
- 한 번에 여러 독립 결정 질문
- 감사 전에 막연한 선호 인터뷰
- 이전 승인 미동기화 상태에서 다음 질문

표준 형식:

```md
## Grill Me — <Decision ID>

### 확인된 기획 공백·충돌
### 기존 정본과 실제 구현
### 보호할 강점
### 질문
### 선택지별 장점·단점·영향
### Evidence와 반증
### GPT 권장안
### 확정 시 갱신할 정본·소비자·검증
### 답변: A / B / 직접 수정안 / 권장안대로
```

사용자가 `모두 권장안대로`라고 하면 동등 유형 결정을 반복 질문하지 않는다.

답변 후:

```text
Decision 기록
→ CURRENT_CONFIRMED_DECISIONS
→ 분야 정본·Approval Bundle
→ Issue·Plan·Active Context
→ 구성된 Sheet
→ Commit·PR
→ 재조회
→ SYNCED 판정
```

사용자 승인 전 GPT 제안은 확정 Decision이 아니다.

---

## 19. 승인된 개선 반영

`AUTO_FIX_ELIGIBLE`인 검증된 `MUST_FIX`·`SHOULD_FIX`, 사용자 승인 finding, 사용자 확정 Decision만 반영한다.

`RESEARCH_OR_TEST_REQUIRED`는 조사·플레이테스트·런타임 검증 없이 문서상 확정으로 승격하지 않는다.

### Approval Bundle

```yaml
bundle_id:
goal:
findings:
protected_strengths:
current_decisions:
approved_improvements:
evidence_ids:
scope:
out_of_scope:
dependencies:
affected_canonical_sources:
affected_consumers:
actual_implementation_impact:
sheet_and_derivative_impact:
acceptance_criteria:
validation:
rollback:
```

### 반영 규칙

- 가장 작은 검증 가능한 변경을 우선한다.
- 기능 추가와 구조 리팩터링을 분리한다.
- 한 질문에 활성 정본 하나만 유지한다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 초기 수치는 `RECOMMENDED_DEFAULT` 또는 `TEST_VALUE`로 표시한다.
- 경로·ID·Schema 변경은 모든 활성 소비자를 추적한다.
- 승인되지 않은 주요 방향·자산을 변경하지 않는다.
- 제품 구현은 명시된 `implementation_authority` 범위만 수행한다.

---

## 20. 주요 변경·승인 Decision 즉시 동기화

### IMMEDIATE_CANONICAL_DECISION_SYNC

다음 사건이 발생하면 최종 단계까지 미루지 않고 같은 작업 흐름 안에서 즉시 동기화한다.

- 사용자가 주요 기획안·권장안·변경안을 승인함
- Decision이 `PROPOSED`에서 `APPROVED / REPLACED / REJECTED / DEFERRED`로 바뀜
- 프로젝트 코어·기능 범위·완료 기준·버티컬 슬라이스 범위가 바뀜
- 기획과 실제 구현의 충돌을 해결함
- Codex 인계 계약이나 구현 순서가 바뀜
- 정본·계획·Sheet 중 하나의 내용이 다른 Surface보다 앞서감

### NO_DEFERRED_DECISION_SYNC

```text
승인·주요 변경 감지
→ 동일 Decision ID 생성 또는 기존 ID 재사용
→ GitHub 권위 문서·계획 데이터 위치 탐색
→ 연결된 Google Sheet의 Tab·Range·행 탐색
→ GitHub 정본·Decision Registry·GDD·Plan 갱신
→ Commit
→ commit SHA와 변경 경로·섹션·행 기록
→ 연결된 Google Sheet에 동일 Decision ID·상태·요약·GitHub 위치·commit SHA 반영
→ GitHub와 Sheet 재조회
→ SAME_DECISION_ID·내용·상태·Commit 일치 검증
→ DECISION_SYNC_LEDGER 기록
→ SYNCED 판정
```

GitHub가 권위 원본이며 Google Sheet는 연결된 계획·운영 Surface다. Sheet 내용이 GitHub 정본을 임의로 덮어쓰지 않는다.

### 동일 Decision 기록 계약

```yaml
SAME_DECISION_ID:
decision_status:
decision_summary:
rationale_and_evidence:
approval_source_and_time:
affected_scope:
GITHUB_CANONICAL_LOCATION:
  repository:
  file_path:
  section_or_line:
  plan_or_issue:
  commit_SHA:
GOOGLE_SHEET_LOCATION:
  spreadsheet:
  tab:
  range_or_row:
  github_commit_reference:
readback_result:
sync_status:
```

### DECISION_SYNC_LEDGER

| Decision ID | 상태 | GitHub 권위 문서·계획 데이터 | 변경 경로·섹션·행 | commit SHA | 연결된 Google Sheet 위치 | 재조회 | 동기화 상태 |
|---|---|---|---|---|---|---|---|

동기화 상태:

- `SYNCED`: 동일 Decision ID·의미·상태·GitHub 위치·commit SHA가 재조회 결과 일치
- `PARTIAL_SYNC_BLOCKED`: GitHub 또는 Sheet 중 하나를 읽거나 쓸 수 없음
- `SYNC_CONFLICT`: 같은 Decision ID의 내용·상태가 다름
- `NOT_APPLICABLE`: 프로젝트에 연결된 Sheet가 없다는 사실이 확인되고 정본에 기록됨

`PARTIAL_SYNC_BLOCKED` 또는 `SYNC_CONFLICT` 상태에서는 동기화 완료를 주장하지 않으며, 사용자 승인으로 명시적 보류 처리하지 않는 한 **다음 주요 기획·구현 단계로 진행하지 않는다**.

---

## 21. 기획·검수 완료와 Codex 구현 인계

### PLANNING_AND_REVIEW_COMPLETE_GATE

다음이 모두 닫혀야 Codex 구현 인계를 생성한다.

- `[핵심 내용]` 추적 항목이 허용 상태로 닫힘
- 프로젝트 코어·전체 기획 Coverage·버티컬 슬라이스 범위 확정
- `MUST_FIX` 0 또는 승인된 보류·재개 조건 존재
- 필요한 Grill Me Decision 완료
- GitHub 권위 문서·계획 데이터·연결 Sheet가 최신 Decision ID로 `SYNCED`
- 실제 구현 기준선과 보호할 정상 경로 기록
- 구현 범위·제외 범위·의존성·수용 기준·검증·롤백 확정
- v9 버티컬 슬라이스 구현 Prompt와 충돌 없는 책임 경계 확인

하나라도 닫히지 않으면 `CODEX_NOT_READY`다.

### CODEX_DEFINITION_OF_READY

Codex는 기획을 다시 설계하거나 빈칸을 추측하는 역할이 아니다. 다음 항목을 저장소 사실과 함께 전달한다.

```yaml
implementation_goal:
player_observable_result:
approved_decision_ids:
canonical_baseline_commit:
working_branch_and_head:
vertical_slice_scope:
exact_in_scope_features_and_content:
explicit_out_of_scope:
protected_behaviors_assets_and_interfaces:
existing_implementation_state:
exact_files_scenes_resources_data_and_schema:
interfaces_and_dependencies:
implementation_sequence:
save_migration_and_compatibility:
accessibility_and_performance_constraints:
automated_test_commands_and_expected_results:
manual_engine_and_demo_checks:
document_and_sheet_sync_targets:
commit_and_pr_strategy:
rollback:
ambiguities_or_blockers:
```

### CODEX_EXECUTION_PACKET

Codex에 전달하는 구현 계약은 다음을 포함한다.

1. **왜 만드는가** — 플레이어 약속·기획 의도·완성 데모의 관찰 가능한 결과
2. **무엇을 구현하는가** — 기능·시스템·콘텐츠·UI·자산·데이터의 정확한 범위
3. **어디를 수정하는가** — 실제 경로·Scene·Resource·Schema·ID·소비자
4. **어떤 순서로 구현하는가** — 의존성에 따른 Goal·Task·Checkpoint
5. **무엇을 보존하는가** — 정상 경로·저장 호환성·승인 자산·공개 인터페이스
6. **어떻게 검증하는가** — 테스트 명령·기대 결과·수동 실행·데모 시나리오
7. **어떻게 기록하는가** — Decision ID·Commit·PR·정본·Sheet 갱신 위치
8. **어떻게 되돌리는가** — 롤백 단위와 복구 기준

금지:

- “적절히 구현”, “알아서 완성”, “기획서를 참고” 같은 비검증 지시
- 존재하지 않는 파일·API·Scene·Resource 추정
- 사용자 승인 없이 기능 삭제·축소·대체
- 테스트 명령·관찰 결과 없는 완료 기준
- Codex 보고만 신뢰하고 실제 diff·실행·정본 동기화를 생략

불명확한 핵심 계약이 발견되면 Codex는 임의 보완하지 않고 `BLOCKED_IMPLEMENTATION_CONTRACT`로 보고한다.

실제 제품 구현은 `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`로 라우팅하되, 이 Packet의 Decision ID·범위·수용 기준을 입력 계약으로 사용한다.

---

## 22. 완성형 버티컬 슬라이스 데모 목표

### COMPLETE_VERTICAL_SLICE_TARGET

게임 제작의 목표는 아이디어 확인용·일회성 프로토타입이 아니라 **승인된 전체 기획과 구성을 실제로 플레이할 수 있는 완성형 데모**다.

버티컬 슬라이스 범위 안의 모든 승인 기획은 다음 중 하나여야 한다.

```text
IMPLEMENTED_AND_VALIDATED
또는
EXPLICITLY_EXCLUDED_WITH_DECISION_ID
```

이 조건을 `ALL_APPROVED_PLANNING_IMPLEMENTED_OR_EXPLICITLY_EXCLUDED`로 관리한다.

“전체 기획 구현”은 출시판의 모든 콘텐츠 수량을 미리 만드는 뜻이 아니다. 대신 최종 게임 경험에 필요한 승인된 시스템 종류·상호작용·표현·데이터·제작 파이프라인을 대표 콘텐츠와 함께 실제 품질로 완결한다. 버티컬 슬라이스 범위 안에는 `NO_PAPER_ONLY_FEATURES`, 즉 문서에만 존재하는 승인 기능을 남기지 않는다.

### VERTICAL_SLICE_COMPLETENESS_MATRIX

| Surface | 승인 기획·Decision ID | 구현 위치 | 대표 콘텐츠 | 자동 검증 | 수동 데모 검증 | 상태 |
|---|---|---|---|---|---|---|
| 핵심 플레이·Core Loop |  |  |  |  |  |  |
| Session·Meta Loop |  |  |  |  |  |  |
| 주요 시스템·상호작용 |  |  |  |  |  |  |
| 대표 콘텐츠·난이도 |  |  |  |  |  |  |
| 온보딩·조작·UX·UI |  |  |  |  |  |  |
| 실패·복구·보상 |  |  |  |  |  |  |
| 아트·애니메이션·이펙트 |  |  |  |  |  |  |
| 사운드·음악·정보 전달 |  |  |  |  |  |  |
| 데이터·저장·불러오기·마이그레이션 |  |  |  |  |  |  |
| 접근성·가독성 |  |  |  |  |  |  |
| 성능·안정성 |  |  |  |  |  |  |
| Build·패키징·실행 |  |  |  |  |  |  |
| QA·회귀·데모 시나리오 |  |  |  |  |  |  |
| 정본·Sheet·Handoff |  |  |  |  |  |  |

상태:

- `IMPLEMENTED_AND_VALIDATED`
- `IMPLEMENTED_TEST_PENDING`
- `PARTIAL`
- `MISSING`
- `EXPLICITLY_EXCLUDED_WITH_DECISION_ID`
- `BLOCKED_UNVERIFIED`

### DEMO_READY_GATE

다음을 모두 만족해야 완성형 버티컬 슬라이스 데모로 판정한다.

- 승인된 전체 기획과 Matrix 항목이 구현되거나 Decision ID로 명시적 제외됨
- 프로젝트 시작부터 핵심 목표·결과까지 한 세션을 끝까지 플레이 가능
- 핵심 경로에 진행을 막는 미구현·가짜 버튼·임시 데이터·수동 조작 의존이 없음
- 대표 콘텐츠가 시스템의 재미·난이도·반복 가능성을 검증할 수 있음
- 온보딩·조작·상태 전달·실패·복구가 실제 동작함
- 저장·불러오기·데이터 호환성 또는 명시적 비적용 근거가 있음
- 승인된 UI·아트·사운드가 정보 전달과 게임 필을 지원함
- 접근성·성능·안정성 기준을 실행 증거로 확인함
- 자동 테스트와 수동 플레이테스트의 실제 결과가 있음
- 깨끗한 환경에서 Build·패키징·설치·실행·종료가 가능함
- GDD·Decision·Codex Packet·실제 구현·GitHub Commit·연결 Sheet가 일치함
- 알려진 제한·보류·롤백과 이후 제작 확장 경로가 기록됨

Matrix에 `MISSING / PARTIAL / BLOCKED_UNVERIFIED`가 남으면 `DEMO_NOT_READY`다. 문서·스크린샷·테스트 일부 통과만으로 데모 완료를 주장하지 않는다.

---

## 23. 파일 처리 Matrix

모든 관련 파일을 다음으로 분류한다.

```text
KEEP / INTEGRATE / REVISE / CREATE / HOLD / REMOVE_CANDIDATE
```

| 파일 | 현재 역할 | 발견 문제 | 처리 | 통합 대상·새 경로 | 참조 영향 | 상태 |
|---|---|---|---|---|---|---|

### 분류 원칙

- `KEEP`: 현행 책임과 내용이 유효함
- `INTEGRATE`: 다른 현행 책임 원본으로 흡수해야 함
- `REVISE`: 현행 역할은 맞지만 내용·경로·상태를 수정해야 함
- `CREATE`: 필요한 책임 원본·Gate·Skill이 실제로 없음
- `HOLD`: 현재 범위 밖이며 재개 조건이 있음
- `REMOVE_CANDIDATE`: 중복·고아·폐기·구조 불일치 후보

삭제 전 확인:

- README·START_HERE
- Documentation Map·Registry
- 다른 문서 링크
- 코드 주석·데이터
- Issue·PR
- Skill·Template
- Test·Workflow·자동화
- 외부 링크·Sheet·파생본

위험하면 삭제하지 않고 `REMOVE_CANDIDATE`로 보고한다. 단순 이전 버전은 Git 이력으로 보존하며 불필요한 백업 파일을 만들지 않는다.

---

## 24. PDF·파생본 감사

### PDF_AND_DERIVATIVE_AUDIT

다음을 확인한다.

- 최신 승인 결정과 전체 과정 포함
- 승인 이미지·캡션·원출처
- 이전 시안 혼입 여부
- 원본 Markdown·정본과 일치
- 해당 분야 흐름의 가독성
- 역할: 책임 원본인지 배포용 파생본인지
- 생성 기준 Commit·Manifest·해시
- PDF만 최신이고 원본이 오래된 역전 상태
- DOCX·Dashboard·Sheet·Figma와 Decision ID 연결
- 파생본 재생성 또는 보류 조건

상태:

`CURRENT / STALE / MISMATCHED / NOT_GENERATED / NOT_APPLICABLE / BLOCKED_UNVERIFIED`

이미지·PDF 존재를 실제 구현·접근성·런타임 검증으로 오인하지 않는다.

---

## 25. Skill·작업 흐름 감사

### SKILL_AND_WORKFLOW_AUDIT

각 분야에 대해 확인한다.

| 분야 | 책임 문서 | 주 Skill | Trigger | 비사용 조건 | 입력 | 산출물 | Gate | 검증 | 실제 파일 |
|---|---|---|---|---|---|---|---|---|---|

Skill 최소 계약:

- 이름·목적
- 사용 조건·비사용 조건
- 필수 입력
- 먼저 읽을 책임 원본
- 작업 절차
- 산출물
- 완료 기준
- 검증 방법
- 실패 조건
- 관련 Skill
- 프로젝트 전용 규칙
- 학습·갱신 조건

공용 책임은 Base Foundation 또는 프로젝트 Adapter로 라우팅한다. 프로젝트 세계관·수치·기능명·실제 경로·승인 자산은 프로젝트에 유지한다.

새 Skill은 기존 책임에 흡수할 수 없고, 반복 가능한 독립 계약이 필요할 때만 제안한다.

---

## 26. 콜드 스타트 검증

### COLD_START_VALIDATION

새 AI가 과거 대화 없이 저장소만 읽는다고 가정한다.

다음 질문에 답할 수 있어야 한다.

1. 이 프로젝트는 무엇을 만드는가.
2. 핵심 플레이어·사용자 경험은 무엇인가.
3. 현재 어느 단계까지 진행됐는가.
4. 지금 가장 우선할 작업은 무엇인가.
5. 무엇을 변경하면 안 되는가.
6. 각 분야의 책임 원본은 어디인가.
7. 어떤 Skill과 Work Mode를 사용해야 하는가.
8. 구현 전후 어떤 Gate가 있는가.
9. 완료 후 무엇을 갱신해야 하는가.
10. 남은 위험·보류·미확정은 무엇인가.
11. 프로젝트 교훈은 어디에 기록하는가.

권장 읽기 경로:

```text
AGENTS
→ START_HERE
→ Base pin
→ Documentation Map
→ Active Context·Handoff
→ 프로젝트 방향
→ 해당 분야 책임 원본
→ 해당 Skill
→ Roadmap·Issue·Plan
→ 실제 파일·테스트
```

실패하면 진입 문서·Map·Handoff·책임 연결을 개선하고 다시 검증한다.

---

## 27. 프로젝트 학습·Base 환류

### PROJECT_LEARNING_AND_BASE_FEEDBACK

```text
Skill 적용
→ 실제 작업
→ 결과 검증
→ 성공·실패·예외 기록
→ 프로젝트 고유 정보와 재사용 원리 분리
→ 프로젝트 Skill 갱신
→ 반복 검증
→ 공용화 가치 판정
→ 필요 시 Base 제안
```

학습 상태:

- `OBSERVATION`
- `HYPOTHESIS`
- `PATTERN`
- `VALIDATED_PRACTICE`
- `BASE_PROMOTION_CANDIDATE`

한 번 성공한 방법을 즉시 공용 강제 규칙으로 만들지 않는다.

실패도 다음과 함께 보존한다.

- 상황
- 시도
- 실패 이유
- 재발 조건
- 수정할 Skill·검수 기준
- 재검증 방법

---

## 28. 검증 계층

현재 범위에 적용되는 것만 실제 실행한다.

```text
contract-check
→ previous-contract-preservation
→ project-inventory
→ multi-lens-review
→ reference-freshness
→ static-validation
→ runtime-validation
→ accessibility-review
→ performance-profile
→ cold-start-validation
→ decision-sync-readback
→ codex-packet-readiness
→ vertical-slice-completeness
→ demo-build-and-playthrough
→ regression
→ evidence-report
```

상태:

- `PASS`
- `FAIL`
- `NOT_RUN`
- `NOT_APPLICABLE`
- `BLOCKED_UNVERIFIED`

한 계층의 통과를 다른 계층으로 확대하지 않는다.

- 문서 검사 ≠ 런타임 검증
- 이미지 존재 ≠ UI 구현·접근성
- 테스트 통과 ≠ 재미 검증
- Evidence Pack ≠ 시장성·출시 준비
- 콜드 스타트 통과 ≠ 실제 게임 품질

---

## 29. PR Check

파일 변경 시 다음을 수행한다.

```text
최신 main·동일 Goal PR 재조회
→ 별도 Branch/worktree
→ 기준 main SHA·작업 HEAD 기록
→ 승인 범위·예상 파일
→ 최소 변경
→ 관련 검증
→ attack → validate-critique
→ Draft PR
→ PR metadata·base·head
→ exact HEAD SHA
→ 전체 changed-file inventory·diff
→ 승인 계약·정본·실제 변경 대조
→ untouched 소비자·테스트·파생본
→ Required Check·Actions
→ review·unresolved review thread
→ 최신 main·behind·mergeability
→ Ruleset·branch protection·merge 방식
→ regression-recheck
→ 최종 판정
```

HEAD가 바뀌면 이전 검수·승인·CI 판정을 무효화하고 재검증한다.

PR 상태:

- `PR_DRAFT_IN_PROGRESS`
- `PR_REVISE`
- `PR_USER_DECISION_REQUIRED`
- `PR_BLOCKED_UNVERIFIED`
- `PR_CHECKS_FAILED`
- `PR_REVIEW_THREADS_OPEN`
- `PR_APPROVED_EXACT_HEAD`
- `AUTO_MERGE_ELIGIBLE`
- `MERGE_NOT_REQUESTED`

병합 가능 조건:

- Draft가 아님
- 검수 exact HEAD와 현재 HEAD 일치
- 승인 범위와 전체 diff 일치
- Required Check 성공
- unresolved review thread 0
- 차단 finding·사용자 결정 없음
- 최신 main 기준 검증
- 저장소 merge 정책 확인
- 적대적 회귀 검수 완료

사용자가 병합을 명시하지 않으면 `MERGE_NOT_REQUESTED`로 멈춘다.

---

## 30. 필수 산출물

### `[총기획]`

1. Baseline Recovery Record
2. `[핵심 내용]` 추적표
3. 이전 계약 보존 비교표
4. 프로젝트 전체 인벤토리
5. 보존 강점 지도
6. Responsibility Source Map
7. Project Health Matrix
8. 개발 Gate 감사
9. `00 / 10 / 20 / 30 / 40 / 50 / 99` 기획 Coverage
10. 기획 결함·분야 충돌 Ledger
11. 벤치마크·플레이어·현업 Evidence
12. 적대적 검토와 검증된 finding
13. Improvement Backlog
14. 필요한 Grill Me Decision
15. 승인 개선과 정본·소비자 반영
16. File Treatment Matrix
17. PDF·파생본 감사
18. Skill·Workflow 감사
19. 콜드 스타트 검증
20. 프로젝트 학습·Base 환류 후보
21. Decision Sync Ledger와 동일 Decision ID 재조회 증거
22. Planning and Review Complete Gate 판정
23. Codex Definition of Ready와 Codex Execution Packet
24. Vertical Slice Completeness Matrix와 Demo Ready 판정
25. 검증 보고
26. 변경 시 PR exact-HEAD Check

### `[검수]`

동일 산출물을 읽기 전용으로 만들되 승인되지 않은 수정은 수행하지 않는다.

---

## 31. 완료 기준

다음을 모두 충족해야 한다.

- `[핵심 내용]` 전체 추적
- 이전 총기획 계약의 강점이 보존·개선됨
- 프로젝트 전체 Surface의 인벤토리와 검수 상태 존재
- 핵심 분야에 현행 책임 원본 존재
- 한 주제를 여러 활성 문서가 중복 책임하지 않음
- 기획 공백·충돌·실제 구현 불일치가 판정됨
- 보호 강점과 정상 경로가 유지됨
- 필요한 개발 Gate가 반영됨
- 프로젝트 Skill과 공용 Skill 경계가 명확함
- 승인 개선이 정본과 활성 소비자에 전파됨
- 제거·이동 파일의 잔여 참조가 없음
- PDF·Sheet·파생본과 원본이 일치하거나 상태가 명시됨
- 새 채팅에서 저장소만으로 작업을 재개할 수 있음
- Active Context·Handoff가 현재 상태를 반영함
- 실행하지 않은 검증이 명시됨
- 프로젝트 고유 정보와 Base 공용 원리가 분리됨
- 주요 변경·승인 Decision이 GitHub 권위 문서·계획 데이터·연결 Sheet에 동일 Decision ID와 commit SHA로 `SYNCED`
- 기획·검수 완료 Gate가 닫히고 Codex가 재해석 없이 실행 가능한 Packet이 존재함
- 승인된 버티컬 슬라이스 기획이 구현·검증되거나 Decision ID로 명시적 제외됨
- 완성형 데모의 Build·패키징·실행·플레이스루 증거가 있음
- exact-HEAD PR Check가 현재 변경과 일치함
- 차단 finding이 없거나 사용자 결정·재개 조건이 명시됨

최종 판정:

- `TOTAL_PLANNING_IMPROVED`
- `TOTAL_PLANNING_IMPROVED_WITH_DEFERRED_ITEMS`
- `REVIEW_ONLY_COMPLETE`
- `MUST_FIX_REMAINS`
- `USER_DECISION_REQUIRED`
- `BLOCKED_UNVERIFIED`
- `REVISE`

---

## 32. 최종 보고 형식

```md
# 프로젝트 총기획·검수 결과

## 1. 결론
- 전체 상태:
- 보존한 강점:
- 즉시 수정한 문제:
- 남은 차단 문제:
- 사용자 결정:

## 2. 기준선
- Base·Project main SHA:
- Branch·HEAD:
- 관련 PR:
- 정본·실제 구현·Sheet·파생본:

## 3. 이전 지시문 대비
- 보존:
- 개선:
- 의도적 대체:
- 회귀:

## 4. 프로젝트 건강도
- 운영:
- 제품·경험:
- 시스템·콘텐츠:
- 세계·서사:
- UX·표현:
- 기술·데이터:
- 제작·검증:
- Skill·Workflow:
- 콜드 스타트:

## 5. 기획 공백·충돌
| ID | 유형 | 영향 | 판정 | 개선 | 검증 |

## 6. Grill Me·승인 Decision

## 7. 파일 처리
| 파일 | 처리 | 이유 | 현행 책임 원본 | 상태 |

## 8. 정본·소비자·파생본 반영

## 9. Decision 즉시 동기화
- Decision ID:
- GitHub 권위 위치:
- 계획 데이터 위치:
- 연결 Sheet 위치:
- commit SHA:
- 재조회·SYNCED:

## 10. Codex 구현 인계
- Planning and Review Complete Gate:
- Codex Definition of Ready:
- Execution Packet:
- v9 라우팅:

## 11. 완성형 버티컬 슬라이스
- Completeness Matrix:
- 미구현·명시적 제외:
- Demo Ready Gate:
- Build·패키징·플레이스루:

## 12. 적대적 검토
- MUST_FIX:
- SHOULD_FIX:
- REJECTED_CRITIQUE:
- BLOCKED_UNVERIFIED:
- 회귀 재검사:

## 13. 검증
- PASS:
- FAIL:
- NOT_RUN:
- NOT_APPLICABLE:
- BLOCKED_UNVERIFIED:

## 14. PR Check
- exact HEAD:
- changed files:
- Required Check:
- unresolved thread:
- merge 판정:

## 15. 보류·제거 후보·Base 환류

## 16. 다음 Gate·롤백
```

---

## 33. 실패 조건

다음 중 하나라도 해당하면 완료가 아니다.

- 프로젝트 전체 감사 전에 새 기획을 발명함
- 기존 강점·승인 결정·사용자 변경을 고정하지 않음
- 저장소에서 확인 가능한 사실을 사용자에게 반복 질문함
- `[핵심 내용]`을 축약해 목적을 약화함
- 이전 총기획 계약의 검수 Surface를 이유 없이 삭제함
- 기능 목록은 많지만 플레이어 약속·Core Loop와 연결되지 않음
- 분야별 기획 간 충돌을 검사하지 않음
- 성공 사례만 벤치마킹함
- AI 추론을 공식 사실로 사용함
- 시험값을 확정값으로 기록함
- Grill Me를 감사 전 선호 인터뷰로 사용함
- 반대를 위한 적대 검토를 수행함
- 비판의 사실성·영향을 재검증하지 않음
- 사용자 승인 없이 주요 기획·자산을 변경함
- 주요 변경·승인 Decision을 작업 끝까지 배치하고 즉시 정본·Sheet 동기화하지 않음
- 동일 Decision ID 없이 GitHub와 Sheet에 서로 다른 기록을 남김
- commit SHA·변경 경로·섹션·행·Sheet 위치를 기록하지 않음
- `PARTIAL_SYNC_BLOCKED` 상태에서 다음 주요 기획·구현 단계로 진행함
- 기획·검수 Gate가 닫히기 전에 Codex 구현을 시작함
- Codex에 파일·데이터·Scene·테스트·수용 기준 없이 모호한 지시를 전달함
- Codex가 기획 공백을 임의 재해석하도록 방치함
- 승인된 버티컬 슬라이스 범위에 문서상 기능·미구현·가짜 흐름을 남기고 데모 완료를 주장함
- Build·패키징·전체 플레이스루 없이 완성형 데모를 주장함
- changed file만 보고 untouched 소비자를 누락함
- 모든 파일을 거대한 단일 문서로 합침
- 새 버전·final·latest 복제본을 현행 정본으로 만듦
- 구형 파일명만 보고 삭제함
- 삭제 전에 참조 관계를 확인하지 않음
- PDF·Sheet·Dashboard를 정본이나 실제 구현으로 오인함
- PDF만 갱신하고 원본을 방치함
- 프로젝트 고유 정보를 Base에 복사함
- 검증되지 않은 한 번의 성공을 공용 규칙으로 승격함
- 콜드 스타트 검증을 생략함
- 실행하지 않은 테스트·런타임·사람 검수를 PASS로 보고함
- 과거 HEAD의 증거로 현재 PR을 승인함
- Required Check 실패·skip·unresolved thread를 무시함
- 남은 위험·미검증·롤백 없이 완료를 선언함
