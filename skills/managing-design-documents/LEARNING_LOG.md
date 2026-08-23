# Managing Design Documents — Learning Log

## 2026-08-24 — Rich Human Home downstream consumer drift

### Observation

`HUMAN_HOME_SELF_CONTAINED_POLICY`와 `building-project-visual-dashboards`는 이미 정보량이 충분한 Project Home, 프로젝트 고유 핵심 데이터, AI 해석 교정면, 사용자 수정 경로를 요구하고 있었다. 그러나 `managing-design-documents`의 Project Home 요약과 machine-readable workspace authority의 required-section 목록은 이전의 얇은 상태·링크 허브 정의에 머물러 있었다.

그 결과 상위 owner가 정상이어도 downstream consumer가 사람용 Home을 다시 축약하거나 핵심 교정면을 누락시킬 수 있는 재발 경로가 남았다.

### Decision

새 Skill이나 제2 Home schema를 만들지 않는다. 기존 owner에 downstream consumer를 다시 결속한다.

```text
HUMAN_HOME_SELF_CONTAINED_POLICY
→ PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json
→ managing-design-documents
→ focused regression + AI/System boundary regression
→ Notion human-facing projection
```

### Added contract

- `managing-design-documents`는 Project Home을 짧은 상태·빠른 링크 허브로 재축약하지 않고 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`을 명시적으로 따른다.
- Project Home consumer는 `PROJECT_SPECIFIC_CORE_DATA`, `AI_INTERPRETATION_FOR_USER_CORRECTION`, `HUMAN_EDIT_GUIDE_REQUIRED`를 보존한다.
- machine-readable `human_home_required_sections`도 같은 세 항목을 요구한다.
- AI/System operational metadata와 Human Home의 rich information은 서로 다른 문제다. 사람용 정보량을 줄이는 것으로 metadata 분리를 해결하지 않는다.
- 현재 SHA·열린 PR처럼 자주 변하는 operational truth는 사람이 읽는 서술에 current 값으로 중복 고정하지 않고 live read/system owner를 사용한다.

### Evidence and limits

- TDD RED: PR #629 test-only head에서 `test_design_document_skill_routes_project_home_to_rich_human_owner`가 실제 CI에서 실패하여 downstream drift를 재현했다.
- 이후 owner routing과 machine contract를 최소 수정했다.
- exact-head GREEN과 Notion destination readback은 이 변경 작업의 최종 검증 단계에서 별도로 확인한다.
- Notion 화면의 실제 픽셀 배치·크롭·모바일 가독성은 connector readback만으로 PASS를 주장하지 않는다.
- 프로젝트 runtime·Human play evidence는 이 문서 구조 교정의 증거 범위가 아니다.

## 2026-08-10 — BCP-011 game feature design spec hierarchy

### Observation

Base already separated concept/PoC ownership, canonical design-document ownership, and post-approval traceability, but a reusable gap remained between a feature surviving PoC and multiple disciplines being able to implement the same intended behavior.

### Decision

Absorb the gap into existing owners instead of adding a new ACTIVE Skill.

```text
analyzing-and-refining-game-concepts
→ benchmark / PoC / adversarial review
→ promote only surviving major L2 features

managing-design-documents
→ canonical GAME_FEATURE_DESIGN_SPEC authoring

FEATURE_SPEC_TRACEABILITY_PACKET
→ post-approval Task / implementation / verification linkage
```

### Added contract

- `templates/planning/GAME_FEATURE_DESIGN_SPEC.md` owns intended player-facing behavior, rules, states, feedback, edge cases, data/balance, dependencies, acceptance, telemetry/playtest plan, and cut-down/rollback.
- The feature spec does **not** own Task progress, implementation completion, PR state, or executed verification results.
- Specialized design contracts remain authoritative where they are more precise; the generic feature spec references/composes them.
- L0/L1 and pre-PoC ideas do not receive mandatory L2 detail.
- Google Sheets remains a summary/workspace and does not duplicate the detailed canonical source.

### Rejected alternatives

- New broad `game-feature-design` ACTIVE Skill.
- Monolithic MASTER_GDD.
- Mandatory detailed spec for every feature or idea.
- Expanding Traceability Packet into a second detailed canonical source.
- Copying the full detailed spec into Google Sheets.

### Evidence and limits

- Industry evidence was recorded in `BCP-2026-011` from GDC one-page/layered design documentation, Ubisoft production-stage separation, and contemporary GDD communication practice.
- TDD RED was observed on the exact implementation PR head before production changes: the CI-executed regression failed specifically because `GAME_FEATURE_DESIGN_SPEC.md` was missing.
- GREEN repository CI must be re-run on the exact final implementation head.
- Real-project pilot: `NOT_RUN`.
- Human usability/comprehension: `HUMAN_NOT_RUN`.
- Gameplay quality improvement caused by this template: `BLOCKED_UNVERIFIED` until applied to a real project and tested.
