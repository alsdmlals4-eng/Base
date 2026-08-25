# Canonical Reference Freshness Learning Log

## 2026-08-17 — Universal Loop v1 closure evidence hardening

- **상태:** `PATTERN`
- **Trigger:** Universal Loop v1 REAL A2 closure #494에서 machine checkpoint와 실제 terminal receipt를 기준으로 완료를 정본화하는 과정에서 handoff 요약 불일치, 테스트 미소비 false-GREEN 위험, predecessor ceiling freeze, stale-head Actions run, zero-escape 범위 과승격 위험을 함께 확인했다.
- **MACHINE_EVIDENCE_CORRECTION:** chat/handoff/worker summary와 exact repository 또는 terminal receipt가 충돌하면 summary를 counterevidence로 처리하고 실제 issue/run/SHA/receipt digest에 맞춰 파생 기록을 교정한다.
- **TEST_CONSUMPTION_PROOF:** workflow trigger나 `tests/**` path match는 테스트 실행 증거가 아니다. 실제 unittest/discovery command가 신규 회귀를 소비했는지 확인하고 가능하면 의도한 RED를 먼저 증명한다.
- **VERIFIED_SUCCESSOR_STATE:** exact successor evidence가 current state를 전진시켰다면 `CURRENT_MUTABLE` consumer와 predecessor regression assertion을 재검사한다. `HISTORICAL_DISCOVERY`의 당시 PR/SHA/run 값은 그대로 보존한다.
- **LATEST_EXACT_HEAD_ONLY:** stale-head, cancelled, superseded, zero-step, queued 또는 still-running run은 current exact HEAD의 required gate PASS를 대신할 수 없다.
- **BOUNDED_ZERO_ESCAPE:** omission/drift/unauthorized-addition 0건은 측정한 exact package·authority·evidence window에만 적용하며 게임 전체 품질 주장으로 일반화하지 않는다.
- **실제 사례:** #489 `BS_A2_DIAG_20260817_005`는 non-counting diagnostic PASS였고, #490/#491/#492의 `BS_A2_BURNIN_001_R1/R2/R3`만 counted REAL burn-in 3회로 사용했다. #494가 그 exact receipt identities/digests를 machine checkpoint에 정본화했다.
- **TDD 재검증:** 후속 #497/#498 RED에서 새 회귀가 Base-v9의 실제 unittest command에 명시적으로 소비됐고, 기존 문서가 아직 네 successor-learning 계약을 갖지 않아 정확히 4개 신규 assertion이 실패했다.
- **Boundary:** 새 광역 Skill을 만들지 않는다. paid OpenAI API/API-key fallback, A3 auto-merge, Scheduler, 자동 product scope를 열지 않는다. 과거 evidence를 현재 값으로 rewrite하지 않는다.
- **왜 글로벌 로그에 복제하지 않았는가:** 글로벌 `skills/SKILL_LEARNING_LOG.md`에는 이미 테스트 파일 미소비/false-GREEN과 정본 전파 누락의 유사 교훈이 존재한다. 이번에는 existing coupled-change contract가 허용하는 owner-local Learning Log에 exact #489~#494 provenance를 보존하고, 공용 동작은 Claim/Freshness 계약으로 승격한다.
- **Next trigger:** 다른 lifecycle에서 machine summary 충돌, false-GREEN, `PREDECESSOR_CEILING_FREEZE`, stale-head gate 재사용, 또는 bounded zero-escape의 범위 과승격이 재발할 때 재검토한다.

## 2026-08-25 — Blacksmith successor-state consumer recurrence

- **상태:** `VERIFIED_RECURRENCE / PROMOTE_EXISTING_OWNER_EVIDENCE`
- **Source project:** `alsdmlals4-eng/Blacksmith`, planning PR #207.
- **Trigger:** 사용자 승인 successor Decisions25~27/Art03가 current planning authority를 전진시킨 뒤 세 개의 서로 다른 current consumer/regression이 predecessor 값을 계속 요구해 정상적인 successor state를 실패 처리했다.
- **Recurrence 1 — Visual scrub:** `Validate Visual GDD Canon Scrub`이 과거 schema v1, CURRENT/MAX structure owner, `CURRENT=MAX` repair semantics를 current binding에 요구했다. 수정은 과거 scrub assertion을 역사로 보존하고 current binding assertion만 successor owner로 전진시켰다.
- **Recurrence 2 — Living GDD art:** `Blacksmith Living GDD Home contract`가 `BS-ART-20260825-02 / REWORK_REQUIRED`를 current `AGENTS.md`에 요구했다. `BS-ART-20260825-03 / ILLUSTRATED_WORKSHOP_BOOK / USER_APPROVED_DIRECTION`이 current가 된 뒤에도 predecessor ceiling이 남아 있었다. 역사 Decision03 snapshot check는 유지하고 current AGENTS assertion만 전진시켰다.
- **Recurrence 3 — current router:** `test_current_active_context_priority_overlay`가 구형 `BLOCKED_UNTIL_NEW_PLANNING_COMPLETE_DECLARATION`과 2026-08-20 Active Context snapshot을 current routing ceiling으로 고정했다. current resume owner를 `AGENTS.md + BS-OPS-20260825-08 handoff + successor canon`으로 분리하고 기존 Active Context snapshot은 `LEGACY_COMPATIBILITY_ROUTER / HISTORICAL`로 보존했다.
- **Reinforced rule:** successor가 current로 VERIFIED되면 모든 consumer/assertion을 `CURRENT_MUTABLE | HISTORICAL_DISCOVERY`로 분류한다. 전자는 successor로 전진시키고 후자는 당시 값을 보존한다. current test를 통과시키려고 predecessor token을 current 문서에 재주입하는 compatibility fix를 금지한다.
- **Execution proof rule:** 수정 후 실제 consumer workflow를 실행해 GREEN을 확인해야 한다. 새 standalone test 파일의 존재만으로 current propagation 완료를 주장하지 않는다.
- **Owner decision:** 이미 `auditing-canonical-reference-freshness`가 `VERIFIED_SUCCESSOR_STATE / PREDECESSOR_CEILING_FREEZE`를 소유한다. **새 Skill/새 광역 policy를 만들지 않는다.** 이번 Blacksmith evidence는 기존 rule의 재발 증거와 future eval fixture 후보로 승격한다.
- **Evidence packet:** `docs/evidence/2026-08-25-blacksmith-canon-visual-handoff-learning.md`.
- **Boundary:** Blacksmith의 +10 정밀강화, 4단계 damage 명칭/확률, repair, customer event, art style 등 프로젝트 제품 규칙은 Base로 승격하지 않는다.
- **Next trigger:** 다른 프로젝트에서 successor decision 후 current regression이 predecessor token을 강제하거나, history/current assertion ownership이 다시 섞일 때 cross-project promotion/eval 강화를 재검토한다.
