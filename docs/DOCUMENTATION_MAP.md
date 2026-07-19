# Base 문서·스킬 역할표

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** 작업 원칙, Method, Skill, Template, Test와 일반화된 Case를 관리한다. 프로젝트의 세계관, 실제 수치, 구현 상태, 파일 경로, 승인 이미지와 테스트 결과는 프로젝트 저장소가 책임진다.

## 1. 최초 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업의 Method·Skill·Template·Test
→ 대상 프로젝트의 Registry·Markdown 또는 JSON 책임 원본·실제 파일
```

최소 호출문:

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

대상 프로젝트 읽기 순서:

```text
프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 분야 Markdown 또는 JSON 책임 원본
→ SKILL_REGISTRY.json
→ 현재 요청에 필요한 Foundation·분야 스킬
→ 사람 검토가 필요하면 DOCX/PDF·다이어그램·승인 이미지
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
```

저장소 전체나 전체 스킬을 무작정 읽지 않는다. 백업·보류·제거 후보는 감사·재개 요청이 없는 한 기본 읽기에서 제외한다.

## 2. 루트 기획서 계약

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 바로 아래에 둔다.

```text
<repository-root>/[기획서]/
```

`docs/[기획서]`, `src/[기획서]` 같은 중첩 현행 복제본을 만들지 않는다. 기존 프로젝트의 안정된 경로는 감사와 사용자 승인 없이 강제 이동하지 않는다.

## 3. 기획 본책의 책임 구조

### AI·자동 검사

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 프로젝트 종합 기획 책임 원본
→ 분야별 Markdown 또는 JSON 책임 원본
→ 실제 코드·데이터·자산·테스트
```

### 사람 열람

```text
기획서 PDF
→ 기본 최신 통합본

기획서 DOCX
→ 문서 형식 검토용 파생본

기획서.assets/
→ 자동 다이어그램·승인 이미지·실제 캡처
```

### 최신성

```text
기획서_PUBLICATION_MANIFEST.json
→ JSON·생성기·DOCX·PDF·다이어그램·승인 이미지 SHA-256
```

서술 중심 기획은 Markdown을 기본 책임 원본으로, Registry·Manifest·상태·ID·경로·게임 데이터는 JSON으로 관리한다. 각 문서는 하나의 책임 원본만 가지며 PDF는 항상 동기화한다.

## 4. 프로젝트 스킬맵

```text
SKILL_REGISTRY.json
→ AI 선택적 호출 책임 원본

PROJECT_SKILL_MAP.pdf
→ 사람이 보는 이미지 포함 최신본

PROJECT_SKILL_MAP.md 또는 PROJECT_SKILL_MAP.docx
→ 문서 검토용 파생본

PROJECT_SKILL_MAP.assets/
→ 호출 흐름·분야 라우팅·상태 매트릭스
```

`PROJECT_SKILL_MAP.md`는 설정한 경우 자동 생성하며 수동 책임 원본으로 사용하지 않는다.

## 5. 최상위 지속성 계약

새 채팅과 새 AI는 저장소만으로 다음을 확인할 수 있어야 한다.

- 프로젝트 목적과 핵심 플레이어 경험
- 현재 개발 단계, 다음 게이트와 최우선 작업
- 승인·구현·검증·미확정·보류 상태
- 변경하면 안 되는 결정과 보호 경로
- 프로젝트 전체·분야별 Markdown 또는 JSON 책임 원본
- 사람용 최신 PDF·선택 DOCX와 승인 이미지
- 분야별 프로젝트 스킬과 최소 호출 스킬
- 실제 코드·데이터·자산·테스트 경로
- 작업 종료 갱신 대상, Learning Log와 Base 환류 경계

## 6. Base 공용 작업 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | Base URL 호출과 프로젝트 읽기 순서 |
| 공용 규칙 | `AGENTS.md` | 우선순위·보존·혼용 책임 원본·발행·검증·학습 |
| 저장소 개요 | `README.md` | 구조·Method·Skill·Template·Test 안내 |
| 문서·스킬 지도 | `docs/DOCUMENTATION_MAP.md` | 작업별 최소 읽기와 책임 원본 |
| Base Skill Registry | `skills/SKILL_REGISTRY.json` | 공용 스킬 trigger·상태·경로 |
| Base Skill Learning Log | `skills/SKILL_LEARNING_LOG.md` | 실행 결과·실패·갱신 판정 |
| Base 수정제안서 | `[수정제안서]/PROPOSAL_REGISTRY.json` | 프로젝트발 승격 후보·승인·구현 상태 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 시작·게이트·발행·종료 검수 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 버전·동기화 기준 |

## 7. 핵심 Method

| 질문 | Method |
|---|---|
| 프로젝트 허브·본책·스킬·이미지·GitHub를 어떻게 연결하는가? | `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` |
| 작업·제품 개발 게이트를 어떻게 판정하는가? | `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md` |
| 기존 프로젝트를 어떻게 안전하게 재배치하는가? | `docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` |
| 분야별 스킬을 어떻게 선택·학습·통합하는가? | `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md` |
| Markdown·JSON 기획서를 최신 PDF와 선택 파생본으로 어떻게 발행하는가? | `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md` |
| 전체 기획 계층과 추적성을 어떻게 설계하는가? | `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md` |
| 새 AI가 재개할 Handoff를 어떻게 만드는가? | `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` |

추가 분야 Method:

- 콘텐츠 기획: `docs/CONTENT_DESIGN_METHOD.md`
- 서사·관계: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 아트 방향: `docs/knowledge/methods/ART_DIRECTION_METHOD.md`
- 캐릭터·서사 아트: `docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- AI 아트 프롬프트: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- 애니메이션·전투 연출: `docs/knowledge/methods/ANIMATION_AND_PRESENTATION_METHOD.md`
- 대화·이벤트 연출: `docs/knowledge/methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- 조사·근거: `docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`

## 8. 실행 스킬

| 작업 | 스킬 | 호출 조건 |
|---|---|---|
| 주 책임 분야·최소 스킬 판정 | `routing-project-work-by-discipline` | L1 이상 새 요청·범위 변경·콜드 스타트 |
| 신규 운영체계 설치 | `installing-game-project-operating-system` | 신규·미설치 프로젝트 |
| 기존 프로젝트 안전 마이그레이션 | `migrating-existing-game-project-structure` | 기존 구조 전면 감사·재배치 |
| 분야별 스킬 생성·학습 | `evolving-project-discipline-skills` | 스킬 추가·중복·반복 실패·Registry 변경 |
| Markdown·JSON 기획서 PDF 발행 | `publishing-discipline-bibles` | 책임 원본·승인 이미지·Mermaid·생성기 변경 또는 stale |
| Active Context·Handoff | `maintaining-project-context-and-handoff` | 상태·다음 작업·게이트·위험 변경 |
| 운영체계 Health Review | `verifying-game-project-operating-system` | 설치·마이그레이션·주요 게이트·콜드 스타트 실패 |
| 실행 프롬프트 변환 | `transforming-requests-into-prompts` | 요청·범위·완료 기준이 모호함 |
| Vertical Slice 설계 | `designing-vertical-slices` | 대표 품질·제작 파이프라인 검증 |
| 기획 책임 구조 설계 | `writing-game-design-documents` | Registry·Markdown/JSON 책임 원본·Roadmap 구조 변경 |
| 외부 AI 작업 격리 | `orchestrating-deepseek-worktrees` | 대량 초안·분류 위임 |
| 외부 AI 결과 검수 | `reviewing-external-ai-drafts` | 외부 AI 결과 실제 반영 전 |
| 아트 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` | 새 아트 방향·생성·편집 프롬프트 |
| 프로젝트 교훈 환류 | `promoting-project-knowledge` | 반복 검증된 프로젝트 독립 원리 존재 |
| Base 수정제안서 검토·구현 | `reviewing-and-implementing-base-change-proposals` | 사용자가 BCP 검토 또는 승인된 구현을 요청 |

## 9. 선택적 호출과 항상 학습

```json
{
  "load_all_skills": false,
  "default_selection": "none",
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출은 Learning Log에 기록한다. 사소한 성공 호출은 기록을 강제하지 않으며 근거가 없으면 스킬 본문을 바꾸지 않는다.

## 10. 프로젝트 운영 키트

| 목적 | 템플릿·도구 |
|---|---|
| 키트 인덱스 | `templates/project-operations/README.md` |
| 신규 설치 계획 | `PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` |
| 기존 프로젝트 감사 | `EXISTING_PROJECT_MIGRATION_AUDIT.md` |
| 시작 화면 | `PROJECT_START_HERE.md` |
| Documentation Map | `PROJECT_DOCUMENTATION_MAP.md` |
| 개발 게이트 | `DEVELOPMENT_GATES.md` |
| 변경 갱신표 | `DOCUMENT_UPDATE_MATRIX.md` |
| Markdown 기획서 원형 | `DESIGN_DOCUMENT.md` |
| 구조화 JSON 기획서 원형 | `DESIGN_DOCUMENT.json` |
| schema v2.2.0 → v3.0.0 전환 | `docs/migrations/v2.2.0-to-v3.0.0.md` |
| schema v3 발행 결정 | `docs/releases/v3.0.0-hybrid-publications.md` |
| Design Document Registry | `DESIGN_DOCUMENT_REGISTRY.json` |
| Skill Registry | `SKILL_REGISTRY.json` |
| 분야·Foundation 스킬 | `skills/FOUNDATION_SKILL.md`, `skills/DISCIPLINE_SKILL.md` |
| Learning Log | `skills/SKILL_LEARNING_LOG.md` |
| 이미지 책임 원본 | `VISUAL_SOURCE_OF_TRUTH.md`, `ASSET_MANIFEST.yml` |
| 기획서 생성기 | `tools/build_design_documents.py`, `tools/design_document_diagrams.py` |
| 스킬맵 생성기 | `tools/build_project_skill_map.py`, `tools/skill_map_diagrams.py` |
| 문서·링크 검사 | `github/check_documentation_governance.py` |
| 스킬·스킬맵 검사 | `github/check_skill_routing_governance.py` |
| Markdown·JSON 기획서 발행 검사 | `github/check_design_document_publications.py` |
| GitHub Actions | `github/documentation-governance.yml` |

## 11. 구조화 기획서 발행 흐름

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 활성 Markdown 또는 JSON 책임 원본
→ 작업 흐름·상태·책임 다이어그램 생성
→ 승인 이미지·실제 캡처 포함
→ DOCX 생성
→ PDF 변환
→ 전 페이지 렌더 검수
→ 입력·생성기·출력·이미지 해시 Manifest
→ Governance 검사
```

필수 파생본:

- `.docx`
- `.pdf`
- `.assets/generated/workflow.png`
- `.assets/generated/status-summary.png`
- `.assets/generated/responsibility-map.png`
- `_PUBLICATION_MANIFEST.json`

## 12. 자동 검증

Base 회귀 테스트와 프로젝트 Governance는 다음을 확인한다.

- 루트 `[기획서]`와 중첩 복제본
- Design Document Registry와 책임 범위
- 책임 원본 ID·형식·상태·필수 구조
- PDF·선택 DOCX 헤더·SHA-256
- 생성기 변경 후 미재생성
- 다이어그램·승인 이미지 누락·해시
- PDF 전 페이지 렌더와 빈 페이지
- 등록되지 않은 Markdown 본책과 수동 변경된 파생본 탐지
- Skill Registry·분야 진입·Learning Log
- 스킬맵 필수 PDF·Manifest와 설정한 선택 Markdown/DOCX/다이어그램
- 링크·금지 파일명·갱신 누락

## 13. 완료 시 갱신

```text
실제 결과
→ 관련 Markdown 또는 JSON 책임 원본
→ DESIGN_DOCUMENT_REGISTRY.json
→ DOCX/PDF·다이어그램·Manifest
→ 관련 Skill Registry·Learning Log
→ Active Context·Roadmap·Development Gates
→ Documentation Map·Handoff
→ 자동·수동·사람 시각 검수
→ Base 환류 후보
```

실행하지 않은 구현·테스트·렌더·브랜치 보호는 완료로 보고하지 않는다.
