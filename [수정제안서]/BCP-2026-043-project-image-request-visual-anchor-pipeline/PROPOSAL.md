# BCP-2026-043 · Project Image Request Visual Anchor Pipeline

## 상태

```yaml
proposal_id: BCP-2026-043
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: USER_CHAT_2026-08-27_PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE
source_base_main: 1213aa45f2965c4aab67d6284367c6240e98dc2c
incremental_cost: 0
```

## 사용자 승인 목표

사용자는 프로젝트 이미지 작업마다 다음 장문 설명을 반복하지 않는다.

- 먼저 프로젝트에 이미 승인된 시각 1안이 있는지 확인
- 있으면 실제 이미지를 사용자에게 보여주고 해당 방향으로 진행
- 없으면 몇 가지 컨셉/스타일 후보를 만들어 사용자가 하나를 선택
- 확정된 컨셉·Flow·스타일 앵커를 기준으로 후속 자산의 분위기·그림체·색감 일관성 유지
- 탐색 시안과 실제 runtime asset 구분
- 결과 적대검토와 bounded correction

표준 trigger는 사용자의 current-turn `이미지 만들어줘` 같은 명시적 요청이다. 별도 장문 이미지 작업지시문은 필요하지 않다.

## 실제 Base 상태 감사

현재 Base에는 필요한 부분 기능이 이미 존재한다.

- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
  - actual consumer, requirement, generation/approval/runtime 분리
- `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
  - Visual Requirement Gate, `GENERATE_EXPLORATION`, `CREATE_CUSTOM`
- `IMAGE_CONVERSATION_APPROVAL_GATE.md`
  - text brief, next-turn approval, one deliverable, no automatic chain
- `notion-project-visual-continuity-gate.md`
  - `APPROVED_VISUAL_REFERENCE`, Keep/Avoid/Do Not Drift, fail-closed conflict
- `candidate-review-and-reusable-harvest.md`
  - candidate comparison, approval states, reuse classification
- `NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md`
  - Visual Bible, approval/readback, runtime handoff

그러나 다음 end-to-end 연결이 없었다.

```text
explicit image request
→ current approved visual 1안 resolution
→ show/reuse when found
→ concept comparison fallback when absent
→ user selection
→ standalone anchor lock
→ consistent production
→ style/flow adversarial review
```

또한 기존 conversation gate는 사용자가 이미 current turn에서 `이미지 만들어줘`라고 명시해도 text brief 뒤 다음 turn의 중복 승인을 요구했다. 사용자는 별도 장문 문구 없이 명시 요청 자체가 current deliverable pipeline을 시작하기를 승인했다.

## 비교안

| 안 | 장점 | 실패 모드 | 판정 |
|---|---|---|---|
| 기존 two-turn Gate만 유지 | 변경 작음 | 사용자가 매번 pipeline을 다시 설명하거나 중복 승인해야 함 | REJECT |
| explicit request 즉시 final asset 생성 | 빠름 | 승인 1안 부재·스타일 drift·재작업 위험 | REJECT |
| explicit request → anchor resolution → found/reuse or concept comparison | 자동화와 사용자 결정 경계 동시 보존 | 새 thin owner와 회귀 테스트 필요 | ADOPT |
| 모든 layer를 하나의 동일 그림체로 강제 | 표면 통일 | UI/VFX/marketing 역할 차이 손상 | REJECT |

## 채택 설계

새 thin owner:

`docs/knowledge/game-development/PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`

### 1. Explicit request route

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact Project + actual consumer
→ approved visual direction resolution
→ one output authority
```

명시 요청은 current deliverable 1건의 authority다. 생성 결과 승인·asset promotion·다음 image chain authority는 아니다.

### 2. Anchor found

```text
APPROVED_VISUAL_ANCHOR_FOUND
→ actual preview/binary readback
→ SURFACE_APPROVED_ANCHOR_TO_USER
→ Keep/Avoid/Do Not Drift
→ Flow/Screen context
→ requested output 1건
```

실제 anchor binary를 읽지 못하면 같은 스타일을 확인했다고 주장하지 않는다.

### 3. Anchor absent

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ one concept comparison deliverable
→ 3 materially distinct visual options by default
→ user selection
→ standalone anchor
→ project approval/readback
```

comparison sheet는 `GENERATED_EXPLORATION`이며 production/runtime asset이 아니다.

### 4. Direction lock

`VISUAL_DIRECTION_LOCK_PACKET`은 global grammar, layer anchor, Flow/Screen context, palette/value/lighting, camera/composition, Keep/Avoid/Do Not Drift, permitted variation, superseded refs와 destination readback을 연결한다. Project Decision/Visual Bible/Manifest를 복제하지 않는다.

### 5. Production consistency

후속 요청마다 current anchor와 relevant Flow/Screen/System을 fresh-read한다.

```text
STYLE_CONTINUITY_REVIEW_REQUIRED
FLOW_AND_SCREEN_SEMANTIC_CONSISTENCY_REQUIRED
NO_UNAPPROVED_STYLE_DRIFT
```

global grammar와 layer-specific 표현을 구분해 모든 자산을 복사처럼 만들지 않는다.

### 6. Correction

객관적 artifact·crop·alpha·dimension·approved-style drift·Flow mismatch는 current deliverable 안에서 bounded correction할 수 있다. 새 style/asset/count/core identity는 correction이 아니라 새 decision이다.

host가 사용자 노출 전 내부 retry를 지원하지 않으면 자동 교정을 과장하지 않고 `REVISION_REQUIRED`로 둔다.

## TDD

### RED

Test-only head `f9b7923aef4e73bf033e563e26610f0d629e3789`:

- Base v9 Operating Contracts: PASS
- docs/Ubuntu/publication checks: PASS
- whole core regression: expected FAIL
- failure cause: `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md` owner와 explicit request route가 없음

### GREEN 요구

- new thin pipeline owner
- existing conversation Gate에 user-initiated direct route + assistant-initiated two-turn route 분리
- old Gate tokens와 no-chain/evidence ceilings 비퇴행
- focused and whole-core regression
- current open PR path overlap 0
- 최소 5회 full-scope adversarial review
- exact-head safe squash merge + post-merge readback

## 범위 제외

- 실제 이미지 생성 없음
- Project GitHub/Notion/asset/runtime 변경 없음
- 모든 프로젝트 Art Direction 일괄 migration 없음
- comparison sheet 자동 승인 없음
- 새 Skill·Tool·provider·dependency·유료 비용 없음
- direct main·force·ruleset/admin bypass 없음

## 동시성

- PR #713은 UI/Visual generation integrity 관련 다른 경로를 소유하며 read-only다.
- PR #748은 five-stage proposal/spec/test 경로를 소유하며 read-only다.
- 이번 active path는 새 pipeline owner, conversation gate, proposal/case/test로 제한한다.
- `PROPOSAL_REGISTRY.json`은 PR #678 소유 중이므로 수정하지 않는다.

## 롤백

구현 squash commit을 revert하고 `IMAGE_CONVERSATION_APPROVAL_GATE.md`에서 새 pipeline route를 제거한다. 기존 two-turn Gate와 전문 visual owner는 그대로 유지된다.
