---
name: diagnosing-game-engine-runtime-failures
description: Use when a Godot, Unity, or comparable game-engine project crashes, throws errors, loads incorrectly, loses signals or references, corrupts state, or behaves differently at runtime and needs evidence-based reproduction, isolation, minimal repair, and revalidation.
---

# Diagnosing Game Engine Runtime Failures

## Core principle

증상을 추측으로 고치지 않는다. 같은 조건에서 재현하고 로그·Scene·Node·Component·Signal·데이터·상태 흐름을 좁힌 뒤 가장 작은 수정으로 원인을 제거한다.

이 Skill은 엔진 런타임 원인 격리와 최소 수정을 책임진다. 일반 구조 개선은 `refactoring-with-contract-preservation`, 변경 전체의 정적·접근성·성능·호환성·PR 완료 판정은 `reviewing-and-validating-project-changes`가 책임진다.

## Modes

`reproduce` → `isolate` → `form-hypotheses` → `fix-minimally` → `revalidate` → `prevent`

## Required inputs

```yaml
engine_version_platform_and_build:
reproduction_steps_expected_actual:
logs_stack_trace_and_screenshots:
scene_prefab_node_component_structure:
scripts_signals_events_and_data:
recent_diff_and_known_good_baseline:
validation_environment:
```

상세 런타임 체크리스트는 `references/runtime-debugging-checklist.md`를 필요할 때만 읽는다.

## Output contract

```md
## 재현 조건과 관찰 결과
## 가장 가능성 높은 원인과 반증
## 확인한 Scene·Node·Signal·Component·데이터
## 최소 수정과 영향 범위
## 정상·실패·경계·저장·플랫폼 재검증
## 재발 방지 테스트·문서·규칙
## 미검증·사용자 엔진 확인 항목
```

## Quality gate

재현 없이 대규모 수정하거나, 오류 메시지만 숨기거나, 엔진 버전·플랫폼·최근 diff를 무시하거나, 수정 후 원래 재현 절차와 인접 경로를 다시 확인하지 않으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
