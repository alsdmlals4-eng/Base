# GPT Work — 프로젝트 정본 기반 2파일 통합 제작 기획서 실행 지시문

@Superpowers @GitHub

현재 이 채팅이 연결된 프로젝트의 최신 정본과 실제 구현 상태를 기준으로, 프로젝트 전체를 재구성한 통합 제작 기획서를 완성해.

이 작업은 기존 문서를 단순 병합하거나 요약하는 작업이 아니다. 사람이 프로젝트의 핵심 경험·핵심 시스템·핵심 콘텐츠·시각 방향과 Godot 구현 원리를 한 파일에서 이해하고, 사용자 최종 승인 뒤 GPT/Codex가 후속 구현·검증을 정확히 이어갈 수 있도록 다음 산출물을 **정확히 2개**만 만든다.

1. 사용자용 상세 기획서 PDF
2. AI용 상세 기획·구현 명세 Markdown

`HUMAN_GAME_BLUEPRINT_GDD_LAYERED_PROFILE`을 적용하되 `NO_SEPARATE_BLUEPRINT_ARTIFACT`를 지켜. Blueprint는 이 두 파일의 읽기·구성 layer이며 세 번째 파일, Notion page/view, 보드, 부록이 아니다. Notion용 신규 page/database/view, DOCX, ZIP, 별도 appendix, 별도 이미지 묶음, 별도 benchmark 보고서는 만들지 마. 필요한 flow/system card, state/evidence legend, 표·traceability·benchmark·asset matrix는 두 파일 안에 통합해.

새 이미지 생성·편집은 이 지시문의 범위가 아니다. `NO_AUTOMATIC_IMAGE_GENERATION`과 `CURRENT_IMAGE_CREATION_POLICY_REQUIRED`를 적용하고, 기존 승인 이미지와 실제 build capture만 우선 사용해. 승인된 시각자료가 없으면 임의로 채우지 말고 `현재 승인 Visual 없음`과 필요한 consumer·상태·규격을 기록해. 새 image deliverable이 별도로 필요해져도 자동 생성하거나 세 번째 산출물로 추가하지 말고, 별도 사용자 명시적 요청과 현행 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`로 넘겨.

이미 저장소·연결 자료에서 확인할 수 있는 사실을 사용자에게 다시 묻지 마. 안전한 범위의 조사·정리·교정·두 문서 생성·검증·GitHub 반영은 중간 승인 없이 연속 수행하고, 정말 위험한 정본 의미 변경이나 복구 불가능한 변경만 보류해. 이 연속 수행 권한은 product implementation 실행 권한이 아니다.

### Prospective Blueprint 사전 구현 승인 Gate

`BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE`

`REQUIRED_IMAGE_AND_MATERIAL_PREPARATION`

`USER_FINAL_REVIEW_APPROVAL_REQUIRED`

`NO_IMPLEMENTATION_BEFORE_USER_FINAL_APPROVAL`

새 implementation package에는 다음 순서를 적용해.

```text
PLAN
→ REQUIRED_IMAGE_AND_MATERIAL_PREPARATION
→ BLUEPRINT_REVIEW_PUBLICATION
→ USER_FINAL_REVIEW_APPROVAL
→ IMPLEMENTATION_AUTHORIZED
```

- **PLAN**: 이 지시문의 정본 재구성·벤치마킹·ID/상태·PDF/AI 명세 작업을 Game Design Loop의 `FRAME → RESEARCH → DESIGN → SPECIFY`로 묶어. player promise와 결정 target을 frame하고, 질문에 필요한 근거만 research하고, player loop에서 system/content/UX를 design한 뒤 rule/state/acceptance/non-goal을 specify해.
- **REQUIRED_IMAGE_AND_MATERIAL_PREPARATION**: Blueprint 판단에 실제로 필요한 기존 승인 image, build capture, reference, data, audio/material과 누락 상태를 consumer별로 준비해. 새 image deliverable은 `docs/knowledge/game-development/IMAGE_CONVERSATION_APPROVAL_GATE.md`와 `docs/knowledge/game-development/IMAGE_MODEL_ONLY_VISUAL_CREATION_POLICY.md`로 넘기고, 이 지시문만으로 생성 authority를 추정하지 마. `STRUCTURED_INFORMATION_ARTIFACTS_REMAIN_TEXT_NATIVE`: Mermaid / Flow / table은 이미지 후보가 아니라 정확한 구조 정보 artifact로 유지해.
- **BLUEPRINT_REVIEW_PUBLICATION**: layered Blueprint를 정확히 두 산출물 안에 합성하고 `CREATIVE → STRUCTURAL → RULE → CONTINUITY → ADVERSARIAL → POLISH` pass를 모두 실행한 뒤 검토용 exact revision을 사용자에게 제공해.
- **USER_FINAL_REVIEW_APPROVAL**: `USER_FINAL_APPROVAL_DECISION_ID`로 `DEC-` ID를 부여하고 AI Markdown의 CONFIRMED DECISIONS에 사용자가 검토한 PDF와 AI Markdown의 branch/SHA, 승인 scope, known risk·N/A·미결정을 기록해. 프로젝트에 별도 repository Decision owner가 있으면 같은 ID로 동기화하되 새 artifact를 만들지 마. `DRAFT | INTERNAL_REVIEW | GENERATED_IMAGE | AUTOMATED_TEST | ASSISTANT_INFERENCE`는 `USER_FINAL_REVIEW_APPROVAL`이 아니야.
- **IMPLEMENTATION_AUTHORIZED**: 위 exact revision에 대한 명시적 사용자 최종 승인이 기록된 뒤에만 실제 구현 execution이나 Codex implementation package를 시작해. `TASK_BREAKDOWN_READY_IMPLEMENTATION_EXECUTION_BLOCKED`: 구현 task breakdown·dependency·acceptance는 미리 준비할 수 있지만 승인 전에는 실행하지 마.

`PROSPECTIVE_ONLY_EXISTING_IMPLEMENTATION_EVIDENCE_PRESERVED`: 이 Gate는 앞으로 시작할 구현에만 적용해. 이미 merge된 code/data/scene/test와 기존 runtime·UX evidence를 무효화하거나 상태를 낮추지 말고, 소급 backfill도 하지 마.

`PROSPECTIVE_ONLY_PREEXISTING_EXACT_USER_APPROVED_IMPLEMENTATION_AUTHORITY_PRESERVED`: Gate 채택 전에 package ID, exact scope와 artifact revision/branch/SHA에 연결된 명시적 사용자 구현 승인 기록이 있으면 `PRE_ADOPTION_USER_APPROVED_BUT_IMPLEMENTATION_NOT_STARTED`여도 그 package는 다시 승인받지 않고 실행할 수 있어. `EXACT_APPROVED_SCOPE_AND_REVISION_ONLY`: 승인 기록과 동일한 package·scope·revision만 grandfathering해. `SCOPE_EXPANSION | SUCCESSOR_PACKAGE | INFERRED_BLANKET_APPROVAL`에는 기존 authority를 적용하지 말고 이 Gate의 새 lifecycle과 사용자 최종 승인을 요구해.

## 1. 최신 정본 재구성

과거 채팅이나 memory를 current truth로 가정하지 말고 다음 순서로 fresh-read해.

1. 프로젝트 root부터 적용되는 모든 active `AGENTS.md`
2. `PROJECT_START_HERE`, `CURRENT_CONFIRMED_DECISIONS`, `ACTIVE_CONTEXT`, 최신 handoff
3. 프로젝트 GitHub latest completed `main`
4. 모든 open/draft PR과 각 PR의 정확한 역할·미병합 변경
5. 현재 코드, 씬, Resource, 데이터, import 설정, 테스트, 빌드 설정
6. 승인된 이미지·애니메이션·VFX·사운드와 실제 runtime consumer
7. 프로젝트 안의 GDD, system/content spec, Visual Bible, asset catalog, QA 문서
8. 프로젝트가 채택한 Base 규칙과 동기화된 project adapter
9. 기존 Notion에만 남은 고유 미이관 자료가 있는 경우 그 자료
10. legacy Google Sheets·HTML·Figma·기타 자료는 현재 owner에 없는 `UNIQUE` 정보 확인용으로만 사용

기존 Notion은 고유 미이관 자료가 있을 때 입력 자료로만 읽는다. 이 작업의 결과를 Notion에 신규 출력·갱신·동기화하지 말고, Notion write/readback을 완료 조건으로 두지 마. Notion-only 고유 정보가 사용되면 AI 명세의 Source Registry에 정확한 출처와 migration gap을 기록해.

`REUSE_OR_ADAPT_EXISTING_BLUEPRINT_BEFORE_NEW_REPRESENTATION`: 기존 정본에 유효한 Blueprint·flow·system representation이 있으면 먼저 재사용하고 현재 범위에 필요한 부분만 adapt해. `NO_MASS_BLUEPRINT_BACKFILL`: untouched project/system을 일괄 변환하지 말고 이번 Master GDD에서 실제로 중요한 flow/system만 두 산출물 안에 구성해.

정본 충돌을 발견하면 임의로 혼합하지 말고 다음 순서로 판정해.

```text
최신 사용자 승인
→ 프로젝트 AGENTS와 분야별 owner
→ CURRENT_CONFIRMED_DECISIONS / ACTIVE_CONTEXT / handoff
→ latest completed main의 코드·데이터·씬·테스트·runtime evidence
→ open/draft PR의 미병합 후보
→ 프로젝트가 채택한 Base 규칙
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

두 산출물에는 동일한 source branch, 기준 commit SHA, 생성일을 기록해. 작업 중 repository가 변경되면 최종 생성 직전에 source snapshot을 다시 고정하고 두 파일을 같은 시점으로 맞춰.

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

코드 덩어리를 길게 붙이는 대신 scene tree, sequence diagram, state diagram, data table, signal flow와 짧은 pseudo-code를 사용해 구조를 명확히 보여줘.

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
current authority fresh-read
→ 정본 충돌·gap 교정
→ 벤치마킹·현업 조사
→ 공통 ID registry 확정
→ AI용 Markdown 작성·repository 저장
→ 실제 코드·씬·데이터·테스트와 readback
→ 사용자용 PDF 작성
→ 두 파일 branch/SHA/ID 일치 확인
→ PDF 실제 렌더 검사
→ repository test/check
→ PR·merge·post-merge readback
→ 최종 제공
```

### 6.1 AI 문서 저장 검증

- 프로젝트 active AGENTS와 branch/PR 규칙을 따른다.
- 기존 사용자 변경과 열린 PR을 보호한다.
- 허용 범위에서는 논리 commit, PR 생성, review/check, 안전한 merge, post-merge readback까지 완료한다.
- 변경이 실제 코드·데이터 의미를 바꾸지 않는 문서 교정인지 확인한다.
- AI 명세의 path, branch, commit SHA, PR, validation result를 확보한다.
- AI 명세가 최신 main과 실제 runtime 구조를 과장하지 않는지 검사한다.

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

1. 최신 정본 누락·open PR 누락·과거 정보 혼입
2. 핵심 시스템·핵심 콘텐츠·플레이어 경험 누락
3. Godot 구현 설명의 가상 경로·불명확한 책임·데이터 owner 누락
4. 시스템↔콘텐츠↔UI↔asset/audio↔code/data/test 추적 누락
5. DOCUMENTED/IMPLEMENTED/TEST/RUNTIME/UX/RELEASE 상태 과장
6. PDF와 AI 문서 ID·source SHA drift
7. Notion 신규 출력, 불필요한 DOCX/ZIP/부록 생성, 자동 이미지 생성
8. PDF 실제 렌더·가독성·시각자료 목적 오류

새 MUST_FIX, 회귀, 정본 drift가 나오면 안전한 범위에서 즉시 교정하고 다시 검증해.

## 7. 최종 제공 방식

최종 사용자 응답에는 **사용자용 PDF만 다운로드 링크**로 제공해.

이 제공은 `BLUEPRINT_REVIEW_PUBLICATION`이며 구현 승인이 아니다. 응답에 `AWAITING_USER_FINAL_REVIEW_APPROVAL` 상태를 명시하고, 사용자가 현재 PDF와 AI Markdown exact revision을 검토한 뒤 승인·수정 요청·보류 중 하나를 명시하도록 요청해. 명시적 승인 전에는 다음 구현을 시작하거나 기존 포괄 승인에서 구현 authority를 추론하지 마.

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
→ Godot 구현 방식이 명확해진 부분
→ 실제 사용 예
→ 기대효과
→ 아직 개선되지 않은 범위
→ 사용자 결정 필요 항목
→ 다음 단일 마일스톤
→ AI 명세 path/branch/SHA/PR/validation
→ 사용자용 PDF 다운로드 링크
```

## 8. 완료 기준

다음을 모두 만족할 때까지 연속 진행해.

- 프로젝트 산출물 정확히 2개
- `BLUEPRINT_PRE_IMPLEMENTATION_REVIEW_GATE` lifecycle 순서 누락 0
- required image/material 준비 상태·consumer·approval gap 누락 0
- creative/structural/rule/continuity/adversarial/polish pass 누락 0
- exact revision의 명시적 사용자 최종 승인 전 신규 구현 execution 0
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
