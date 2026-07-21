# 작업 분해·의존성·실행 순서 모델

이 문서는 `managing-project-intake-and-work-contract`의 `decompose-and-sequence` mode가 사용하는 상세 모델이다. 큰 요청을 체크박스 목록으로 잘게 자르는 것이 아니라, **각 단계가 검증 가능한 결과를 만들고 다음 단계를 안전하게 여는 실행 구조**를 만든다.

## 1. 입력 계약

```yaml
confirmed_work_contract:
current_stage_and_gate:
actual_repository_state:
protected_paths_and_behavior:
available_people_tools_and_permissions:
known_dependencies_and_blockers:
external_deliveries:
milestone_or_deadline:
validation_environment:
rollback_constraints:
```

요구가 확정되지 않았거나 중요한 사용자 결정이 남아 있으면 실행 순서를 확정하지 않는다.

## 2. 분해 단위

하나의 작업 항목은 다음을 모두 가져야 한다.

```yaml
step_id:
outcome:
why_now:
inputs:
files_or_systems:
owner_or_skill:
dependencies:
parallel_with:
protected_scope:
output:
acceptance_criteria:
validation:
rollback:
```

좋은 단계는 “코딩하기”, “문서 수정하기”가 아니라 다음처럼 관찰 가능한 결과를 만든다.

- 저장 Schema와 마이그레이션 계약을 확정한다.
- 최소 정상·실패 fixture가 통과하는 파서를 구현한다.
- 대표 플레이 흐름이 목표 플랫폼에서 끝까지 실행된다.
- 변경된 정본의 모든 소비자와 파생본이 동기화된다.

## 3. 분해 원칙

- 하나의 단계는 하나의 주 결과와 하나의 완료 판정을 가진다.
- 서로 다른 승인 경계·도구·실패 복구가 있으면 분리한다.
- 같은 파일을 여러 단계가 동시에 수정해야 하면 순차화하거나 경계를 재설계한다.
- 구현과 대규모 리팩터링, 원본 변경과 발행, 자동 검증과 사용자 체감 검수는 필요에 따라 분리한다.
- 단계가 너무 커 독립 검증이 불가능하면 더 분해한다.
- 단계가 너무 작아 독립 가치·검증·인수인계가 없으면 합친다.

Scrum Guide는 선택된 작업을 더 작고 정밀한 작업 항목으로 분해하며, 실제 작업자가 수행 방법을 결정하도록 설명한다. Base는 이를 고정 시간 추정 규칙으로 강제하지 않고 **작고 투명하며 검증 가능한 결과**라는 원칙으로 사용한다.

## 4. 의존성 지도

각 관계를 명시적으로 구분한다.

- `BLOCKS`: 완료 전 다음 작업을 시작할 수 없다.
- `INFORMS`: 결과가 다음 결정의 입력이지만 병렬 탐색은 가능하다.
- `USES_OUTPUT`: 생성 파일·Schema·자산·API를 소비한다.
- `SHARES_RESOURCE`: 같은 사람·파일·환경 때문에 충돌할 수 있다.
- `VALIDATES`: 다른 작업 결과를 독립 검증한다.
- `OPTIONAL_FOLLOWUP`: 핵심 완료를 막지 않는 후속이다.

GitHub Issues의 sub-issue와 dependency는 큰 목표를 작은 작업으로 나누고 blocked-by·blocking 관계를 표시하는 데 사용할 수 있다. Milestone은 여러 Issue·PR의 진행을 한 게이트로 묶는 데 사용한다.

## 5. 실행 순서

기본 정렬 기준:

```text
보안·권한·환경 선행 조건
→ 정본·인터페이스·Schema 계약
→ 가장 위험한 가설·기술 불확실성
→ 핵심 사용자·플레이어 경로
→ 데이터·자산·인접 시스템 통합
→ 정상·실패·경계·회귀 검증
→ 문서·발행·참조 최신성
→ 사용자 체감 검수·통합·인수인계
```

다음 기준을 함께 사용한다.

1. `dependency`: 다른 작업을 여는 선행 작업인가?
2. `risk`: 실패했을 때 전체 방향을 바꾸는가?
3. `value`: 가장 빨리 사용자·플레이어 가치를 증명하는가?
4. `reversibility`: 되돌리기 어려운 결정을 너무 일찍 고정하는가?
5. `feedback speed`: 짧은 주기로 실제 결과를 볼 수 있는가?
6. `resource conflict`: 같은 파일·사람·환경을 동시에 요구하는가?

## 6. 병렬화

병렬 작업은 다음을 모두 만족할 때만 허용한다.

- 입력과 책임 원본이 고정됐다.
- 출력 경계와 통합 지점이 명확하다.
- 같은 파일·Schema·자산을 경쟁적으로 수정하지 않는다.
- 각각 독립적으로 검증할 수 있다.
- 한 작업 실패가 다른 작업의 대규모 재작업을 만들지 않는다.

병렬화가 가능한 예:

- 확정된 데이터 계약을 기준으로 코드와 문서 fixture 작성
- 독립된 아트 자산 제작과 테스트 harness 구축
- 대표 정상 경로와 별도 실패·경계 테스트 작성

## 7. 게이트와 재계획

각 묶음 끝에 다음을 둔다.

```yaml
gate:
entry_conditions:
exit_evidence:
if_passed:
if_failed:
if_unverified:
replan_trigger:
```

새 사실·실패·범위 변경이 생기면 이후 단계를 무조건 유지하지 않는다. Sprint Backlog처럼 계획은 목표를 향해 적응 가능해야 하며, 완료 기준과 보호 범위는 추적 가능하게 유지한다.

## 8. 출력 형식

```text
목표·완료 기준
→ 단계 목록
→ 의존성 그래프
→ 병렬 작업 묶음
→ 게이트·검증
→ 위험·롤백
→ 다음 단계 진입 조건
```

## 9. 실패 조건

- 동사만 있는 체크리스트를 만든다.
- 요구 확정 전에 세부 구현 순서를 고정한다.
- 파일·데이터·승인·환경 의존성을 기록하지 않는다.
- 위험한 가설을 뒤로 미루고 쉬운 장식 작업부터 한다.
- 모든 작업을 병렬화해 같은 파일과 정본을 충돌시킨다.
- 테스트·문서·발행을 마지막 한 단계에 몰아넣는다.
- 일정 숫자를 근거 없이 발명한다.
- 선행 단계 실패 후에도 이후 계획을 그대로 실행한다.

## 공식 참고 자료

- Scrum Guide 2020: https://scrumguides.org/scrum-guide.html
- GitHub Docs — About issues, sub-issues and dependencies: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues
- GitHub Docs — Planning and tracking work: https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project
- GitHub Docs — Milestones: https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones
