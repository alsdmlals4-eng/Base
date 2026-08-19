# Visual Style Source Radar

> domain_id: `ART_DIRECTION_AND_VISUAL_STYLE`
> 역할: 새로운 그림체·UI 시각언어·픽셀/하이브리드 제작법·현업 사례를 지속 발견해 기존 Art owner로 보내는 bounded discovery reference
> owner_policy: `PERIODIC_SPECIALTY_SOURCE_RADAR.md`
> watchlist_owner: `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`
> evidence_owner: `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`
> consumer: `PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md`, `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`, `PIXEL_ART_STYLE_SYSTEM.md`
> scheduler_authority: `EXTERNAL_TO_BASE`
> independent_ledger: `false`

## 1. 목적과 경계

이 문서는 별도 crawler·scheduler·두 번째 Evidence 원장·두 번째 Art Bible이 아니다. 기존 `PERIODIC_SPECIALTY_SOURCE_RADAR.md`의 전문 discovery 계약을 **시각 스타일 분야에만 구체화**한다.

목표는 스타일 이름을 많이 모으는 것이 아니라 다음 질문에 답할 수 있는 새로운 근거를 찾는 것이다.

- AI 생성 티처럼 보이는 무작위성·과밀도를 줄일 제작 규칙이 있는가.
- 캐릭터·환경·UI·VFX를 여러 자산에서 일관되게 반복할 수 있는가.
- 실제 플레이 크기에서 가독성이 유지되는가.
- 스타일이 세계관뿐 아니라 핵심 시스템의 판단·행동·피드백을 지원하는가.
- 1인 개발자가 두 번째·열 번째 자산까지 감당할 생산 파이프라인인가.

이 Radar에서 외부 이미지를 발견했다는 사실만으로 Base 또는 프로젝트 자산으로 복사하지 않는다.

## 2. `ORIGINAL_SOURCE_BACKTRACE`

검색 결과·SNS·Pinterest·커뮤니티 repost·영상 요약은 discovery surface일 수 있다. 채택 판단 전에 가능한 한 다음 원출처로 되돌린다.

```text
discovery surface
→ ORIGINAL_SOURCE_BACKTRACE
→ developer / artist / studio / publisher / GDC / official technical post
→ publication date + context + rights/provenance note
→ extracted principle
```

우선순위:

1. 개발사·작가·스튜디오의 공식 제작 과정·Art Bible/기술 포스트.
2. GDC Vault, 공식 컨퍼런스 발표, 개발자가 직접 작성한 postmortem/deep dive.
3. 퍼블리셔·플랫폼의 공식 작품 페이지와 공식 screenshot/trailer — 관찰 사실에만 사용.
4. 전문 매체의 개발자 기고·인터뷰 — 발언자와 맥락을 보존.
5. 포트폴리오·ArtStation 등 — 발견용으로 사용하고 실제 작업자·프로젝트 원문으로 역추적.
6. Pinterest·검색 썸네일·repost — 원출처가 확인되지 않으면 채택 근거로 사용하지 않는다.

## 3. Source pool

### `FIRST_PARTY_ART_PROCESS`

- 개발사/스튜디오 공식 art process, animation pipeline, UI/UX production 글.
- 특정 게임의 스타일 표면보다 **왜 그런 제약·실루엣·팔레트·파이프라인을 선택했는지**를 추출한다.

초기 seed:

- Yacht Club Games — character sprite process, palette/detail limits, pixel-perfect presentation.
- Supergiant Games — UI/icon/art production과 gameplay clarity 관련 공식 자료.
- Subset Games — 정보 중심 전술 설계와 실제 화면의 telegraph 원리.
- Square Enix 공식 작품/개발 자료 — pixel + 3D/depth/light hybrid 관찰.

### `PROFESSIONAL_TALK_AND_POSTMORTEM`

- GDC Vault Art Direction/UI/VFX/production 발표.
- Game Developer 등에서 실제 개발자가 직접 작성한 production deep dive.
- 반복 제작 비용, outsourcing brief, pipeline, readability, iteration 실패 사례를 우선한다.
- GDC 2026 NetEase Games의 `'LifeAfter': AIGC Paradigm Change in Mobile Game Art Production`은 인간-AI 협업·value-oriented workflow·과학적 평가·asset management·performance까지 함께 평가한다는 원칙을 `ADAPT`한다. 발표가 제시한 기업 규모의 절감 수치나 자체 toolchain은 Base 기본값으로 승격하지 않는다.

### `VISUAL_DISCOVERY_FEED`

- ArtStation, itch.io, Steam, 공식 trailer/screenshot, festival/showcase.
- 후보 다양성 확보에는 사용하지만 성공 원인·제작 효율을 화면만 보고 추론해 확정하지 않는다.
- 실제 상용 작품을 발견하면 개발사/작가 원문을 다시 찾는다.

### `TECHNICAL_RENDERING_SOURCE`

- Godot/Aseprite/Blender 등 공식 문서와 실제 엔진/툴 제작 자료.
- pixel filtering, palette/indexed workflow, render-assisted animation, camera/scaling처럼 스타일을 실제 제품으로 반복 구현하는 조건을 확인한다.

## 4. Candidate packet

후보 수는 `UNCAPPED_CANDIDATE_INTAKE`다. 임의 상한으로 좋은 후보를 버리지 않지만, 아래 packet을 채우지 못한 항목은 Library 채택 후보가 아니다.

```yaml
candidate_id:
discovered_from:
ORIGINAL_SOURCE_BACKTRACE:
original_url:
creator_or_team:
project_or_talk:
published_or_verified_at:
visual_family_candidate:
observable_visual_principle:
production_principle:
readability_principle:
world_or_system_fit_example:
AI_GENERATED_LOOK_REDUCTION:
STYLE_CONSISTENCY_AND_READABILITY:
WORLD_CORE_SYSTEM_FIT:
AI_ASSISTED_PRODUCTION_VALUE_GATE:
  baseline_workflow:
  comparable_task_or_asset_class:
  retake_rate:
  style_consistency_acceptance:
  human_review_cost:
  runtime_or_export_impact:
rights_or_reference_boundary:
counterexample_or_failure_mode:
existing_base_overlap:
STYLE_FAMILY_MATCH:
NEW_FAMILY_CANDIDATE:
long_term_cost_signal:
validation_needed:
disposition: ADOPT | ADAPT | TEST | REFERENCE_ONLY | AVOID | IGNORE
recheck_trigger:
```

## 5. Family routing

```text
candidate
→ existing family can express the important grammar/cost/risk?
   ├─ yes → STYLE_FAMILY_MATCH
   └─ no  → NEW_FAMILY_CANDIDATE
```

`NEW_FAMILY_CANDIDATE`는 이름이 새롭다는 이유로 열지 않는다. 다음 중 하나 이상이 실제로 달라야 한다.

- production pipeline 또는 반복 자산 비용 구조.
- silhouette/edge/palette/material/light처럼 관찰 가능한 핵심 문법.
- gameplay readability 위험과 검증법.
- world/core-system에서 맡는 역할.
- 기존 family에 넣었을 때 중요한 금지 규칙이나 실패 조건이 사라짐.

새 family는 `PREFERRED_VISUAL_STYLE_REFERENCE_LIBRARY.md`에 바로 확정하지 않고 최소 3개 실질 대안·`BETTER_ALTERNATIVE_SEARCH`·`LONG_TERM_PLAN_FIT_REQUIRED`·적대적 재검토를 거친다.

## 6. 세 평가축

### `AI_GENERATED_LOOK_REDUCTION`

- 이유 없는 micro-detail, pseudo-text, 무작위 장식, 장면마다 다른 재질/광원/해부 shortcut을 줄일 수 있는가.
- visual rule을 이름 붙이고 반복할 수 있는가.
- 자산 #2와 #10에서 같은 rule을 재현할 수 있는가.

### `STYLE_CONSISTENCY_AND_READABILITY`

- 실제 플레이 크기·thumbnail·grayscale에서도 역할과 상태가 읽히는가.
- 캐릭터·배경·UI·VFX가 같은 visual grammar를 공유하면서 정보 위계는 분리되는가.
- mobile/PC/zoom/animation에서 유지되는가.

### `WORLD_CORE_SYSTEM_FIT`

- 세계관 mood만 강화하는가, 아니면 핵심 판단·선택·피드백도 강화하는가.
- 핵심 시스템 정보를 숨기는 장식 비용은 없는가.
- 시스템에 필요한 telegraph·state·interaction hierarchy와 함께 작동하는가.

### `AI_ASSISTED_PRODUCTION_VALUE_GATE`

AI-assisted visual workflow는 이미지가 생성되거나 첫 결과가 보기 좋다는 이유만으로 production improvement로 판정하지 않는다. 동일하거나 충분히 비슷한 asset class·과제를 기존 baseline workflow와 비교하고 다음 증거를 본다.

- `retake_rate`: 승인 가능한 자산 하나를 얻기 위해 재생성·재작업·재수정이 얼마나 발생했는가. 실제 표본이 없으면 `UNVERIFIED`다.
- `style_consistency_acceptance`: 같은 character/prop/UI family를 반복 제작했을 때 visual grammar·identity·readability 기준을 몇 개가 통과했는가. 첫 자산 한 장만으로 PASS하지 않는다.
- `human_review_cost`: prompt 조정, paint-over, 레이어 정리, provenance 확인, 검수·재검수에 실제 사람이 쓰는 시간/노력을 함께 기록한다.
- `runtime_or_export_impact`: asset size, memory/performance 후보, export/import 단계, 레이어·atlas·압축·포맷 재작업이 늘거나 줄었는지 확인한다.

수치는 실제 측정치가 있을 때만 기록한다. 표본이 없으면 `LOW/MEDIUM/HIGH` 같은 상대 신호도 근거와 함께 쓰고, 검증 전에는 `TEST` 또는 `BLOCKED_UNVERIFIED`로 둔다. 외부 기업 사례의 절감률을 1인 개발 프로젝트의 기대치로 그대로 전이하지 않는다.

## 7. 성공작 사용법

`최고의 작품을 찾는다`는 것은 한 작품을 최종 정답으로 복제한다는 뜻이 아니다.

```text
strong work
→ identify why it works in its own constraints
→ separate visual signature from reusable principle
→ find counterexample / production cost
→ compare against at least 2 other substantive approaches
→ ADOPT / ADAPT / REJECT the principle
```

예:

- Shovel Knight에서 제한 팔레트·실루엣·idle pose와 gameplay intent 연결은 `ADOPT/ADAPT`할 수 있지만 캐릭터 디자인은 복제하지 않는다.
- Dead Cells의 3D-assisted animation은 반복 frame 비용이 실제 병목일 때만 `ADAPT`한다.
- depth-lit pixel hybrid는 공간감이 핵심 가치일 때만 후보로 두며 특정 상용작의 branded visual signature는 모사하지 않는다.

## 8. 지속 갱신 절차

```text
source scan / user reference / project lesson
→ candidate packet
→ ORIGINAL_SOURCE_BACKTRACE
→ evidence + rights + freshness
→ STYLE_FAMILY_MATCH | NEW_FAMILY_CANDIDATE
→ 3 evaluation axes + AI_ASSISTED_PRODUCTION_VALUE_GATE when applicable
→ benchmark + counterexample
→ disposition
→ if reusable Base delta exists: normal Base PR
→ exact-head validation
→ project use remains separate approval
```

이 절차는 후보 수를 채우기 위한 정기 PR을 만들지 않는다. `NO_MATERIAL_FOLLOWUP`이면 새 파일 변경을 만들지 않는다. 새 근거가 실제로 family 정의·금지 규칙·생산법·평가 기준을 개선할 때만 Base delta를 유지한다.

## 9. 재검토 조건

- 새로운 성공작/실패 사례가 기존 family의 장기 비용 가정을 뒤집음.
- 새 도구/엔진 기능으로 동일 품질의 반복 제작비가 크게 낮아짐.
- AI-assisted workflow의 일관성 실패 패턴이 새로 관찰됨.
- `retake_rate`·`human_review_cost`·`runtime_or_export_impact`가 기존 제작법보다 악화됨.
- 모바일/PC/접근성 검증에서 기존 스타일의 정보 손실이 확인됨.
- 사용자 선호 Reference가 누적되어 기존 family로 설명할 수 없는 공통 문법이 반복됨.
- 외부 source가 삭제·변경되거나 provenance/rights 해석이 달라짐.

재검토 뒤에도 프로젝트 Art Bible은 자동 변경하지 않는다.
