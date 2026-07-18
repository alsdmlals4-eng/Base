# Base 시작 지점

이 문서는 새 채팅, 새 GPT, 새 Codex 또는 새 작업자가 `Base`를 프로젝트 작업에 적용할 때 사용하는 최상위 라우터다.

## 사용자가 기억할 최소 요청

다음처럼 요청하면 된다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

저장소 접근이 가능한 AI는 파일을 무작정 전부 읽거나 Base를 통째로 복사하지 않는다. 현재 작업에 필요한 공용 책임 원본을 선별하고 대상 프로젝트의 현행 상태와 함께 확인한다.

```text
Base/START_HERE.md
→ Base/AGENTS.md
→ Base/docs/DOCUMENTATION_MAP.md
→ 대상 프로젝트 AGENTS.md
→ 대상 프로젝트 START_HERE·Documentation Map·Active Context
→ 프로젝트 DEVELOPMENT_GATES·PROJECT_SKILL_MAP
→ 현재 작업의 분야 본책·분야 스킬
→ 실제 파일·데이터·자산·테스트
→ 필요한 Base method·skill·template·case
```

대상 프로젝트 저장소가 명확하지 않으면 먼저 저장소를 식별한다. 저장소 접근 없이 설치·검수 완료를 주장하지 않는다.

## 요청별 라우팅

### 1. 새 프로젝트 또는 운영체계가 없는 프로젝트

`skills/installing-game-project-operating-system/SKILL.md`를 사용한다.

목표:

- GPT와 Codex가 같은 시작 문서를 읽는다.
- 분야별 활성 책임 원본이 고정된다.
- 변경 전에 주 책임 분야와 영향 분야를 판정한다.
- 개발 게이트와 완료 증거가 연결된다.
- 분야별 프로젝트 스킬과 foundation 스킬이 구분된다.
- 관련 본책·상태·Roadmap·검증 문서를 같은 작업에서 갱신한다.
- 이미지 승인 상태, 캐노니컬 경로와 실제 적용 상태를 구분한다.
- 분야 PDF가 책임 Markdown과 승인 이미지에서 생성된다.
- PR에서 문서·이미지·스킬·PDF 갱신 누락을 검사할 수 있다.
- 새 AI가 과거 대화 없이 저장소만으로 현재 상태를 복원한다.

### 2. 이미 운영 중인 기존 프로젝트의 구조 검수·재배치

`skills/migrating-existing-game-project-structure/SKILL.md`를 사용한다.

첫 단계는 `Audit only`다. 사용자 승인 전에는 대량 삭제·이동·통합·강제 개명을 수행하지 않는다.

```text
기존 내용 보존
→ 책임·참조 조사
→ 중복·충돌·누락 분석
→ 변경 전후 보존 대조가 포함된 제안
→ 사용자 승인
→ 승인 범위만 변경
→ 링크·PDF·스킬·콜드 스타트 검증
```

### 3. 이미 운영체계가 설치된 프로젝트의 일반 작업

```text
프로젝트 AGENTS.md
→ START_HERE.md
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ 현재 작업의 분야 본책
→ PROJECT_SKILL_MAP.md의 foundation + 분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 파일·자산·테스트
```

그 후 `DOCUMENT_UPDATE_MATRIX.md`로 변경 영향을 판정한다.

### 4. 개발 단계·작업 완료 게이트 설계·검수

- 방법: `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`
- 프로젝트 템플릿: `templates/project-operations/DEVELOPMENT_GATES.md`
- Vertical Slice 상세: `skills/designing-vertical-slices/SKILL.md`

작업 실행 게이트와 Concept·Prototype·Vertical Slice·Alpha·Beta 같은 제품 마일스톤 게이트를 구분한다.

### 5. 분야별 프로젝트 스킬 생성·통합·학습

- 실행 스킬: `skills/evolving-project-discipline-skills/SKILL.md`
- 방법: `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md`
- 지도: `templates/project-operations/PROJECT_SKILL_MAP.md`

공용 절차는 foundation에 한 번만 두고, 각 분야는 실제 책임 문서·경로·산출물·검증을 가진 독립 프로젝트 스킬로 분화한다.

### 6. 분야별 최신 PDF 발행·검수

- 실행 스킬: `skills/publishing-discipline-bibles/SKILL.md`
- 방법: `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md`
- 발행 계획: `templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md`
- 최신성 기록: `templates/project-operations/PUBLICATION_MANIFEST.json`

PDF는 단순 요약이 아니라 해당 분야의 목적, 전체 작업 흐름, 승인 결정, 실제 경로, 승인 이미지, 구현·검증 상태와 다음 작업을 한눈에 볼 수 있는 읽기 전용 통합본이다.

### 7. 특정 기획·개발 작업

`docs/DOCUMENTATION_MAP.md`에서 작업에 맞는 method·skill·template을 선택한다. Base 전체를 프로젝트에 복사하지 않고 현재 작업에 필요한 공용 규칙만 프로젝트에 분화한다.

### 8. Base 자체 갱신

```text
START_HERE.md
→ README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 변경 대상 책임 원본
→ 관련 skill·template·case
→ docs/CHANGELOG.md
```

프로젝트 고유 이름, 수치, 세계관, 실제 경로와 미검증 결과는 Base 공용 규칙으로 승격하지 않는다.

## 게임 프로젝트 운영체계의 기본 분야

프로젝트 규모에 따라 통합하거나 분리할 수 있지만 책임은 누락하지 않는다.

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

**테크니컬 아트(Technical Art)**: 아트 자산을 엔진에 안정적으로 적용하기 위해 제작 규격, Import, 도구, 성능과 시각 품질을 연결하는 분야다.

**통합검수(Integrated Review)**: 개별 버그를 찾는 QA를 넘어 기획·구현·이미지·사운드·검증·일정이 서로 일치하는지 확인하는 최종 품질 게이트다.

## 상태 언어와 수명주기

| 상태 | 의미 |
|---|---|
| 확정 | 사용자 또는 책임자가 방향·규칙을 승인함 |
| 구현 | 코드·Scene·데이터·자산에 존재함 |
| 검증 | 테스트·실행·플레이 또는 실제 캡처로 확인함 |
| 진행 중 | 일부 구현 또는 일부 검증 상태 |
| 가설 | PoC·사용자 테스트·조사가 필요함 |
| 미확정 | 아직 결정되지 않음 |
| 보류 | 의도적으로 활성 범위에서 제외함 |
| 대체됨 | 새 책임 원본이나 자산으로 교체됨 |
| 불일치 | 문서·구현·검증·자산이 서로 다름 |

수명주기 영역:

- `[현행]`: 기본 읽기 대상인 현재 책임 원본과 실행 스킬
- `[백업]`: 외부 원본·감사·승인 근거처럼 Git 이력만으로 부족한 자료
- `[보류]`: 재개 조건 전에는 구현하지 않는 미래 항목
- `[제거 후보]`: 보존·참조 검증과 승인 전에는 삭제하지 않는 후보

단순 이전 버전은 `[백업]` 복제본을 만들지 않고 Git 이력으로 보존한다. 문서가 존재한다는 사실을 구현 또는 검증 완료로 사용하지 않는다.

## 작업 시작 계약

모든 L1 이상 작업은 최소한 다음을 선언한다.

```yaml
primary_discipline:
affected_disciplines:
change_type:
goal:
scope:
out_of_scope:
protected_paths:
required_docs:
foundation_skills:
discipline_skills:
acceptance_criteria:
validation:
```

**영향도 분석(Impact Analysis)**: 한 변경이 어떤 시스템, 문서, 자산, 스킬과 테스트에 영향을 주는지 작업 전에 확인하는 절차다.

## 작업 종료 계약

작업은 다음이 끝나야 완료다.

1. 실제 결과와 승인·구현·검증 상태를 일치시킨다.
2. 관련 분야 본책, 프로젝트 스킬과 Active Context를 갱신한다.
3. Development Gate, Documentation Map과 변경 이력을 확인한다.
4. 이미지·사운드·데이터 Manifest 영향을 확인한다.
5. 책임 원본 또는 승인 이미지가 바뀌면 PDF·Publication Manifest 영향을 확인한다.
6. 실행한 검증과 미검증 항목을 분리한다.
7. 다음 작업과 선행 조건을 기록한다.
8. 프로젝트 고유 교훈과 Base 환류 후보를 분리한다.
9. 새 작업자가 10분 안에 방향·상태·분야 스킬·다음 작업·검증 경로를 찾는지 콜드 스타트 검수한다.

**콜드 스타트 검수(Cold-start Review)**: 과거 대화와 작성자의 설명 없이 새 작업자가 저장소만으로 작업을 재개할 수 있는지 확인하는 검수다.

## 이미지 계약

- 활성 항목에는 캐노니컬 경로 하나만 사용한다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 기존 승인 이미지가 있으면 사용자 지시 없이 새 시안을 만들지 않는다.
- 콘셉트, 방향 승인, 제작 준비, 구현, 실제 화면 검증을 구분한다.
- 이미지 전체를 승인하지 않고 채택 요소와 비채택 요소를 기록한다.
- 이전 버전은 Git 이력으로 보존한다.

**캐노니컬 경로(Canonical Path)**: 현재 공식 자료가 항상 존재하는 고정 파일 경로다.

## 사용자 열람 계약

- Markdown은 편집 가능한 단일 책임 원본이다.
- PDF·HTML·DOCX는 Markdown과 승인 이미지에서 생성하는 읽기 전용 파생본이다.
- 각 분야 PDF는 요약이 아니라 해당 분야의 전체 작업 과정, 승인 이미지, 현재 구현·검증과 다음 작업을 포함한다.
- Publication Manifest와 입력 해시로 최신성을 추적한다.
- 열람본을 별도 책임 원본으로 수동 수정하지 않는다.
- 각 본책 상단에는 요약, 상태, 갱신일, 기준 커밋, 최신 자료, 위험과 다음 작업을 둔다.
- 전문 용어는 처음 등장할 때 짧은 주석을 붙이고 전체 정의는 프로젝트 Glossary에서 관리한다.

## 중요한 한계

Base를 참고하라는 문장만으로 GitHub 파일이 스스로 바뀌지는 않는다. AI가 대상 저장소에 읽기·쓰기 권한을 가지고 실제 작업을 실행해야 한다. GitHub Actions와 PR 템플릿은 누락을 탐지할 수 있지만 재미, 방향 적합성, 이미지 품질, PDF의 최종 시각 품질과 사용자 승인까지 자동으로 대신할 수는 없다.
