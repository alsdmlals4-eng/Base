# Image-Model-Only Visual Creation Policy

## Status and authority

- 상태: `ACTIVE_BASE_POLICY`
- 범위: Base를 사용하는 모든 프로젝트의 새 이미지 생성·이미지 편집·시각 후보 제작
- 대화 실행 Gate: `IMAGE_CONVERSATION_APPROVAL_GATE.md`
- 실제 소비처·필요성 Gate: `Visual Requirement Gate` / `ACTUAL_CONSUMER_REQUIRED`
- 상위 우선권: `HOST_PLATFORM_PRECEDENCE`

이 문서는 **이미지 자체가 deliverable인 작업에서 어떤 제작 수단을 사용해야 하는가**를 책임진다. 이미지가 필요한지, 어떤 프로젝트 정본을 따라야 하는지, 언제 생성 authority가 생기는지는 기존 owner가 계속 책임진다.

```text
IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING
DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED
IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

---

## 1. 이미지 생성·편집은 이미지 모델을 반드시 사용한다

`IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING`

새 이미지, 기존 이미지의 시각적 편집, concept candidate, comparison visual, screen mockup, illustration, character/environment art, icon, texture, sprite, UI art, key art처럼 **이미지 자체가 결과물인 작업은 host가 제공하는 image generation model 또는 image editing model을 반드시 사용한다.**

다음은 이미지 제작 완료가 아니다.

- prompt나 Brief만 작성한 상태
- 텍스트·표·도형만 조합한 대체 시안
- 코드로 직접 렌더링한 placeholder
- 직접 작성한 SVG/vector artwork
- image model 호출 없이 만든 mockup을 생성 결과처럼 제시하는 행위

이미지 모델을 사용했다는 사실도 실제 소비처, 품질, 프로젝트 정본 일치, 사용자 승인 또는 runtime 적합성을 자동으로 증명하지 않는다.

---

## 2. 직접 벡터·코드 드로잉으로 이미지 요청을 충족하지 않는다

`DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED`

`NO_SVG_OR_VECTOR_PATH_AS_IMAGE_GENERATION_SUBSTITUTE`

`NO_CODE_DRAWN_IMAGE_AS_IMAGE_MODEL_BYPASS`

이미지 deliverable을 만들거나 이미지 모델을 대신하기 위해 다음을 직접 작성·조립·렌더링하지 않는다.

- `SVG/XML path`, Bézier/path data, manually assembled vector shape
- Illustrator류의 수동 vector redraw를 대신하는 직접 path 제작
- `HTML/CSS/Canvas`로 그린 artwork 또는 mockup
- `Python/Pillow/Cairo/matplotlib` 등 코드 드로잉으로 만든 artwork
- `Godot draw_* / Line2D / Polygon2D / primitive drawing`으로 만든 이미지 대체물
- 텍스트·도형·gradient·clip-path를 조립해 이미지 모델 결과처럼 제시하는 산출물

이 금지는 `prototype`, `placeholder`, `임시 이미지`, `빠른 시안`, `단순 아이콘`, `작은 장식`, `최종 후보`라는 이유로 완화하지 않는다. **새 이미지가 필요하면 이미지 모델을 사용한다.**

직접 벡터·코드 드로잉 산출물을 이미지 모델이 만든 결과라고 표시하거나, 이미지 모델 호출 실패를 숨긴 채 동일한 deliverable로 승격해서도 안 된다.

---

## 3. 이미지 모델을 사용할 수 없으면 이미지 제작을 차단한다

`IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION`

이미지 생성·편집 모델 또는 승인된 host image tool을 현재 환경에서 호출할 수 없으면 다음 상태로 닫는다.

```text
BLOCKED_IMAGE_MODEL_UNAVAILABLE
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
TEXT_BRIEF_AND_REQUIREMENT_WORK_MAY_CONTINUE
```

이 상태에서도 실제 consumer, 규격, reference, Keep/Avoid/Do Not Drift, prompt, 검수 기준과 텍스트 Brief는 준비할 수 있다. 그러나 다음은 금지한다.

- 직접 SVG/vector artwork로 대체
- Python·HTML·Canvas·Godot primitive로 대신 그리기
- placeholder를 production candidate나 완료 결과로 주장
- 이미지 파일을 만들지 않았는데 이미지 제작이 완료됐다고 보고

이미지 모델이 다시 사용 가능해지기 전까지 상태는 `BLOCKED_IMAGE_MODEL_UNAVAILABLE`이며, 이미지 deliverable의 완료 수는 증가하지 않는다.

---

## 4. 허용 범위는 이미지 제작 우회 권한이 아니다

### 4.1 기존 승인 벡터 자산의 재사용

`EXISTING_APPROVED_VECTOR_ASSET_REUSE_ONLY`

이미 프로젝트에서 승인되고 출처·라이선스·consumer가 확인된 기존 SVG/vector asset을 **새로 그리지 않고 그대로 재사용·배치·연결**하는 것은 허용한다. 색·형태·path를 창작적으로 다시 그리거나 새 variant를 직접 제작하면 재사용이 아니라 새 이미지 제작이므로 이미지 모델 계약을 적용한다.

### 4.2 실제 runtime-native UI·효과 구현

`ENGINE_NATIVE_UI_AND_EFFECT_IMPLEMENTATION_IS_NOT_IMAGE_DELIVERABLE_CREATION`

Godot Control, Theme, StyleBox, shader, particle, mask, layout, primitive와 같은 엔진 기능으로 **실제 runtime UI·상태 표현·효과를 구현하는 일 자체**는 이미지 파일 제작과 구분한다. 다만 이를 캡처해 image model 대신 concept art, UI art, icon, texture, sprite 또는 승인 후보 이미지로 공급하면 우회이므로 금지한다.

### 4.3 구조 정보는 편집 가능한 형식을 유지한다

`STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE`

`TEXT_TABLE_FLOW_DB_FIRST`

Mermaid, Flow, 표, JSON, database, 문서 native diagram, 데이터 chart, 기술 diagram처럼 정확성·검색성·편집성이 중요한 production information은 기존 text-native 원칙을 유지한다. 이것은 artwork나 runtime visual asset을 직접 벡터로 제작할 권한이 아니다.

### 4.4 화면 인벤토리 용어의 한계

`PROCEDURAL_OR_ENGINE_RENDERED_IS_IMPLEMENTATION_MODE_NOT_IMAGE_CREATION_AUTHORITY`

`NO_NEW_IMAGE_FILE_REQUIRED_DOES_NOT_AUTHORIZE_NEW_VECTOR_ART`

화면 인벤토리의 `PROCEDURAL_OR_ENGINE_RENDERED`, `NO_NEW_IMAGE_FILE_REQUIRED`, `SVG` 표기는 **runtime 구현 방식 또는 기존 자산 형식**을 나타낼 수 있을 뿐, 새 SVG/vector artwork를 직접 제작하거나 이미지 모델을 우회할 authority가 아니다.

---

## 5. 최종 vector 형식이 필요한 경우에도 model-first를 지킨다

Runtime consumer나 사용자가 SVG/vector 최종 형식을 명시한 경우 다음 순서를 적용한다.

```text
IMAGE_MODEL_SOURCE_FIRST
→ EXPLICIT_VECTOR_FORMAT_REQUIREMENT
→ NON_CREATIVE_VECTORIZATION_POSTPROCESS_ONLY
→ SOURCE_RESULT_FIDELITY_READBACK_REQUIRED
```

- 시각 원본은 이미지 모델로 먼저 생성·승인한다.
- vectorization은 새 형태를 손으로 다시 그리는 창작 단계가 아니라 기술적 변환 후처리로만 수행한다.
- `NO_MANUAL_VECTOR_REDRAW`를 적용한다.
- 원본과 변환본의 실루엣, 구성, 색, 의미, 투명도, edge, 해상도/스케일 결과를 readback한다.
- 안전한 변환·검증 경로가 없으면 직접 path를 작성하지 않고 `BLOCKED_VECTOR_POSTPROCESS_UNAVAILABLE`로 둔다.

기술적 변환 결과가 원본에서 의미 있게 drift하면 자동 승인하지 않고 이미지 모델 원본 또는 변환 방식을 교정한다.

---

## 6. 기존 Gate와 승인·증거 경계를 모두 유지한다

이 정책은 다음 계약을 대체하거나 완화하지 않는다.

```text
ACTUAL_CONSUMER_REQUIRED
Visual Requirement Gate
Image Conversation Approval Gate
GENERATE_EXACTLY_ONE
STOP_REQUIRED_AFTER_GENERATION
HOST_PLATFORM_PRECEDENCE
```

- current-turn explicit request와 assistant-initiated need를 구분한다.
- 필요한 프로젝트 정본과 approved visual anchor를 먼저 확인한다.
- 한 authority에서 허용된 deliverable 수를 넘겨 자동 연속 생성하지 않는다.
- 생성 뒤 사용자의 승인·수정·폐기 결정을 받기 전에 다음 이미지로 넘어가지 않는다.
- 상위 system/developer/host tool 계약이 Base와 충돌하면 상위 계약을 우선하고 `HOST_POLICY_OVERRIDE`를 기록한다.

증거 ceiling은 다음과 같다.

```text
image generation success != user approval != PROJECT_ASSET_APPROVED != runtime integration
```

이미지 모델 호출 성공은 사용자 승인, 프로젝트 자산 승격, 저장소 반영, engine import 또는 실제 화면 검증을 의미하지 않는다.

---

## 7. 실행 판정표

| 상황 | 판정 | 다음 행동 |
|---|---|---|
| 새 이미지·편집 결과가 deliverable | 이미지 모델 필수 | 승인 Gate와 project canon을 거쳐 model generate/edit 실행 |
| 이미지 모델 사용 불가 | 차단 | Brief·consumer·규격만 준비하고 `BLOCKED_IMAGE_MODEL_UNAVAILABLE` |
| 직접 SVG/vector/path로 새 artwork 제작 | 금지 | 중단하고 이미지 모델 경로로 복귀 |
| Python/HTML/Canvas/Godot primitive로 이미지 대체 | 금지 | `NO_CODE_DRAWN_IMAGE_AS_IMAGE_MODEL_BYPASS` |
| 승인된 기존 vector를 수정 없이 runtime에 연결 | 허용 | provenance·consumer·readback 유지 |
| 실제 Godot UI/Theme/shader/VFX 구현 | 허용 | runtime evidence로 검증하되 이미지 후보 제작과 혼동 금지 |
| Mermaid/표/Flow/JSON 작성 | 허용 | `TEXT_TABLE_FLOW_DB_FIRST` 유지 |
| SVG 최종 형식이 필수 | 조건부 | image-model source first, 비창작 변환, fidelity readback |

---

## 8. 검증 체크

이미지 작업 기록과 검수에서 최소 다음을 확인한다.

- 이미지 자체가 deliverable이면 실제 image generation/editing model을 사용했는가
- 직접 SVG/XML path, vector shape 또는 code drawing으로 대체하지 않았는가
- image model unavailable 상태에서 fail closed 했는가
- 기존 vector 재사용과 새 vector authoring을 구분했는가
- runtime-native 구현을 이미지 모델 우회 산출물로 쓰지 않았는가
- vector 형식이 필요하면 model-first source와 비창작 변환 증거가 있는가
- actual consumer, Visual Requirement Gate, conversation approval, one-output, stop 규칙을 함께 지켰는가
- 생성·승인·자산 승격·runtime 통합 상태를 분리했는가

하나라도 충족하지 못하면 해당 이미지 산출물은 `REVIEW_REQUIRED`이며, 프로젝트 승인 자산 또는 runtime-ready 결과로 승격하지 않는다.
