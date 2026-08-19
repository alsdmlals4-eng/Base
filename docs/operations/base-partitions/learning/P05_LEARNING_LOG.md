# P05 · Art, UX/UI & Visual Assets — Learning Log

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

## 2026-08-19 · P05 independent optimization

```yaml
date: 2026-08-19
work_ref: "PR #538 · opt/base-part-P05-visual-evidence-accessibility"
baseline_and_result: "df8ef644d30fc96456da23a5157e5efb61b620bb → Godot semantic accessibility evidence + baseline-relative AI-assisted visual production value gate; open PR #530 paths left read-only"
what_worked:
  - "TDD RED isolated the two missing contracts before implementation: semantic accessibility and AI-assisted production-value evidence."
  - "The existing auditing-and-refining-ui-art Skill already routes Godot details to its owned implementation reference, so the reference could be strengthened without widening the Skill or touching CP0 routing."
  - "Primary/professional sources were reduced to reusable principles instead of copying platform or enterprise-scale claims."
  - "The AI production-value regression was ultimately bound to the Manifest-required P05 visual workflow test so the partition validation entrypoint exercises the new contract."
what_failed_or_was_rejected:
  - "Broad HTML-dashboard/legacy visual routing cleanup was rejected in this PR because #530 already edits those paths and CP0 owns global routes."
  - "A new accessibility Skill or AI-art-production Skill was rejected because existing P05 responsibilities already own the behavior and a new Skill would add routing/context cost."
  - "Moving the visual-value regression into tests/test_pixel_art_style_system.py was reverted after the P05 scope audit found that path is not owned by the current Manifest patterns."
  - "Temporarily keeping the same production-value regression in both the UX/UI test and the P05 visual workflow test was rejected as duplicate maintenance; the UX/UI test now keeps only semantic accessibility."
reusable_lesson: "Visual accessibility PASS needs semantic/runtime evidence separate from visual or focus checks; AI-assisted art production value needs baseline-relative retake, repeated-style acceptance, human review cost, and runtime/export evidence rather than generation success alone."
anti_pattern:
  - "Inferring screen-reader usability from rendered UI or keyboard focus alone."
  - "Treating first-generation quality or a vendor/presenter savings headline as production-value proof."
  - "Assuming conceptual domain ownership implies Manifest write ownership for a similarly named test file."
  - "Duplicating one contract across unrelated test owners merely to trigger CI."
affected_rules_skills_modules:
  - "auditing-and-refining-ui-art / UX/UI Audit"
  - "VISUAL_STYLE_SOURCE_RADAR / Art Direction"
  - "P05 scope ownership"
evidence:
  - "RED exact-head 29ade30083f25d6169481c5b05c8e6f5aecd05c7: Validate Game UX UI System failed only the two newly added contracts."
  - "GREEN exact-head bad7e5ddd0afa2ca96ffeb4a0db169332dd70db5: Manifest-required P05 visual workflow suite ran 39 tests with OK, including the production-value gate; UX/UI suite ran 55 unittest cases plus 9 pytest cases with PASS."
  - "Godot stable documentation: screen-reader integration requires accessibility labels, logical reading flow, and target-platform testing."
  - "Xbox Accessibility Guidelines V3.2: game accessibility guidance for design/development/testing, not a legal-compliance checklist."
  - "GDC 2026 LifeAfter AIGC production session: value-oriented evaluation, human-AI workflow, asset management, and performance were adopted as evaluation principles; reported enterprise savings were not promoted as Base expectations."
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "semantic accessibility evidence boundary + baseline-relative AI-assisted production value gate"
source_followup_questions:
  - "What actual target-platform screen-reader evidence appears when a Godot project implements these properties?"
  - "What retake/review/runtime baseline emerges after a repeated family of visual assets is produced in a solo project?"
revisit_condition: "Revisit when #530/Integration changes visual routing, Godot accessibility APIs change, or project measurements show these evidence fields do not predict lower rework or better consistency."
```

### Adversarial review record

1. Full loop 1 — found an out-of-partition regression-test path; reverted it and restored the contract under a P05-owned UI test.
2. Full loop 2 — found a future workflow-trigger gap for `VISUAL_STYLE_SOURCE_RADAR.md`; recorded as a non-blocking CP0/Integration request instead of editing `.github/**`.
3. Full loop 3 — rechecked engine/accessibility freshness and overclaim risk; Godot 4.7.1 remains stable while 4.7.2 is pre-release, so no stable baseline change was justified.
4. Full loop 4 — found `BLOCKED_UNVERIFIED` used by the new production-value rule but absent from its candidate disposition enumeration; aligned the packet.
5. Full loop 5 — re-attacked P05 ownership, concurrent PR protection, accessibility/player value, AI-production evidence, legacy-authority risk, long-term fit, validation and rollback; no new in-scope MUST_FIX was found at that head.
6. Full loop 6 — after binding the production-value regression to the Manifest-required P05 visual test, re-reviewed the full diff, found duplicate ownership of the same regression in the UX/UI test, removed the duplicate, and re-ran exact-head validation.

`CLEAN_REVIEW_EXIT` applies to PR #538's P05-owned scope only after the final exact-head CI, scope validation, Notion readback, unresolved-thread check, merge, and post-merge readback complete. It does not claim that #530/CP0 legacy-routing cleanup is complete.

## Source Learning

- Source domains: GAME_DEVELOPMENT
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.
