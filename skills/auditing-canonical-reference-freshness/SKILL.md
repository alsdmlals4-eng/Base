---
name: auditing-canonical-reference-freshness
description: Use when a patch, rename, consolidation, schema change, document update, generator change, or release may leave active files pointing to obsolete paths, superseded skill IDs, stale policies, outdated generated outputs, or canonical-source changes that were not propagated to dependent files.
---

# Auditing Canonical Reference Freshness

## Core principle

최신 파일이 존재하는 것만으로는 충분하지 않다. **정본 변경이 모든 활성 소비자·참조·파생본·검사·템플릿에 전파됐는지** 확인하고, 오래된 파일·경로·Skill ID·Schema·정책·해시를 현행처럼 사용하는 상태를 차단한다.

이 Skill은 일반 변경 검증을 대체하지 않는다. `reviewing-and-validating-project-changes`가 전체 검증을 오케스트레이션하고, 이 Skill은 참조 최신성·변경 전파·파생본 동기화라는 고유 검증을 제공한다.

## Use when

- 파일·폴더·Skill ID·문서 ID·Schema·명령·도구 경로를 추가·이동·통합·삭제·교체했다.
- 정본 문서·Registry·운영 모델·정책·템플릿·생성기를 변경했다.
- 패치는 작아 보이지만 여러 문서·코드·테스트가 같은 이름·경로·계약을 참조한다.
- 기존 파일과 최신 파일이 함께 남아 무엇이 현행인지 불명확하다.
- 발행본·Manifest·자동 생성 파일이 원본보다 오래됐을 가능성이 있다.
- PR·릴리스·마이그레이션 전에 갱신 누락과 오래된 참조를 찾아야 한다.
- 새 채팅이나 작업자가 오래된 파일을 정본으로 선택하는 문제가 발생했다.

## Do not use when

- 외부 참조가 없는 L0 오탈자다.
- 변경된 정본·경로·계약이 없고 동일 입력의 검사를 재실행한다.
- 문서 내용의 품질·게임 재미·UI 시각 품질만 평가하려 한다.
- Git 이력·과거 PR·Change Log의 역사적 표현까지 현행 표현으로 강제하려 한다.

## Modes

- `impact-map`: 변경된 정본과 직접·간접 소비자를 계산한다.
- `reference-scan`: 오래된 경로·ID·버전·명령·용어와 고아 참조를 찾는다.
- `content-drift`: 동일 책임을 설명하는 활성 파일들의 정책·상태·용어 충돌을 찾는다.
- `derivative-freshness`: PDF·DOCX·생성 파일·Manifest·해시·렌더 상태를 확인한다.
- `propagation-gap`: 변경됐어야 하지만 diff에 포함되지 않은 소비자·테스트·템플릿을 찾는다.
- `closure-report`: 결함·허용된 Legacy·미검증·필수 후속 갱신을 보고한다.

하나의 변경 검수에서는 `impact-map → reference-scan → 필요한 추가 mode → closure-report` 순서로 실행한다.

## Required inputs

```yaml
baseline_branch_and_commit:
head_branch_and_commit:
changed_files_or_diff:
canonical_sources: []
registries_and_documentation_maps: []
known_renames_and_replacements: []
legacy_aliases_and_allowed_history_paths: []
generated_outputs_and_manifests: []
active_entrypoints_and_templates: []
validation_and_test_paths: []
ignore_or_history_globs: []
repository_search_roots: []
```

정본과 소비자 관계가 등록돼 있지 않으면 실제 참조 검색으로 후보를 만들되, 추정 관계를 확정 사실처럼 기록하지 않는다.

## Finding types

- `STALE_REFERENCE`: 활성 파일이 폐기·이동·교체된 경로·ID·명령을 참조한다.
- `ORPHANED_REFERENCE`: 참조 대상이 존재하지 않거나 Registry에서 비활성이다.
- `MISSING_PROPAGATION`: 정본이 바뀌었지만 영향 소비자·템플릿·테스트가 갱신되지 않았다.
- `CONFLICTING_SOURCE`: 동일 책임을 가진 활성 파일들이 서로 다른 정책·상태·값을 주장한다.
- `DERIVATIVE_STALE`: 파생본·Manifest·해시·렌더 상태가 현재 원본·생성기와 맞지 않는다.
- `DUPLICATE_ACTIVE_SOURCE`: 같은 질문에 둘 이상의 현행 정본이 존재한다.
- `LEGACY_REFERENCE_ALLOWED`: 과거 이력·Alias·Migration 문서에서 의도적으로 유지한다.
- `UNVERIFIED_DEPENDENCY`: 참조·생성 관계를 확인할 도구·환경·권한이 없다.

## Process

### 1. Freeze the baseline

- 비교할 base·head 커밋과 실제 diff를 고정한다.
- 이름이 같은 로컬 파일이나 과거 대화가 아니라 해당 커밋의 파일을 기준으로 한다.
- 추가·수정·삭제·이동을 구분한다.

### 2. Identify canonical-source changes

다음 변경을 정본 영향으로 우선 분류한다.

- Registry·Documentation Map·START_HERE·AGENTS·운영 모델.
- 등록된 Markdown 또는 JSON 책임 원본.
- Schema·공개 인터페이스·데이터 ID·파일 경로.
- Skill ID·mode·trigger·상태·Legacy Alias.
- 생성기·발행 정책·Manifest 계약.
- 프로젝트가 명시한 안정 경로와 승인 자산.

### 3. Build an impact map

```text
변경된 정본
→ 명시적으로 등록된 소비자
→ 실제 문자열·링크·import·ID 참조
→ 생성된 파생본·Manifest
→ 검사·테스트·Workflow
→ 시작 문서·템플릿·Handoff
```

각 소비자를 `must-update / inspect / history-only / unrelated`로 분류한다.

### 4. Scan stale and orphaned references

- 삭제·이동 전 경로와 이전 Skill·문서 ID를 검색한다.
- Registry가 가리키는 실제 파일이 존재하고 활성 상태인지 확인한다.
- 새 파일이 생겼지만 START_HERE·Documentation Map·Registry가 여전히 이전 원본을 가리키는지 확인한다.
- 코드 import, JSON path, Markdown link, 명령 예시, Workflow path filter, 테스트 fixture를 포함한다.
- Legacy Alias·Change Log·과거 case처럼 허용된 이력 경로는 별도 분류한다.

### 5. Detect content drift

문자열이 최신이어도 의미가 오래됐을 수 있다.

- 같은 정책을 설명하는 활성 문서의 mode·상태·완료 기준이 일치하는가?
- 숫자·버전·지원 범위·활성 Skill 수·발행 정책이 서로 다른가?
- 새 통합 Skill이 생겼는데 이전 실행 순서를 설명하는 문서가 남았는가?
- 새 정본이 생겼는데 복제 문서가 독립 정본처럼 유지되는가?

자동으로 판정하기 어려운 의미 충돌은 근거 문장과 책임 원본을 함께 제시해 수동 검토 대상으로 남긴다.

### 6. Verify derivative freshness

- Manifest의 source·generator·output 해시가 현재 파일과 일치하는가?
- 정책이 요구하는 PDF·선택 DOCX·assets가 CURRENT인가?
- 생성기 변경 뒤 파생본이 재생성됐는가?
- Registry 변경 뒤 Skill Map·Manifest가 갱신됐는가?
- 실제 렌더·실행이 필요한 검증을 파일 존재로 대체하지 않았는가?

분야별 발행 검증은 `managing-design-documents: validate` 또는 운영체계 `verify` mode의 고유 도구를 사용한다.

### 7. Find propagation gaps

변경 파일만 보지 않고 **변경되지 않은 영향 파일**을 찾는다.

```yaml
source_change:
expected_consumers: []
changed_consumers: []
untouched_consumers: []
reason_each_consumer_should_or_should_not_change:
```

`untouched`가 곧 결함은 아니다. 새 정본과 이미 일치하거나 참조하지 않는다는 근거가 있으면 통과한다.

### 8. Run automated checks

Base 기본 검사:

```text
python tools/check_canonical_reference_freshness.py \
  --config .github/reference-freshness.json \
  --base <base-sha> --head <head-sha>
```

자동 검사는 다음을 우선 담당한다.

- Legacy Skill ID와 삭제 경로의 활성 파일 잔존.
- 필수 진입 문서의 정본 링크 누락.
- 정본 변경과 Registry·Learning Log·테스트·템플릿의 coupled-change 누락.
- 프로젝트가 등록한 금지된 구버전 토큰.

의미 충돌·정본 선택·실제 파생본 최신성은 관련 Registry·Manifest·분야 검증으로 보완한다.

### 9. Close findings

각 finding은 다음 중 하나로 판정한다.

- `BLOCKING`: 병합·배포 전에 수정해야 한다.
- `FIX_NOW`: 현재 범위에서 갱신한다.
- `FOLLOW_UP`: 유효하지만 별도 작업으로 추적한다.
- `ALLOWED_LEGACY`: 역사·호환 목적으로 유지한다.
- `FALSE_POSITIVE`: 실제 소비자가 아니거나 이미 최신이다.
- `UNVERIFIED`: 확인 환경·권한이 없다.

## Output contract

```md
# 정본·참조 최신성 감사

## 기준선과 변경된 정본
## 영향 지도
## 오래된·고아 참조
## 내용 충돌·중복 정본
## 파생본·Manifest·해시
## 변경 전파 누락
## 허용된 Legacy·History
## 자동 검사 결과
## 수정한 파일과 수정하지 않은 파일
## 미검증·후속 작업
## 최종 판정
```

## Definition of Ready

- [ ] base·head와 실제 diff가 고정됐다.
- [ ] 변경된 정본·경로·ID·Schema 후보를 식별했다.
- [ ] 활성 파일과 역사·백업·보류 경로를 구분했다.
- [ ] Registry·Documentation Map·Manifest·Alias를 찾았다.

## Definition of Done

- [ ] 변경된 모든 정본에 영향 소비자 목록이 있다.
- [ ] 오래된 경로·ID·명령·버전과 고아 참조를 검색했다.
- [ ] 변경되지 않은 영향 파일마다 갱신 필요 여부를 판정했다.
- [ ] 정본·파생본·Manifest·테스트·템플릿의 상태가 연결됐다.
- [ ] 허용된 역사 참조와 활성 stale reference를 구분했다.
- [ ] 실행하지 못한 검증을 통과로 표시하지 않았다.
- [ ] 최종 보고가 실제 수정·미수정·후속 작업을 설명한다.

## Failure conditions

- 새 파일이 있다는 이유로 이전 파일 참조를 검사하지 않는다.
- 변경된 파일만 검토하고 변경됐어야 할 untouched 파일을 보지 않는다.
- 모든 과거 표현을 무조건 수정해 이력·호환 정보를 파괴한다.
- 문자열 검색만 하고 동일 책임의 의미 충돌을 생략한다.
- Manifest·해시가 있는데 실제 원본·생성기와 대조하지 않는다.
- 경로 존재만으로 활성·정본·최신 상태를 통과 처리한다.
- 자동 검사 오탐을 검증 없이 모두 수정한다.

## Relationship with other skills

- `reviewing-and-validating-project-changes`: 전체 변경 검증에서 이 Skill을 필요 시 호출하고 결과를 최종 판정에 포함한다.
- `managing-design-documents`: 문서 정본·발행 정책·PDF·Manifest의 고유 검증을 제공한다.
- `managing-game-project-operating-system`: Registry·시작 문서·자동화·콜드 스타트 전체 연결을 검증한다.
- `evolving-project-discipline-skills`: Skill 통합·ID 변경·Legacy Alias 갱신 시 이 Skill을 필수 검증으로 사용한다.
- `maintaining-project-context-and-handoff`: 최신 감사 결과를 바탕으로 오래된 기본 읽기 경로를 제거한다.

## Learning contract

다음이 반복되면 `skills/SKILL_LEARNING_LOG.md`와 자동 검사 규칙을 갱신한다.

- 오래된 경로·Skill ID·문서 ID가 병합 후 발견됨.
- 정본 변경 뒤 특정 소비자·템플릿·테스트가 반복 누락됨.
- 자동 검사가 역사 참조를 활성 stale reference로 반복 오탐함.
- 파생본·Manifest가 CURRENT로 표시됐지만 실제 입력과 불일치함.
- 새 채팅이 최신 정본 대신 오래된 파일을 선택함.

Template: `templates/quality/CANONICAL_REFERENCE_FRESHNESS_AUDIT.md`
