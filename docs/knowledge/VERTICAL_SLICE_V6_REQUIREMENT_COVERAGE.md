---
document_role: MIGRATION_TRACEABILITY
source_contract: VERTICAL_SLICE_MASTER_REFERENCE_v6
replacement_execution_prompt: templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md
active_authority: false
implementation_authority: NONE
---

# Vertical Slice v6 → 통합 실행문 v7 마이그레이션 추적표

## 목적

이 문서는 사용자가 제공한 `VERTICAL_SLICE_MASTER_REFERENCE_v6`와 별도 축약 실행문의 요구를 현재 Base의 Registry·통합 Skill·지식 Reference·Template·Test와 단일 첨부용 v7 통합 실행문에 어떻게 무손실로 승계했는지 추적한다.

이 파일은 현행 실행 정본이 아니다. 실제 작업 실행은 다음 순서로 권한을 확인한다.

```text
사용자 최신 승인
→ 프로젝트 AGENTS·CURRENT_CONFIRMED_DECISIONS·분야 정본·실제 파일
→ 프로젝트에 동기화된 Base 규칙
→ Base 최신 main 정본·Registry
→ templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md
→ 이 MIGRATION_TRACEABILITY 기록
```

## 통합 원칙

- 사용자 최신 지시가 최상위다.
- Base 공용 Skill 본문은 프로젝트에 복제하지 않는다.
- 새 Skill은 기존 Base에 같은 책임이 없을 때만 만든다.
- 저장소 전체 감사는 새 중복 Skill이 아니라 `running-adversarial-review-and-refinement: repository-wide-audit` mode와 전문 Reference로 통합한다.
- 기존 `designing-vertical-slices` Skill의 책임·mode·Registry 계약은 보존한다.
- Grill Me·적대적 검토·자산 조사·문서·검증·인수인계는 기존 전문 Skill에 위임한다.
- v6 상세 내용과 당시 축약 실행 지시는 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` 한 파일에 통합한다.
- 통합 Prompt는 Base·프로젝트 정본보다 높은 권한을 갖지 않으며 drift는 `STALE_PROMPT_CONTRACT`로 보고한다.
- 별도 `CORE_POC` 제품 Gate는 사용하지 않고 완성 품질 `DEMO_FIRST_VERTICAL_SLICE`와 필요 시 Slice 내부 `TECHNICAL_SPIKE`로 승계한다.
- Base 자체는 Google Sheets 동기화 대상이 아니며 `BASE_EXCLUDED`다.

## Requirement Coverage

| v6 책임 | v7·Base 책임 원본 | 승계·변경 |
|---|---|---|
| 상세 참고 파일 + 별도 축약 실행문 | `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | 상세 정본과 작업 시작 인터뷰·실행 지시를 단일 첨부 파일로 통합 |
| 4단계 제품 Gate | `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md` + 통합 Prompt | `CONCEPT_APPROVAL → DEMO_FIRST_VERTICAL_SLICE → PRODUCTION_APPROVAL → RELEASE_CANDIDATE_APPROVAL` |
| 과거 `CORE_POC`·`SLICE_VALIDATION` | concept Skill + Gate Reference + 통합 Prompt | 별도 Core PoC Gate를 제거하고 내부 `TECHNICAL_SPIKE`·`DEMO_VALIDATION` 호환 해석으로 변경 |
| 프로토타입에서 멈추지 않는 Stage 2 | Gate Reference·Vertical Slice Template·통합 Prompt | 완성 품질 데모·통합 QA·내부/외부 플레이테스트·반응 조사까지 연속 프로그램으로 확정 |
| 작업 전 저장소 읽기 | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` + Intake Skill + 통합 Prompt | 최신 main·Decision·정본·PR·실제 파일·프로젝트 Sheet 선감사 추가 |
| 반복 질문 방지 | `docs/CONFIRMED_DECISION_SYNC_POLICY.md` + Intake Skill | 기존 Decision 복원·`RECOMMENDED_DEFAULT`·`USER_DECISION_REQUIRED` 분리 |
| 분야별 기획 순서 | Planning Sequence Policy + Sheet tab Template + 통합 Prompt | 00→99 Approval Bundle·프로젝트 Sheet tab 순서 추가 |
| 벤치마킹 | concept Skill Evidence Reference + 통합 Prompt | 벤치마크·플레이어 반응·현업/공식 권장 3층 Evidence Pack으로 확대 |
| PC Steam·STOVE·itch.io 패키지 | Gate Reference·Vertical Slice Template·통합 Prompt | 상세 데모·상점·Playtest 계약 보존 |
| 모바일 Google Play 패키지 | Gate Reference·Vertical Slice Template·통합 Prompt | AAB·기기·저장·정책·퍼널 계약 보존 |
| Steam 출시 예정 페이지·트레일러·스크린샷 | Gate Reference·Template 추적표·통합 Prompt | Slice 요소의 플레이·테스트·판매 추적성 보존 |
| STOVE 피드백·핵심 재미 시작점 | Gate Reference·통합 Prompt | 외부 검증 항목 보존 |
| Steam Playtest | Vertical Slice Skill·Gate Reference·통합 Prompt | 빌드·표본·과제·관찰·설문 계약 보존 |
| 텀블벅 준비도 | Gate Reference·통합 Prompt | 팬덤·리워드·남은 범위·위험 계약 보존 |
| 세부 수치 유예 | Asset·Mascot·Tuning Reference·Template·통합 Prompt | 상태·Balance Tuning Backlog 보존 |
| UI·UX·사운드 콘셉트 우선 | Asset·Mascot Reference·통합 Prompt | 상세 역할·접근성·무음 피드백 보존 |
| 에셋스토어 우선·없는 경우 생성 | Godot Asset Skill + 통합 Prompt | Pinterest 포함 발견 → 원출처·라이선스·유사성 → 채택/생성 순서로 확대 |
| 세계관 마스코트 | Asset·Mascot Reference·통합 Prompt | 역할·제한·Slice 증거 보존 |
| Grill Me 0~3 | Skill orchestration Reference + 통합 Prompt | 저장소로 해결되지 않는 차단 기획 결정에만 조건부 적용 |
| 적대적 검토 5개 렌즈 | 기존 review Skill + 통합 Prompt | 공격·비판 검증·최소 수정·회귀 분리 보존 |
| 저장소 전체 검수 | `running-adversarial-review-and-refinement: repository-wide-audit` | 권한 지도·전수 범위·stale·untouched 소비자·Prompt/파생본 drift 추가 |
| 많은 Skill의 적절한 사용 | Skill orchestration Reference + 통합 Prompt | 하위 작업별 최소 충분 Skill 체인 보존 |
| Superpowers 개발 체인 | Skill orchestration Reference + 통합 Prompt | 실제 설치·Trigger·승인 조건부 연결 보존 |
| DeepSeek·외부 AI 격리 | Skill orchestration Reference + 통합 Prompt | external-source-review 연결 보존 |
| P0~P3 | Skill orchestration Reference·통합 Prompt | 우선순위와 실패 시나리오 근거 보존 |
| HiGodot 조건부 구조 검증 | Skill orchestration Reference·통합 Prompt | 실제 연결·도구 확인 조건 보존 |
| GitHub·PDF 발행 | Skill orchestration Reference·통합 Prompt | 조건부 프로필·Manifest·전 페이지 검수 보존 |
| Skill 실행 증거 | `SKILL_EXECUTION_EVIDENCE.md` + 통합 Prompt | 읽음과 실제 실행을 분리 |
| Requirement·Skill·Artifact 완전성 | 지식 Reference·Template·Test·통합 Prompt | 3중 감사 보존 |
| 내용 누락 방지 | Completeness-first 정책 + 통합 Prompt | 줄 수·문자 수·분량 상한 대신 내용 보존·한 단계 발견성 적용 |

## 2026-07-28 최신 사용자 결정

- 상세 참고 계약과 짧은 실행문을 분리하지 않고 **상세 정본을 포함한 통합 실행문 한 파일**을 사용한다.
- 통합 실행문이 작업마다 저장소 조사 후 필요한 인터뷰를 수행한다.
- 별도 `CORE_POC` 제품 단계는 사용하지 않는다.
- 첫 통합 플레이 제품은 완성 품질의 `DEMO_FIRST_VERTICAL_SLICE`다.
- 기술 불확실성은 Slice 내부의 제한된 `TECHNICAL_SPIKE`로만 검증한다.
- 과거 v6의 `CORE_POC`·`PROTOTYPE_AND_VERTICAL_SLICE`·`SLICE_VALIDATION`·`VERTICAL_SLICE_FULL_PROFILE` 표기는 각각 내부 Spike·`DEMO_FIRST_VERTICAL_SLICE`·`DEMO_VALIDATION`·`DEMO_FIRST_FULL_PROFILE`의 역사·호환 용어다.
- 모든 L1 이상 작업은 중복·누락·충돌·구형 참조·소비처 미반영을 먼저 감사한다.
- 새 정책·Template·Skill은 README·정본·Registry·프로젝트 설치·분야 소비자·Test의 실제 연결을 검증한다.
- 중요한 기획은 벤치마킹·플레이어 반응·현업/공식 권장 근거를 함께 검토한다.

## 기존 책임 보존

다음 기존 계약을 제거하지 않는다.

- Prototype / Vertical Slice / MVP / Demo의 개념 구분. 단, Prototype은 필수 제품 Gate가 아니다.
- `slice-contract / quality-bar / pipeline-proof / playtest-evidence / decision-gate`
- 접근성·성능 전문 검증 위임
- 선택적 하이라이트의 보유·미보유 정상 완주 사례
- 실제 빌드·표본·행동·자기보고 분리
- 제작 파이프라인의 두 번째 콘텐츠 반복 증명
- `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP`의 과거 판정은 현행 Gate 판정과 대체 관계를 명시해 보존
- `skills/SKILL_REGISTRY.json`의 단일 `designing-vertical-slices` 항목
- 시스템·규칙·예외·콘텐츠 제작 문법·마스코트·에셋 원장·출시 준비의 상세 표와 체크리스트

## 비채택·변형

- v6 파일을 Base 정본보다 높은 독립 정본으로 두지 않는다. v7 통합 Prompt는 실행 Template이며 최신 정본 drift를 스스로 보고한다.
- 별도 짧은 실행문을 유지하지 않는다. 통합 Prompt의 시작 인터뷰가 현재 목표·단계·범위를 수집한다.
- 모든 Skill을 한 번에 로드하지 않는다. 하위 작업별 최소 충분 Skill을 순차 오케스트레이션한다.
- 고정 횟수의 적대적 검토 대신 독립 렌즈와 `repository-wide-audit`를 위험에 맞춰 적용한다.
- 모든 작업에서 PDF·HiGodot·DeepSeek를 강제하지 않는다. Trigger·도구·발행 정책이 맞을 때만 실행한다.
- 세부 수치 조정은 기획 승인 질문이 아니라 플레이테스트 Backlog로 관리한다.
- 검색 결과만으로 전체 저장소 검수를 완료했다고 주장하지 않는다. tracked inventory 또는 미검증 범위가 필요하다.

## ALLOWED_LEGACY — 허용된 역사·호환 표현

다음 위치의 과거 용어는 현행 권한이 없다는 문맥이 명시된 경우 유지할 수 있다.

- GitHub 병합 PR·Issue·Discussion
- `docs/CHANGELOG.md`
- 완료된 `docs/superpowers/plans/**`
- 이 Migration Traceability 문서
- Legacy Alias·Migration·Compatibility 문서
- 구형 상태를 재현하는 Test fixture

활성 README·START_HERE·운영 정본·Skill·Template·Prompt·실행 순서에서 구형 단계가 현행처럼 사용되면 `STALE_REFERENCE` 또는 `STALE_PROMPT_CONTRACT`다.

## 검증

- `tests/test_integrated_vertical_slice_prompt_v7.py`
- `tests/test_vertical_slice_v6_contract.py`
- `tests/test_demo_first_planning_sequence.py`
- `tests/test_consolidated_skill_references.py`
- Skill Registry·package integrity·reference freshness·documentation routing CI
- PR Actions의 contract·publication·`ci-gate`
- 병합 후 `repository-wide-audit`와 중복 PR·branch 재검사
