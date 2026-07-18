---
name: [foundation-skill-name]
description: [여러 분야가 공통으로 사용하는 실행 조건과 목적]
---

# [Foundation Skill Name]

## Registry metadata

```yaml
skill_id:
layer: foundation
discipline: project-operations
status: ACTIVE
load_by_default: false
trigger_tags: []
registry_path: [기획서]/00_프로젝트_허브/SKILL_REGISTRY.json
learning_log:
last_reviewed_at:
last_reviewed_commit:
knowledge_state: OBSERVATION
```

## 목적

- 해결하는 공용 문제:
- 여러 분야에서 재사용하는 이유:
- 이 스킬이 직접 책임하지 않는 분야 고유 판단:

## 사용 조건

- [작성 필요]

## 사용하지 않는 조건

- [작성 필요]

## 필수 입력

```yaml
request:
project_start_here:
documentation_map:
active_context:
project_skill_registry:
primary_discipline:
affected_disciplines:
current_issue_or_plan:
actual_files_and_tests:
```

## 먼저 읽을 문서

1. 프로젝트 `AGENTS.md`
2. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
3. Documentation Map·Active Context
4. `SKILL_REGISTRY.json`
5. 현재 작업의 분야 본책
6. 실제 파일·테스트
7. 관련 Base Method·Skill

## 작업 절차

```text
호출 trigger 확인
→ 입력 검수
→ 현행 책임 원본 확인
→ 공용 판단·절차 수행
→ 분야 스킬에 필요한 출력 전달
→ 검증
→ 문서·상태 영향 확인
→ 실행 결과 Learning Log 기록
→ 근거가 있을 때만 스킬 계약 갱신
```

## 산출물

- [작성 필요]

## Definition of Ready

- [ ] 목적·범위·책임 분야가 명확하다.
- [ ] 현행 책임 원본과 실제 대상이 확인됐다.
- [ ] Registry trigger가 현재 작업과 일치한다.
- [ ] 완료 기준과 검증이 있다.

## Definition of Done

- [ ] 산출물이 실제 작업에 사용 가능하다.
- [ ] 분야 고유 결정을 임의로 만들지 않았다.
- [ ] 검증 결과와 미검증을 분리했다.
- [ ] 관련 지도·상태·스킬을 갱신했다.
- [ ] Learning Log에 실행 결과와 변경 필요성을 기록했다.

## 검증

- 자동:
- 수동:
- 사용자 확인:
- 선택적 호출 검수:

## 실패 조건

- trigger와 무관한 작업에서 호출됨
- 공용 스킬이 프로젝트 세계관·수치·승인 자산을 소유함
- 같은 공용 절차를 분야 스킬에 장문 복사하게 함
- 실제 파일·책임 원본을 확인하지 않음
- 실행하지 않은 검증을 통과 처리
- 모든 작업에서 기본 호출되도록 설정함
- 호출 결과를 Learning Log에 기록하지 않음

## 관련 스킬

- 선행 foundation:
- 후속 분야 스킬:
- 후속 검증·발행·인수인계 스킬:
- 대체 스킬:

## 학습·갱신

- Learning Log:
- 검토 트리거:
- 마지막 사용일:
- 마지막 검토일·기준 커밋:
- 현재 지식 상태: 관찰/가설/패턴/검증/승격 후보
- 이번 실행의 스킬 변경 필요: 예/아니오
- 변경하지 않는 이유:
- 프로젝트 전용으로 남길 내용:
- Base Method·Skill·Template·Test 환류 후보:
