# P0 Reusable Module Implementation Pilot

- 상태: TDD 계약
- 승인: 사용자 2026-08-20 — P0 1~4순위 실제 구현 및 프로젝트 Pilot
- 목적: `MODULE_CONTRACT_DEFINED`에서 실제 재사용 가능한 reference implementation + project adapter evidence로 승격한다.

## 구현 대상

1. `RM-TOOL-001 DATA_SCHEMA_CROSSREF_VALIDATOR`
2. `RM-SYS-001 GRID_PLACEMENT_RULE_ENGINE`
3. `RM-SYS-003 CANDIDATE_DRAFT_WEIGHT_ENGINE`
4. `RM-VIS-001 SEMANTIC_UI_SKIN_KIT`
5. `RM-VIS-002 GAMEPLAY_SYMBOL_ATLAS`

## 구현 경계

```text
small neutral core
→ thin project adapter
→ project-owned data / rules / visual language
→ deterministic or runtime test
→ adoption decision
```

- Base 공용 코어는 project canon, save state, runtime singleton을 소유하지 않는다.
- Python validator는 stdlib-only, deterministic, read-only를 기본으로 한다.
- Godot reference modules는 `RefCounted` 기반 순수 helper로 시작하고 Autoload/global mutable state를 도입하지 않는다.
- Visual module은 semantic role/symbol contract만 공유하고 실제 product art는 프로젝트 owner가 유지한다.
- Tetris는 진행 중 PR 보호로 `DEFERRED_CONCURRENCY`다.
- Ninja Survival은 프로젝트 phase gate 때문에 `DEFERRED_PHASE_GATE`다.
- Base PR #556의 P09 퇴역 작업 경로는 read-only이며 이 Pilot은 Tool Hub/QA Evidence Studio에 의존하지 않는다.

## RED acceptance

영구 P04 Evidence workflow가 `tests/test_p04_reverse_engineering_reuse_pipeline.py`의 P0 구현 계약을 실제 실행하고, 구현 파일 부재 또는 동작 부재 때문에 실패해야 한다. test-only Green이면 false Green으로 판정하고 구현을 시작하지 않는다.

## 완료 증거 ceiling

- reference source 존재만으로 프로젝트 재사용 PASS를 주장하지 않는다.
- project adapter 테스트가 실제 해당 프로젝트 CI/Godot에서 실행돼야 `PROJECT_ADAPTER_VERIFIED`다.
- player fun/immersion은 별도 Vertical Slice/player evidence 없이는 `NOT_RUN`이다.
