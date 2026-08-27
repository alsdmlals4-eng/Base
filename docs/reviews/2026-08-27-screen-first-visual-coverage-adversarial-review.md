# Screen-first Visual Coverage 교정 — 적대적 검토 기록

- 날짜: `2026-08-27`
- Base 변경 제안: `BCP-2026-045`
- 제안 PR: `#760`
- 구현 PR: `#761`
- 범위: project-neutral documentation contract, paste-ready Work instruction, focused regression
- evidence ceiling: 정적 Base 계약과 GitHub CI 검증. 개별 프로젝트의 이미지 품질, Notion 반영, Godot runtime, player UX PASS는 주장하지 않는다.

## 1. 문제 재현

기존 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`는 캐릭터, 환경, UI, VFX, 상태군, 기술 소비 조건과 `Main Menu / System Screens` 범주까지 폭넓게 포함한다.

그러나 audit 순서가 asset category 중심이어서 다음 실패가 가능했다.

```text
캐릭터 있음
배경 있음
아이콘 있음
UI component 있음
VFX 있음

하지만
메인 화면 전체 없음
전투 준비 화면 전체 없음
결과·보상 화면 전체 없음
pause/settings와 error/loading surface 없음
```

개별 자산 존재와 플레이 가능한 전체 화면 coverage가 같은 것으로 취급되는 구조적 누락이다.

## 2. 대안 비교

### A. 기존 자산 체크리스트의 `Main Menu / System Screens` 항목만 확장

장점:

- 변경량이 작다.
- 기존 owner 하나만 유지한다.

문제:

- audit 시작점이 계속 자산 category다.
- 화면별 player goal, entry/exit, overlay, transition, error state를 구조적으로 강제하지 못한다.
- 화면 전체 composition과 runtime component의 구분이 약하다.

판정: `REJECT`.

### B. 화면 인벤토리 companion contract + 기존 자산 catalog 교차 검사

장점:

- `화면 → component → state/variant → asset category` 순서를 명확히 고정한다.
- 기존 자산 체크리스트와 승인 state machine을 대체하지 않는다.
- 화면 자체의 visual design 필요성과 신규 bitmap 필요성을 분리할 수 있다.
- Work 채팅에서 바로 실행할 수 있는 correction instruction으로 연결할 수 있다.

위험:

- companion 문서가 두 번째 GDD·Asset Manifest가 될 수 있다.
- 모든 화면을 신규 고해상도 이미지로 만들라는 오해가 생길 수 있다.

완화:

- `COVERAGE_CHECK_ONLY`, `NOT_A_SECOND_ASSET_CANON`, 기존 owner link를 명시한다.
- `SCREEN_DESIGN_REFERENCE`, `RUNTIME_COMPONENT_ASSET`, `NO_NEW_IMAGE_FILE_REQUIRED`를 분리한다.

판정: `ADOPT`.

### C. 화면·자산·승인·runtime을 하나의 통합 master schema로 재설계

장점:

- 단일 표에서 모든 상태를 볼 수 있다.

문제:

- 기존 Notion, Asset Manifest, requirement, runtime evidence와 정본 경쟁이 발생한다.
- 모든 프로젝트에 migration 비용을 강제한다.
- 현재 문제보다 범위가 훨씬 크다.

판정: `REJECT`.

## 3. TDD 증거

### RED

- head: `bbcd57b86dbb5e540fcc6cfc3d9e48456bfd8c20`
- workflow run: `33075476173`
- `core-regression`: 실패
- 전체 결과: `failures=2`, 기존 관련 회귀는 유지
- 의도한 실패:
  1. `screen-first visual coverage owner must exist`
  2. `paste-ready Work instruction must exist`

syntax, dependency, proposal validation, canonical-reference 오류가 아니라 새 owner와 template이 실제로 없어서 실패했다.

### GREEN — 최소 구현 확인

- pre-review head: `8ea99ab37eba07c20555a30ee5ec0eda1d6d9d32`
- workflow run: `33076058316`
- `docs-validation`: PASS
- `ubuntu-contract`: PASS
- `core-regression`: PASS
- 별도 Evidence-Based Knowledge와 Base v9 workflow: PASS

최종 merge 전에는 이 review receipt까지 포함한 exact head에서 전체 required check를 다시 확인한다.

## 4. 전체 상태 적대적 검토 — Loop 1

관점: **owner와 중복 정본**

공격:

- 새 screen matrix가 기존 GDD, Flow, Asset Manifest, Notion Asset Library를 복제할 수 있다.
- 기존 coverage owner와 책임이 겹칠 수 있다.

검사:

- 새 owner 첫 부분에서 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`를 대체하지 않는다고 명시했다.
- screen row는 기존 project canon, requirement, asset record, scene, evidence에 link하도록 제한했다.
- Work instruction은 기존 owner가 있으면 그 owner를 교정하고 새 owner를 만들지 않도록 했다.

교정:

- `COVERAGE_CHECK_ONLY`, `NOT_A_SECOND_ASSET_CANON`을 상단 hard boundary로 고정했다.
- Notion은 사람용 정본, GitHub는 구조·runtime 정본이라는 domain split을 명시했다.

결과: blocking finding `0`.

## 5. 전체 상태 적대적 검토 — Loop 2

관점: **화면 누락과 실제 플레이 흐름**

공격:

- title과 gameplay만 있고 preparation, result, settings, error flow가 다시 빠질 수 있다.
- overlay나 popup이 독립 화면으로 취급되지 않을 수 있다.
- 모든 게임에 불필요한 화면을 강제할 수 있다.

검사:

- `PLAYER_VISIBLE_SCREEN_FAMILIES`에 boot/loading, main/title, save/load, select, hub/map, core gameplay, dialogue, preparation, battle, special overlay, result/reward, progression, archive/tutorial, pause/settings, failure/ending, transition/error를 포함했다.
- popup/overlay도 입력과 판단이 달라지면 별도 surface로 기록한다.
- 적용하지 않는 family는 삭제가 아니라 `NOT_APPLICABLE + reason`으로 처리한다.

교정:

- `MAIN_TITLE_MENU`, `RESULT_REWARD`, `PAUSE_SETTINGS`, `LOADING_TRANSITION_ERROR`를 regression token으로 고정했다.
- screen row에 `flow_entry`, `flow_exit`, `player_goal`, `player_question`을 필수화했다.

결과: blocking finding `0`.

## 6. 전체 상태 적대적 검토 — Loop 3

관점: **이미지 과잉 생산과 구현 비용**

공격:

- “화면도 필수 이미지”라는 교정이 모든 화면을 한 장의 고해상도 bitmap으로 만들라는 규칙으로 왜곡될 수 있다.
- text와 UI state가 이미지에 baked되어 localization과 유지보수 비용이 증가할 수 있다.

검사:

- 화면 전체의 composition evidence는 요구하지만 runtime file type은 별도로 판정한다.
- `SCREEN_DESIGN_REFERENCE`와 `RUNTIME_COMPONENT_ASSET`을 분리했다.
- Godot Control/Theme/StyleBox, text layer, SVG, shader, procedural draw를 공식 production mode로 포함했다.

교정:

- `NO_NEW_IMAGE_FILE_REQUIRED`를 추가해 “시각 표현 필수”와 “신규 bitmap 필수”를 분리했다.
- 전체 목업을 runtime UI 한 장으로 쓰지 않고 layer/component로 분해하도록 했다.
- `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS`를 owner와 Work instruction 양쪽에 유지했다.

결과: blocking finding `0`.

## 7. 전체 상태 적대적 검토 — Loop 4

관점: **실제 consumer, 구현 현실성, readback**

공격:

- screen inventory가 예쁜 기획 표로 끝나고 실제 scene/node/resource와 연결되지 않을 수 있다.
- Notion visual과 GitHub/Godot runtime 사실이 drift할 수 있다.
- Work가 구현 완료를 과장할 수 있다.

검사:

- screen matrix에 `consumer_kind`, `consumer_surface`, `runtime_consumer`, `validation`, Notion/GitHub destination을 포함했다.
- Work instruction은 실제 consumer가 존재할 때 Godot scene/node/resource와 목표 해상도를 확인하도록 한다.
- Work 범위를 넘는 구현은 Codex handoff로 분리하고 runtime PASS를 주장하지 않도록 했다.

교정:

- Notion readback, GitHub exact path/readback, 가능한 범위의 Godot evidence를 완료 Gate에 포함했다.
- screen design reference, asset approval, implementation, runtime/player evidence의 claim ceiling을 분리했다.

결과: blocking finding `0`.

## 8. 전체 상태 적대적 검토 — Loop 5

관점: **회귀, 권한, 장기 운영**

공격:

- 기존 이미지 승인 Gate를 우회할 수 있다.
- open PR을 takeover하거나 Registry path를 충돌 수정할 수 있다.
- template이 프로젝트마다 placeholder 편집을 요구해 복사 즉시 실행되지 않을 수 있다.

검사:

- gap은 이미지 생성 권한이 아니며 current-turn explicit request가 없으면 이미지 도구를 호출하지 않는다.
- pre-existing open PR은 read-only, current work는 latest completed main 기반 별도 PR로 제한했다.
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 다른 open PR ownership 때문에 건드리지 않았다.
- template은 `[프로젝트명]`, `TBD` 없이 `현재 이 채팅이 연결된 프로젝트`를 기준으로 작성했다.
- test가 owner와 template의 경로·핵심 token·paste-ready 조건을 고정한다.

교정:

- Work instruction에 actual correction, readback, remaining-work rescan, no-auto-generation, Godot 종료를 명시했다.
- owner와 template을 additive path로 두고 기존 대형 owner를 불필요하게 재작성하지 않았다.

결과: blocking finding `0`.

## 9. 최종 판정

```text
full review loops: 5
new valid P0 finding after loop 5: 0
new valid P1 finding after loop 5: 0
duplicate canon introduced: NO
automatic image-generation authority introduced: NO
new dependency/provider/paid service: NO
project-specific value promoted to Base: NO
```

`CLEAN_REVIEW_EXIT` 판정은 design/document scope에서 충족한다.

최종 merge 판정은 별도다.

```text
latest main reconciliation
→ exact final HEAD CI PASS
→ required checks / review / unresolved thread 확인
→ safe squash merge
→ post-merge main readback
```

## 10. 롤백

구현 PR을 한 단위로 revert한다.

- screen-first companion owner 제거
- paste-ready Work instruction 제거
- focused regression 원복
- 이 review receipt 제거

기존 `GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`, image policy, approval gate, project Asset/Notion/runtime authority는 그대로 유지한다.