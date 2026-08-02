# Prompt Templates

이 디렉터리는 Base와 프로젝트에서 반복 사용하는 작업별 실행 Prompt를 보관한다. 불변 규칙은 `AGENTS.md`, 요청 라우팅은 `START_HERE.md`, 생명주기는 `docs/OPERATING_MODEL.md`, Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`와 `skills/SKILL_REGISTRY.json`이 책임진다.

Prompt는 최신 사용자 지시·프로젝트 정본·실제 구현·최신 Base보다 높은 권한을 갖지 않는다.

## 현재 선택

| Prompt | 상태 | 사용 범위 |
|---|---|---|
| `PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_WORK_INSTRUCTION_v3.md` | `ACTIVE_PROJECT_TOTAL_PLANNING_AUDIT_AND_IMPROVEMENT_PROMPT` | `WHOLE_PROJECT_AUDIT_FIRST` 방식의 프로젝트 `[총기획]`과 `[검수]`. 전체 프로젝트를 먼저 감사하고, 강점 보호·기획 공백·충돌·구현 불일치·파일/Skill/PDF/콜드 스타트를 검수한 뒤 승인된 개선을 반영한다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | `ACTIVE_EXECUTION_CONTRACT` | 버티컬 슬라이스 중심 기획·Codex 인계·제품 구현·검수·병합 후 동기화. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `SUPERSEDED_COMPATIBILITY` | v9 이전 비교·마이그레이션 입력. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | `SUPERSEDED_COMPATIBILITY` | 과거 호환·요구 추적 입력. |

## 선택

1. 프로젝트 전체를 검수하고 기획적으로 부족·충돌하는 부분을 개선: v3 `TOTAL_PLANNING`
2. 동일 범위를 읽기 전용으로 판정: v3 `REVIEW`
3. 버티컬 슬라이스 제품 구현·Codex 인계·병합·동기화: v9
4. v7·v8: 호환·Prompt drift 비교에만 사용
5. Prompt와 최신 Base 충돌: 최신 Base 적용 + `STALE_PROMPT_CONTRACT`
6. 현재 요청에 필요한 최소 정본·Skill만 로드

## v3 핵심 차이

- 기획 작성 우선이 아니라 전체 프로젝트 감사 우선
- 이전 총기획 지시문을 실제 비교 입력으로 받아 보존·회귀 판정
- 안전한 비방향성 수정은 `AUTO_FIX_ELIGIBLE`, 핵심 방향은 `USER_DECISION_REQUIRED`, 근거 부족은 `RESEARCH_OR_TEST_REQUIRED`
- 이전 총기획 계약의 개발 Gate·파일 처리·PDF·Skill·콜드 스타트·학습 환류 보존
- 보존 강점 지도와 Responsibility Source Map
- 기획 공백·충돌·구현 불일치 분류
- 적대적 공격과 비판 검증 분리
- Grill Me는 검증된 핵심 결정 공백에만 사용
- 승인 개선만 정본·소비자에 반영
- exact-HEAD PR Check와 회귀 검수

## 변경 검증

- `[핵심 내용]`과 이전 계약 보존
- `WHOLE_PROJECT_AUDIT_FIRST`
- 전체 인벤토리·건강도·책임 원본 지도
- 개발 Gate·기획 Coverage·파일 생명주기
- PDF·파생본·Skill·Workflow·콜드 스타트
- 중립성 Gate·Grill Me·적대적 루프
- 검수 기본 `READ_ONLY`
- 미실행 검증 명시
- PR exact HEAD·전체 diff·Required Check·unresolved thread
- v9 전문 Prompt와 책임 비중복
