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
baseline_and_result: "df8ef644d30fc96456da23a5157e5efb61b620bb → Godot semantic accessibility evidence + baseline-relative AI-assisted visual production value gate; open PR #530 paths left read-only in the final diff"
what_worked:
  - "TDD RED isolated the two missing contracts before implementation: semantic accessibility and AI-assisted production-value evidence."
  - "The existing auditing-and-refining-ui-art Skill already routes Godot details to its owned implementation reference, so the reference could be strengthened without widening the Skill or touching CP0 routing."
  - "Primary/professional sources were reduced to reusable principles instead of copying platform or enterprise-scale claims."
  - "A fresh recheck of #530 changed filenames caught a newly introduced path overlap before merge and forced the final diff back to independent P05-owned paths."
  - "Repository merge rules rejected reuse of an older successful merge-context after main advanced, forcing a fresh required-gate cycle instead of allowing stale integration evidence to be treated as current."
  - "A working peer Partition PR showed the missing integration step: the branch itself must absorb the latest completed main with an explicit two-parent sync commit before final required-gate evaluation."
what_failed_or_was_rejected:
  - "Broad HTML-dashboard/legacy visual routing cleanup was rejected in this PR because #530 already edits those paths and CP0 owns global routes."
  - "A new accessibility Skill or AI-art-production Skill was rejected because existing P05 responsibilities already own the behavior and a new Skill would add routing/context cost."
  - "Moving the visual-value regression into tests/test_pixel_art_style_system.py was reverted after the P05 scope audit found that path is not owned by the current Manifest patterns."
  - "A later attempt to bind the regression to tests/test_bca_visual_sheet_workflow.py was also reverted because a fresh #530 diff check showed that exact path is already modified by the open protected PR."
  - "The first squash-merge attempt after main advanced was rejected with Required status check 'ci-gate' is expected; reusing the previous green synthetic merge ref was rejected as insufficient evidence for the new base."
  - "A second merge attempt was also rejected even after the refreshed synthetic merge-ref had ci-gate PASS. Root-cause comparison with merged P07 #542 showed that synthetic merge-ref validation alone is not equivalent to strict current-main branch synchronization for this repository's merge rule."
reusable_lesson: "Visual accessibility PASS needs semantic/runtime evidence separate from visual or focus checks; AI-assisted art production value needs baseline-relative retake, repeated-style acceptance, human review cost, and runtime/export evidence rather than generation success alone. Concurrent-PR protection must be rechecked after every changed-path expansion. For this Base repository, when main advances during a Part PR, final integration must follow the proven strict-current-main pattern: explicitly merge only the latest completed main into the Part branch, then rerun required gates on that synchronized head; a green synthetic merge-ref alone may still leave the repository rule's required check in EXPECTED state."
anti_pattern:
  - "Inferring screen-reader usability from rendered UI or keyboard focus alone."
  - "Treating first-generation quality or a vendor/presenter savings headline as production-value proof."
  - "Assuming conceptual domain ownership implies Manifest write ownership for a similarly named test file."
  - "Reusing an earlier no-overlap result after the current PR's changed-path set has expanded."
  - "Treating a stale synthetic merge-ref PASS as current integration evidence after the base branch advances."
  - "Repeatedly rerunning the same synthetic merge-context without comparing against a known successfully merged Partition pattern."
affected_rules_skills_modules:
  - "auditing-and-refining-ui-art / UX/UI Audit"
  - "VISUAL_STYLE_SOURCE_RADAR / Art Direction"
  - "P05 scope and concurrent-PR ownership"
  - "required merge-context validation freshness"
  - "strict current-main Part branch synchronization"
evidence:
  - "RED exact-head 29ade30083f25d6169481c5b05c8e6f5aecd05c7: Validate Game UX UI System failed only the two newly added contracts."
  - "Exact head 7dbfdc598ca7425020de4d519827a00dbefeedc8 against its then-current merge context passed UX/UI, evidence knowledge, Skill routing, Base Partition, Base v9, publication and final ci-gate validation."
  - "After main advanced to 3be8a3fb763327ad59cdc99a9bb15263f487cf90, GitHub rejected the squash merge with HTTP 405 because required status check ci-gate was expected for the refreshed merge context; no stale PASS was promoted."
  - "Head be22b58f518d5500faad738b461d307711909c03 produced synthetic merge ref d369a36908b50b04081454fc428544b3f122bf4f over main a347d7ccf6436b131a61416695447b30dcaecd2d and all triggered checks including ci-gate passed, but direct merge still returned the same EXPECTED violation."
  - "Merged P07 #542 used final commit d2e587e0cc80ef866d03273d2a9b786ad8f026c9 ('sync latest completed main before merge') with two parents: its prior Part head and then-current main 3be8a3fb763327ad59cdc99a9bb15263f487cf90."
  - "P05 then created the equivalent two-parent branch sync commit 823551406e0c5182e4898bafc6cd8a064703235e using the already-validated synthetic merge tree and parents be22b58f518d5500faad738b461d307711909c03 + a347d7ccf6436b131a61416695447b30dcaecd2d."
  - "Temporary validation head bad7e5ddd0afa2ca96ffeb4a0db169332dd70db5 ran the integrated suite with 39 tests OK, but its test_bca path change was later reverted after #530 overlap discovery and is not part of final scope evidence."
  - "Godot stable documentation: screen-reader integration requires accessibility labels, logical reading flow, and target-platform testing."
  - "Xbox Accessibility Guidelines V3.2: game accessibility guidance for design/development/testing, not a legal-compliance checklist."
  - "GDC 2026 LifeAfter AIGC production session: value-oriented evaluation, human-AI workflow, asset management, and performance were adopted as evaluation principles; reported enterprise savings were not promoted as Base expectations."
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "semantic accessibility evidence boundary + baseline-relative AI-assisted production value gate + changed-path expansion requires renewed concurrent-PR overlap audit + Part finalization should reuse the proven strict current-main sync pattern rather than relying only on synthetic merge-ref freshness"
source_followup_questions:
  - "What actual target-platform screen-reader evidence appears when a Godot project implements these properties?"
  - "What retake/review/runtime baseline emerges after a repeated family of visual assets is produced in a solo project?"
revisit_condition: "Revisit when #530/Integration changes visual routing, Godot accessibility APIs change, required-gate topology changes, or project measurements show these evidence fields do not predict lower rework or better consistency."
```

### Adversarial review record

1. Full loop 1 — found an out-of-partition regression-test path; reverted it and restored the contract under a P05-owned UI test.
2. Full loop 2 — found a future workflow-trigger gap for `VISUAL_STYLE_SOURCE_RADAR.md`; recorded as a non-blocking CP0/Integration request instead of editing `.github/**`.
3. Full loop 3 — rechecked engine/accessibility freshness and overclaim risk; Godot 4.7.1 remains stable while 4.7.2 is pre-release, so no stable baseline change was justified.
4. Full loop 4 — found `BLOCKED_UNVERIFIED` used by the new production-value rule but absent from its candidate disposition enumeration; aligned the packet.
5. Full loop 5 — re-attacked P05 ownership, concurrent PR protection, accessibility/player value, AI-production evidence, legacy-authority risk, long-term fit, validation and rollback; no new in-scope MUST_FIX was found at that head.
6. Full loop 6 — after temporarily binding production-value regression to the Manifest-required visual test, found duplicate ownership of the same regression and removed the duplicate.
7. Full loop 7 — re-fetched open PR #530 changed paths after the test-owner change, found `tests/test_bca_visual_sheet_workflow.py` overlap, reverted that entire path to the protected version, restored the regression only under the non-overlapping P05-owned UX/UI test, and restarted exact-head validation.
8. Full loop 8 — after all checks passed, main advanced because completed P06/P07 work merged. A squash merge was correctly blocked until required integration evidence was refreshed; stale PASS was not promoted.
9. Full loop 9 — the refreshed synthetic merge-ref reached ci-gate PASS but merge remained blocked. Systematic comparison with successfully merged P07 #542 isolated the root cause: P07 had explicitly synchronized current completed main into its own branch with a two-parent commit. P05 applied the same minimal sync pattern using only completed main, without touching any open foreign PR, and restarted final validation on the synchronized branch.

`CLEAN_REVIEW_EXIT` applies to PR #538's P05-owned scope only after the synchronized-head required CI, scope/concurrency validation, Notion readback, unresolved-thread check, merge, and post-merge readback complete. It does not claim that #530/CP0 legacy-routing cleanup is complete.

## 2026-08-25 · Blacksmith layered Visual approval evidence

```yaml
date: 2026-08-25
work_ref: "Blacksmith Visual GDD / art-direction transition / Decisions25~27"
baseline_and_result: "Eight generated boards had been approved as explanatory Visual GDDs; later mechanic and art-direction decisions changed both gameplay semantics and rendering direction. The project preserved the boards as information references while explicitly invalidating stale system values and separating final asset/runtime approval."
what_worked:
  - "Keep an approved board usable for information hierarchy even when example numbers, mechanic semantics, or rendering language become stale."
  - "Make current gameplay values flow from current canon/resolver rather than OCR or image text."
  - "Separate user approval of art direction from final product asset/runtime/release evidence."
  - "Regenerate a small representative screen set after system sync instead of bulk-regenerating every asset."
what_failed_or_was_rejected:
  - "A single Approved=true meaning all of layout, gameplay values, art style, and product-asset readiness was rejected because those claims changed independently during the same project."
  - "The original black/gold generated look was accepted as explanatory GDD but later rejected as final style; keeping that style current merely because the image was approved would have frozen the wrong visual authority."
  - "CURRENT/MAX and old multi-precision values inside approved boards became stale after successor mechanic decisions; image approval could not preserve those gameplay values."
reusable_lesson: "Visual approval should be claim-scoped. At minimum distinguish INFORMATION_ARCHITECTURE/EXPLANATORY_GDD, GAMEPLAY_VALUE_AUTHORITY, ART_DIRECTION, and FINAL_PRODUCT_ASSET/RUNTIME evidence. A downstream consumer must know which layer it is allowed to reuse."
anti_pattern:
  - "one Approved flag treated as universal proof"
  - "image text used as gameplay authority after successor canon"
  - "art-direction approval inferred from explanatory-board approval"
  - "bulk asset regeneration before representative-screen review"
affected_rules_skills_modules:
  - "auditing-and-refining-ui-art"
  - "Visual GDD / Art Direction / Asset evidence"
  - "canonical reference freshness"
evidence:
  - "Blacksmith BS-ART-20260825-03 = ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION"
  - "Blacksmith eight Asset records remain INFORMATION_ARCHITECTURE_AND_EXPLANATORY_GDD references"
  - "Blacksmith Decisions25~27 supersede CURRENT/MAX/multi-precision/detailed dated-history semantics shown in earlier boards"
  - "Base evidence packet docs/evidence/2026-08-25-blacksmith-canon-visual-handoff-learning.md"
reuse_scope: BASE_PROMOTION_CANDIDATE
promotion_candidate: "Add claim-scoped Visual approval/evidence semantics to an existing P05 owner rather than creating a new Skill. Promote globally only after Integration/cross-project review."
source_followup_questions:
  - "Which existing Asset/Visual contract should own the four approval layers without adding a duplicate status system?"
  - "Can another project demonstrate the same need when a style changes but layout remains approved?"
revisit_condition: "Revisit on the next project where approved Visual GDD layout survives a mechanic/style successor decision, or during the next P05/Integration contract revision."
```

## Source Learning

- Source domains: GAME_DEVELOPMENT
- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.
- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.
- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.