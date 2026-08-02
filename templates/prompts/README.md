# Prompt Templates

이 디렉터리는 Base와 대상 프로젝트에서 반복 사용하는 작업별 실행 Prompt를 보관한다. 항상 적용되는 불변 규칙은 루트 `AGENTS.md`, 요청별 라우팅은 `START_HERE.md`, 전체 생명주기는 `docs/OPERATING_MODEL.md`, Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`와 `skills/SKILL_REGISTRY.json`이 책임진다.

Prompt는 해당 정본을 복제하거나 덮어쓰지 않는다. 최신 사용자 지시·프로젝트 정본·실제 구현·최신 Base가 Prompt보다 우선한다.

## 현재 선택

| Prompt | 상태 | 사용 범위 |
|---|---|---|
| `PROJECT_TOTAL_PLANNING_AND_REVIEW_WORK_INSTRUCTION_v1.md` | `ACTIVE_PROJECT_PLANNING_AND_REVIEW_PROMPT` | 프로젝트의 `[총기획]` 또는 `[검수]`. 전체 GDD 기획, 분야 간 정합성, 기획·정본·실제 구현의 적대적 검수와 승인된 최소 수정을 수행한다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | `ACTIVE_EXECUTION_CONTRACT` | 게임 프로젝트의 버티컬 슬라이스 중심 기획·Codex 인계·구현·검수·병합 후 동기화. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `SUPERSEDED_COMPATIBILITY` | v9 이전 프로젝트의 비교·마이그레이션 입력. 새 작업의 활성 계약으로 사용하지 않는다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | `SUPERSEDED_COMPATIBILITY` | 과거 호환·요구 추적 입력. 새 작업의 활성 계약으로 사용하지 않는다. |

## 선택 규칙

1. 프로젝트 전체 기획을 작성·통합·보완할 때는 새 Prompt의 `TOTAL_PLANNING`을 사용한다.
2. 기존 총기획·GDD·구현을 판정할 때는 새 Prompt의 `REVIEW`를 사용한다.
3. 총기획 후 검수까지 요청하면 `TOTAL_PLANNING → REVIEW` 순서로 실행한다.
4. 버티컬 슬라이스의 구현·Codex 인계·병합·동기화까지 단일 첨부로 실행할 때는 v9 전문 Prompt를 사용한다.
5. v7·v8은 legacy requirement 추적과 Prompt drift 비교에만 사용한다.
6. Prompt와 최신 Base가 충돌하면 최신 Base를 적용하고 `STALE_PROMPT_CONTRACT`를 기록한다.
7. 모든 Prompt와 전체 Skill을 한꺼번에 로드하지 않는다. 현재 요청의 책임 원본과 trigger가 일치하는 최소 항목만 사용한다.

## 변경 검증

Prompt 추가·수정 시 최소 확인 항목:

- `[총기획]`과 `[검수]`의 책임과 권한이 분리되는가.
- `[핵심 내용]`의 목적이 추적 가능한가.
- 프로젝트 작업 환경과 정본을 먼저 확인하는가.
- 총기획 필수 영역과 분야 간 연결을 검수하는가.
- 사용자안과 AI안을 동일 기준으로 검토하는가.
- 적대적 공격과 비판 검증이 분리되는가.
- 검수의 기본 권한이 읽기 전용인가.
- 실행하지 않은 검증을 완료로 보고하지 않는가.
- 새 Prompt가 이 README에 등록되고 v9 전문 Prompt와 책임이 중복되지 않는가.
