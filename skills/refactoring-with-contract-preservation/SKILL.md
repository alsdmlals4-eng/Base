---
name: refactoring-with-contract-preservation
description: Use when code, documents, data structures, automation, or a skill system must be structurally improved by reducing duplication and complexity while preserving approved behavior, interfaces, data compatibility, outputs, and user-visible capabilities.
---

# Refactoring with Contract Preservation

## Core principle

리팩토링은 기능을 다시 설계하는 일이 아니라 **승인된 동작과 계약을 유지한 채 구조를 개선**하는 일이다. 기능 추가·삭제·정책 변경과 같은 PR에 섞지 않는다.

도달 불가·오래된 자료의 제거는 `pruning-stale-and-nonfunctional-material`, SKILL.md의 조건부 상세 분리는 `simplifying-skill-bodies`, 의도적 기능 변경은 별도 작업 계약, 최종 diff·런타임·회귀 증거는 `reviewing-and-validating-project-changes`가 책임진다.

## Modes

`baseline-contract` → `smell-audit` → `refactor` → `regression-validate` → `report`

## Required inputs

```yaml
approved_behavior_and_scope:
public_interfaces_and_outputs:
data_schema_and_compatibility:
current_implementation:
baseline_tests_and_examples:
protected_paths_assets_and_decisions:
validation_environment:
```

## Workflow

1. 정상·실패·경계 동작, API·파일·Schema·출력·성능 기준을 baseline으로 고정한다.
2. 중복, 긴 함수·문서, 복잡한 조건, 강결합, 책임 혼합, 잘못된 추상화를 근거로 찾는다.
3. 가장 작은 단계로 이동·추출·이름 정리·중복 통합을 수행한다.
4. 단계마다 baseline과 실제 결과를 비교한다.
5. 구조 개선과 동작 변경을 diff·보고에서 분리한다.

상세 냄새·변환·증거표는 `references/refactoring-checklist.md`를 필요할 때만 읽는다.

## Output contract

```md
## 보존 계약과 baseline
## 발견한 구조 문제와 근거
## 수행한 리팩토링
## 기능·인터페이스·데이터 보존 증거
## 회귀·성능·호환성 결과
## 의도적 동작 변경 없음 또는 별도 변경 목록
## 남은 위험·미검증
```

## Quality gate

동작을 설명할 baseline이 없거나, 리팩토링 명목으로 기능·정책·Schema를 바꾸거나, 테스트를 삭제해 통과시키거나, 추상화와 파일 수만 늘리면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
