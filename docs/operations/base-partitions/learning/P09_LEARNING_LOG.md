# P09 · Content, Narrative & Publication — Learning Log

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

## Source Learning

- Source domains: FICTION_AND_INTERACTIVE_NARRATIVE, YOUTUBE_AND_VIDEO_EDITING
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.

## 2026-08-19 — P09 independent optimization checkpoint

```yaml
date: 2026-08-19
work_ref: P09_OPTIMIZATION_2026-08-19
baseline_and_result: >
  Baseline df8ef644d30fc96456da23a5157e5efb61b620bb. P09's two ACTIVE Skills and
  their core evidence boundaries remain fit for purpose; one CP0 Manifest ownership-path
  drift was isolated and handed off without creating duplicate canon. The latest merged
  YouTube Shorts metric-definition lesson was added to the YouTube Skill Learning Log.
what_worked:
  - Read actual Skill, Registry, tests, Context Pack, Notion page and same-goal merged work before proposing changes.
  - Existing-solution-first prevented a third narrative Skill and prevented a serial-fiction/YouTube umbrella merge.
  - Current first-party YouTube checks confirmed the existing sample/metric-definition boundaries instead of forcing a new KPI rule.
  - Cross-part ownership kept the CP0 Manifest out of the P09 branch.
what_failed_or_was_rejected:
  - Keeping the stale Manifest aliases unchanged.
  - Creating duplicate docs/knowledge/writing or templates/game-dev-youtube trees just to satisfy the Manifest spelling.
  - Renaming active canonical trees with broad consumer churn.
  - Compressing large Skill bodies solely because of file size without measured routing/context failure.
reusable_lesson: >
  When a maintenance Partition's declared write path disagrees with the path actually consumed
  by Skills/tests, repair ownership at the control plane; do not manufacture a second canonical
  tree inside the Part. File size alone is not proof that progressive-disclosure refactoring is beneficial.
anti_pattern:
  - MANIFEST_PATH_CREATED_AS_DUPLICATE_CANON
  - SIZE_ONLY_SKILL_COMPRESSION
  - CONTENT_SKILL_MERGE_BY_CATEGORY_NAME
  - PLATFORM_METRIC_LABEL_WITHOUT_DEFINITION_CONTEXT
affected_rules_skills_modules:
  - P09 ownership boundary
  - developing-and-revising-serial-fiction
  - producing-game-development-youtube-videos
  - Publication Evidence
  - Reusable Writing Lessons
evidence:
  - docs/operations/content-publication/P09_OPTIMIZATION_2026-08-19.md
  - skills/producing-game-development-youtube-videos/LEARNING_LOG.md
  - tests/test_serial_fiction_discipline.py
  - tests/test_game_development_youtube_skill.py
  - tests/test_youtube_metric_definition_context.py
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: >
  Integration should align P09 Manifest owned_write_paths to the already active canonical
  serial-fiction and game-development-youtube paths and remove dead aliases unless a real consumer exists.
source_followup_questions:
  - Has YouTube changed Shorts public-view/Engaged-view definitions or title/thumbnail experiment eligibility?
  - Do real project pilots expose narrative or publication evidence gaps that are not already owned?
  - Do measured context/routing failures justify progressive disclosure changes to either P09 Skill body?
revisit_condition: >
  Reopen when the CP0 path request is integrated, a real P09 edit needs one of the mismatched
  canonical paths, YouTube changes metric/experiment semantics, or repeated project evidence shows a missing owner.
```
