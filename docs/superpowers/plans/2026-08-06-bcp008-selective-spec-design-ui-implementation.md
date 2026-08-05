# BCP-008 Selective Spec, Design, and UI Procurement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans and superpowers:test-driven-development. Each implementation task begins with a failing exact-HEAD test and ends with adversarial regression review.

**Goal:** Improve existing Base skills without adding a new active Skill by adding L2+ traceability, cross-discipline review lenses, an optional project DESIGN.md adapter, and a fail-closed external UI procurement gate.

**Architecture:** Keep the existing owner Skills. Add thin routes in the owner bodies, detailed references and templates, deterministic behavior-eval pressure cases, and a read-only shadcn source-registry procurement receipt. Do not install external UI code into Base.

**Baseline:** `cabbc59b170c5da2bb1df7e4d4d535857dd35495`

**Approval:** `https://github.com/alsdmlals4-eng/Base/pull/190#issuecomment-5198050799`

## Global constraints

- No new ACTIVE Skill.
- `skills/SKILL_REGISTRY.json` and released lock files remain unchanged.
- L0/L1 work does not receive the L2+ traceability packet or full lens set.
- `DESIGN.md` owns visual tokens only; `GAME_UX_UI_SYSTEM.md` remains the experience and behavior authority.
- External registry access, code admission, installation, and visual-quality acceptance are separate gates.
- Actual model behavior remains `NOT_RUN` without an independent model runner.
- External code is not installed into Base; the pilot is read-only source acquisition and fail-closed validation.

## Tasks

1. Commit failing contract and behavior tests; verify expected RED on exact PR HEAD.
2. Add `FEATURE_SPEC_TRACEABILITY_PACKET.md` and phase-specific owner routes.
3. Add cross-discipline adversarial review lenses without named-agent authority.
4. Add optional project `DESIGN.md` template and Godot/Web mapping contract.
5. Add external UI procurement and anti-generic quality reference.
6. Add deterministic receipt validator, exact shadcn source procurement receipt, and behavior-eval pressure cases.
7. Update documentation map, implementation evidence, and learning log only where required.
8. Run focused, behavior-eval, reference-freshness, and full Base CI checks.
9. Run adversarial attack, validate critiques, fix approved findings, and regression-recheck.
10. Keep the implementation PR Draft and do not merge without a separate user decision.
