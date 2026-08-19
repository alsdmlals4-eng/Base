# P04 · Game Design, Core, Player Research & Vertical Slice — Learning Log

> 이 로그는 해당 Part 작업에서 실제로 확인된 교훈만 축적한다. 추정·외부 snippet·미검증 Source는 학습 사실로 승격하지 않는다.

## 작업별 Learning Checkpoint

각 완료 작업마다 아래 형식으로 하나의 checkpoint를 추가한다. 새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`로 명시하고 억지 교훈을 만들지 않는다.

```yaml
date:
work_ref:
baseline_and_result:
what_worked: []
what_failed_or_was_rejected: []
reusable_lesson:
anti_pattern: []
affected_rules_skills_modules: []
evidence: []
reuse_scope: PART_ONLY | BASE_PROMOTION_CANDIDATE | PROJECT_ONLY | NO_NEW_REUSABLE_LESSON
promotion_candidate:
source_followup_questions: []
revisit_condition:
```

### 2026-08-19 · P04 player-value-to-evidence contract

```yaml
date: 2026-08-19
work_ref: "PR #539"
baseline_and_result: "df8ef644d30fc96456da23a5157e5efb61b620bb -> P04 keeps five existing Skills while making player value, research questions, evidence ceilings, and Vertical Slice acceptance explicitly traceable."
what_worked:
  - "The existing GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE already separated technical/UI/usability/player-experience evidence, so the missing trace could be added without a new Skill."
  - "identifying-project-core and establishing-project-core already had distinct existing-project vs new/redefined-core authority, so preserving both reduced lifecycle ambiguity."
  - "Question-first Games User Research fit the existing evidence-aware design instead of requiring a separate research framework."
what_failed_or_was_rejected:
  - "Treating all eleven research domains as a 11/11 completion checklist."
  - "Merging core identification and establishment despite different authority and lifecycle responsibilities."
  - "Creating another player-research or Vertical Slice Skill when existing owners were sufficient."
  - "Treating retired Google Sheets as a default active tutorial audit surface."
reusable_lesson: "P04 decisions are easier to verify when player_promise -> meaningful_choice -> expected_experience -> research_question -> observable_signal -> evidence_ceiling -> slice_acceptance stays one trace across concept research and Vertical Slice gates."
anti_pattern:
  - "Feature/UI completion used as a proxy for player value."
  - "Research method or coverage checklist selected before the development decision and research question."
  - "Automation or static evidence promoted above its human-experience evidence ceiling."
affected_rules_skills_modules:
  - "GAME_DESIGN_AND_PLAYER_EXPERIENCE_GUIDE"
  - "analyzing-and-refining-game-concepts"
  - "governing-game-user-research-coverage"
  - "designing-vertical-slices"
  - "Concept Refinement / Player Research Coverage / Vertical Slice modules"
evidence:
  - "Base main baseline df8ef644d30fc96456da23a5157e5efb61b620bb and P04 Context Pack/Manifest"
  - "MDA: A Formal Approach to Game Design and Game Research"
  - "Games User Research: Choose the right playtest method"
  - "GDC Vault: The Vertical Slice Challenge"
  - "P04 player-value evidence contract in tests/test_game_design_difficulty_workflow.py"
reuse_scope: PART_ONLY
promotion_candidate: "None; the reusable rule is now represented directly in the P04 canonical guide/Skills and does not need a new global control-plane rule."
source_followup_questions:
  - "When simulation-heavy projects cannot produce a representative polished slice early, which alternative representative-system proof should P04 standardize without weakening evidence ceilings?"
revisit_condition: "Revisit if P04 gains a new research execution Skill, if eleven-domain coverage becomes mandatory routing, or if a project type repeatedly cannot use a representative Vertical Slice without misleading production readiness."
```

### 2026-08-19 · PR #539 copied continuation and consumer closure

```yaml
date: 2026-08-19
work_ref: "PR #543; source PR #539 kept read-only"
baseline_and_result: "User explicitly authorized copying #539 into an independent P04 workstream. The copied contract was replayed on completed main and extended until the actual planning consumers carried the same player-value, alternative, world/story fit, evidence-ceiling, and current-workspace semantics."
what_worked:
  - "Consumer-first regression tests exposed gaps that Skill text alone did not catch: Vertical Slice trace fields, world/story/player-fantasy fit, three real alternatives and long-term fit, and retired workspace authority in active templates."
  - "The focused P04 test module was bridged into the repository's already-required game-design test so RED/GREEN evidence came from a Required Check rather than an unconsumed test file."
  - "Keeping `usage_context` while changing its values to current Notion/repository meanings preserved the P05 UX contract without restoring Figma authority."
  - "Separating technical/UI evidence from human usability/player-experience evidence prevented repository CI from being mislabeled as player-experience PASS."
what_failed_or_was_rejected:
  - "A first attempt to retire `PROJECT_PLANNING_SEQUENCE_AND_SHEET_TABS.md` inside P04 failed Game Project OS freshness because the current coupled-change rule requires companion tests owned by other Parts. The P04 change was reverted instead of bypassing ownership."
  - "Removing the generic UX `usage_context` field together with Figma caused P05's UX contract test to fail; the field was restored with `NOTION_PROJECT / REPOSITORY_HANDOFF / BOTH`."
  - "Treating a newly added test file as sufficient before confirming that Required CI actually executes it."
reusable_lesson: "A P04 rule is not closed until at least one real authoring/decision consumer can carry it and a required regression gate exercises that consumer; retired tool names should be removed without deleting still-valid semantic metadata."
anti_pattern:
  - "Skill-only policy with stale downstream templates."
  - "Deleting semantic metadata just because its old values referenced a retired tool."
  - "Cross-Part companion tests edited from the wrong Part merely to make freshness pass."
affected_rules_skills_modules:
  - "P04_PLAYER_VALUE_TO_EVIDENCE_TRACE"
  - "WORLD_STORYLINE_FIT_REQUIRED"
  - "CURRENT_STATE_BENCHMARK_ALTERNATIVE_TRADE_STUDY"
  - "MINIMUM_VIABLE_ALTERNATIVES: 3"
  - "BETTER_ALTERNATIVE_SEARCH"
  - "LONG_TERM_PLAN_FIT_REQUIRED"
  - "Concept Refinement / Feature-Balance / Player Research / Vertical Slice consumers"
evidence:
  - "Required Check RED then GREEN for tests/test_p04_vertical_slice_player_value_trace.py through tests/test_game_design_difficulty_workflow.py"
  - "Validate Evidence-Based Game Development Knowledge"
  - "Validate Game UX UI System"
  - "Validate Base Partition Contract / Skill Routing Precision / Base v9 Operating Contracts"
  - "External source recheck: MDA and Games User Research question-first playtest guidance"
reuse_scope: PART_ONLY
promotion_candidate: "No new global rule. Cross-Part retirement coupling is an Integration/P02 freshness request rather than a P04 promotion."
source_followup_questions:
  - "Should Integration/P02 revise the legacy-Sheet coupled-change topology so P04-owned migration-only planning surfaces can be retired without requiring another Part to falsify ownership?"
revisit_condition: "Revisit if planning consumer ownership moves out of P04, if Notion/repository authority changes, or if Required CI stops consuming the P04 focused regression through the game-design test bridge."
```

## Source Learning

- Source domains: GAME_DEVELOPMENT
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
