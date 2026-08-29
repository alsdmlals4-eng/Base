# BCP-2026-048 · 이미지 생성 시 이미지 모델 필수 및 직접 벡터 제작 금지

## 출처와 상태

- 출처: Base를 사용하는 모든 프로젝트의 이미지 생성·편집 작업에 대한 사용자 공용 운영 결정
- 기준 Base: `2e6fa14a93ffba177b22fd7ff21e2f654ea15bb0`
- 제출일: `2026-08-29`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `명시적 사용자 승인 운영 요구 + current Base 모호성 확인 + 구현 전 계약`
- 승인 근거:
  - 사용자 메시지: `이미지 사용시 절대 벡터 이미지를 직접 그리지마말고 이미지 모델을 꼭 사용하도록 base에 명시해주고 교정작업까지 진행해줘`

## 관찰과 증거

현재 Base는 이미지 생성 전에 actual consumer, Visual Requirement Gate, 대화 내 명시적 승인, 한 번에 한 deliverable, 생성 후 중지, 승인과 runtime 승격 분리를 요구한다.

그러나 current active owner에는 다음 금지·실패 경계가 명시적으로 고정되어 있지 않다.

1. 이미지 요청을 SVG/XML path, 직접 작성한 vector shape, HTML/CSS/Canvas, Python drawing, Godot primitive drawing 등으로 대신하지 말아야 한다는 규칙
2. 이미지 생성·편집 산출물에는 host가 제공하는 image generation/editing model을 반드시 사용해야 한다는 규칙
3. 이미지 모델이 없거나 호출할 수 없을 때 직접 벡터·코드 드로잉으로 우회하지 않고 fail closed 해야 한다는 규칙
4. 화면 인벤토리의 `PROCEDURAL_OR_ENGINE_RENDERED`, `NO_NEW_IMAGE_FILE_REQUIRED`, `SVG` 같은 runtime implementation 표현이 새 이미지 제작 권한으로 오해되지 않게 하는 경계
5. 최종 형식이 SVG/vector여야 할 때도 시각 원본은 이미지 모델로 먼저 만들고 변환은 기술적 후처리로만 제한해야 한다는 경계

이 누락 때문에 이미지 모델을 사용해야 하는 요청이 직접 벡터 제작이나 코드 드로잉으로 대체될 수 있고, 사용자는 이미지 모델 결과라고 기대했지만 실제 산출 방식이 다른 drift가 발생할 수 있다.

## 일반화 후보

### 1. `IMAGE_MODEL_REQUIRED_FOR_IMAGE_CREATION_OR_EDITING`

새 이미지, 이미지 편집, concept candidate, screen mockup, illustration, character/environment art, icon, texture, sprite, UI art, key art처럼 **이미지 자체가 deliverable인 작업**은 host가 제공하는 image generation/editing model을 사용한다.

텍스트 prompt만 작성하거나 requirement를 정리한 상태는 이미지 제작 완료가 아니다.

### 2. `DIRECT_VECTOR_IMAGE_AUTHORING_PROHIBITED`

이미지 deliverable을 만들기 위해 다음을 직접 작성·합성하지 않는다.

- SVG/XML path, vector path, manually assembled vector shape
- HTML/CSS art, Canvas drawing
- Python/Pillow/Cairo/matplotlib 등으로 만든 대체 artwork
- Godot `draw_*`, Polygon2D, Line2D, primitive shape를 사용한 이미지 모델 우회 산출물
- 텍스트·도형·gradient를 조립해 이미지 생성 결과처럼 제시하는 placeholder/final candidate

직접 vector 제작을 작은 placeholder, prototype, 빠른 시안, 임시 이미지라는 이유로 허용하지 않는다. 이미지가 필요하면 이미지 모델을 사용한다.

### 3. `IMAGE_MODEL_UNAVAILABLE_BLOCKS_IMAGE_CREATION`

이미지 모델이나 승인된 image editing tool을 현재 환경에서 사용할 수 없으면 다음으로 닫는다.

```text
BLOCKED_IMAGE_MODEL_UNAVAILABLE
NO_VECTOR_OR_CODE_DRAWN_FALLBACK
```

텍스트 Brief, requirement, consumer, 규격, 검수 기준은 계속 준비할 수 있지만 이미지 산출 완료를 주장하거나 직접 벡터·코드 드로잉으로 대체하지 않는다.

### 4. runtime·정보 산출물의 좁은 비적용 경계

다음은 **이미지 deliverable을 생성하는 행위가 아닐 때만** 허용된다.

- 기존 승인·라이선스 확인된 SVG/vector asset의 재사용
- Godot Control/Theme/StyleBox/shader/particle/primitive를 사용한 실제 runtime UI·효과 구현
- Mermaid, Flow, 표, 텍스트, JSON, document-native diagram처럼 editable production information 작성
- 데이터 chart나 기술 diagram처럼 이미지 생성 모델의 artwork 대체가 목적이 아닌 구조적 표현

이 경계는 새 SVG/vector artwork를 직접 제작하거나 이미지 요청을 procedural output으로 우회할 authority가 아니다.

```text
PROCEDURAL_OR_ENGINE_RENDERED_IS_IMPLEMENTATION_MODE_NOT_IMAGE_CREATION_AUTHORITY
NO_NEW_IMAGE_FILE_REQUIRED_DOES_NOT_AUTHORIZE_NEW_VECTOR_ART
```

### 5. vector 형식이 실제로 필요한 경우

사용자가 SVG/vector 최종 형식을 명시하거나 runtime consumer가 이를 요구하더라도:

```text
IMAGE_MODEL_SOURCE_FIRST
→ explicit vector format requirement
→ non-creative conversion/vectorization post-process
→ source/result fidelity readback
```

- 시각 원본은 먼저 이미지 모델로 만든다.
- vectorization은 직접 다시 그리기가 아니라 기술적 후처리로만 수행한다.
- 원본과 변환본을 비교해 의미·형태·색·투명도 drift를 검수한다.
- 안전한 변환 경로가 없으면 직접 path를 작성하지 않고 `BLOCKED_VECTOR_POSTPROCESS_UNAVAILABLE`로 둔다.

### 6. 기존 승인·증거 경계 유지

이 규칙은 다음을 우회하지 않는다.

- `ACTUAL_CONSUMER_REQUIRED`
- `Visual Requirement Gate`
- `Image Conversation Approval Gate`
- `GENERATE_EXACTLY_ONE`
- `STOP_REQUIRED_AFTER_GENERATION`
- 사용자 승인과 project asset/runtime promotion 분리
- host/system/tool policy precedence

## 프로젝트 전용으로 남길 내용

- 프로젝트별 사용 image model과 실제 tool capability
- prompt, reference image, size, aspect ratio, alpha, format
- project visual canon과 Keep/Avoid/Do Not Drift
- SVG/vector 최종 형식 필요 여부와 import/runtime 규격
- 실제 asset path, SHA-256, manifest, engine import 설정
- 승인, 수정, 폐기, runtime 적용과 화면 검증 상태

## 적용 조건과 비사용 조건

적용:

- 사용자가 새 이미지를 그리거나 생성해 달라고 요청한 경우
- 기존 이미지의 시각 내용을 편집·복원·변형하는 경우
- 프로젝트 검토 중 승인된 이미지 deliverable을 실제 생산하는 단계
- concept comparison, mockup, runtime candidate, marketing visual 제작

비적용 또는 별도 분류:

- 이미지의 텍스트 분석·비평·요구사항 정리만 하는 경우
- 기존 승인 vector asset을 수정 없이 runtime에 연결하는 경우
- 텍스트·표·Mermaid·Flow·JSON 같은 production information 작성
- Godot의 실제 UI layout, Theme, shader, VFX 구현 자체
- source image의 시각 내용을 새로 만들지 않는 metadata·파일 이동·manifest 갱신

비적용 항목도 이미지 생성 요청의 우회 수단으로 사용하면 이 계약을 적용한다.

## 반례와 위험

- 모든 vector·procedural 기술을 금지한다고 오해하면 Godot runtime UI, shader, VFX, diagram 작성까지 불필요하게 막힌다. 금지 대상은 **이미지 deliverable의 직접 제작과 이미지 모델 우회**다.
- 기존 승인 SVG 재사용까지 금지하면 이미 검증된 자산을 다시 만들게 된다. 재사용은 허용하되 새 artwork authoring과 구분한다.
- 이미지 모델이 vector를 직접 출력하지 못할 수 있다. 이 경우 model-first source와 기술적 vectorization을 분리하고, 안전한 후처리 수단이 없으면 fail closed 한다.
- 이미지 모델 사용만으로 project canon, 소비처, 규격, 품질, 승인, runtime 적합성이 보장되지는 않는다. 기존 Gate와 검증을 유지한다.
- 문서용 Flow와 데이터 chart까지 이미지 모델로 만들면 텍스트 정확성·편집성·검색성이 떨어질 수 있다. 구조 정보는 기존 `TEXT_TABLE_FLOW_DB_FIRST`를 유지한다.

## 영향 범위와 검증

### 승인된 구현 범위

1. 이미지 모델 전용 생성·편집 계약 문서 추가
2. `IMAGE_CONVERSATION_APPROVAL_GATE.md`에서 해당 계약을 모든 generate/edit 경로의 필수 owner로 routing
3. 직접 SVG/vector/code drawing 금지, model unavailable fail-closed, runtime/information exception, model-first vector post-process를 보호하는 focused regression test 추가
4. 화면 인벤토리의 procedural/SVG 용어가 이미지 제작 authority가 아님을 새 owner에서 명시

### 제외·보호 범위

- 실제 프로젝트 이미지 생성 없음
- 기존 이미지·vector asset 수정·삭제 없음
- Godot runtime UI·shader·VFX 구현 방식의 전면 금지 없음
- Mermaid·Flow·표·JSON 작성 금지 없음
- 새 provider·dependency·paid service 추가 없음
- host/system image tool 계약 변경 없음
- 열린 다른 PR·branch는 read-only
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 기존 open PR이 소유 중이므로 이번 제안·구현에서 수정하지 않음

### TDD 검증 계획

1. focused contract test를 먼저 추가한다.
2. current main에는 새 owner와 routing token이 없으므로 RED를 확인한다.
3. 승인 범위의 최소 정책 owner와 gate routing만 추가한다.
4. focused contract와 repository CI를 GREEN으로 확인한다.
5. exact-head diff, open PR path conflict, 기존 image approval/actual-consumer/one-output/stop gate 회귀를 검토한다.
6. 최소 5회 whole-state adversarial review 후 새 blocking finding 0일 때만 merge한다.
7. squash merge 뒤 main에서 policy·routing·test readback과 CI 상태를 다시 확인한다.

## 필요한 도구·파일·권한

- 필요 항목: 기존 GitHub connector, repository write/PR/CI/merge 권한
- 필요한 이유: proposal과 implementation 분리, RED/GREEN 증거, exact-head merge, post-merge readback
- 설치·적용 방법: 새 설치 없음
- 설치 후 확인 명령: 해당 없음
- 최소 권한: Base branch 생성, 파일 작성, PR 생성, Actions read, squash merge

## 승인과 구현

- 사용자 승인 근거: 현재 대화의 명시적 Base 반영·교정 요청, `2026-08-29`
- 구현 PR: 별도 implementation PR로 생성
- 롤백: implementation PR을 squash 단위로 revert하고, proposal 기록은 이력으로 유지
