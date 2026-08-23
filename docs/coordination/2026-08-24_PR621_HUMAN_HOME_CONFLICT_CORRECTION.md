# PR #621 · Human Home Compatibility Correction · 2026-08-24

## Purpose

이 문서는 PR #621의 Narrative/World `summary-first → detail` UX가 이미 `main`에 병합된 PR #620의 Human Home 계약을 침범하지 않도록 충돌을 닫는 **호환성·검증 기록**이다.

새 Human Home 정본을 만들지 않는다. Human Home 내용·분리·사용자 교정 계약의 owner는 계속 다음 두 곳이다.

- `docs/operations/HUMAN_HOME_SELF_CONTAINED_POLICY.md`
- `skills/building-project-visual-dashboards/SKILL.md`

`SUMMARY_FIRST_IS_PROGRESSIVE_DISCLOSURE_NOT_SECTION_REMOVAL`

## Conflict found

PR #621의 Notion pilot은 Project Home을 짧은 요약과 toggle 중심으로 재배치하면서, #620이 사람용 Home에 필수화한 사용자 교정 surface까지 `redundant`로 취급해 제거했다.

이 해석은 잘못이다.

Narrative Gallery / Center Peek / toggle은 **긴 서사 detail을 progressive disclosure로 내리는 규칙**이다. 다음 사람용 섹션을 제거할 권한을 만들지 않는다.

- `AI_INTERPRETATION_FOR_USER_CORRECTION`
- `HUMAN_EDIT_GUIDE_REQUIRED`

반대로 다음 운영 정보는 계속 Human Home 기본 화면에서 분리한다.

- `AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED`
- raw PR / SHA / CI / Prompt / Hash / path / routing / receipt

`HUMAN_HOME_PROGRESSIVE_DISCLOSURE`는 정보량 축소가 아니라 **30초 전체 그림 → 5분 핵심 이해 → drilldown 상세**의 계층화다.

## Correct merged interpretation

```text
rich Human Project Home
→ project summary / core promise
→ Flow / core systems / project-specific core data / approved visual anchors
→ AI_INTERPRETATION_FOR_USER_CORRECTION
→ HUMAN_EDIT_GUIDE_REQUIRED
→ summary-first toggle / Gallery / Center Peek for long detail
→ specialist pages / evidence drilldown

AI/System operational metadata
→ System Masters / Registry / Handoff / repository evidence
```

Narrative Knowledge Model은 `Entity → Event → Relation → Rule → Evidence`와 narrative summary/detail 구조를 소유한다. Human Home 전체 정보구조와 사용자 교정 surface는 소유하지 않는다.

## Notion correction applied

현재 10개 Human Project Home 모두 프로젝트별 내용으로 다음 두 surface를 복구했다.

- `AI가 이해한 핵심`
- `내가 수정하는 방법`

복구 시 기존 Flow, 핵심 시스템·데이터, Visual 상태, 하위 페이지와 summary-first toggle은 유지했다. raw PR/SHA/CI/Prompt/Hash/path는 Home으로 되돌리지 않았다.

복구 대상:

- COC-Fiction
- 오멘워드
- 십보강호
- Tetris
- 괴이기록국
- 블랙스미스
- GRIMOIRE
- Switchy Express
- 닌자 서바이벌
- 마이 리틀 보트

Notion workspace search/readback에서 10개 Home의 `내가 수정하는 방법`이 모두 확인됐다. `AI가 이해한 핵심`도 각 Home에 프로젝트별 설계 의도 projection으로 복구했다.

## Three alternatives rechecked

### A · summary-first를 이유로 AI 이해/수정 가이드 제거

- 장점: Home 길이가 짧아진다.
- 문제: 사용자가 AI의 프로젝트 이해를 직접 검토·교정할 수 없고 #620 계약을 회귀시킨다.
- 결정: **REJECT**.

### B · AI/System 원시 metadata까지 Home으로 복원

- 장점: 모든 증거가 한 화면에 보인다.
- 문제: 사람용 Home이 다시 context dump가 되고 책임 분리가 깨진다.
- 결정: **REJECT**.

### C · rich Home + progressive disclosure + user-correctable AI interpretation/edit guide + separate System metadata

- 장점: 프로젝트 전체 이해, 사용자 교정 가능성, 장문 detail 가독성, 운영 metadata 분리를 동시에 유지한다.
- 결정: **ADOPT**.

## Regression rule

다음은 Human Home regression이다.

```text
summary-first rewrite
AND (
  AI_INTERPRETATION_FOR_USER_CORRECTION removed
  OR HUMAN_EDIT_GUIDE_REQUIRED removed
  OR AI_SYSTEM_OPERATIONAL_METADATA_EXCLUDED violated
)
→ MUST_FIX_BEFORE_MERGE_OR_COMPLETION
```

Narrative-specific 화면은 필요한 경우 Gallery/Center Peek/toggle을 적극 사용하되, Home 자체의 사람용 교정 surface를 drilldown-only 정보로 밀어내지 않는다.

## Image boundary

`내가 수정하는 방법`의 이미지 경로는 PR #620의 활성 image conversation gate를 그대로 따른다.

```text
current project / visual canon review
→ text Brief
→ assistant response STOP
→ next user explicit approval
→ exactly one image/edit
→ STOP
```

Narrative `Text Approval=APPROVED`는 Visual Gate 진입 자격일 뿐, 같은 assistant 응답에서 이미지 생성을 자동 승인하지 않는다.

## Implementation Reality Gate

Verified:

- #620 Human Home owner files exist on current `main`.
- #621 Narrative Method remains a separate narrative/world knowledge owner.
- all ten Human Homes were restored with project-specific AI-understanding + edit-guide surfaces and read back by workspace search.
- raw operational metadata remains separated from Human Home.
- no project gameplay/runtime files were changed by this correction.
- no image was generated.

Not claimed:

- Home wording has been comprehension-tested with a new user: `NOT_RUN`.
- exact desktop/mobile Notion geometry: `UI_GEOMETRY_NOT_VERIFIED`.
- COC Part 1 narrative migration: `NOT_RUN / STILL_APPROVAL_GATED`.
- new visual quality/runtime integration: `NOT_RUN / N/A`.

## TDD evidence

The regression test was committed before this file. The temporary focused PR runner then failed because this compatibility contract did not yet exist. This file is the minimal production-side change intended to turn that focused test GREEN.

## Rollback

- repository: revert this compatibility record and its regression assertion only if a later approved Human Home owner supersedes #620 explicitly.
- Notion: restore the prior Home version only if a later explicit user decision removes or replaces the two human correction surfaces.

Until such an explicit superseding decision exists, summary-first narrative work must remain compatible with the #620 Human Home contract.
