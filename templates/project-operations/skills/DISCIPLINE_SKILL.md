---
name: [discipline-skill-name]
description: [이 분야에서 언제 어떤 결과를 만들기 위해 사용하는지]
---

# [Discipline Skill Name]

## Registry metadata

```yaml
skill_id:
layer: discipline
discipline:
status: ACTIVE
load_by_default: false
trigger_tags: []
registry_path: [기획서]/00_프로젝트_허브/SKILL_REGISTRY.json
learning_log:
last_reviewed_at:
last_reviewed_commit:
knowledge_state: OBSERVATION
```

## 분야와 목적

- 분야:
- 해결하는 문제:
- 플레이어·사용자 가치:
- 책임 본책:
- 실제 파일·자산·테스트 범위:

## 사용 조건

- [작성 필요]

## 사용하지 않는 조건

- [작성 필요]

## 필수 입력

```yaml
request:
discipline_bible:
project_skill_map:
skill_registry:
foundation_skills:
current_stage_and_gate:
roadmap_issue_plan:
actual_paths:
approved_assets:
validation_paths:
```

## 먼저 읽을 문서

1. 프로젝트 `AGENTS.md`
2. 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`
3. Active Context·Documentation Map
4. 이 분야 본책
5. `SKILL_REGISTRY.json`과 Project Skill Map
6. 필요한 foundation 의존성
7. 현재 Roadmap·Issue·Plan
8. 실제 코드·데이터·자산·테스트

## Foundation 의존성

| 공용 스킬 | 사용하는 단계 | 이 분야의 추가 규칙 |
|---|---|---|
|  |  |  |

공용 절차 전문을 복사하지 않는다. 실제로 필요한 foundation 스킬만 호출한다.

## 프로젝트 전용 규칙

- 공식 용어·ID:
- 실제 경로:
- 보호할 승인 결정·자산:
- 데이터·상태 소유:
- Quality Bar:
- 금지 방향:
- 프로젝트 전용 예외·폴백:

## 작업 절차

```text
분야 목표·현재 상태 확인
→ 입력·의존성 검수
→ 분야 전문 판단
→ 산출물 제작·수정
→ 다른 분야 계약 확인
→ 자동·수동 검증
→ 본책·상태·PDF·Active Context 영향 확인
→ 실행 결과 Learning Log 기록
→ 근거가 있을 때만 스킬 계약 갱신
```

### 단계별 계약

| 단계 | 입력 | 판단·행동 | 산출물 | 실패·폴백 | 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 산출물

- 필수:
- 선택:
- 생성하지 않는 것:

## Definition of Ready

- [ ] 분야 목표와 사용자 가치가 명확하다.
- [ ] 책임 본책·실제 파일·영향 분야를 확인했다.
- [ ] 승인·구현·검증·미확정이 구분됐다.
- [ ] 기존 승인 자료와 보호 경로를 확인했다.
- [ ] 완료 기준과 검증 방법이 있다.
- [ ] Registry trigger가 현재 작업과 일치한다.

## Definition of Done

- [ ] 승인 범위가 실제 산출물에 반영됐다.
- [ ] 분야 Quality Bar를 증거로 판정했다.
- [ ] 관련 자동·수동 검증을 실행했다.
- [ ] 본책·Manifest·PDF·Active Context 영향이 최신이다.
- [ ] 다른 분야의 입력·출력 계약을 확인했다.
- [ ] 미검증·위험·다음 작업을 분리했다.
- [ ] Learning Log에 결과·실패·예외·사용자 피드백을 기록했다.
- [ ] 스킬 변경 필요 여부와 변경하지 않는 이유를 판정했다.

## 검증

| 종류 | 명령·방법 | 합격 조건 | 증거 |
|---|---|---|---|
| 자동 |  |  |  |
| 수동 |  |  |  |
| 시각·오디오·성능 |  |  |  |
| 사용자·플레이테스트 |  |  |  |

## 실패 조건

- 책임 본책·실제 파일을 확인하지 않음
- trigger와 무관한 작업에서 호출됨
- 사용자 승인 없이 제품 방향·수치·자산 교체
- 다른 분야가 소유한 상태·결과를 변경
- 기존 승인 이미지가 있는데 임의 새 시안 생성
- 검증하지 않은 결과를 완료로 표시
- 공용 절차를 장문 복사해 foundation과 충돌
- 호출 결과를 Learning Log에 기록하지 않음

## 관련 스킬

- 선행:
- 함께 사용:
- 후속:
- 사용하지 않을 대체 경로:

## 학습·갱신 계약

- Learning Log:
- 검토 트리거:
- 마지막 사용일:
- 마지막 검토일·기준 커밋:
- 현재 지식 상태: 관찰/가설/패턴/검증/승격 후보
- 반복된 성공 조건:
- 반복된 실패·예외:
- 이번 실행의 스킬 변경 필요: 예/아니오
- 변경하지 않는 이유:
- 프로젝트 스킬 변경:
- 프로젝트 전용으로 유지:
- Base Method·Skill·Template·Test 환류 후보:
