# Project Creation & Delivery Orchestration Design

**Date:** 2026-08-12 KST
**Status:** USER-APPROVED DESIGN / IMPLEMENTATION ACTIVE
**Baseline:** `aa45a7589cede16be027b55f15ea4813681df8e3`
**Product decision change:** `false`

## Goal

프로젝트의 기획·최종 검수·시각 자산 생산·Codex 구현 사이 순서를 명확히 하고, 현지화·반응형 UI·프로젝트 전용 로컬 실행환경·사건/장애 학습·서사 사건 설계를 기존 Base owner와 충돌 없이 한 단계에서 조율한다.

이 변경은 새 광역 Skill을 만들지 않는다. 실행 책임은 현재 owner가 유지하고, 새 Guide는 **cross-owner orchestration only**를 소유한다.

## Existing Solution First

현재 Base에는 이미 다음 owner가 있다.

- 시각 자산 필요성·우선순위: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 `Visual Requirement Gate`
- 이미지 프롬프트·생성·검수: `designing-art-prompts-and-technique-cards`
- UI/UX: `auditing-and-refining-ui-art`
- PC/Android 배치·입력·출시: `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- Godot persistent authoring: HiGodot
- deterministic GDScript tests: GUT
- live QA/observability: Hera
- 프로젝트 전용 로컬 실행환경: `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST` / `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`
- 런타임 장애: `diagnosing-game-engine-runtime-failures`
- 공용 학습 승격: `managing-base-change-proposals`
- 서사/연재소설: `developing-and-revising-serial-fiction`
- 공격 검토: `running-adversarial-review-and-refinement`

따라서 새 Guide는 세부 알고리즘을 복제하지 않고 **owner 사이의 진입/종료 Gate와 project-adapter boundary**만 정의한다.

## Generic orchestration

```text
PLANNING_COMPLETE
→ FINAL_REVIEW_COMPLETE
→ SERIAL_VISUAL_PRODUCTION when the project requires user-gated final visual production
→ VISUAL_PRODUCTION_COMPLETE
→ PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
→ CODEX_BUILD_ALLOWED
```

기획 단계의 탐색 시각화는 명시된 `DRAFT_VISUAL`일 수 있지만 최종 자산 생산 완료나 BUILD 승인으로 승격하지 않는다.

## Visual production coordination

최종 제품용 시각 생산에 user-gated workflow를 채택한 프로젝트는 먼저 다음을 잠근다.

```text
VISUAL_ASSET_INVENTORY
+ ART_STYLE_LOCK
```

그 뒤 생산 큐는 다음을 사용한다.

```text
NEXT_ASSET_BRIEF
→ GENERATION_APPROVAL
→ GENERATE_ONE_ASSET
→ VISUAL_QA
→ RESULT_APPROVAL_OR_REVISION
→ RESULT_APPROVAL_BEFORE_NEXT_ASSET
```

Base는 모든 프로젝트가 사람에게 이미지마다 승인받아야 한다고 강제하지 않는다. **해당 approval mode를 프로젝트가 채택했을 때** 순차성·승인 경계를 보존한다.

## Localization-ready coordination

Base 공용 원칙은 `PROJECT_DECLARED_LOCALE_SET`을 초기에 선언하고 다음을 준비하는 것이다.

- locale key 기반 문자열 분리
- 이미지에 번역 대상 제품 텍스트 baked-in 금지 또는 editable layer 분리
- font glyph/fallback coverage
- 긴 문자열·CJK 줄바꿈·문장부호·숫자/단위 stress
- locale별 실제 QA 증거와 pseudo/stress evidence 구분

한국어·영어·일본어·중국어 최소 4언어는 현재 소비 프로젝트의 adapter 값이며 Base 전체의 보편 강제값으로 승격하지 않는다. 중국어는 `zh-Hans`, `zh-Hant`, 또는 둘 다 중 프로젝트가 명시한다.

## Responsive layout coordination

프로젝트가 PC·wide·mobile landscape를 목표로 할 때 다음을 보존한다.

```text
SAME_INFORMATION_HIERARCHY_NOT_PIXEL_IDENTICAL
SAME_PRIMARY_ACTION_SEMANTICS
SAME_STATE_MEANING
RESPONSIVE_LAYOUT_ADAPTATION
```

정확한 해상도는 프로젝트가 소유한다. Godot 공식 Multiple Resolutions 계약의 base resolution, `canvas_items`, `expand`, anchors/containers를 현재 버전에서 재확인하고, wide/ultrawide·mobile landscape·safe area·input·locale stress를 실제 target matrix에서 확인한다.

## Dedicated local execution coordination

새 Guide는 기존 Base 계약을 재사용한다.

```text
fresh project-scoped PowerShell
→ dedicated/self-contained Godot
→ project-scoped HiGodot profile/server/ports
→ project-scoped CODEX_HOME/executor profile
→ project-adopted Hera live-QA profile when required
→ Codex in exact project/worktree
```

`dedicated PowerShell`은 별도 PowerShell binary가 아니라 fresh process에 프로젝트 환경을 주입한 세션이다. 이전 shell이 닫혔다고 가정한다. 필요한 경우 create/repair가 product work보다 먼저이며, 사용자 handoff는 one-shot copy/paste launcher를 우선한다.

Hera는 금지 대상이 아니다. 현재 Base 채택 경계에서 live QA/observability로 사용하며 persistent Godot authoring authority는 HiGodot이 유지한다.

## Incident/case recovery coordination

```text
PRESERVE_EVIDENCE
→ REPRODUCE_OR_NARROW
→ BOUNDED_WORKAROUND_OR_RECOVERY
→ BASE_CASE_RECOVERY_LOOP
→ REVALIDATE
→ NEW_VERIFIED_CASE_IF_NEEDED
→ BCP_ONLY_IF_GENERALIZABLE
```

Base Case, 분야별 Learning Log, `skills/SKILL_LEARNING_LOG.md`, `[수정제안서]/**`, 최근 동일-goal PR/Issue를 검색한다. 증상 문자열만 비슷한 사례를 복사하지 않고 환경·원인·적용/비사용 조건을 대조한다.

새 해결은 재현·원인·실패 접근·해결·회귀·교훈·재사용/비사용 조건을 갖춘 Case가 될 수 있다. 한 번의 성공을 바로 활성 Skill/공용 규칙으로 만들지 않고, 공용화가 필요하면 BCP 생명주기를 사용한다.

## Narrative event ideation coordination

서사 사건 아이디어는 다음 heuristic을 제공한다.

```text
MESSAGE_AND_CHARACTER_BEFORE_EVENT
MESSAGE_OR_QUESTION
→ CHARACTER_VALUES_WANTS_RELATIONSHIPS
→ EVENT_PRESSURE
→ CHOICE_OR_ACTION
→ CONSEQUENCE
→ AFTERMATH
```

`MESSAGE_OR_QUESTION`은 강제 교훈이 아니라 질문·감정·가치 충돌·경험일 수 있다. 모든 장면을 교훈적으로 만들지 않으며, 사건/퀘스트/게임플레이 기능도 보존한다. 목적은 임의 사건을 먼저 고르고 캐릭터 동기를 사후 조작하는 실패를 줄이는 것이다.

## External benchmark

- Godot Multiple Resolutions: https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html
- Godot Localization using spreadsheets: https://docs.godotengine.org/en/latest/tutorials/i18n/localization_using_spreadsheets.html
- Microsoft PowerShell environment variables: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables
- Google SRE Postmortem Culture: https://sre.google/sre-book/postmortem-culture/
- GDC, The System Is the Message: https://www.gdcvault.com/play/1020428/The-System-Is-the-Message
- GDC, Characterization, Purpose, and Action: https://www.gdcvault.com/play/1021727/Characterization-Purpose-and-Action-Creating

외부 근거는 Base/project authority를 대체하지 않는다.

## Adversarial review targets

- 프로젝트 고유 4개 locale을 Base 전체 의무로 오승격하는가
- 동일 UI를 동일 픽셀 좌표로 오해해 ultrawide/mobile을 깨는가
- final visual gate가 유용한 planning visualization까지 금지하는가
- 새 Guide가 art/UI/runtime/narrative Skill의 세부 책임을 복제하는가
- Hera 사용을 금지하거나 반대로 persistent authoring authority로 오승격하는가
- incident workaround를 무한 우회 또는 원인 미확인 성공으로 세탁하는가
- 새 Case 1건을 즉시 활성 Base 규칙으로 승격하는가
- message-first가 강제 교훈·작가 설교로 변질되는가
- 기존 Open/Draft PR과 파일 충돌하는가

## Acceptance

Focused RED→GREEN은 최소 다음을 증명한다.

- new orchestration Guide가 없으면 RED;
- Game Development README one-hop route가 없으면 RED;
- `PLANNING_COMPLETE → FINAL_REVIEW_COMPLETE → SERIAL_VISUAL_PRODUCTION → CODEX_BUILD_ALLOWED` 경계 존재;
- user-gated visual queue의 inventory/style/one-at-a-time result approval 존재;
- generic locale-set readiness와 project-specific locale boundary 존재;
- PC/wide/mobile-landscape responsive semantic parity 존재;
- existing dedicated local execution contract와 Hera role을 재사용;
- Base Case/Learning/BCP recovery loop 존재;
- `MESSAGE_AND_CHARACTER_BEFORE_EVENT` heuristic 존재;
- 새 broad Skill 없음;
- exact PR head CI와 adversarial review 통과;
- merge 뒤 new main readback과 remaining PR recheck.

## Current PR concurrency

작업 시작 시 Draft PR #301은 `PERIODIC_EXTERNAL_SOURCE_DISCOVERY_SEEDS.md`와 해당 전용 테스트만 변경한다. 이번 변경과 직접 파일 중복은 없으나, main이 먼저 움직이면 current main 위에서 재검증 후 병합한다.
