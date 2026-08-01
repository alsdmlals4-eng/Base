---
name: governing-legacy-retention-and-archives
description: Use when legacy documents, assets, paths, skills, derivatives, evidence, backups, placeholders, or branches need recoverable non-current retention.
---

# Governing Legacy Retention and Archives

## Core principle

레거시 정리는 파일 수를 줄이는 작업이 아니다. **원문을 비우지 않는다.** 고유 정보·활성 참조·호환성·복구 가능성을 보존하면서 현재 정본·구현 권한·기본 라우팅에서 격리한다.

## Skill Modes

- `inventory`: 현행·레거시·파생본과 참조 관계를 변경 없이 수집한다.
- `classify`: lifecycle과 retention classification을 각각 하나씩 판정한다.
- `reconcile`: 승인 범위에서 갱신·통합·호환 stub을 수행한다.
- `archive`: 원문, metadata와 Manifest를 함께 보관한다.
- `delete-approved`: 삭제 gate를 모두 통과한 항목만 제거한다.
- `verify`: 참조·권한·본문·Manifest·복구 경로와 untouched 소비자를 검사한다.

## Required project adapter roles

```text
project_agents
documentation_map
active_context
skill_registry
canonical_sources
archive_root
archive_readme
archive_manifest
protected_paths
legacy_search_roots
generated_derivative_roots
protected_evidence_roots
validators
rollback_reference
```

프로젝트 어댑터는 실제 경로·정본·검증기·예외만 제공한다. 공용 절차를 복제하거나 완화하지 않는다.

## Lifecycle states

```text
CURRENT / UPDATE_IN_PLACE / MERGE_TO_CANONICAL / COMPATIBILITY_STUB
ARCHIVE_HISTORY / DELETE_CANDIDATE / DELETE_APPROVED
KEEP_UNRESOLVED / BLOCKED
```

## Retention classifications

```text
CURRENT_AUTHORITY / COMPATIBILITY_ONLY / ARCHIVE_HISTORY
EVIDENCE_RETENTION / GENERATED_DERIVATIVE
DELETE_PROHIBITED_SECRET / DELETE_APPROVED / KEEP_UNRESOLVED
```

Lifecycle은 처리 단계, retention classification은 보존 책임이다. 둘을 하나의 필드로 혼합하지 않는다. 불명확하면 `KEEP_UNRESOLVED`이며 파일명·날짜만으로 판정하지 않는다.

## Workflow

1. 사용자 지시, 프로젝트 `AGENTS.md`, Documentation Map과 어댑터를 읽는다.
2. 내용·해시·활성 참조·생성 관계·고유 정보·호환 소비자를 조사한다.
3. lifecycle과 retention classification, 대체 정본과 근거를 기록한다.
4. 승인 전에는 대량 이동·통합·삭제·본문 비우기를 수행하지 않는다.
5. 승인 후 가장 보존적인 처리와 metadata·Manifest 갱신을 수행한다.
6. archive 항목은 `active_authority: false`, `implementation_authority: NONE`으로 고정한다.
7. Registry·aliases·Documentation Map·링크·생성기·테스트와 파생본을 갱신한다.
8. 본문·replacement·hash·rollback ref·secret boundary·cold start·직접 라우팅을 검증한다.

상세 계약은 `references/archive-contract.md`, pressure 기록은 `references/pressure-scenarios.md`를 필요한 경우에만 읽는다.

## Content boundaries

- 문서·계획: 원문 보존, metadata·Manifest, 활성 참조를 현재 정본으로 변경.
- inactive Skill: `load_by_default: false`, direct routing 금지, `replaced_by`·alias·test 동시 갱신.
- 증거·테스트: 실패 은폐 목적으로 삭제하지 않고 build·commit·실행 상태와 주장 범위를 보존.
- 생성물: source·generator·input hash 또는 source commit·freshness 기록.
- 코드·runtime asset: 활성 트리를 박물관으로 만들지 않고 Git history·tag·release 등 복구 근거 후 승인 제거.
- 비밀키·token·credential: `DELETE_PROHIBITED_SECRET`; revoke·rotate·remove하며 archive 금지.
- branch: unique commit 감사 → PR 상태 확인 → optional archive tag → 검증 → 삭제 가능 시 제거.

## Deletion gate

다음을 모두 충족하지 않으면 삭제하지 않는다.

- 고유 결정·문장·표·이미지·예외·보류가 정본 또는 archive에 승계됐다.
- 활성·보조·외부 참조가 갱신되거나 compatibility stub이 있다.
- 생성물·Manifest·hash·ID·Schema가 검증됐다.
- 재현 가능한 rollback ref가 있다.
- 사용자 지시 또는 승인 계약의 삭제 근거가 있다.
- 프로젝트 validator와 reference-freshness에 차단 finding이 없다.

## Archive record

```text
archive_id / classification / original_path / current_path
content_sha256 / archived_at / superseded_by / reason
active_authority=false / implementation_authority=NONE
compatibility_consumers / rollback_ref / validation_status
```

## Output contract

```md
## 프로젝트 어댑터·정본·후보
## lifecycle·retention classification·근거
## 보존한 원문·고유 정보·호환성
## metadata·Manifest·활성 권한·라우팅 변경
## 이동·삭제·secret·branch 처리
## PASS·PARTIAL·FAIL·NOT_RUN
## rollback·미확정·차단·남은 위험
```

## Quality gate

- 원문을 비우지 않았고 archive가 current canon·기본 cold start·직접 Skill route에 포함되지 않는다.
- metadata, hash, replacement, rollback ref와 검증 상태가 있다.
- 공용 정책은 Base에만 있고 프로젝트에는 adapter만 있다.
- secret이 archive에 없으며 실행하지 않은 검사·branch 삭제는 `NOT_RUN`이다.

## Failure conditions

빈 파일 퇴역, metadata 없는 backup 이동, Git history만으로 현재 문서 대체, Registry·alias·test 없는 Skill 이동, secret archive, unique commit 감사 없는 branch 삭제는 실패다.

## Related skills

`managing-game-project-operating-system`은 inventory·migration 범위를, `pruning-stale-and-nonfunctional-material`은 stale 후보 분석을 담당한다. 변경 후 `auditing-canonical-reference-freshness`와 `reviewing-and-validating-project-changes`를 사용한다.

## Learning Log

`skills/governing-legacy-retention-and-archives/LEARNING_LOG.md`
