# Work 작업지시문 Superset 비퇴행 통합 사례

```text
BCP-2026-039
PRESERVED
IMPROVED
DELEGATED_TO_CURRENT_OWNER
REJECTED_AS_PROJECT_SPECIFIC
CORRECTED_AS_UNSAFE_GENERALIZATION
```

## 1. 문제

여러 세대의 공용 작업지시문과 진행 중 프로젝트에서 추가된 운영 요청을 그대로 합치면 다음 문제가 생긴다.

- Base current owner와 같은 절차를 복제하는 두 번째 정본
- 프로젝트 전용 PR·SHA·경로·해상도·Art Style의 공용 오염
- 과거에 필요했던 승인·Notion·Git·Godot 규칙이 최신 사용자 결정과 충돌
- 문서 SHA와 실제 제품 구현 기준 SHA 혼동
- local test PASS와 exact-head CI PASS 혼동
- Godot import cache와 tracked source 혼동
- 이미지 후보·승인·runtime 승격 혼동
- local-only 결과를 remote durable input으로 오인

사용자가 요청한 목적은 과거 문서를 보존 전시하는 것이 아니라, 핵심 기능을 잃지 않으면서 현재 가장 효율적인 Work→Codex→버티컬 슬라이스 자동화로 교정하는 것이었다.

## 2. 입력 계보

검토 대상:

- v4.8 r5.4 capability superset
- v4.9 Work-native adapter
- 프로젝트 작업 중 수집된 추가 요청
- Base latest completed main과 current owner
- 실제 PR·CI·Godot·Visual 전달 실패 사례

과거 파일은 baseline evidence로 사용하고 current canon으로 복제하지 않았다.

## 3. 비교한 방법

| 방법 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| 과거 지시문 전체를 새 파일로 결합 | 한 파일에서 모든 문구 확인 가능 | second canon, stale rule, 긴 context, 유지보수 중복 | REJECT |
| 최신 Starter만 유지하고 추가 요청을 채팅에 의존 | 짧음 | 새 채팅에서 위임·경계 누락 | REJECT |
| current owner 유지 + 얇은 router + 누락된 identity 계약 | 비퇴행·발견성·유지비 균형 | owner routing과 contract test 필요 | ADOPT |

## 4. 분류 결과

### PRESERVED

다음 v4.8/v4.9 핵심 capability를 유지했다.

- Base·Project GitHub·Notion·실제 구현 fresh-read
- Project canon 우선과 과거 대화 discovery-only
- Whole Project Audit과 Requirement Traceability
- 핵심 재미·player promise·핵심 시스템·의미 있는 선택
- 증거 기반 SWOT·현재 stage·남은 작업·작업순서
- Reuse First·시장/성공/실패 조사·최소 3개 실질 대안
- Brainstorming·Superpowers·TDD·systematic debugging·verification
- Visual Delete Test·actual consumer·coverage·Art Style Lock
- Work preparation → Codex implementation → Work final review
- GUT/Hera 또는 adopted equivalent machine QA
- IRG와 TECH/UI/HUMAN/PLAYER evidence 분리
- safe Git fetch/pull/push/PR/merge/post-merge readback
- multi-route recovery와 Incident→Solution→Lesson
- required work 0 → completion rescan → 최소 5회 full adversarial loops
- 다운로드 가능한 사용자 실행 경로와 user validation 전 다음 Slice 금지

### IMPROVED

PR #735에서 작업 시작 전 다음을 한 receipt로 확인·교정하도록 강화했다.

```text
핵심 재미
핵심 시스템
증거 기반 SWOT
current stage / Slice
남은 작업
의존성·player value 기반 작업순서
정본 충돌·누락 선교정
```

BCP-2026-039 구현에서는 다음을 추가로 분리했다.

```text
current_completed_product_main
latest_router_or_documentation_sync
current_validation_head
candidate_product_head

TEST_LOGIC_PASS != CI_GATE_PASS
IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF
LOCAL_ONLY_NOT_REMOTE_SYNCED
```

### DELEGATED_TO_CURRENT_OWNER

중복 구현하지 않고 다음 current owner에 위임했다.

- startup canon receipt: `WORK_PROJECT_START_CANON_CHECKLIST.md`
- Work↔Codex minimum transition: `WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md`
- local Visual delivery: `WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md`
- Visual generation/review: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- project asset vault: `docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md`
- detailed Git·CI·Godot·IRG·completion: current Base/Project owner

PR #736은 최신 사용자 결정에 따라 다음 경로를 구현했다.

```text
Notion structure / Art Direction reference
→ project-local candidate
→ PROJECT_ASSET_APPROVED
→ tracked project asset + ASSET_MANIFEST
→ commit/push/remote readback
→ Codex/runtime consumer
```

### REJECTED_AS_PROJECT_SPECIFIC

다음을 Base 공용 계약에 흡수하지 않았다.

- 특정 프로젝트명·캐릭터·유파·세계관·기능명
- 특정 PR/Issue/Task/Decision 번호
- 특정 SHA·branch·worktree·local path
- 특정 해상도·HUD·palette·Art Style
- 특정 완료 목록·다음 작업
- 특정 플랫폼·콘텐츠 전용 Human gate
- 특정 기존 PR 번호를 영구 보호하는 규칙

프로젝트 전용 사실은 해당 AGENTS·Active Context·Decision·Visual Bible·runtime owner에 남긴다.

### CORRECTED_AS_UNSAFE_GENERALIZATION

다음 과거 표현은 현재 결정과 증거에 맞게 교정했다.

| 과거 표현 | 교정 |
|---|---|
| `origin/main` 고정 | 실제 remote/upstream/default branch 발견 |
| dirty/diverged에서도 자동 pull | clean·tracking·non-diverged·FF 가능할 때만 pull --ff-only |
| push/PR마다 새 사용자 승인 | 검증된 current-task branch/PR은 standing delegation 안에서 자동 진행 |
| 모든 승인 이미지에 Notion binary 직접 첨부 필수 | explicit local profile에서는 project-owned tracked bytes + manifest가 기본; Notion은 구조·Art Direction 참고 |
| 모든 `.import`·`.uid`를 generated noise로 간주 | exact engine version·tracking policy·source identity 확인 |
| `addons/gut` 무조건 ignore/commit | current adoption 방식과 exact version 확인 |
| test logic PASS = CI 완료 | parser·summary·artifact·required check·exact HEAD까지 분리 |
| 자동 screenshot/GUT/Hera = Human QA | Human/Player evidence는 실제 수행 전 NOT_RUN |
| 문서 PR SHA = 제품 baseline SHA | product baseline과 router/documentation sync 분리 |

## 5. 실제 구현 구조

```text
WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md
→ WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md
→ WORK_PROJECT_START_CANON_CHECKLIST.md
→ WORK_CODEX_MINIMUM_TRANSITION_VERTICAL_SLICE_PROFILE.md
→ WORK_PROJECT_LOCAL_VISUAL_ASSET_DELIVERY_PROFILE.md when explicitly enabled
→ WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
→ triggered current Base/Project owners
```

router는 세부 정책을 복제하지 않는 `THIN_ROUTER_NOT_SECOND_CANON`이다.

## 6. Visual·Notion 교정

최신 정책:

```text
PROJECT_LOCAL_VISUAL_BINARY_FIRST
NOTION_VISUAL_STRUCTURE_REFERENCE_ONLY
NO_NOTION_BINARY_UPLOAD_REQUIRED
```

이는 Notion을 무시한다는 뜻이 아니다.

- Project Home·Visual Bible·Asset Catalog·Flow·Art Direction은 계속 fresh-read한다.
- 사람이 보는 텍스트·상태를 수정하면 destination readback한다.
- image binary를 실제로 업로드하지 않았으면 업로드했다고 주장하지 않는다.
- local-only 후보는 Codex/CI/new Work durable input이 아니다.
- current Slice에서 사용할 자산은 tracked project bytes와 manifest로 승격한다.
- runtime import·actual consumer·screen evidence 뒤에만 `RUNTIME_PROMOTED`로 올린다.

Project가 별도 Notion binary owner를 명시하면 해당 current Project decision이 우선한다.

## 7. official evidence

공식 근거를 통해 다음을 검증했다.

- GitHub required status checks는 exact latest commit과 current required check identity가 중요하다.
- GitHub workflow artifact는 test/build 결과와 별도 evidence layer다.
- Godot의 `.godot/` cache와 source-control 대상은 구분해야 한다.
- modern Godot의 `.uid`는 source identity가 될 수 있다.
- GUT의 `addons/gut`은 설치·vendor 방식에 따라 dependency source일 수 있다.

공식 근거는 Project/Base canon을 덮어쓰는 권위가 아니라 현재 기술 의미를 검증하는 evidence로 사용했다.

## 8. 비퇴행 검증

계약 테스트는 다음을 요구한다.

- thin router와 current owner 링크
- 핵심 재미·시스템·SWOT·남은 작업·작업순서 startup Gate 보존
- 제품 baseline과 router/document sync 분리
- product-byte-aware candidate freshness
- CI result chain과 exact validator/HEAD
- Godot cache·UID·adopted addon 분류
- local Visual owner로 위임된 candidate/approved/runtime 상태
- local/remote sync 상태
- heartbeat cleanup
- project-specific 값 제외
- Human/Player evidence ceiling

RED에서는 owner/router/case가 없어 실패해야 하고, GREEN에서는 focused test와 current Base required workflows가 exact HEAD에서 통과해야 한다.

## 9. 적대적 검토 축

각 full loop에서 전체 상태를 다시 공격한다.

1. 사용자 의도·Authority·v4.8/v4.9 capability 비퇴행
2. startup checklist·핵심 재미·Work↔Codex minimum transition
3. local Visual·Notion 의미·권리·durability
4. product candidate·CI·Godot source identity·remote sync
5. project-specific leakage·Human/Player overclaim·public/cost/security boundary

유효 finding을 교정하면 resulting state를 다시 전체 재검토한다. 최소 5회 후 새 blocking finding이 0이어야 한다.

## 10. Evidence ceiling

```text
Base policy/contract PASS
!= specific project local filesystem callable
!= image file written
!= tracked asset promoted
!= Codex consumed
!= Godot runtime verified
!= downloadable build exists
!= Human usability PASS
!= Player Experience PASS
```

프로젝트별 실행 증거는 해당 프로젝트가 별도로 남긴다.

```text
HUMAN_USABILITY_EVIDENCE: NOT_RUN
PLAYER_EXPERIENCE_EVIDENCE: NOT_RUN
NO_PUBLIC_RELEASE_AUTHORITY
ZERO_INCREMENTAL_COST_REQUIRED
PROJECT_SPECIFIC_VALUES_EXCLUDED
PROJECT_SPECIFIC_PR_AND_PATH_STAY_IN_PROJECT_CANON
```

## 11. rollback

BCP-2026-039 구현이 잘못된 경우:

```text
implementation squash commit revert
→ current router에서 evidence owner link 제거
→ focused/core regression
→ current Base owner readback
```

PR #735 startup checklist와 PR #736 local Visual owner는 독립적으로 유지된다. 이 rollback 때문에 Project product code·asset·engine baseline·CI workflow를 자동 변경하지 않는다.
