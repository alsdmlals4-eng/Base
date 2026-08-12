# 프로젝트 생성·전달 Orchestration Guide

## 1. 목적과 권한 경계

이 Guide는 게임 프로젝트에서 **기획 완료 → 최종 검수 → 최종 시각 제작 → 프로젝트 전용 로컬 실행환경 → Codex BUILD**를 기존 Base owner 사이에서 연결하는 얇은 orchestration 계약이다.

새 광역 Skill을 만들지 않는다. 각 세부 책임의 current owner는 그대로 유지한다.

- 프로젝트 요청·범위·Decision·승인: `managing-project-intake-and-work-contract`
- Visual Requirement·필요성·우선순위·재사용: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- 이미지 프롬프트·생성·visual QA: `designing-art-prompts-and-technique-cards`
- UI/UX·Godot UI·접근성: `auditing-and-refining-ui-art`
- PC/Android 공용 코어·layout/input/lifecycle: `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- persistent Godot authoring: 현재 프로젝트가 채택한 HiGodot 계약
- deterministic GDScript test: GUT
- live QA/observability: Hera
- runtime failure diagnosis: `diagnosing-game-engine-runtime-failures`
- 공격 검토: `running-adversarial-review-and-refinement`
- 프로젝트 교훈의 Base 승격: `managing-base-change-proposals`
- 서사/연재소설 discipline: `developing-and-revising-serial-fiction`

이 문서는 위 owner의 세부 알고리즘·정본을 복제하지 않고 **진입 Gate, 종료 Gate, handoff와 project-adapter boundary**만 소유한다.

## 2. 전체 단계 Gate

프로젝트가 최종 제품용 시각 제작을 구현 전 단계로 채택한 경우 기본 순서는 다음과 같다.

```text
PLANNING_COMPLETE
→ FINAL_REVIEW_COMPLETE
→ SERIAL_VISUAL_PRODUCTION
→ VISUAL_PRODUCTION_COMPLETE
→ PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
→ CODEX_BUILD_ALLOWED
```

### 2.1 `PLANNING_COMPLETE`

- 프로젝트 정본·목표·핵심루프·시스템·콘텐츠·UI/UX·기술 제약·출시 목표를 필요한 수준까지 닫는다.
- 주요 충돌·사용자 고유 결정은 Grill Me/Decision으로 해결한다.
- 구현하지 않은 것을 구현 사실로 쓰지 않는다.

### 2.2 `FINAL_REVIEW_COMPLETE`

기획 완료 선언 뒤 다시 독립적으로 다음을 공격한다.

```text
현재 정본 재조회
→ 기능 단위 분해
→ 이미 반영됨 / 현재 유효 / 충돌·구형 / 부분 재사용 / 누락 필요 분류
→ 외부 benchmark·현업 근거 대조
→ 의존성·작업순서·보호범위 확정
→ 적대적 검토
→ 구현 Definition of Ready
```

기획을 처음 작성한 판단과 최종 검수 판단을 같은 한 번의 통과로 합치지 않는다.

### 2.3 기획 중 시각화 예외

최종 시각 생산 Gate가 있다고 해서 기획 중 시각적 사고를 금지하지 않는다.

사용자가 필요성을 승인했거나 현재 결정의 해석 위험을 줄이기 위한 제한된 기획 시각화는 `DRAFT_VISUAL`로 만들 수 있다.

`DRAFT_VISUAL`은 다음을 뜻하지 않는다.

- final product asset
- `PROJECT_ASSET_APPROVED`
- Asset Manifest 승격
- 최종 시각 생산 완료
- `CODEX_BUILD_ALLOWED`

## 3. 최종 시각 제작 — inventory/style first

프로젝트가 **user-gated** 최종 시각 제작을 채택했다면 여러 이미지를 먼저 생성한 뒤 고르는 방식보다, 실제 소비처를 조사하고 필요한 목록과 스타일을 먼저 잠근다.

```text
CURRENT_PROJECT_CANON_READBACK
→ REAL_CONSUMER_AND_SCREEN_READBACK
→ VISUAL_REQUIREMENT_GATE
→ VISUAL_ASSET_INVENTORY
→ ART_STYLE_LOCK
→ SERIAL_VISUAL_PRODUCTION
```

### 3.1 `VISUAL_ASSET_INVENTORY`

각 항목은 최소 다음을 가진다.

```yaml
visual_asset_item:
  id:
  asset_type:
  purpose:
  consumer:
  player_or_user_question:
  priority:
  dimensions_and_aspect:
  alpha_or_background:
  editable_text_policy:
  localization_impact:
  responsive_layout_impact:
  protected_identity:
  reference_rights:
  validation:
  approval_state:
```

인게임 아트, 캐릭터·환경 이미지, UI 컴포넌트 시각 요소, 아이콘, 설명 이미지, PPT/발표 시각물, 마케팅 시각물 등은 실제 사용처가 다르므로 같은 생성 규격을 자동 재사용하지 않는다.

### 3.2 `ART_STYLE_LOCK`

그림체·비주얼 방향은 형용사 목록만으로 잠그지 않는다.

```yaml
art_style_lock:
  visual_pillars:
  shape_language:
  silhouette_rules:
  color_value_contrast:
  material_and_lighting:
  line_texture_render_density:
  typography_and_iconography_boundary:
  ui_vs_ingame_shared_rules:
  crop_and_safe_composition:
  protected_identity:
  forbidden_expression:
  runtime_readability:
```

특정 상업 IP나 살아있는 작가의 식별 가능한 스타일 모사를 목표로 삼지 않는다. 레퍼런스는 기능적 원리·구도 목적·정보 위계·재질/광원 원리를 추출하는 용도로 사용하고 제품 자산은 프로젝트 고유 정본으로 다시 설계한다.

## 4. user-gated 시각 제작은 한 항목씩 닫는다

프로젝트가 이미지마다 사용자 승인을 요구하는 경우 다음 큐를 사용한다.

```text
NEXT_ASSET_BRIEF
→ GENERATION_APPROVAL
→ GENERATE_ONE_ASSET
→ VISUAL_QA
→ RESULT_APPROVAL_OR_REVISION
→ RESULT_APPROVAL_BEFORE_NEXT_ASSET
→ APPROVED_RESULT_SYNC
→ NEXT_ASSET_BRIEF
```

### 4.1 `NEXT_ASSET_BRIEF`

생성 전에 다음 한 항목만 설명한다.

- 목적·실제 사용처
- 전달해야 할 정보/감정
- 채택한 그림체/Visual Pillar
- 구도·카메라·첫 시선
- 형태·색·재질·광원
- 화면비·해상도·크롭·알파
- PC/wide/mobile landscape 사용 방식
- locale/텍스트 처리 방식
- 유지할 캐릭터·세계관·브랜드 정체성
- 금지 표현·권리 위험
- 실패 기준과 재생성 조건

### 4.2 `GENERATION_APPROVAL`

사용자가 해당 Brief의 생성 진행을 승인한 뒤에만 그 항목을 생성한다.

### 4.3 `GENERATE_ONE_ASSET`

승인된 큐에서 정확히 한 항목을 생성한다. 편의를 위해 다음 항목까지 연속 생성하지 않는다.

### 4.4 `VISUAL_QA`

생성 뒤 기존 visual owner의 계약에 따라 최소 다음을 본다.

- 프로젝트 정본과 일치하는가
- 실제 사용 크기에서 읽히는가
- PC/wide/mobile landscape crop·safe area에서 핵심 정보가 남는가
- 텍스트를 나중에 locale별로 교체할 수 있는가
- 손·관절·문자·원근·광원·로고·icon 오류가 없는가
- 구현 난이도와 asset pipeline이 현실적인가
- 원본/레퍼런스/모델/권리/유사성 경계가 남는가

### 4.5 `RESULT_APPROVAL_BEFORE_NEXT_ASSET`

사용자가 결과를 승인하거나 수정 방향을 정하기 전에는 다음 최종 항목으로 넘어가지 않는다.

수정이면 같은 항목의 Brief를 갱신하고 재생성·재검수한다. 결과 승인을 생성 승인과 같은 승인으로 간주하지 않는다.

Base는 모든 프로젝트가 사람에게 이미지마다 승인받아야 한다고 강제하지 않는다. 이 순차 계약은 **프로젝트가 user-gated visual production mode를 채택했을 때** 적용한다.

## 5. Localization-ready 설계

UI·게임 데이터·이미지·PPT·컴포넌트는 번역이 나중에 추가될 수 있다는 사실을 구현 후반에 처음 발견하지 않게 한다.

```text
PROJECT_DECLARED_LOCALE_SET
→ LOCALIZATION_READY
→ FONT_AND_LAYOUT_STRESS
→ LOCALE_CONTENT
→ LOCALE_RUNTIME_QA
```

### 5.1 `PROJECT_DECLARED_LOCALE_SET`

지원 locale은 프로젝트가 소유한다.

예를 들어 한 프로젝트가 다음을 선언할 수 있다.

```text
ko
en
ja
zh-Hans 또는 zh-Hant 또는 둘 다
```

이 값은 `PROJECT_ADAPTER_VALUE`다. **Base 전체의 고정 4개 언어 의무가 아니다.**

중국어를 지원한다고만 쓰고 `zh-Hans`·`zh-Hant` 중 무엇인지 임의로 확정하지 않는다.

### 5.2 `LOCALIZATION_READY`

초기 기획/구현부터 다음을 고려한다.

- 사용자 노출 문자열을 가능한 한 `locale key`로 분리한다.
- 번역 대상 제품 텍스트를 최종 이미지에 불필요하게 `baked-in`하지 않는다.
- 텍스트가 필요한 이미지/PPT/UI는 editable text layer나 실제 UI text component로 분리한다.
- 프로젝트 locale의 glyph coverage와 `font fallback`을 확인한다.
- CJK 줄바꿈·문장부호·숫자·단위·문맥·복수형처럼 locale별 구조 차이를 데이터/UI 계약에 반영한다.
- 버튼·탭·카드·tooltip·dialog는 긴 문자열 stress에서 clipping/overlap을 확인한다.
- pseudo/long-string 검사를 실제 번역 완료로 과장하지 않는다.
- locale별 runtime screenshot/interaction QA와 번역 품질 검수를 구분한다.

Godot spreadsheet/CSV 번역을 사용할 때는 현재 Godot 버전의 공식 문서를 다시 확인하고 valid locale tag, unique key, UTF-8 import 계약을 따른다.

## 6. PC·wide·mobile landscape Responsive Parity

“같은 UI/UX”를 모든 해상도에서 같은 픽셀 좌표로 복제한다는 뜻으로 해석하지 않는다.

프로젝트가 이 세 surface를 목표로 하면 최소 다음 profile을 선언한다.

```text
PC_STANDARD
PC_WIDE
MOBILE_LANDSCAPE
```

보존해야 할 것은 다음이다.

```text
SAME_INFORMATION_HIERARCHY_NOT_PIXEL_IDENTICAL
+ SAME_PRIMARY_ACTION_SEMANTICS
+ SAME_STATE_MEANING
+ SAME_FEEDBACK_MEANING
+ RESPONSIVE_LAYOUT_ADAPTATION
```

### 6.1 Godot 기본 원칙

- `Control`의 `anchors`와 `Container`/`containers`를 우선한다.
- 고정 좌표·고정 폭을 여러 화면비에 복제하는 방식을 기본값으로 삼지 않는다.
- 프로젝트가 승인한 base resolution, stretch mode, stretch aspect를 실제 target에서 검증한다.
- 여러 화면비를 목표로 할 때 `expand` 같은 현행 Godot 다중해상도 옵션의 의미를 현재 공식 문서로 확인한다.
- mobile의 notch·cutout·gesture 영역 등 `safe area`를 실제 target 기기에서 확인한다.

### 6.2 Profile별 검수

`PC_STANDARD`:
- keyboard/mouse/gamepad 등 선언된 입력이 핵심 행동을 완결하는가
- window resize에서 정보 위계와 modal/focus가 유지되는가

`PC_WIDE`:
- 핵심 정보가 양끝으로 과도하게 분산돼 시선 이동이 증가하지 않는가
- ultrawide에서 배경 확장과 UI anchor가 의도대로 분리되는가
- 빈 공간을 억지 정보로 채우지 않는가

`MOBILE_LANDSCAPE`:
- 핵심 버튼과 결과가 손가락·safe area에 가려지지 않는가
- PC의 hover/right-click 전용 정보에 touch 대안이 있는가
- 같은 semantic action이 touch에서도 완결되는가
- 물리적 hit target을 PC pixel size와 동일하게 강제하지 않는가

모든 profile에서 `PROJECT_DECLARED_LOCALE_SET`의 긴/짧은 문자열과 font fallback을 함께 stress한다.

## 7. 프로젝트 전용 로컬 실행환경을 먼저 확립한다

로컬 PowerShell/Codex/Godot 작업은 현재 Base의 `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`와 `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP` 계약을 재사용한다.

권장 orchestration은 다음과 같다.

```text
fresh project-scoped PowerShell
→ self-contained Godot
→ project-scoped HiGodot profile/server/ports
→ project-scoped CODEX_HOME / executor profile
→ project-adopted Hera live QA profile when needed
→ Codex in the exact project/worktree
```

### 7.1 Dedicated PowerShell 의미

전용 PowerShell은 **별도 PowerShell 설치본**을 뜻하지 않는다.

매 작업마다 fresh PowerShell process를 열고 그 프로젝트의 Godot/HiGodot/CODEX_HOME/Hera 관련 환경을 해당 process에 주입한 세션을 뜻한다.

```text
ASSUME_PREVIOUS_POWERSHELL_CLOSED
ASSUME_PREVIOUS_PROCESS_ENVIRONMENT_LOST
```

따라서 이전 shell의 `$env:*`, alias, current directory, PID, port ownership을 현재 상태 증거로 재사용하지 않는다.

전용 local environment가 없거나 깨졌다면 제품 구현보다 create/repair가 먼저다.

사용자에게 로컬 실행 지시가 필요한 경우 가능한 한 `one copy/paste` PowerShell launcher로 다음을 묶는다.

```text
현재 repo/worktree/branch 확인
→ project env 확인/생성/복구
→ self-contained Godot readiness
→ HiGodot profile/port readiness
→ project-scoped CODEX_HOME readiness
→ adopted Hera readiness when required
→ exact project directory
→ Codex launch
```

전달 전에 worktree, path quoting, port/profile collision, executable path, environment scope, stale PID/session, expected success output을 적대적으로 검토한다.

### 7.2 Hera 권한 경계

**Hera는 금지 도구가 아니다.**

프로젝트가 채택하면 실행 중 UI/게임 상태·상호작용·visual QA·관찰을 위한 `LIVE_QA_AND_OBSERVABILITY_ONLY` 역할로 적극 사용할 수 있다.

그러나 Hera 사용만으로 persistent Godot authoring authority가 바뀌었다고 간주하지 않는다. 현재 Base 계약에서 persistent authoring은 HiGodot, deterministic GDScript test는 GUT, live QA/observability는 Hera로 역할을 분리한다.

## 8. 문제 발생 시 Base 사건 사례 재사용

장애가 발생하면 무작정 다음 workaround를 추가해 원인을 숨기지 않는다.

```text
PRESERVE_EVIDENCE
→ REPRODUCE_OR_NARROW
→ BOUNDED_WORKAROUND_OR_RECOVERY
→ BASE_CASE_RECOVERY_LOOP
→ REVALIDATE
→ NEW_VERIFIED_CASE_IF_NEEDED
→ BCP_ONLY_IF_GENERALIZABLE
```

### 8.1 `BASE_CASE_RECOVERY_LOOP`

안전한 bounded workaround/복구를 시도했는데 해결되지 않거나 원인이 불명확하면 현재 Base에서 다음을 검색한다.

```text
docs/knowledge/cases/**
분야별 docs/knowledge/**/case·incident·diagnostic 자료
skills/**/LEARNING_LOG.md
skills/SKILL_LEARNING_LOG.md
[수정제안서]/**
최근 동일-goal PR/Issue와 해당 해결 evidence
```

과거 사례는 증상 문자열만 같다는 이유로 복사하지 않는다. 최소 다음을 대조한다.

- engine/tool/version
- OS/platform
- project/runtime state
- earliest failing boundary
- 실제 원인
- 적용 조건
- 비사용 조건
- 과거 해결이 현재에도 유효한지

### 8.2 새 해결 사건의 기록

Base에 없던 문제를 실제로 해결했고 재현·회귀 증거가 있다면 적절한 Case/Learning surface에 다음을 남길 수 있다.

```text
발생 문제
→ 영향과 재현 조건
→ 원인
→ 시도했으나 실패한 접근
→ 해결방법
→ 회귀/재검증
→ 교훈
→ 재사용 조건
→ 비사용 조건
```

`NEW_VERIFIED_CASE_IF_NEEDED`는 사건을 해결했다는 사실과 재사용 가능한 교훈을 보존하는 것이다. 한 프로젝트의 한 번 성공을 즉시 active Base Skill/보편 규칙으로 승격한다는 뜻이 아니다.

공용 동작 변경 가치가 있으면 `BCP_ONLY_IF_GENERALIZABLE`을 적용해 `managing-base-change-proposals`의 proposal → evidence/review/approval → 별도 implementation 생명주기를 따른다.

## 9. 서사 사건 설계 — 메시지·캐릭터 후 사건

새 사건·퀘스트·에피소드·narrative event를 발상할 때 임의의 큰 사건부터 고른 뒤 인물 동기를 사후 조작하는 실패를 줄이기 위해 다음 heuristic을 사용할 수 있다.

```text
MESSAGE_AND_CHARACTER_BEFORE_EVENT

MESSAGE_OR_QUESTION
→ CHARACTER_VALUES_WANTS_RELATIONSHIPS
→ EVENT_PRESSURE
→ CHOICE_OR_ACTION
→ CONSEQUENCE
→ AFTERMATH
```

### 9.1 `MESSAGE_OR_QUESTION`

메시지는 반드시 작가가 정답을 설교하는 문장이 아니다.

- 플레이어/독자에게 남기고 싶은 질문
- 경험시키고 싶은 감정
- 충돌시키고 싶은 가치
- 관계에서 시험하고 싶은 믿음
- 캐릭터가 스스로 드러내게 할 모순

일 수 있다.

### 9.2 `CHARACTER_VALUES_WANTS_RELATIONSHIPS`

사건에 등장할 인물을 plot utility로만 선택하지 않는다.

```yaml
character_event_seed:
  current_want:
  value_or_belief:
  fear_or_avoidance:
  relationship_pressure:
  contradiction:
  possible_choice:
  cost_or_consequence:
```

그 뒤 이 욕망·가치·관계가 행동하지 않을 수 없게 만드는 `EVENT_PRESSURE`를 설계한다.

### 9.3 실패 경계

- 멋진 사건부터 선택하고 아무 캐릭터나 배치
- 반전부터 선택하고 캐릭터 동기를 사후 변조
- 메시지는 대사로 설명하지만 행동·결과는 무관
- 모든 장면에 강제 교훈 삽입
- 사건 규모만 커지고 캐릭터 선택·관계·상태는 변하지 않음

이 heuristic은 “메시지가 gameplay/plot보다 항상 상위”라는 서열 규칙이 아니다. 사건 자체의 재미·기능·세계관 확장·플레이 압력도 보존한다.

## 10. 벤치마킹과 외부 근거

이 Guide를 적용할 때 current Base/project authority가 우선이며 외부 근거는 설계 선택을 검증하는 참고다.

### 공식/현업 참고

- Godot Multiple Resolutions: `https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html`
  - base resolution, stretch mode/aspect, 다양한 화면비와 Control layout을 현재 버전 기준으로 확인한다.
- Godot Localization using spreadsheets: `https://docs.godotengine.org/en/latest/tutorials/i18n/localization_using_spreadsheets.html`
  - locale key/CSV/import와 현재 locale 규격을 확인한다.
- Microsoft PowerShell Environment Variables: `https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables`
  - process-scoped environment와 child process inheritance를 확인한다.
- Google SRE, Postmortem Culture: `https://sre.google/sre-book/postmortem-culture/`
  - 사건의 영향·원인·해결·재발방지 action을 기록하는 학습 관점을 참고한다.
- GDC, *The System Is the Message*: `https://www.gdcvault.com/play/1020428/The-System-Is-the-Message`
- GDC, *Characterization, Purpose, and Action*: `https://www.gdcvault.com/play/1021727/Characterization-Purpose-and-Action-Creating`

외부 자료의 구체 수치·툴 버전·플랫폼 정책은 적용 시점에 current official source를 다시 확인한다.

## 11. 적대적 검토

적용 전에 최소 다음 공격 질문을 통과한다.

### phase/order
- `PLANNING_COMPLETE`를 단순 문서 존재로 착각했는가?
- final review가 기획 작성 과정과 같은 한 번의 자기확인으로 축소됐는가?
- `DRAFT_VISUAL`을 최종 자산으로 세탁했는가?
- 시각 큐가 미완료인데 편의를 위해 Codex BUILD를 먼저 시작했는가?

### visual
- asset list와 실제 consumer를 읽기 전에 생성했는가?
- user-gated인데 여러 final asset을 연속 생성했는가?
- 결과 승인 전에 다음 Brief를 생성/실행했는가?
- 승인되지 않은 후보를 Manifest/current canon으로 올렸는가?

### localization/responsive
- 프로젝트 전용 locale를 Base 보편값으로 오승격했는가?
- 중국어를 `zh-Hans`/`zh-Hant` 구분 없이 처리했는가?
- PC와 mobile에서 동일 픽셀 위치를 강제했는가?
- wide/mobile에서 정보 위계·semantic action이 달라졌는가?
- 이미지 내부 baked-in text가 번역을 막는가?

### local environment
- 이전 PowerShell PID/env/port를 현재 증거로 재사용했는가?
- project-scoped CODEX_HOME 대신 다른 프로젝트 상태를 재사용했는가?
- Hera를 금지했는가, 또는 반대로 persistent authoring authority로 과승격했는가?
- 사용자 copy/paste launcher가 다른 worktree/branch를 열 위험이 있는가?

### incident learning
- workaround가 원인 파악을 영구 대체했는가?
- Base 사례의 비사용 조건을 무시하고 증상만 보고 복제했는가?
- 해결되지 않은 사건을 success case로 기록했는가?
- 한 번의 성공을 검증 없이 active Base 규칙으로 승격했는가?

### narrative
- message-first가 강제 교훈/설교로 변질됐는가?
- 캐릭터가 바뀌어도 사건이 완전히 동일하게 작동하는가?
- 캐릭터의 욕망·가치·관계가 실제 선택/결과에 영향을 주는가?
- 사건의 규모가 의미와 캐릭터 변화를 압도하는가?

## 12. 완료 판정

이 Guide가 존재하거나 문서 계약을 통과한 것만으로 프로젝트 구현이 완료된 것은 아니다.

완료 증거는 선택된 실제 owner의 Output Contract와 프로젝트 증거를 따른다.

```text
phase gate evidence
+ approved visual queue evidence when used
+ locale/layout profile evidence
+ fresh dedicated local environment identity
+ exact project/worktree Codex/Godot evidence
+ test/runtime/human evidence as required
+ adversarial review
+ exact-head PR validation
```

실행하지 않은 사람 검증, 실기기 QA, 번역 품질 검수, Godot runtime, Hera live QA, Codex build는 각각 `NOT_RUN` 또는 `UNVERIFIED`로 남긴다.
