# Base 문서·스킬 역할표

Base는 공용 작업 원칙, 기획·아트·서사·연출 방법, 조사 기준, 실행 스킬, 템플릿과 일반화된 사례를 관리한다. 프로젝트의 활성 기획, 코드, 수치, 파일 경로와 테스트 결과는 프로젝트 저장소가 책임진다.

## 1. 최초 읽기

```text
README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 작업에 맞는 기준 문서 또는 skills/<name>/SKILL.md
→ 필요한 method·research·case·template
```

프로젝트 작업에서는 프로젝트 `AGENTS.md`, Handoff·Active Context, 현재 Issue·Goal, Base 로컬 사본을 먼저 읽는다.

## 2. 공용 작업 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최소 규칙 | `AGENTS.md` | 우선순위, 작업 흐름, 파일 수명주기, 검증 |
| 상세 규칙 | `docs/AI_SHARED_WORK_RULES.md` | 역할·범위·품질·승격 운영 |
| 작업 흐름 | `docs/AI_WORKFLOW_RULES.md` | L0~L4 분류와 설계→실행→검증 |
| 콘텐츠 기획 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 |
| 스킬 운영 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 스킬 선택·작성·권한·검증 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 작업 시작·종료 체크 |
| 벤치마킹 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 조사와 적용·제외 결론 |
| 맞춤 지침 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 지침 작성 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 버전과 변경 |

## 3. 실행 스킬

| 작업 | 스킬 |
|---|---|
| 요청을 좋은 프롬프트로 변환 | `skills/transforming-requests-into-prompts/SKILL.md` |
| Vertical Slice 설계 | `skills/designing-vertical-slices/SKILL.md` |
| 기획서 종류·책임 구조 설계 | `skills/writing-game-design-documents/SKILL.md` |
| 프로젝트 지식 Base 승격 | `skills/promoting-project-knowledge/SKILL.md` |

루트 `skills/`는 직접 적용 가능한 절차를 관리한다. `docs/knowledge/skills/`는 넓은 분야의 능력 지도와 검수 계약을 관리한다.

## 4. 공용 지식 베이스

시작 문서: `docs/knowledge/README.md`

| 영역 | 책임 |
|---|---|
| `methods/` | 반복 가능한 설계·제작 판단 방법 |
| `research/` | 조사 질문·출처·근거·적용 결론 |
| `skills/` | 분야별 입력·산출물·검수 능력 계약 |
| `cases/` | 프로젝트·벤치마킹 사례에서 추출한 교훈 |

핵심 라우팅:

- 전체 기획 체계: `methods/PLANNING_SYSTEM_METHOD.md`
- 인수인계: `methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
- 서사·관계: `methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 아트: `methods/ART_DIRECTION_METHOD.md`
- 캐릭터·서사 아트: `methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- 애니메이션·전투 연출: `methods/ANIMATION_AND_PRESENTATION_METHOD.md`
- 대화·이벤트 연출: `methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- 조사·근거: `research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`
- 분야별 능력 지도: `skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md`
- 구체 사례: `cases/README.md`

## 5. 기획서와 템플릿

| 목적 | 템플릿 |
|---|---|
| 실행 프롬프트 | `templates/EXECUTABLE_PROMPT.md` |
| 기획서 책임 지도 | `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` |
| 프로젝트 방향 | `templates/planning/PROJECT_DIRECTION_BRIEF.md` |
| 콘텐츠·첫 10분·PoC | `templates/CONTENT_DESIGN_BRIEF.md` |
| Vertical Slice | `templates/planning/VERTICAL_SLICE_PLAN.md` |
| 서사·관계 | `templates/planning/NARRATIVE_CONTENT_PLAN.md` |
| 아트 방향 | `templates/planning/ART_DIRECTION_BRIEF.md` |
| 연출 | `templates/planning/PRESENTATION_PLAN.md` |
| 인수인계 | `templates/planning/HANDOFF_CONTEXT.md` |
| 프로젝트 스킬 확장 | `templates/skills/PROJECT_SKILL_EXTENSION.md` |
| 사례 연구 | `templates/KNOWLEDGE_CASE_STUDY.md` |

## 6. 작업별 최소 읽기

| 작업 | 최소 기준 |
|---|---|
| 요구 구체화·Goal | `AGENTS.md`, 요청 변환 스킬, 실행 프롬프트 템플릿 |
| 전체 기획 체계 | 기획 시스템 method, 기획서 작성 스킬 |
| 핵심 재미·첫 10분 | 콘텐츠 기획 method와 brief |
| Vertical Slice | Vertical Slice 스킬과 템플릿 |
| 인수인계 | Handoff method와 템플릿 |
| 서사·아트·연출 | 해당 method·skill matrix·관련 case |
| 벤치마킹 | 조사 method와 벤치마킹 가이드 |
| 스킬 도입 | 스킬 채택 가이드 |
| 지식 승격 | 승격 스킬과 knowledge README |

## 7. Base와 프로젝트 책임

Base:

- 재사용 가능한 규칙·method·research·skill·template
- 검증된 체크리스트
- 일반화된 사례

프로젝트:

- 프로젝트 비전과 실제 GDD
- 세계관·캐릭터·수치·데이터·파일 경로
- 활성 로드맵·Issue·Goal·Plan
- 현재 구현과 테스트 결과
- Base 스킬의 프로젝트 전용 확장

## 8. 프로젝트 기본 문서

프로젝트가 필요에 따라 관리한다.

- `AGENTS.md`
- `docs/BASE_RULES_VERSION.md`
- `README.md`
- Documentation Map
- Handoff 또는 Active Context
- 프로젝트 방향서와 분야별 책임 기획서
- Roadmap과 Decisions Pending
- 현재 Issue·Goal·Plan
- 프로젝트 전용 skill extension
- 테스트·QA 기록

## 9. 관리 원칙

- 같은 규칙을 여러 문서에 장문으로 복사하지 않는다.
- 한 질문에는 현행 책임 원본 하나를 둔다.
- 실행 절차는 루트 `skills/`, 넓은 참고 계약은 `docs/knowledge/skills/`에 둔다.
- 검증되지 않은 가설은 프로젝트에 남기고 Base 확정 규칙으로 쓰지 않는다.
- 구버전은 Git 이력으로 보존하고 활성 복제본을 만들지 않는다.
- `archive`·`hold`는 기본 읽기에서 제외한다.
- 외부 사례의 표면을 복제하지 않고 문제 해결 원리만 기록한다.
