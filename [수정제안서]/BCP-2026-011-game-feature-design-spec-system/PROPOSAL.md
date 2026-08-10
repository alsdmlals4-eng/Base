# BCP-2026-011 — 게임 기능 세부기획 Spec 계층 통합

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `2a6ced23f6d6de1fb6e0a281c7138beb03f1a13b`
- 제출일: `2026-08-10`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴 + 구현 전 가설`

## 관찰과 증거

Base는 이미 다음 책임을 분리한다.

- `analyzing-and-refining-game-concepts`: 핵심 컨셉, 시스템 설계, 벤치마크, PoC, 플레이테스트.
- `managing-design-documents`: 승인된 기획 책임 원본의 작성·갱신·구조·발행.
- `FEATURE_SPEC_TRACEABILITY_PACKET`: L2 이상 승인 작업에서 `Decision → Requirement → Acceptance → Task → Implementation → Verification` 추적.
- 프로젝트 Google Sheets GDD: 상세 정본을 복제하지 않는 `USER_FACING_GDD_WORKSPACE`.
- `running-adversarial-review-and-refinement`: 설계·정책·구조의 실패 가정, 비판 검증, 회귀 재검토.

그러나 범용 기획 문서 작성 골격은 `목적 → 경험 → 규칙 → 흐름 → 예외 → 실제 경로 → 검증 → 다음 단계` 수준이며, PoC를 통과한 기능을 프로그래밍·UX/UI·아트·오디오·QA가 같은 의미로 구현하기 위한 **기능 단위 세부 설계 계약**은 공용 Template으로 명시되어 있지 않다.

현업 벤치마킹은 하나의 거대한 GDD보다 유지 가능한 여러 해상도의 문서와 명확한 팀 커뮤니케이션을 지지한다.

- GDC 2025, Ian Schreiber, *The Four One-Page Design Docs You Need (And How to Use Them)*: game vision, pillars, loops, resource flow처럼 목적이 다른 핵심 문서를 유지 가능하게 분리한다.
- GDC 2010, Stone Librande, *One-Page Designs*: 핵심 설계 아이디어를 짧고 시각적으로 전달해 팀 커뮤니케이션을 개선한다.
- Ubisoft Creative Process: Conception의 비전·연구·PoC, Preproduction의 First Playable, Production의 본격 자산·코드 제작을 구분한다.
- Game Developer 2023의 현업 인터뷰: 현대 GDD는 monolithic design bible보다 검색 가능하고 읽기 쉽고 프로젝트에 맞게 구성되어야 하며, 여러 직군이 동일한 설계 의도를 이해할 수 있어야 한다.

상세 근거와 Base 대조는 `evidence/INDUSTRY_BENCHMARK_AND_BASE_GAP_ANALYSIS.md`에 기록한다.

## 일반화 후보

### 1. 문서 해상도 계층

```text
L0 PROJECT DIRECTION
게임 비전·Pillar·Core Loop·Resource Flow

→ L1 FEATURE BRIEF
플레이어 문제·경험 약속·범위·핵심 위험을 짧게 정의

→ PoC / benchmark / adversarial review

→ L2 GAME FEATURE DESIGN SPEC
실제 제작자가 구현할 수 있는 행동·규칙·상태·피드백·예외·데이터·제작 입력·검증 계약

→ 승인

→ L3 FEATURE SPEC TRACEABILITY PACKET
Decision·Requirement·Acceptance를 Task·Implementation·Verification에 연결
```

### 2. 새 광역 Skill을 만들지 않는다

새 `game-detailed-planning` 계열 ACTIVE Skill은 추가하지 않는다.

- 설계 전략·PoC: 기존 `analyzing-and-refining-game-concepts`.
- 세부기획 책임 원본 작성: 기존 `managing-design-documents`.
- 구현 추적: 기존 `FEATURE_SPEC_TRACEABILITY_PACKET` + intake/validation.
- 실패 공격: 기존 `running-adversarial-review-and-refinement`.

기존 owner의 mode/reference/Template 확장으로 책임을 보존할 수 있으므로 `Consolidation First`를 적용한다.

### 3. L2 `GAME_FEATURE_DESIGN_SPEC`가 소유할 질문

기능 Spec은 최소 다음을 답한다.

1. `Identity`: Feature ID, Decision ID, 책임 정본, 상태.
2. `Player Problem`: 어떤 플레이 문제·욕구를 해결하는가.
3. `Experience Intent`: 행동·판단·감정·피드백 목표.
4. `Core Alignment`: Pillar·Core Loop와의 연결.
5. `Scope`: 포함·제외·비목표.
6. `Player Verbs`: 실제 입력과 반복 행동.
7. `Entry / Exit`: 진입·종료·취소·재진입.
8. `Flow`: 조건 → 입력 → 처리 → 판단 → 결과 → 다음 상태.
9. `State & Rules`: 상태, 전이, 판정, 우선순위.
10. `Feedback`: UI·VFX·Animation·Audio 정보 전달.
11. `Success / Failure / Recovery`: 성공·실패·부분 성공·복구.
12. `Edge Cases`: 연타, 자원 부족, 저장/불러오기, 취소, 재시도, 중복 보상 등.
13. `Data & Balance`: 공식·단위·초기값·조정 범위·데이터 정본·재조정 조건.
14. `UX/UI & Accessibility`: 화면, 입력, focus, 읽기·색·동작 대안.
15. `Art / Audio / Narrative Inputs`: 필요한 제작 입력과 책임 owner.
16. `Technical Constraints`: 플랫폼·성능·저장·온라인·데이터 제약.
17. `Content Pipeline`: 반복 콘텐츠의 제작 방식과 데이터 경계.
18. `Benchmark Decision`: `ADOPT / ADAPT / TEST / AVOID / IGNORE`.
19. `Risk & Prototype`: 가장 위험한 가정과 PoC 증거.
20. `Acceptance`: `조건 → 플레이어 행동 → 관찰 가능한 결과`.
21. `Telemetry / Playtest`: 성공·실패를 판정할 관찰과 지표.
22. `Cut-down / Rollback`: 일정·위험 발생 시 제거 순서와 복귀 조건.
23. `Open Decisions`: `CONFIRMED / RECOMMENDED_DEFAULT / USER_DECISION_REQUIRED / BLOCKED_UNVERIFIED`.

### 4. 소유하지 않을 질문

`GAME_FEATURE_DESIGN_SPEC`는 다음을 소유하지 않는다.

- Task별 구현 진행률.
- 코드 파일별 완료 여부.
- 실제 테스트 실행 결과.
- PR/Commit별 변경 상태.
- Google Sheets의 현재 Decision 원장.
- 프로젝트 전체 Roadmap.

이 항목은 기존 Traceability Packet, 실제 구현·테스트, Decision 정본, Roadmap이 계속 소유한다.

### 5. Progressive Detail Gate

세부기획은 기능 아이디어가 생길 때마다 완전한 Spec을 강제하지 않는다.

```text
아이디어/방향 탐색
→ L1 Feature Brief
→ 위험 가설·벤치마크·PoC
→ KEEP / CHANGE / REMOVE / DEFER
→ 살아남은 기능만 L2 Feature Design Spec
→ 승인 후 L3 Traceability
```

문서 양보다 **결정을 바꿀 위험을 먼저 싸게 검증**하는 것을 우선한다.

## 프로젝트 전용으로 남길 내용

- 게임별 실제 Feature ID·Decision ID.
- 장르별 수치·공식·밸런스 범위.
- 프로젝트 고유 UI·아트·오디오·서사 내용.
- 실제 Godot Scene·Resource·Script·데이터 경로.
- 팀 구성·스프린트·일정·예산.
- 프로젝트별 Google Sheets tab/row와 실제 구현·테스트 상태.

## 적용 조건과 비사용 조건

적용:

- PoC 이후 제작 준비가 필요한 주요 기능.
- 여러 직군이 같은 기능 의미를 공유해야 하는 L2 이상 설계.
- 상태·규칙·예외·수치·UI·제작 입력이 얽힌 시스템.
- 구현 전에 Acceptance와 Cut-down 경계를 명시해야 하는 기능.

비사용:

- L0 오탈자·링크 수정.
- 이미 승인·정의된 단일 구현의 작은 수정.
- 아직 폐기 가능성이 큰 초기 아이디어.
- Traceability만 필요한 승인 완료 기능.
- 특정 전문 분야 Template이 이미 더 정확한 책임 원본을 제공하고 추가 Feature Spec이 중복 정본이 되는 경우.

## 반례와 위험

### 공격 결과

1. **거대한 MASTER_GDD로 통합**
   - 장점: 단일 진입점.
   - 실패: 수정 충돌·중복·낮은 검색성·과도한 컨텍스트·한 질문 한 정본 위반.
   - 판정: `AVOID`.

2. **새 ACTIVE 세부기획 Skill 추가**
   - 장점: 발견성이 높음.
   - 실패: concept/document owner와 승인·출력 경계 중복.
   - 판정: `AVOID`.

3. **모든 Feature에 상세 Spec 강제**
   - 장점: 일관성.
   - 실패: PoC 전에 문서 비용을 과투자하고 폐기 비용 증가.
   - 판정: `AVOID`.

4. **Feature Spec에 Task·테스트 결과까지 포함**
   - 장점: 한 파일에서 전체 상태 확인.
   - 실패: 기존 Traceability Packet·실제 구현·테스트와 이중 정본.
   - 판정: `MUST_NOT_DUPLICATE`.

5. **전문 분야 Template을 Feature Spec으로 대체**
   - 장점: 양식 통일.
   - 실패: 전투 AI, UX/UI, 아트 등 전문 계약의 고유 필드 손실.
   - 판정: `REFERENCE_OR_COMPOSE`, 대체 금지.

### PRE_EXISTING_GOVERNANCE_FINDING

현재 main의 `PROPOSAL_REGISTRY.json`에는 `BCP-2026-008`이 없지만 PR #190의 proposal과 병합된 구현 PR #192에서 해당 ID가 역사적으로 사용됐다. 새 제안은 ID 재사용을 피하기 위해 `BCP-2026-011`을 사용한다.

이 불일치는 이번 기능 세부기획 구조와 독립된 기존 Governance 문제이므로 proposal 범위에서 자동 수정하지 않는다. 별도 repository-wide audit에서 `ALLOWED_LEGACY / MISSING_REGISTRY_HISTORY / REPAIR_REQUIRED`를 판정해야 한다.

## 영향 범위와 검증

승인 후 구현 후보:

- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` 신규.
- `skills/managing-design-documents/SKILL.md`에 Feature Design Spec 작성/갱신 경계 연결.
- `skills/analyzing-and-refining-game-concepts/SKILL.md`에 PoC → 상세 Spec 승격 Gate 연결.
- `templates/planning/DESIGN_DOCUMENT_SYSTEM.md`에 L0→L1→L2→L3 해상도 계층 연결.
- `templates/planning/FEATURE_SPEC_TRACEABILITY_PACKET.md`에 upstream `design_spec_id / canonical_design_spec_path` 연결만 추가.
- 필요 시 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`·Sheet Template에 Feature Spec 링크 규칙만 보강하며 전문은 복제하지 않음.
- 관련 reference-freshness·contract tests와 Learning Log.

승인 전에는 위 활성 파일을 변경하지 않는다.

검증 계획:

1. 기존 전문 Template과 책임 중복 검사.
2. L0/L1 비사용 시나리오.
3. PoC 전 과도한 상세화 방지.
4. Feature Spec → Traceability 연결 테스트.
5. Google Sheets가 상세 전문을 복제하지 않는지 검사.
6. `running-adversarial-review-and-refinement`로 cross-discipline 누락 공격.
7. canonical reference freshness와 관련 Base 필수 CI.
8. 실제 프로젝트 Pilot 전에는 사람 이해도·실제 구현 품질을 통과로 주장하지 않음.

## 필요한 도구·파일·권한

- 필요 항목: GitHub Base repository read/write, 웹 공개 자료 조회, 기존 Base validation.
- 필요한 이유: proposal 추적, 현행 책임 원본 대조, 구현 후 회귀 검증.
- 설치·적용 방법: 신규 외부 도구 설치 없음.
- 설치 후 확인 명령: 구현 단계에서 Base의 기존 테스트·validation 명령 사용.
- 최소 권한: Base proposal branch/PR 작성 권한. 시스템 전역 설치·보안 권한 확대 불필요.

## 승인과 구현

- 사용자 승인 근거: `2026-08-10 현재 대화에서 "진행해"로 written spec 검토 및 구현 진행 승인.`
- 승인 참조: `[수정제안서]/BCP-2026-011-game-feature-design-spec-system/PROPOSAL.md#승인과-구현`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 구현 계획: `[수정제안서]/BCP-2026-011-game-feature-design-spec-system/IMPLEMENTATION_PLAN.md`
- 구현 PR: `등록 전`
- 롤백: 구현 PR을 닫고 이 상태전이 커밋을 되돌리면 활성 Base 기능 변경 없이 `SUBMITTED`로 복귀할 수 있다.
