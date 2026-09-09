"""Text-contract regression only; does not certify artistic or runtime quality."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'skills/designing-art-prompts-and-technique-cards'

class ActionStagingContract(unittest.TestCase):
    def test_sprite_requires_research_and_outcome_contract(self):
        text = (ART / 'references/sprite-pose-sequence-controls.md').read_text(encoding='utf-8')
        for marker in ('STAGING_RESEARCH_BEFORE_PRODUCTION', 'source_and_evidence',
                       'focal_point', 'outcome_branches', 'NO_VISUAL_RULE_INVENTION',
                       'EFFECT_OFF_REVIEW', 'ROLE_REVERSED_REVIEW'):
            with self.subTest(marker=marker): self.assertIn(marker, text)

    def test_effect_is_bound_to_event_not_fake_contact(self):
        text = (ART / 'references/effect-stage-compositing-controls.md').read_text(encoding='utf-8')
        for marker in ('STAGING_RESEARCH_BEFORE_PRODUCTION', 'resolved_event',
                       'NO_VFX_TO_HIDE_POSE_ERRORS', 'reduced_effect_review'):
            with self.subTest(marker=marker): self.assertIn(marker, text)

    def test_template_and_skill_consume_gate(self):
        template = (ROOT / 'templates/planning/ART_TECHNIQUE_CARD.md').read_text(encoding='utf-8')
        for marker in ('staging_research', 'outcome_branches', 'effect_off_review', 'runtime_evidence'):
            with self.subTest(marker=marker): self.assertIn(marker, template)
        self.assertIn('STAGING_RESEARCH_BEFORE_PRODUCTION', (ART/'SKILL.md').read_text(encoding='utf-8'))

if __name__ == '__main__': unittest.main()
