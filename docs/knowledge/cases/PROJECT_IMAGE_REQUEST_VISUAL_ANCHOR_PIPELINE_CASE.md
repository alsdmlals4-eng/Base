# Project Image Request · Visual Anchor Resolution 사례

```text
IMAGE_REQUEST_SHOULD_RESOLVE_CURRENT_VISUAL_DIRECTION_FIRST
APPROVED_ANCHOR_OR_CONCEPT_COMPARISON_NOT_BLIND_FINAL_PRODUCTION
COMPARISON_BOARD_IS_NOT_RUNTIME_ASSET
STYLE_CONTINUITY_NEEDS_FLOW_AND_LAYER_CONTEXT
```

## 1. 문제

사용자가 프로젝트 채팅에서 `이미지 만들어줘`라고 요청할 때마다 긴 pipeline 문구를 다시 붙여야 하거나, 반대로 AI가 current Project Visual canon을 읽지 않고 즉시 final 이미지를 만들면 다음 문제가 생긴다.

- 이미 승인된 Art Direction·Visual North Star를 놓치고 다른 그림체를 생성
- 승인 1안이 없는데 final asset부터 만들어 재작업 증가
- 컨셉 비교 시트를 runtime asset이나 최종 master로 오인
- 배경·캐릭터·UI·VFX가 서로 다른 프로젝트처럼 drift
- Flow/Screen에 없는 버튼·상태·시스템을 이미지가 새 요구사항처럼 발명
- 생성 성공을 project approval·Manifest·runtime 적용으로 과장
- 사용자가 매번 같은 장문 지시를 복사해야 하는 운영비 증가

## 2. 기존 기능과 연결 누락

Base에는 이미 다음 전문 기능이 있었다.

```text
Visual Requirement Gate
actual consumer
Image Conversation Approval Gate
APPROVED_VISUAL_REFERENCE continuity
candidate review
Notion approval/readback
runtime handoff
```

그러나 user current-turn image request에서 이들을 다음처럼 연결하는 owner가 없었다.

```text
explicit request
→ exact Project
→ current approved visual anchor
→ show/reuse or concept comparison
→ selected standalone anchor
→ consistent production
```

부분 기능의 존재는 end-to-end 실행성을 보장하지 않는다.

## 3. 채택한 해결

### 3.1 사용자가 현재 출력을 명시한 경우

```text
이미지 만들어줘
→ exact Project + actual consumer fresh-read
→ visual anchor resolution
→ current deliverable one-output authority
```

별도 장문 pipeline 지시나 같은 요청의 중복 승인을 요구하지 않는다.

### 3.2 현재 승인 1안이 있는 경우

```text
approved Decision / Visual Bible / Asset / Manifest
→ current and non-superseded 확인
→ actual preview/source binary readback
→ 사용자에게 surface
→ Keep/Avoid/Do Not Drift
→ relevant Flow/Screen context
→ requested candidate one output
```

텍스트에 `승인 이미지 있음`이라고 적혀 있어도 실제 visual을 읽지 못하면 style continuity PASS가 아니다.

### 3.3 현재 승인 1안이 없는 경우

```text
no usable anchor
→ one comparison board
→ same actual consumer, three materially distinct directions
→ user selects one
→ standalone anchor production
→ user/project approval + destination readback
```

비교 보드는 방향 선택 도구다. panel crop을 final master나 runtime asset으로 사용하지 않는다.

### 3.4 후속 생산

```text
current anchor
+ global grammar
+ layer-specific anchor
+ Flow/Screen semantics
+ actual consumer constraints
→ requested output
→ adversarial review
→ bounded correction
```

같은 프로젝트라는 것은 모든 layer의 detail density가 같다는 뜻이 아니다. 캐릭터·환경·UI·VFX는 역할별 표현을 가질 수 있지만 palette family, shape/material language, camera tendency, lighting grammar, identity hierarchy와 정보 의미를 공유한다.

## 4. 적대적 검토에서 확인할 실패 모드

1. **Anchor authority 공격**
   - draft/rejected/old chat/다른 프로젝트 이미지를 current 1안으로 사용했는가
2. **Comparison inflation 공격**
   - 비교용 board가 production asset 또는 여러 deliverable로 승격됐는가
3. **Style sameness/drift 공격**
   - 모든 layer를 똑같게 만들어 역할을 잃었거나, 반대로 공통 grammar가 사라졌는가
4. **Flow invention 공격**
   - 이미지가 승인되지 않은 screen state·button·mechanic을 추가했는가
5. **Evidence overclaim 공격**
   - generated candidate를 user-approved/runtime-applied로 기록했는가

## 5. Objective correction 경계

같은 requested deliverable의 다음 결함은 bounded correction 대상이다.

- anatomy·edge·artifact
- crop·alpha·margin·dimension·format
- 승인 anchor에서 벗어난 명백한 palette/camera/material drift
- current Flow/consumer와 다른 정보 배치
- gameplay scale에서 읽히지 않는 대비·실루엣

다음은 correction이 아니다.

- 새 Art Direction
- 독립 variant·pose·character·screen 추가
- asset count 확대
- core identity 변경
- 다른 consumer로 용도 변경

host가 visible output 전에 review/retry를 지원하지 않으면 correction을 자동 완료했다고 주장하지 않고 `REVISION_REQUIRED`로 둔다.

## 6. 교훈

```text
EXPLICIT_REQUEST_REMOVES_PROMPT_REPETITION_NOT_CANON_CHECKS
SHOWING_ANCHOR_REQUIRES_ACTUAL_VISUAL_READBACK
NO_ANCHOR_MEANS_COMPARE_BEFORE_PRODUCTION
SELECTED_PANEL_NEEDS_STANDALONE_MASTER
CONSISTENCY_IS_SHARED_GRAMMAR_PLUS_ROLE_VARIATION
```

- 사용자의 짧은 이미지 요청은 long prompt 반복을 없애지만 Project/consumer/rights 검증을 없애지 않는다.
- current 승인 1안이 있으면 다시 새 스타일을 발명하지 않는다.
- 1안이 없으면 final production보다 비교·선택 비용이 더 싸다.
- style continuity는 이미지 유사도만이 아니라 Flow·Screen·정보 의미와 실제 gameplay scale까지 포함한다.
- 생성·승인·asset·runtime 상태를 분리해야 후속 Codex가 올바른 binary를 소비한다.

## 7. Evidence ceiling

이 사례는 Base visual process contract다. 특정 프로젝트의 Art Direction 승인, 생성 이미지 품질, Notion delivery, repository asset, runtime 적용 또는 Human/Player PASS를 증명하지 않는다.
