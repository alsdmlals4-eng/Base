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
