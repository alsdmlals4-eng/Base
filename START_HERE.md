# Base 시작 지점

이 문서는 새 채팅, 새 GPT, 새 Codex 또는 새 작업자가 `Base`를 프로젝트 작업에 적용할 때 사용하는 최상위 라우터다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일을 무작정 읽는 뜻이 아니다. 현재 작업에 필요한 책임 원본과 최소 스킬 집합을 Registry와 Documentation Map에서 선별한다.

```text
Base START_HERE
→ Base AGENTS
→ Base Documentation Map
→ Base Skill Registry
→ 대상 프로젝트 AGENTS
→ 루트 [기획서]/00_프로젝트_허브/START_HERE
→ Active Context·Documentation Map·Development Gates
→ Design Document Registry·Skill Registry
→ 현재 분야의 Markdown 또는 JSON 책임 원본·필요한 스킬
→ 사람 검토가 필요하면 DOCX/PDF·다이어그램·승인 이미지
→ 실제 코드·데이터·자산·테스트
```

저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.

### Base 저장소 자체를 콜드 스타트할 때

`Base`는 프로젝트 운영 키트의 공용 원본이므로 프로젝트 전용 `ACTIVE_CONTEXT.md`, `DEVELOPMENT_GATES.md`, `ROADMAP.md`, `INTERVIEW_REGISTRY.json`을 활성 파일로 두지 않는다. 이 경로들은 `templates/project-operations/`에서 대상 프로젝트에 설치하는 템플릿이다.

Base 자체의 현재 상태는 다음 책임 원본에서 찾는다.

```text
확정된 운영 계약 → AGENTS.md·START_HERE.md·docs/DOCUMENTATION_MAP.md
완료된 변경 → docs/CHANGELOG.md
활성 스킬 → skills/SKILL_REGISTRY.json
검토 대기 작업 → [수정제안서]/PROPOSAL_REGISTRY.json·개별 PROPOSAL.md
진행 중 구현 → GitHub PR·Actions
현재 인터뷰 → Base 변경 인터뷰가 실제 등록된 경우에만 해당 Registry·기록
```

활성 Base 인터뷰가 없으면 `등록 없음`, 제출된 제안의 우선순위가 승인되지 않았으면 `사용자 검토 대기·우선순위 미확정`으로 답한다. 프로젝트용 상태 파일이 Base 루트에 없다는 이유만으로 결함이나 누락으로 판정하지 않는다.

## 루트 기획서 위치

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 바로 아래에 둔다.

```text
<repository-root>/[기획서]/
```

`docs/[기획서]`, `src/[기획서]` 같은 중첩 위치에 별도 현행 기획서를 만들지 않는다. 운영 중인 기존 프로젝트의 안정된 경로는 감사와 사용자 승인 없이 강제로 이동하지 않는다.

## 기획서 책임 구조

### AI·자동 검사

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 프로젝트 종합·분야별 Markdown 또는 JSON 책임 원본
→ 실제 코드·데이터·자산·테스트 경로
```

### 사람 열람

```text
기획서 PDF
→ 기본 최신 열람본

기획서 DOCX
→ 문서 형식 검토용 파생본

기획서.assets/
→ 자동 다이어그램·승인 이미지·실제 캡처
```

### 최신성

```text
기획서_PUBLICATION_MANIFEST.json
→ JSON·생성기·DOCX·PDF·다이어그램·승인 이미지 해시
```

서술 중심 기획은 Markdown을 기본 책임 원본으로, Registry·Manifest·상태·ID·경로·게임 데이터는 JSON으로 관리한다. 각 문서는 단일 책임 원본만 가지며 PDF는 항상 동기화한다. DOCX와 다이어그램은 선택 파생본이다.

`START_HERE`, `ACTIVE_CONTEXT`, `DOCUMENTATION_MAP`, 작업 절차와 Skill처럼 빠른 라우팅이 필요한 운영 문서는 Markdown을 유지할 수 있다.

## 프로젝트 스킬맵 구조

```text
SKILL_REGISTRY.json
→ AI가 trigger·상태·경로를 판독

PROJECT_SKILL_MAP.pdf
→ 사람이 가장 먼저 보는 이미지 포함 최신본

PROJECT_SKILL_MAP.md 또는 PROJECT_SKILL_MAP.docx
→ 문서 검토용 파생본

PROJECT_SKILL_MAP.assets/
→ 호출 흐름·분야 라우팅·상태 매트릭스
```

`PROJECT_SKILL_MAP.md`는 설정한 프로젝트에서만 자동 생성하며 수동 책임 원본으로 사용하지 않는다.

## 요청별 라우팅

### 새 요청의 분야·스킬 판정

- 실행 스킬: `skills/routing-project-work-by-discipline/SKILL.md`
- 기계 판독 라우터: `skills/SKILL_REGISTRY.json`

L1 이상 작업은 주 책임 분야 하나, 영향 분야, 변경 유형과 현재 단계에서 필요한 최소 Foundation·분야 스킬만 선택한다.

기능·게임 경험·아트 방향·구조·워크플로·Base 변경 제안은 `conducting-deep-requirement-interviews`를 먼저 적용한다. 저장소 사실을 조사한 뒤 사용자 결정만 질문하고, 마지막 재진술 확인 전에는 실행 프롬프트나 구현으로 넘어가지 않는다. 오탈자·명확한 단일 파일 기계 수정·동일 검사 재실행은 예외다.

Godot 또는 Web UI 결과 감사는 `auditing-and-refining-ui-art`를 사용한다. 정적 검사는 A~E 후보만 보고하며, 사용자 승인 전에는 대상 UI를 수정하지 않는다. 승인 후 순차 개선하고 새 검사 컨텍스트와 실제 렌더로 전후를 재검수한다.

금지:

- 전체 skills 폴더 기본 로드
- trigger와 무관한 스킬 호출
- 같은 책임의 중복 스킬 호출
- 검증·발행·Handoff 스킬의 조기 호출
- `[보류]`, `[백업]`, `[제거 후보]` 스킬 호출

### 새 프로젝트 또는 운영체계 미설치

`skills/installing-game-project-operating-system/SKILL.md`를 사용한다.

설치 목표:

- 루트 `[기획서]`와 공통 시작 문서
- `DESIGN_DOCUMENT_REGISTRY.json`
- `INTERVIEW_REGISTRY.json`, `INTERVIEWS/`, `EXECUTABLE_PROMPTS/`
- 프로젝트 종합·분야별 Markdown 또는 JSON 책임 원본
- Markdown 또는 JSON 책임 원본에서 생성한 최신 PDF·Manifest와 선택 DOCX·다이어그램·승인 이미지 구조
- `SKILL_REGISTRY.json`과 사람용 필수 스킬맵 PDF·선택 Markdown/DOCX/assets
- Development Gates·Roadmap·Active Context
- 분야별 프로젝트 스킬·Learning Log
- GitHub Governance 검사와 Required Check 준비
- 새 AI의 콜드 스타트 복원

### 운영 중인 기존 프로젝트의 구조 검수·재배치

`skills/migrating-existing-game-project-structure/SKILL.md`를 사용한다.

첫 단계는 `Audit only`다.

```text
기존 내용 보존
→ Markdown·문서·자산·코드·참조 감사
→ 보존하거나 승인할 Markdown/JSON 책임 구조와 발행 구조 제안
→ 변경 전후 보존 대조
→ 사용자 승인
→ 승인 범위만 마이그레이션
→ DOCX/PDF·링크·스킬·콜드 스타트 검증
→ 기존 본책은 제거 후보로 별도 승인
```

### 일반 작업

```text
프로젝트 AGENTS
→ 루트 [기획서]/00_프로젝트_허브/START_HERE
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야의 Markdown 또는 JSON 책임 원본
→ SKILL_REGISTRY.json
→ 필요한 Foundation + 분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 파일·자산·테스트
```

변경 후 `DOCUMENT_UPDATE_MATRIX.md`로 영향 범위를 확인한다.

### 분야별 기획서 생성·갱신

- 실행 스킬: `skills/publishing-discipline-bibles/SKILL.md`
- 방법: `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`
- JSON 템플릿: `templates/project-operations/DESIGN_DOCUMENT.json`
- Registry 템플릿: `templates/project-operations/DESIGN_DOCUMENT_REGISTRY.json`
- 생성기: `tools/build_design_documents.py`

```text
책임 원본·승인 이미지·Mermaid
→ 자동 다이어그램
→ DOCX
→ PDF
→ 전 페이지 렌더 검수
→ Publication Manifest
→ Governance 검사
```

### 분야별 스킬 생성·학습

- 실행 스킬: `skills/evolving-project-discipline-skills/SKILL.md`
- 방법: `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md`
- AI Registry: `templates/project-operations/SKILL_REGISTRY.json`
- 사람용 출력: 필수 `PROJECT_SKILL_MAP.pdf`, 선택 `PROJECT_SKILL_MAP.md/.docx/.assets`

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출은 Learning Log에 기록한다. 사소한 성공 호출은 기록을 강제하지 않으며 스킬 본문은 반복 검증된 근거가 있을 때만 갱신한다.

### 프로젝트 교훈의 Base 승격

- 제안 생성: `skills/promoting-project-knowledge/SKILL.md`
- 제안 위치: `[수정제안서]/`
- 승인 후 구현: `skills/reviewing-and-implementing-base-change-proposals/SKILL.md`

프로젝트발 승격 후보는 제안 전용 PR에 먼저 보존한다. 사용자가 제안서를 검토하고 구현을 명시적으로 승인한 뒤에만 별도 PR에서 활성 Base를 변경한다. 사용자가 직접 승인한 Base 변경 요청은 별도 제안서 없이 작업 계약이 될 수 있다.

### Active Context·Handoff

`skills/maintaining-project-context-and-handoff/SKILL.md`를 사용한다. 현재 상태, 다음 작업, 위험과 읽기 순서만 압축하고 등록된 책임 원본의 전문을 복제하지 않는다.

### 운영체계 Health Review

`skills/verifying-game-project-operating-system/SKILL.md`를 사용한다.

호출 시점:

- 설치·마이그레이션 직후
- 본책·스킬·생성기·자동화의 큰 변경 후
- Vertical Slice·Production·Alpha·Beta·Release Candidate 전
- 새 채팅이 문서·스킬을 찾지 못할 때
- JSON·구현·자산·DOCX/PDF·검증 불일치가 의심될 때

## 선택 가능한 책임 분야 카탈로그

1. 설정·내러티브
2. 게임 디자인
3. UX·UI·접근성
4. 개발·엔지니어링
5. 테크니컬 아트·콘텐츠 파이프라인
6. 아트
7. 사운드
8. QA
9. 프로덕션·PM
10. 분석·유저리서치
11. 통합검수

프로젝트에 실제로 필요한 분야만 선택한다. 작은 프로젝트는 본책과 진입 스킬을 통합할 수 있으며 선택한 책임은 `responsibility_coverage`와 통합 책임자에서 추적한다. 11개 분야 전체를 일률적으로 설치하지 않는다.

## 작업 시작 계약

```yaml
primary_discipline:
affected_disciplines:
change_type:
goal:
scope:
out_of_scope:
protected_paths:
required_design_document_ids:
foundation_skills:
discipline_skills:
deferred_skills:
asset_impact:
publication_impact:
acceptance_criteria:
validation:
```

## 작업 종료 계약

1. 실제 결과와 승인·구현·검증 상태를 일치시킨다.
2. 관련 Markdown 또는 JSON 책임 원본과 Design Document Registry를 갱신한다.
3. 관련 스킬·Skill Registry·Learning Log를 갱신한다.
4. 책임 원본 또는 승인 이미지가 바뀌면 PDF·Manifest와 선언한 선택 DOCX·다이어그램을 재생성한다.
5. Active Context·Roadmap·Development Gates·Documentation Map을 확인한다.
6. 실행한 검증과 미검증을 분리한다.
7. 다음 작업과 선행 조건을 기록한다.
8. 새 작업자가 저장소만으로 방향·상태·기획서·스킬·검증을 찾는지 확인한다.

## 이미지 계약

- 활성 항목에는 캐노니컬 경로 하나만 사용한다.
- 기존 승인 이미지가 있으면 사용자 지시 없이 새 시안을 만들지 않는다.
- 콘셉트·방향 승인·제작 준비·구현·실제 화면 검증을 구분한다.
- 채택 요소와 비채택 요소를 JSON에 기록한다.
- 이전 버전은 Git 이력으로 보존한다.

## 중요한 한계

Base를 참고하라는 문장만으로 GitHub 파일이 스스로 바뀌지는 않는다. AI가 대상 저장소에 읽기·쓰기 권한을 가지고 실제 작업을 실행해야 한다. 자동 검사는 구조·해시·누락·렌더 실패를 탐지하지만 재미, 방향 적합성, 이미지 품질과 사용자 승인까지 대신하지 않는다.
