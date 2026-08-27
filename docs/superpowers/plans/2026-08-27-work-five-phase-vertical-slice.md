# Work Five-Phase Vertical Slice Implementation Plan

**Source:** `[수정제안서]/BCP-2026-040-work-five-phase-vertical-slice/PROPOSAL.md`

**Goal:** 승인된 5단계 Work interface를 하나의 thin macro owner로 구현하고, 기존 Project canon과 minimum-transition 상세 owner를 보존한다.

## Constraints

- Project 고유 state/Decision/Task/Gate rename 금지.
- Base 세부 owner를 새 계약에 복제하지 않는다.
- 핵심 제품 의미는 routine standing approval로 자동 확정하지 않는다.
- Phase 2 통과 전 serial production asset 또는 Codex product implementation 시작 금지.
- Phase 4 automated readiness와 Phase 5 user-validated state를 분리한다.
- 현재 open PR changed path takeover 금지.
- Notion/Project 대량 migration 금지.

## Tasks

- [x] Current Base/Project/Notion/actual evidence audit and BCP-2026-040 approval reconciliation.
- [x] Latest main에서 새 workstream 생성.
- [x] Focused RED contract 작성 및 draft PR 생성.
- [ ] RED workflow evidence 확인.
- [ ] `WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md` 구현.
- [ ] Current Router에서 새 owner를 우선 route.
- [ ] Local Visual starter에서 새 owner를 route.
- [ ] Minimum-transition profile의 Stage A/B/C를 macro phase가 아닌 내부 transfer grouping으로 교정.
- [ ] Project-canon mapping case 작성; project native state는 rename하지 않음.
- [ ] Existing/new regression contract GREEN.
- [ ] Open PR path overlap 재검증.
- [ ] 5회 이상 full-scope adversarial review.
- [ ] Exact-head required CI 확인.
- [ ] Safe squash merge + post-merge main/file/readback.
- [ ] Superseded PR #742 closeout.

## Five-phase target

```text
PHASE_1_PLANNING_CO_DESIGN
→ PHASE_2_PREPRODUCTION_REVIEW
→ PHASE_3_WORK_INGAME_ELEMENT_PRODUCTION
→ PHASE_4_CODEX_IMPLEMENTATION_AND_MACHINE_CLOSEOUT
→ PHASE_5_USER_VERTICAL_SLICE_VALIDATION
```

Phase 4 exit is `AUTOMATED_VERTICAL_SLICE_READY / READY_FOR_USER_VERTICAL_SLICE_VALIDATION` with Human/Player evidence still `NOT_RUN`. Phase 5 actual user play produces `USER_VALIDATED_VERTICAL_SLICE` or an explicit rework/blocking outcome.
