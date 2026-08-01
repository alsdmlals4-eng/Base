#!/usr/bin/env python3
"""Synchronize the approved Base v9.4 Skill and UI consumers."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, section: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    suffix = "" if text.endswith("\n") else "\n"
    write(path, text + suffix + "\n" + section.rstrip() + "\n")


def insert_before(path: Path, marker: str, block_marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if block_marker in text:
        return
    if marker not in text:
        raise RuntimeError(f"Cannot locate insertion marker in {path.relative_to(ROOT)}")
    write(path, text.replace(marker, block.rstrip() + "\n" + marker, 1))


def replace_once(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    if old not in text:
        raise RuntimeError(f"Cannot locate {label} in {path.relative_to(ROOT)}")
    write(path, text.replace(old, new, 1))


def main() -> int:
    append_once(
        ROOT / "skills/README.md",
        "## Base v9.4 AI 운영 진입점",
        """## Base v9.4 AI 운영 진입점

- 모델·추론 단계·Prompt caching·비용 추정·실측 재보정: `optimizing-ai-model-and-prompt-costs`
- 지시 권위·Interface-first Prompt·Context 큐레이션·Artifact 주장 상한: `docs/knowledge/game-development/AI_INSTRUCTION_AND_CONTEXT_DESIGN_METHOD.md`
- 게임 UI 모션·중단·반복·Reduced Motion·도메인 상태 권위: `auditing-and-refining-ui-art` → `references/ui-motion-and-interaction-principles.md`

Luna / Terra / Sol은 논리적 작업 등급이며 실제 provider 옵션의 존재를 보장하지 않는다. BCP-2026-004는 새 활성 Skill을 만들지 않고 기존 intake·simplifying·UI Skill의 책임으로 유지한다.
""",
    )

    reference_card = ROOT / "templates/research/UX_UI_REFERENCE_CARD.md"
    replace_once(
        reference_card,
        """  reduced_motion_mute_haptic_off_path:
  before_after_validation:
copying_prohibited:
""",
        """  reduced_motion_mute_haptic_off_path:
  before_after_validation:
motion_interaction_evidence:
  motion_purpose: ORIENT | CONFIRM | PROGRESS | RESULT | WARN | REWARD | DECORATE | NOT_APPLICABLE
  staging_and_first_attention:
  input_accepted_processing_result:
  interruption_and_instant_complete:
  rapid_repeat_and_reentry:
  reduced_motion_mute_haptic_off:
  domain_state_authority:
  target_platform_performance:
copying_prohibited:
""",
        "UI motion evidence fields",
    )
    append_once(
        reference_card,
        "11. UI 모션 자료는",
        """11. UI 모션 자료는 staging·입력 접수/처리 중/결과·중단·즉시 완료·빠른 반복·재진입·Reduced Motion·mute·haptic-off·도메인 상태 권위를 함께 검토한다.
12. AnimationPlayer·Tween 표현이 구매·보상·저장·진행의 실제 결과를 소유하는 사례는 `AVOID`한다.
""",
    )

    insert_before(
        ROOT / "tests/test_game_ux_ui_system.py",
        "\n\nif __name__ == \"__main__\":\n",
        "def test_ui_motion_reference_is_routed_and_reviewable",
        '''
    def test_ui_motion_reference_is_routed_and_reviewable(self) -> None:
        motion = REFERENCE_ROOT / "ui-motion-and-interaction-principles.md"
        self.assertTrue(motion.is_file())
        text = motion.read_text(encoding="utf-8")
        for required in (
            "staging",
            "입력 접수",
            "처리 중",
            "중단",
            "즉시 완료",
            "빠른 반복",
            "재진입",
            "Reduced Motion",
            "mute",
            "haptic-off",
            "AnimationPlayer",
            "Tween",
            "도메인 상태 권위",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
        self.assertIn("ui-motion-and-interaction-principles.md", SKILL.read_text(encoding="utf-8"))

    def test_reference_card_tracks_motion_claims_and_domain_authority(self) -> None:
        text = REFERENCE_CARD.read_text(encoding="utf-8")
        for required in (
            "motion_interaction_evidence",
            "motion_purpose",
            "input_accepted_processing_result",
            "interruption_and_instant_complete",
            "rapid_repeat_and_reentry",
            "domain_state_authority",
            "target_platform_performance",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_registry_routes_v94_ui_motion_without_a_duplicate_skill(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        ui = by_id["auditing-and-refining-ui-art"]
        for trigger in ("ui-motion-design", "animation-interruption", "instant-complete", "reduced-motion"):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, ui["trigger_tags"])
        self.assertNotIn("designing-ui-motion", by_id)
''',
    )

    insert_before(
        ROOT / "tests/test_skill_system_coverage.py",
        "\n\nclass LegacyRetentionArchiveGovernanceTests(unittest.TestCase):\n",
        "def test_base_v94_ai_operations_have_distinct_registry_boundaries",
        '''
    def test_base_v94_ai_operations_have_distinct_registry_boundaries(self) -> None:
        registry = json.loads((ROOT / "skills/SKILL_REGISTRY.json").read_text(encoding="utf-8"))
        by_id = {item["skill_id"]: item for item in registry["skills"]}
        model = by_id["optimizing-ai-model-and-prompt-costs"]
        self.assertEqual("skills/optimizing-ai-model-and-prompt-costs/SKILL.md", model["path"])
        self.assertEqual("ACTIVE", model["status"])
        self.assertFalse(model["load_by_default"])
        self.assertTrue({"model-recommendation", "prompt-caching", "provider-profile"}.issubset(model["trigger_tags"]))

        intake = by_id["managing-project-intake-and-work-contract"]
        simplifying = by_id["simplifying-skill-bodies"]
        ui = by_id["auditing-and-refining-ui-art"]
        self.assertIn("instruction-authority", intake["trigger_tags"])
        self.assertIn("example-as-fixture", simplifying["trigger_tags"])
        self.assertIn("ui-motion-design", ui["trigger_tags"])
        self.assertNotIn("designing-ai-instructions", by_id)
        self.assertNotIn("designing-ui-motion", by_id)
''',
    )

    workflow = ROOT / ".github/workflows/validate-game-ux-ui-system.yml"
    replace_once(
        workflow,
        '      - "tests/test_game_ux_ui_system.py"\n      - "tests/test_ui_art_audit.py"\n',
        '      - "tests/test_game_ux_ui_system.py"\n      - "tests/test_base_v9_4_ai_operations_contract.py"\n      - "tests/test_ui_art_audit.py"\n',
        "pull request UX/UI test paths",
    )
    # The same path block occurs in the push section; replace the next remaining occurrence.
    replace_once(
        workflow,
        '      - "tests/test_game_ux_ui_system.py"\n      - "tests/test_ui_art_audit.py"\n',
        '      - "tests/test_game_ux_ui_system.py"\n      - "tests/test_base_v9_4_ai_operations_contract.py"\n      - "tests/test_ui_art_audit.py"\n',
        "push UX/UI test paths",
    )
    replace_once(
        workflow,
        """          python -m unittest \\
            tests/test_game_ux_ui_system.py \\
            tests/test_ui_art_audit.py \\
            -v
""",
        """          python -m unittest \\
            tests/test_game_ux_ui_system.py \\
            tests/test_base_v9_4_ai_operations_contract.py \\
            tests/test_ui_art_audit.py \\
            -v
""",
        "UX/UI v9.4 test command",
    )

    print("Base v9.4 consumers synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
