# Image Conversation Approval Gate

## Purpose

프로젝트용 이미지·목업·UI 시각화·캐릭터/배경/에셋 생성·편집에서 **기획 검토와 이미지 실행을 같은 대화 턴에 연속 수행하지 않도록** 하는 공용 hard conversation gate다.

이 계약은 기존 `Visual Requirement Gate`, 프로젝트 Visual Canon, 승인/자산 promotion, Notion delivery/readback 계약을 대체하지 않는다. 이미지가 정말 필요한지와 어떤 이미지를 만들지는 기존 owner가 판단하고, 이 문서는 **언제 생성 실행으로 넘어갈 수 있는가**만 책임진다.

## Machine contract

```text
PROJECT_REVIEW_COMPLETE
VISUAL_NEED_DEFINED
TEXT_BRIEF_COMPLETE
TEXT_BRIEF_STOP_REQUIRED
NEXT_USER_EXPLICIT_APPROVAL
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
NO_AUTOMATIC_IMAGE_CHAIN
```

## Required sequence

```text
프로젝트 전체 또는 현재 이미지 결정에 필요한 정본 검토
→ PROJECT_REVIEW_COMPLETE
→ Visual Need / 사용처 / 보호 요소 / 금지 drift 정의
→ 텍스트 Brief 작성
→ TEXT_BRIEF_STOP_REQUIRED

[반드시 다음 사용자 메시지]

→ NEXT_USER_EXPLICIT_APPROVAL
→ 승인된 Brief 범위의 이미지/편집 1건 실행
→ GENERATE_EXACTLY_ONE
→ 결과 제시
→ STOP_REQUIRED_AFTER_GENERATION

[다음 사용자 메시지]

→ 승인 / 수정 / 폐기 / 다음 이미지 논의
```

## TEXT_BRIEF_STOP_REQUIRED

이미지 생성/편집 전에 텍스트로 최소 다음을 합의한다.

- 어떤 프로젝트/작품인가
- 이 이미지가 어디에 쓰이는가
- 무엇을 보여줘야 하는가
- 유지해야 하는 기존 캐릭터/세계관/UI/스타일 정본
- 바꾸면 안 되는 것
- 레이아웃/화면/Flow에서의 역할
- 후보가 exploration인지 production candidate인지

Brief를 작성한 **같은 assistant 응답에서 곧바로 image generation tool을 호출하지 않는다**. Brief 제시 후 작업을 종료하고 다음 사용자 메시지를 기다린다.

## NEXT_USER_EXPLICIT_APPROVAL

다음 메시지에서 사용자가 `진행해`, `그려줘`, `이대로 만들어`, `승인`처럼 현재 Brief의 이미지 제작/편집을 명확히 승인해야 생성 단계로 이동한다.

다음은 이미지 생성 승인으로 보지 않는다.

- 이전 기획 단계에서의 포괄적 작업 승인
- Base/Notion 구조 변경 승인
- 이미지 필요성만 승인
- `좋아`, `그 방향 괜찮아`처럼 제작 실행 여부가 모호한 반응
- 과거 대화의 이미지 생성 승인

현재 대화에서 이미 명시적으로 특정 이미지 제작을 요청한 경우에도, 프로젝트 작업 정책이 이 Gate를 적용하는 범위라면 **먼저 프로젝트/정본 검토와 text brief를 마치고 한 번 종료**한다.

## GENERATE_EXACTLY_ONE

한 번의 승인 메시지는 기본적으로 **한 이미지 또는 한 편집 결과**만 생성한다.

- 한 장 안의 여러 구성요소는 하나의 합성 이미지 요구로 볼 수 있다.
- `전체 목업 1개 → 개별 요소 1개씩 → 재합성` 파이프라인에서도 각 생성 단계 사이에 사용자 채팅/승인 checkpoint를 둔다.
- 사용자가 명시적으로 여러 이미지를 한 번에 만들어 달라고 요청하더라도 프로젝트 연속 자산 제작에서는 현재 프로젝트 정책이 더 엄격하면 이 Gate를 우선한다.

## STOP_REQUIRED_AFTER_GENERATION

이미지 생성 직후:

- 결과를 사용자가 검토할 수 있게 제시한다.
- 같은 assistant turn에서 자동으로 다음 이미지/변형/개별 에셋 생성으로 넘어가지 않는다.
- 다음 사용자 메시지에서 승인·수정·폐기·다음 생성 여부를 받는다.

`NO_AUTOMATIC_IMAGE_CHAIN`은 이미지 한 장 생성 뒤 `다음 캐릭터`, `다음 포즈`, `다음 UI`, `분해 에셋`을 연속 호출하는 것을 금지한다.

## Project context requirement

이미지 작업은 현재 프로젝트의 필요한 범위를 먼저 읽는다.

```text
latest user decision
→ exact Project relation
→ project canon / current decisions
→ Home / Visual Bible / approved asset references
→ related Flow/Screen/System when relevant
→ actual implementation state when visual must match runtime
→ brief
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

이 Gate는 사용자가 명시적으로 요청한 **프로젝트 시각 자산 생성/편집**에 적용한다. 다음은 이미지 생성이 아니므로 적용하지 않는다.

- 기존 이미지에 대한 텍스트 분석/비평
- Notion에 이미 승인된 이미지를 재배치/링크하는 작업
- 이미지 없는 Flow/표/텍스트 문서 편집
- 생성 도구를 호출하지 않는 이미지 requirement inventory 작성

## Verification

작업 기록 또는 검토 시 다음을 확인한다.

- `PROJECT_REVIEW_COMPLETE` 증거가 있는가
- 생성 전 text brief가 있는가
- brief 응답과 image generation 호출이 같은 assistant turn이 아니었는가
- 다음 사용자 메시지에 `NEXT_USER_EXPLICIT_APPROVAL`이 있었는가
- 승인당 기본 생성이 `GENERATE_EXACTLY_ONE`인가
- 생성 뒤 `STOP_REQUIRED_AFTER_GENERATION`을 지켰는가
- 자동 image chain이 없었는가
- 생성/승인/Notion delivery/runtime 상태를 서로 과장하지 않았는가

위 조건을 충족하지 않으면 해당 프로젝트 이미지 작업은 `REVIEW_REQUIRED`이며, 존재하는 결과물을 자동 승인하거나 다음 생성의 근거로 사용하지 않는다.
