# Base Skill Implementation Evidence

> Generated from `skills/SKILL_REGISTRY.json`, behavior evaluation sets, and `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`. Do not edit this derivative.
> Active Skill count: `30`
> External model behavior run: `NOT_RUN`
> Behavior evaluation case count: `47`
> Behavior evaluation source SHA-256: `5d93325f9f39e5a1326843b656bcdacb4b5057ba68e13a9ee69b1ae11641d0c7`

`EXECUTABLE_EVIDENCE` means a repository test, tool, workflow, or package script is linked. It does not mean that evidence passed on the current commit. `CONTRACT_EVIDENCE` means only a contract or documentation consumer is linked. Actual model, runtime, device, and human validation remain separate.

| Skill | Owner | Primary behavior | Non-selection behavior | Evidence class | Repository evidence |
| --- | --- | --- | --- | --- | --- |
| `managing-project-intake-and-work-contract` | planning-project-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_neutral_adversarial_feature_lifecycle.py`<br>TEST: `tests/test_consolidated_skill_references.py`<br>TEST: `tests/test_feature_spec_traceability_contract.py`<br>TEST: `tests/test_skill_system_coverage.py` |
| `managing-game-project-operating-system` | project-operations-integrated-review | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_game_project_operating_system_structure.py` |
| `evolving-project-discipline-skills` | project-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py`<br>TEST: `tests/test_skill_behavior_evidence_hardening.py` |
| `managing-design-documents` | planning-documentation-publication | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_consolidated_skill_references.py`<br>TEST: `tests/test_feature_spec_traceability_contract.py` |
| `maintaining-project-context-and-handoff` | project-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_gpt_codex_workflow_contract.py` |
| `analyzing-and-refining-game-concepts` | game-design-strategy | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_game_design_difficulty_workflow.py` |
| `designing-vertical-slices` | game-design-production | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_vertical_slice_v9_contract.py` |
| `producing-game-development-youtube-videos` | game-marketing-content-production | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_game_development_youtube_skill.py`<br>CONTRACT: `skills/producing-game-development-youtube-videos/SKILL.md`<br>CONTRACT: `templates/game-development-youtube/EPISODE_PACKET.md` |
| `orchestrating-deepseek-worktrees` | external-ai-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TOOL: `tools/check_external_ai_worktree_contract.py`<br>TEST: `tests/test_external_ai_worktree_contract.py` |
| `reviewing-and-validating-project-changes` | integrated-review | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_consolidated_skill_references.py`<br>TEST: `tests/test_feature_spec_traceability_contract.py`<br>TEST: `tests/test_claim_and_intent_verification_contract.py` |
| `auditing-canonical-reference-freshness` | integrated-review-knowledge-governance | PASS | PASS | EXECUTABLE_EVIDENCE | TOOL: `tools/check_canonical_reference_freshness.py`<br>TEST: `tests/test_reference_freshness.py` |
| `designing-art-prompts-and-technique-cards` | art-ui | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_bca_visual_sheet_workflow.py` |
| `auditing-and-refining-ui-art` | art-ui | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_game_ux_ui_system.py`<br>TEST: `tests/test_project_design_md_adapter.py`<br>TEST: `tests/test_external_ui_procurement_gate.py`<br>TEST: `tests/test_bcp008_behavior_and_procurement_pilot.py` |
| `managing-base-change-proposals` | knowledge-management | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_consolidated_skill_references.py` |
| `identifying-project-core` | project-core-governance | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `establishing-project-core` | game-design-strategy | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `running-adversarial-review-and-refinement` | integrated-review | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_neutral_adversarial_feature_lifecycle.py`<br>TEST: `tests/test_cross_discipline_review_lenses.py` |
| `refactoring-with-contract-preservation` | structure-maintenance | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `simplifying-skill-bodies` | skill-context-optimization | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `pruning-stale-and-nonfunctional-material` | repository-pruning | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `synchronizing-local-and-github-state` | git-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py`<br>TEST: `tests/test_github_connector_fallback_policy.py` |
| `maintaining-long-running-task-continuity` | execution-continuity | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `governing-game-user-research-coverage` | games-user-research-governance | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `creating-user-learning-notes` | user-learning | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `building-project-visual-dashboards` | project-visualization | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `diagnosing-game-engine-runtime-failures` | game-engine-debugging | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `governing-legacy-retention-and-archives` | knowledge-governance-and-archives | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py`<br>TOOL: `templates/project-operations/github/check_archive_governance.py` |
| `evaluating-godot-assets-and-plugins-before-creation` | godot-asset-and-plugin-evaluation | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_base_shared_skill_routes.py` |
| `optimizing-ai-model-and-prompt-costs` | ai-model-cost-operations | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_skill_system_coverage.py` |
| `developing-and-revising-serial-fiction` | serial-fiction-writing-and-revision | PASS | PASS | EXECUTABLE_EVIDENCE | TEST: `tests/test_serial_fiction_discipline.py`<br>CONTRACT: `skills/developing-and-revising-serial-fiction/SKILL.md`<br>CONTRACT: `docs/knowledge/serial-fiction/SERIAL_FICTION_WRITING_AND_REVISION_GUIDE.md` |
