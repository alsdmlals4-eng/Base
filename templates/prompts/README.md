# Prompt Templates

이 디렉터리는 Base와 프로젝트에서 반복 사용하는 작업별 실행 Prompt를 보관한다. 불변 규칙은 `AGENTS.md`, 요청 라우팅은 `START_HERE.md`, 생명주기는 `docs/OPERATING_MODEL.md`, Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`와 `skills/SKILL_REGISTRY.json`이 책임진다.

Prompt는 최신 사용자 지시·프로젝트 정본·실제 구현·최신 Base보다 높은 권한을 갖지 않는다.

## 현재 선택

| Prompt | 상태 | 사용 범위 |
|---|---|---|
| `PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v2.md` | `ACTIVE_PROJECT_PLANNING_AND_REVIEW_PROMPT` | 프로젝트 `[총기획]`과 `[검수]`. Grill Me 핵심 결정, 전체 GDD Coverage, 벤치마킹, 적대적 검토, PR_CHECK exact-HEAD Gate를 통합한다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | `ACTIVE_EXECUTION_CONTRACT` | 버티컬 슬라이스 중심 기획·Codex 인계·구현·검수·병합 후 동기화. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `SUPERSEDED_COMPATIBILITY` | v9 이전 비교·마이그레이션 입력. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | `SUPERSEDED_COMPATIBILITY` | 과거 호환·요구 추적 입력. |

## 선택

1. 프로젝트 전체 기획 작성·통합·보완: v2 `TOTAL_PLANNING`
2. 기존 GDD·구현·PR 검수: v2 `REVIEW`
3. 총기획 후 검수: `TOTAL_PLANNING → REVIEW`
4. 버티컬 슬라이스 구현·Codex 인계·병합·동기화: v9
5. v7·v8: 호환·Prompt drift 비교에만 사용
6. Prompt와 최신 Base 충돌: 최신 Base 적용 + `STALE_PROMPT_CONTRACT`
7. 현재 요청에 필요한 최소 정본·Skill만 로드

## 변경 검증

- `[총기획]`과 `[검수]` 책임·권한 분리
- `[핵심 내용]` 추적
- 환경·정본 우선
- Grill Me 중복 질문 방지·한 번에 하나·승인 동기화
- 총기획 Coverage·분야 연결
- 중립성 Gate와 적대적 공격·비판 검증·회귀
- 검수 기본 `READ_ONLY`
- PR_CHECK exact HEAD·전체 diff·Required Check·unresolved thread
- 미실행 검증 명시
- v9 전문 Prompt와 책임 비중복
