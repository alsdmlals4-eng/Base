# Backend, AI Coding, Deployment, and Media Source Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add source-backed backend/API, AI coding, cloud deployment, PC capture, and AI media-editing discovery routes without creating duplicate Skills or changing current Base authority.

**Architecture:** Extend the existing periodic discovery seed document with four role-separated source groups. Route every group to current Base owners and enforce evidence ceilings with one focused regression test. Existing Cloud Run, AI development, YouTube/video, and art owners remain canonical.

**Tech Stack:** Markdown source contracts, Python `unittest`, GitHub Actions Base validation workflows.

## Global Constraints

- Source/reference expansion only; no new ACTIVE Skill, deployment, cloud resource creation, or product-direction change.
- `GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md` remains the backend/deployment decision owner.
- `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md` remains the AI coding/eval owner.
- `producing-game-development-youtube-videos` remains the video production owner.
- Image/thumbnail findings route to `designing-art-prompts-and-technique-cards` and the art-direction owner.
- Cloud Run is not universally superior; compare alternatives by workload fit and measured evidence.
- AI coding vendor/benchmark claims do not prove project correctness, security, productivity, or merge readiness.
- Capture/editing product features do not prove actual PC performance, output quality, rights safety, or cost efficiency.
- Vendor pricing, quotas, models, and product features are volatile and must be reverified before adoption.

---

### Task 1: Add focused RED regression

**Files:**
- Modify: `tests/test_periodic_external_source_discovery_seeds.py`

**Interfaces:**
- Consumes: current `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md` text contract.
- Produces: `test_backend_ai_deploy_and_media_sources_route_to_existing_owners` enforcing source identity, routing, and claim ceilings.

- [ ] **Step 1: Add the failing test**

Add one test that reads the discovery seed document and asserts these required tokens/groups are present:

```python
def test_backend_ai_deploy_and_media_sources_route_to_existing_owners(self):
    text = self.discovery_seeds.read_text(encoding="utf-8")

    required = [
        "Backend / API engineering",
        "OpenAPI Specification",
        "FastAPI official",
        "PostgreSQL official",
        "OWASP API Security",
        "AI coding / coding agents",
        "OpenAI Developers / Codex",
        "Claude Code",
        "Gemini CLI",
        "aider",
        "SWE-bench",
        "Deployment / WAS / cloud runtime",
        "Cloudflare Workers",
        "Fly.io Machines",
        "Railway",
        "Render",
        "PC capture and AI-assisted media editing",
        "OBS Studio",
        "FFmpeg",
        "Xbox Game Bar",
        "NVIDIA App / ShadowPlay",
        "DaVinci Resolve",
        "Adobe Premiere / Photoshop / Firefly",
        "Runway",
        "GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md",
        "AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md",
        "producing-game-development-youtube-videos",
        "designing-art-prompts-and-technique-cards",
        "Cloud Run is not universally better",
        "benchmark score does not prove project correctness",
        "actual PC capture measurement",
        "rights + provenance + similarity",
    ]
    for token in required:
        self.assertIn(token, text)
```

- [ ] **Step 2: Run the focused test and confirm RED**

Run the repository's Evidence Knowledge workflow/test command that already includes `tests/test_periodic_external_source_discovery_seeds.py`, or execute the focused unittest module in the same environment.

Expected: existing discovery-seed tests pass and the new test fails because the new source groups are absent.

- [ ] **Step 3: Record RED head in the PR body**

Record exact head SHA, total focused test count, and the expected missing-token reason. Do not count unrelated skipped tests as PASS.

---

### Task 2: Add four source groups with existing-owner routing

**Files:**
- Modify: `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`

**Interfaces:**
- Consumes: current Watchlist governance, existing Cloud Run backend guide, AI-assisted development guide, YouTube video Skill, art technique owner.
- Produces: four `ACTIVE_DISCOVERY_SEED` groups consumed by periodic scans and weekly reviews.

- [ ] **Step 1: Add Backend / API engineering group**

Include source entries and boundaries for:

```text
OpenAPI Specification -> AUTHORITY_TARGET for OAS behavior/specification
FastAPI official docs -> AUTHORITY_TARGET for FastAPI behavior only
PostgreSQL official docs -> AUTHORITY_TARGET for PostgreSQL behavior only
Redis official docs -> AUTHORITY_TARGET when Redis is selected
OWASP API Security Project -> PROFESSIONAL_SECURITY_GUIDANCE / not security PASS
```

Route architecture, API contract, auth/idempotency/state/security findings to `GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md` and target-project implementation/tests. State that FastAPI/PostgreSQL/Redis are not mandatory stack choices.

- [ ] **Step 2: Add AI coding / coding agents group**

Include:

```text
OpenAI Developers / Codex official docs
Anthropic Claude Code official docs
Gemini CLI / Gemini Code Assist official docs
existing GitHub Copilot AUTHORITY_TARGET reuse
Aider official docs/repository
SWE-bench official leaderboard/papers as benchmark/discovery evidence
```

Route to `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`. Require project-local test/diff/review/eval evidence. Include exact phrase `benchmark score does not prove project correctness` and preserve vendor/product version freshness.

- [ ] **Step 3: Add Deployment / WAS / cloud runtime comparison group**

Keep Google Cloud Run as the existing Base-owned default candidate for appropriate stateless HTTPS/container workloads. Add official discovery sources for:

```text
Cloudflare Workers
Fly.io Machines
Railway
Render
```

Compare workload shape, protocol, durable state, region/latency, worker lifetime, operational burden, portability, observability, quota, provider lock-in, recovery, and measured cost. Include exact phrase `Cloud Run is not universally better`.

- [ ] **Step 4: Add PC capture and AI-assisted media editing group**

Capture/local processing sources:

```text
OBS Studio official Knowledge Base
FFmpeg official documentation
Microsoft Xbox Game Bar / Snipping Tool official support
NVIDIA App / ShadowPlay official documentation
```

Editing sources:

```text
DaVinci Resolve official documentation
Adobe Premiere / Photoshop / Firefly official documentation
Runway official help/documentation
```

Route video work to `producing-game-development-youtube-videos` and image/thumbnail work to `designing-art-prompts-and-technique-cards` plus art direction. Require `actual PC capture measurement` for frame pacing/audio sync/encoder/storage/quality claims and `rights + provenance + similarity` review for AI-assisted edits.

- [ ] **Step 5: Run focused GREEN validation**

Run the same focused Evidence Knowledge test path used for RED.

Expected: all discovery-seed tests pass, including `test_backend_ai_deploy_and_media_sources_route_to_existing_owners`.

- [ ] **Step 6: Commit source implementation**

Commit test + discovery source implementation with a bounded message such as:

```text
docs: add backend AI deploy and media sources
```

---

### Task 3: Full validation and adversarial review

**Files:**
- Review only unless an evidence-backed omission is found.

**Interfaces:**
- Consumes: exact feature head, current main, PR diff, existing source/governance owners.
- Produces: merge decision and `OMISSION | CONFLICT | COMPLEMENT_GAP | DUPLICATE_WORK | NO_MATERIAL_FOLLOWUP` verdict.

- [ ] **Step 1: Run full relevant CI**

Require fresh exact-head results for:

```text
Validate Evidence-Based Game Development Knowledge
Validate Base v9 Operating Contracts
Validate Game Project Operating System
ubuntu-contract / canonical reference freshness
docs-validation / Required Check topology
publication-validation
final ci-gate
```

Record platform-specific skipped jobs as `skipped / non-applicable`, not PASS.

- [ ] **Step 2: Adversarially attack the source set**

Check at minimum:

```text
mandatory-stack overreach
Cloud-Run universalization
vendor marketing as authority
AI leaderboard laundering
stale model/product/pricing facts
security-guidance-as-security-PASS
capture-feature-as-performance-proof
AI-edit availability as rights grant
source duplication with current Watchlist
new-Skill inflation
same-goal PR duplication
untouched consumer omission
```

- [ ] **Step 3: Apply only validated minimal fixes**

If a finding is `OMISSION` or `COMPLEMENT_GAP` inside scope, make the smallest source/test correction and rerun focused + required CI. Do not change policy/authority/security/product direction.

- [ ] **Step 4: Final PR gate**

Verify current main, exact head, same-goal open/recent PRs, unresolved review threads, mergeability, strict up-to-date status, and final `ci-gate` success.

- [ ] **Step 5: Squash merge with expected-head protection**

Only merge if all low-risk Base gates remain satisfied.

- [ ] **Step 6: Post-merge monitor loop**

Read merged main, confirm the source groups remain present, recheck same-goal PRs and consumers, classify any follow-up, and report expected outcomes separately from measured outcomes.