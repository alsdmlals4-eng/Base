# GPT Work — 프로젝트 정본 기반 2파일 통합 제작 기획서 실행 지시문

@Superpowers @GitHub

현재 이 채팅이 연결된 프로젝트의 최신 정본과 실제 구현 상태를 기준으로, 프로젝트 전체를 재구성한 통합 제작 기획서를 완성해.

이 작업은 기존 문서를 단순 병합하거나 요약하는 작업이 아니다. 사람이 프로젝트의 핵심 경험·핵심 시스템·핵심 콘텐츠·시각 방향과 Godot 구현 원리를 한 파일에서 이해하고, 사용자 최종 승인 뒤 GPT/Codex가 후속 구현·검증을 정확히 이어갈 수 있도록 다음 산출물을 **정확히 2개**만 만든다.

1. 사용자용 상세 기획서 PDF
2. AI용 상세 기획·구현 명세 Markdown

`HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE`을 적용하되 `NO_SEPARATE_BLUEPRINT_ARTIFACT`를 지켜. Blueprint는 이 두 파일의 읽기·구성 layer이며 세 번째 파일, Notion page/view, 보드, 부록이 아니다. Notion용 신규 page/database/view, DOCX, ZIP, 별도 appendix, 별도 이미지 묶음, 별도 benchmark 보고서는 만들지 마. 필요한 flow/system card, state/evidence legend, 표·traceability·benchmark·asset matrix는 두 파일 안에 통합해.

새 이미지 생성·편집은 무소비처·무검수 상태에서 이 지시문만으로 자동 허용되지 않는다. `NO_AUTOMATIC_IMAGE_GENERATION`과 `CURRENT_IMAGE_CREATION_POLICY_REQUIRED`를 적용하고, 기존 승인 이미지와 실제 build capture를 우선 사용해. 다만 1차 구조 Blueprint가 concrete consumer·상태·규격·일관성 경계를 확정하고, 이미 승인된 프로젝트 작업 안에서 현행 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`의 bounded candidate 조건을 충족하면 필요한 후보를 1차와 2차 Blueprint 사이에 제작·검수할 수 있다. 후보는 세 번째 프로젝트 산출물이 아니며 사용자 lock 전 정본·runtime 자산이 아니다.

이미 저장소·연결 자료에서 확인할 수 있는 사실을 사용자에게 다시 묻지 마. 안전한 범위의 조사·정리·교정·두 문서 생성·검증·GitHub 반영은 중간 승인 없이 연속 수행하고, 정말 위험한 정본 의미 변경이나 복구 불가능한 변경만 보류해. 이 연속 수행 권한은 product implementation 실행 권한이 아니다.

### Base revision fresh-read와 bounded execution

`LATEST_BASE_DISCOVERY_REQUIRED`

`PIN_IS_EVIDENCE_NOT_FRESHNESS_BYPASS`

`PROJECT_ADOPTED_BASE_CONTRACT_PRESERVED`

`BASE_DRIFT_CLASSIFICATION_REQUIRED`

`BASE_EXECUTION_SHA_PINNED_PER_BOUNDED_WORK`

`NO_PERMANENT_STALE_PIN`

`NO_FLOATING_EXECUTION`

`BOUNDARY_FRESH_READ_REQUIRED`

과거에 기록된 Base SHA만 영구 사용하거나 작업 중 이동하는 Base `main`을 계속 추종하지 마. 각 L1+ 작업 시작에서 최신 completed Base `main`을 fresh-read하고, 프로젝트가 채택한 Base 계약·project adapter·프로젝트 정본·실제 구현과 비교해 drift를 분류한 뒤 이번 bounded 작업/Slice가 실제 적용할 execution revision을 고정해.

```yaml
base_observed_head_sha:
base_adopted_contract_sha:
base_execution_sha:
base_drift_classification: NO_RELEVANT_DRIFT | COMPATIBLE_ADOPTION | MIGRATION_REQUIRED | PROJECT_OVERRIDE | BLOCKED_UNVERIFIED
```

- 최신 Base가 더 새롭다는 이유만으로 프로젝트 코어·승인 Decision·실제 구현·채택 계약을 자동 교체하지 마.
- bounded 작업 중 `base_execution_sha`를 floating ref로 바꾸지 마. 관련 Base 변경을 발견하면 impact·migration·affected consumer/test를 먼저 분류해.
- 구현 인계, pre-merge, post-merge, closeout에서 최신 Base를 다시 fresh-read하고 drift를 재분류해. 무관하면 현재 execution pin을 유지하고, 관련 있으면 reconcile과 영향 범위 재검증 뒤 새 revision을 채택해.

### Prospective Blueprint 사전 구현 승인 Gate

`BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE`

`PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH`

`BLUEPRINT_PASS_1_STRUCTURAL_DRAFT`

`STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT`

`BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`

`REQUIRED_IMAGE_AND_MATERIAL_PREPARATION`

`REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`

`BLUEPRINT_PASS_2_FINAL`

`VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`

`ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`

`USER_FINAL_REVIEW_APPROVAL_REQUIRED`

`NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL`

새 implementation package에는 다음 순서를 적용해.

```text
PLAN
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

- **PLAN**: 이 지시문의 정본 재구성·벤치마킹·ID/상태·PDF/AI 명세 작업을 Game Design Loop의 `FRAME → RESEARCH → DESIGN → SPECIFY`로 묶어. `PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH`에 따라 프로젝트 전체 material system의 지도·책임·경계·의존성은 넓게 연결하고, 현재 다음 플레이 의미 Slice만 rule/state/acceptance/consumer 수준으로 깊게 명세해.
- **BLUEPRINT_PASS_1_STRUCTURAL_DRAFT**: 이미지 제작 전에 같은 두 산출물의 working revision에서 전체 Game Flow, system 관계, state/data 처리 흐름, Screen Inventory, 최소 대표 low-fidelity wireframe, entry/exit/cancel/re-entry, target viewport/input, player question, planned/actual consumer와 필요한 state family를 먼저 정리해. `STRUCTURAL_BLUEPRINT_DRAFT_NOT_THIRD_ARTIFACT`: 이 1차 Blueprint는 세 번째 파일·정본·보드가 아니라 최종 Blueprint로 승격될 동일 owner·ID의 구조 초안이야.
- **REQUIRED_IMAGE_AND_MATERIAL_PREPARATION**: 1차 Blueprint의 `BLUEPRINT_PASS_1_ACTUAL_CONSUMER_CONTRACT`를 입력으로 기존 승인 image, build capture, reference, data, audio/material을 우선 재사용하고, 현재 Slice의 P0/P1과 반복 일관성에 필요한 일부 P2 gap만 준비해. `REQUIRED_MATERIALS_NOT_ALL_PROJECT_ASSETS`: 미래 전체 프로젝트의 화면·캐릭터·콘텐츠·P3 장식 자산을 일괄 제작하지 마. 새 image deliverable은 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`와 `docs/knowledge/game-development/IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`를 따라 bounded candidate로 다루고, `STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE`: Mermaid / Flow / table은 이미지 후보가 아니라 정확한 구조 정보 artifact로 유지해.
- **VFX preparation boundary**: `VFX_BRIEF_AND_SOURCE_BEFORE_FINAL_BLUEPRINT`로 VFX의 목적, trigger, 시작/peak/종료 timing, layer, 화면 점유, storyboard/frame intent, texture/mask/sprite source, reduced-motion 동등 경로, 성능 budget과 fallback을 준비해. `ENGINE_NATIVE_VFX_IN_GODOT_PRODUCT_BUILD`: Particle, Shader, `AnimationPlayer`, Tween, Signal/event wiring, 빠른 입력·중단·재진입, 실제 성능 측정과 runtime tuning은 최종 Blueprint 승인 뒤 Codex의 Godot 제품 구현에 남겨.
- **BLUEPRINT_REVIEW_PUBLICATION (`BLUEPRINT_PASS_2_FINAL`)**: 검수·재사용·candidate review 결과를 두 산출물의 같은 ID에 통합하고 layered Blueprint를 합성해. `CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH` pass를 모두 실행한 뒤 검토용 exact final revision을 사용자에게 제공해.
- **USER_FINAL_REVIEW_APPROVAL**: `USER_FINAL_APPROVAL_DECISION_ID`로 `DEC-` ID를 부여하고 AI Markdown의 CONFIRMED DECISIONS에 사용자가 검토한 PDF와 AI Markdown의 branch/SHA, 승인 scope, known risk·N/A·미결정을 기록해. 프로젝트에 별도 repository Decision owner가 있으면 같은 ID로 동기화하되 새 artifact를 만들지 마. `DRAFT | INTERNAL_REVIEW | GENERATED_IMAGE | AUTOMATED_TEST | ASSISTANT_INFERENCE`는 `USER_FINAL_REVIEW_APPROVAL`이 아니야.
- **IMPLEMENTATION_AUTHORIZED**: 위 `BLUEPRINT_PASS_2_FINAL` exact revision에 대한 명시적 사용자 최종 승인이 기록된 뒤에만 실제 구현 execution이나 Codex implementation package를 시작해. `TASK_BREAKDOWN_READY_IMPLEMENTATION_EXECUTION_BLOCKED`: 구현 task breakdown·dependency·acceptance는 미리 준비할 수 있지만 승인 전에는 실행하지 마.

`PROSPECTIVE_ONLY_EXISTING_IMPLEMENTATION_EVIDENCE_PRESERVED`: 이 Gate는 앞으로 시작할 구현에만 적용해. 이미 merge된 code/data/scene/test와 기존 runtime·UX evidence를 무효화하거나 상태를 낮추지 말고, 소급 backfill도 하지 마.

`PROSPECTIVE_ONLY_PREEXISTING_EXACT_USER_APPROVED_IMPLEMENTATION_AUTHORITY_PRESERVED`: Gate 채택 전에 package ID, exact scope와 artifact revision/branch/SHA에 연결된 명시적 사용자 구현 승인 기록이 있으면 `PRE_ADOPTION_USER_APPROVED_BUT_IMPLEMENTATION_NOT_STARTED`여도 그 package는 다시 승인받지 않고 실행할 수 있어. `EXACT_APPROVED_SCOPE_AND_REVISION_ONLY`: 승인 기록과 동일한 package·scope·revision만 grandfathering해. `SCOPE_EXPANSION | SUCCESSOR_PACKAGE | INFERRED_BLANKET_APPROVAL`에는 기존 authority를 적용하지 말고 이 Gate의 새 lifecycle과 사용자 최종 승인을 요구해.

## 1. 최신 정본 재구성

과거 채팅이나 memory를 current truth로 가정하지 말고 다음 순서로 fresh-read해.

1. 최신 completed Base `main`의 `AGENTS.md`, `START_HERE.md`, V4 workspace machine contract와 현재 작업 관련 Registry/owner
2. 프로젝트 root부터 적용되는 모든 active `AGENTS.md`
3. `PROJECT_START_HERE`, `CURRENT_CONFIRMED_DECISIONS`, `ACTIVE_CONTEXT`, 최신 handoff
4. 프로젝트 GitHub latest completed `main`
5. 모든 open/draft PR과 각 PR의 정확한 역할·미병합 변경
6. 현재 코드, 씬, Resource, 데이터, import 설정, 테스트, 빌드 설정
7. 승인된 이미지·애니메이션·VFX·사운드와 실제 runtime consumer
8. 프로젝트 안의 GDD, system/content spec, Visual Bible, asset catalog, QA 문서
9. 프로젝트가 채택한 Base 규칙과 동기화된 project adapter
10. 최신 Base와 채택 Base의 drift, 이번 작업의 `base_observed_head_sha` / `base_adopted_contract_sha` / `base_execution_sha`
11. 기존 Notion에만 남은 고유 미이관 자료가 있는 경우 그 자료
12. legacy Google Sheets·HTML·Figma·기타 자료는 현재 owner에 없는 `UNIQUE` 정보 확인용으로만 사용

기존 Notion은 고유 미이관 자료가 있을 때 입력 자료로만 읽는다. 이 작업의 결과를 Notion에 신규 출력·갱신·동기화하지 말고, Notion write/readback을 완료 조건으로 두지 마. Notion-only 고유 정보가 사용되면 AI 명세의 Source Registry에 정확한 출처와 migration gap을 기록해.

`REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION`: 기존 정본에 유효한 Blueprint·flow·system representation이 있으면 먼저 재사용하고 현재 범위에 필요한 부분만 adapt해. `NO_MASS_BLUEPRINT_BACKFILL`: untouched project/system을 일괄 변환하지 말고 이번 Master GDD에서 실제로 중요한 flow/system만 두 산출물 안에 구성해.

### Blueprint wireframe 결정 surface

`BLUEPRINT_WIREFRAME_DECISION_SURFACE`와 `WIREFRAME_WITHIN_EXISTING_TWO_ARTIFACTS`를 적용해. 와이어프레임은 세 번째 설계 파일·Notion view·보드·이미지 묶음이 아니라 PDF와 AI Markdown 안에서 동일한 `screen_id`를 공유하는 text-native 구조 검토 자료야.

`TWO_ARTIFACT_PROFILE_CONDITIONALLY_APPLIES`: 이 지시문은 사용자가 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD` profile을 명시적으로 선택한 경우에만 사용한다. 이 profile 밖의 프로젝트에는 두 산출물이나 이 지시문의 Blueprint 위치를 강제하지 말고, 해당 프로젝트의 현행 design-document owner를 따라.

`WIRE_FRAME_ONLY_FOR_MATERIAL_PLAYER_FACING_SURFACE`: 이번 Blueprint의 player-facing surface 중 layout, input, state 또는 navigation 결정에 실제로 필요한 것만 고른다. 각각 `screen_id`, `priority`, target viewport / aspect, input mode, entry / exit / cancel / re-entry, player goal/question, visual hierarchy, primary / secondary action, normal state, disabled / error / unavailable state, planned or actual consumer, `SCREEN_LEVEL_COMPOSITION_REQUIRED` reference, evidence reference를 기록해. 적용되지 않는 surface에는 `NOT_APPLICABLE_WITH_REASON`을 남겨.

`SMALLEST_REPRESENTATIVE_WIREFRAME_SET`: 동일 navigation/state contract의 변형 화면은 같은 wireframe를 참조하고, 현재 결정·구현·검수에 필요한 최소 대표 화면만 만든다. 모든 기존 화면의 backfill이나 장식용 wireframe는 금지한다.

`WIREFRAME_NOT_RUNTIME_OR_USER_APPROVAL_EVIDENCE`: wireframe는 `DOCUMENTED` 구조 증거일 뿐이야. 실제 capture가 없으면 runtime 상태를 `NOT_RUN`으로 쓰고, capture·자동 test·wireframe를 Human/Player·device·UX·release 승인으로 올려 쓰지 마. 구현 후에는 `GAME_SCREEN_SURFACE_INVENTORY_AND_VISUAL_ASSET_MATRIX.md`의 screen row와 runtime evidence owner를 readback해서 planned or actual consumer를 확인해.

정본 충돌을 발견하면 임의로 혼합하지 말고 다음 순서로 판정해.

```text
최신 사용자 승인
→ 프로젝트 AGENTS와 분야별 owner
→ CURRENT_CONFIRMED_DECISIONS / ACTIVE_CONTEXT / handoff
→ latest completed main의 코드·데이터·씬·테스트·runtime evidence
→ open/draft PR의 미병합 후보
→ 프로젝트가 채택한 Base 규칙
→ 최신 Base remote의 관련 drift와 검증된 migration evidence
→ 기존 Notion·legacy 자료
→ 과거 채팅·memory·추정
```

각 충돌에는 항목, 각 source의 주장, 실제 구현 현실, 최신 근거, 영향, 권장 판정, 사용자 결정 필요 여부를 남겨. 최신 근거로 안전하게 해결할 수 있으면 직접 교정하고, 플레이 의미를 바꾸는 중대한 미결정만 `USER_DECISION_REQUIRED`로 분리해.

## 2. 벤치마킹·현업 조사

현재 장르·플랫폼·규모와 실제 목표 플레이 범위에 맞춰 최신 자료를 조사해.

- 직접 경쟁작 5~8개
- 인접 장르 참고작 2~3개
- 핵심 시스템별 현업 사례
- UI/UX·온보딩·접근성 사례
- 시각 가독성·애니메이션·VFX·사운드 피드백 사례
- 경제·성장·콘텐츠 생산 구조 사례
- 성공 사례뿐 아니라 실패 사례와 사용자 불만
- 대상 플랫폼의 현재 입력·해상도·스토어·출시 관행

레퍼런스를 복사하지 말고 모든 관찰을 `ADOPT / ADAPT / REJECT`로 판정해. 각 판정에는 다음을 포함해.

- 관찰한 사실
- 우리 프로젝트에 적용할 부분
- 그대로 적용하면 안 되는 부분
- 플레이어 감정·선택·고민·보상·기억에 미치는 영향
- 차별점과 판매 포인트에 미치는 영향
- 구현 비용과 유지보수 비용
- 콘텐츠 생산 비용
- 범위·성능·접근성 위험
- 적용 방법
- 검증 방법
- 출처와 조사일

벤치마크 게임 이름만 적고 “이 게임처럼 구현”으로 끝내지 마. 입력, 규칙, 상태, 피드백, 데이터, 콘텐츠 변주, 실패·복구, 구현 제약까지 우리 프로젝트 언어로 변환해.

## 3. 공통 ID와 상태 모델

사용자용 PDF와 AI용 Markdown이 서로 추적되도록 같은 항목에 같은 고유 ID를 부여해.

```text
SYS- : 시스템
CNT- : 콘텐츠
UI-  : 화면·UI
UX-  : 사용자 흐름
AST- : 시각 에셋
AUD- : 음악·SFX·음성
DAT- : 데이터 계약
QA-  : 테스트·검증
DEC- : 결정
```

기존 ID가 있으면 재사용하고, 새 ID는 프로젝트의 명명 규칙에 맞춰 충돌 없이 만든다. 같은 개념을 PDF와 AI 문서에서 다른 이름·ID로 중복 생성하지 마.

구현 현실은 다음 상태를 분리해.

`STATE_AND_EVIDENCE_LEGEND`를 두 산출물에 넣고 각 상태의 의미, 필요한 evidence, 그 evidence 없이 주장할 수 없는 상위 상태를 설명해.

```text
DOCUMENTED
CONFIRMED
IMPLEMENTED
AUTOMATED_TEST_PASS
RUNTIME_VERIFIED
UX_VERIFIED
RELEASE_READY
```

문서화됨을 구현됨으로, 테스트 통과를 runtime 확인으로, runtime 확인을 UX 확인으로, 이미지 존재를 실제 consumer 연결 완료로 과장하지 마. 각 상태에는 가능한 경우 branch, commit SHA, 파일 경로, test run, screenshot/log/video 등 근거를 연결해.

두 산출물에는 동일한 source branch, 기준 commit SHA, 생성일을 기록해. 작업 중 repository가 변경되면 최종 생성 직전에 source snapshot을 다시 고정하고 두 파일을 같은 시점으로 맞춰. Source Registry에는 `base_observed_head_sha`, `base_adopted_contract_sha`, `base_execution_sha`, drift classification, `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT` revision과 `BLUEPRINT_PASS_2_FINAL` revision을 함께 기록해.

## 4. 사용자용 PDF

사람이 다운로드해서 읽는 최종 파일은 다음 목적을 만족해야 한다.

> 이 PDF 하나만 읽어도 게임이 무엇인지, 플레이어가 무엇을 보고 판단하고 선택하는지, 핵심 시스템과 핵심 콘텐츠가 어떻게 작동하는지, 이를 Godot에서 어떤 구조와 순서로 구현하는지, 현재 무엇이 구현·검증됐고 무엇이 남았는지 이해할 수 있어야 한다.

프로젝트 slug를 repository에서 안전하게 회수해 다음 형식으로 생성해.

```text
exports/<project-slug>_MASTER_PRODUCTION_GDD_<YYYYMMDD>.pdf
```

### 4.1 기본 목차

프로젝트에 해당하는 범위에서 다음 구조를 사용해. 해당하지 않는 장은 억지로 채우지 말고 N/A 이유를 짧게 기록해.

`CONDITIONAL_MODULE_NA_WITH_REASON`: 적용되지 않는 장·card field·시각 모듈은 빈 placeholder나 추정 내용으로 채우지 말고 `N/A — 이유`로 닫아.

00. 문서 기준, Canon Snapshot, source branch/SHA
01. 프로젝트 한눈에 보기
02. 플레이어 경험과 `FIRST_5_15_30` 첫 5·15·30분
03. Design Pillars, 차별점, 판매 포인트
04. 벤치마킹과 시장 포지셔닝
05. Core Loop / Session Loop / Meta Loop
06. 전체 Game Flow와 시스템 관계
07. 핵심 시스템 상세
08. 서브 시스템 상세
09. 핵심 콘텐츠 구조와 콘텐츠별 상세
10. 스테이지·레벨·전투·퍼즐·사건 구조
11. 세계관·서사·캐릭터·세력·관계
12. 경제·성장·보상·밸런스
13. UI/UX·입력·온보딩·접근성
14. Visual Bible·애니메이션·VFX
15. Runtime Asset Consumer
16. 사운드·음악·음성·오디오 피드백
17. Godot 구현 구조
18. 데이터·씬·노드·스크립트·신호 흐름
19. 저장·로드·플랫폼·성능 요구
20. Vertical Slice
21. 테스트와 QA
22. 현재 구현·검증 상태
23. 로드맵·위험·의존성·삭제 후보
24. 결정 기록·정본 충돌·미해결 항목
25. 용어집·출처·부록

### Layered reading/composition profile

PDF와 AI Markdown에서 같은 ID와 cross-reference를 사용해 다음 네 layer를 합성해.

| Layer token | 필수 구성 |
|---|---|
| `PROJECT_PLAYER_LAYER` | One-Page Vision, player promise/pillar, loop, `FIRST_5_15_30` |
| `SYSTEM_LAYER` | 핵심 flow/system card, choice/condition, state/data change, output/feedback, 시스템 관계 |
| `CONTENT_UX_PRESENTATION_LAYER` | content card, UX flow, UI state, visual/audio consumer와 presentation rule |
| `PRODUCTION_EVIDENCE_LAYER` | scene/node/script/data owner, 구현 순서, acceptance, test/runtime/UX evidence |

표지·목차·요약·cross-reference를 다음 읽기 순서로 실제 탐색할 수 있게 배치해.

```text
3-MINUTE PROJECT / PLAYER READ
→ 10-MINUTE SYSTEM + CONTENT / UX / PRESENTATION READ
→ DETAIL READ
→ IMPLEMENTATION READ
→ VERIFICATION READ
```

`REUSABLE_FLOW_AND_SYSTEM_CARDS`: 중요한 flow와 system은 같은 card schema를 사용해. 각 card에 ID, player purpose, trigger/input, choice/condition, state/data change, output/feedback, 연결 콘텐츠·UX, implementation owner, acceptance/evidence를 넣고 두 산출물에서 같은 의미로 재사용해.

### 4.2 핵심 시스템 표준

모든 핵심 시스템은 다음 5단 구조로 설명해.

#### 1) 왜 존재하는가

- 플레이어에게 주는 약속과 가치
- 목표 감정
- 반복해서 만드는 선택·고민
- 즉시·장기 보상
- 기억에 남아야 하는 순간
- Design Pillar와 차별점 연결
- 이 시스템이 없을 때 사라지는 경험

#### 2) 어떻게 플레이하는가

- 진입·종료 조건
- 플레이어 입력
- 핵심 규칙과 제한 규칙
- 처리 순서
- 상태와 상태 전이
- 성공·실패 조건
- 예외, 취소, 되돌리기, 복구
- 즉시 피드백과 장기 영향

#### 3) 어떤 콘텐츠가 필요한가

- 스테이지·맵·웨이브·퍼즐·사건
- 캐릭터·적·유닛·건물
- 아이템·능력·업그레이드·보상
- UI/HUD·튜토리얼·텍스트
- 이미지·애니메이션·VFX
- 음악·SFX·음성
- 밸런스·스폰·진행 데이터
- 각 consumer와 필요한 상태 전체

#### 4) 어떻게 구현하는가

코딩 경험이 적은 사람도 구조와 이유를 이해할 수 있도록 실제 예시와 도식으로 설명해.

- Godot 씬 경로와 권장 scene tree
- 주요 노드와 각각의 책임
- controller/model/view/resolver/persistence 분리
- 스크립트 경로·클래스 책임·공개 API
- Resource/JSON/Dictionary 등 데이터 형식과 데이터 소유권
- field/type/default/range/ID/reference 계약
- 상태 전이도
- signal emitter/receiver/payload/timing
- 입력 처리와 중복 입력 방지
- UI 상태와 focus/navigation
- animation/VFX/SFX trigger
- 저장·로드와 migration 영향
- 플랫폼·해상도·입력·성능 제약
- 기존 module·asset·reference 재사용 여부
- 의존성과 충돌 가능성
- 구현 순서와 각 단계의 확인 방법

코드 덩어리를 길게 붙이는 대신 scene tree, sequence diagram, state diagram, data table, signal flow와 짧은 pseudo-code를 사용해 구조를 명확히 보여줘. 권장 scene tree와 책임·공개 경계는 제시하되, 승인된 WHAT/WHY를 보존하는 더 안전한 내부 Node·함수 토폴로지는 exact repository를 fresh-read한 Codex가 결정할 수 있게 해.

#### 5) 어떻게 완료를 판단하는가

- Acceptance Criteria
- 정상 경로
- 실패·오류·경계값 경로
- GUT 또는 프로젝트 표준 자동 테스트
- integration test
- Godot 실제 실행 검증
- 화면·입력·해상도·성능 검증
- UX 이해도와 목표 감정 검증
- 필요한 screenshot/log/video evidence
- 미구현·미검증 범위

### 4.3 핵심 콘텐츠 표준

각 핵심 콘텐츠에는 최소한 다음을 기록해.

- ID, 이름, 분류, 상태
- 존재 목적과 목표 플레이어 경험
- 등장·해금·종료 조건
- 사용하는 핵심 시스템과 영향을 주는 시스템
- 규칙, 패턴, 상태, 변주, 난이도
- 카운터·실패·복구·보상
- 요구 UI, 시각 에셋, 애니메이션, VFX, 오디오
- scene/resource/data/script 구조
- 재사용 template과 콘텐츠 생산 비용
- 밸런스 변수와 튜닝 범위
- 구현 순서와 Acceptance Criteria
- 현재 구현·자동 테스트·runtime·UX 상태

적·유닛은 역할, 이동, 공격, AI 상태 머신, 카운터, 피격·사망·선택 상태를 포함하고, 스테이지는 학습 목표, 동선, 배치, trigger, 난이도 곡선, 보상, scene 구조를 포함해. 아이템·능력은 대상, 효과, stacking, duration, priority, conflict resolver, UI 표시, data schema를 포함해. 사건·퀘스트는 발생 조건, 정보 공개, 선택, 결과, 저장 상태, 재발생, 분기와 후속 영향을 포함해.

### 4.4 필수 시각자료

승인된 기존 자료와 실제 구현 증거를 우선 사용해. `TEXT_NATIVE_EXACT_DIAGRAMS`: flow/state/sequence/system 관계/data처럼 의미가 정확해야 하는 문서 도식은 `Mermaid / Flow / table`의 text-native source로 작성하고 두 산출물 안에 렌더링해.

- 승인 대표 이미지 또는 실제 플레이 화면
- One-Page Project Vision
- Core / Session / Meta Loop
- 전체 Game Flow
- 시스템 관계도와 자원 순환도
- 상태 전이도와 처리 sequence
- UX Screen Flow와 주요 wireframe
- 첫 10~30분 storyboard
- 진행·해금·난이도 구조
- 콘텐츠 관계도
- 세계·세력·인물 관계도
- Visual Bible과 asset family
- Runtime Asset/Audio Consumer Matrix
- 실제 구현 증거 화면

각 시각자료에는 목적, 설명, 관련 ID, 정본 출처, 승인 상태, 실제 consumer, 구현 상태, runtime 검증 상태를 표시해. 장식용으로 이미지를 추가하지 마.

## 5. AI용 Markdown

AI용 상세 기획·구현 명세 Markdown을 다음 경로에 저장해.

```text
docs/design/PROJECT_AI_PRODUCTION_SPEC.md
```

이 파일은 PDF 요약 복제본이 아니라 GPT/Codex가 구현·테스트·검수를 이어가는 machine-searchable 계약이다. 실제 코드·씬·Resource·데이터·테스트·runtime evidence를 대신하지는 않는다.

### 5.1 필수 구조

00. CANON SNAPSHOT
01. SOURCE REGISTRY
02. CURRENT PROJECT STATE
03. CONFIRMED DECISIONS
04. DESIGN PILLARS
05. PLAYER EXPERIENCE CONTRACT
06. CORE / SESSION / META LOOP
07. SYSTEM REGISTRY
08. SYSTEM SPECIFICATIONS
09. CONTENT REGISTRY
10. CONTENT SPECIFICATIONS
11. UI/UX AND INPUT CONTRACT
12. VISUAL ASSET CONSUMER MATRIX
13. AUDIO CONSUMER MATRIX
14. TECHNICAL ARCHITECTURE
15. DATA CONTRACTS
16. SCENE MAP
17. SCRIPT RESPONSIBILITY MAP
18. SIGNAL AND EVENT FLOW
19. STATE MACHINES
20. SAVE/LOAD CONTRACT
21. IMPLEMENTATION TRACEABILITY
22. TEST AND QA CONTRACT
23. VERTICAL SLICE DEFINITION
24. RISKS AND BLOCKERS
25. USER DECISION REQUIRED
26. IMPLEMENTATION QUEUE
27. CHANGE LOG

### 5.2 시스템·콘텐츠 machine contract

각 시스템과 콘텐츠에 다음을 구조화해.

- ID와 상태
- player contract와 목표 감정
- Design Pillar 연결
- rules / entry / exit / success / failure / exception / recovery
- states와 transition table
- input / process / output
- data field / type / default / range / owner / reference
- scene path와 node tree
- script path, class responsibility, public API
- signal/event emitter, receiver, payload, timing
- UI visible/hover/pressed/disabled/locked/warning/error 상태
- animation/VFX/SFX/audio trigger
- runtime asset consumer와 durable locator
- save/load, migration, platform, performance 영향
- dependency와 conflict
- 구현 순서
- Acceptance Criteria
- automated/unit/integration test
- Godot runtime verification
- 화면·입력·UX verification
- remaining work

### 5.3 구현 추적

다음 연결이 한 방향 링크가 아니라 양방향으로 추적되게 해.

`LAYERED_TRACEABILITY_REQUIRED`를 적용해 각 layer의 promise/card/consumer/owner/evidence 사이가 끊기지 않게 해.

```text
플레이어 경험
↔ 시스템
↔ 콘텐츠
↔ UI/UX
↔ visual/audio consumer
↔ scene/node/script/data
↔ test
↔ runtime/UX evidence
```

각 구현 항목에는 실제 repository path와 가능한 경우 source line, commit/PR, test 이름을 연결해. 구현되지 않은 항목은 존재하지 않는 경로나 가상 API를 만들지 말고 `NOT_IMPLEMENTED`로 남겨.

## 6. 생성·저장·검증

다음 순서를 지켜.

```text
latest completed Base fresh-read
→ project-adopted Base + project canon comparison
→ Base drift classification
→ base execution SHA selection and bounded pin
→ 정본 충돌·gap 교정
→ 벤치마킹·현업 조사
→ project-wide system coverage + next-Slice depth
→ BLUEPRINT_PASS_1_STRUCTURAL_DRAFT
→ required image/material/VFX-source preparation and candidate review
→ 공통 ID registry 확정
→ AI용 Markdown 작성·repository 저장
→ 실제 코드·씬·데이터·테스트와 readback
→ BLUEPRINT_REVIEW_PUBLICATION (`BLUEPRINT_PASS_2_FINAL`)
→ 두 파일 branch/SHA/ID 일치 확인
→ PDF 실제 렌더 검사
→ repository test/check
→ 사용자 최종 승인
→ implementation handoff boundary fresh-read
→ PR·merge·post-merge boundary fresh-read와 readback
→ 최종 제공
```

### 6.1 AI 문서 저장 검증

- 프로젝트 active AGENTS와 branch/PR 규칙을 따른다.
- 기존 사용자 변경과 열린 PR을 보호한다.
- 허용 범위에서는 논리 commit, PR 생성, review/check, 안전한 merge, post-merge readback까지 완료한다.
- 변경이 실제 코드·데이터 의미를 바꾸지 않는 문서 교정인지 확인한다.
- AI 명세의 path, branch, commit SHA, PR, validation result를 확보한다.
- AI 명세가 최신 main과 실제 runtime 구조를 과장하지 않는지 검사한다.
- `base_observed_head_sha`, `base_adopted_contract_sha`, `base_execution_sha`가 이동 ref가 아니라 관찰·채택·실행 의미에 맞는 exact revision인지 확인한다.

### 6.2 PDF 생성 검증

- 파일이 실제로 열리는지 확인한다.
- 목차와 페이지 번호가 올바른지 확인한다.
- 한글 font가 정상 렌더링되는지 확인한다.
- 표·도식·문장이 페이지 밖으로 잘리지 않는지 확인한다.
- 이미지 해상도와 caption을 확인한다.
- 내부 link와 cross-reference를 확인한다.
- 빈 페이지·중복 페이지·깨진 glyph를 확인한다.
- 기준 branch/SHA/생성일을 확인한다.
- 모든 페이지를 실제 page image로 렌더링해 육안 검사한다.
- PDF의 시스템·콘텐츠·구현 설명이 AI 명세와 충돌하지 않는지 확인한다.

### 6.3 적대적 검토

최소 다음 관점으로 whole-state를 반복 검토해.

Game Design Loop review는 다음 여섯 pass를 순서대로 실행하고 finding을 교정한 뒤 영향받은 규칙·example·traceability를 다시 확인해.

```text
CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH
```

1. 최신 Base·프로젝트 정본 누락, observed/adopted/execution revision 혼동, open PR 누락·과거 정보 혼입
2. 프로젝트 전체 system coverage와 다음 Slice depth 혼동, 핵심 시스템·핵심 콘텐츠·플레이어 경험 누락
3. 1차 Blueprint 전 이미지 제작, 1차·2차 Blueprint의 별도 정본화, 실제 consumer·state family 누락
4. current Slice를 넘어선 전체 asset waterfall, VFX source 준비와 Godot engine-native 구현 혼동
5. Godot 구현 설명의 가상 경로·불명확한 책임·데이터 owner 누락
6. 시스템↔콘텐츠↔UI↔asset/audio↔code/data/test 추적 누락
7. DOCUMENTED/IMPLEMENTED/TEST/RUNTIME/UX/RELEASE 상태 과장
8. PDF와 AI 문서 ID·source SHA drift
9. Notion 신규 출력, 불필요한 DOCX/ZIP/부록 생성, 자동 이미지 생성
10. PDF 실제 렌더·가독성·시각자료 목적 오류

새 MUST_FIX, 회귀, 정본 drift가 나오면 안전한 범위에서 즉시 교정하고 다시 검증해.

## 7. 최종 제공 방식

최종 사용자 응답에는 **사용자용 PDF만 다운로드 링크**로 제공해.

이 제공은 `BLUEPRINT_REVIEW_PUBLICATION`이자 `BLUEPRINT_PASS_2_FINAL`이며 구현 승인이 아니다. 응답에 `AWAITING_USER_FINAL_REVIEW_APPROVAL` 상태를 명시하고, 사용자가 현재 PDF와 AI Markdown exact revision을 검토한 뒤 승인·수정 요청·보류 중 하나를 명시하도록 요청해. 명시적 승인 전에는 다음 구현을 시작하거나 기존 포괄 승인에서 구현 authority를 추론하지 마.

AI용 Markdown은 다운로드 링크를 제공하지 말고 다음만 보고해.

- repository path
- branch
- commit SHA
- PR 번호와 상태
- validation result

DOCX, ZIP, 별도 appendix, 개별 이미지, AI Markdown 다운로드 링크, Notion 결과 링크를 추가하지 마.

최종 보고는 다음 순서로 작성해.

```text
작업 전 상태
→ 사용자용 PDF에서 개선된 기능
→ AI용 명세에서 개선된 기능
→ 핵심 시스템·핵심 콘텐츠 정리 결과
→ 1차 구조 Blueprint에서 확정한 Flow·화면·consumer
→ 이미지·VFX source·준비물 제작 결과
→ 2차 최종 Blueprint에서 확정한 구현 계약
→ Godot 구현 방식이 명확해진 부분
→ 실제 사용 예
→ 기대효과
→ 아직 개선되지 않은 범위
→ 사용자 결정 필요 항목
→ 다음 단일 마일스톤
→ Base observed/adopted/execution SHA와 drift
→ AI 명세 path/branch/SHA/PR/validation
→ 사용자용 PDF 다운로드 링크
```

## 8. 완료 기준

다음을 모두 만족할 때까지 연속 진행해.

- 프로젝트 산출물 정확히 2개
- Base 최신 completed main fresh-read, project-adopted Base drift 비교, execution SHA 선택 기록 누락 0
- 과거 SHA 영구 잠금 0, bounded 작업 중 floating latest 0
- implementation handoff·pre-merge·post-merge·closeout boundary fresh-read 누락 0
- `BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE` lifecycle 순서 누락 0
- `PROJECT_WIDE_SYSTEM_COVERAGE_SLICE_DEPTH` 누락 0
- `BLUEPRINT_PASS_1_STRUCTURAL_DRAFT → REQUIRED_IMAGE_AND_MATERIAL_PREPARATION → BLUEPRINT_PASS_2_FINAL` 의미·순서 누락 0
- 1차·2차 Blueprint를 별도 세 번째 artifact 또는 parallel canon으로 만든 사례 0
- 1차 Blueprint의 Flow·Screen Inventory·대표 wireframe·actual/planned consumer·state family 누락 0
- required image/material 준비 상태·consumer·approval gap 누락 0
- 현재 Slice를 넘어 모든 미래 project asset을 일괄 제작한 사례 0
- VFX brief/source 준비와 Godot engine-native VFX 구현 경계 혼합 0
- creative/structural/rule/continuity/adversarial/polish pass 누락 0
- exact `BLUEPRINT_PASS_2_FINAL` revision의 명시적 사용자 최종 승인 전 신규 구현 execution 0
- draft·내부 review·생성 이미지·자동 test·assistant inference를 최종 승인으로 대체한 사례 0
- 기존 구현·runtime evidence의 소급 무효화·하향 재분류 0
- `HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE`이 두 산출물 안에만 있고 별도 Blueprint artifact 0
- 3분 → 10분 → 상세 → 구현 → 검증 읽기 경로 누락 0
- four layer, `FIRST_5_15_30`, reusable flow/system card, traceability, state/evidence legend 누락 0
- 조건부 module의 빈 placeholder 0, 비적용 항목의 `N/A — 이유` 누락 0
- 기존 유효 Blueprint 재사용/adapt 누락 0, untouched 범위 mass backfill 0
- 최신 정본·open/draft PR·실제 구현 source 누락 0
- 미표시 정본 충돌 0
- 핵심 시스템 누락 0
- 핵심 콘텐츠 누락 0
- 시스템·콘텐츠별 플레이어 감정·선택·보상 설명 누락 0
- 시스템·콘텐츠별 Godot 씬·노드·스크립트·데이터·신호·상태·저장·테스트 설명 누락 0
- 시스템↔콘텐츠↔UI↔asset/audio↔implementation↔test 추적 누락 0
- 목적 없는 시각자료 0
- 승인되지 않은 신규 이미지 생성 0
- 근거 없는 구현·runtime·UX·release 완료 주장 0
- PDF와 AI 문서 ID 불일치 0
- PDF와 AI 문서 source branch/SHA 불일치 0
- Notion 신규 출력·갱신·동기화 0
- DOCX·ZIP·별도 appendix·별도 이미지 묶음 0
- PDF 렌더·표·이미지·font·link 오류 0
- repository validation 실패 0
- 신규 MUST_FIX 0
- 정본 drift 0
- 검증 가능한 이 문서 생성 작업의 남은 작업 0

## 9. 기존 Blueprint 증분 수정과 통합 작업 현황 실행

`EXISTING_BLUEPRINT_INCREMENTAL_REVISION_REQUIRED`

`NO_BLANK_REBUILD_WHEN_VALID_PREDECESSOR_EXISTS`

`PREDECESSOR_BLUEPRINT_AND_SOURCE_INVENTORY`

`STABLE_ID_SECTION_AND_EVIDENCE_PRESERVATION`

`SEMANTIC_DELTA_AND_CARRY_FORWARD_REQUIRED`

`UNEXPLAINED_REMOVAL_OR_STATUS_DOWNGRADE_FORBIDDEN`

`BLUEPRINT_LOSS_REGRESSION_GATE`

`PREDECESSOR_UNAVAILABLE_BLOCKED_UNVERIFIED`

### 9.1 시작 전에 predecessor를 고정해

기존 Blueprint가 있으면 새 문서를 빈 상태에서 다시 만들지 마. 다음을 predecessor set으로 fresh-read하고 exact locator를 기록해.

1. latest valid 사람용 Blueprint PDF
2. 해당 PDF를 만든 source branch/SHA와 source document
3. 현재 `docs/design/PROJECT_AI_PRODUCTION_SPEC.md`
4. 승인 Decision·Active Context·handoff
5. 실제 code/data/scene/resource/asset/test/runtime evidence
6. Library·legacy source에만 남은 고유 자료가 있을 때 그 자료

최소 receipt:

```yaml
predecessor_blueprint_ref:
predecessor_source_commit:
revision_mode: INCREMENTAL_WHEN_VALID_PREDECESSOR_EXISTS
work_status_snapshot_at:
```

PDF와 source를 실제로 읽어 project/goal/system/content/UI/UX/asset/audio/data/QA/decision ID, section anchor, flow/system/content card, diagram source, 승인 visual, consumer, evidence, blocker와 known risk를 inventory해. 파일명이 같거나 오래됐다는 이유로 predecessor를 추정하지 마.

### 9.2 기존 Blueprint를 직접 수정해

기존 source가 있으면 그 source와 stable ID를 기준으로 touched section만 수정하고 untouched content는 carry-forward해. 다음을 기본 보존해.

- 기존 확정 내용과 사용자 승인 결정
- 시스템·콘텐츠·화면·에셋·QA ID와 cross-reference
- 상세 설명, 수치, 예외, 용어집과 N/A 이유
- flow/state/sequence/system diagram의 text-native source
- 승인 이미지, caption, provenance, actual consumer와 상태군
- Godot scene/node/script/data owner와 공개 경계
- test/runtime/UX/user approval evidence와 evidence ceiling
- blocker, resume condition, 다음 안전 작업과 변경 이력

새 레이아웃이나 더 짧은 문장을 만들기 위해 의미 있는 기존 내용을 버리지 마. ID rename·split·merge는 predecessor↔successor mapping과 migration 영향이 있을 때만 허용해.

정말 valid predecessor가 없을 때만 `INITIAL_CREATION_NO_VALID_PREDECESSOR`를 사용하고, 기존 PDF·repository design docs·Library/legacy source 검색 결과를 근거로 남겨. 최초 발행 뒤 모든 갱신은 증분 수정으로 전환해.

### 9.3 Blueprint 안에 PM 현황을 통합해

별도 HTML, PM PDF, board snapshot 또는 세 번째 상태 문서를 만들지 마. 현재 repository owner와 `project_work_kanban`에서 다음 View를 같은 사람용 Blueprint PDF에 투영해.

- `PROJECT_GOAL_STATUS_SUMMARY`: 프로젝트 목표, 현재 Slice, 완료/적용 목표, 진행 중, 검증 대기, blocker, 사용자 결정, 다음 안전 작업
- `GOAL_LEVEL_CHECKLIST`: 목표별 player value, Acceptance, 관련 system/work item, 상태·evidence·blocker·next action
- `SYSTEM_LEVEL_CHECKLIST`: 시스템별 목적, 입력·출력, owner·consumer·dependency, 기획·데이터·자산·구현·검증 상태
- `CASE_LEVEL_STATUS_MATRIX`: 필요한 정상·경계·실패·충돌·중단·복구·저장·UI·접근성·성능 case별 현황
- `BLOCKERS_DECISIONS_AND_NEXT_SAFE_ACTION`: 실제 blocker, decision packet, resume condition, 현재 작업과 다음 단일 작업

목표→시스템→케이스→work item→evidence를 stable ID로 양방향 추적해. 프로젝트가 이미 같은 의미의 ID/field를 사용하면 그것을 재사용하고 Base 명칭을 중복 생성하지 마.

완료 수에는 evidence-backed PASS/DONE만 포함하고 `NOT_APPLICABLE`은 이유와 함께 분모에서 제외해. 다음 상태를 한 퍼센트나 하나의 완료 표시로 합치지 마.

```text
DOCUMENTED
IMPLEMENTED
AUTOMATED_TEST_PASS
RUNTIME_VERIFIED
UX_VERIFIED
USER_APPROVED
```

### 9.4 semantic delta와 loss-regression 검사를 실행해

successor 발행 전에 predecessor와 successor inventory를 비교해.

```yaml
predecessor_inventory:
successor_inventory:
semantic_delta_summary:
removal_or_downgrade_justifications:
```

각 추가·변경·삭제·대체·rename·상태 하향에 source, 이유, 영향받는 ID/consumer/evidence, replacement 또는 rollback을 기록해. 그대로 유지한 묶음은 `CARRIED_FORWARD_UNCHANGED`와 source locator로 요약할 수 있어.

다음 중 하나라도 설명 없이 발생하면 `BLUEPRINT_LOSS_REGRESSION_GATE`를 FAIL로 처리하고 predecessor를 보존한 채 successor 승격을 중단해.

- stable ID 또는 section/card가 사라짐
- 확정 규칙·상세 설명·예외·용어가 사라짐
- diagram source·승인 이미지·caption·provenance가 사라짐
- actual consumer·repository path·test/runtime/UX evidence가 사라짐
- 구현·검증·사용자 승인 상태가 낮아짐
- 목표→시스템→케이스→evidence 연결이 끊김
- PDF와 AI Markdown의 source SHA·ID·semantic delta가 다름
- page render 또는 text extraction에서 잘림·누락·빈 페이지·깨진 glyph가 생김

기존 predecessor나 source를 신뢰성 있게 읽을 수 없으면 채팅 기억으로 복원하지 마. 누락 locator, 영향받는 범위, 복구 경로를 기록하고 `BLOCKED_UNVERIFIED`로 둬. 읽을 수 있는 부분만 안전하게 수정할 수 있다면 touched scope와 evidence ceiling을 제한해서 명시해.

### 9.5 생성 순서에 증분 Gate를 삽입해

기존 Section 6 순서에 다음 단계를 결합해.

```text
predecessor discovery and exact source pin
→ predecessor Blueprint/source/ID/evidence inventory
→ repository canon and current work-status reconciliation
→ touched-scope incremental source revision
→ project goal/system/case progress projection
→ required image/material preparation and final Blueprint composition
→ successor inventory and semantic delta
→ BLUEPRINT_LOSS_REGRESSION_GATE
→ PDF render/page inspection/text readback
→ AI Markdown/source SHA/ID/delta cross-check
→ exact-head repository validation
→ user final review
```

최종 보고에는 predecessor ref/source SHA, revision mode, semantic delta, 삭제·상태 하향 정당화, carry-forward 범위, PM snapshot 시각과 loss-regression 결과를 추가해. 이 규칙은 `NO_SEPARATE_BLUEPRINT_ARTIFACT`, `NO_MASS_BLUEPRINT_BACKFILL`, `RUNTIME_TRUTH_SEPARATE`, 이미지 승인 경계와 사용자 최종 승인 Gate를 그대로 유지해.

<!-- FEDERATED_DUAL_CANON_ROUTE -->

> V4 authority route: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON` owns editable structured, execution, runtime, work-status, and evidence facts. Only a `USER_APPROVED_AND_MANIFEST_REGISTERED` `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` owns the immutable human visual/review baseline. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON` and PDF annotations do not mutate repository-owned facts. See `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` and `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
