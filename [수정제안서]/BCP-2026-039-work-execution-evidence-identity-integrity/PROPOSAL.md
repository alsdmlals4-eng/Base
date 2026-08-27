# BCP-2026-039 — Work 실행 증거·후보·동기화 identity 무결성

## 출처와 상태

- 출처 프로젝트: 여러 진행 중 게임 프로젝트의 Work→Codex→Godot→CI→Notion closeout 피드백 묶음
- 출처 자료:
  - `CHATGPT_WORK_PROJECT_EXECUTION_INSTRUCTION_v4.9_TERRA_MAX_FINAL_20260826(10).md`
  - `PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.8-r5.4_SUPERSET_FINAL_20260826.md`
  - `붙여넣은 텍스트 (1)(20260827-001940).txt`
- 기준 Base completed main: `1df8878d8a99d91a318ad4adff722d78c763a69a`
- 제출일: `2026-08-27`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `반복 관찰 + 공식 문서 검증 + Base owner 대조`
- approval_ref: `2026-08-27 user instruction — 이전 v4.8/v4.9와 프로젝트별 추가 요청을 비교해 공용으로 흡수할 것은 흡수하고 누락·핵심기능·시작 체크리스트를 교정하라는 명시 승인`

## 관찰과 증거

PR #735로 작업 시작 시 다음을 먼저 확인·교정하는 공용 Gate는 이미 구현·병합됐다.

```text
핵심 재미
핵심 시스템
증거 기반 SWOT
현재 단계·Slice
남은 작업
의존성·player value 기반 작업순서
정본 충돌·누락 선교정
GitHub·Notion destination readback
```

그 후 프로젝트별 피드백을 다시 비퇴행 비교한 결과, 현재 Base에는 다음 반복 실패를 한 번에 막는 명시 계약이 부족했다.

1. 최신 문서·router PR의 SHA가 실제 player-facing 제품 구현 기준 SHA를 덮어쓰는 문제
2. player-facing bytes 또는 export/package 설정이 바뀌었는데 이전 build/candidate를 current로 재사용하는 문제
3. 로컬 test logic은 통과했지만 CI parser·summary·artifact·required check가 실패한 상태를 완료로 오인하는 문제
4. Godot import cache, modern `.uid` source identity, vendored/adopted `addons/gut`를 모두 같은 generated noise로 취급하는 문제
5. 사용자 승인 이미지의 보관·기획 승인과 실제 runtime import/consumer promotion을 같은 상태로 취급하는 문제
6. 아직 원격에 push되지 않은 local commit을 Notion에서 GitHub current locator처럼 표기하는 문제
7. PR merge·post-merge·Notion readback이 끝났는데 heartbeat/monitor가 계속 완료 PR을 감시하는 문제

## 일반화 후보

### A. 제품 기준선과 문서 동기화 identity 분리

```text
current_completed_product_main
latest_router_or_documentation_sync
current_validation_head
candidate_product_head
```

- player-facing 제품 구현의 최신 병합 SHA와 문서/router-only 후속 SHA를 분리한다.
- 문서-only PR이 병합됐다는 이유로 실제 제품 구현 기준선을 자기 SHA로 순환 갱신하지 않는다.

### B. Exact Candidate Freshness

후보는 생성 당시의 exact game-consumer bytes와 export/package identity에만 유효하다.

player-facing code·Scene·Resource·data·localization·UI renderer·consumed asset/path·export/package 설정이 바뀌면 기존 후보를:

```text
HISTORICAL_SUPERSEDED_BY_PRODUCT_BYTE_CHANGE
```

로 내린다.

문서-only, tooling-only, test-only 변경은 실제 product bytes가 같다는 증거가 있으면 자동 무효화하지 않는다.

### C. CI 결과 체인 분리

```text
TEST_LOGIC_PASS != CI_GATE_PASS
```

완료·병합 전 다음을 분리 확인한다.

```text
test runner exit status
→ formal result/JUnit or equivalent
→ summary/parser compatibility
→ required diagnostic/build artifact
→ current repository required check
→ exact current HEAD
```

parser나 artifact 실패를 테스트 삭제·기준 완화·check 우회로 숨기지 않는다.

### D. Godot 생성물과 source identity 분리

```text
IMPORT_CACHE_DIFF != PRODUCT_SOURCE_DIFF
NEVER_STAGE_GENERATED_IMPORT_NOISE
NO_BLANKET_UID_OR_ADOPTED_ADDON_IGNORE
```

- current Godot 4.1+에서 `.godot/`는 cache이며 기본 ignore 대상이다.
- Godot 3.x와 4.x의 ignore 규칙은 같다고 가정하지 않는다.
- Godot 4.4+의 `.uid`는 source identity가 될 수 있으며 blanket ignore/delete하지 않는다.
- `addons/gut`은 설치·vendor·submodule·외부 공유 방식에 따라 dependency source일 수 있으므로 current adoption record와 exact version을 따른다.

### E. Visual 후보와 runtime 승격 분리

```text
USER_APPROVED_VISUAL_CANDIDATE != RUNTIME_PROMOTED
```

사용자 승인·보관은 runtime 교체를 뜻하지 않는다. 동일 원본 bytes의 local archive, Notion direct attachment, SHA-256, provenance/rights, exact consumer/slot, import/crop/readability/runtime evidence가 있어야 runtime promotion한다.

이 제안은 이미지 생성 승인권을 확대하지 않으며 current Visual owner가 최종 권위다.

### F. 원격 동기화 상태와 완료 자동화 정리

- local-only commit을 가리키는 Notion 기록은 `LOCAL_ONLY_NOT_REMOTE_SYNCED`로 표시한다.
- push 뒤 remote HEAD readback 전에는 GitHub durable locator라고 주장하지 않는다.
- current-task PR이 merge되고 post-merge main·Notion readback까지 끝나면 해당 PR heartbeat/monitor를 disable/remove한다.
- durable completion receipt와 증거는 삭제하지 않는다.

### G. Slice 작업 소유 경계

GitHub Issues를 사용하는 프로젝트에서는 하나의 Playable Slice에 하나의 current implementation Issue/PR을 기본으로 하되, 독립적인 기반 enablement 수정은 별도 PR로 분리할 수 있다. 병합 뒤 Slice PR을 latest completed main에서 재검증한다.

## 프로젝트 전용으로 남길 내용

다음은 공용 Base에 흡수하지 않는다.

- 특정 프로젝트명·캐릭터·유파·세계관·기능명
- 특정 PR 번호, Issue 번호, branch, worktree, 로컬 절대 경로, 현재 완료 SHA
- 특정 화면 해상도, HUD 항목, 색상 언어, 화풍, 캐릭터 기본값
- 특정 프로젝트의 현재 완료 범위와 다음 우선순위
- 특정 플랫폼·유파·콘텐츠 확장에만 적용되는 Human QA 차단 조건
- 특정 기존 PR을 영구 보호하는 번호 기반 규칙

위 값은 해당 프로젝트 AGENTS·Active Context·Decision·Visual Bible·runtime owner가 소유한다.

## 적용 조건과 비사용 조건

### 적용

- Work→Codex→Godot→CI→Notion으로 이어지는 Playable Slice
- build candidate, runtime asset promotion, CI 결과, post-merge closeout identity가 material한 작업
- local/remote Git과 Notion이 함께 사용되는 작업

### 비사용·축소

- 문서 오탈자처럼 제품 후보·CI artifact·runtime consumer와 관계없는 L0 수정
- Godot/GUT을 채택하지 않은 프로젝트
- Visual이 없는 프로젝트의 이미지 상태 계약
- GitHub Issues를 사용하지 않는 프로젝트의 Issue 단일 소유 규칙

## 반례와 위험

- 모든 문서 변경마다 build 후보를 폐기하면 불필요한 재빌드가 늘어난다. 따라서 product bytes 영향 여부를 기준으로 한다.
- 모든 `.uid`를 generated noise로 보면 modern Godot의 resource identity가 깨질 수 있다.
- 모든 `addons/gut`을 추적 대상으로 강제하면 외부 package/submodule 운영과 충돌한다. current adoption이 우선한다.
- Visual 2단계 상태를 별도 asset canon으로 만들면 중복 정본이 된다. current Visual/Asset owner의 status vocabulary에 interface로만 연결한다.
- heartbeat 정리 시 완료 evidence까지 삭제하면 continuity가 깨진다. watcher만 종료하고 receipt는 보존한다.

## 공식·현업 근거

- Godot stable VCS guide: `.godot/` cache exclusion과 engine-version별 ignore 차이
  - https://docs.godotengine.org/en/stable/tutorials/best_practices/version_control_systems.html
- Godot 4.4 UID guidance: `.uid` 파일을 version control에 commit해야 함
  - https://godotengine.org/article/uid-changes-coming-to-godot-4-4/
- GUT install guide: `addons/gut`은 프로젝트에 설치되는 plugin directory이며 설치 방식이 여러 개임
  - https://gut.readthedocs.io/en/v9.6.1/Install.html
- GitHub required status checks: latest commit SHA에서 required checks가 성공해야 함
  - https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks
- GitHub workflow artifacts: test/build output은 workflow artifact로 별도 보존·검증 가능
  - https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts

## 영향 범위와 검증

승인 구현은 새 얇은 owner/router와 contract test를 중심으로 한다.

예상 구현 경로:

```text
templates/project-operations/WORK_EXECUTION_EVIDENCE_IDENTITY_INTEGRITY.md
templates/project-operations/WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md
docs/knowledge/cases/WORK_INSTRUCTION_SUPERSET_RECONCILIATION_CASE.md
docs/superpowers/plans/2026-08-27-work-instruction-superset-reconciliation.md
tests/test_work_instruction_superset_reconciliation_contract.py
```

검증:

- RED: 새 owner/router/token이 current main에 없어 focused contract 실패
- GREEN: 새 파일과 routing contract 추가
- project-specific name/PR/style/resolution/path가 공용 파일에 없음을 negative test
- `.uid`와 `addons/gut` blanket ignore 금지 test
- exact-head Base required workflows
- 최소 5회 full-scope adversarial review

## 필요한 도구·파일·권한

- 필요 항목: GitHub connector, Base current main, uploaded source instructions, official public documentation
- 필요한 이유: exact current owner·open PR·CI·merge/readback 확인
- 설치·적용 방법: 신규 설치 없음
- 설치 후 확인 명령: 해당 없음
- 최소 권한: Base feature branch/PR write와 current ruleset이 허용하는 merge
- 신규 비용: `0`

## 승인과 구현

- 사용자 승인 근거: `2026-08-27 current chat explicit instruction`
- 승인 범위: 위 A~G의 project-neutral contract와 thin router/test/case/plan
- 제외 범위: Visual owner의 생성 승인 정책 변경, project-specific 값, engine baseline 변경, CI workflow 약화, public release
- 구현 PR: `별도 생성 예정`
- Proposal Registry: open PR #678이 소유 중이므로 현재 PR에서 수정하지 않음
- 롤백: 구현 PR squash commit revert + 새 router 사용 중단; 기존 v4.9/current Starter와 #735 체크리스트는 유지
