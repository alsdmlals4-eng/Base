---
name: governing-legacy-retention-and-archives
description: Use when current and legacy documents, assets, paths, skill packages, generated derivatives, or historical records must be classified, merged, retained, archived, compatibility-preserved, or approved for deletion.
---

# Governing Legacy Retention and Archives

## Core principle

레거시 정리는 파일 수를 줄이는 작업이 아니라 **현재 정본·고유 정보·활성 참조·복구 가능성**을 보존하면서 책임을 명확히 하는 작업이다. 프로젝트 경로와 검증기는 프로젝트 어댑터에서 읽고, 공용 판정 규칙은 이 Skill만 책임진다.

## Skill Modes

- `inventory`: 현행·레거시·파생본과 참조 관계를 변경 없이 수집한다.
- `classify`: 각 항목의 수명주기 상태와 대체 정본을 판정한다.
- `reconcile`: 승인된 범위에서 갱신·통합·호환 stub을 수행한다.
- `archive`: 역사적 가치가 있는 항목을 인덱스와 함께 보관한다.
- `delete-approved`: 삭제 승인과 모든 안전 조건이 충족된 항목만 제거한다.
- `verify`: 참조·정본·파생본·복구 경로와 untouched 소비자를 재검증한다.

## Required project adapter roles

```text
project_agents
documentation_map
active_context
skill_registry
canonical_sources
archive_root
protected_paths
legacy_search_roots
validators
rollback_reference
```

프로젝트 어댑터는 경로·정본·검증기·예외만 제공한다. 이 Skill의 판정 정책이나 절차를 프로젝트에 복제하지 않는다.

## Lifecycle states

```text
CURRENT
UPDATE_IN_PLACE
MERGE_TO_CANONICAL
COMPATIBILITY_STUB
ARCHIVE_HISTORY
DELETE_CANDIDATE
DELETE_APPROVED
KEEP_UNRESOLVED
BLOCKED
```

## Workflow

1. 최신 사용자 지시와 프로젝트 `AGENTS.md`를 먼저 읽는다.
2. 어댑터에서 Documentation Map, 정본, 보호 경로, 아카이브 위치와 검증기를 해석한다.
3. 파일명만 보지 말고 내용·해시·활성 참조·생성 관계·고유 정보를 조사한다.
4. 각 항목을 수명주기 상태 하나로 분류하고 대체 정본과 근거를 기록한다.
5. 충돌·미확정·고유 정보는 `KEEP_UNRESOLVED` 또는 `BLOCKED`로 분리한다.
6. 사용자 승인 전에는 대량 이동·통합·삭제를 수행하지 않는다.
7. 승인 후 `UPDATE_IN_PLACE → MERGE_TO_CANONICAL → COMPATIBILITY_STUB → ARCHIVE_HISTORY → DELETE_APPROVED` 순으로 가장 보존적인 처리를 선택한다.
8. Registry, Documentation Map, 링크, 생성기, Manifest, 테스트와 파생본을 갱신한다.
9. 프로젝트 어댑터의 검증기를 실행하고 변경됐어야 하지만 untouched인 소비자를 검사한다.
10. 복구 경로와 남은 위험을 결과에 남긴다.

## Deletion gate

다음을 모두 충족하지 않으면 삭제하지 않는다.

- 고유 결정·문장·표·이미지·예외·보류가 정본 또는 아카이브에 승계됐다.
- 활성·보조·외부 참조가 새 경로로 갱신되거나 호환 stub이 있다.
- 생성물·Manifest·해시·ID·Schema가 검증됐다.
- Git 커밋·태그·백업 등 재현 가능한 복구 경로가 있다.
- 사용자 지시 또는 승인된 작업 계약에 삭제 근거가 있다.
- 프로젝트 검증기와 reference-freshness에 차단 finding이 없다.

## Archive contract

아카이브는 폐기물이 아니라 의사결정 이력이다. 각 항목에 다음을 기록한다.

```text
original_path
archived_path
lifecycle_state
reason
canonical_replacement
active_reference_status
unique_information_status
archived_at
rollback_reference
```

## Output contract

```md
## Work Mode·Skill Mode
## 프로젝트 어댑터와 정본
## 레거시 인벤토리
## 상태·근거·대체 정본 처리표
## 실제 갱신·통합·stub·아카이브·삭제
## 보존한 고유 정보와 보호 대상
## 참조·파생본·복구 검증
## PASS·PARTIAL·FAIL·NOT_RUN
## 미확정·차단·남은 위험
```

## Quality gate

- 프로젝트 경로를 Skill 본문에 하드코딩하지 않았다.
- 파일명이나 오래된 날짜만으로 레거시를 판정하지 않았다.
- 공용 정책은 Base에만 있고 프로젝트에는 어댑터만 있다.
- 승인 전 쓰기와 승인 후 처리를 구분했다.
- 삭제보다 통합·stub·아카이브를 우선 검토했다.
- 실행하지 않은 검증을 통과로 보고하지 않았다.

## Do not use

- 현재 정본이 명확한 단일 파일의 오탈자 수정.
- 레거시 수명주기와 무관한 신규 기능 구현.
- 프로젝트 운영체계 전체 설치·대규모 구조 마이그레이션. 이 경우 `managing-game-project-operating-system`을 사용한다.

## Learning Log

오삭제 위험, 고유 정보 발견, 호환 stub 필요, 아카이브 복구 성공·실패, 반복되는 레거시 유형과 검증 누락을 `skills/SKILL_LEARNING_LOG.md`에 기록한다.
