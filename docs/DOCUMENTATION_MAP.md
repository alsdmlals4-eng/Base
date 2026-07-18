# Base 문서·스킬 역할표

Base는 **[학습형] [공용]** 작업 원칙, 설계 방법, 실행 스킬, 템플릿과 일반화된 사례를 관리한다. 프로젝트의 세계관, 실제 수치, 구현 상태, 파일 경로, 승인 이미지와 테스트 결과는 프로젝트 저장소가 책임진다.

## 1. 최초 읽기

Base를 참고하거나 Base 자체를 정비할 때:

```text
START_HERE.md
→ README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 현재 작업에 맞는 method·skill
→ 필요한 template·research·case
→ 대상 프로젝트 현행 책임 원본과 실제 파일
```

최소 호출문:

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

프로젝트 작업 읽기 순서:

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 적용 Base 기준
→ 프로젝트 START_HERE·Active Context·Documentation Map
→ DEVELOPMENT_GATES·PROJECT_SKILL_MAP
→ 관련 분야 본책·분야 스킬
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
→ 현재 작업에 필요한 Base method·skill·template·case
```

저장소 전체를 무작정 읽지 않는다. Documentation Map에서 현재 질문과 영향 분야에 필요한 현행 책임 원본만 선택한다. `[백업]`, `[보류]`, `[제거 후보]`, archive·hold·deprecated는 감사·재개 요청이 없는 한 기본 읽기에서 제외한다.

## 2. 최상위 지속성 계약

새 채팅과 새 AI는 저장소만으로 다음을 확인할 수 있어야 한다.

- 프로젝트 목적과 핵심 플레이어 경험
- 현재 개발 단계, 다음 게이트와 최우선 작업
- 승인·구현·검증·미확정·보류 상태
- 변경하면 안 되는 결정과 보호 경로
- 분야별 현행 책임 본책과 프로젝트 스킬
- 실제 코드·데이터·자산·테스트 경로
- 승인 이미지, 실제 캡처와 최신 분야 PDF
- 작업 종료 시 갱신 대상과 Base 환류 경계

## 3. Base 공용 작업 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최초 라우터 | `START_HERE.md` | Base URL 호출 계약과 요청별 라우팅 |
| 최소 규칙 | `AGENTS.md` | 우선순위, 보존, 검증, 문서 수명주기와 학습 환류 |
| 저장소 개요 | `README.md` | 주요 구조·method·skill·template 안내 |
| 상세 공용 규칙 | `docs/AI_SHARED_WORK_RULES.md` | 역할·범위·품질·공용화 운영 |
| AI 작업 흐름 | `docs/AI_WORKFLOW_RULES.md` | L0~L4, 공용·전용 컨텍스트, 외부 AI, 검증 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 시작·게이트·구현·종료 체크 |
| 콘텐츠 기획 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 |
| 스킬 채택 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬·모델·권한·비용·검증 |
| 벤치마킹 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 조사 질문·근거·적용·제외 |
| 맞춤 지침 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 지침 작성 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 변경과 동기화 기준 |

## 4. 게임 프로젝트 운영체계 Method

| 질문 | Method |
|---|---|
| 분야별 본책·이미지·GitHub 운영을 어떻게 연결하는가? | `docs/knowledge/methods/GAME_PROJECT_OPERATING_SYSTEM_METHOD.md` |
| 작업과 제품 단계의 개발 게이트를 어떻게 판정하는가? | `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md` |
| 운영 중인 기존 프로젝트를 어떻게 안전하게 재배치하는가? | `docs/knowledge/methods/EXISTING_PROJECT_SAFE_MIGRATION_METHOD.md` |
| 분야별 프로젝트 스킬을 어떻게 분리·학습·통합하는가? | `docs/knowledge/methods/DISCIPLINE_SKILL_EVOLUTION_METHOD.md` |
| 분야별 최신 PDF를 어떻게 생성·검수하는가? | `docs/knowledge/methods/DISCIPLINE_PDF_PUBLICATION_METHOD.md` |
| 전체 기획 계층과 책임 원본을 어떻게 설계하는가? | `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md` |
| 새 AI가 재개할 Handoff를 어떻게 만드는가? | `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` |

추가 분야 Method:

- 서사·관계: `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 아트 방향: `docs/knowledge/methods/ART_DIRECTION_METHOD.md`
- 캐릭터·서사 아트: `docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- AI 아트 프롬프트: `docs/knowledge/methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- 애니메이션·전투 연출: `docs/knowledge/methods/ANIMATION_AND_PRESENTATION_METHOD.md`
- 대화·이벤트 연출: `docs/knowledge/methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- 조사·근거: `docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`

## 5. 실행 스킬

| 작업 | 스킬 |
|---|---|
| 새 프로젝트 운영체계 감사·설치 | `skills/installing-game-project-operating-system/SKILL.md` |
| 기존 운영 프로젝트 안전 마이그레이션 | `skills/migrating-existing-game-project-structure/SKILL.md` |
| 분야별 프로젝트 스킬 생성·통합·학습 | `skills/evolving-project-discipline-skills/SKILL.md` |
| 분야별 기획서 PDF 생성·최신성 검수 | `skills/publishing-discipline-bibles/SKILL.md` |
| 요청을 실행 가능한 프롬프트로 변환 | `skills/transforming-requests-into-prompts/SKILL.md` |
| Vertical Slice 설계 | `skills/designing-vertical-slices/SKILL.md` |
| 기획서 종류·책임 구조 설계 | `skills/writing-game-design-documents/SKILL.md` |
| DeepSeek·외부 AI 대량 작업 격리 | `skills/orchestrating-deepseek-worktrees/SKILL.md` |
| 외부 AI 초안·diff 검수 | `skills/reviewing-external-ai-drafts/SKILL.md` |
| 아트·UI 프롬프트와 기술 카드 | `skills/designing-art-prompts-and-technique-cards/SKILL.md` |
| 프로젝트 교훈을 Base로 환류 | `skills/promoting-project-knowledge/SKILL.md` |

루트 `skills/`는 직접 실행 가능한 절차를 관리한다. `docs/knowledge/skills/`는 넓은 분야의 능력 지도와 검수 계약을 관리한다.

## 6. 프로젝트 운영 키트 템플릿

| 목적 | 템플릿 |
|---|---|
| 키트 인덱스 | `templates/project-operations/README.md` |
| 신규 설치 계획 | `templates/project-operations/PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` |
| 기존 프로젝트 마이그레이션 감사 | `templates/project-operations/EXISTING_PROJECT_MIGRATION_AUDIT.md` |
| 사용자·AI 시작 화면 | `templates/project-operations/PROJECT_START_HERE.md` |
| 프로젝트 Documentation Map | `templates/project-operations/PROJECT_DOCUMENTATION_MAP.md` |
| 개발 게이트 | `templates/project-operations/DEVELOPMENT_GATES.md` |
| 분야별 활성 본책 | `templates/project-operations/DISCIPLINE_BIBLE.md` |
| 프로젝트 스킬 지도 | `templates/project-operations/PROJECT_SKILL_MAP.md` |
| Foundation 스킬 계약 | `templates/project-operations/skills/FOUNDATION_SKILL.md` |
| 분야 스킬 계약 | `templates/project-operations/skills/DISCIPLINE_SKILL.md` |
| 스킬 학습 기록 | `templates/project-operations/skills/SKILL_LEARNING_LOG.md` |
| 변경 유형별 갱신 판정 | `templates/project-operations/DOCUMENT_UPDATE_MATRIX.md` |
| GPT·Codex·GitHub Workflow | `templates/project-operations/AI_WORKFLOW.md` |
| 현행·백업·보류·제거 후보 | `templates/project-operations/LIFECYCLE_AREAS.md` |
| 시각 책임 원본 | `templates/project-operations/VISUAL_SOURCE_OF_TRUTH.md` |
| 이미지·자산 Manifest | `templates/project-operations/ASSET_MANIFEST.yml` |
| 분야 PDF 발행 계획 | `templates/project-operations/DISCIPLINE_PDF_PUBLICATION.md` |
| PDF 최신성 Manifest | `templates/project-operations/PUBLICATION_MANIFEST.json` |
| Issue·PR·CODEOWNERS·자동 검사 | `templates/project-operations/github/` |

기존 공용 템플릿:

- 실행 프롬프트: `templates/EXECUTABLE_PROMPT.md`
- 프로젝트 AI 역할: `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md`
- 외부 AI 작업·검수: `templates/ai/DEEPSEEK_WORK_PACKAGE.md`, `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md`
- Vertical Slice: `templates/planning/VERTICAL_SLICE_PLAN.md`
- 프로젝트 방향: `templates/planning/PROJECT_DIRECTION_BRIEF.md`
- 콘텐츠 기획: `templates/CONTENT_DESIGN_BRIEF.md`
- 서사·아트·연출: `templates/planning/`
- Base skill 프로젝트 확장: `templates/skills/PROJECT_SKILL_EXTENSION.md`
- 사례 연구: `templates/KNOWLEDGE_CASE_STUDY.md`

## 7. 작업별 최소 읽기

| 작업 | 최소 기준 |
|---|---|
| 새 프로젝트 운영체계 설치 | Base START_HERE, 운영체계 Method, installer Skill, project-operations 키트, 대상 프로젝트 현황 |
| 기존 프로젝트 구조 검수·재배치 | 대상 저장소 전체 현황, 안전 마이그레이션 Method·Skill·Audit 템플릿 |
| 개발 게이트 설계·검수 | 프로젝트 방향·Roadmap·현재 증거, DEVELOPMENT_GATES Method·템플릿 |
| 분야별 프로젝트 스킬 구축 | 분야 본책·실제 작업·검증, 스킬 진화 Method·Skill·Skill Map |
| 분야 PDF 발행 | 분야 본책·활성 부록·Visual Source·Manifest·실제 캡처, PDF Method·Skill |
| 요구 구체화·Goal | 프로젝트 방향, 요청 변환 Skill, 실행 프롬프트 템플릿 |
| 전체 기획 체계 | Handoff, 기획 시스템 Method, 기획서 Skill, Roadmap |
| 핵심 재미·첫 10분 | 프로젝트 방향, 콘텐츠 기획 Method와 Brief |
| Vertical Slice | 방향·Roadmap·게이트, Vertical Slice Skill·템플릿·사례 |
| 이미지 유입·교체 | Visual Source·Asset Manifest, 아트 Method, 기존 승인 이미지, 실제 캡처 |
| DeepSeek 대량 초안 | 프로젝트 AI 프로필, worktree Skill과 작업 패키지 |
| 외부 AI 결과 반영 | 프로젝트 책임 원본, 외부 AI 검수 Skill과 실제 diff·테스트 |
| 인수인계 | Handoff Method·템플릿, Roadmap, Map, Project Skill Map |
| 벤치마킹 | 프로젝트 결정 질문, 조사 Method, 벤치마킹 가이드 |
| 지식 승격 | 실제 결과·반복 검증, 승격 Skill과 기존 Base 중복 확인 |

## 8. 게임 프로젝트 기본 책임 분야

프로젝트 규모에 따라 폴더·본책을 통합할 수 있지만 다음 책임은 누락하지 않는다.

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

각 분야는 `분야 진입 문서 → 활성 본책 → 프로젝트 분야 스킬 → Roadmap·Issue·Plan → 실제 파일 → 검증 → PDF`로 연결한다. 공용 절차는 foundation 스킬에 둔다.

## 9. Base와 프로젝트 경계

### Base — [학습형] [공용]

- 재사용 가능한 규칙·Method·Research·Skill·Template
- 검증 상태와 적용 조건이 기록된 체크리스트
- 프로젝트 결과에서 일반화한 성공·실패·미검증 사례

### 프로젝트 — [전용] [분화·적용·검증]

- 비전·세계관·캐릭터·게임 규칙·수치
- 실제 파일·데이터·자산·엔진 경로
- 활성 Roadmap·Issue·Goal·Plan
- 현재 구현·테스트·PDF·승인 이미지
- Base 공용 스킬을 실제 경로에 연결한 프로젝트 스킬
- 공용화 전 관찰·가설·실험 결과

충돌 시 최신 사용자 지시와 프로젝트 현행 책임 원본이 우선한다.

## 10. 프로젝트 최소 책임 원본

- `AGENTS.md`
- `BASE_RULES_VERSION.md`
- `START_HERE.md`
- Active Context·Handoff
- Documentation Map
- 프로젝트 방향서와 분야별 본책
- Development Gates와 Roadmap
- Document Update Matrix
- Project Skill Map과 분야별 프로젝트 스킬
- Visual Source·Asset Manifest·실제 캡처
- Publication Manifest와 분야별 PDF
- 테스트·QA·통합검수 기록

실제 프로젝트에 필요하지 않은 파일을 억지로 생성하지 않는다. 기존 파일이 같은 책임을 안정적으로 수행하면 경로를 유지하고 Map에서 연결한다.

## 11. 작업 종료·인수인계

1. 실제 결과와 승인·구현·검증 상태를 본책에 반영한다.
2. Roadmap·게이트·Active Context·Handoff를 갱신한다.
3. Documentation Map과 Project Skill Map의 경로를 확인한다.
4. 분야 스킬이 실제 파일·검증과 일치하는지 확인한다.
5. 이미지·자산·PDF Manifest와 파생본 최신성을 확인한다.
6. 백업·보류·제거 후보가 기본 컨텍스트에 혼입되지 않는지 확인한다.
7. 프로젝트 전용 교훈과 Base 공용화 후보를 분리한다.
8. 새 작업자가 10분 안에 방향·상태·다음 작업·스킬·검증을 찾는지 확인한다.

## 12. 관리 원칙

- 한 질문에 현행 책임 원본 하나를 둔다.
- 같은 내용을 여러 문서·스킬·PDF에 장문 복사하지 않는다.
- 단순 이전 버전은 Git 이력으로 보존한다.
- `[백업]`은 외부 원본·감사·승인 근거처럼 Git 이력만으로 부족할 때만 사용한다.
- `[보류]`에는 보류 이유·재개 조건·책임 원본·선행 작업을 기록한다.
- 제거 후보는 고유 정보·참조·복구·사용자 승인을 검증하기 전 삭제하지 않는다.
- 한 번 성공한 방법은 관찰·가설로 기록하고 반복 검증 전에는 공용 강제 규칙으로 쓰지 않는다.
- 외부 AI 결과는 실제 diff·근거·테스트 확인 전까지 검수 대기 입력이다.
