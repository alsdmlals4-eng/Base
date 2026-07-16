---
name: transforming-requests-into-prompts
description: Use when a user request is brief, ambiguous, design-sensitive, spans multiple files, or lacks explicit scope, exclusions, completion criteria, or verification.
---

# Transforming Requests Into Prompts

## Core principle

사용자의 문장을 길게 반복하지 말고, 해결할 문제와 사용자·플레이어 경험을 보존한 실행 계약으로 변환한다.

## Use level

- `L0`: 오탈자·명확한 형식 변경 — 변환 없이 처리
- `L1`: 작은 수정 — 누락된 범위·검증만 보완
- `L2`: 대안·시스템 영향 — 브레인스토밍 적용
- `L3`: 여러 시스템·핵심 구조 — 기획서와 Plan 분리
- `L4`: 재사용 방법 — 프로젝트 검증 후 Base 승격

## Required inputs

- 사용자 원문
- 프로젝트 기준 문서와 현재 상태
- 기존 결정과 보호할 동작
- 작업의 사용자·플레이어 가치

## Process

1. 원문에서 명시 요구를 추출한다.
2. 해결하려는 문제와 필요한 경험을 분리한다.
3. `[확정]`, `[권장]`, `[확인 필요]`, `[제외]`, `[보류]`로 상태를 구분한다.
4. `DOCUMENTATION_MAP.md`를 따라 관련 기준 문서와 영향 파일만 확인한다.
5. L2 이상이면 2~3개 접근법을 비용·위험·장점과 함께 비교한다.
6. 선택한 방향을 아래 8요소로 작성한다.
7. 실행자에게 필요한 읽기 순서, 위험, 보고 형식을 추가한다.
8. 구현·검증·문서 최신화를 서로 다른 단계로 분리한다.

## Output contract

```md
# 작업 제목
## 목적
## 맥락
## 목표 사용자·플레이어 경험
## 작업 범위
## 제약·제외 범위
## 산출물
## 완료 기준
## 테스트·검증
## 먼저 읽을 문서와 파일
## 위험·의존성
## 작업 후 보고
```

공식:

```text
목적 → 맥락 → 경험 → 범위 → 제약 → 산출물 → 완료 기준 → 검증
```

## Failure conditions

- 원문을 장문으로 재진술하고 결정은 추가하지 않음
- 사용자 가치 없이 파일·기능 목록만 작성
- 추정을 확정 사실로 표현
- 범위와 제외 범위가 없음
- “깔끔하게”, “최고로”처럼 측정 불가능한 완료 기준
- 구현과 대규모 리팩터링을 한 작업에 혼합
- 이미 확정된 사항을 반복 질문

## Validation scenarios

1. “카드에 사거리도 넣어줘”를 새 자원 추가 없이 UI·데이터·예외·회귀 검증이 포함된 프롬프트로 변환한다.
2. “전투를 개선해줘”에서는 바로 구현하지 않고 핵심 문제와 2~3개 접근법을 제시한다.
3. 완성된 상세 명세를 받으면 불필요한 브레인스토밍 없이 누락된 검증만 보완한다.

Template: `templates/EXECUTABLE_PROMPT.md`
