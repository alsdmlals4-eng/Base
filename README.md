# Base

여러 프로젝트가 함께 사용하는 **AI 협업 규칙과 공용 기획 지식 베이스**의 원본 저장소입니다.

Base에는 특정 게임, 엔진, 세계관, 제품의 활성 사양을 두지 않습니다. 대신 여러 프로젝트에서 재사용할 수 있는 작업 원칙, 기획 방법, 아트·서사·연출 제작 기준, 정보 수집 방법, 검수 스킬과 일반화된 사례 연구를 관리합니다.

각 프로젝트는 필요한 Base 문서를 저장소 내부에 로컬 사본 또는 명시적 참고 기준으로 연결하고, 프로젝트 전용 규칙과 현재 상태는 해당 프로젝트 저장소에 둡니다.

## 목적

- 새 프로젝트와 새 AI가 같은 작업 기준으로 시작한다.
- 공용 방법과 프로젝트 전용 기획을 섞지 않는다.
- 좋은 기획·아트·서사·연출 작업의 판단 순서와 검수 기준을 누적한다.
- 프로젝트와 벤치마킹에서 얻은 교훈을 재사용 가능한 사례로 남긴다.
- Base 원격 변경이 진행 중인 프로젝트를 갑자기 바꾸지 않도록 기준 커밋을 기록한다.
- 한 프로젝트의 결정은 우선 사례로 남기고 반복 검증된 원칙만 공용 method·skill로 승격한다.

## 공용 작업 규칙

| 파일 | 역할 |
|---|---|
| `AGENTS.md` | 여러 프로젝트에 공통인 최소 AI 작업 원칙 |
| `docs/AI_SHARED_WORK_RULES.md` | 역할 분리, 범위 관리, 품질 원칙, Base 승격 운영 방식 |
| `docs/AI_WORKFLOW_RULES.md` | 공통 작업 순서와 Goal 작성 기준 |
| `docs/CONTENT_DESIGN_METHOD.md` | 의도→경험→규칙→흐름 기반 콘텐츠 기획, 첫 10분, PoC와 채택 기준 |
| `docs/AI_SKILL_ADOPTION_GUIDE.md` | 외부 스킬 채택, 보안 사전점검, context compact 기준 |
| `docs/MVP_WORKFLOW_CHECKLIST.md` | 실제 작업 시작·종료 체크리스트 |
| `docs/BENCHMARKING_REFERENCE_GUIDE.md` | 벤치마킹 기록과 적용 기준 |
| `docs/DOCUMENTATION_MAP.md` | Base와 프로젝트 문서의 책임 경계 |
| `docs/CUSTOM_INSTRUCTIONS_GUIDE.md` | ChatGPT·Codex 맞춤형 지침 작성 기준 |
| `docs/CHANGELOG.md` | Base 변경 기록 |

## 공용 기획 지식 베이스

시작 문서: [`docs/knowledge/README.md`](docs/knowledge/README.md)

```text
docs/knowledge/
├─ methods/   반복 가능한 기획·제작 방법
├─ research/  정보 수집·벤치마킹·근거 관리
├─ skills/    작업 유형별 실무 능력과 검수 계약
└─ cases/     프로젝트·벤치마킹에서 추출한 사례 연구
```

### 핵심 methods

- `PLANNING_SYSTEM_METHOD.md` — 상태·방향·분야별 책임 문서·로드맵·검증을 연결하는 기획 체계.
- `PROJECT_HANDOFF_CONTEXT_METHOD.md` — 문서만으로 현재 방향과 다음 작업을 이해시키는 인수인계 구조.
- `NARRATIVE_AND_RELATIONSHIP_METHOD.md` — 장면·대사·선택 기억·관계·후일담 설계.
- `ART_DIRECTION_METHOD.md` — 화면 기준, 형태 언어, 제작 규격과 아트 검수.
- `CHARACTER_AND_NARRATIVE_ART_METHOD.md` — 캐릭터·초상·표정·텍스트 없는 서사형 자산 운영.
- `ANIMATION_AND_PRESENTATION_METHOD.md` — 상태·판정·이동·공격·피격·승리 연출 동기화.
- `DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md` — 대화 UI·캐릭터 배치·표정·컷인·음향·접근성.

### research·skills·cases

- `research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md` — 조사 질문, 출처 평가, 적용·제외 결론.
- `skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md` — 의도 합성, 상태 감사, 기획, 조사, PoC, 인수인계 능력 계약.
- 기존 `skills/` — 아트, 애니메이션, 인수인계·검수 실무 매트릭스.
- `cases/README.md` — OMENWARD와 urban-legend에서 추출한 공용 사례 라우터.

## 템플릿

| 파일 | 역할 |
|---|---|
| `templates/CONTENT_DESIGN_BRIEF.md` | 핵심 재미·첫 10분·콘텐츠 정체성·PoC 정리 |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 프로젝트·벤치마킹 사례를 공용 학습 데이터로 기록 |
| `templates/planning/PROJECT_DIRECTION_BRIEF.md` | 프로젝트 약속·핵심 경험·불변 조건 |
| `templates/planning/NARRATIVE_CONTENT_PLAN.md` | 장면·대사·선택·관계·데이터 경계 |
| `templates/planning/ART_DIRECTION_BRIEF.md` | 시각 약속·스타일 축·자산 티어·QA |
| `templates/planning/PRESENTATION_PLAN.md` | 화면 시선·표정·컷인·접근성 |
| `templates/planning/HANDOFF_CONTEXT.md` | 현재 상태·책임 원본·다음 작업 인수인계 |
| `templates/` | 새 프로젝트용 기타 작업·기획 템플릿 |

## 사용 방식

1. Base에서 공용 작업 규칙, methods, research, skills, cases를 관리한다.
2. 프로젝트는 필요한 문서를 로컬 사본으로 동기화하거나 기준 커밋과 경로를 기록한다.
3. 일상적인 프로젝트 작업에서는 프로젝트의 `AGENTS.md`, Handoff/Active Context, 현재 Issue를 먼저 읽는다.
4. Base는 작업 방법, 조사 방식, 품질 기준과 유사 사례를 찾을 때 사용한다.
5. Base의 내용이 프로젝트 최신 승인과 충돌하면 프로젝트 규칙이 우선한다.
6. 프로젝트의 `docs/BASE_RULES_VERSION.md`에 기준 Base 커밋 SHA와 동기화 날짜를 기록한다.
7. Base 변경을 프로젝트에 자동 병합하지 않는다.

## 지식 승격 방식

```text
프로젝트 전용 해결안
→ 실제 작업·PoC·검수
→ 공용성 판단
→ cases에 사례 기록
→ 다른 맥락에서 반복 확인
→ methods 또는 skills로 승격
```

- 한 프로젝트에서 한 번 사용한 결정은 우선 사례로 남긴다.
- 결과가 없는 결정은 `가설` 상태로 표시한다.
- 여러 프로젝트에서 유효하거나 충분한 검증 근거가 있을 때 공용 방법으로 승격한다.
- 프로젝트 고유 이름, 수치, 경로, 저장 구조는 제거한다.
- 구현 작업자는 Base를 임의로 수정하지 않는다. 사용자가 공용 반영을 승인한 경우에만 갱신한다.

## 맞춤형 지침 운영

ChatGPT나 Codex 맞춤형 지침에는 긴 프로젝트 세계관이나 MVP 명세를 넣지 않는다.

- 맞춤형 지침: 안정적인 작업 태도와 읽기 순서.
- Base: 공용 작업 방법과 지식.
- 프로젝트 GitHub 문서: 프로젝트별 상세 규칙과 현재 상태.
- Issue / Goal / 전달 패키지: 현재 작업의 구체적 구현 기준.

기준 문서:

- `docs/CUSTOM_INSTRUCTIONS_GUIDE.md`
- `templates/custom-instructions.gpt.md`
- `templates/custom-instructions.codex.md`

## 경계

Base에 두지 않는다:

- 활성 프로젝트의 전체 GDD와 현재 밸런스 수치.
- 엔진 코드와 프로젝트 전용 데이터·테스트 결과.
- 비공개 원문과 공개 권한이 없는 자료.
- 외부 작품의 코드·아트·사운드·문구·UI 복제본.

Base 사례에는 프로젝트 이름과 공개 가능한 맥락을 적을 수 있지만 문제·결정·결과·재사용 원칙으로 일반화한다. 현재 구현 경로와 세부 수치는 프로젝트 책임 문서에서 관리한다.
