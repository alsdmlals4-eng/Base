# BCP-2026-033 — Visual Generation Scope & Deliverable Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 프로젝트 증거 branch: `docs/visual-quality-handoff-20260825`
- 프로젝트 증거 commit: `b45c45a0ad6d11e698289f3e44a80780716a76f6`
- 문제→교훈 owner: `docs/knowledge/2026-08-25-visual-iteration-problem-lessons.md`
- 제출일: `2026-08-25`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 사용자 승인 근거: 2026-08-25 현재 작업에서 사용자가 "인수인계 진행하자 ... Base 승격, 문제-교훈 자료도 잘 올려줘"라고 명시

## 관찰과 실제 문제

Switchy Express의 2026-08-25 Visual GDD/이미지 반복 작업에서 다음 문제가 실제 발생했다.

1. **Scope drift** — `Capstone RUN Screen`처럼 단일 화면을 요청했지만 생성 결과가 전체 프로젝트 인포그래픽/대시보드로 확대됐다.
2. **Decision-critical readability conflict** — 기존 미니어처 철도 스타일은 유지 가치가 높았지만 분기·선택 경로·점유/잠금 같은 판단 정보가 배경과 경쟁할 수 있었다.
3. **Batch semantic mismatch** — 사용자가 "3장씩"을 독립 결과 3개로 요청했지만 생성기가 한 장의 3-panel collage로 합쳤다.
4. **Evidence inflation risk** — 고품질 mock/reference가 실제 runtime/physical PASS처럼 오인될 위험이 있었다.
5. **Destination completion ambiguity** — 생성 파일 존재만으로는 Notion에서 실제 지속 소비 가능한지 보장되지 않아 destination readback이 필요했다.

프로젝트는 이 문제를 다음 방식으로 복구했다.

- 한 이미지가 답할 visual question을 먼저 고정.
- 기존 art style/승인 asset은 유지하고 판단 정보만 semantic redundancy로 강화.
- N장 요청은 N개의 독립 검토 가능한 deliverable로 분리.
- mock/reference에 `NOT_RUNTIME_PROOF` evidence ceiling을 명시.
- Notion Visual owner에 실제 embed 후 destination fetch/readback을 확인.

## Existing Solution First / 중복 검토

현재 Base main에는 이미 다음 강한 계약이 존재한다.

- `auditing-and-refining-ui-art`: 상태는 색 하나에만 의존하지 않고 텍스트·형태·아이콘 등 동등 신호를 둔다.
- BCP-2026-032: Notion visual delivery에서 destination readback과 `SERVER_READBACK_PASS != HUMAN_VISIBLE_PASS` 경계를 강화했다.
- Base evidence discipline: mock/자동 검증을 실제 사람·기기·runtime 증거로 과장하지 않는다.

따라서 본 제안은 위 계약을 복제하지 않는다. 새로 공용화할 가치가 있는 좁은 gap은 다음 세 가지다.

1. 이미지 생성 **scope fidelity**를 결과 acceptance에 명시적으로 연결하는 규칙.
2. 사용자의 **N장 batch = N independent deliverables** 기본 해석.
3. decision-critical visual에서 style replacement보다 기존 정체성 보존 + semantic redundancy를 먼저 비교하는 guardrail.

Evidence ceiling/readback은 새 owner를 만들지 않고 기존 Base 계약을 참조한다.

## 일반화 후보

### 1. `VISUAL_TASK_SCOPE_FIDELITY`

이미지 제작 전에 다음을 한 줄로 고정한다.

```text
visual_question / target_screen / target_state / excluded_scope
```

생성물이 이 경계를 넘어 전체 dashboard, unrelated screen, 새로운 게임 규칙/UI를 추가하면 보기 좋더라도 같은 deliverable의 PASS로 세지 않는다.

적용:
- single-screen mock
- component/state sheet
- before/after comparison
- visual QA reference

비사용:
- 사용자가 poster, dashboard, collage, broad concept board를 명시적으로 요청한 경우

### 2. `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N장의 이미지/결과를 요청하면 기본 해석은 **독립 검토·교체·배치 가능한 N개 결과**다.

- 한 collage의 N panel은 사용자가 collage를 요청한 경우에만 N장과 동등하다.
- 잘못 합쳐졌고 의미 손실 없이 분리 가능하면 독립 파일로 분리할 수 있다.
- 각 panel이 서로 의존하거나 crop으로 의미가 손상되면 재생성한다.

프로젝트 고유 숫자 `3`은 Base 규칙에 넣지 않는다.

### 3. `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

플레이 판단에 직접 쓰는 정보가 현재 art style에서 묻히면 다음 3안을 최소 비교한다.

| 안 | 장점 | 주요 위험 | 기본 판정 |
| --- | --- | --- | --- |
| 전체 art style 교체 | 큰 변화 | 기존 asset/identity 비용, 원인 오진 가능 | 마지막 수단 |
| color/intensity 한 축만 강화 | 빠름 | color-only/상태 혼동 | 단독 사용 회피 |
| 기존 정체성 유지 + 독립 semantic cue 중복 | 기존 asset 보존, 판단성 직접 개선 | 상태 규칙 consistency 필요 | 우선 검토 |

공용 원칙은 특정 색/화살표/두께를 고정하지 않는다. 프로젝트의 의미에 맞게 color, direction, shape, text/icon, brightness/thickness, motion 중 독립 신호를 조합한다.

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

## 반례·비사용 조건

- 사용자가 broad moodboard/concept sheet를 원하면 scope expansion이 결함이 아니다.
- 실제 제품 fantasy가 transformation/style replacement 자체라면 기존 style 보존이 목표가 아닐 수 있다.
- color가 정보가 아닌 순수 장식이면 semantic redundancy를 강제하지 않는다.
- N-panel이 하나의 비교 문맥을 구성해야 의미가 있는 경우 collage가 올바른 deliverable일 수 있다.
- visual mock만으로 human comprehension improvement를 증명하지 않는다.

## 영향 범위 / 권장 구현

신규 Skill/Tool을 만들지 않는다.

권장 최소 구현:

1. `skills/auditing-and-refining-ui-art/SKILL.md`
   - visual task scope acceptance
   - decision-critical semantic redundancy의 기존 규칙을 더 명시적인 recovery gate로 강화
   - batch-independent deliverable 규칙 추가
2. `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
   - image generation/Visual GDD delivery에서 visual question + excluded scope + independent batch output를 기록
3. focused regression test 1개
   - 위 세 계약 문자열과 BCP provenance를 검증
4. 문제→교훈 case 1개
   - Switchy 프로젝트 값은 제거하고 문제/복구/반례/evidence ceiling만 남김

BCP-2026-032의 Notion preview fallback/readback owner는 변경하지 않고 참조만 한다.

## 5-pass adversarial review

1. **중복:** Base에는 상태 semantic redundancy는 있으나 image-generation scope fidelity와 N-independent-deliverable 계약은 없음.
2. **과잉 일반화:** Switchy 스타일·색·3장 숫자는 제외함.
3. **증거 한계:** 실제 player comprehension 개선은 미검증이며 방법론/guardrail만 승격함.
4. **비용/복잡도:** 신규 Skill/Tool 없이 기존 UI/Visual owner에 additive rule만 넣어 churn을 최소화함.
5. **롤백/충돌:** additive owner section + focused test 단위로 되돌릴 수 있고, BCP-032와 책임이 겹치지 않음.

새 blocking finding: `0`.

검토 판정: `APPROVED_FOR_IMPLEMENTATION`.

## 승인과 구현

- 사용자 승인 근거: 2026-08-25 현재 Switchy Express closeout 작업에서 "Base 승격, 문제-교훈 자료도 잘 올려줘" 명시.
- `approval_ref`: `[수정제안서]/BCP-2026-033-visual-generation-scope-deliverable-integrity/PROPOSAL.md#승인과-구현 (2026-08-25 current task user instruction)`.
- 제안과 active Base 구현은 별도 PR로 유지한다.
- 구현 전 proposal/registry merge를 먼저 완료한다.
- 구현은 위 권장 최소 구현 범위를 넘기지 않는다.
