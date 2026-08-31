# BCP-2026-047 — Repository Runtime Visual Capture Manifest Pattern

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Ten-Paces-Hidden-Moves`
- 기준 커밋: `4032cf550295da6d55646a8fb64fb27acaf1ddc3` (project PR #304 merge commit)
- 제출일: `2026-09-01`
- 상태: `SUBMITTED`
- 지식 상태: `관찰`

## 후보보고서 상태와 정본 경계

`CANDIDATE_REPORT_IS_NOT_BASE_CANON`

- 후보보고서·첨부물의 역할: Ten Paces의 repository-controlled combat capture, registrar, test, and execution report는 **입력 증거와 단일 프로젝트 사례**다.
- Base 정본 또는 구현 지시가 아닌 이유: 현재 직접 검증된 consumer는 한 프로젝트 하나뿐이며, Base-wide file layout·storage retention·engine adapter를 아직 증명하지 않았다.
- 프로젝트 고유 결론·설정·수치·경로·자산 중 제외한 것: `TEN-RVC-*` IDs, Korean wuxia screen composition, Godot scene/consumer paths, HERA invocation, screenshot bytes, project policy Decision, 15 MiB limit, and project test/tool names.

## 관찰과 증거

- 실제로 확인한 작업·구현·검증:
  - Project main `4032cf550295da6d55646a8fb64fb27acaf1ddc3` contains `TEN-RVC-20260901-001`: a repository PNG bound to its source commit, scene/state, route, consumer files, diagnostics, dimensions, SHA-256, and explicit evidence ceilings.
  - The copied PNG hash was read back from its manifest; its declared consumer files existed. The project-local registrar rejected non-PNG input, a nonexistent declared consumer, and an unreasoned third capture state.
  - The focused project suite completed `23 tests, OK`; its exact Godot/HERA capture reported `0` errors and `0` warnings.
  - Existing Base owners already require current capture context (`RM-TOOL-004`) and fresh artifact path/hash/run identity (`FRESH_RUNTIME_ARTIFACT_GATE`).
- 추측·미실행 항목과 evidence ceiling:
  - This is one project and one direct no-state-injection preview capture, not a demonstrated second-project pattern.
  - It does not establish human readability, accessibility, device behavior, release performance, asset rights, or a preferred Base binary-retention budget.
  - It does not show that every visual change needs a screenshot; deterministic assertions remain preferable when pixels/layout are not the acceptance target.

## 일반화 후보

`COMMON_LESSON_AND_CORRECTION_REQUEST_REQUIRED`

When a player-visible visual/layout acceptance decision genuinely needs a runtime image, a project can retain the smallest representative image set in a repository or governed CI artifact **with a compact record** that binds:

1. exact source commit/build and run/entry identity;
2. scene or visible state, viewport/input context when relevant, and source-delta/diagnostic readback;
3. copied image path, dimensions/bytes, digest, and actual consumer paths; and
4. an explicit evidence ceiling that prevents a machine capture from becoming Human, accessibility, device, release, rights, or user-approval PASS.

This is a candidate complement to existing Base evidence language, not a proposal for a common capture executable.

## 적용 조건과 비사용 조건

- 적용 조건:
  - the task changes a player-visible visual/layout/motion surface;
  - a fresh runtime artifact is required because pixels or layout are part of acceptance;
  - the project already has an approved runtime capture source and a repository/CI-artifact retention owner;
  - only the final normal/readable state plus a genuinely distinct impact/result or unavailable baseline state is retained.
- 비사용 조건:
  - logic/data-only work, deterministic assertions that fully cover acceptance, static design candidates without an actual runtime consumer, or environments where a fresh runtime artifact cannot be produced;
  - a project with a stronger approved evidence system already providing equivalent source/build/path/hash/state/ceiling readback;
  - any task where storing screenshot bytes conflicts with rights, privacy, security, cost, repository-size, or release policy.
- 그대로 복사하면 안 되는 요소:
  - project paths, identifiers, raw screenshot binaries, a universal JSON schema, a new HERA/Godot dependency, a dedicated capture app, or a rule that screenshots prove Human quality.

## 기존 Base owner gap과 최소 수정 요청

`MINIMUM_OWNER_CORRECTION_REQUEST`

- 현재 owner·경로:
  - `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md` → `RM-TOOL-004 · REPOSITORY_NATIVE_EVIDENCE_CAPTURE`;
  - `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md` → `FRESH_RUNTIME_ARTIFACT_GATE`.
- 확인한 gap 또는 충돌:
  - No conflict was found. `RM-TOOL-004` already lists commit/build/viewport/input context, capture sources, storage, and evidence ceiling; the Fresh Runtime Artifact Gate already requires fresh artifact path/hash/run identity.
  - The current Base text leaves the **bounded, reviewable manifest pattern for player-visible runtime images** implicit: it does not show a minimal cross-reference set covering image digest/dimensions, visible scene/state, actual consumers, diagnostics/source delta, and non-human ceilings together.
- 최소 수정 요청:
  - Review whether `RM-TOOL-004` should add one optional example or checklist line: when retaining a runtime image for visual acceptance, record exact source/run identity, image digest/path/dimensions, visible state, consumer, diagnostics/source-delta where available, and evidence ceiling in the project’s existing evidence owner.
  - Preserve the Fresh Runtime Artifact Gate as the freshness owner. Do not add a Base CLI, new Skill, mandatory JSON schema, repository binary requirement, or automatic Human/device elevation.
- 새 Skill·문서·registry가 필요 없는 이유 또는 필요한 근거:
  - The existing owners already own the behavior. If approved after independent review, a one-paragraph optional extension to `RM-TOOL-004` is the smallest possible implementation; no new registry entry is justified.
- 변경하지 않을 보호 범위:
  - all project-local capture tools; Base process/engine ownership; existing screenshot/video storage choices; visual asset approval and rights rules; Human/device/release gates; open BCPs #044/#045 and their proposals.

## 프로젝트 전용으로 남길 내용

- Ten Paces hidden-planning gameplay, martial-arts art direction, exact scene and consumer names, the `TEN-RVC-*` namespace, source PNG, and capture-policy Decision remain project-owned.
- The project-local Python registrar remains a bounded adapter until another materially different project demonstrates that its inputs, storage model, and validation boundary are stable.

## 반례와 위험

`EVIDENCE_CEILING_AND_NONUSE_CONDITIONS`

- 반례:
  - A hash-valid screenshot can still portray an injected debug state, stale code, clipped UI, the wrong device, or an unreadable design.
  - A project may have a secure CI artifact system where repository screenshots are unnecessary or prohibited.
  - Video/frame-heavy features can cause repository growth if a “capture every state” reading is allowed.
- evidence ceiling:
  - `MACHINE_RUNTIME_CAPTURE` proves only that the stated runtime/render artifact was recorded at its declared identity. It is not Human UX, accessibility-user, Android/console/device, performance, rights, or user final approval evidence.
- 승인 전 구현 금지 범위:
  - Do not modify active Base methods, Skills, templates, tests, registries, tooling, or project adapters from this proposal.

## 영향 범위와 검증

- Proposed impact if later approved: one optional, owner-local wording/checklist addition under `RM-TOOL-004`; inspect the Fresh Runtime Artifact Gate for duplicated terminology, then run Base reference-freshness and relevant evidence/BCP tests.
- Current proposal-only verification:
  - proposal registry schema and proposal-only diff validator;
  - `tests/test_base_change_proposals.py`;
  - Base reference-freshness from `f098af54625e25dc084e76294dbc65fbba7769fb` to the proposal commit.
- Rollback: remove this registry item and its proposal file if rejected; no active Base source or project runtime code needs rollback.

## 필요한 도구·파일·권한

- 필요 항목: existing Base proposal registry, validator, and test only.
- 필요한 이유: register one reviewable candidate without changing active Base behavior.
- 설치·적용 방법: no installation, external service, credential, or paid tool.
- 설치 후 확인 명령: `python tools/check_base_change_proposals.py --base-ref <base-main-sha>`.
- 최소 권한: repository write for a proposal-only PR; no runtime, platform, or user-data access.

## 승인과 구현

- 사용자 승인 근거: user direction on `2026-09-01` permits reusable tools/modules/skills to be promoted to Base when suitable; it authorizes this proposal submission, not an active Base implementation.
- Base implementation approval ref: `미승인`.
- 구현 PR: `없음`.
- 롤백: reject/defer the proposal or revert only its registry record and proposal file; never remove the Ten Paces project evidence as a consequence.
