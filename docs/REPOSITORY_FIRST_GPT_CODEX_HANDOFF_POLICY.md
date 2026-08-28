# Repository-First GPT–Codex Handoff Policy

## 0. 역할 경계

```text
GPT_PLANNING_RESEARCH_REVIEW_VISUAL_OWNER
GPT_REPOSITORY_CANON_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
EXACT_REPOSITORY_COMMIT
REPOSITORY_PATH_MANIFEST_SHA256_READBACK
NOTION_ABSENCE_IS_NOT_A_BLOCKER
```

이 문서는 `docs/GPT_CODEX_WORKFLOW_POLICY.md`의 Godot 제품 구현 역할 분리를 유지하면서, Notion-first 인계 부분만 repository-first 경로로 교정한다.

- GPT는 기획, 조사, 재사용 판단, 적대적 검토, 이미지 생성·편집, 프로젝트 비제품 정본, Codex 인계 명세와 최종 검수를 소유한다.
- Codex는 실제 게임 프로젝트의 Godot 제품 구현, GDScript, Scene/Resource/runtime wiring, build/export와 implementation/runtime/play test를 소유한다.
- `CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`: Base 정책·문서·Registry·공용 테스트나 순수 기획 파일이라는 이유로 Codex가 기본 owner가 되지 않는다.

## 1. 인계 진입 조건

실제 Godot 제품 구현이 필요한 현재 `PLAY_MEANINGFUL_WORK_SLICE`만 Codex에 넘긴다.

GPT는 인계 전에 다음을 저장소에 기록하고 readback한다.

```yaml
work_slice_id:
player_outcome:
player_action_and_choice:
approved_scope:
explicit_non_scope:
protected_rules:
required_data_and_inputs:
ui_ux_flow:
actual_asset_consumers:
asset_audio_dependencies:
acceptance_criteria:
review_evidence_expected:
source_commit:
```

`source_commit`은 이동하는 branch 이름이 아니라 검토한 `EXACT_REPOSITORY_COMMIT` 40자 SHA다.

## 2. 인계 흐름

```text
GPT minimum implementation-ready planning
→ repository AI canon update
→ CURRENT_CONFIRMED_DECISIONS and ACTIVE_CONTEXT update
→ required asset/audio readiness check
→ REPOSITORY_PATH_MANIFEST_SHA256_READBACK
→ exact source commit readback
→ Codex handoff
→ Codex repository fresh-read at exact commit
→ actual Godot product implementation
→ automated/runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ GPT FIX | TUNE | REDESIGN review
→ impact-bounded revalidation
→ CANON_SYNC_AFTER_VALIDATION
```

Codex fresh-read 최소 범위:

1. 프로젝트 `AGENTS.md`와 `START_HERE.md`;
2. `ACTIVE_CONTEXT.md`;
3. `CURRENT_CONFIRMED_DECISIONS.md`;
4. AI 기획·구현 명세 owner;
5. current Codex handoff;
6. 관련 code/data/Scene/Resource/assets/tests;
7. `ASSET_MANIFEST.json`과 실제 binary;
8. 같은 Goal의 open/recent PR read-only reconciliation;
9. 현재 Slice와 직접 연결된 runtime evidence.

과거 채팅이나 memory는 discovery-only이며 exact repository truth를 덮지 않는다.

## 3. Visual·Audio 입력

Codex는 이미 승인되어 현재 구현에 사용할 수 있는 입력만 소비한다.

`REPOSITORY_PATH_MANIFEST_SHA256_READBACK` 완료 조건:

```text
asset_id exists
repository_path resolves at source commit
actual_consumer matches the current implementation surface
approval_status permits current use
sha256 matches the stored file
version and supersession are unambiguous
rights_or_license_state is sufficient for the current stage
implementation_status is APPROVED_FOR_IMPLEMENTATION or equivalent
```

필요한 visual이 없거나 consumer·규격·approval·hash가 불명확하면:

```text
GPT_VISUAL_REQUEST
→ GPT creates or edits exactly the approved bounded output
→ user approval when required
→ repository path + manifest update
→ readback
→ new exact source commit
→ Codex resumes
```

`NOTION_ABSENCE_IS_NOT_A_BLOCKER`: Notion 페이지, attachment 또는 readback이 없다는 이유만으로 구현을 막지 않는다. 반대로 repository asset이 없거나 manifest가 불일치하면 Notion에 이미지가 보이더라도 구현 준비 완료가 아니다.

Codex는 프로젝트 이미지를 새로 생성하거나 generative edit하지 않는다. 코드 기반 shader/VFX/feedback 구현은 Godot 제품 구현 범위에서 허용된다.

## 4. 기술 자율과 보호 범위

GPT는 player outcome, 규칙 의미, UX 정보 구조, data 의미, asset 소비처, Acceptance와 explicit non-scope를 확정한다. Node·Scene·함수·클래스 배치와 구체 구현 방식은 Codex가 current project truth에서 선택한다.

Codex가 다음 변경 필요를 발견하면 `CHANGE_PROPOSAL`로 돌려보낸다.

- 코어 loop 또는 player outcome 변경;
- 경제·밸런스 의미 변경;
- 주요 UX 의미나 입력 방식 변경;
- 서사·정사·Art Direction 변경;
- approved asset의 의미 있는 교체;
- 저장 호환성·플랫폼·비용·보안 경계 확대;
- explicit non-scope 편입.

컴파일 오류, bounded 리팩터링, 테스트 가능성 개선, 현재 의미를 보존하는 Scene/Resource 구조 선택은 기술 자율 범위다.

## 5. 구현 반환 계약

Codex는 `READY_FOR_GPT_REVIEW`에서 다음을 반환한다.

```yaml
implemented_scope:
files_changed:
source_planning_commit:
implementation_head:
asset_manifest_entries_consumed:
automated_test_evidence:
runtime_evidence:
play_evidence:
visual_audio_evidence:
known_limits:
explicit_non_scope_preserved:
rollback:
```

다음 claim은 분리한다.

- test PASS;
- runtime PASS;
- visual/audio consumption PASS;
- UX/player PASS;
- release readiness.

하나가 다른 하나를 자동 증명하지 않는다.

## 6. 검수와 정본 동기화

GPT는 구현 결과를 다음 기준으로 분류한다.

- `FIX`: 기획·Acceptance·오류·회귀 불일치.
- `TUNE`: 의미는 맞지만 체감·가독성·밸런스·피드백 개선 필요.
- `REDESIGN`: current design 자체가 플레이어 가치나 구현 현실에 맞지 않음.

수정 후에는 영향 범위만 `IMPACT_BOUNDED_REVALIDATION`한다. 통과하면 `CANON_SYNC_AFTER_VALIDATION`으로 실제 구현 상태, test/runtime evidence, asset implementation status와 Active Context를 갱신한다.

사람용 PDF가 필요한 Gate라면 exact implementation commit을 기준으로 `HUMAN_GDD_PDF_DERIVED_VIEW`를 생성한다. PDF 생성이 구현 검증을 대신하지 않는다.

## 7. Legacy Notion 인계

기존 프로젝트 handoff가 Notion URL을 포함할 수 있다. 이는 `LEGACY_DISCOVERY_ONLY` locator다.

- repository에 없는 unique meaning을 발견하면 migration checklist로 이관한다.
- repository canon과 충돌하면 latest user decision과 repository current owner를 우선하고 충돌을 기록한다.
- Notion-only asset은 repository delivery가 끝날 때까지 `GPT_VISUAL_REQUEST` 또는 migration pending이다.
- project-specific 최신 사용자 결정이 Notion 유지로 명시된 경우에만 해당 프로젝트 override를 적용한다.

## 8. 안전과 완료

- force push, destructive reset, unrelated PR mutation, ruleset bypass 금지.
- exact project/repository/worktree identity 확인.
- stale PID/session이나 다른 Godot 인스턴스를 작업 소유 process로 추정하지 않는다.
- Work가 직접 실행한 Godot은 검증 종료 후 해당 작업 소유 process만 정리한다.
- repository readback, test/runtime evidence와 cleanup evidence를 분리한다.

이 정책의 적용 성공은 공용 인계 경로가 repository-first임을 뜻한다. 개별 프로젝트의 Notion unique material이 모두 이관되었다는 뜻은 아니다.
