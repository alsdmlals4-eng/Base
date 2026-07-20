---
name: maintaining-project-context-and-handoff
description: Use when a game-project task changes current status, next work, risks, decisions, gates, or ownership and the repository must be compacted so a new chat or worker can resume without reading past conversations.
---

# Maintaining Project Context and Handoff

## Core principle

Active Context와 Handoff는 다른 책임 원본을 복제하는 장문 문서가 아니라 **현재 상태, 읽기 순서, 미완료 작업과 위험을 연결하는 압축 라우터**다.

## 전역 handoff와의 경계

이 스킬의 Handoff는 저장소 안의 현행 상태 라우터다. 전역 `handoff`는 운영체제 임시 폴더에 만드는 대화 인수인계 문서이고, 전역 `resume-work`는 AgentMemory에서 이전 작업을 찾는 기능이다. 임시 대화 문서를 프로젝트의 책임 원본으로 등록하거나 Active Context를 대체하지 않는다.

## Use when

- L1 이상 작업으로 현재 구현·검증·우선순위가 바뀌었다.
- 단계·게이트·Roadmap·다음 작업이 바뀌었다.
- 세션, 담당자, AI, 브랜치 또는 마일스톤 경계에서 인수인계가 필요하다.
- 새 채팅이 과거 대화 없이 작업을 재개해야 한다.
- Active Context가 실제 파일이나 본책과 불일치한다.

## Do not use when

- 저장소 상태가 바뀌지 않은 단순 설명·브레인스토밍이다.
- 오탈자처럼 다음 작업자에게 영향을 주지 않는 L0 수정이다.
- 분야 본책이나 Roadmap을 대신하는 거대한 요약본을 만들려는 경우다.
- 미검증 내용을 확정 상태로 압축하려는 경우다.

## Required inputs

```yaml
project_agents:
project_start_here:
documentation_map:
active_context:
handoff:
current_stage_and_gate:
roadmap_issue_plan:
changed_files:
validation_results:
remaining_risks:
next_work:
invoked_skills:
```

## Read first

1. 프로젝트 `AGENTS.md`
2. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
3. Documentation Map
4. 현재 Active Context·Handoff
5. 변경된 분야 본책과 실제 파일
6. Roadmap·Issue·Plan·검증 결과

## Process

### 1. Runtime truth 확인

실제 코드·데이터·자산·테스트와 문서 상태를 비교한다. 확인하지 못한 결과는 `[미검증]`으로 남긴다.

### 2. 상태 분리

다음을 혼용하지 않는다.

- 확정
- 구현
- 검증
- 진행 중
- 미확정
- 보류
- 불일치

### 3. 책임 원본 갱신

먼저 해당 분야 본책, Roadmap, Decision, Manifest와 Project Skill을 갱신한다. Active Context에 전문을 복사하지 않고 경로와 현재 차이만 기록한다.

### 4. Active Context 압축

다음만 유지한다.

- 프로젝트 한 줄 방향과 현재 단계
- 이번 작업에서 실제로 바뀐 것
- 현재 구현·검증 상태
- 가장 중요한 미확정·위험
- 다음 우선 작업과 선행 조건
- 변경 금지·보호 경로
- 먼저 읽을 3~7개 책임 원본
- 호출할 스킬과 검증 경로

### 5. Handoff 작성

```text
현재 상태
→ 이번 작업 결과
→ 남은 작업
→ 위험·미검증
→ 다음 작업자의 첫 행동
→ 검증·롤백
```

과거 대화 전체, 도구 호출 로그, 이미 본책에 반영된 전문은 포함하지 않는다.

### 6. 콜드 스타트 검수

새 작업자가 10분 안에 다음을 찾는지 확인한다.

- 무엇을 만드는가?
- 현재 어디까지 됐는가?
- 다음 작업은 무엇인가?
- 무엇을 바꾸면 안 되는가?
- 관련 본책·스킬·실제 파일·검증은 어디인가?

## Output contract

```md
## 현재 상태
## 이번 작업 결과
## 확정·구현·검증·미확정
## 다음 작업과 선행 조건
## 보호 범위
## 먼저 읽을 책임 원본
## 호출 스킬
## 검증·미검증·롤백
```

## Definition of Ready

- [ ] 실제 변경 파일과 검증 결과를 확인했다.
- [ ] 관련 본책·Roadmap·Skill의 책임을 식별했다.
- [ ] 다음 작업과 미완료 범위가 있다.

## Definition of Done

- [ ] Active Context가 실제 상태와 일치한다.
- [ ] Handoff가 다음 작업자의 첫 행동을 명확히 한다.
- [ ] 전문 중복 없이 책임 원본을 연결한다.
- [ ] `[백업]`, `[보류]`, 제거 후보가 기본 읽기에 혼입되지 않는다.
- [ ] 콜드 스타트 질문에 답할 수 있다.
- [ ] 인수인계 실패나 누락을 Learning Log에 기록했다.

## Validation

- 본책과 Active Context의 상태가 충돌하지 않는가?
- 실제 파일·검증 경로가 존재하는가?
- 다음 작업의 선행 조건과 완료 기준이 명확한가?
- 새 채팅이 과거 대화 없이 작업을 시작할 수 있는가?
- 기본 읽기 문서가 과도하게 많지 않은가?

## Failure conditions

- Active Context가 분야 본책의 복제본이 됨
- 과거 대화나 도구 로그 전체를 필수 컨텍스트로 만듦
- 실제 확인 없이 구현·검증 완료로 기록함
- 다음 작업·위험·보호 범위를 누락함
- 오래된 경로나 보류 문서를 기본 읽기에 남김

## Learning contract

다음이 발생하면 학습 기록을 갱신한다.

- 새 채팅이 핵심 상태나 다음 작업을 찾지 못함
- Active Context와 실제 파일이 반복 충돌함
- 필수 문서가 너무 많아 콜드 스타트가 느림
- 인수인계 후 동일 질문이 반복됨
- 롤백·검증 경로가 부족해 작업이 중단됨
