# AI Bootstrap and Project Drift Hardening Design

## Status

`APPROVED_DIRECT_REQUEST` — 2026-08-22

## Goal

GPT 맞춤설정 교정 이후 남은 Codex/Copilot/project scaffold drift를 제거하고, 같은 회귀가 다시 active authority로 들어오는 것을 자동 검증한다. Legacy Sheet는 current authority와 frozen historical evidence를 구분해 보존한다.

## Current-state findings

1. `templates/custom-instructions.codex.md`는 Codex를 항상 `구현 담당자`로 고정하고, `AI_WORKFLOW_RULES`·`MVP_WORKFLOW_CHECKLIST` 등 과거 파일 목록을 매 작업마다 강제한다.
2. `templates/copilot-instructions.md`도 고정 read-order를 가진다.
3. `templates/AGENTS.project.md`는 Base 로컬 사본의 과거 고정 목록을 기본 전제로 하며 현재 `DOMAIN_SPLIT_CANON`을 직접 설명하지 않는다.
4. `docs/operations/SHEET_CONTROL_CONTRACT.json`은 단독으로 보면 `USER_FACING_GDD_WORKSPACE`라 stale처럼 보이지만, Base v9 regression이 이 파일을 **frozen historical evidence**로 명시적으로 보호한다. Current authority는 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`의 `MIGRATION_ONLY_UNTIL_REMOVAL`이다. 따라서 frozen 파일은 수정 대상이 아니다.
5. 실제 프로젝트 감사에서 Ten-Paces와 Blacksmith의 `AGENTS.md`가 Google Sheet/HTML workbook을 사람용 정본으로 유지하고, Tetris는 이미 종료된 PR 번호를 영구 보호 규칙으로 고정하며, MylittleBoat는 최신 Base/Notion authority bootstrap이 거의 없다.
6. GRIMOIRE에는 현재 열린 PR #151이 있으므로 이번 교정에서 write 대상에서 제외하고 read-only cold-start 검증만 한다.

## Verified Notion reality

- TEN_PACES Project Home이 존재하며 Notion을 사람용 전체 그림/Visual/Flow/예산표 owner로, repository를 structured/runtime owner로 명시한다.
- BLACKSMITH Project Home도 같은 `DOMAIN_SPLIT_CANON`을 명시한다.
- MylittleBoat에는 사람용 Project Home이 존재하고 플레이어 경험·핵심 루프·시각 상태를 사람용 정보로 제공한다.

따라서 해당 프로젝트의 repository instruction 교정은 새로운 authority를 발명하는 작업이 아니라 이미 존재하는 Notion/Repository 분할 정본으로 repository bootstrap을 맞추는 작업이다.

## External practice comparison

### OpenAI Codex

OpenAI의 공개 Harness Engineering 사례는 `AGENTS.md`를 백과사전이 아니라 짧은 table-of-contents/map으로 사용하고, 깊은 지식은 구조화된 `docs/` system of record에 둔다. Codex agent loop는 root에서 cwd까지의 `AGENTS.override.md`/`AGENTS.md`를 구체성 순서로 합성한다.

- https://openai.com/index/harness-engineering/
- https://openai.com/index/unrolling-the-codex-agent-loop/

### GitHub Copilot

GitHub는 repository-wide custom instructions와 path-specific instructions를 분리하며, 특정 경로에만 필요한 내용을 전역 instructions에 과적재하지 않도록 한다.

- https://docs.github.com/en/copilot/how-tos/configure-custom-instructions-in-your-ide/add-repository-instructions-in-your-ide

## Alternatives

### A. Codex template only

Codex 맞춤설정만 최신화한다.

**Reject.** Project scaffold와 Copilot bootstrap drift가 계속 구형 authority를 재생산한다.

### B. Rewrite/delete all legacy instruction and Sheet surfaces

과거 AI workflow 문서와 Sheet control 파일을 일괄 삭제·최신화한다.

**Reject.** 미이관 unique material, historical discovery, frozen release evidence를 깨뜨릴 수 있다. 실제 CI가 frozen Sheet mutation을 3개 기존 regression으로 거부했다.

### C. Stable bootstrap + frozen-history preservation + regression guard

Codex/Copilot/project scaffold는 짧은 dynamic authority bootstrap으로 바꾸고, current Sheet authority는 기존 migration-only policy에서 검증한다. Frozen v9 Sheet contract는 원문 그대로 보존한다. 프로젝트별 stale `AGENTS.md`는 실제 Notion/repository current authority를 확인한 곳만 별도 PR로 교정한다.

**Adopt.** 현재 정본과 외부 agent-instruction 실무 패턴을 만족하면서 history/rollback/compatibility까지 보존한다.

## Base design

### Codex custom instructions

- Codex라는 제품명을 영구 `구현 담당` 역할과 동일시하지 않는다.
- 현재 세션의 실제 tool/permission과 사용자 요청에 따라 조사·계획·구현·검증 역할을 수행한다.
- Base 작업은 Base `AGENTS.md`/`START_HERE.md`; project 작업은 project `AGENTS.md`/Active Context/current domain canon으로 진입한다.
- 모든 과거 Base 파일을 고정 목록으로 읽지 않는다. 현재 router/Documentation Map/Skill registry가 지시하는 최소 관련 owner만 progressive-load한다.
- 완료 주장은 실제 diff/test/runtime/readback evidence를 요구한다.

### Copilot template

- repository-wide instruction은 프로젝트 구조·정본 라우팅·검증 진입점만 가진다.
- 경로별 규칙은 path-specific instructions/nearest `AGENTS.md`로 분화 가능하게 한다.
- 구형 Base 파일명을 전역 고정 목록으로 강제하지 않는다.

### Project AGENTS scaffold

- `DOMAIN_SPLIT_CANON`을 기본 scaffold에 직접 넣는다.
- `NOTION_HUMAN_FACING_CANON` / `REPOSITORY_STRUCTURED_CANON` / `REPOSITORY_RUNTIME_TRUTH`를 분리한다.
- Google Sheets는 current policy의 `MIGRATION_ONLY_UNTIL_REMOVAL`로만 라우팅한다.
- local Base copy가 존재하면 채택 버전과 freshness를 확인하되 특정 과거 파일목록을 영구 요구하지 않는다.
- 열린 PR 보호는 current Base rule을 따라 동적으로 판단하고 PR 번호를 template에 고정하지 않는다.

### Frozen Sheet history boundary

`docs/operations/SHEET_CONTROL_CONTRACT.json`은 Base v9 당시 상태를 증명하는 frozen historical artifact다. current policy로 덮어쓰지 않는다.

```text
frozen v9 evidence
→ docs/operations/SHEET_CONTROL_CONTRACT.json
→ USER_FACING_GDD_WORKSPACE / HOLD state preserved exactly

current authority
→ docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md
→ MIGRATION_ONLY_UNTIL_REMOVAL
→ NOTION_DEFAULT_PROJECT_WORKSPACE + repository runtime truth
```

Regression guard는 두 층을 동시에 검증해, 과거 증거 rewrite와 current Sheet-first 회귀를 모두 막는다.

### Regression guard

새 `tests/test_ai_bootstrap_drift_contract.py`가 다음을 고정한다.

- GPT/Codex/Copilot에서 dynamic authority routing과 deprecated default-workspace 금지.
- Codex template에서 fixed `구현 담당자`와 deprecated mandatory file list 금지.
- project scaffold에서 `DOMAIN_SPLIT_CANON`, dynamic open-PR protection, current migration-only Sheet route 요구.
- frozen Sheet contract는 v1 historical identity를 그대로 유지.
- current Google Sheets policy는 migration-only/Notion route를 유지.
- Custom Instructions Guide가 Codex audit을 future TODO로 남기지 않음.

## Project rollout

### Write candidates

- `Ten-Paces-Hidden-Moves`: Sheet-first `AGENTS.md` authority를 current Notion/repository split으로 교정.
- `Blacksmith`: Google Sheet/HTML workbook primary authority를 migration compatibility로 낮춤.
- `Tetris`: 종료된 PR #9 고정 보호 규칙을 current Base dynamic open-PR protection으로 교체.
- `MylittleBoat`: current Notion Project Home + repository structured/runtime bootstrap을 추가.
- `urban-legend`: old copied AI workflow docs의 unique content를 조사하고, unique가 없으면 compatibility alias로 낮추거나 active references를 current AGENTS/Base로 라우팅.

### Read-only/current candidates

- `Switchy-Express-Cargo-Puzzle`, `omenward`, `ninja-survival-godot`, `Coc-Fiction`: current domain split이 이미 존재하므로 필요 최소 범위만 교정. Base gate 횟수 복제는 regression-risk finding으로 별도 판단한다.
- `GRIMOIRE-`: open PR #151 보호 때문에 이번 sweep에서는 write하지 않고 cold-start readback만 한다.

## Validation

Base와 각 write project는 다음을 독립적으로 충족해야 한다.

1. latest main + open/recent PR collision preflight.
2. exact changed-file diff readback.
3. 최소 5회 adversarial full review: authority drift / legacy route / volatile state / runtime-evidence boundary / cold-start.
4. repository CI가 있으면 exact HEAD success.
5. unresolved review thread 0.
6. merge 직전 latest main reconciliation.
7. exact HEAD merge only; no force/direct-main/admin bypass.
8. post-merge main readback.

## Acceptance criteria

- Base의 Codex/Copilot/project scaffold가 stale fixed-file bootstrap을 요구하지 않는다.
- frozen Sheet evidence는 변경되지 않고 current policy는 migration-only로 검증된다.
- regression test가 primary Sheet/fixed executor role 회귀와 historical rewrite를 모두 막는다.
- 확인된 stale project instructions가 current Notion/repository authority와 일치한다.
- 현재로서 올바른 프로젝트는 불필요하게 재작성하지 않는다.
- GRIMOIRE PR #151은 변경·흡수·병합하지 않는다.
