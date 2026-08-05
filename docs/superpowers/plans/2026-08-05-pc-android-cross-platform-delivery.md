# PC·Android Cross-Platform Delivery Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an evidence-backed, conditional Windows PC + Android delivery profile that keeps one shared game core, adapts input/UI/lifecycle per platform, and stages STOVE·Google Play·Steam release decisions without forcing simultaneous launch.

**Architecture:** Keep execution authority in the existing game-concept, technical-production, validation, and adversarial-review Skills. Add one specialized knowledge Guide and one project planning Template, then connect them through existing discovery surfaces and protect the contract with a focused test. Do not add a new broad Skill or universalize this profile to projects whose controls, UI, performance, QA capacity, or platform obligations do not fit.

**Tech Stack:** Markdown contracts, Python `unittest`, GitHub Actions, Godot 4 display/input/lifecycle guidance.

## Global Constraints

- Baseline is exact `main@6788f40712f7182261a470bad0c1e5fb4717c632`.
- Default target pair is `WINDOWS_PC + ANDROID_MOBILE` only when the eligibility gate passes.
- Shared gameplay rules, content/data, save schema, and deterministic state remain one core.
- Input, layout, lifecycle, quality, and store services use replaceable platform adapters.
- A PC layout must not be accepted merely by shrinking it onto mobile.
- Google Play production-first sequencing is conditional on current account and testing eligibility; STOVE fees and terms remain `VERIFY_CURRENT_OFFICIAL_SOURCE` unless an authoritative current contract is available.
- Store fees, account gates, SDK/API rules, and review policies are checked-at facts, not permanent constants.
- Same-day public launch is not required.
- `docs/CHANGELOG.md` records completed Base changes, so this Draft implementation PR does not predeclare itself complete; the integrated change is recorded after merge.
- No new active Skill, Skill Registry entry, release lock, project repository, Google Sheet, or platform account change is in scope.

---

### Task 1: Contract RED

**Files:**
- Create: `tests/test_pc_android_cross_platform_delivery.py`

**Interfaces:**
- Consumes: current Base discovery and knowledge-hub paths.
- Produces: a focused contract that fails while the Guide, Template, and discovery links are absent.

- [x] **Step 1: Write the failing contract test**

Assert the specialized Guide and Template exist; require conditional eligibility, shared-core/platform-adapter boundaries, mobile UI/input/lifecycle defaults, staged release waves, current-fee/test-gate caveats, discovery links, and no new broad Skill.

- [x] **Step 2: Run an isolated RED contract probe**

Observed failure: the Guide and Template paths were both missing, and the probe exited with status 1 for that reason.

- [x] **Step 3: Record the exact failing head and failure cause in the Draft PR**

Draft PR #178 records test-only head `fcace296ac940acd7c8c9f6496c4fe08ce1648fd`. Pull-request Actions had not yet been created at that head, so no CI failure is claimed; the isolated RED probe is the available evidence.

### Task 2: Conditional Guide and Project Profile

**Files:**
- Create: `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- Create: `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`

**Interfaces:**
- Consumes: Godot multiple-resolution guidance; Android touch, lifecycle, and device-test guidance; current Steam, Google Play, and STOVE official rules; representative PC-to-mobile adaptation cases.
- Produces: `PC_ANDROID_DUAL_TARGET_CANDIDATE`, eligibility/opt-out rules, shared-core/platform-adapter contract, UI/input/lifecycle defaults, QA matrix, and release-wave decision fields.

- [ ] **Step 1: Write the minimum Guide that satisfies the contract**

Include evidence status, applicability, non-use conditions, one-core architecture, adaptive layout rules, semantic input actions, Android interruption recovery, target-device evidence, release sequencing, failure conditions, output contract, and revalidation date.

- [ ] **Step 2: Write the project planning Template**

Include target stores, account/test readiness, screen/input profiles, shared and platform-specific responsibilities, physical-device evidence, performance budget, release waves, decision status, rollback, and unresolved evidence.

- [ ] **Step 3: Adversarially review the defaults**

Reject forced dual-target development, code-sharing percentage targets, same-day launch, emulator-only mobile validation, permanent store-price assumptions, hover-only interaction, and PC-UI shrinking.

### Task 3: Existing-Route Integration

**Files:**
- Modify: `README.md`
- Modify: `START_HERE.md`
- Modify: `docs/knowledge/game-development/README.md`
- Modify: `skills/analyzing-and-refining-game-concepts/SKILL.md`

**Interfaces:**
- Consumes: the specialized Guide and Template.
- Produces: one-step discovery from Base entrypoints and conditional consumption by the existing concept/production lifecycle.

- [ ] **Step 1: Add minimal discovery links**

Link the Guide and Profile from the root README, START_HERE request router, and knowledge-hub map without duplicating detailed rules.

- [ ] **Step 2: Connect the existing Skill**

During `constrain`, `poc-contract`, or `production-gate`, require the Guide/Profile only when Windows+Android dual targeting or staged STOVE·Google Play·Steam delivery materially affects the project.

- [ ] **Step 3: Preserve completion-record authority**

Do not add a Draft-only entry to `docs/CHANGELOG.md`. Record the completed change after merge with the integrated commit and validation evidence.

### Task 4: Green Verification and PR Evidence

**Files:**
- Verify: all changed paths and PR metadata.

**Interfaces:**
- Consumes: the complete branch diff.
- Produces: exact-head test, reference, and review evidence.

- [ ] **Step 1: Run the focused and applicable repository validation through GitHub Actions**

Expected: focused contract and required `ci-gate` report success on the exact PR head.

- [ ] **Step 2: Inspect the complete PR diff**

Confirm only planned files changed, no new Skill/Registry/release-lock/project/Sheet changes occurred, and no stale `workflow/` path was introduced.

- [ ] **Step 3: Re-check current official facts and evidence limits**

Confirm volatile fees, account gates, and policies remain dated and require implementation-time revalidation.

- [ ] **Step 4: Leave the PR as Draft**

Report branch, exact head, changed files, RED/GREEN evidence, current CI state, and remaining project/device/human validation as unverified.
