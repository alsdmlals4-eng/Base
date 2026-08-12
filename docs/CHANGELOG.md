# Changelog

## Unreleased — Base v9.5 focused maintenance candidate

- Added a planning-locked `LOOP_ENGINEERING_CONTROL_PLANE` with `Human-led WHAT/WHY, Agent-led HOW`: user-reviewed `PLANNING_LOCKED` scope can be autonomously decomposed, isolated, implemented, independently verified, repaired, and integrated through A0–A4 risk-scaled autonomy, semantic `TASK_LEASE`/`RESOURCE_LOCK`, design-drift, budget/`NO_PROGRESS`, exact-SHA freshness, evidence-ceiling, and Learning→BCP boundaries. The initial project default is A2 isolated execution with an empty A3 auto-merge allowlist; this contract does not itself install or claim a scheduler, webhook, daemon, or 24/7 agent runtime.
- Added `LOWEST_VIABLE_RATING` with `AVOID_ADULTS_ONLY`: projects avoid 청소년이용불가·18+ by default but choose the lowest honest rating that preserves the approved core experience instead of forcing all-ages or hiding content.
- Added a platform review and asset-rights workflow for Steam, STOVE, and Google Play, including per-asset provenance, commercial/build-distribution rights, secure contract references, and 참조 기반 독립 제작 for images, audio, fonts, 3D, animation, plugins, open source, AI, outsourcing, voice, composition, and translation.
- Added a neutral-adversarial recommendation Gate to the existing feature lifecycle: user proposals and AI first proposals now receive the same criteria, alternatives, counterevidence, risk, reversibility, and evidence-limit review; unsupported agreement and disagreement-for-its-own-sake are both rejected without adding a broad Skill or changing Registry bytes.
- Clarified the immutable v9.0 baseline, released v9.4 compatible line, current routing authority, and frozen v9.0 release derivatives without changing released locks.
- Reduced active Skill discovery metadata while preserving Registry bytes, Skill IDs, trigger contracts, and Skill bodies.
- Added realistic prompt-to-Skill behavior fixtures and a deterministic contract/result scorer; live model execution remains `NOT_RUN` until external results are supplied.
- Integrated Issue #74's Build-Measure-Learn, element decomposition, four review lenses, Golden Path/Edge/Regression, and Base-versus-project learning boundary into existing workflows rather than adding a broad Skill.
- Consolidated the Required Check to one owner, removed the canonical PR trigger filter, and kept focused Base v9 evidence as a separate check.
- Replaced file-existence publication gates with shared executable LibreOffice/Poppler and regular/bold-font readiness, and added an isolated canonical local-validation entrypoint whose owned temporary session is cleaned on success or failure.
- Split the two Base entrypoints by responsibility: `AGENTS.md` now keeps only always-on authority, safety, protection, evidence, and completion invariants, while `START_HERE.md` is a one-step request router to existing canonical procedures. Semantic regressions preserve discoverability without introducing a line or character limit, and active local-validation examples now require the exact trusted 40-character main SHA instead of a moving ref name.
- Added a repository governance baseline: MIT reuse terms, a scope-bound private vulnerability reporting policy, actual-owner CODEOWNERS, and weekly manifest-backed Dependabot proposals for pip and GitHub Actions. The repository's pnpm 11 is outside GitHub's currently documented pnpm v7-v10 range, so it remains explicitly deferred instead of falsely reported as covered or silently downgraded. Current repository identity now lives in a mutable governance profile instead of a frozen release lock, and the governance regression runs even for docs-only changes. Repository settings and first platform behavior remain separately verified rather than inferred from files.
- Integrated PR #178 at merge `3c7b97dab19284999f39d79e04e1845bdff0ff06`: eligible projects may use one shared Windows PC + Android game core with platform-specific input, layout, lifecycle, quality, and store adapters; dual targeting and same-day public launch remain conditional. Exact-head `ci-gate`, focused knowledge contracts, Ubuntu governance regression, publication validation, and Windows smoke passed; actual game builds, physical Android devices, human usability, and store submissions remain `NOT_RUN`.

## 2026-08-01 — Base v9.4 released pins

- Finalized Base v9.4 as `BASE_RELEASED`.
- Payload: `a728712cb776ec98f4875914a580fcf7d0156593`.
- Trusted evidence: `ef1fba11167e4da0b298123b0c85ebd268191a42`.
- Registry SHA-256: `693a0dff3f054ecdd653079909e044211473838e73dd9aff07734d1ce5694c59`.
- BCP-2026-003 and BCP-2026-004 transitioned to `IMPLEMENTED`.
- Project adoption remains a separate post-release wave.

## 2026-08-01 — Base v9.4 AI operations candidate

- Added provider-neutral model/effort routing, Prompt caching boundaries, cost measurement and recalibration.
- Added instruction authority budgeting, Interface-first Prompt, Context curation, Example-as-Fixture and Artifact claim limits.
- Added Godot game UI motion contracts for interruption, instant completion, repetition, Reduced Motion, mute, haptic-off and domain authority.
- Preserved released Base v9.3 history and separated candidate, trusted evidence and pin-finalization stages.

## 2026-07-30 — GDD module and visual-workspace index

- Kept the compact six-domain GDD and single current-decision ledger, while adding a `GDD Module ID` card so a reader can find one topic's decision, responsible source, visual reference, implementation state, and next gate together.
- Added an optional `06_시각_작업면` Sheet index for Figma, Whimsical, or other visual artifacts in `GDD`, `EXTERNAL_COLLABORATION`, or `BOTH` contexts. It links IDs and snapshots rather than copying boards or becoming a second canon.
- Updated the working-template comparison to current living-GDD examples and preserved the existing `PROPOSED_SHEET_CHANGE` and post-main-sync boundaries.

## 2026-07-30 — Base v9.1 derived project routing

- First migration now derives active/inactive project routes from the declared project Registry and Base routes only from active Base Skills explicitly named by legacy shared overrides.
- The artifact generator writes a project-specific thin workflow router from the adapter and snapshot without copying shared Base Skill bodies.

## 2026-07-30 — Base v9.1 first-migration completion

- Project-local Skill body paths may resolve relative to the declared project Registry only when their fully resolved path stays within the project root and contains no link traversal.
- First migration now creates a conservative, non-overwriting `PROJECT_OPERATING_HEALTH` artifact when it is absent. Baseline-declared future protected roots remain protected without being falsely reported as missing product paths.

## 2026-07-30 — Base v9.1 legacy project Registry-path migration

- The migration generator now preserves a legacy adapter's declared local Skill Registry path instead of requiring a copied `skills/SKILL_REGISTRY.json`.
- Added non-default path and root-escape regressions so per-project canonical structures remain local and fail closed.

## 2026-07-30 — Agent merge execution policy

- Replaced separate user merge approval with `AGENT_MERGE_REQUIRED`: a non-Draft PR whose reviewed HEAD, required checks, independent review, thread state, and decision gates all pass must be merged by the responsible agent using GitHub auto-merge or the repository's allowed direct method.
- Kept `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, P0/P1 findings, failed or missing checks, unresolved threads, conflicts, and unsupported merge methods as explicit merge blockers; these are evidence gates, not a default approval wait.

## 2026-07-30 — Base v9.1 immutable project pins

- Finalized the v9.1 payload pin (`3c158f5…`) and separate trusted-main evidence pin (`dd20ad3…`) for project adapters.
- The integrity checker now rejects self-attested, non-ancestral, payload-mismatched, Registry-mismatched, or Registry-mutating evidence. Released Registry bytes are read from the evidence commit, so later Base Skill evolution does not alter the v9.1 release contract.

## 2026-07-30 — Base v9.1 trusted release-evidence record

- Added a schema-validated v9.1 evidence record for merged candidate payload `3c158f52cfdad889970aef4d6ce6650a6fea0645` and its raw-byte Skill Registry identity.
- Established the two-step trusted-main sequence: merge evidence without changing the Registry, then finalize immutable project pins in a separate PR. Runtime, device, accessibility, and human validation remain `NOT_RUN`.

## 2026-07-30 — Base v9.1 CI capability correction

- Added the pinned Pillow, Markdown-It, and PyPDF validation dependencies required by the Windows PDF command safety and document-publication regressions on clean GitHub runners.
- Made dependency review capability-aware: it runs on public repositories or after a private repository owner enables GitHub Advanced Security and sets `DEPENDENCY_REVIEW_ENABLED=true`; otherwise the workflow records `DEFERRED_UNTIL_REPOSITORY_SECURITY_ENABLED` instead of a false pass.

## 2026-07-30 — Base v9.1 external protected-baseline authority

- Anchored each protected baseline to an explicit external Git authority and required exact equality instead of allowing adapter or CLI baseline replacement.
- Added fail-closed local remote-ref resolution, exact GitHub pull-request base-SHA invocation, explicit migration authority inputs, and adversarial self-attestation fixtures.
- Reconciled the #72 governance-ledger evolution with v9.0 immutability by pinning each release-evidence Git blob OID and SHA-256 instead of requiring current working-path equality.
- Bound those historical pins to the exact v9.0 pending-to-released transition inside an externally trusted Git history and sourced historical Registry authority from the evidence `base.lock.json` blob.

## 2026-07-30 — Base v9.1 first-migration baseline source fix

- Replaced the canonical-adapter-at-baseline assumption with a commit-qualified protected-policy source contract supporting legacy-only first migrations and canonical later waves.
- Migration now anchors protected paths to the explicit legacy Git blob and refuses missing, unextractable, hash-mismatched, or weakened policy.

## 2026-07-30 — Base v9.1 second-review hardening

- Required project-confined, existing, raw-SHA-matching, globally unique health evidence and a mandatory protected baseline commit.
- Expanded the v9.0 frozen contract to all eight generator outputs with CRLF-safe Git-blob comparison, and separated historical v9.0 Registry authority from the current v9.1 candidate Registry.
- Standardized snapshot/dashboard adapter provenance on `RAW_FILE_BYTES_SHA256` and expanded dependency review to workflow and Action metadata.

## 2026-07-30 — Base v9.1 review remediation

- Closed Issue #71 review blockers across Action provenance, historical artifact immutability, release-lock binding, health evidence, routing/aliases, protected/path safety, generator preflight, legacy projections, dashboard provenance, migration pins, Skill duplication, Windows wrapper safety, and clean-runner dependencies.
- Replaced prose-only pressure checks with executable Git fixtures and retained runtime/device/accessibility/human evidence as `NOT_RUN`.

## Unreleased - Base audit and operating-contract consistency

- Base 저장소 무결성 감사에서 프로젝트 간 `docs/ACTIVE_HANDOFF.md` 이중 정본을 제거하고, 원문은 `docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md`에 `ARCHIVE_HISTORY`로 보존했으며 기존 경로는 `COMPATIBILITY_ONLY` Stub으로 전환했다. Archive Manifest·본문 SHA-256·rollback ref·소비자 연결 회귀를 추가했다.
- `docs/DOCUMENTATION_MAP.md`를 책임 원본·프로젝트 경계·Reference·안정 호환 라우트 중심으로 컴팩트화하고, 축약 중 발견된 game-system Mode·Evidence Template·v8 Prompt·Grill Me·GPT→Codex·GitHub Pro·UX/UI 폴리싱 진입점은 회귀 테스트에 따라 복구했다.
- `skills/README.md`의 통합 전 수동 Skill 표를 Registry Router로 교체하고, 구형 `conducting-deep-requirement-interviews` agent metadata를 현행 `managing-project-intake-and-work-contract` package로 승계했다.
- 릴리스 전 `BASE_V9_INTEGRITY_AUDIT.md`를 `HISTORY_ONLY` release evidence snapshot으로 명확히 구분했다.
- 해결된 구형 PR이 반복 감사되지 않도록 `GITHUB_OBJECT_LEDGER.json`과 Migration Map에 terminal marker를 추가했다. PR #5·#28은 `[구현됨]`, PR #18·#29·#30은 `[대체됨]`으로 현행 대체 경로·검증·`do_not_reassess: true`를 기록하고 종료했다.
- Base v9.1 adds a canonical project adapter, deterministic Skill snapshot/health dashboard and one-cycle compatibility views, fail-closed cross-repository validation, dual OM/PE maturity axes, safe Windows PDF wrapper execution, and least-privilege SHA-pinned CI contracts. The v9.0 release history remains unchanged; runtime/device/accessibility/human evidence is not claimed.

- Base v9.0.0 adds Registry-derived plugin metadata, `base.lock.json`, a
  deterministic active-Skill snapshot and summary, a project-hold Sheet control
  contract, release/maturity/system/migration canon, and a Base-only integrity
  checker. Active Skill count is now an observed generated value, not a fixed
  policy number. Project adoption is a separate
  `POST_RELEASE_PROJECT_ADOPTION_WAVE` and does not block the Base release.
- The UX/UI reference card now requires open-source template license, commercial
  use, attribution, modification/redistribution, Godot compatibility,
  maintenance, dependency-removal, non-copying, transformation, and validation
  records. The Godot UI contract explicitly adds focus, input, accessibility,
  long Korean text, and resolution verification.

- 게임 시스템·난이도·전투 AI 설계 구조를 기존 `analyzing-and-refining-game-concepts`의 `system-design`·`difficulty-and-combat-ai` Mode로 통합했다. 새 독립 Skill을 추가하지 않음으로써 주 책임 분야 중복을 피하고, 전용 reference·프로젝트 contract·Registry trigger·사람용 라우팅·게임 기획 Guide·TDD 계약을 연결했다.
