---
contract_name: VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT
contract_version: "9.1"
release_line: "Base v9.3"
active_authority: true
status: ACTIVE_EXECUTION_CONTRACT
language: ko-KR
base_repository: "https://github.com/alsdmlals4-eng/Base"
usage: "이 파일 하나만 첨부하면 저장소 우선 인터뷰부터 기획·Codex 인계·구현·검수·병합 후 Notion/repository readback까지 현재 작업에 필요한 절차를 실행한다."
execution_model: SINGLE_ATTACHMENT_RECONCILIATION_AWARE_INTEGRATED_EXECUTION
legacy_contracts:
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md
  - templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md
  - LEGACY_REFERENCE_INPUT: VERTICAL_SLICE_MASTER_REFERENCE_v6.md
core_policies:
  - APPLICATION_BINDING
  - REPOSITORY_FIRST_INTERVIEW
  - INTEGRATED_DELIVERY_PROFILE
  - RECONCILIATION_PLANNING_PROFILE
  - CONDITIONAL_RECONCILIATION
  - DUPLICATE_OMISSION_CONFLICT_AUDIT
  - LEGACY_REQUIREMENT_TRACEABILITY
  - SOURCE_CONSUMER_PROPAGATION_AUDIT
  - EVIDENCE_BEFORE_COMPLETION
  - INTERMEDIATE_VISUAL_CHECKPOINT
  - LEGACY_SHEET_COMPATIBILITY_MIGRATION
  - NOTION_HUMAN_FACING_CANON
  - REPOSITORY_STRUCTURED_CANON
  - AGENT_MERGE_REQUIRED
---

# 버티컬 슬라이스 중심 게임 기획·제작·검수 통합 실행 계약 v9

## 0. 사용 범위와 권한 순서

이 파일은 **상세 정본과 실행 지시를 합친 단일 첨부용 통합 실행문**이다. 이 파일 하나만 첨부해도 저장소 우선 인터뷰를 시작하고, 현재 요청·프로젝트 Gate·승인 범위에 맞춰 기획, Codex 인계와 구현, 검수, GitHub 병합, 병합 후 repository와 적용 가능한 Notion destination readback까지 필요한 단계를 연결한다.

기존 기획을 폐기하거나 새 게임을 백지에서 설계하지 않는다. 먼저 이미 진행된 프로젝트의 정본·실제 구현·결정·증거를 복원하고, 누락·부족·중복·충돌·구형 참조만 영향도에 맞게 보완한다. **첨부 사실만으로 제품 범위나 사용자 Decision을 추정·승인하지 않는다.** 현재 사용자 요청이 감사·검토만이면 그 경계에서 끝내고, 구현을 요청·승인한 경우에만 아래의 Codex 인계와 구현 단계를 연다.

**승인 요청에서 사용자가 확정한 선택은 그대로 집행한다.** 그 선택을 사후 벤치마킹으로 되돌리거나 묵시적으로 대체하지 않는다. 반대로 **승인 외 변경은 벤치마킹·현업 비교·충돌·누락 조사와 적대적 검토**를 거쳐, 현재 증거와 장기 비용을 비교한 뒤에만 더 나은 안을 채택한다.

권한은 아래 순서로 해석한다. 하위 자료가 상위 자료를 자동으로 덮어쓰지 않는다.

```text
최신 사용자 결정
→ 프로젝트 정본과 실제 구현
→ PROJECT_BASE_ADAPTER.json · PROJECT_SKILL_SNAPSHOT.json · router
→ 현재 프로젝트에 고정된 Base 릴리스
→ 이 v9 계약
→ v6~v8 LEGACY_REFERENCE_INPUT
```

- 과거 Prompt, 첨부 파일, 예전 HTML, 구형 Skill 이름은 정본이 아니라 이력·비교 입력이다.
- `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md`는 삭제하지 않고 `SUPERSEDED_COMPATIBILITY`로 보존한다.
- `CORE_POC`, `SLICE_VALIDATION`, `VERTICAL_SLICE_FULL_PROFILE`은 이름만 보고 바꾸지 않는다. 각 프로젝트에서 `CURRENT`, `LEGACY_REFERENCE_ALLOWED`, `CANON_CONFLICT`, `STALE_REFERENCE` 중 하나를 판정하고 근거를 남긴다.
- Prompt drift, 활성인데 정본과 충돌하는 구형 문서는 `STALE_PROMPT_CONTRACT`로 기록한다.

## 1. APPLICATION_BINDING — 어떤 프로젝트에 어떤 계약을 적용하는가

다른 단계보다 먼저 다음을 읽고 `Baseline Recovery Record`에 기록한다.

1. `origin/main`의 정확한 SHA와 현재 작업 브랜치·PR 기준선.
2. `skills/PROJECT_BASE_ADAPTER.json`, `skills/PROJECT_SKILL_SNAPSHOT.json`, `.agents/skills/<project>-workflow-router/SKILL.md`.
3. 프로젝트의 Active Context, Decision Log/Registry, 설계 문서 지도, 구현 상태, 열린 Issue/PR.
4. 보호 경로와 실제 Godot 프로젝트 경로. 읽기·감사 단계에서는 보호된 코드·Scene·데이터·에셋을 수정하지 않는다. 후속 구현은 승인된 Issue/Goal·범위·검증 계약이 있을 때에만 보호 정책을 통과해 수행한다.
5. 정확한 `Project Notion Home`, Project relation, 관련 사람용 Flow/Visual/표와 마지막 destination readback. legacy Sheet가 **알려진 unique unmigrated material**을 가진 migration scope일 때만 source ID·상태를 읽고 `COMPATIBILITY_ONLY`로 기록한다. Sheet가 없거나 읽을 수 없어도 정상 계획·구현·Decision sync를 차단하지 않는다.
6. 고정된 Base `release_commit`, `release_evidence_commit`, Registry raw-byte hash, 프로젝트 로컬 Registry hash.

어댑터·스냅샷·router·실제 로컬 Skill 경로가 맞지 않거나 Base 핀이 검증되지 않으면 추측 실행하지 말고 실패 종료한다. `PROJECT_BASE_SKILL_ADAPTER.json`, `PROJECT_PATH_ADAPTER.json`, `BASE_V9_ADAPTER`는 생성된 호환 뷰일 뿐 수동 정본이 아니다.

## 2. 실행 프로필과 작업 경계

### 기본: REPOSITORY_FIRST_INTERVIEW + INTEGRATED_DELIVERY_PROFILE

첨부 직후 `APPLICATION_BINDING`을 완료하면, 기본으로 `REPOSITORY_FIRST_INTERVIEW`를 실행한다. 이 인터뷰는 프로젝트 정본·실제 구현·열린 Issue/PR·Project Notion Home과 관련 사람용 source를 먼저 읽고, 이미 확정된 질문을 되묻지 않으며, 현재 요청을 다음 네 가지로 분류한다.

```text
AUDIT_ONLY                 → 읽기·감사·시각 점검·Change Plan
PLAN_OR_DECISION           → 기획·Approval Bundle·책임 정본 갱신 제안
IMPLEMENTATION_REQUESTED   → Issue → /plan(필요 시) → /goal → Codex 인계·구현·검수
SYNC_OR_RELEASE_FOLLOWUP   → merged main 재조회 → 적용 가능한 Notion destination readback → Gate Close
```

`INTEGRATED_DELIVERY_PROFILE`은 `PLAN_OR_DECISION` 또는 `IMPLEMENTATION_REQUESTED`에 쓰는 기본 실행 경로다. 필요한 최소 Skill을 현재 Registry와 프로젝트 Snapshot에서 선택하고, 해당 Skill이 이후 추가·교체되어도 route·입력 정본·검증 증거가 유효하면 그대로 선택할 수 있다. 고정된 Skill 이름 목록이나 과거 Prompt의 절차 목록으로 제한하지 않는다.

```text
허용: 저장소 우선 인터뷰, 기획, Approval Bundle, GitHub Issue, /plan(필요 시),
      /goal, Codex 구현 인계, 승인된 범위의 정본/제품 변경, 테스트·Godot 검증,
      독립 리뷰·적대적 검토, 필수 Gate 통과 뒤 병합, merged main 기준 repository·Notion readback
금지: 요청·승인·Issue/Goal 없이 제품 범위를 발명하는 구현, 보호 경로 우회,
      legacy Sheet/Figma를 새 default workspace·write target·동기화 Gate로 복원,
      legacy Sheet 단독 변경의 자동 정본 승격,
      실제 증거 없는 런타임·사람·기기 검증 완료 주장
```

구현을 여는 최소 조건은 다음과 같다.

1. 현재 요청이 구현 또는 승인된 Change Plan 실행을 명시한다.
2. `APPLICATION_BINDING`과 필요한 정본 복원이 완료되고, 차단 `P0/P1` 또는 `CANON_CONFLICT`가 해결·승인되었다.
3. GitHub Issue와 `/goal Implement GitHub Issue #[NUMBER] exactly as specified.`가 있으며, 다중 파일·고위험·모호한 작업은 그 전에 `/plan`을 작성했다.
4. 영향받는 소비처, 보호 경로, 수용 기준, 자동·Godot 수동 검증과 문서 갱신 책임이 구현 계약에 있다.

구현 PR이 main에 병합된 **뒤에만** GitHub main SHA와 실제 구현을 다시 읽고, 사람이 봐야 하는 변화는 적용 가능한 Project Notion destination에 반영한 뒤 `Notion destination readback`으로 확인한다. legacy Sheet 단독 변경은 언제나 `PROPOSED_SHEET_CHANGE`이며, unique material이 실제로 남아 있을 때만 repository 또는 Notion owner로 이관 → destination readback → `UNIQUE / DUPLICATE / OBSOLETE` 수명주기 판정을 한다. Sheet가 존재한다는 사실만으로 새 write나 active sync를 요구하지 않는다.

### RECONCILIATION_PLANNING_PROFILE

`RECONCILIATION_PLANNING_PROFILE`은 모든 첨부의 기본값이 아니라 다음 경우에만 선택하는 안전한 감사 프로필이다.

- 사용자가 감사·복원·중간 점검·보완 계획만 요청했다.
- 구현 권한이나 제품 범위가 아직 승인되지 않았다.
- 정본 충돌, 누락된 책임, 보호 경로 영향, `P0/P1`, `CANON_CONFLICT` 때문에 구현 전 Approval Bundle이 필요하다.
- 첫 이관 파동처럼 프로젝트 적용 계약이 명시적으로 감사 전용으로 고정되어 있다.

```text
허용: 정본 복원, 비교, 무결성 검사, 시각 시뮬레이션, Finding/Change Plan/Issue 초안
금지: 게임 코드·Scene·데이터·에셋 수정, 승인 Decision 변경, 정본 덮어쓰기,
      legacy Sheet/Figma의 normal write 또는 active authority 복원, 제품 범위 PR 병합,
      성숙도/런타임 증거의 근거 없는 상승
```

이 프로필 자체를 담는 문서·계약·감사 산출물의 PR은 허용된다. 구현·정본 변경은 사용자 Decision과 별도 승인 묶음의 후속 Change Plan으로 분리한다. 감사 결과가 구현 조건을 충족하면 같은 단일 첨부 계약 안에서 `INTEGRATED_DELIVERY_PROFILE`로 전환할 수 있으며, 새 첨부나 별도 축약 Prompt를 요구하지 않는다.

### 후속 프로필 선택

후속 작업에서만 `CONCEPT_APPROVAL`, `DEMO_FIRST_VERTICAL_SLICE`, `DEMO_VALIDATION`, `TECHNICAL_SPIKE`, `PRODUCTION_APPROVAL`, `RELEASE_CANDIDATE_APPROVAL` 중 필요한 최소 프로필을 선택한다. `CORE_POC`나 이전 전체 실행 프로필을 자동으로 치환하지 않는다.

## 3. 단일 첨부 통합 실행 루프

1. `APPLICATION_BINDING` — 적용 대상, Base 핀, 보호 경계, Project Notion Home/repository owner와 필요한 legacy compatibility 상태를 확정한다.
2. `REPOSITORY_FIRST_INTERVIEW` — 요청을 정본·실제 구현·진행 상태에 대조하고, 범위·결정·다음 Gate를 확인한다. 필요한 질문만 한 번에 묻는다.
3. `PROFILE_SELECTION` — 감사만 필요한 경우 `RECONCILIATION_PLANNING_PROFILE`, 그 밖에는 `INTEGRATED_DELIVERY_PROFILE`을 선택한다.
4. `BASELINE_RECOVERY` + `DUPLICATE_OMISSION_CONFLICT_AUDIT` — 필요한 깊이만큼 기존 정본·실제 파일·결정·증거를 복원하고 Finding Ledger를 만든다.
5. `EVIDENCE_PACK` + `APPROVAL_BUNDLE` — Git SHA, 검증 상태, 소스 링크, 가정·미결정과 변경 책임·범위·수용 기준을 묶는다. 이미 확정된 질문은 다시 묻지 않는다.
6. `PLAN_AND_CODEX_HANDOFF` — 구현이 요청·승인되면 Issue → `/plan`(필요 시) → `/goal` → 구현 계약을 만든다. 요청이 감사뿐이면 Change Plan과 다음 사용자 Decision으로 끝낸다.
7. `CANONICAL_UPDATE_AND_IMPLEMENTATION` — 승인된 Issue/Goal 범위에서만 책임 정본과 Godot 구현을 최소 변경한다. 첫 감사 파동에서는 Change Plan만 만든다.
8. `PROPAGATION_AUDIT` — 변경된 repository/Notion 정본, 시각 자료, Skill, Issue, 구현 계약, 테스트 소비처를 재조회한다.
9. `VALIDATION` — 정적 검사, 관련 테스트, Godot headless/사람/기기 증거를 분리해 실행 또는 `NOT_RUN`으로 기록한다.
10. `INDEPENDENT_REVIEW` — 코드리뷰와 적대적 검토로 권한 원본 중복, Base/프로젝트 책임 침범, 보호 경로 변경, legacy surface 부활, 근거 없는 성숙도 상승을 확인한다.
11. `MERGE_AND_SYNC` — 필수 Gate가 통과하면 병합하고, 병합된 main을 기준으로만 repository와 적용 가능한 Notion destination을 재조회한다.
12. `GATE_CLOSE` — Critical Gate와 P0/P1을 별도로 판정하고, 다음 작업·미검증·보류를 남긴다. 평균 점수로 차단 문제를 가리지 않는다.

## 4. 필수 복원·감사 산출물

각 프로젝트는 Base 템플릿을 프로젝트 경로에 맞게 적용하고, 사실에는 링크·SHA·파일 경로를 붙인다.

| 산출물 | 최소 내용 | 정본 역할 |
| --- | --- | --- |
| Baseline Recovery Record | main SHA, 현재 Gate, 사실/가정/미결정, 보호 범위 | 감사 기준선 |
| Legacy Requirement Traceability | v6~v8 요구사항 → 현재 책임 원본 → 상태/이유 | 이관 추적 |
| Source / Consumer / Propagation Map | 정본, 소비자, 전파 대상, 책임자, 재조회 방법 | 영향도 지도 |
| Duplicate·Omission·Conflict Finding Ledger | ID, 심각도, 증거, 상태, 다음 Gate | 문제 관리 |
| Vertical Slice Readiness + Critical Gate | 플레이어 경험, 대표 화면, 검증 증거, 차단 Gate | 준비도 판정 |
| Approval Bundle + Change Plan | 승인 질문, 최소 변경, 제외 범위, 수용 기준, rollback | 후속 구현 계약 |

`P0`/`P1`, 보호 경로 변경, legacy surface의 무단 활성화, 근거 없는 성숙도 상승은 병합 후보가 아니다. `P2`/`P3`는 영향·소유자·다음 Gate를 남긴다.

## 5. Skill 선택과 책임 경계

Skill을 고정 이름 목록으로 실행하지 않는다. 현재 Registry와 프로젝트 스냅샷에서 문제에 필요한 최소 충분 능력을 선택하고 다음을 Evidence Pack에 기록한다.

```text
문제와 선택 이유 → 입력 정본 → 담당 Skill / mode → 산출물 → 검증 증거 → 소비처
```

- 공용 방법·검증 원리는 Base route만 사용한다. 공용 본문을 프로젝트에 복제하지 않는다.
- 프로젝트 특유의 게임 규칙·세계관·화면·데이터·검수는 실제 로컬 `SKILL.md` route가 담당한다.
- 같은 이름의 공용·로컬 Skill이 있으면 Snapshot의 `project_routes`를 우선하고, 없는 경우에만 Base route를 쓴다.
- route 중복, orphan, 순환 alias, 등록되지 않은 활성 Skill, 만료된 Base 핀은 실패 종료다.
- `running-adversarial-review-and-refinement`의 `repository-wide-audit`는 정본/소비처/보호 경로/구형 참조를 독립 검토한다. 별도 중복 Skill을 만들지 않는다.

## 6. INTERMEDIATE_VISUAL_CHECKPOINT — 기획 해석을 화면으로 검증하기

다음 발화가 있거나, 기획 해석 차이가 `P1` 위험이면 이 점검을 실행한다.

```text
중간 점검
예상 게임 화면 확인
UI를 포함한 화면으로 보여줘
```

현재 정본만 입력으로 사용해 **한 화면 흐름**의 예상 플레이 화면을 시뮬레이션한다. 이미지 생성 도구와 생성 권한이 있으면 `DRAFT_VISUAL` 이미지를 만들고, 없으면 같은 정보의 Screen Brief·텍스트 와이어프레임·Mermaid·Notion visual/flow 대체안을 만든다. 도구 부재는 실패가 아니다.

### Screen Brief 필수 입력

- 화면 목적, 플레이어의 첫 시선, 한 번에 할 주요 행동.
- 플랫폼·해상도·화면비·입력 방식.
- 상태, 위험·비용·보상, 성공·실패·복구 피드백.
- 정보 우선순위, 긴 한글, 터치·키보드·패드, 포커스·접근성 제약.
- 관련 Decision ID, 책임 정본, 확인된 사실, `MISSING_CANON` 미결정.
- 선택한 아트 방향과 비교 대안(최대 3개).

이미지/와이어프레임에는 사실로 가장된 추정 수치·텍스트·저작물·브랜드 요소를 넣지 않는다. 이미지 안 한글은 레이아웃 검토용이며 최종 텍스트 자산이 아니다.

### 결과의 권한과 검토

생성물은 `DRAFT_VISUAL` 기획 검토 자료다. 그것은 최종 게임 리소스, 저작권·라이선스 승인, 구현 명세 확정, Godot 구현 완료, 런타임/사람 검증 증거를 의미하지 않는다.

직후 `Screen Interpretation Review`를 작성한다.

1. 정본과 일치해 확인된 요소.
2. AI가 가정한 요소와 `MISSING_CANON`.
3. 기획에 맞지 않은 표현과 `VISUAL_CANONICAL_CONFLICT`.
4. 채택 검토 가치가 있는 UX 표현과 `TECHNICAL_REVIEW_PROPOSAL`.
5. 버려야 할 표현과 이유.

사용자 Decision 없이는 이미지를 정본으로 승격하거나 구현 범위를 바꾸지 않는다. 사용자가 고른 결과만 Visual Artifact Registry에 책임 문서·Decision ID·스냅샷·링크와 함께 `APPROVED_VISUAL_REFERENCE` **후보**로 기록한다.

## 7. Notion·Mermaid와 legacy compatibility surface의 경계

현재 사람용 작업면은 `NOTION_HUMAN_FACING_CANON`, 구조화·구현 사실은 `REPOSITORY_STRUCTURED_CANON`/runtime owner다. Mermaid 같은 source-derived flow는 Project Notion Home에서 사람에게 직접 보이는 흐름/시스템 표현을 지원할 수 있지만, 규칙·수치·runtime proof를 소유하지 않는다.

```text
Notion Project Home / Flow / Visual / human table → 사람이 읽고 비교·수정하는 현재 표현
Mermaid / source-derived flow → 루프, 관계, 분기, 여정, 시스템 맵의 보조 표현
GitHub Markdown·JSON → 규칙, 승인 결정, 구현 계약, 변경 이력의 structured canon
Godot + tests → 실제 구현과 검증 증거
```

Google Sheets와 Figma는 migration-only historical surface다. 기존 Figma·Whimsical·Google Sheets에 unique material이나 사용자가 제공한 reference가 있을 때만 `COMPATIBILITY_ONLY` / `REFERENCE_ONLY`로 분류하고, 올바른 Notion 또는 repository owner에 이관한 뒤 destination readback한다. 새로 생성·작성·동기화·필수 Gate로 요구하지 않으며, legacy Sheet 단독 변경은 언제나 `PROPOSED_SHEET_CHANGE`다.

## 8. Vertical Slice 계약과 검증 증거

버티컬 슬라이스는 기능 목록이 아니라 플레이어가 약속을 경험하는 최소의 검증 가능한 대표 구간이다.

```text
Intent → Player Experience → Scope → Implementation Contract → Verification → Documentation
```

각 Slice는 핵심 루프, 대표 장면/화면, 선택과 결과, 실패/복구, 저장/재진입 필요성, 접근성·성능 위험, 콘텐츠 생산 비용, 완료 증거를 명시한다. `DEMO_FIRST_VERTICAL_SLICE`, `DEMO_VALIDATION`, `TECHNICAL_SPIKE`는 현재 프로젝트 상태에 맞게만 선택한다.

운영 성숙도 `OM-L0..L5`와 제품 증거 `PE-0..PE-5`는 평균내지 않는다. Godot 실행, 실기기, 접근성, 사람 검증은 실제 증거 전까지 `NOT_RUN`이며, Godot 프로젝트가 없는 저장소는 `NOT_APPLICABLE_NO_PROJECT`로만 표시한다.

## 9. GitHub·Goal·PR·자동 병합

구현 또는 문서 변경 작업은 GitHub Issue에 근거한다. Goal 첫 줄은 정확히 아래 문장으로 시작한다.

```text
/goal Implement GitHub Issue #[NUMBER] exactly as specified.
```

작업이 다중 파일·고위험·불명확하면 `/plan` 후 Goal을 만든다. Base와 각 프로젝트는 별도 Issue·Goal·격리 브랜치·PR을 사용한다.

정적 검증, 독립 코드리뷰, 적대적 검토가 통과하고 P0/P1·미해결 review·보호 경로 변경·미승인 정본 덮어쓰기·근거 없는 성숙도 상승이 없으면 `AUTO_MERGE_AFTER_REQUIRED_CHECKS` 및 `AGENT_MERGE_REQUIRED`에 따라 병합한다. 그렇지 않으면 자동 병합하지 않는다.

## 10. 완료 보고와 후속 Change Plan

감사 전용 파동의 완료는 “감사 결과, 중간 시각화 검토, 승인 가능한 보완 계획이 책임 정본에 연결됨”이다. `INTEGRATED_DELIVERY_PROFILE`의 완료는 이보다 더 나아가 승인된 기획·Codex 인계·구현·검수·병합 후 repository와 적용 가능한 Notion destination readback까지, **이번 요청에 실제로 포함된 단계**의 증거를 남긴 상태다. 실행하지 않은 게임 구현·런타임·사람 검증을 주장하지 않는다.

완료 보고는 다음을 구분한다.

- **Confirmed:** 정본·main·실제 파일로 확인한 사실.
- **Implemented:** 이번 계약/감사 파동에서 추가한 문서와 검증기.
- **Verified:** 실행한 테스트와 근거.
- **Assumed / Undecided:** 사용자 Decision 또는 외부 증거가 필요한 항목.
- **Recommended next action:** P0/P1 해소, 별도 Issue, 다음 Gate.

모든 후속 Change Plan은 변경 대상·제외 범위·소비처·테스트·Godot 수동 검증·repository/Notion readback 조건과, 적용 시 legacy migration 경계를 포함한다.
