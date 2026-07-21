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

## 5. 필수 실행 보고

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
→ 사용 이유
→ 얻은 결과·증거
```

중요 후보를 사용하지 않았으면 `trigger 불일치 / 비사용 조건 / 현재 단계 아님 / 도구·입력 없음`을 기록한다. 모든 Skill을 나열하지 않는다.

## 6. 예시

### 기능 구현

```text
Prompt: 전투 결과 저장 기능을 구현해줘.
PLAN: 저장 책임·Schema·호환성 확인
BUILD: 구현 Skill과 저장 데이터 Skill Mode 실행
REVIEW: 저장·불러오기·경계·회귀 검증
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
