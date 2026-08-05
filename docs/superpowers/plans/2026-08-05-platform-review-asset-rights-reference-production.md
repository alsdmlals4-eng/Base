# Platform Review, Asset Rights, and Reference Production Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Base-wide, fail-closed workflow that selects the lowest viable age rating without damaging a game’s core experience, records platform review evidence, proves per-asset rights and provenance, and turns lawful reference analysis into independently produced project assets.

**Architecture:** Keep existing Skill ownership and add one canonical game-development Guide plus two project evidence Templates. Existing project-operating, asset/plugin evaluation, art-prompt, vertical-slice, validation, and adversarial-review Skills consume those contracts; no new broad compliance Skill or automated legal judgment is introduced. Structural tests assert discoverability, required fields, fail-closed states, and preservation of the active Skill Registry and release locks.

**Tech Stack:** Python 3.12, `unittest`, Markdown, JSON, existing Base validation suites and GitHub Actions.

## Global Constraints

- Start from `agent/platform-rating-asset-rights-reference-production` at approved design commit `d2f954ec5a2434bb93b16c9376f7e7392d9900e0`; recheck latest `main` and same-goal open PRs before implementation.
- Use `LOWEST_VIABLE_RATING` as the Base default strategy: choose the lowest rating that preserves the approved core experience and can be disclosed truthfully.
- Do not make `ALL_AGES` a universal requirement. Use it only when the actual build, store materials, audio, text, ads, online features, and generated content naturally fit the applicable rating criteria.
- Keep `content_rating_target` separate from `target_audience`. A low content rating does not automatically mean the game is designed for children; declaring children in Google Play target audiences triggers additional Families requirements.
- Default platforms are Steam, STOVE, and Google Play, but record territory-specific ratings rather than pretending one global rating applies everywhere.
- Never conceal, downplay, or misstate content to obtain a lower rating. Build, store page, trailers, screenshots, uploaded but inaccessible content, ads, and questionnaires must agree.
- Preserve these asset categories: music/SFX, fonts, characters/illustrations, 3D/animation, plugins/assets, open-source libraries, AI outputs/models/terms, outsourcing contracts, and voice/composer/translator contracts.
- Distinguish `commercial_use`, `distribution_in_game_build`, and `raw_source_redistribution`; do not require raw redistribution when only packaged-game distribution is needed.
- Distinguish direct inclusion from reference-only analysis. “Modified,” “AI-regenerated,” or “inspired by” is not proof of independent creation.
- Reference-only input must be lawfully accessed, source-recorded, excluded from the shipped product, reduced to functional/general production principles, and followed by a project-specific brief plus similarity review.
- Do not commit unredacted contracts, IDs, signatures, payment details, personal data, or confidential terms to the public Base repository. Store only evidence metadata, hashes, redacted excerpts when lawful, and a secure reference.
- Use `RELEASE_BLOCKED_UNVERIFIED` whenever required rights, rating disclosures, build/store consistency, source, contract, terms version, or similarity review is unresolved.
- Do not claim legal clearance, platform approval, rating-board certification, or child-safety compliance from document existence or static tests.
- Revalidate platform policies and account-specific submission screens immediately before submission; record checked date, locale, account type, and source URL.
- Keep `skills/SKILL_REGISTRY.json`, released lock files, frozen snapshots, and generated derivatives unchanged unless a failing contract test proves an existing route is undiscoverable. This plan does not require such a change.
- Every implementation task follows RED → verify RED → minimal GREEN → verify GREEN → commit.

---

## File Responsibility Map

### Create

- `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md` — canonical rating strategy, platform matrix, rights model, reference-to-original workflow, evidence security, release blockers, and revalidation rules.
- `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md` — one record per source asset, commissioned work, open-source component, AI output/input, or reference-only input.
- `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md` — project-level Steam/STOVE/Google Play rating, target-audience, store/build consistency, rights coverage, and release decision.
- `tests/test_platform_review_asset_rights_reference_production.py` — structural and routing contract for the complete workflow.

### Modify

- `docs/superpowers/specs/2026-08-05-platform-review-asset-rights-reference-production-design.md` — add the approved clarification that Base uses `LOWEST_VIABLE_RATING`, not universal `ALL_AGES`, and separates content rating from target audience.
- `docs/knowledge/game-development/README.md` — discover the new Guide and Templates from the knowledge hub.
- `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md` — connect technical release work to rating selection, platform questionnaires, asset evidence, and release blockers.
- `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md` — add official Steam, STOVE, Google Play content-rating, target-audience/Families, and IP-policy records with checked date and revalidation conditions.
- `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md` — link decision evidence to the asset-rights record and release-compliance pack.
- `skills/managing-game-project-operating-system/SKILL.md` — install/audit/migrate the two Templates and enforce the release gate during project audits.
- `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md` — classify direct adoption, adaptation, reference-only use, and custom production; require rights evidence before adoption.
- `skills/designing-art-prompts-and-technique-cards/SKILL.md` — formalize reference-to-original visual production, forbidden imitation, and final similarity review.
- `skills/designing-vertical-slices/SKILL.md` — require representative content-risk and asset-rights evidence before production proof.
- `skills/reviewing-and-validating-project-changes/SKILL.md` — distinguish static evidence, runtime use, platform submission readiness, and legal/platform review.
- `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md` — connect image references and AI generation to the common provenance record and independent-production gate.
- `AGENTS.md` — add the invariant that release-ready claims require resolved platform and rights evidence.
- `START_HERE.md` — route release/rating/asset-rights/reference-production requests to the existing game project and asset/art Skills plus the canonical Guide.
- `README.md` — surface the new release and rights workflow without duplicating the Guide.
- `docs/DOCUMENTATION_MAP.md` — register the canonical Guide and project Templates under their single responsibilities.
- `templates/project-operations/github/documentation-governance.json` — register project evidence roles and secure-original exclusion.
- `tests/test_evidence_based_game_development_knowledge.py` — include the new Guide and official domains in the game-development knowledge contract.
- `tests/test_local_validation.py` — import the new focused contract test into local required validation.
- `tests/test_v9_machine_contracts.py` — import the new focused contract test into the Base v9 required suite.
- `docs/CHANGELOG.md` — record the workflow and its non-guarantee boundary.
- `skills/SKILL_LEARNING_LOG.md` — record why no new broad Skill or automated legal classifier was added.

## Exact Contract Vocabulary

The Guide and Templates use these exact machine-readable values.

```text
rating_strategy:
  LOWEST_VIABLE_RATING
  FIXED_PROJECT_TARGET
  PLATFORM_ASSIGNED
  UNDECIDED

creation_route:
  OWNED_ORIGINAL
  COMMISSIONED_ORIGINAL
  LICENSED_THIRD_PARTY
  OPEN_SOURCE
  AI_GENERATED
  REFERENCE_TO_ORIGINAL
  MIXED_ROUTE

rights_value:
  ALLOWED
  CONDITIONAL
  PROHIBITED
  NOT_REQUIRED
  UNKNOWN

record_status:
  APPROVED
  CONDITIONAL
  REJECTED
  RELEASE_BLOCKED_UNVERIFIED
  SUPERSEDED

reference_similarity_status:
  PASS
  REVISION_REQUIRED
  BLOCKED_UNVERIFIED
  NOT_APPLICABLE

platform_review_status:
  NOT_STARTED
  IN_PROGRESS
  READY_FOR_SUBMISSION
  SUBMITTED
  APPROVED
  RETURNED
  RELEASE_BLOCKED_UNVERIFIED
  NOT_APPLICABLE
```

The project-level pack keeps these fields separate:

```yaml
rating_strategy:
core_experience_protected:
content_rating_target:
target_audience:
children_in_target_audience:
families_policy_applicable:
platform_ratings:
platform_questionnaire_versions:
build_store_questionnaire_consistency:
asset_rights_coverage:
secure_evidence_policy:
release_decision:
```

---

### Task 1: Add the Focused RED Contract and Approved Rating Clarification

**Files:**
- Create: `tests/test_platform_review_asset_rights_reference_production.py`
- Modify: `tests/test_local_validation.py`
- Modify: `tests/test_v9_machine_contracts.py`
- Modify: `docs/superpowers/specs/2026-08-05-platform-review-asset-rights-reference-production-design.md`

**Interfaces:**
- Consumes: existing `Path`, UTF-8, `unittest`, local aggregate-import patterns, and the approved design.
- Produces: `PlatformReviewAssetRightsReferenceProductionTests` and a design clarification used by every later task.

- [ ] **Step 1: Write the missing-artifact and rating-strategy RED tests**

Create `tests/test_platform_review_asset_rights_reference_production.py`:

```python
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = (
    ROOT
    / "docs"
    / "knowledge"
    / "game-development"
    / "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md"
)
ASSET_RECORD = (
    ROOT
    / "templates"
    / "project-operations"
    / "ASSET_RIGHTS_AND_PROVENANCE_RECORD.md"
)
RELEASE_PACK = (
    ROOT
    / "templates"
    / "project-operations"
    / "GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md"
)
DESIGN = (
    ROOT
    / "docs"
    / "superpowers"
    / "specs"
    / "2026-08-05-platform-review-asset-rights-reference-production-design.md"
)


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class PlatformReviewAssetRightsReferenceProductionTests(unittest.TestCase):
    maxDiff = None

    def test_required_artifacts_exist(self) -> None:
        required = (GUIDE, ASSET_RECORD, RELEASE_PACK, DESIGN)
        missing = [
            str(path.relative_to(ROOT))
            for path in required
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_rating_strategy_is_lowest_viable_not_universal_all_ages(self) -> None:
        design = read(DESIGN)
        self.assertIn("LOWEST_VIABLE_RATING", design)
        self.assertIn("content_rating_target", design)
        self.assertIn("target_audience", design)
        self.assertIn("전체이용가를 모든 프로젝트의 강제 목표로 두지 않는다", design)
```

- [ ] **Step 2: Import the focused suite into required aggregate modules**

Add to `tests/test_local_validation.py` and `tests/test_v9_machine_contracts.py`:

```python
from tests.test_platform_review_asset_rights_reference_production import (
    PlatformReviewAssetRightsReferenceProductionTests
    as _PlatformReviewAssetRightsReferenceProductionTests,
)
```

- [ ] **Step 3: Run the focused test and verify RED**

Run:

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
```

Expected: FAIL because the Guide and two Templates do not exist and the design lacks the exact rating clarification.

- [ ] **Step 4: Add the minimal approved clarification to the design**

Under `## 2. 사용자 요구의 해석`, add:

```markdown
### 2.4 등급 목표 전략

Base의 기본 전략은 `LOWEST_VIABLE_RATING`이다. 이는 승인된 핵심 경험과 정체성을 훼손하지 않으면서 실제 콘텐츠를 정직하게 공개했을 때 가능한 가장 낮은 등급을 목표로 한다.

전체이용가를 모든 프로젝트의 강제 목표로 두지 않는다. 귀여운 캐주얼·가족 친화 게임은 전체이용가 후보가 될 수 있지만, 공포·괴이·현실적 폭력·범죄·약물·사행성·선정성이 핵심 경험에 포함된 프로젝트는 12세·15세 또는 지역별 상응 등급을 목표로 할 수 있다.

`content_rating_target`과 `target_audience`는 별도 결정이다. Google Play에서 낮은 콘텐츠 등급을 받았다는 이유만으로 아동을 타깃으로 선언하지 않으며, 아동을 타깃에 포함하면 Families·광고 SDK·데이터·개인정보 요구를 별도로 적용한다.
```

- [ ] **Step 5: Re-run the focused test**

Run the same command.

Expected: still FAIL only for the three missing implementation artifacts; the rating-strategy test passes.

- [ ] **Step 6: Commit the RED gate and design clarification**

```bash
git add \
  tests/test_platform_review_asset_rights_reference_production.py \
  tests/test_local_validation.py \
  tests/test_v9_machine_contracts.py \
  docs/superpowers/specs/2026-08-05-platform-review-asset-rights-reference-production-design.md
git commit -m "test: define platform review and asset rights gate"
```

---

### Task 2: Create the Canonical Guide and Official Platform Source Records

**Files:**
- Create: `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
- Modify: `docs/knowledge/game-development/README.md`
- Modify: `docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`
- Modify: `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- Modify: `tests/test_platform_review_asset_rights_reference_production.py`
- Modify: `tests/test_evidence_based_game_development_knowledge.py`

**Interfaces:**
- Consumes: exact vocabulary in this plan and existing evidence tiers.
- Produces: one canonical method referenced by project Templates and existing Skills.

- [ ] **Step 1: Add RED assertions for Guide sections, official sources, and hub discovery**

Append:

```python
    def test_canonical_guide_contract(self) -> None:
        guide = read(GUIDE)
        for term in (
            "LOWEST_VIABLE_RATING",
            "content_rating_target",
            "target_audience",
            "Steam",
            "STOVE",
            "Google Play",
            "build_store_questionnaire_consistency",
            "RELEASE_BLOCKED_UNVERIFIED",
            "REFERENCE_TO_ORIGINAL",
            "commercial_use",
            "distribution_in_game_build",
            "raw_source_redistribution",
            "secure_original_location",
            "법률 자문",
            "승인 보증",
        ):
            self.assertIn(term, guide)

        for domain in (
            "partner.steamgames.com",
            "studio-docs.onstove.com",
            "support.google.com/googleplay/android-developer",
        ):
            self.assertIn(domain, guide)

    def test_knowledge_hub_and_release_guide_discover_contract(self) -> None:
        hub = read("docs/knowledge/game-development/README.md")
        release = read(
            "docs/knowledge/game-development/"
            "TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md"
        )
        filename = (
            "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md"
        )
        self.assertIn(filename, hub)
        self.assertIn(filename, release)
        self.assertIn("LOWEST_VIABLE_RATING", release)
        self.assertIn("content_rating_target", release)
        self.assertIn("target_audience", release)
```

Extend `tests/test_evidence_based_game_development_knowledge.py`:

```python
"PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
```

and add these domains to the official source assertions:

```python
"studio-docs.onstove.com",
"support.google.com/googleplay/android-developer",
```

- [ ] **Step 2: Run the two focused test modules**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production \
  tests.test_evidence_based_game_development_knowledge -v
```

Expected: FAIL because the Guide, hub route, release integration, and catalog records are absent.

- [ ] **Step 3: Create the canonical Guide with these exact sections**

Create:

```markdown
# 플랫폼 심사·에셋 권리·참조 기반 독립 제작 Guide

## 1. 목적·권한·비보증
## 2. LOWEST_VIABLE_RATING
## 3. 콘텐츠 등급과 타깃 연령 분리
## 4. Steam·STOVE·Google Play Matrix
## 5. 콘텐츠 위험 항목
## 6. 에셋 범위와 creation_route
## 7. 권리 3축
## 8. Reference-to-Original 절차
## 9. 이미지·UI 세부 규칙
## 10. 음악·효과음 세부 규칙
## 11. 폰트 세부 규칙
## 12. 3D·애니메이션 세부 규칙
## 13. 플러그인·에셋·오픈소스 세부 규칙
## 14. AI 입력·모델·서비스·출력
## 15. 외주·성우·작곡·번역 계약
## 16. 증빙 보안
## 17. 빌드·상점·트레일러·설문 일치
## 18. 출시 차단과 예외 금지
## 19. 업데이트·재심사·재검증
## 20. 적대적 검토 시나리오
## 21. Output Contract
```

Use these official URLs and record `checked_at: 2026-08-05`:

```text
https://partner.steamgames.com/doc/gettingstarted/contentsurvey?l=english
https://partner.steamgames.com/steamdirect/
https://studio-docs.onstove.com/pc/StudioGuide/selfrating.html
https://support.google.com/googleplay/android-developer/answer/9898843
https://support.google.com/googleplay/android-developer/answer/9859655
https://support.google.com/googleplay/android-developer/answer/9893335
https://support.google.com/googleplay/android-developer/answer/9888072
```

The platform matrix must state:

- Steam compares the survey with the build and store page and uses general-content answers for regional ratings.
- STOVE self-rating covers 전체·12·15 and routes 청소년이용불가 to GRAC; its questionnaire covers violence, sexuality, horror, language, drugs, crime, and gambling.
- Google Play requires accurate IARC questionnaires and resubmission when relevant content changes.
- Google Play content rating and target-audience declaration are separate.
- All statements remain `RECHECK_BEFORE_SUBMISSION`.

- [ ] **Step 4: Link the Guide from the hub and technical release Guide**

Add the filename and one-sentence role to `docs/knowledge/game-development/README.md`.

In `TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`, add:

```yaml
rating_strategy: LOWEST_VIABLE_RATING | FIXED_PROJECT_TARGET | PLATFORM_ASSIGNED | UNDECIDED
content_rating_target:
target_audience:
children_in_target_audience:
families_policy_applicable:
platform_questionnaire_versions:
asset_rights_evidence_pack:
build_store_questionnaire_consistency:
release_decision:
```

Add explicit checks that all-ages is not forced, content rating is not target audience, and unresolved rights/rating evidence yields `RELEASE_BLOCKED_UNVERIFIED`.

- [ ] **Step 5: Add official source records**

Add source records to `REFERENCE_SOURCE_CATALOG.md` using the existing `T1_PRIMARY_OFFICIAL` format. Each record includes:

```yaml
checked_at: 2026-08-05
use_for:
사용_한계:
재검증_조건: 제출 직전 또는 플랫폼 정책·계정 화면 변경 시
```

Do not copy full policy text.

- [ ] **Step 6: Run focused tests and commit**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production \
  tests.test_evidence_based_game_development_knowledge -v
git add \
  docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md \
  docs/knowledge/game-development/README.md \
  docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md \
  docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md \
  tests/test_platform_review_asset_rights_reference_production.py \
  tests/test_evidence_based_game_development_knowledge.py
git commit -m "docs: add platform review and rights guide"
```

Expected: Guide and source tests PASS; Template and routing tests remain RED until later tasks.

---

### Task 3: Add Per-Asset Provenance and Project Release Evidence Templates

**Files:**
- Create: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- Create: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- Modify: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`
- Modify: `tests/test_platform_review_asset_rights_reference_production.py`

**Interfaces:**
- Consumes: Guide vocabulary and project-specific evidence locations.
- Produces: one asset-level record and one project-level release pack; no legal judgment automation.

- [ ] **Step 1: Add RED assertions for exact fields and fail-closed states**

Append:

```python
    def test_asset_record_contract(self) -> None:
        record = read(ASSET_RECORD)
        for term in (
            "asset_id:",
            "category:",
            "creation_route:",
            "source_url_or_path:",
            "source_checked_at:",
            "license_or_contract:",
            "license_version_or_terms_date:",
            "commercial_use:",
            "distribution_in_game_build:",
            "raw_source_redistribution:",
            "modification:",
            "attribution:",
            "platform_or_territory_restrictions:",
            "proof_reference:",
            "proof_hash:",
            "secure_original_location:",
            "reference_brief:",
            "reference_similarity_status:",
            "final_asset_record:",
            "RELEASE_BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, record)

        for route in (
            "OWNED_ORIGINAL",
            "COMMISSIONED_ORIGINAL",
            "LICENSED_THIRD_PARTY",
            "OPEN_SOURCE",
            "AI_GENERATED",
            "REFERENCE_TO_ORIGINAL",
            "MIXED_ROUTE",
        ):
            self.assertIn(route, record)

    def test_release_pack_contract(self) -> None:
        pack = read(RELEASE_PACK)
        for term in (
            "rating_strategy:",
            "core_experience_protected:",
            "content_rating_target:",
            "target_audience:",
            "children_in_target_audience:",
            "families_policy_applicable:",
            "platform_ratings:",
            "Steam",
            "STOVE",
            "Google Play",
            "platform_questionnaire_versions:",
            "build_store_questionnaire_consistency:",
            "asset_rights_coverage:",
            "secure_evidence_policy:",
            "release_decision:",
            "RELEASE_BLOCKED_UNVERIFIED",
        ):
            self.assertIn(term, pack)

    def test_game_evidence_pack_links_specialized_evidence(self) -> None:
        evidence = read("templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md")
        self.assertIn("ASSET_RIGHTS_AND_PROVENANCE_RECORD.md", evidence)
        self.assertIn("GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md", evidence)
        self.assertIn("REFERENCE_TO_ORIGINAL", evidence)
        self.assertIn("RELEASE_BLOCKED_UNVERIFIED", evidence)
```

- [ ] **Step 2: Run focused RED**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
```

Expected: FAIL for both missing Templates and Evidence Pack links.

- [ ] **Step 3: Create the asset-level Template**

The Template must contain:

```yaml
asset_id:
category: MUSIC_SFX | FONT | CHARACTER_ILLUSTRATION | MODEL_3D_ANIMATION | PLUGIN_ASSET | OPEN_SOURCE_LIBRARY | AI_OUTPUT_MODEL_TERMS | OUTSOURCING_CONTRACT | VOICE_COMPOSER_TRANSLATOR_CONTRACT | OTHER
name:
project:
creation_route:
creator_or_vendor:
source_url_or_path:
source_checked_at:
acquired_or_created_at:
license_or_contract:
license_version_or_terms_date:
commercial_use: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
distribution_in_game_build: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
raw_source_redistribution: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
modification: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
attribution:
platform_or_territory_restrictions:
term_or_expiration:
seat_account_or_project_restrictions:
open_source_notice_or_source_obligation:
ai_model_service_version:
ai_input_rights:
ai_output_terms:
contract_scope:
voice_clone_or_ai_training_rights:
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
proof_reference:
proof_hash:
secure_original_location:
reviewed_by:
reviewed_at:
status: APPROVED | CONDITIONAL | REJECTED | RELEASE_BLOCKED_UNVERIFIED | SUPERSEDED
notes:
```

Include rules:

- `UNKNOWN` in a required right blocks release.
- `REFERENCE_TO_ORIGINAL` must link a reference-only record and a separate final asset record.
- A final asset never inherits safety merely from “AI-generated,” “modified,” or “inspired.”
- Secure originals stay outside public GitHub.

- [ ] **Step 4: Create the project-level release pack**

The Template must include:

```yaml
release_pack_id:
project:
baseline_commit:
target_build:
rating_strategy:
core_experience_protected:
content_rating_target:
target_audience:
children_in_target_audience:
families_policy_applicable:
platform_ratings:
platform_questionnaire_versions:
platform_policy_checked_at:
content_risk_matrix:
build_store_questionnaire_consistency:
asset_rights_coverage:
open_source_notice_status:
ai_disclosure_status:
contract_coverage:
secure_evidence_policy:
unresolved_items:
release_decision:
reviewed_by:
reviewed_at:
```

Provide one row for Steam, STOVE, and Google Play with:

```text
target/assigned rating
questionnaire version or checked date
build evidence
store evidence
trailer/screenshot evidence
AI disclosure
ads/UGC/online interaction
current status
```

The rating section must explicitly say:

```text
ALL_AGES is a candidate, not a universal Base mandate.
Content rating and target audience are independent declarations.
```

- [ ] **Step 5: Link the specialized records from the general Evidence Pack**

Add a section:

```markdown
## 자산 권리·플랫폼 출시 특화 증빙

- 자산별 기록: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- 프로젝트 출시 Pack: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- `REFERENCE_TO_ORIGINAL` 참조 입력과 최종 자산은 별도 Record로 연결한다.
- 필수 권리·등급·설문·빌드 일치가 미확인되면 `RELEASE_BLOCKED_UNVERIFIED`다.
```

- [ ] **Step 6: Run tests and commit**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
git add \
  templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md \
  templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md \
  templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md \
  tests/test_platform_review_asset_rights_reference_production.py
git commit -m "feat: add asset rights and release evidence templates"
```

Expected: Template and specialized Evidence Pack tests PASS.

---

### Task 4: Integrate Existing Skills Without Creating a New Broad Skill

**Files:**
- Modify: `skills/managing-game-project-operating-system/SKILL.md`
- Modify: `skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md`
- Modify: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- Modify: `skills/designing-vertical-slices/SKILL.md`
- Modify: `skills/reviewing-and-validating-project-changes/SKILL.md`
- Modify: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- Modify: `tests/test_platform_review_asset_rights_reference_production.py`

**Interfaces:**
- Consumes: canonical Guide and project Templates.
- Produces: existing Skill routes for installation, evaluation, creation, production proof, and final validation.

- [ ] **Step 1: Add RED routing and no-duplicate-Skill tests**

Append:

```python
    def test_existing_skill_routes_consume_the_contract(self) -> None:
        files = (
            "skills/managing-game-project-operating-system/SKILL.md",
            "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md",
            "skills/designing-art-prompts-and-technique-cards/SKILL.md",
            "skills/designing-vertical-slices/SKILL.md",
            "skills/reviewing-and-validating-project-changes/SKILL.md",
            "docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md",
        )
        for path in files:
            text = read(path)
            self.assertIn(
                "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md",
                text,
                path,
            )
            self.assertIn("RELEASE_BLOCKED_UNVERIFIED", text, path)

        asset_skill = read(
            "skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md"
        )
        for term in (
            "LICENSED_THIRD_PARTY",
            "REFERENCE_TO_ORIGINAL",
            "BUILD_CUSTOM",
            "distribution_in_game_build",
        ):
            self.assertIn(term, asset_skill)

        art_skill = read(
            "skills/designing-art-prompts-and-technique-cards/SKILL.md"
        )
        for term in (
            "reference_brief",
            "forbidden_expression",
            "reference_similarity_status",
        ):
            self.assertIn(term, art_skill)

    def test_no_new_broad_compliance_skill_or_registry_identity_change(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        forbidden = (
            '"skill_id":"platform-review-compliance"',
            '"skill_id":"asset-rights-compliance"',
            '"skill_id":"reference-to-original-production"',
        )
        for token in forbidden:
            self.assertNotIn(token, registry)
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
```

Expected: FAIL because existing Skills do not yet reference the canonical Guide or blocker.

- [ ] **Step 3: Extend `managing-game-project-operating-system`**

In install/audit/migrate/release phases, require:

- project copies or registered equivalents of both Templates;
- inventory of all nine requested asset/contract categories;
- migration of existing asset records without overwriting project-specific evidence;
- target rating and target audience as separate project decisions;
- project audit finding `RELEASE_BLOCKED_UNVERIFIED` for missing required evidence.

Do not add a new Skill mode solely for compliance; integrate with existing audit and lifecycle modes.

- [ ] **Step 4: Extend the asset/plugin evaluation Skill**

Add the decision sequence:

```text
ADOPT / ADAPT
→ direct inclusion
→ LICENSED_THIRD_PARTY or OPEN_SOURCE
→ required rights evidence

REFERENCE_ONLY
→ REFERENCE_TO_ORIGINAL
→ no source asset in build
→ independent brief and final record

BUILD_CUSTOM
→ OWNED_ORIGINAL, COMMISSIONED_ORIGINAL, AI_GENERATED, or MIXED_ROUTE
→ input and contract evidence
```

Require `distribution_in_game_build` separately from `raw_source_redistribution`.

- [ ] **Step 5: Extend the art-prompt and image policy route**

Add exact fields:

```text
reference_sources
reference_brief
forbidden_expression
final_asset_record
reference_similarity_status
```

Require removal of identifiable character design, composition, logo, UI skin, signature shape combinations, and artist-specific imitation. State that AI transformation does not erase input-rights or similarity review.

- [ ] **Step 6: Extend vertical-slice and validation Skills**

Vertical Slice cannot claim production proof when representative assets are `UNKNOWN`, reference-only originals are present in the build, or the intended rating depends on hiding representative content.

Validation must report separately:

```text
STATIC_EVIDENCE_CHECKED
RUNTIME_ASSET_USE_CHECKED
BUILD_STORE_CONSISTENCY_CHECKED
PLATFORM_SUBMISSION_NOT_RUN
LEGAL_REVIEW_NOT_PERFORMED
```

Any required unresolved item remains `RELEASE_BLOCKED_UNVERIFIED`.

- [ ] **Step 7: Run tests and commit**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
git add \
  skills/managing-game-project-operating-system/SKILL.md \
  skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md \
  skills/designing-art-prompts-and-technique-cards/SKILL.md \
  skills/designing-vertical-slices/SKILL.md \
  skills/reviewing-and-validating-project-changes/SKILL.md \
  docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md \
  tests/test_platform_review_asset_rights_reference_production.py
git commit -m "feat: integrate rights and rating gates into existing skills"
```

Expected: routing tests PASS and Registry remains unchanged.

---

### Task 5: Add Top-Level Discovery, Governance, and Public-Repository Safety

**Files:**
- Modify: `AGENTS.md`
- Modify: `START_HERE.md`
- Modify: `README.md`
- Modify: `docs/DOCUMENTATION_MAP.md`
- Modify: `templates/project-operations/github/documentation-governance.json`
- Modify: `tests/test_platform_review_asset_rights_reference_production.py`

**Interfaces:**
- Consumes: canonical Guide and two Templates.
- Produces: one-step discovery and project governance roles without a second source of truth.

- [ ] **Step 1: Add RED discovery and governance tests**

Append:

```python
    def test_top_level_discovery_and_governance(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md"
        )
        asset_path = (
            "templates/project-operations/"
            "ASSET_RIGHTS_AND_PROVENANCE_RECORD.md"
        )
        release_path = (
            "templates/project-operations/"
            "GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md"
        )

        for path in (
            "AGENTS.md",
            "START_HERE.md",
            "README.md",
            "docs/DOCUMENTATION_MAP.md",
        ):
            text = read(path)
            self.assertIn(guide_path, text, path)

        doc_map = read("docs/DOCUMENTATION_MAP.md")
        self.assertIn(asset_path, doc_map)
        self.assertIn(release_path, doc_map)

        governance = json.loads(
            read("templates/project-operations/github/documentation-governance.json")
        )
        serialized = json.dumps(
            governance,
            ensure_ascii=False,
            sort_keys=True,
        )
        for token in (
            "ASSET_RIGHTS_AND_PROVENANCE_RECORD",
            "GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK",
            "secure_original_location",
            "RELEASE_BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, serialized)

    def test_public_repository_safety_is_explicit(self) -> None:
        for path in (
            GUIDE,
            ASSET_RECORD,
            RELEASE_PACK,
            "AGENTS.md",
        ):
            text = read(path)
            self.assertIn("unredacted", text.lower())
            self.assertIn("secure_original_location", text)
            self.assertIn("공개", text)
```

- [ ] **Step 2: Run RED**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
```

Expected: FAIL for missing top-level paths and governance roles.

- [ ] **Step 3: Add the Base invariant**

In `AGENTS.md`, add:

```text
출시 준비·상점 제출·제품 자산 승인 주장은 목표 등급·타깃 연령·플랫폼 설문·실제 빌드/상점 일치와 자산별 권리·출처·계약 증빙이 확인된 경우만 가능하다. 미확인은 RELEASE_BLOCKED_UNVERIFIED다. 공개 저장소에 unredacted 계약 원본·신분증·서명·결제·개인정보를 커밋하지 않고 secure_original_location 참조만 남긴다.
```

- [ ] **Step 4: Add routing and documentation map entries**

`START_HERE.md` routes:

```text
플랫폼 출시·이용등급·스토어 설문·에셋 권리·레퍼런스 독립 제작
→ managing-game-project-operating-system
→ 필요 시 evaluating-godot-assets-and-plugins-before-creation
→ 이미지/UI는 designing-art-prompts-and-technique-cards
→ canonical Guide
```

`README.md` adds one compact entry.

`docs/DOCUMENTATION_MAP.md` declares:

- Guide: common policy and method authority.
- Asset Record: per-asset project evidence Template, not Base project evidence.
- Release Pack: per-project submission and release decision Template, not a platform approval artifact.

- [ ] **Step 5: Register governance roles**

Add JSON roles whose exact identifiers are:

```text
ASSET_RIGHTS_AND_PROVENANCE_RECORD
GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK
```

Each role states:

- project-owned instantiated evidence;
- Base Template is not project truth;
- `secure_original_location` points outside public GitHub;
- unknown required fields block release;
- original contracts and personal data are forbidden in public repositories.

Keep JSON valid and preserve existing unrelated roles.

- [ ] **Step 6: Run tests and commit**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
python -m json.tool \
  templates/project-operations/github/documentation-governance.json \
  > /dev/null
git add \
  AGENTS.md \
  START_HERE.md \
  README.md \
  docs/DOCUMENTATION_MAP.md \
  templates/project-operations/github/documentation-governance.json \
  tests/test_platform_review_asset_rights_reference_production.py
git commit -m "docs: route platform and asset evidence workflow"
```

Expected: discovery, governance, and public-repository safety tests PASS.

---

### Task 6: Record Adversarial Cases, Learning Boundaries, and Full Verification

**Files:**
- Modify: `docs/CHANGELOG.md`
- Modify: `skills/SKILL_LEARNING_LOG.md`
- Modify: `tests/test_platform_review_asset_rights_reference_production.py`
- Review only: `skills/SKILL_REGISTRY.json`
- Review only: released `base-v*.lock.json`
- Review only: frozen snapshots and generated derivatives

**Interfaces:**
- Consumes: all prior tasks.
- Produces: complete evidence for the PR without claiming unperformed legal or platform review.

- [ ] **Step 1: Add final RED assertions for learning and adversarial coverage**

Append:

```python
    def test_adversarial_and_learning_record(self) -> None:
        guide = read(GUIDE)
        for term in (
            "상업 사용 가능하지만 게임 포함 배포 불가",
            "폰트 임베딩",
            "Content ID",
            "NOTICE",
            "AI 약관 버전",
            "외주 권리 범위",
            "음성 복제",
            "설문과 빌드 불일치",
            "민감한 계약 원본",
            "조금 바꿨으므로",
        ):
            self.assertIn(term, guide)

        changelog = read("docs/CHANGELOG.md")
        learning = read("skills/SKILL_LEARNING_LOG.md")
        self.assertIn("LOWEST_VIABLE_RATING", changelog)
        self.assertIn("참조 기반 독립 제작", changelog)
        self.assertIn("새 광역 Skill을 추가하지 않음", learning)
        self.assertIn("자동 법률 판정기를 추가하지 않음", learning)
```

- [ ] **Step 2: Run focused RED**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production -v
```

Expected: FAIL until the Guide’s adversarial section and logs contain the exact cases.

- [ ] **Step 3: Complete the adversarial section**

The Guide must attack at least:

1. commercial use allowed but packaged-game distribution prohibited;
2. raw redistribution confused with packaged distribution;
3. font desktop license lacking app/game embedding;
4. music license allowing use but causing Content ID claims;
5. open-source attribution, NOTICE, source, or modification obligations omitted;
6. AI terms changed after generation and no terms-version snapshot exists;
7. commissioned work lacks platform, territory, duration, modification, or derivative-use scope;
8. voice contract lacks cloning, synthetic voice, or AI-training limits;
9. reference brief still preserves identifiable expression;
10. build, store page, trailer, screenshots, and questionnaire disagree;
11. low rating is achieved only by hiding content from the questionnaire;
12. all-ages content rating is confused with child-directed target audience;
13. unredacted contracts or personal data are committed publicly;
14. static Template completion is reported as legal clearance or platform approval.

- [ ] **Step 4: Update Change and Learning Logs**

`docs/CHANGELOG.md` records:

- `LOWEST_VIABLE_RATING`, not universal all-ages;
- Steam/STOVE/Google Play review matrix;
- two project Templates;
- reference-to-original workflow;
- fail-closed release blocker;
- sensitive evidence boundary.

`skills/SKILL_LEARNING_LOG.md` records:

- new broad Skill rejected because existing lifecycle Skills own execution;
- automatic legal or similarity classifier rejected because facts and human review cannot be inferred from filenames or hashes;
- project Pilot, actual platform submission, and legal review remain future evidence.

- [ ] **Step 5: Run focused and related suites**

```bash
python -m unittest \
  tests.test_platform_review_asset_rights_reference_production \
  tests.test_evidence_based_game_development_knowledge -v
python -m unittest tests.test_local_validation -v
python -m unittest tests.test_v9_machine_contracts -v
```

Expected: PASS. Record unavailable dependencies or skipped environments as `NOT_RUN`, not PASS.

- [ ] **Step 6: Run repository contract checks**

Use the repository’s current required commands from CI and `AGENTS.md`. At minimum:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python -m json.tool \
  templates/project-operations/github/documentation-governance.json \
  > /dev/null
git diff --check
```

Expected: PASS.

- [ ] **Step 7: Verify protected identity and release boundaries**

```bash
git diff --exit-code \
  d2f954ec5a2434bb93b16c9376f7e7392d9900e0..HEAD \
  -- skills/SKILL_REGISTRY.json \
     base-v9.1.lock.json \
     base-v9.2.lock.json \
     base-v9.3.lock.json \
     base-v9.4.1.lock.json \
     base-v9.4.2.lock.json \
     base-v9.4.3.lock.json
```

Expected: no diff. Also inspect generated/frozen paths named by current Base validation; do not update them merely to silence a stale-reference failure.

- [ ] **Step 8: Commit logs and final test contract**

```bash
git add \
  docs/CHANGELOG.md \
  skills/SKILL_LEARNING_LOG.md \
  tests/test_platform_review_asset_rights_reference_production.py \
  docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md
git commit -m "test: verify platform review and asset rights workflow"
```

- [ ] **Step 9: Perform exact-head PR review**

Check:

```text
changed files match the approved scope
unresolved review threads = 0
P0/P1 findings = 0
focused tests = PASS
required repository tests = PASS
Registry and release locks = unchanged
legal review = NOT_PERFORMED
real platform submission = NOT_RUN
real project asset audit = NOT_RUN
```

Update Draft PR #163 with exact commit SHA, commands, results, skipped checks, and rollback notes. Keep Draft until all implementation checks are green and review findings are resolved.

---

## Plan Self-Review Result

- Spec coverage: platform matrix, rating strategy, target-audience separation, all nine asset/contract categories, rights axes, reference-to-original workflow, AI/outsourcing evidence, secure storage, release blockers, routing, and adversarial cases each map to a task.
- Placeholder scan: no deferred implementation placeholders are present.
- Type consistency: exact enum values and field names are identical across Guide, Templates, tests, and Skill integration.
- Scope: one implementation plan is appropriate because every change supports one release-evidence workflow and shares the same canonical Guide and Templates.
- Exclusions remain explicit: no new broad Skill, legal classifier, platform submission, project migration, real asset audit, rating guarantee, or release-lock update.
