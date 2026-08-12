# BCP-2026-026 — Project Creation & Delivery Orchestration

## 출처와 상태

```yaml
proposal_id: BCP-2026-026-project-creation-delivery-orchestration
status: SUBMITTED
source_project: "base 업뎃 / PROJECT_TOTAL_PLANNING_IMPLEMENTATION_AND_DELIVERY_INSTRUCTION_v4.6.md"
source_artifact_sha256: 6875473193259cfb126cc5d8b9e682decb7c47d57fdadda510e0e34c182e65a7
base_extraction_baseline: 1b34ad02d442ab8cfd47db8a2202defc6b13c65f
submitted_at: 2026-08-12
approval_ref: null
implementation_pr: null
prototype_pr: 302
prototype_pr_state: CLOSED_UNMERGED_GOVERNANCE_SUPERSEDED
```

이 제안은 프로젝트 작업지시문 v4.6에서 확정된 운영 요구를 Base 공용 후보로 추출한 것이다.

PR #302에서 공용 Guide/Test/Workflow의 RED→GREEN prototype을 만들었으나, 적대적 검토에서 현행 `managing-base-change-proposals`의 **proposal-only → 승인 → 별도 implementation** 경계와 충돌하는 것을 발견했다. 따라서 #302는 병합하지 않고 닫았으며, 그 결과는 구현 사실이 아니라 pre-approval design/test evidence로만 사용한다.

## 관찰과 증거

### 1. 프로젝트 운영에서 발견된 결합 문제

프로젝트 작업에는 다음 단계가 서로 다른 owner에 흩어져 있다.

```text
기획 완료
→ 최종 검수
→ 최종 시각 자산 제작
→ 전용 로컬 실행환경 준비
→ Codex/Godot 구현
```

Base에는 각 세부 owner가 이미 존재하지만, 프로젝트 수준에서 이 단계들의 **handoff 순서와 완료 Gate**를 한 곳에서 조율하는 공용 얇은 계약은 충분히 명시되어 있지 않다.

현재 확인한 owner:

- Visual Requirement·Art Direction: `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- 이미지 프롬프트·생성·visual QA: `designing-art-prompts-and-technique-cards`
- UI/UX: `auditing-and-refining-ui-art`
- PC/Android layout/input/lifecycle: `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- 프로젝트 전용 로컬 실행환경: `PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST`, `ONE_SHOT_LOCAL_EXECUTOR_BOOTSTRAP`
- persistent authoring: HiGodot
- deterministic GDScript test: GUT
- live QA/observability: Hera
- runtime diagnosis: `diagnosing-game-engine-runtime-failures`
- 프로젝트 교훈 승격: `managing-base-change-proposals`
- 서사 discipline: `developing-and-revising-serial-fiction`
- 공격 검토: `running-adversarial-review-and-refinement`

### 2. 프로젝트 전용 요구

현재 프로젝트에서는 다음을 명시적으로 요구한다.

```text
기획 완료 → 검수 완료 → 최종 시각 제작 완료 → Codex BUILD
```

최종 시각 제작은:

```text
제작 목록·그림체 선확정
→ 다음 이미지/시각물 설명
→ 사용자 생성 승인
→ 정확히 1개 생성
→ 결과 검수
→ 사용자 결과 승인/수정
→ 승인 뒤 다음 항목 설명
```

또한:

- 최소 한국어·영어·일본어·중국어를 고려한다.
- PC standard·wide/ultrawide·mobile landscape에서 같은 정보 위계와 행동 의미를 유지한다.
- 로컬 실행은 fresh project-scoped PowerShell에서 self-contained Godot → project HiGodot → project CODEX_HOME → 채택된 Hera QA → Codex 순서로 시작한다.
- 사용자가 작업 후 PowerShell을 닫는다고 가정한다.
- 문제는 bounded workaround 뒤 Base 사건/Case/Learning/BCP를 검색하고, 새로 검증된 해결은 Case로 환류한다.
- 서사 사건은 메시지/질문과 캐릭터의 욕망·가치·관계를 먼저 정하고 사건 압력을 설계한다.

### 3. Prototype RED→GREEN 증거

폐쇄된 PR #302에서 다음 focused contract를 실험했다.

RED head에서 기존 Evidence Knowledge 계약은 유지된 상태로 새 테스트가 정확히 `PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md` 부재 때문에 실패했다.

```text
Ran 86 tests
FAILED (failures=1, errors=7)
```

오류는 새 Guide 부재 경계에서 발생했고, broad Skill 비생성 검사는 이미 PASS였다.

이후 Guide와 README one-hop route를 추가한 prototype exact head에서는:

- `Validate Evidence-Based Game Development Knowledge`: PASS
- `Dependency Review`: PASS

를 관찰했다. 그러나 이 active prototype은 BCP 승인 전 구현이므로 **병합하지 않았다.**

### 4. 외부 벤치마킹

공용 후보는 다음 primary/professional 자료와 방향이 맞는다.

- Godot Multiple Resolutions — base resolution, stretch/aspect, responsive Control layout
  - `https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html`
- Godot Localization using spreadsheets — locale-key/CSV/import와 locale 식별
  - `https://docs.godotengine.org/en/latest/tutorials/i18n/localization_using_spreadsheets.html`
- Microsoft PowerShell environment variables — process scope와 child process inheritance
  - `https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables`
- Google SRE Postmortem Culture — 사건 impact/root cause/resolution/follow-up 학습
  - `https://sre.google/sre-book/postmortem-culture/`
- GDC, *The System Is the Message*
  - `https://www.gdcvault.com/play/1020428/The-System-Is-the-Message`
- GDC, *Characterization, Purpose, and Action*
  - `https://www.gdcvault.com/play/1021727/Characterization-Purpose-and-Action-Creating`

외부 근거는 Base/project 정본을 대체하지 않으며, 적용 시 current version/source를 다시 확인해야 한다.

## 일반화 후보

### 후보 A — Thin cross-owner orchestration

새 광역 Skill을 만들기보다 기존 owner 사이의 순서와 handoff만 소유하는 얇은 Guide를 둘 수 있다.

```text
PLANNING_COMPLETE
→ FINAL_REVIEW_COMPLETE
→ SERIAL_VISUAL_PRODUCTION when project-selected
→ VISUAL_PRODUCTION_COMPLETE
→ PROJECT_DEDICATED_LOCAL_EXECUTION_ENVIRONMENT_FIRST
→ CODEX_BUILD_ALLOWED
```

기획 단계의 시각 사고가 필요한 경우 `DRAFT_VISUAL`은 허용하되 최종 자산이나 BUILD 승인으로 승격하지 않는다.

### 후보 B — user-gated visual production mode

Base 전체에 이미지별 사용자 승인을 강제하지 않고, **프로젝트가 user-gated mode를 채택한 경우** 다음 순차 계약을 제공한다.

```text
VISUAL_ASSET_INVENTORY
+ ART_STYLE_LOCK
→ NEXT_ASSET_BRIEF
→ GENERATION_APPROVAL
→ GENERATE_ONE_ASSET
→ VISUAL_QA
→ RESULT_APPROVAL_BEFORE_NEXT_ASSET
```

### 후보 C — localization-ready, project-owned locale set

Base 공용값은 `PROJECT_DECLARED_LOCALE_SET`과 localization-ready 구조다.

- locale key 분리
- glyph/font fallback
- 긴 문자열·CJK stress
- 번역 대상 텍스트의 불필요한 image baked-in 방지
- runtime locale QA와 번역 품질 검수 분리

한국어·영어·일본어·중국어라는 정확한 4개 locale 조합은 **현재 프로젝트 adapter 값으로 남긴다.** 중국어도 프로젝트가 `zh-Hans`/`zh-Hant`/둘 다를 명시해야 한다.

### 후보 D — responsive semantic parity

PC/wide/mobile landscape를 모두 목표로 하는 프로젝트는 pixel-identical layout이 아니라 다음 의미를 보존한다.

```text
SAME_INFORMATION_HIERARCHY_NOT_PIXEL_IDENTICAL
SAME_PRIMARY_ACTION_SEMANTICS
SAME_STATE_MEANING
SAME_FEEDBACK_MEANING
RESPONSIVE_LAYOUT_ADAPTATION
```

정확한 해상도·target matrix는 프로젝트가 소유한다.

### 후보 E — dedicated local environment owner 재사용

새 실행 도구를 만들지 않고 현행 Base의 전용 로컬 실행환경 계약을 재사용한다.

```text
fresh project-scoped PowerShell
→ self-contained/dedicated Godot
→ project-scoped HiGodot profile/server/ports
→ project-scoped CODEX_HOME
→ project-adopted Hera live-QA when required
→ Codex in exact project/worktree
```

Dedicated PowerShell은 별도 PowerShell 설치본이 아니라 fresh process에 project environment를 주입한 세션이다.

Hera는 금지하지 않는다. 현재 Base 권한 경계에서는 live QA/observability로 사용하고 persistent authoring은 HiGodot이 유지한다.

### 후보 F — incident/case recovery feedback

```text
PRESERVE_EVIDENCE
→ REPRODUCE_OR_NARROW
→ BOUNDED_WORKAROUND_OR_RECOVERY
→ BASE_CASE_RECOVERY_LOOP
→ REVALIDATE
→ NEW_VERIFIED_CASE_IF_NEEDED
→ BCP_ONLY_IF_GENERALIZABLE
```

Base Case, 분야별 Learning Log, `skills/SKILL_LEARNING_LOG.md`, `[수정제안서]/**`, 최근 동일-goal PR/Issue를 검색한다.

새 Case는 `문제 → 원인 → 실패 접근 → 해결 → 회귀 → 교훈 → 재사용 조건 → 비사용 조건`을 기록한다.

### 후보 G — message/character-before-event heuristic

서사 사건 아이디어에 다음 순서를 **heuristic**으로 제공할 수 있다.

```text
MESSAGE_AND_CHARACTER_BEFORE_EVENT
MESSAGE_OR_QUESTION
→ CHARACTER_VALUES_WANTS_RELATIONSHIPS
→ EVENT_PRESSURE
→ CHOICE_OR_ACTION
→ CONSEQUENCE
→ AFTERMATH
```

메시지는 강제 교훈이 아니라 질문·감정·가치 충돌일 수 있다. 사건/게임플레이 기능보다 메시지가 항상 상위라는 보편 규칙으로 만들지 않는다.

## 적용 조건과 비사용 조건

### 적용 조건

- 여러 기존 owner가 존재하지만 phase/handoff 경계가 흩어져 프로젝트 실행 순서가 자주 흔들리는 경우
- 최종 시각물의 실제 consumer·style·approval state를 구현 전에 잠글 필요가 있는 경우
- 다국어/여러 화면비/복수 입력이 제품 요구에 포함되는 경우
- 프로젝트별 local Godot/HiGodot/Codex/Hera 상태가 서로 오염될 위험이 있는 경우
- 장애 해결 교훈을 재사용 가능한 Case로 보존할 가치가 있는 경우
- 서사 사건이 캐릭터 동기와 무관한 spectacle-first로 반복되는 경우

### 비사용 조건

- 단순 L0 문서 수정이나 단일 독립 task에서 cross-owner phase orchestration이 불필요한 경우
- 프로젝트가 최종 시각 제작을 Codex 이전에 요구하지 않는 경우
- user-gated visual approval이 필요 없는 자동/대량 생성 파이프라인
- localization을 지원하지 않는 실험용 프로젝트
- mobile/wide 등 해당 target이 없는 프로젝트
- 기존 Base owner 하나만으로 해결되고 별도 handoff 계약이 불필요한 문제
- message-first가 작품 의도와 맞지 않거나 emergent/systemic narrative가 핵심인 경우

프로젝트 전용 4개 언어, 고정 해상도, 이미지 개수, 캐릭터/세계관, PowerShell 실제 경로·port·profile ID를 Base 공용 상수로 올리지 않는다.

## 반례와 위험

### 위험 1 — orchestration Guide가 또 다른 권위 원본이 되는 문제

세부 절차를 복제하면 current owner와 drift한다.

**완화:** 새 Guide는 phase/handoff만 소유하고 domain-specific 알고리즘은 one-hop reference로 둔다.

### 위험 2 — 프로젝트 고유값의 Base 승격

`ko/en/ja/zh-*`, 이미지마다 사용자 승인, PC/wide/mobile landscape는 현재 프로젝트에서 필수지만 모든 Base consumer의 보편값은 아니다.

**완화:** exact values를 `PROJECT_ADAPTER_VALUE`로 분리하고 Base는 선언/모드/검증 구조만 제공한다.

### 위험 3 — responsive를 pixel-identical로 오해

같은 좌표를 강제하면 ultrawide·mobile에서 가독성/입력성이 악화될 수 있다.

**완화:** semantic/information hierarchy parity만 공용화하고 exact layout/profile은 프로젝트가 소유한다.

### 위험 4 — visual gate가 기획 탐색을 막음

최종 이미지 gate를 너무 강하게 적용하면 유용한 concept mock도 금지할 수 있다.

**완화:** 명시적 `DRAFT_VISUAL` 탐색 예외를 두고 product asset 승격만 막는다.

### 위험 5 — Hera 권한 왜곡

Hera를 금지하거나 persistent authoring authority로 과승격할 수 있다.

**완화:** 현행 채택 역할 `LIVE_QA_AND_OBSERVABILITY_ONLY`를 재사용하고 HiGodot/GUT 역할과 분리한다.

### 위험 6 — workaround가 원인 분석을 대체

우회가 성공했다는 이유로 원인·재현·회귀를 기록하지 않을 수 있다.

**완화:** bounded workaround 뒤 Base Case recovery와 revalidation을 요구한다.

### 위험 7 — 단일 성공을 즉시 Base 활성 규칙으로 승격

사건 하나를 해결하고 바로 Skill/Policy를 바꾸면 과잉 일반화다.

**완화:** Case와 BCP implementation을 분리한다.

### 위험 8 — message-first가 설교가 됨

모든 장면에 교훈을 강제하면 서사와 플레이 자율성을 손상할 수 있다.

**완화:** message를 질문/감정/가치 충돌까지 확장하고 heuristic으로만 사용한다.

### 반례

- procedural/emergent simulation처럼 사건이 시스템 상호작용에서 생성되는 작품은 message/character-first보다 system-rule-first가 더 적합할 수 있다.
- localization이 없는 내부 tool은 locale stress가 불필요하다.
- server-side/headless work에는 visual-production gate가 불필요하다.
- 자동 asset build pipeline은 human one-at-a-time approval이 병목이 될 수 있다.

## 영향 범위와 검증

### 승인될 경우 예상 구현 후보

새 broad Skill은 만들지 않는다.

후보:

1. `docs/knowledge/game-development/PROJECT_CREATION_DELIVERY_ORCHESTRATION_GUIDE.md`
   - cross-owner phase/handoff only
2. `docs/knowledge/game-development/README.md`
   - one-hop routing
3. `tests/test_project_creation_delivery_orchestration.py`
   - phase/boundary/regression contract
4. 기존 Evidence Knowledge workflow에 focused test를 추가

필요하다면 기존 active owner에 작은 one-hop link만 추가하되, 승인 범위를 벗어난 세부 재작성은 하지 않는다.

### 검증 계획

TDD:

```text
RED: Guide/route 없음 때문에 focused contract 실패
GREEN: 최소 Guide/route로 focused contract 통과
REGRESSION: 기존 Evidence Knowledge + Base v9 + Game Project Operating System
```

적대적 검토:

- authority duplication
- project-value promotion
- image approval mode의 보편 강제
- final visual vs `DRAFT_VISUAL` 혼동
- responsive pixel-identity 오해
- Hera ban/authority inflation
- incident over-generalization
- narrative moralization
- 새 broad Skill 생성
- current-main/other PR overlap

객관 증거:

- exact PR head SHA
- required checks terminal Green
- unresolved review threads = 0
- strict-up-to-date current main
- changed-file inventory가 승인 범위와 일치
- merge 후 new-main readback

## 승인과 구현

현재 상태는 `SUBMITTED`다.

```yaml
approval_ref: null
implementation_pr: null
```

이 proposal PR은 `[수정제안서]/**`만 변경한다.

**이 제안의 병합은 활성 Base 구현 승인이 아니다.**

다음 단계는 별도다.

```text
SUBMITTED
→ UNDER_REVIEW
→ 사용자 APPROVED_FOR_IMPLEMENTATION | DEFERRED | REJECTED
→ approval_ref 기록
→ 별도 implementation PR
→ TDD / exact-head CI / adversarial review
→ merge
```

승인 전에는 Active Method·Skill·Template·Tool·Schema·Guide·Test·Workflow를 변경하지 않는다.

PR #302의 prototype은 향후 구현의 참고 증거일 뿐이며 재사용 시 current main 위에서 다시 구성·검증해야 한다.
