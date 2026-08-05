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
LEARNING_LOG = (
    ROOT
    / "skills"
    / "managing-game-project-operating-system"
    / "LEARNING_LOG.md"
)


def read(path: Path | str) -> str:
    target = path if isinstance(path, Path) else ROOT / path
    return target.read_text(encoding="utf-8")


class PlatformReviewAssetRightsReferenceProductionTests(unittest.TestCase):
    maxDiff = None

    def test_required_artifacts_exist(self) -> None:
        required = (GUIDE, ASSET_RECORD, RELEASE_PACK, LEARNING_LOG)
        missing = [
            str(path.relative_to(ROOT))
            for path in required
            if not path.is_file()
        ]
        self.assertEqual([], missing)

    def test_rating_strategy_avoids_adults_only_without_forcing_all_ages(self) -> None:
        guide = read(GUIDE)
        for term in (
            "LOWEST_VIABLE_RATING",
            "AVOID_ADULTS_ONLY",
            "content_rating_target",
            "target_audience",
            "청소년이용불가·18+를 기본적으로 회피",
            "전체이용가를 모든 프로젝트의 강제 목표로 두지 않는다",
        ):
            self.assertIn(term, guide)

    def test_canonical_guide_contract(self) -> None:
        guide = read(GUIDE)
        for term in (
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
            "adult_only_avoidance:",
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

    def test_no_new_broad_compliance_skill(self) -> None:
        registry = read("skills/SKILL_REGISTRY.json")
        forbidden = (
            '"skill_id":"platform-review-compliance"',
            '"skill_id":"asset-rights-compliance"',
            '"skill_id":"reference-to-original-production"',
        )
        for token in forbidden:
            self.assertNotIn(token, registry)

    def test_knowledge_hub_and_top_level_discovery(self) -> None:
        guide_path = (
            "docs/knowledge/game-development/"
            "PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md"
        )
        for path in (
            "docs/knowledge/game-development/README.md",
            "docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md",
            "AGENTS.md",
            "START_HERE.md",
            "README.md",
            "docs/DOCUMENTATION_MAP.md",
        ):
            self.assertIn(guide_path, read(path), path)

    def test_documentation_governance_roles(self) -> None:
        governance = json.loads(
            read("templates/project-operations/github/documentation-governance.json")
        )
        serialized = json.dumps(governance, ensure_ascii=False, sort_keys=True)
        for token in (
            "ASSET_RIGHTS_AND_PROVENANCE_RECORD",
            "GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK",
            "secure_original_location",
            "RELEASE_BLOCKED_UNVERIFIED",
        ):
            self.assertIn(token, serialized)

    def test_public_repository_safety_is_explicit(self) -> None:
        for path in (GUIDE, ASSET_RECORD, RELEASE_PACK, "AGENTS.md"):
            text = read(path)
            self.assertIn("unredacted", text.lower())
            self.assertIn("secure_original_location", text)
            self.assertIn("공개", text)

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
        learning = read(LEARNING_LOG)
        self.assertIn("LOWEST_VIABLE_RATING", changelog)
        self.assertIn("참조 기반 독립 제작", changelog)
        self.assertIn("새 광역 Skill을 추가하지 않음", learning)
        self.assertIn("자동 법률 판정기를 추가하지 않음", learning)


if __name__ == "__main__":
    unittest.main()
