# Work Mode·Skill·Skill Mode 라우팅 계약

## 1. 용어

### Work Mode

요청을 처리하는 동안 AI의 **주된 작업 자세·권한·증거 기준**을 정한다. 대화 전체에 영구 고정되는 성격이 아니라 현재 작업 단계의 운영 상태다.

| Work Mode | 핵심 목적 | 기본 행동 |
|---|---|---|
| `PLAN` | 의도·요구·근거·설계·순서 확정 | 조사와 읽기 우선, 구현은 승인 전 보류 |
| `BUILD` | 승인된 계약의 코드·데이터·문서·자산 구현 | 범위 내 쓰기, 단계별 테스트·롤백 |
| `REVIEW` | 결과를 적대적으로 검토·검증·판정 | 기본 읽기 전용, 증거·반례 우선, 승인된 수정은 `BUILD`로 전환 |

복합 작업은 `PLAN → BUILD → REVIEW`처럼 순차 전환할 수 있다. 한 시점에는 주 Work Mode 하나만 둔다.

### Skill

특정 책임을 반복 수행하는 전문 작업 계약이다. trigger, 입력, 절차, 산출물, 실패 조건과 검증을 가진다.

예: `managing-game-project-operating-system`, `reviewing-and-validating-project-changes`.

### Skill Mode

한 Skill 내부에서 현재 필요한 세부 절차·권한을 선택한다.

예: 운영체계 Skill의 `audit / reconcile-legacy / migrate / verify`, 변경 검증 Skill의 `reference-freshness / regression`.

문서에서 별도 수식어 없이 Skill 안에 적힌 `mode`는 **Skill Mode**를 뜻한다.

### Grill Me

Grill Me는 독립 Skill ID가 아니라 `managing-project-intake-and-work-contract`의 `clarify` Skill Mode에서 실행하는 핵심 의사결정 인터뷰 프로토콜이다.

- 저장소에서 답할 수 있는 사실을 묻지 않는다.
- 프로젝트 방향을 바꾸는 사용자 결정만 한 번에 하나씩 묻는다.
- 선택지·장단점·GPT 권장안·확정 영향을 제공한다.
- 답변을 결정 원장과 책임 원본에 즉시 반영한다.
- 사용자가 `모두 권장안대로`라고 하면 남은 동등 유형 결정을 권장안으로 확정하고 질문을 계속 늘리지 않는다.

Reference: `skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md`

### Prompt

현재 사용자가 원하는 구체적인 목표·제약·산출물이다. Prompt가 Work Mode·Skill·Skill Mode를 직접 선언할 필요는 없다.

## 2. 자동 실행 순서

```text
사용자 Prompt
→ 의도·현재 단계·위험 파악
→ 주 Work Mode 자동 선택
→ Skill Registry trigger 대조
→ 필요한 최소 Skill 자동 선택
→ 각 Skill의 Skill Mode 자동 선택
→ 실행·검증·필요 시 Work Mode 전환
→ 사용 이유·얻은 결과·증거 보고
```

사용자가 Skill 이름이나 mode를 지정하면 강한 힌트로 사용하지만, 실제 trigger·비사용 조건·권한과 충돌하면 그대로 실행하지 않고 이유를 설명한다.

## 3. 자동 선택 규칙

- `load_by_default=false`는 자동 선택 금지가 아니라 trigger가 없을 때 불필요하게 읽지 않는다는 뜻이다.
- 사용자가 “어떤 Skill을 쓸지” 선택하지 않아도 Registry가 자동 라우팅한다.
- 주 책임 분야 Skill은 최대 하나다.
- Foundation·검증·발행·Handoff Skill은 현재 단계에 필요한 것만 추가한다.
- 같은 책임을 여러 Skill로 중복 실행하지 않는다.
- 새 사실·실패·범위 변경·정본 변경이 생기면 다시 라우팅한다.
- Skill 파일을 읽은 것과 실제 절차를 실행한 것을 구분한다.
- 새 독립 Skill보다 기존 통합 Skill의 Skill Mode·reference로 책임을 보존할 수 있는지 먼저 확인한다.

## 4. 권한 전환

```text
PLAN
- 읽기·조사·제안·계약 작성
- 사용자 승인 전 제품 동작·구조 변경 금지

BUILD
- 승인 범위만 수정
- 단계별 검증과 롤백 유지

REVIEW
- 독립 검수와 반례 탐색
- 발견 즉시 수정하지 않고 finding·심각도·증거를 먼저 기록
- 사용자가 수정까지 요청했거나 승인 범위가 있으면 BUILD로 전환해 최소 수정
- 수정 뒤 REVIEW로 돌아와 재검증
```

## 5. GPT → Codex 구현 라우팅

공용 정본: `docs/GPT_CODEX_WORKFLOW_POLICY.md`

```text
GPT PLAN
→ 저장소·대화 감사
→ Grill Me 핵심 결정
→ 기획·벤치마킹·시스템·데이터·UX 확정
→ 비-Godot 파일·GitHub 계약·마스터 구현계획 완료

Codex PLAN
→ 최신 main·실제 Godot 파일 읽기 전용 재검수
→ 기술 개선·CHANGE_PROPOSAL·사용자 결정 보고

GPT PLAN/BUILD
→ 보고서 검수
→ 기술 개선 승인
→ 패키지 Plan·Issue·체크리스트 최신화
→ READY_FOR_BUILD 판정

Codex BUILD
→ 지정 패키지 Branch의 Godot 구현·테스트·Commit·Push

GPT REVIEW
→ diff·Commit·테스트·기획 일치 검수
→ 패키지 게이트 판정

사용자
→ 체감·기획 변경·PR 병합 최종 결정
```

### GPT 권한

- 기획·조사·설계·비-Godot 파일·GitHub 계약
- 마스터 구현계획과 패키지 Plan 문서
- Codex Plan 결과 반영과 구현 결과 검수

### Codex Plan 권한

- 최신 저장소 읽기·분석·제안
- 파일·Commit·Push·PR·Issue 수정 금지

### Codex Build 권한

- 지정 Branch의 Godot 런타임 파일
- 독립 Commit과 지정 Branch Push
- `main` 직접 Push, force push, amend, PR 생성·병합 금지

### 변경 권한

동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경이다. 프로젝트 코어, Core Loop, 플레이 규칙, MVP, 주요 UI·UX, 콘텐츠 의미, 승인 기능 제거, 저장 호환성 파괴는 `CHANGE_PROPOSAL`로 GPT 단계에 반환한다.

## 6. 구현 패키지와 승인 게이트

전체 설계는 마스터 구현계획 하나로 유지하고 구현은 검증 가능한 결과 단위의 패키지로 순차 진행한다.

```text
상위 구현 Issue
├─ 패키지별 Branch / PR
└─ Vertical Slice 통합 Branch / PR
```

기본 병렬성은 `SEQUENTIAL`이다.

패키지 종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

사용자의 명시적 승인 전에는 PR을 병합하지 않는다.

담당 Skill: `maintaining-project-context-and-handoff`의 `implementation-package-handoff`.

## 7. 필수 실행 보고

L1 이상 작업은 최종 보고에 실제 사용한 항목을 남긴다.

```yaml
work_mode:
skill_id:
skill_mode:
selection: automatic | user-directed
reason:
work_performed:
result:
evidence:
status: PASS | PARTIAL | FAIL | UNVERIFIED
```

최소 사용자 표시:

```text
사용한 Work Mode·Skill·Skill Mode
→ 사용한 이유
→ 얻은 결과·증거
```

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음`을 기록한다. 모든 Skill을 나열하지 않는다.

## 8. 예시

### 기능 구현

```text
Prompt: 전투 결과 저장 기능을 구현해줘.
GPT PLAN: 저장 책임·Schema·호환성·패키지 계약 확정
Codex PLAN: 실제 Godot 저장 구조·파일·테스트 읽기 전용 재검수
GPT: Plan 보고 반영·READY_FOR_BUILD
Codex BUILD: 지정 Branch 구현·테스트·Commit·Push
GPT REVIEW: 저장·불러오기·경계·회귀·기획 일치 검수
사용자: 병합 승인
```

### 구형 파일 정리

```text
Prompt: 오래된 v2·final 파일을 최신화하고 불필요한 파일을 정리해줘.
PLAN: 운영체계 Skill `audit → reconcile-legacy`
BUILD: 승인된 UPDATE·MERGE·ARCHIVE·DELETE 처리
REVIEW: reference-freshness·발행본·복구 경로 검증
```

### GDD 검수

```text
Prompt: GDD를 적대적으로 검토하고 개선해줘.
REVIEW: 기획 검토 Skill·변경 검증 Skill 선택
BUILD: 승인된 개선안 반영
REVIEW: 모순·누락·구현 가능성 재검증
```

### Grill Me

```text
Prompt: Grill Me로 프로젝트 방향을 확실히 정해줘.
PLAN: 저장소·대화 조사
→ `clarify` + Grill Me 프로토콜
→ 결정 질문 하나와 권장안
→ 답변을 결정 원장·책임 원본에 반영
→ 차단 질문이 없으면 종료
```
