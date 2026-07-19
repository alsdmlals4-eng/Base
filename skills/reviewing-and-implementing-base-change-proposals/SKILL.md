---
name: reviewing-and-implementing-base-change-proposals
description: Review, approve, defer, reject, or implement a Base change proposal stored under [수정제안서]. Use when the user asks to evaluate a project-to-Base promotion proposal or explicitly authorizes implementation of an existing BCP; require durable approval evidence before changing active Base methods, skills, templates, tools, schemas, or tests.
---

# Reviewing and Implementing Base Change Proposals

## Core contract

제안 검토와 Base 구현을 분리한다. `SUBMITTED` 제안은 활성 Base 규칙이 아니며 사용자 승인 근거가 없으면 `[수정제안서]` 밖을 변경하지 않는다.

## Read first

1. `[수정제안서]/PROPOSAL_REGISTRY.json`
2. 대상 `PROPOSAL.md`와 evidence
3. 제안이 변경하려는 현행 Base 책임 원본·테스트
4. 출처 프로젝트의 기준 커밋과 실제 검증 근거

필요한 파일·도구·인증·권한이 없으면 필요한 이유, 설치·적용 방법, 확인 명령과 최소 권한을 사용자에게 요청한다. 확인하지 못한 근거는 `[미검증]`으로 남긴다.

## Review

1. 제안 ID·경로·상태와 출처 커밋을 확인한다.
2. 프로젝트 이름·경로·수치·자산을 공용 규칙과 분리한다.
3. 기존 Base 책임과 중복·충돌·대체 관계를 찾는다.
4. 성공 증거뿐 아니라 실패 조건·반례·비사용 조건을 확인한다.
5. 보안·라이선스·비용·호환성·마이그레이션·롤백을 평가한다.
6. `APPROVED_FOR_IMPLEMENTATION`, `DEFERRED`, `REJECTED` 중 하나를 사용자에게 제안한다.
7. 사용자의 명시적 결정과 근거 위치를 Registry의 `approval_ref`에 기록한다.

## Implement approved scope

1. `status=APPROVED_FOR_IMPLEMENTATION`과 비어 있지 않은 `approval_ref`를 확인한다.
2. 새 구현 브랜치·PR을 만들고 제안 PR과 분리한다.
3. 제안의 승인 범위·제외 범위·보호 대상을 작업 계약으로 옮긴다.
4. 필요한 Method·Skill·Template·Tool·Schema·Test만 변경한다.
5. 기준·대표·변형·반례·회귀 시나리오를 검증한다.
6. 제안서에 구현 PR과 실제 검증을 연결하고 `IMPLEMENTED`로 갱신한다.
7. 실패하면 활성 Base를 부분 반영 상태로 두지 말고 롤백·복구 방법을 보고한다.

사용자가 직접 승인한 요청은 제안서 없이도 작업 계약이 될 수 있다. 다만 프로젝트에서 자동 추출한 승격 후보는 항상 제안 전용 PR부터 시작한다.

## Failure conditions

- 신규 제안과 활성 Base 변경을 같은 PR에 넣음
- 사용자 승인 없이 `APPROVED_FOR_IMPLEMENTATION`으로 변경
- 출처 프로젝트의 고유 코드·아트·수치·경로를 공용 원칙으로 복사
- 한 번의 성공 또는 미검증 추측을 검증된 스킬로 승격
- 거절·보류·구현된 제안 기록을 삭제
- 실행하지 않은 테스트나 권한 확인을 통과로 표시

## Output

```md
## 제안 판정
## 공용화 가능한 원리와 프로젝트 전용 요소
## 중복·충돌·반례
## 승인 상태와 근거
## 승인된 구현 범위·제외 범위
## 검증·롤백
## Registry·제안서·구현 PR 연결
```
