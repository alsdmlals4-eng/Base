# Ten Paces Knowledge Promotion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 십보강호 문서 작업에서 확인한 재사용 가능한 기획·서사형 정보 표현·Vertical Slice·문서 책임 분리 노하우를 Base의 현행 method·skill·case에 사례로 반영하고 프로젝트에 승격 결과를 역기록한다.

**Architecture:** 프로젝트 고유 수치·문파명·파일 경로는 사례의 출처 맥락에만 제한하고, 공용 원리는 Base의 기존 책임 원본에 최소 변경으로 통합한다. 독립 사례 두 건을 추가하고 관련 method·skill에는 짧은 적용 사례와 사례 링크를 넣는다. Base 반영을 먼저 완료한 뒤 확정 커밋을 프로젝트의 Base 버전·학습 기록에 동기화한다.

**Tech Stack:** Markdown, GitHub Contents API, GitHub branch/PR workflow.

## Global Constraints

- 십보강호의 활성 수치·세계관·문파·무공·Godot 경로를 Base 공용 규칙으로 복사하지 않는다.
- 구현·플레이테스트가 없는 내용은 `검증`으로 표시하지 않는다.
- 기존 책임 문서를 직접 갱신하고 `v2`, `final`, `latest` 복제본을 만들지 않는다.
- 모든 신규 사례는 문제·대안·결정·위험·검증·재사용 조건·비사용 조건을 포함한다.
- Base와 프로젝트 변경은 각각 격리 브랜치에서 수행하고 검증 뒤 PR로 병합한다.

---

### Task 1: 문서 감사 결과와 승격 경계 고정

**Files:**
- Read: `alsdmlals4-eng/Ten-Paces-Hidden-Moves/docs/**`
- Read: `docs/CONTENT_DESIGN_METHOD.md`
- Read: `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md`
- Read: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- Read: `docs/knowledge/methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- Read: `skills/writing-game-design-documents/SKILL.md`
- Read: `skills/designing-vertical-slices/SKILL.md`
- Read: `docs/knowledge/cases/DIEGETIC_OPPONENT_INFORMATION_CASE.md`

**Interfaces:**
- Consumes: 십보강호의 활성·보류·백업 문서와 Base v1.9.2 현행 책임 원본.
- Produces: 공용으로 승격할 네 가지 원리와 프로젝트에 남길 고유 요소의 분리표.

- [ ] 십보강호 `docs`의 활성 17개, 백업 4개, 보류 2개, 프로젝트 스킬 1개, Superpowers Plan 1개를 확인한다.
- [ ] 다음 승격 후보를 기존 Base와 대조한다.
  1. 규칙→UI→연출→QA의 동일 순서 추적성.
  2. 내부 의미 키→세계관 문구→정보 단계 구체화의 카피 계약.
  3. 하이라이트 기능을 강조하되 완주 필수 게이트로 만들지 않는 Vertical Slice 설계.
  4. 과적재된 기획 문서를 질문별 책임 원본으로 분리하고 콜드 스타트로 검증하는 방법.
- [ ] 백업의 6슬롯·9전·1~5성 구조와 보류의 문파별 성과 평가를 반례로만 사용하고 현행 규칙으로 승격하지 않는다.
- [ ] 상태를 `문서 구조 채택·구현 전 검증 필요`로 고정한다.

### Task 2: 기획·연출 추적성 사례 작성

**Files:**
- Create: `docs/knowledge/cases/TEN_PACES_RULE_PRESENTATION_TRACEABILITY_CASE.md`
- Modify: `docs/knowledge/cases/README.md`

**Interfaces:**
- Produces: 규칙 해상 순서, UI 정보 순서, 연출 재생 순서, QA 관찰 순서를 같은 의미 단계로 연결하는 사례.

- [ ] 사례에 문제, 기존 혼합 문서의 위험, 검토 대안, 채택 구조, 상태 소유 경계, 검증 방법을 작성한다.
- [ ] `규칙 원본 → 구조화 결과 → 프레젠테이션 → 사용자 설명 가능성 테스트` 흐름을 공용 형태로 제시한다.
- [ ] 프레젠테이션이 결과를 재계산하거나 저장을 소유하지 않는 실패 기준을 포함한다.
- [ ] 프로젝트 고유 수치와 무공 이름은 `그대로 복사하면 안 되는 요소`에만 기록한다.
- [ ] 사례 인덱스의 Base·프로젝트 학습 순환 사례와 문제별 라우팅에 연결한다.

### Task 3: 선택적 하이라이트 Vertical Slice 사례 작성

**Files:**
- Create: `docs/knowledge/cases/TEN_PACES_OPTIONAL_HIGHLIGHT_VERTICAL_SLICE_CASE.md`
- Modify: `docs/knowledge/cases/README.md`

**Interfaces:**
- Produces: 희귀·상위 하이라이트를 목표로 제시하면서 미획득 경로도 완결시키는 Vertical Slice 사례.

- [ ] `하이라이트 보유 경로`와 `미보유 정상 경로`를 동시에 완료 기준에 넣은 이유를 작성한다.
- [ ] 검토 대안으로 `하이라이트 필수`, `하이라이트 제거`, `선택적 하이라이트`를 비교한다.
- [ ] 하이라이트 체험률, 완주율, 실패 원인, 반복 동기를 검증 항목으로 정의한다.
- [ ] 스토리 프로젝트에도 적용할 수 있도록 `특수 능력·관계 장면·반전·보너스 결말`로 일반화한다.
- [ ] 하이라이트가 핵심 약속 자체인 프로젝트에는 적용하지 않는 비사용 조건을 명시한다.

### Task 4: 기획 method에 프로젝트 유래 사례 반영

**Files:**
- Modify: `docs/CONTENT_DESIGN_METHOD.md`
- Modify: `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md`

**Interfaces:**
- Consumes: Task 2·3 사례.
- Produces: 콘텐츠 기획과 책임 문서 설계에서 바로 참고할 짧은 사례 섹션.

- [ ] `CONTENT_DESIGN_METHOD.md`에 `사례 — 선택적 하이라이트를 완주 게이트와 분리` 절을 추가한다.
- [ ] 하이라이트의 감정적 가치, 정상 경로, 검증 지표를 3단 구조로 적는다.
- [ ] `PLANNING_SYSTEM_METHOD.md`에 `사례 — 규칙·UI·연출·QA의 추적성` 절을 추가한다.
- [ ] 동일 전문 복사가 아니라 각 책임 문서가 같은 의미 단계와 원본 링크를 공유하는 방식으로 설명한다.
- [ ] 두 절에서 신규 사례 문서를 링크한다.

### Task 5: 서사·대화 method에 정보 카피 사례 반영

**Files:**
- Modify: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- Modify: `docs/knowledge/methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- Modify: `docs/knowledge/cases/DIEGETIC_OPPONENT_INFORMATION_CASE.md`

**Interfaces:**
- Produces: 내부 상태를 세계관 문구로 표현할 때의 대사·카피 작성 순서와 단계별 구체화 사례.

- [ ] `NARRATIVE_AND_RELATIONSHIP_METHOD.md`에 `사례 — 수치를 말하지 않고 같은 사실을 더 구체적으로 말하기` 절을 추가한다.
- [ ] 기능 대화·세계관 대화의 경계를 유지하며, 문구가 선택 근거를 제공하되 정답을 대신하지 않게 한다.
- [ ] `DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`에 `의미 키 기반 정보 문구` 사례를 추가한다.
- [ ] 최초 정보, 반복 정보, 정탐·상세 정보의 문장 역할과 금지 패턴을 구분한다.
- [ ] 기존 diegetic case에 `문구 작성 절차`와 `대화·현지화 검수`를 보강한다.

### Task 6: 실행 스킬에 실제 적용 사례 반영

**Files:**
- Modify: `skills/writing-game-design-documents/SKILL.md`
- Modify: `skills/designing-vertical-slices/SKILL.md`

**Interfaces:**
- Produces: 스킬 사용자가 프로젝트 사례를 따라 수행할 수 있는 짧은 사례와 검수 질문.

- [ ] 기획서 작성 스킬에 `사례 — UI 문서에서 연출 책임을 분리`를 추가한다.
- [ ] 분리 전 문제, 책임 원본 결정, 동기화 대상, 콜드 스타트 검수 순서를 적는다.
- [ ] Vertical Slice 스킬에 `사례 — 선택적 하이라이트와 정상 완주 경로`를 추가한다.
- [ ] 특수 기능 보유·미보유 양쪽을 테스트하는 완료 기준을 명시한다.
- [ ] 각 스킬에서 관련 사례 문서를 링크한다.

### Task 7: Base 라우팅·버전 갱신

**Files:**
- Modify: `README.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `docs/knowledge/README.md`
- Modify: `docs/CHANGELOG.md`

**Interfaces:**
- Produces: 신규 사례와 보강된 method·skill을 찾을 수 있는 Base v1.9.3 라우팅.

- [ ] README의 주요 사례 라우팅에 신규 두 사례를 추가한다.
- [ ] Documentation Map의 기획·서사·연출·Vertical Slice 작업에 사례 링크를 연결한다.
- [ ] knowledge README에 신규 사례의 지식 상태와 재검증 조건을 기록한다.
- [ ] Changelog 최상단에 `v1.9.3 - planning, dialogue and vertical-slice applied cases`를 추가한다.
- [ ] 구현·플레이 검증 전임을 명시하고 스킬 자체의 검증 상태를 과장하지 않는다.

### Task 8: Base 정적 검증과 병합

**Files:**
- Verify: Base branch diff.

**Interfaces:**
- Produces: 병합 가능한 Base 문서 변경과 확정 커밋 SHA.

- [ ] main 대비 변경 파일 목록을 확인한다.
- [ ] 신규 사례 두 파일이 인덱스, method, skill, Documentation Map에서 모두 연결되는지 확인한다.
- [ ] Base 문서에서 프로젝트 고유 수치·문파명·Godot 경로가 공용 규칙으로 단정되지 않았는지 검수한다.
- [ ] `검증`, `완료`, `구현됨` 표현을 찾아 실제 근거 없는 과장이 없는지 확인한다.
- [ ] Base PR을 생성하고 문서 변경 요약·검증·미검증 항목을 본문에 기록한다.
- [ ] PR을 squash merge하고 확정 Base 커밋 SHA를 기록한다.

### Task 9: 십보강호 프로젝트에 승격 결과 역기록

**Files:**
- Modify: `docs/11_BASE_ADOPTION_AND_LEARNING_LOG.md`
- Modify: `docs/BASE_RULES_VERSION.md`
- Verify: `docs/DOCUMENTATION_MAP.md`

**Interfaces:**
- Consumes: Task 8의 Base v1.9.3 확정 커밋.
- Produces: 프로젝트가 참조할 최신 Base 버전과 승격·미검증 기록.

- [ ] 학습 기록에 신규 사례, 갱신 method·skill, 프로젝트 전용으로 남긴 항목을 구분해 추가한다.
- [ ] 실제 구현·플레이 검증은 여전히 미완료임을 유지한다.
- [ ] Base 버전과 기준 커밋을 v1.9.3 확정 SHA로 갱신한다.
- [ ] Documentation Map의 기존 Base 동기화 경로가 유효한지 확인한다.
- [ ] 프로젝트 PR을 생성하고 Base PR·커밋을 연결한다.
- [ ] 프로젝트 PR을 squash merge한다.

## Plan Self-Review

- 모든 사용자 요구는 Task 2~7의 기획 사례, 대화 사례, 스킬 사례와 Task 9의 역기록에 배정했다.
- 프로젝트 고유 정보는 사례 출처와 금지 복사 항목 외에 공용 규칙으로 사용하지 않는다.
- 새 사례는 두 건으로 제한하고 기존 diegetic case를 보강해 중복을 줄인다.
- 문서 전용 작업이므로 실행 테스트 대신 링크·상태·중복·표현·브랜치 diff를 검증한다.
