# Base 문서·스킬 역할표

Base는 **[학습형] [공용]** 작업 원칙, 기획·아트·서사·연출 방법, 조사 기준, 실행 스킬, 템플릿과 일반화된 사례를 관리한다. 프로젝트 저장소는 이 공용 지식을 자신의 세계관, 수치, 엔진, 파일 경로와 현재 구현 상태에 맞게 분화·적용·검증한다.

프로젝트의 활성 기획, 코드, 수치, 파일 경로와 테스트 결과는 프로젝트 저장소가 책임진다. 프로젝트 작업에서 얻은 공용 교훈은 작업 종료·인수인계 시 Base method·skill·template·case로 환류한다.

## 1. 최초 읽기

Base 자체를 정비할 때:

```text
README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 작업에 맞는 기준 문서 또는 skills/<name>/SKILL.md
→ 필요한 method·research·case·template
```

프로젝트 작업에서는 다음 순서를 사용한다.

```text
프로젝트 AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ 프로젝트 Documentation Map
→ Handoff·Active Context
→ 프로젝트 방향·전체 기획서
→ 관련 분야 책임 문서
→ Roadmap
→ 현재 Issue·Goal·Plan
→ 프로젝트 skill extension
→ 실제 대상과 연결 파일
```

`공용 정보와 프로젝트 정보를 모두 확인한다`는 것은 저장소 모든 파일을 무작정 읽는다는 뜻이 아니다. 현재 작업에 적용되는 공용·전용 현행 책임 원본과 영향 파일을 Documentation Map과 참조 관계로 선별해 빠짐없이 확인한다.

## 2. 최상위 지속성 규칙

새 채팅, 새 AI, 새 작업자는 저장소만으로 다음을 확인할 수 있어야 한다.

- 프로젝트의 핵심 플레이어 경험과 방향
- 현재 단계, 우선순위, 선행 조건과 다음 작업
- 승인·구현·검증·미확정 상태
- 변경하면 안 되는 범위와 폐기된 방향
- 질문별 현행 책임 문서
- 적용할 Base skill과 프로젝트 extension
- 실제 파일·데이터·테스트 경로
- 작업 종료 시 Base로 환류할 공용 학습 데이터

이를 위해 프로젝트 기획서·로드맵·스킬·Documentation Map·Active Context를 항상 현재 상태로 유지한다. 방향, 수치, 용어, 범위, 구현 상태 또는 작업 절차가 바뀌면 같은 작업 안에서 영향받는 책임 원본을 갱신한다.

## 3. 공용 작업 원본

| 구분 | 파일 | 책임 |
|---|---|---|
| 최소 규칙 | `AGENTS.md` | 우선순위, 지속성, 공용·전용 확인, 작업 종료·학습 환류 |
| 상세 규칙 | `docs/AI_SHARED_WORK_RULES.md` | 역할·범위·품질·승격 운영 |
| 작업 흐름 | `docs/AI_WORKFLOW_RULES.md` | L0~L4, 공용·전용 컨텍스트, Superpowers, 외부 AI, 검증·환류 |
| 콘텐츠 기획 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름→검증 |
| 스킬 운영 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 스킬·외부 모델 선택, 권한·비용·검증 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 작업 시작·종료 체크 |
| 벤치마킹 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 조사와 적용·제외 결론 |
| 맞춤 지침 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 지침 작성 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 버전과 변경 |

## 4. 실행 스킬

| 작업 | 스킬 |
|---|---|
| 요청을 좋은 프롬프트로 변환 | `skills/transforming-requests-into-prompts/SKILL.md` |
| Vertical Slice 설계 | `skills/designing-vertical-slices/SKILL.md` |
| 기획서 종류·책임 구조 설계 | `skills/writing-game-design-documents/SKILL.md` |
| DeepSeek·외부 AI 대량 작업 격리 | `skills/orchestrating-deepseek-worktrees/SKILL.md` |
| 외부 AI 초안·diff 검수 | `skills/reviewing-external-ai-drafts/SKILL.md` |
| 아트·UI 프롬프트와 디자인 기술 카드 | `skills/designing-art-prompts-and-technique-cards/SKILL.md` |
| 프로젝트 결과를 Base 학습 데이터로 환류 | `skills/promoting-project-knowledge/SKILL.md` |

루트 `skills/`는 직접 적용 가능한 절차를 관리한다. `docs/knowledge/skills/`는 넓은 분야의 능력 지도와 검수 계약을 관리한다.

## 5. 공용 학습 지식 베이스

시작 문서: `docs/knowledge/README.md`

| 영역 | 책임 |
|---|---|
| `methods/` | 반복 가능한 설계·제작 판단 방법 |
| `research/` | 조사 질문·출처·표준·근거·적용 결론 |
| `skills/` | 분야별 입력·산출물·검수 능력 계약 |
| `cases/` | 프로젝트·벤치마킹 사례에서 추출한 성공·실패·미검증 교훈 |

핵심 라우팅:

- 전체 기획 체계: `methods/PLANNING_SYSTEM_METHOD.md`
- 인수인계·콜드 스타트: `methods/PROJECT_HANDOFF_CONTEXT_METHOD.md`
- 서사·관계: `methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md`
- 아트: `methods/ART_DIRECTION_METHOD.md`
- 캐릭터·서사 아트: `methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md`
- AI 아트 프롬프트·기술 카드: `methods/AI_ART_PROMPT_TECHNIQUE_METHOD.md`
- 애니메이션·전투 연출: `methods/ANIMATION_AND_PRESENTATION_METHOD.md`
- 대화·이벤트 연출: `methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`
- 조사·근거: `research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`
- 외부 AI·프롬프트 공식 자료: `research/AI_WORKFLOW_AND_PROMPT_SOURCE_NOTES.md`
- FACS 표정 제어 참고: `research/FACS_ACTION_UNIT_PROMPT_REFERENCE.md`
- 분야별 능력 지도: `skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md`
- 아트 실무 능력: `skills/ART_DIRECTION_SKILL_MATRIX.md`
- 구체 사례: `cases/README.md`

## 6. 기획서와 템플릿

| 목적 | 템플릿 |
|---|---|
| 실행 프롬프트 | `templates/EXECUTABLE_PROMPT.md` |
| 프로젝트 AI 역할·worktree | `templates/ai/PROJECT_AI_COLLABORATION_PROFILE.md` |
| DeepSeek 작업 패키지 | `templates/ai/DEEPSEEK_WORK_PACKAGE.md` |
| 외부 AI 결과 검수 | `templates/ai/EXTERNAL_AI_DRAFT_REVIEW.md` |
| 기획서 책임 지도·로드맵·스킬 연결 | `templates/planning/DESIGN_DOCUMENT_SYSTEM.md` |
| 프로젝트 방향 | `templates/planning/PROJECT_DIRECTION_BRIEF.md` |
| 콘텐츠·첫 10분·PoC | `templates/CONTENT_DESIGN_BRIEF.md` |
| Vertical Slice | `templates/planning/VERTICAL_SLICE_PLAN.md` |
| 서사·관계 | `templates/planning/NARRATIVE_CONTENT_PLAN.md` |
| 아트 방향·기술·프롬프트 | `templates/planning/ART_DIRECTION_BRIEF.md` |
| 아트·UI 디자인 기술 카드 | `templates/planning/ART_TECHNIQUE_CARD.md` |
| 표정·FACS 보조 제어 | `templates/planning/EXPRESSION_CONTROL_CARD.md` |
| 캐릭터 포스터·상세 페이지 | `templates/planning/CHARACTER_PROMO_POSTER_BRIEF.md` |
| 연출 | `templates/planning/PRESENTATION_PLAN.md` |
| 인수인계 | `templates/planning/HANDOFF_CONTEXT.md` |
| 프로젝트 스킬 확장 | `templates/skills/PROJECT_SKILL_EXTENSION.md` |
| 사례 연구 | `templates/KNOWLEDGE_CASE_STUDY.md` |

## 7. 작업별 최소 읽기

| 작업 | 최소 기준 |
|---|---|
| 요구 구체화·Goal | AGENTS, Base version, 요청 변환 스킬, 프로젝트 방향, 실행 프롬프트 템플릿 |
| 전체 기획 체계 | Handoff, 기획 시스템 method, 기획서 작성 스킬, Roadmap |
| 핵심 재미·첫 10분 | 프로젝트 방향, 콘텐츠 기획 method와 brief |
| Vertical Slice | 프로젝트 방향·Roadmap, Vertical Slice 스킬과 템플릿 |
| DeepSeek 대량 초안 | 프로젝트 AI 프로필, DeepSeek worktree 스킬과 작업 패키지 |
| 외부 AI 결과 실제 반영 | 프로젝트 책임 문서, 외부 AI 검수 스킬과 검수 템플릿 |
| 인수인계 | Handoff method·템플릿, Roadmap, Documentation Map, skill extensions |
| 서사·아트·연출 | 프로젝트 방향·관련 책임 기획서·해당 Base method·skill matrix·case |
| 아트 기술 추천·이미지 프롬프트 | 프로젝트 아트 방향, AI 아트 prompt method, 실행 스킬, 기술 카드 |
| FACS 표정 편집 | 프로젝트 캐릭터 원본, FACS reference, 표정 카드, 관련 case |
| 캐릭터 포스터 | 프로젝트 아트 방향, 포스터 brief와 관련 case |
| 벤치마킹 | 프로젝트 문제·결정 범위, 조사 method와 벤치마킹 가이드 |
| 스킬 도입 | 프로젝트 AI 프로필, 스킬 채택 가이드 |
| 지식 승격·인수인계 | 실제 결과·검증, 승격 스킬과 knowledge README |

## 8. Base와 프로젝트 책임

### Base — [학습형] [공용]

- 재사용 가능한 규칙·method·research·skill·template
- 검증 상태와 적용 조건이 기록된 체크리스트
- 프로젝트 결과에서 일반화한 성공·실패·미검증 사례
- 프로젝트가 분화해 사용할 공용 원본

### 프로젝트 — [전용] [분화·적용·검증]

- 프로젝트 비전과 실제 GDD
- 세계관·캐릭터·수치·데이터·파일 경로
- 활성 Roadmap·Issue·Goal·Plan
- 현재 구현과 테스트 결과
- 실제 모델·계정·비용·원본 이미지·승인 프롬프트
- Base 스킬의 프로젝트 전용 확장
- 공용화 전의 관찰·가설·실험 결과

## 9. 프로젝트 기본 문서

프로젝트가 필요에 따라 관리하되, 새 작업자가 저장소만으로 재개할 수 있도록 다음 책임을 유지한다.

- `AGENTS.md`: 최상위 규칙
- `docs/BASE_RULES_VERSION.md`: 공용 학습 데이터 기준 버전
- `README.md`: 프로젝트 요약과 최초 읽기
- Documentation Map: 질문별 책임 원본
- Handoff 또는 Active Context: 현재 상태와 다음 작업
- 프로젝트 방향서와 전체·분야별 책임 기획서
- Roadmap과 Decisions Pending
- 프로젝트 AI 협업 프로필
- 현재 Issue·Goal·Plan
- 프로젝트 전용 skill extension
- 아트 기술 카드·프롬프트 사례·자산 manifest
- 테스트·QA 기록

## 10. 작업 종료·인수인계 갱신

반드시 확인한다.

1. 기획서에 최신 방향, 플레이어 가치, 범위와 금지 방향이 반영됐는가?
2. Roadmap에 현재 단계, 우선순위, 선행 조건, 다음 작업과 종료 기준이 반영됐는가?
3. 프로젝트 skill extension이 실제 파일·데이터·검증과 일치하는가?
4. Active Context·Handoff가 현재 상태와 읽기 순서를 올바르게 연결하는가?
5. Documentation Map과 README의 경로가 유효한가?
6. 프로젝트 전용 기록과 Base 공용 학습 데이터가 구분됐는가?
7. method·skill·template 반영과 case 작성·상태 갱신이 필요한가?
8. 새 작업자가 콜드 스타트 질문에 10분 안에 답할 수 있는가?

## 11. 관리 원칙

- 같은 규칙을 여러 문서에 장문으로 복사하지 않는다.
- 한 질문에는 현행 책임 원본 하나를 둔다.
- 실행 절차는 루트 `skills/`, 넓은 참고 계약은 `docs/knowledge/skills/`에 둔다.
- 한 번 성공한 방법은 먼저 case로 남기고 반복 검증 전에는 공용 확정 규칙으로 쓰지 않는다.
- 외부 AI 결과는 실제 diff·근거·테스트 확인 전까지 검수 대기 입력이다.
- 구버전은 Git 이력으로 보존하고 활성 복제본을 만들지 않는다.
- `archive`·`hold`는 기본 읽기에서 제외한다.
- 외부 사례의 표면을 복제하지 않고 문제 해결 원리만 기록한다.
