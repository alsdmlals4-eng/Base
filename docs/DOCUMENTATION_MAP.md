# Base 문서 역할표

## Base의 책임

Base는 여러 프로젝트에 공통으로 필요한 AI 협업 원칙, 기획·아트·연출 방법, 정보 수집 기준, 실무 스킬과 일반화된 사례 연구의 원본 저장소다.

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
| 작업 원칙 | `AGENTS.md` | 최소 공용 AI 작업 원칙 |
| 작업 원칙 | `docs/AI_SHARED_WORK_RULES.md` | 역할, 범위, 품질, Base 승격 운영 |
| 작업 흐름 | `docs/AI_WORKFLOW_RULES.md` | 공통 작업 순서와 Goal 기준 |
| 콘텐츠 기획 | `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름, 첫 10분, PoC |
| 스킬 채택 | `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬, 권한, compact, 검증 |
| 실행 체크 | `docs/MVP_WORKFLOW_CHECKLIST.md` | 작업 시작·종료 체크리스트 |
| 벤치마킹 | `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 사례 조사와 적용 결론 |
| 문서 라우터 | `docs/DOCUMENTATION_MAP.md` | Base와 프로젝트 책임 경계 |
| 맞춤 지침 | `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 지침 작성 |
| 변경 기록 | `docs/CHANGELOG.md` | Base 버전과 변경 내용 |

## 공용 기획 지식 베이스

| 구분 | 파일 | 역할 |
|---|---|---|
| 지식 인덱스 | `docs/knowledge/README.md` | methods·research·skills·cases 구조와 승격 규칙 |
| 인수인계 방법 | `docs/knowledge/methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` | 문서만으로 현재 방향과 다음 작업을 이해시키는 방법 |
| 아트 방법 | `docs/knowledge/methods/ART_DIRECTION_METHOD.md` | 화면 기준, 형태 언어, 제작 규격, 검수 |
| 애니메이션 방법 | `docs/knowledge/methods/ANIMATION_AND_PRESENTATION_METHOD.md` | 상태, 판정 동기화, 피격·승리, 재사용 구조 |
| 조사 방법 | `docs/knowledge/research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md` | 조사 질문, 출처, 근거, 적용·제외 결론 |
| 아트 스킬 | `docs/knowledge/skills/ART_DIRECTION_SKILL_MATRIX.md` | 아트 디렉션 입력·산출물·실패 기준 |
| 연출 스킬 | `docs/knowledge/skills/ANIMATION_PRESENTATION_SKILL_MATRIX.md` | 모션·전투 연출 실무 계약 |
| 인수인계 스킬 | `docs/knowledge/skills/DESIGN_HANDOFF_AND_REVIEW_SKILL_MATRIX.md` | 책임 원본·동기화·콜드 스타트 검수 |
| 사례 인덱스 | `docs/knowledge/cases/README.md` | 프로젝트·벤치마킹 사례 목록과 상태 |

## 사례 라우팅

| 문제 | 참고 사례 |
|---|---|
| 같은 역할의 진영별 데이터 중복 | `docs/knowledge/cases/OMENWARD_SHARED_ARCHETYPE_FACTION_VISUAL_CASE.md` |
| 화면 전체가 보이는데 미니맵을 둘지 판단 | `docs/knowledge/cases/OMENWARD_TACTICAL_VISIBILITY_WITHOUT_MINIMAP_CASE.md` |
| 특수 경로·범위를 언제 공개할지 판단 | `docs/knowledge/cases/OMENWARD_FOGGED_SPECIALIST_ROUTE_CASE.md` |
| 버전 문서와 레거시 Issue 정리 | `docs/knowledge/cases/OMENWARD_CANONICAL_HANDOFF_CONTEXT_CASE.md` |

## 공용 템플릿

| 파일 | 역할 |
|---|---|
| `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·PoC 기획 양식 |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 공용 사례 연구 양식 |
| `templates/` | 프로젝트용 문서·Issue·Goal 템플릿 |

## 작업별 최소 읽기

| 작업 | 문서 |
|---|---|
| 요구 구체화·Issue·Goal | `AGENTS.md`, `AI_WORKFLOW_RULES.md`, 관련 템플릿 |
| 핵심 재미·첫 10분 | `CONTENT_DESIGN_METHOD.md`, `CONTENT_DESIGN_BRIEF.md` |
| 프로젝트 인수인계 | `PROJECT_HANDOFF_CONTEXT_METHOD.md`, `DESIGN_HANDOFF_AND_REVIEW_SKILL_MATRIX.md` |
| 아트 기획·검수 | `ART_DIRECTION_METHOD.md`, `ART_DIRECTION_SKILL_MATRIX.md`, 관련 cases |
| 이동·공격·승리 연출 | `ANIMATION_AND_PRESENTATION_METHOD.md`, `ANIMATION_PRESENTATION_SKILL_MATRIX.md` |
| 정보 조사·벤치마킹 | `DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md`, `BENCHMARKING_REFERENCE_GUIDE.md` |
| 외부 AI 스킬 도입 | `AI_SKILL_ADOPTION_GUIDE.md` |
| 작업 종료·교훈 승격 | `AI_SHARED_WORK_RULES.md`, `knowledge/README.md`, 사례 템플릿 |

## 프로젝트 동기화 규칙

1. 프로젝트는 필요한 Base 문서를 로컬 사본으로 두거나 기준 경로를 명시한다.
2. 일상 작업에서는 프로젝트 내부의 최신 문서를 우선 읽는다.
3. Base 커밋 SHA와 동기화 날짜는 프로젝트의 `docs/BASE_RULES_VERSION.md`에 기록한다.
4. 프로젝트 전용 규칙은 Base를 보완하며 더 구체적인 규칙이 우선한다.
5. Base 원격 변경을 자동 병합하지 않는다.
6. 프로젝트 해결안은 먼저 프로젝트에서 검증하고, 공용성 확인 뒤 cases에 승격한다.
7. 반복 검증된 사례만 methods 또는 skills로 승격한다.

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
- `templates/CONTENT_DESIGN_BRIEF.md`
- `templates/KNOWLEDGE_CASE_STUDY.md`

## 프로젝트에서 새로 작성할 문서

- `docs/BASE_RULES_VERSION.md`
- 프로젝트 전용 `AGENTS.md`
- `README.md`
- Handoff 또는 Active Context
- 프로젝트 전체 기획서
- Documentation Map
- Roadmap
- Decisions Pending
- 주제별 승인 책임 문서
- 현재 Issue·Goal·승인 제안서
- 프로젝트 설정, 데이터, 코드, Scene, 테스트 자산

## 관리 원칙

- 같은 규칙을 여러 문서에 장문으로 중복 작성하지 않는다.
- 반복 가능한 방법은 methods에 둔다.
- 조사·근거 평가 절차는 research에 둔다.
- 작업 역량·입력·산출물·검수는 skills에 둔다.
- 한 프로젝트의 결정과 결과는 먼저 cases에 둔다.
- 엔진, 세계관, 현재 수치, 구현 상태는 프로젝트 저장소에 둔다.
- Issue는 현재 작업 기준서, Goal은 구현 실행 지시서다.
- 외부 작품의 표면을 복제하지 않고 문제 해결 원리만 기록한다.
- Base 승격은 사용자 승인 뒤 별도 커밋으로 반영한다.
