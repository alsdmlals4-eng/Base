# Prompt Templates

이 디렉터리는 Base와 대상 프로젝트에서 반복 사용하는 **작업별 실행 Prompt**를 보관한다. 항상 적용되는 불변 규칙은 루트 `AGENTS.md`, 요청별 라우팅은 `START_HERE.md`, 전체 생명주기는 `docs/OPERATING_MODEL.md`, Skill 선택은 `docs/WORK_MODE_AND_SKILL_ROUTING.md`와 `skills/SKILL_REGISTRY.json`이 책임진다.

Prompt는 해당 정본을 복제하거나 덮어쓰지 않는다. 최신 사용자 지시·프로젝트 정본·실제 구현·최신 Base가 Prompt보다 우선한다.

## 현재 선택

| Prompt | 상태 | 사용 범위 |
|---|---|---|
| `BASE_PROJECT_INTEGRATED_WORK_INSTRUCTION_v1.md` | `ACTIVE_GENERAL_EXECUTION_PROMPT` | Base와 프로젝트의 일반 조사·기획·문서·코드·검수·PR 작업. `[핵심 내용]` 보존, 환경 우선, 벤치마킹, 중립성 Gate, 적대 검토 생명주기를 통합한다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md` | `ACTIVE_EXECUTION_CONTRACT` | 게임 프로젝트의 버티컬 슬라이스 중심 상세 기획·Codex 인계·구현·검수·병합 후 동기화. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v8.md` | `SUPERSEDED_COMPATIBILITY` | v9 이전 프로젝트의 비교·마이그레이션 입력. 새 작업의 활성 계약으로 사용하지 않는다. |
| `VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v7.md` | `SUPERSEDED_COMPATIBILITY` | 과거 호환·요구 추적 입력. 새 작업의 활성 계약으로 사용하지 않는다. |

## 선택 규칙

1. 일반적인 Base·프로젝트 작업은 `BASE_PROJECT_INTEGRATED_WORK_INSTRUCTION_v1.md`를 사용한다.
2. 버티컬 슬라이스 전 과정을 단일 첨부로 실행할 때는 v9 전문 Prompt를 사용한다.
3. v7·v8은 삭제하지 않고 legacy requirement 추적과 Prompt drift 비교에만 사용한다.
4. Prompt와 최신 Base가 충돌하면 최신 Base를 적용하고 `STALE_PROMPT_CONTRACT`를 기록한다.
5. 모든 Prompt와 전체 Skill을 한꺼번에 로드하지 않는다. 현재 요청의 책임 원본과 trigger가 일치하는 최소 항목만 사용한다.

## 변경 검증

Prompt 추가·수정 시 최소 확인 항목:

- `[핵심 내용]` 또는 전문 Prompt의 핵심 목적이 추적 가능한가.
- 최신 권한 순서와 `PLAN / BUILD / REVIEW`가 유지되는가.
- L1 이상 중립성 Gate와 적대 검토 생명주기가 연결되는가.
- 환경·저장소 사실을 먼저 확인하는가.
- 실행하지 않은 검증을 완료로 보고하지 않는가.
- 새 Prompt가 이 README에 등록되고 전문 Prompt와 책임이 중복되지 않는가.
