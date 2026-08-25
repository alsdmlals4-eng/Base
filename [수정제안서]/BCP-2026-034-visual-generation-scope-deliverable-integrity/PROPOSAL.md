# BCP-2026-034 — Visual Generation Scope & Deliverable Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 프로젝트 증거 branch: `docs/visual-quality-handoff-20260825`
- 프로젝트 증거 commit: `b45c45a0ad6d11e698289f3e44a80780716a76f6`
- 문제→교훈 owner: `docs/knowledge/2026-08-25-visual-iteration-problem-lessons.md`
- 제출일: `2026-08-25`
- 상태: `SUBMITTED`
- 사용자 promotion intent: 2026-08-25 현재 작업에서 사용자가 "인수인계 진행하자 ... Base 승격, 문제-교훈 자료도 잘 올려줘"라고 명시했다.
- lifecycle boundary: 신규 proposal은 이 PR에서 `SUBMITTED`로만 등록한다. 승인 상태 변경과 active Base 구현은 proposal 병합 뒤 각각 별도 lifecycle 단계에서 수행한다.
- ID collision note: current Base open PR #693/#679가 BCP-033을 이미 사용하므로 본 current-task proposal은 open-workstream ownership을 침범하지 않기 위해 BCP-034로 배정한다.

## 관찰과 증거

Switchy Express의 2026-08-25 Visual GDD/이미지 반복 작업에서 다음 문제가 실제 발생했다.

1. **Scope drift** — `Capstone RUN Screen`처럼 단일 화면을 요청했지만 생성 결과가 전체 프로젝트 인포그래픽/대시보드로 확대됐다.
2. **Decision-critical readability conflict** — 기존 미니어처 철도 스타일은 유지 가치가 높았지만 분기·선택 경로·점유/잠금 같은 판단 정보가 배경과 경쟁할 수 있었다.
3. **Batch semantic mismatch** — 사용자가 "3장씩"을 독립 결과 3개로 요청했지만 생성기가 한 장의 3-panel collage로 합쳤다.
4. **Evidence inflation risk** — 고품질 mock/reference가 실제 runtime/physical PASS처럼 오인될 위험이 있었다.
5. **Destination completion ambiguity** — 생성 파일 존재만으로는 Notion에서 실제 지속 소비 가능한지 보장되지 않아 destination readback이 필요했다.

프로젝트 복구 증거:

- 한 이미지가 답할 visual question을 먼저 고정했다.
- 기존 art style/승인 asset은 유지하고 판단 정보만 semantic redundancy로 강화하는 방향을 사용자가 승인했다.
- N장 요청을 N개의 독립 검토 가능한 deliverable로 분리했다.
- mock/reference에 `NOT_RUNTIME_PROOF` evidence ceiling을 명시했다.
- Notion Visual owner에 durable preview를 attach/embed한 뒤 destination fetch와 attachment-content readback을 확인했다.
- 최초 GitHub JPG transport는 byte corruption이 확인되어 제거했고 documentation-only reference path를 Godot scan에서 분리했다.

### Existing Solution First / 중복 검토

현재 Base main에는 이미 다음 강한 계약이 존재한다.

- `auditing-and-refining-ui-art`: 상태는 색 하나에만 의존하지 않고 텍스트·형태·아이콘 등 동등 신호를 둔다.
- BCP-2026-032: Notion visual delivery에서 destination readback과 `SERVER_READBACK_PASS != HUMAN_VISIBLE_PASS` 경계를 강화했다.
- `NOTION_APPROVED_ORIGINAL_FIRST_GATE`: 승인 visual의 original-first 보존과 preview/evidence 경계를 관리한다.
- Base evidence discipline: mock/자동 검증을 실제 사람·기기·runtime 증거로 과장하지 않는다.

따라서 본 제안은 위 계약을 복제하지 않는다. 새로 공용화할 좁은 gap은 다음 세 가지다.

1. 이미지 생성 **scope fidelity**를 결과 acceptance에 명시적으로 연결하는 규칙.
2. 사용자의 **N장 batch = N independent deliverables** 기본 해석.
3. decision-critical visual에서 style replacement보다 기존 정체성 보존 + semantic redundancy를 먼저 비교하는 recovery guardrail.

Evidence ceiling/readback/original-first는 새 owner를 만들지 않고 기존 Base 계약을 참조한다.

## 일반화 후보

### 1. `VISUAL_TASK_SCOPE_FIDELITY`

이미지 제작 전에 다음을 한 줄로 고정한다.

```text
visual_question / target_screen / target_state / excluded_scope
```

생성물이 이 경계를 넘어 전체 dashboard, unrelated screen, 새로운 게임 규칙/UI를 추가하면 보기 좋더라도 같은 deliverable의 PASS로 세지 않는다.

### 2. `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N장의 이미지/결과를 요청하면 기본 해석은 **독립 검토·교체·배치 가능한 N개 결과**다.

- 한 collage의 N panel은 사용자가 collage를 요청한 경우에만 N장과 동등하다.
- 잘못 합쳐졌고 의미 손실 없이 분리 가능하면 독립 파일로 분리할 수 있다.
- 각 panel이 서로 의존하거나 crop으로 의미가 손상되면 재생성한다.
- 프로젝트 고유 숫자 `3`은 Base 규칙에 넣지 않는다.

### 3. `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

플레이 판단에 직접 쓰는 정보가 현재 art style에서 묻히면 최소한 다음 대안을 비교한다.

| 안 | 장점 | 주요 위험 | 기본 판정 |
| --- | --- | --- | --- |
| 전체 art style 교체 | 큰 변화 | 기존 asset/identity 비용, 원인 오진 가능 | 마지막 수단 |
| color/intensity 한 축만 강화 | 빠름 | color-only/상태 혼동 | 단독 사용 회피 |
| 기존 정체성 유지 + 독립 semantic cue 중복 | 기존 asset 보존, 판단성 직접 개선 | 상태 규칙 consistency 필요 | 우선 검토 |

공용 원칙은 특정 색/화살표/두께를 고정하지 않는다. 프로젝트 의미에 맞게 color, direction, shape, text/icon, brightness/thickness, motion 중 독립 신호를 조합한다.

## 프로젝트 전용으로 남길 내용

Base에 승격하지 않는다.

- `E+D Hybrid / Neo-Arcade Readability`
- Cozy Miniature railway
- 토끼 기관사
- Switchy의 green/blue/red/yellow 의미색
- 73 product PNG 수량
- `SX59-POC-ACCEPT-003`
- 현재 사용자의 `3장씩`이라는 숫자
- Switchy의 실제 Train/Station/Cargo/Switch 디자인
- 특정 Notion page/file upload ID와 프로젝트 경로

## 적용 조건과 비사용 조건

적용 조건:

- AI 또는 생성형 이미지 도구로 single-screen mock, state sheet, before/after, visual QA reference 등 명확한 deliverable을 제작할 때.
- 사용자가 N개의 이미지/결과 수량을 명시했을 때.
- decision-critical state가 art/background와 경쟁해 판단성이 낮아졌고 기존 제품 정체성/asset을 보존할 가치가 있을 때.

비사용 조건:

- 사용자가 처음부터 poster, dashboard, collage, broad concept board를 요청했을 때.
- N-panel 전체가 하나의 비교 문맥이어야 의미가 있고 사용자가 그 형식을 승인했을 때.
- 실제 제품 fantasy가 transformation/style replacement 자체라서 기존 style 보존이 목표가 아닐 때.
- color가 정보가 아닌 순수 장식이라 semantic redundancy가 불필요할 때.
- 생성 image가 아니라 단순 텍스트/기계 변경만 하는 작업.

## 반례와 위험

1. **과도한 scope rigidity** — 탐색 단계의 broad concept work까지 단일 질문으로 강제하면 발산 탐색을 방해할 수 있다. 명시된 deliverable 유형에만 적용한다.
2. **collage 오판** — 비교표/스토리보드처럼 panel 관계 자체가 정보인 경우에는 독립 파일 분할이 오히려 맥락을 깨뜨릴 수 있다.
3. **semantic overload** — 모든 cue를 동시에 최대 강도로 쓰면 화면이 더 복잡해질 수 있다. 독립 신호 중 필요한 최소 조합을 프로젝트가 선택한다.
4. **style-preservation fetishism** — 기존 style이 실제 문제 원인이거나 제품 방향이 바뀐 경우 style 유지가 자동 정답은 아니다.
5. **evidence inflation** — visual mock만으로 human comprehension, accessibility, runtime/device correctness를 증명하지 않는다.
6. **owner duplication** — BCP-032의 Notion delivery/readback과 latest original-first gate를 중복 구현하면 안 된다.

## 영향 범위와 검증

신규 Skill/Tool/service를 만들지 않는다.

승인될 경우의 권장 최소 구현 후보:

1. `skills/auditing-and-refining-ui-art/SKILL.md`
   - visual task scope acceptance
   - decision-critical semantic redundancy recovery gate
   - batch-independent deliverable 규칙
2. `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
   - image generation/Visual GDD delivery에서 visual question + excluded scope + independent batch output를 기록
3. focused regression test 1개
   - 위 세 계약과 BCP provenance를 검증
4. 문제→교훈 case 1개
   - Switchy 프로젝트 값은 제거하고 문제/복구/반례/evidence ceiling만 남김

Proposal 단계 검증:

- Base change proposal validator PASS
- docs/core proposal-contract regression PASS
- current Base main과 behind/conflict 재확인
- 프로젝트 전용 값 누출 없음
- BCP-032/original-first owner 중복 없음

### 5-pass adversarial review snapshot

1. **중복:** Base에는 상태 semantic redundancy/readback/original-first는 있으나 image-generation scope fidelity와 N-independent-deliverable 계약은 명시적 gap이 있다.
2. **과잉 일반화:** Switchy 스타일·색·3장 숫자·Candidate/asset ID는 제외한다.
3. **증거 한계:** 실제 player comprehension 개선은 미검증이며 방법론/guardrail만 제안한다.
4. **비용/복잡도:** 신규 Skill/Tool 없이 기존 UI/Visual owner의 additive rule을 우선한다.
5. **롤백/충돌:** proposal은 `[수정제안서]/**`만 포함하고 active owner 구현은 별도 승인/PR로 분리한다.

현재 proposal review finding: 새 blocking finding `0`.

## 필요한 도구·파일·권한

- GitHub repository proposal branch/PR
- source project의 current handoff/problem→lesson evidence
- Base current UI/Visual/Notion owner read access
- 신규 도구·서비스·추가 금전 비용 없음
- active Base owner write는 proposal 단계에서 사용하지 않는다.

## 승인과 구현

- 사용자 promotion intent: 2026-08-25 Switchy Express closeout 작업에서 "Base 승격, 문제-교훈 자료도 잘 올려줘"라고 명시했다.
- **현재 lifecycle 상태는 `SUBMITTED`**다. 신규 제안 첫 PR에서 `APPROVED_FOR_IMPLEMENTATION`으로 점프하지 않는다.
- proposal PR 병합 후 current Base에서 별도 status-review PR을 만들고, 현재 사용자 지시를 재현 가능한 approval evidence로 기록하여 `APPROVED_FOR_IMPLEMENTATION` 이동 여부를 검증한다.
- active Base 구현은 승인 상태와 비어 있지 않은 `approval_ref`가 확인된 뒤 **또 다른 별도 implementation PR**에서만 수행한다.
- rollback: proposal 단계는 BCP directory + registry entry만 revert한다.
