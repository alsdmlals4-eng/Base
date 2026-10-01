# BCP-2026-033 — Scoped Generated Visual Approval & Semantic Drift Handoff

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/GRIMOIRE-`
- 출처 Decision: `GM-VISUAL-DIRECTION-20260825-01`, `GM-REPRESENTATIVE-SCREENS-20260825-01`
- 출처 교훈: `GR-LESSON-VISUAL-20260825-01`
- 기준 Base main: `4c49c8b79b52483713247ae22bd39f1bd60c733c`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- 구현 authority: `NONE`

## 문제

AI 생성 화면은 시각적으로 높은 품질을 보여도 mechanics, copy, character identity, numbers, fiction을 임의로 발명하거나 단순화할 수 있다. 사용자가 이미지 전체를 좋아한다고 말했을 때 이 embedded claim들을 모두 Canon으로 승격하면 이후 작업이 semantic drift를 반복한다.

GRIMOIRE에서는 대표 전투 화면의 분위기/구도는 승인됐지만 Stock/Circuit/Spell UI는 current canon과 어긋나 재작업 대상으로 분리됐고, 3D-like 이동 화면은 명시적으로 거절됐다. 대화 화면도 구도/스타일만 승인하고 생성된 이름·대사·의상·관계는 비정본으로 분리했다.

## 재사용 후보

`SCOPED_GENERATED_VISUAL_APPROVAL`:

생성 이미지를 최소 다음 claim surface로 분리 검수한다.

- STYLE
- COMPOSITION
- CHARACTER_PRESENTATION
- ENVIRONMENT
- UI_INFORMATION_ARCHITECTURE
- MECHANIC_SEMANTICS
- COPY_AND_NUMBERS
- FICTION_CANON
- RUNTIME_ASSET_STATUS

`USER_LIKES_IMAGE`는 위 전부의 승인으로 해석하지 않는다. 실제 사용자 발화와 current domain canon으로 승인 범위를 좁혀 기록한다.

`SEMANTIC_DRIFT_REVIEW_AFTER_GENERATION`:

mechanic-bearing 이미지 생성 뒤 current domain canon과 대조해 각 요소를 `KEEP / REWORK / NONCANON`으로 분류한다.

`NEGATIVE_VISUAL_KNOWLEDGE_PRESERVATION`:

거절·재작업 방향도 handoff에 저장해 다음 worker가 같은 실패를 재생성하지 않게 한다.

`VISUAL_HANDOFF_PRESERVES_USER_MODE`:

cross-chat handoff에는 현재 사용자가 visual/planning/implementation 중 무엇을 허용했는지 명시한다. 일반적인 `계속해`가 보류된 implementation authority로 확대되지 않게 한다.

## BCP-2026-032와의 경계

열린 PR #678의 BCP-2026-032는 reference set, bounded image batch, layered visual responsibility, Notion attachment content readback을 다룬다. 이 제안은 해당 PR을 수정·흡수하지 않는다.

겹치지 않는 고유 범위는 다음이다.

- image approval의 claim-surface 분리;
- style/composition approval과 mechanic/copy/fiction canon 승격 분리;
- generation 뒤 semantic drift audit;
- rejected/rework-required visual semantics의 negative-knowledge handoff;
- user work-mode boundary의 cross-chat 보존.

Notion attachment readback 자체는 BCP-032 owner에 남긴다.

## 적용 후보 흐름

```text
fresh domain canon
→ brief approval
→ bounded generation
→ semantic drift review
→ scoped approval
→ negative knowledge + durable reference handoff
```

## 프로젝트 전용으로 남길 것

- FIVE_POINT_STAR, Stock, Prepared Spell 등 GRIMOIRE mechanics.
- Logo 01, Navy/Gold/blue magic 등 GRIMOIRE art direction.
- 특정 Notion page IDs와 image hashes.
- 특정 이동 방식의 최종 UX.

## 위험과 반례

1. 검수 필드가 너무 많아질 위험 → mechanic-bearing/Canon-bearing 생성물에만 적용하고 단순 decorative image에는 축소한다.
2. 사용자 승인을 과도하게 좁게 해석할 위험 → 최신 사용자 발화가 명확히 전체 설정을 승인하면 그 범위를 존중한다.
3. BCP-032 중복 → attachment/batch/reference-set은 032에 남기고 이 제안은 semantic approval boundary만 소유한다.
4. 한 프로젝트 증거를 전역 hard rule로 과승격할 위험 → proposal/case 단계로 제출하고 active Skill/root rule 구현은 후속 Base review로 분리한다.

## 검증 근거

- GRIMOIRE current design authority + actual workflow code를 재검토해 generated spell screen drift를 확인했다.
- 사용자가 3D-like movement를 명시적으로 거절하고 2D 단순화 방향을 요구했다.
- 대표 전투/대화 화면은 scope를 분리해 Notion/GitHub에 기록했다.
- 프로젝트 교훈 `GR-LESSON-VISUAL-20260825-01`에 concrete failure와 recovery를 기록했다.

## 승인과 구현

사용자는 2026-08-25 현재 대화에서 `Base 승격, 문제-교훈 자료도 잘 올려줘`라고 명시했다. 이는 이 reusable lesson의 Base proposal 제출을 승인한다.

이 PR은 proposal lifecycle만 수행한다. Active Base Skill/Guide/root policy 구현은 별도 후속 review/approval 대상이다.

### 동시성

- PR #678 / BCP-2026-032는 READ_ONLY.
- PR #674, #660 등 기존 open workstream도 READ_ONLY.
- `PROPOSAL_REGISTRY.json`은 PR #678이 같은 path를 수정 중이므로 이번 branch에서 건드리지 않는다. BCP-032가 먼저 병합된 뒤 latest main에서 BCP-033 registry entry를 reconciliation하는 후속이 필요하다.
