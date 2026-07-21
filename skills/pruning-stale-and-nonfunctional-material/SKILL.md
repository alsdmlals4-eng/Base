---
name: pruning-stale-and-nonfunctional-material
description: Use when skills, documents, templates, references, tests, or generated artifacts contain duplicated, stale, dead, unreachable, obsolete, or behavior-neutral material that should be reduced without losing unique capabilities, evidence, compatibility, or approved history.
---

# Pruning Stale and Nonfunctional Material

## Core principle

가지치기는 파일 수를 줄이는 목표가 아니라 **행동을 바꾸지 않는 부피와 죽은 경로를 제거하면서 고유 기능·근거·호환성을 보존**하는 작업이다.

## Modes and decisions

`inventory → classify → preserve-unique → prune-approved → verify-no-loss`

`KEEP / MERGE / MOVE_TO_REFERENCE / COMPATIBILITY_STUB / ARCHIVE / DELETE / UNVERIFIED`

## Required inputs

```yaml
active_registry_and_entrypoints:
canonical_sources_and_consumers:
usage_references_and_generation_paths:
unique_capabilities_and_evidence:
compatibility_and_history_requirements:
approval_and_rollback:
```

상세 판정표는 `references/pruning-decision-matrix.md`를 필요할 때만 읽는다.

## Workflow

1. 중복, 도달 불가, 오래된 경로·ID, 보류·백업의 기본 읽기 혼입, 행동을 바꾸지 않는 문장을 찾는다.
2. 삭제 전에 고유 입력·산출물·검증·근거·소비자·호환성을 추출한다.
3. 병합·reference 이동·stub·archive·삭제 중 가장 안전한 처리를 선택한다.
4. 사용자 승인 또는 저장소 계약이 필요한 삭제는 보류한다.
5. 정본 최신성·깨진 링크·Registry·테스트·콜드 스타트·대표 기능을 재검증한다.

## Output contract

```md
## 후보와 사용·참조 근거
## KEEP·MERGE·MOVE·STUB·ARCHIVE·DELETE·UNVERIFIED 판정
## 보존한 고유 기능·근거·호환성
## 실제 제거·축소량
## 정본·링크·라우팅·회귀 결과
## 롤백과 남은 위험
```

## Quality gate

사용 흔적이 없다는 이유만으로 자동 삭제하거나, Git 이력을 활성 백업 파일로 복제하거나, 테스트·문서만 지워 결함을 숨기거나, 고유 기능을 병합 중 잃으면 실패다.

Learning Log: `skills/SKILL_LEARNING_LOG.md`
