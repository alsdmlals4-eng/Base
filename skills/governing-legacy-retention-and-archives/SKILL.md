---
name: governing-legacy-retention-and-archives
description: Use when superseded documents, inactive skills, historical evidence, generated derivatives, backup folders, blank placeholders, or merged branches must remain recoverable without retaining current implementation authority.
---

# Governing Legacy Retention and Archives

## Core principle

과거 자료는 지우거나 원문을 비워서 정리하지 않는다. 고유 결정·증거·호환성과 복구 근거를 보존하되, 현재 정본·구현 권한·기본 라우팅에서는 명확히 격리한다.

## When to use

- 구형 문서·계획·생성물을 `[백업]`, `backup`, `archive`로 옮기려 한다.
- inactive Skill, 과거 ID·경로 또는 호환 stub을 유지해야 한다.
- 증거를 남기되 현재 구현 권한을 제거해야 한다.
- 파일 내용을 비우는 방식이 제안됐다.
- 병합·폐기 브랜치의 tag·삭제 경계를 결정한다.

일반 정본 편집, 단순 stale-reference 검색, 임시 빌드 산출물 청소에는 사용하지 않는다. 비밀정보는 보존 대상이 아니다.

## Required inputs

```yaml
candidate_paths:
current_authority_sources:
consumers_and_references:
unique_material:
project_archive_adapter:
approval_and_rollback:
validation_commands:
```

## Classification

각 후보는 정확히 하나의 주 분류를 가진다.

- `CURRENT_AUTHORITY`
- `COMPATIBILITY_ONLY`
- `ARCHIVE_HISTORY`
- `EVIDENCE_RETENTION`
- `GENERATED_DERIVATIVE`
- `DELETE_PROHIBITED_SECRET`
- `DELETE_APPROVED`
- `KEEP_UNRESOLVED`

판단이 불명확하면 `KEEP_UNRESOLVED`다. 파일명에 `old`, `v2`, `final` 또는 날짜가 있다는 이유만으로 퇴역시키지 않는다.

## Workflow

```text
inventory and authority check
→ unique material and consumer audit
→ one primary classification
→ retention location and metadata
→ remove active authority and default routing
→ update references, registry, aliases and manifests
→ validate content, rollback, cold start and secrets boundary
→ report PASS/PARTIAL/FAIL/NOT_RUN
```

- 아카이브 문서는 원문을 비우지 않는다.
- 아카이브 레코드는 `active_authority: false`, `implementation_authority: NONE`을 사용한다.
- 승인·rollback ref·참조 검증 없이 삭제하지 않는다.
- 폴더명만으로 현재 권한 제거를 주장하지 않는다.
- 프로젝트의 `ARCHIVE_RETENTION_ADAPTER.json`이 경로와 검증 명령을 소유한다.

## Content-type boundaries

- 문서: 원문 보존, metadata·Manifest, 활성 참조를 대체 정본으로 갱신.
- Skill: 필요하면 inactive compatibility로 유지하고 direct routing을 금지.
- 테스트·증거: 실패 은폐 목적으로 삭제하지 않으며 주장 근거와 실행 상태를 보존.
- 생성물: source·generator·commit/hash·freshness를 기록.
- 코드·runtime asset: 활성 트리를 박물관으로 만들지 말고 Git history·tag·release로 복구 가능성을 확보한 뒤 승인 제거.
- 비밀정보: `DELETE_PROHIBITED_SECRET`; 폐기·회수·보안 절차를 적용하고 아카이브하지 않는다.
- branch: unique commit 감사 → PR 상태 확인 → optional archive tag → 검증 → 삭제 가능 시 branch 삭제.

상세 계약은 `references/archive-contract.md`를 필요한 경우에만 읽는다.

## Output contract

```md
## 후보·현재 권한·소비자
## 분류와 근거
## 보존한 원문·고유 정보·호환성
## archive metadata와 Manifest 변경
## 제거한 활성 권한·라우팅·참조
## 삭제·이동·비밀정보 차단
## 검증 결과: PASS/PARTIAL/FAIL/NOT_RUN
## rollback과 남은 위험
```

## Quality gate

- 원문 본문과 고유 증거가 보존됐다.
- archive가 현재 정본·기본 콜드 스타트·직접 Skill 라우팅에 포함되지 않는다.
- metadata, hash, replacement, rollback ref와 검증 상태가 있다.
- 비밀정보가 archive에 없다.
- 실행하지 않은 검사와 branch 삭제는 `NOT_RUN`이다.

## Failure conditions

- 빈 파일을 보존이라고 주장함.
- metadata 없는 범용 backup 폴더로 대량 이동함.
- Git history만을 활성 문서의 대체물로 사용함.
- Registry·alias·test 없이 inactive Skill 경로를 이동함.
- unique commit 감사 없이 branch를 삭제함.
- 비밀키·token·자격증명을 archive함.

## Related skills

- **REQUIRED PRECEDING SKILL:** `managing-game-project-operating-system` for inventory or migration scope.
- **REQUIRED CLASSIFICATION SUPPORT:** `pruning-stale-and-nonfunctional-material` for stale/dead candidate analysis.
- **REQUIRED VALIDATION:** `auditing-canonical-reference-freshness` and `reviewing-and-validating-project-changes` after changes.

## Learning Log

`skills/SKILL_LEARNING_LOG.md`
