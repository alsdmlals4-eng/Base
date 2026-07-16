# Base 문서 역할표

## Base의 책임

Base는 여러 프로젝트에 공통으로 필요한 AI 협업 원칙, 기획·서사·아트·연출 방법, 정보 수집 기준, 실무 스킬과 일반화된 사례 연구의 원본 저장소다.

프로젝트별 엔진 규칙, 활성 제품 기획, 코드, 현재 수치, 파일 경로와 테스트 결과는 각 프로젝트 저장소가 책임진다.

## 최초 읽기 순서

```text
README.md
→ AGENTS.md
→ docs/DOCUMENTATION_MAP.md
→ 작업 성격에 맞는 공용 원본
→ docs/knowledge/README.md
→ 필요한 method / research / skill / case
```

프로젝트 작업 중에는 Base보다 프로젝트의 `AGENTS.md`, Handoff/Active Context, 현재 Issue·Goal을 먼저 읽는다.

## 공용 작업 원본

| 구분 | 파일 | 역할 |
|---|---|---|
| 작업 원칙 | `AGENTS.md` | 최소 공용 AI 작업 원칙과 자동 승격 원칙 |
| 작업 원칙 | `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질, Base 자동 승격 운영 |
| 작업 흐름 | `docs/AI_WORKFLOW_RULES.md` | 공통 작업 순서와 Goal 기준 |
| 콘텐츠 기획 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름, 첫 10분, PoC |
| 스킬 채택 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬, 권한, compact, 검증 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 작업 시작·종료·자동 승격 체크리스트 |
| 벤치마킹 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 사례 조사와 적용 결론 |
| 문서 라우터 | `docs/DOCUMENTATION_MAP.md` | Base와 프로젝트 책임 경계 |
| 맞춤 지침 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 지침 작성 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 버전과 변경 내용 |

## 공용 기획 지식 베이스

| 구분 | 파일 | 역할 |
|---|---|---|
| 지식 인덱스 | `docs/knowledge/README.md` | methods·research·skills·cases 구조와 승격 규칙 |
| 기획 시스템 | `docs/knowledge/methods/PLANNING_SYSTEM_METHOD.md` | 상태·방향·분야별 책임 문서·로드맵·검증 체계 |
| 인수인계 | `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` | 문서만으로 현재 방향과 다음 작업을 이해시키는 방법 |
| 서사·관계 | `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` | 장면·대사·선택 기억·관계·후일담 |
| 전장·유닛 아트 | `docs/knowledge/methods/ART_DIRECTION_METHOD.md` | 화면 기준, 형태 언어, 제작 규격, 검수 |
| 캐릭터·서사 아트 | `docs/knowledge/methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md` | 초상·표정·텍스트 없는 자산·실제 화면 검수 |
| 전투 애니메이션 | `docs/knowledge/methods/ANIMATION_AND_PRESENTATION_METHOD.md` | 상태·판정·이동·공격·피격·승리 연출 |
| 대화·이벤트 연출 | `docs/knowledge/methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md` | 대화 UI·배치·표정·컷인·음향·접근성 |
| 조사 방법 | `docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md` | 조사 질문, 출처, 근거, 적용·제외 결론 |
| 기획·조사·인수 스킬 | `docs/knowledge/skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md` | 의도 합성, 상태 감사, PoC, 수용 기준, handoff |
| 아트 스킬 | `docs/knowledge/skills/ART_DIRECTION_SKILL_MATRIX.md` | 아트 디렉션 입력·산출물·실패 기준 |
| 연출 스킬 | `docs/knowledge/skills/ANIMATION_PRESENTATION_SKILL_MATRIX.md` | 모션·전투 연출 실무 계약 |
| 인수인계 스킬 | `docs/knowledge/skills/DESIGN_HANDOFF_AND_REVIEW_SKILL_MATRIX.md` | 책임 원본·동기화·콜드 스타트 검수 |
| 사례 인덱스 | `docs/knowledge/cases/README.md` | 프로젝트·벤치마킹 사례 목록과 문제별 라우팅 |

## 작업별 최소 읽기

| 작업 | 문서 |
|---|---|
| 요구 구체화·Issue·Goal | `AGENTS.md`, `AI_WORKFLOW_RULES.md`, 관련 템플릿 |
| 전체 기획 체계 | `PLANNING_SYSTEM_METHOD.md`, `CONTENT_DESIGN_METHOD.md` |
| 핵심 재미·첫 10분 | `CONTENT_DESIGN_METHOD.md`, `CONTENT_DESIGN_BRIEF.md` |
| 프로젝트 인수인계 | `PROJECT_HANDOFF_CONTEXT_METHOD.md`, `DESIGN_HANDOFF_AND_REVIEW_SKILL_MATRIX.md` |
| 장면·대사·관계 | `NARRATIVE_AND_RELATIONSHIP_METHOD.md`, 관련 cases |
| 전장·유닛 아트 | `ART_DIRECTION_METHOD.md`, `ART_DIRECTION_SKILL_MATRIX.md`, 관련 cases |
| 캐릭터·서사 아트 | `CHARACTER_AND_NARRATIVE_ART_METHOD.md`, 관련 cases |
| 이동·공격·승리 연출 | `ANIMATION_AND_PRESENTATION_METHOD.md`, `ANIMATION_PRESENTATION_SKILL_MATRIX.md` |
| 대화 UI·표정·컷인 | `DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md`, 관련 cases |
| 정보 조사·벤치마킹 | `DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`, `BENCHMARKING_REFERENCE_GUIDE.md` |
| 기획·조사·handoff 실무 | `PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md` |
| 외부 AI 스킬 도입 | `AI_SKILL_ADOPTION_GUIDE.md` |
| 작업 종료·교훈 자동 승격 | `AI_SHARED_WORK_RULES.md`, `MVP_WORKFLOW_CHECKLIST.md`, `knowledge/README.md` |

## 사례 라우팅

| 문제 | 참고 사례 |
|---|---|
| 같은 역할의 진영별 데이터 중복 | `docs/knowledge/cases/OMENWARD_SHARED_ARCHETYPE_FACTION_VISUAL_CASE.md` |
| 화면 전체가 보이는데 미니맵을 둘지 판단 | `docs/knowledge/cases/OMENWARD_TACTICAL_VISIBILITY_WITHOUT_MINIMAP_CASE.md` |
| 특수 경로·범위를 언제 공개할지 판단 | `docs/knowledge/cases/OMENWARD_FOGGED_SPECIALIST_ROUTE_CASE.md` |
| 버전 문서와 레거시 Issue 정리 | `docs/knowledge/cases/OMENWARD_CANONICAL_HANDOFF_CONTEXT_CASE.md` |
| 정보 패널이 장면과 선택을 가림 | `docs/knowledge/cases/URBAN_LEGEND_SCENE_FIRST_UI_CASE.md` |
| 표시 이름 변경과 저장 호환 | `docs/knowledge/cases/URBAN_LEGEND_DISPLAY_NAME_INTERNAL_ID_CASE.md` |
| 대사량이 기능 흐름을 방해함 | `docs/knowledge/cases/URBAN_LEGEND_DIALOGUE_DENSITY_BY_CONTEXT_CASE.md` |
| 관계를 점수·보너스로만 표현함 | `docs/knowledge/cases/URBAN_LEGEND_RELATIONSHIP_MEMORY_CASE.md` |
| 연출 UI가 결과·저장을 중복 소유함 | `docs/knowledge/cases/URBAN_LEGEND_PRESENTATION_STATE_BOUNDARY_CASE.md` |
| 생성 이미지의 글자·현지화 문제 | `docs/knowledge/cases/URBAN_LEGEND_TEXT_FREE_GENERATIVE_ART_CASE.md` |
| 오래된 문서가 기본 읽기를 방해함 | `docs/knowledge/cases/URBAN_LEGEND_ACTIVE_DOCUMENT_ARCHIVE_CASE.md` |

## 공용 템플릿

| 파일 | 역할 |
|---|---|
| `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·PoC 기획 양식 |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 공용 사례 연구 양식 |
| `templates/planning/PROJECT_DIRECTION_BRIEF.md` | 프로젝트 방향과 불변 조건 |
| `templates/planning/NARRATIVE_CONTENT_PLAN.md` | 장면·대사·선택·관계 |
| `templates/planning/ART_DIRECTION_BRIEF.md` | 시각 약속·스타일 축·자산 티어 |
| `templates/planning/PRESENTATION_PLAN.md` | 화면 시선·표정·컷인·접근성 |
| `templates/planning/HANDOFF_CONTEXT.md` | 현재 상태·책임 원본·다음 작업 |
| `templates/` | 프로젝트용 기타 문서·Issue·Goal 템플릿 |

## 프로젝트 동기화 규칙

1. 프로젝트는 필요한 Base 문서를 로컬 사본으로 두거나 기준 경로를 명시한다.
2. 일상 작업에서는 프로젝트 내부의 최신 문서를 우선 읽는다.
3. Base 커밋 SHA와 동기화 날짜는 프로젝트에 `docs/BASE_RULES_VERSION.md`가 있을 때 기록한다.
4. 프로젝트 전용 규칙은 Base를 보완하며 더 구체적인 규칙이 우선한다.
5. Base 원격 변경을 프로젝트에 무조건 자동 병합하지 않는다.
6. 프로젝트 작업에서 발견한 안정적이고 일반화 가능한 공용 규칙은 Base 기존 기준 파일에 자동 승격한다.
7. 검증되지 않은 가설은 프로젝트의 `확인 필요` 또는 후보 상태로 남긴다.
8. 구체 사례는 필요할 때 cases에 기록하고, methods 또는 skills 승격은 반복 검증이나 강한 근거를 요구한다.

## 새 프로젝트에 복사·연결할 기본 문서

- `AGENTS.md`
- `docs/AI_SHARED_WORK_RULES.md`
- `docs/AI_WORKFLOW_RULES.md`
- `docs/CONTENT_DESIGN_METHOD.md`
- `docs/AI_SKILL_ADOPTION_GUIDE.md`
- `docs/MVP_WORKFLOW_CHECKLIST.md`
- `docs/BENCHMARKING_REFERENCE_GUIDE.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`
- 필요한 `docs/knowledge/` 문서
- 필요한 `templates/planning/` 문서

## 프로젝트에서 새로 작성할 문서

- `docs/BASE_RULES_VERSION.md`
- 프로젝트 전용 `AGENTS.md`
- `README.md`
- Handoff 또는 Active Context
- 프로젝트 방향 기획서
- 분야별 책임 기획서
- Documentation Map
- Roadmap
- Decisions Pending
- 현재 Issue·Goal·승인 제안서
- 프로젝트 설정, 데이터, 코드, Scene, 테스트 자산

## 관리 원칙

- 같은 규칙을 여러 문서에 장문으로 중복 작성하지 않는다.
- 반복 가능한 방법은 methods에 둔다.
- 조사·근거 평가 절차는 research에 둔다.
- 작업 역량·입력·산출물·검수는 skills에 둔다.
- 한 프로젝트의 구체 결정과 결과는 필요할 때 cases에 둔다.
- 안정적이고 일반화 가능한 작업 규칙은 작업 종료 시 Base 기존 파일에 자동 반영한다.
- 엔진, 세계관, 현재 수치, 구현 상태는 프로젝트 저장소에 둔다.
- Issue는 현재 작업 기준서, Goal은 구현 실행 지시서다.
- 외부 작품의 표면을 복제하지 않고 문제 해결 원리만 기록한다.