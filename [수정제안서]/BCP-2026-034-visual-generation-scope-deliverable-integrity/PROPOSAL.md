# BCP-2026-034 — Visual Generation Scope & Deliverable Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 프로젝트 증거 branch: `docs/visual-quality-handoff-20260825`
- 프로젝트 증거 commit: `2659c914be720b1e42279cab8183df6379ad22b9`
- 프로젝트 post-merge main: `4219f4e5e342c09024190e3fdaefa7a20051c988` · PR #177
- 문제→교훈 owner: `docs/knowledge/2026-08-25-visual-iteration-problem-lessons.md`
- 제출일: `2026-08-25`
- proposal PR: `https://github.com/alsdmlals4-eng/Base/pull/711` · merged as `04bf4f216aed42ae9ee18f83e7eecde6f6bd4430`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 사용자 승인 근거: 2026-08-25 현재 작업에서 사용자가 "인수인계 진행하자 ... Base 승격, 문제-교훈 자료도 잘 올려줘"라고 명시했다.
- approval ref: `[수정제안서]/BCP-2026-034-visual-generation-scope-deliverable-integrity/PROPOSAL.md#승인과-구현 (2026-08-25 current task user instruction; proposal PR #711 merged)`
- ID collision note: Base open PR #693/#679가 BCP-033을 이미 사용하므로 본 workstream은 BCP-034를 사용한다. 해당 PR은 계속 READ_ONLY다.

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
- corrected project exact head에서 Project Contract, Thin Adapter, GUT, Godot Tests가 모두 GREEN이었고 PR #177은 exact-head merge 후 main `4219f4e5...`로 readback했다.

### Existing Solution First / 중복 검토

현재 Base main에는 이미 다음 강한 계약이 존재한다.

- `auditing-and-refining-ui-art`: 상태는 색 하나에만 의존하지 않고 텍스트·형태·아이콘 등 동등 신호를 둔다.
- BCP-2026-032: Notion visual delivery에서 destination readback과 `SERVER_READBACK_PASS != HUMAN_VISIBLE_PASS` 경계를 강화했다.
- `NOTION_APPROVED_ORIGINAL_FIRST_GATE`: 승인 visual의 original-first 보존과 preview/evidence 경계를 관리한다.
- Base evidence discipline: mock/자동 검증을 실제 사람·기기·runtime 증거로 과장하지 않는다.

따라서 본 제안은 위 계약을 복제하지 않는다. 공용화할 좁은 gap은 다음 세 가지다.

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

승인된 최소 구현 범위:

1. `skills/auditing-and-refining-ui-art/SKILL.md`
   - bounded visual 작업의 `VISUAL_TASK_SCOPE_FIDELITY`
   - `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`
   - 기존 state redundancy 규칙을 보존하면서 decision-critical visual recovery에서 `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`를 명시
2. `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
   - bounded image generation / Visual GDD delivery에서 `visual_question / target_screen / target_state / excluded_scope` 기록
   - N장 요청의 independent-deliverable 기본값 기록
   - 승인 후 current original-first/readback gate를 그대로 적용
3. 공용 problem→lesson case 1개 + 기존 case index의 최소 discoverability 갱신
4. focused regression test 1개 또는 책임 owner별 최소 테스트

명시적 제외:

- 신규 Skill / Tool / dependency / service / dashboard
- BCP-032의 Notion preview fallback/readback 계약 재구현
- `NOTION_APPROVED_ORIGINAL_FIRST_GATE` 약화 또는 low-res preview를 canonical original로 승격
- Switchy-specific style, palette, character, exact batch count, asset/Candidate ID
- 실제 게임/runtime/프로젝트 변경

검증:

- 구현은 별도 fresh-main branch/PR에서 TDD RED → GREEN
- current Base relevant full regression
- exact-head CI
- 최소 5회 whole-state adversarial review
- proposal/source provenance와 approval scope readback

## Proposal review — 2026-08-25

최소 5회 whole-state proposal review 결과:

1. **Source evidence:** project PR #177의 corrected exact head와 merge/readback, Notion attachment/content readback이 존재하며 runtime/human-visible 범위를 분리했다.
2. **Generalization boundary:** Switchy art style·캐릭터·색·73 PNG·Candidate ID·정확한 `3장` 수치는 Base 범위에서 제외했다.
3. **Existing owner reuse:** state readability는 기존 `auditing-and-refining-ui-art`, visual delivery/readback은 BCP-032 및 current original-first owner에 흡수 가능하며 새 Skill/도구가 필요 없다.
4. **Counterexamples/evidence ceiling:** broad moodboard, meaningful collage, true style replacement, semantic overload 반례를 보존하고 사람 이해/접근성 개선은 미검증으로 둔다.
5. **Lifecycle/rollback/concurrency:** proposal #711은 `SUBMITTED`로 먼저 병합했고, approval은 proposal-only 변경으로 분리하며 open BCP-033 workstreams는 수정하지 않는다. 구현은 별도 PR로 rollback 가능하다.

새 blocking finding: `0`.

검토 판정: `APPROVED_FOR_IMPLEMENTATION`.

## 필요한 도구·파일·권한

- GitHub repository approval/implementation branches and PR workflow
- source project current handoff/problem→lesson evidence read access
- Base current UI/Visual/Notion owner read/write access for the later approved implementation PR
- 신규 도구·서비스·추가 금전 비용 없음
- force push/admin/ruleset bypass 불필요

## 승인과 구현

- 사용자 승인 근거: `2026-08-25 Switchy Express closeout current task — "Base 승격, 문제-교훈 자료도 잘 올려줘"` 및 이후 `진행해` continuation.
- proposal PR: `https://github.com/alsdmlals4-eng/Base/pull/711` · merged as `04bf4f216aed42ae9ee18f83e7eecde6f6bd4430`.
- 검토 판정: `APPROVED_FOR_IMPLEMENTATION`.
- `approval_ref`: `[수정제안서]/BCP-2026-034-visual-generation-scope-deliverable-integrity/PROPOSAL.md#승인과-구현 (2026-08-25 current task user instruction; proposal PR #711 merged)`.
- 구현 PR: `없음 — approval merge 뒤 fresh main에서 별도 TDD PR`.
- 롤백: approval은 proposal/registry status revert; 구현은 owner/case/test additive 변경을 implementation PR 단위로 revert.
