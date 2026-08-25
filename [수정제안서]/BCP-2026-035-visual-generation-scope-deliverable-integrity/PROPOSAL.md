# BCP-2026-035 — Visual Generation Scope & Deliverable Integrity

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Switchy-Express-Cargo-Puzzle`
- 프로젝트 증거 branch: `docs/visual-quality-handoff-20260825`
- 프로젝트 증거 commit: `2659c914be720b1e42279cab8183df6379ad22b9`
- 프로젝트 post-merge main: `4219f4e5e342c09024190e3fdaefa7a20051c988` · PR #177
- 문제→교훈 owner: `docs/knowledge/2026-08-25-visual-iteration-problem-lessons.md`
- 제출일: `2026-08-25`
- historical proposal PR: `#711` · merged `04bf4f216aed42ae9ee18f83e7eecde6f6bd4430`
- historical approval PR: `#712` · merged `3488cdff2f1ec7c2dd04ad2a53d2416fc35db431`
- 상태: `SUBMITTED`
- 사용자 승인 이력: 2026-08-25 Switchy Express closeout에서 사용자가 `Base 승격, 문제-교훈 자료도 잘 올려줘`라고 명시하고 이후 `진행해`로 연속 실행을 승인했다. 이 이력은 후속 approval review의 근거이지만 신규 machine identity `BCP-035`의 lifecycle 단계를 건너뛰는 근거로 사용하지 않는다.

### ID reconciliation

PR #711/#712 당시 Registry에 드러나지 않았던 기존 merged proposal `BCP-2026-034-notion-official-product-operating-reference`가 fresh readback에서 확인됐다. 동일 BCP ID를 유지하면 두 독립 workstream의 lifecycle/provenance가 충돌하므로 **Notion official-product workstream의 기존 BCP-034를 보존하고, Switchy visual-integrity workstream을 BCP-035로 재식별한다.**

- 이 변경은 내용/제품 방향을 바꾸지 않는 identifier reconciliation이다.
- BCP-034 Notion proposal/implementation PR #702/#704는 READ_ONLY이며 수정·흡수하지 않는다.
- historical PR #711/#712의 제목/본문은 당시 snapshot으로 보존한다.
- validator 기준으로 BCP-035는 신규 식별자이므로 `SUBMITTED`부터 lifecycle을 다시 시작한다.

## 관찰과 증거

Switchy Express의 2026-08-25 Visual GDD/이미지 반복 작업에서 다음 문제가 실제 발생했다.

1. **Scope drift** — 단일 `Capstone RUN Screen` 요청이 전체 프로젝트 인포그래픽/대시보드로 확대됐다.
2. **Decision-critical readability conflict** — 기존 미니어처 철도 스타일의 매력은 유지 가치가 높았지만 분기·선택 경로·점유/잠금 같은 판단 정보가 배경과 경쟁할 수 있었다.
3. **Batch semantic mismatch** — 사용자가 `3장씩`을 독립 결과 3개로 요청했지만 생성기가 한 장의 3-panel collage로 합쳤다.
4. **Evidence inflation risk** — 고품질 mock/reference가 실제 runtime/physical PASS처럼 오인될 위험이 있었다.
5. **Destination completion ambiguity** — 생성 파일 존재만으로는 Notion에서 지속 소비 가능한지 보장되지 않아 destination readback이 필요했다.

프로젝트 복구 증거:
- 한 이미지가 답할 visual question을 먼저 고정했다.
- 기존 art style/승인 asset은 유지하고 판단 정보만 semantic redundancy로 강화하는 방향을 사용자가 승인했다.
- N장 요청을 N개의 독립 검토 가능한 deliverable로 분리했다.
- mock/reference에 `NOT_RUNTIME_PROOF` evidence ceiling을 명시했다.
- Notion Visual owner에 durable preview를 attach/embed한 뒤 destination fetch와 attachment-content readback을 확인했다.
- 최초 GitHub JPG transport byte corruption은 제거하고 documentation-only reference path를 Godot scan에서 분리했다.
- corrected project exact head에서 Project Contract, Thin Adapter, GUT, Godot Tests가 GREEN이었고 PR #177은 main `4219f4e5...`로 병합됐다.

## Existing Solution First / 중복 검토

현재 Base에는 이미 다음 강한 계약이 존재한다.
- `auditing-and-refining-ui-art`: 상태는 색 하나에만 의존하지 않고 텍스트·형태·아이콘 등 동등 신호를 둔다.
- BCP-2026-032: Notion visual delivery의 destination readback과 evidence ceiling.
- `NOTION_APPROVED_ORIGINAL_FIRST_GATE`: 승인 visual original-first 보존과 preview 경계.
- Base evidence discipline: mock/자동 검증을 사람·기기·runtime 증거로 과장하지 않는다.

따라서 BCP-035는 세 좁은 gap만 공용화한다.

## 일반화 후보

### `VISUAL_TASK_SCOPE_FIDELITY`

bounded image 작업 전에 아래를 고정한다.

```text
visual_question / target_screen / target_state / excluded_scope
```

생성물이 경계를 넘어 unrelated screen, broad dashboard, 새 게임 규칙/UI를 추가하면 보기 좋더라도 같은 deliverable PASS로 세지 않는다.

### `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`

사용자가 N장의 이미지/결과를 요청하면 기본 해석은 **독립 검토·교체·배치 가능한 N개 결과**다.

- 한 collage의 N panel은 사용자가 collage를 요청한 경우에만 N장과 동등하다.
- 의미 손실 없이 분리 가능하면 독립 파일로 분리할 수 있다.
- panel 의존성이 있거나 crop으로 의미가 손상되면 재생성한다.
- 프로젝트 고유 숫자 `3`은 Base 규칙에 넣지 않는다.

### `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`

플레이 판단에 직접 쓰는 정보가 art/background와 경쟁할 때 최소한 다음을 비교한다.

| 대안 | 장점 | 위험 | 기본 판정 |
| --- | --- | --- | --- |
| 전체 art style 교체 | 큰 변화 | 기존 asset/identity 비용, 원인 오진 | 마지막 수단 |
| color/intensity 한 축만 강화 | 빠름 | color-only/상태 혼동 | 단독 사용 회피 |
| 기존 정체성 유지 + 독립 semantic cue 중복 | 기존 asset 보존, 판단성 직접 개선 | 상태 규칙 consistency 필요 | 우선 검토 |

특정 색/화살표/두께를 Base에 고정하지 않는다. 프로젝트 의미에 맞게 color, direction, shape, text/icon, brightness/thickness, motion 중 필요한 독립 신호를 조합한다.

## 프로젝트 전용으로 남길 내용

Base에 승격하지 않는다.
- `E+D Hybrid / Neo-Arcade Readability`
- Cozy Miniature railway / 토끼 기관사
- Switchy의 green/blue/red/yellow 의미색
- 73 product PNG 수량
- `SX59-POC-ACCEPT-003`
- 사용자의 정확한 `3장씩` 숫자
- Switchy Train/Station/Cargo/Switch 디자인
- 특정 Notion page/file upload ID와 프로젝트 경로

## 적용 조건과 비사용 조건

적용 조건:
- AI/생성형 이미지 도구로 single-screen mock, state sheet, before/after, visual QA reference처럼 명확한 bounded deliverable을 만들 때.
- 사용자가 N개의 이미지/결과 수량을 명시했을 때.
- decision-critical state가 art/background와 경쟁하고 기존 제품 정체성/asset을 보존할 가치가 있을 때.

비사용 조건:
- 사용자가 처음부터 poster, dashboard, collage, broad concept board를 요청했을 때.
- N-panel 전체가 하나의 비교 문맥이어야 의미가 있고 사용자가 그 형식을 승인했을 때.
- 실제 제품 fantasy가 transformation/style replacement 자체일 때.
- color가 정보가 아닌 순수 장식일 때.
- 생성 image가 아니라 단순 텍스트/기계 변경만 하는 작업.

## 반례와 위험

- broad concept work까지 단일 질문으로 강제하면 발산 탐색을 방해할 수 있다.
- 비교표/스토리보드처럼 panel 관계가 정보인 경우 collage가 올바른 deliverable일 수 있다.
- semantic cue를 모두 최대 강도로 쓰면 오히려 과밀해질 수 있다.
- 기존 style이 실제 문제 원인이거나 제품 방향이 바뀐 경우 style 유지가 자동 정답은 아니다.
- visual mock만으로 human comprehension, accessibility, runtime/device correctness를 증명하지 않는다.
- BCP-032 및 original-first owner의 책임을 중복 구현하지 않는다.

## 영향 범위와 검증

후속 approval 시 검토할 최소 구현 후보 범위:

1. `skills/auditing-and-refining-ui-art/SKILL.md`
   - `VISUAL_TASK_SCOPE_FIDELITY`
   - `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`
   - `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`
2. `docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
   - bounded Visual GDD 작업의 visual question / excluded scope 기록
   - N장 요청의 independent-deliverable 기본값
   - current original-first/readback gate 보존
3. 프로젝트 중립 problem→lesson case 1개 + 최소 discoverability 갱신
4. focused regression coverage

명시적 제외:
- 신규 Skill/Tool/dependency/service/dashboard
- BCP-032 Notion preview fallback/readback 재구현
- original-first 약화 또는 preview를 canonical original로 승격
- Switchy-specific 값
- 실제 게임/runtime/project 변경

검증:
- BCP-035 identifier reconciliation은 proposal/registry validation과 exact-head CI를 통과해야 한다.
- 승인 및 구현은 각각 별도 fresh-main PR로 lifecycle을 분리한다.
- 구현 단계에서는 RED → GREEN, exact-head relevant CI, 최소 5회 whole-state adversarial review를 요구한다.
- project evidence는 방법론/guardrail을 지지하지만 player comprehension/accessibility/Candidate 003 physical PASS를 증명하지 않는다.

## 승인과 구현

- 현재 lifecycle 상태: `SUBMITTED`.
- historical user approval intent와 PR #711/#712는 후속 approval review의 evidence로 보존한다.
- `approval_ref`: 아직 BCP-035 machine lifecycle에는 부여하지 않는다.
- 구현 PR: 없음. 기존 draft PR #713은 BCP-035 approval이 main에 정착하기 전까지 active implementation으로 승격하지 않는다.
- 롤백: ID correction은 proposal path/registry identity만 revert; 후속 active implementation은 별도 PR 단위로 revert.
