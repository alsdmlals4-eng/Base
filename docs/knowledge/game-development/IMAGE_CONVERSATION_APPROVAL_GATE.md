# Image Conversation Approval Gate

## Purpose

프로젝트용 이미지·목업·UI 시각화·캐릭터/배경/에셋 생성·편집에서 **사용자가 현재 이미지 출력을 직접 요청한 경우**와 **AI가 이미지 필요성을 먼저 제안한 경우**를 분리하는 Base 수준의 conversation gate다.

이 계약은 기존 `Visual Requirement Gate`, 프로젝트 Visual Canon, 승인/자산 promotion, Notion delivery/readback 계약을 대체하지 않는다. 이미지가 정말 필요한지와 어떤 이미지를 만들지는 기존 owner가 판단하고, 이 문서는 **현재 사용자 메시지가 어떤 generation authority를 제공하는가**를 책임진다.

사용자가 current turn에서 프로젝트 이미지 제작을 명시하면 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`를 적용한다.

```text
PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
```

## Host / system precedence and evidence ceiling

`HOST_PLATFORM_PRECEDENCE`

이 Gate는 Base 프로젝트 작업 규칙이며 **상위 시스템·developer·host platform 정책이나 도구 계약보다 높은 실행 권한을 가지지 않는다**. 상위 정책이 이미지 생성 시점·도구 호출·응답 형태를 다르게 요구하면 해당 상위 정책을 우선한다.

그 때문에 이 Gate의 정상 sequence를 그대로 실행할 수 없는 경우 작업 기록은 다음 상태를 명시한다.

- `HOST_POLICY_OVERRIDE` — 상위 시스템/host 정책이 Base workflow보다 우선되어 실행 순서가 달라짐
- `RUNTIME_ENFORCEMENT_NOT_GUARANTEED` — 이 정적 문서만으로 실제 host runtime 동작을 강제했다고 주장할 수 없음

이 경우에도 호환 가능한 프로젝트 정본·Visual Need·승인/자산 lifecycle·Notion delivery·evidence ceiling은 유지한다. 상위 정책을 위반해서 Base Gate를 강제하거나, host가 보장하지 않은 동작을 `PASS` 또는 runtime-enforced로 과장하지 않는다.

## Machine contract

```text
PROJECT_REVIEW_COMPLETE
VISUAL_NEED_DEFINED
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
TEXT_BRIEF_COMPLETE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
```

---

## Path A — 사용자가 현재 이미지 출력을 명시한 경우

```text
CURRENT_TURN_EXPLICIT_IMAGE_REQUEST
→ exact Project / actual consumer / current requirement resolve
→ PROJECT_REVIEW_COMPLETE
→ PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md
→ current approved visual anchor resolution
→ EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
→ GENERATE_EXACTLY_ONE
→ STOP_REQUIRED_AFTER_GENERATION
```

### Explicit request 판정

다음처럼 현재 turn의 실제 생성·편집을 명확히 요구한 경우다.

- `이미지 만들어줘`
- `그려줘`
- `이 화면을 제작해줘`
- `이 이미지에서 ○○를 바꿔줘`
- `이 Brief대로 생성해`

다음은 current-turn explicit image request가 아니다.

- 이미지가 필요한지 검토해 달라는 요청
- requirement inventory나 brief만 작성해 달라는 요청
- 기존 이미지 분석·비평·정리 요청
- 과거 대화에서의 생성 승인
- Base/Notion 구조 변경 승인

### One-output authority

```text
EXPLICIT_REQUEST_IS_ONE_OUTPUT_AUTHORITY
```

사용자의 현재 명시 요청은 별도 장문 이미지 pipeline 지시문이나 다음 turn의 중복 승인을 요구하지 않고, current request 범위의 **시각 deliverable 1건**을 실행할 authority가 된다.

그 deliverable은 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md` 판정에 따라 다음 중 하나다.

1. usable approved visual anchor가 있으면 해당 앵커를 사용한 요청 image/edit candidate 1건
2. usable approved visual anchor가 없으면 사용자가 1안을 고르기 위한 concept comparison deliverable 1건

```text
GENERATE_EXACTLY_ONE
```

- concept comparison board 하나는 deliverable 1건으로 계산한다.
- comparison board 속 panel은 각각 production asset으로 계산하지 않는다.
- current request가 여러 독립 파일을 명시하지 않았다면 다음 캐릭터·포즈·화면·variant로 자동 확장하지 않는다.
- 현재 명시 요청은 생성 결과의 사용자 승인, `PROJECT_ASSET_APPROVED`, runtime 적용을 뜻하지 않는다.

### Anchor 부재 시

usable current 1안이 없으면 final production asset을 추측하지 않는다.

```text
NO_USABLE_APPROVED_VISUAL_ANCHOR
→ GENERATE_CONCEPT_OPTION_COMPARISON
→ STOP_REQUIRED_AFTER_GENERATION
→ next user message selects one direction
```

사용자의 선택 메시지는 selected direction의 standalone anchor 제작·검수 authority가 될 수 있다. production 파생물은 standalone anchor와 project approval/readback 뒤에 진행한다.

---

## Path B — AI가 이미지 필요성을 먼저 제안한 경우

```text
ASSISTANT_INITIATED_VISUAL_NEED_RETAINS_TWO_TURN_GATE
```

사용자가 current turn에서 이미지 출력을 명시하지 않았는데 검토 중 Visual Need를 발견한 경우 기존 two-turn barrier를 유지한다.

```text
프로젝트 전체 또는 현재 이미지 결정에 필요한 정본 검토
→ PROJECT_REVIEW_COMPLETE
→ Visual Need / 사용처 / 보호 요소 / 금지 drift 정의
→ 텍스트 Brief 작성
→ TEXT_BRIEF_COMPLETE
→ TEXT_BRIEF_STOP_REQUIRED

[반드시 다음 사용자 메시지]

→ NEXT_USER_EXPLICIT_APPROVAL
→ 승인된 Brief 범위의 이미지/편집 1건 실행
→ GENERATE_EXACTLY_ONE
→ 결과 제시
→ STOP_REQUIRED_AFTER_GENERATION
```

### TEXT_BRIEF_STOP_REQUIRED

AI가 먼저 제안한 이미지 생성/편집 전에는 텍스트로 최소 다음을 합의한다.

- 어떤 프로젝트/작품인가
- 이 이미지가 어디에 쓰이는가
- 무엇을 보여줘야 하는가
- 유지해야 하는 기존 캐릭터/세계관/UI/스타일 정본
- 바꾸면 안 되는 것
- 레이아웃/화면/Flow에서의 역할
- 후보가 exploration인지 production candidate인지

Brief를 작성한 **같은 assistant 응답에서 AI가 임의로 image generation tool을 호출하지 않는다**. Brief 제시 후 작업을 종료하고 다음 사용자 메시지를 기다린다.

### NEXT_USER_EXPLICIT_APPROVAL

다음 메시지에서 사용자가 `진행해`, `그려줘`, `이대로 만들어`, `승인`처럼 방금 제시된 Brief의 이미지 제작/편집을 명확히 승인해야 생성 단계로 이동한다.

다음은 assistant-initiated Brief의 생성 승인으로 보지 않는다.

- 이전 기획 단계에서의 포괄적 작업 승인
- Base/Notion 구조 변경 승인
- 이미지 필요성만 승인
- `좋아`, `그 방향 괜찮아`처럼 제작 실행 여부가 모호한 반응
- 과거 대화의 이미지 생성 승인

---

## STOP_REQUIRED_AFTER_GENERATION

이미지 deliverable 생성 직후:

- 결과를 사용자가 검토할 수 있게 제시한다.
- 같은 assistant turn에서 자동으로 다음 이미지·독립 variant·개별 에셋 생성으로 넘어가지 않는다.
- 다음 사용자 메시지에서 승인·수정·폐기·방향 선택·다음 생성 여부를 받는다.

`NO_AUTOMATIC_IMAGE_CHAIN`은 이미지 deliverable 하나 뒤 `다음 캐릭터`, `다음 포즈`, `다음 UI`, `분해 에셋`, `다음 option set`을 자동 호출하는 것을 금지한다.

현재 승인된 deliverable의 객관적 결함 correction은 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`의 bounded correction 규칙을 따른다. host가 사용자 노출 전 내부 retry를 지원하지 않으면 visible automatic chain으로 교정하지 않고 `REVISION_REQUIRED`로 둔다.

## Project context requirement

이미지 작업은 현재 프로젝트의 필요한 범위를 먼저 읽는다.

```text
latest user decision
→ exact Project relation
→ project canon / current decisions
→ Home / Visual Bible / approved asset references
→ related Flow/Screen/System when relevant
→ actual implementation state when visual must match runtime
→ visual anchor resolution / brief
```

프로젝트 identity나 approved direction이 모호하면 `BLOCKED_UNVERIFIED` 또는 `MISSING_CANON`으로 멈춘다. 다른 프로젝트의 시각자료를 편의상 가져오지 않는다.

## Approval and asset lifecycle remain separate

```text
image generation success
!= user approval
!= PROJECT_ASSET_APPROVED
!= runtime integration
```

생성 결과는 후보일 뿐이다. 프로젝트용으로 승인되면 기존 Notion Visual Bible/Asset workflow에 첨부·상태 기록·destination readback을 수행한다. Runtime 사용이 필요하면 repository implementation과 실제 runtime evidence가 별도로 필요하다.

## Exceptions

이 Gate는 사용자가 명시적으로 요청하거나 AI가 제안한 **프로젝트 시각 자산 생성/편집**에 적용한다. 다음은 이미지 생성이 아니므로 generation checkpoint를 만들지 않는다.

- 기존 이미지에 대한 텍스트 분석/비평
- Notion에 이미 승인된 이미지를 재배치/링크하는 작업
- 이미지 없는 Flow/표/텍스트 문서 편집
- 생성 도구를 호출하지 않는 이미지 requirement inventory 작성

## Verification

작업 기록 또는 검토 시 다음을 확인한다.

- `PROJECT_REVIEW_COMPLETE` 증거가 있는가
- current-turn explicit request인지 assistant-initiated need인지 분류했는가
- explicit request이면 `PROJECT_IMAGE_REQUEST_VISUAL_ANCHOR_PIPELINE.md`로 current 1안을 확인했는가
- approved anchor를 실제로 읽고 사용자에게 surface했는가
- anchor 부재 시 comparison deliverable만 만들고 production으로 건너뛰지 않았는가
- assistant-initiated need이면 text brief와 다음-turn 승인을 지켰는가
- 한 authority당 기본 deliverable이 `GENERATE_EXACTLY_ONE`인가
- 생성 뒤 `STOP_REQUIRED_AFTER_GENERATION`을 지켰는가
- 자동 image chain이 없었는가
- 생성/승인/Notion delivery/runtime 상태를 서로 과장하지 않았는가
- host/system 우선권이 개입했다면 `HOST_POLICY_OVERRIDE`와 `RUNTIME_ENFORCEMENT_NOT_GUARANTEED`를 숨기지 않았는가

위 조건을 충족하지 않으면 해당 프로젝트 이미지 작업은 `REVIEW_REQUIRED`이며, 존재하는 결과물을 자동 승인하거나 다음 생성의 근거로 사용하지 않는다.
