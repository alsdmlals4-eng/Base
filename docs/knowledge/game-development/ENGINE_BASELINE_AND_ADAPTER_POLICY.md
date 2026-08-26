# Engine Baseline & Adapter Policy

## 목적

게임 엔진의 최신 릴리스 주기와 프로젝트 생산 버전을 분리하고, Base의 재사용 가능한 구현·검증 규칙을 특정 엔진에 과도하게 결합하지 않기 위한 공용 정책이다.

현재 프로젝트 포트폴리오의 기본 실행 엔진은 Godot이며, 이 정책은 Godot을 폐기하거나 기존 프로젝트를 Unity로 이전하기 위한 정책이 아니다.

## Machine Contract

```text
ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE
GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER
ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
STABLE_ENGINE_BASELINE
NO_AUTOMATIC_LATEST_FOLLOW
CANARY_BEFORE_ENGINE_BASELINE_PROMOTION
ENGINE_UPDATE_REQUIRES_CONCRETE_BENEFIT_OR_BLOCKER
ENGINE_UPDATE_IN_PLANNED_MAINTENANCE_WINDOW
ENGINE_MIGRATION_REQUIRES_SEPARATE_REALITY_GATE
MCP_IS_ADAPTER_CAPABILITY_NOT_ENGINE_SELECTION_AUTHORITY
NOTION_HUMAN_FACING_CANON
REPOSITORY_RUNTIME_TRUTH
WORK_EXECUTION_SURFACE_NOT_CANON
```

## 1. 엔진 중립 Core와 Adapter

`ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE`가 소유하는 것은 특정 엔진 API가 아니라 다음 불변식이다.

- exact project / repository / ref identity;
- 승인된 player outcome / scope / protected scope;
- implementation handoff와 executor rehydration;
- 실행 환경 freshness와 wrong-target 방지;
- test / runtime / play / human evidence 분리;
- `NOT_RUN`·`BLOCKED_UNVERIFIED` evidence ceiling;
- rollback / compatibility / post-change readback;
- 구현 결과의 GPT final review와 canon sync.

엔진별 세부 구현은 adapter가 소유한다.

```text
ENGINE_NEUTRAL_PRODUCT_IMPLEMENTATION_CORE
→ ENGINE_ADAPTER_SELECTED_FROM_PROJECT_CANON
   ├─ Godot adapter: current default
   ├─ Unity adapter: future canary only when separately approved
   └─ other engine adapter: same separate adoption gate
```

### 현재 기본 Adapter

`GODOT_DEFAULT_ACTIVE_ENGINE_ADAPTER`:

- 기존 프로젝트의 승인된 Godot baseline을 유지한다.
- HiGodot를 채택한 프로젝트는 기존 single persistent authoring authority를 유지한다.
- GUT/Hera 및 Godot-specific editor/runtime/build/export 계약은 Godot adapter 책임으로 유지한다.
- `CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER`는 기존 Godot 프로젝트의 compatibility vocabulary로 계속 유효하다.
- 엔진 중립 Core를 만들었다는 이유로 Godot-specific 계약을 일괄 rename/rewrite하지 않는다.

## 2. Production Engine Version Policy

### `STABLE_ENGINE_BASELINE`

프로젝트는 `latest`를 생산 기준으로 사용하지 않는다. 각 프로젝트 또는 함께 운용하는 활성 wave는 검증된 stable baseline을 명시적으로 고정한다.

### `NO_AUTOMATIC_LATEST_FOLLOW`

새 patch/minor/major가 나왔다는 사실만으로 업데이트하지 않는다.

업데이트 검토 Trigger:

- 현재 baseline의 blocker/critical defect;
- 보안 또는 필수 플랫폼/스토어 대응;
- 필요한 plugin/addon/SDK compatibility;
- 빌드·성능·개발 생산성의 구체적이고 측정 가능한 개선;
- 장기 지원 종료 또는 현재 baseline 유지 위험 증가.

Trigger가 없으면 현재 baseline을 유지한다.

### `CANARY_BEFORE_ENGINE_BASELINE_PROMOTION`

```text
new engine release
→ NO_AUTOMATIC_LATEST_FOLLOW
→ concrete benefit / blocker exists?
   ├─ NO → keep STABLE_ENGINE_BASELINE
   └─ YES
      → isolated canary project/worktree/build
      → project import/parse
      → addon/plugin/package compatibility
      → deterministic tests
      → runtime/play smoke
      → build/export/platform checks required by target
      → rollback proof
      → actual benefit confirmed
      → planned maintenance window
      → baseline promotion decision
```

Canary PASS는 다른 프로젝트의 자동 승격 권한이 아니다. 직접 영향 범위가 다른 프로젝트는 필요한 수준의 compatibility evidence를 별도로 확보한다.

### `ENGINE_UPDATE_IN_PLANNED_MAINTENANCE_WINDOW`

프로젝트 기능 개발 중 최신 엔진을 따라가기 위해 baseline을 반복 변경하지 않는다. 업데이트는 독립 maintenance 작업으로 취급해 기능 변경과 엔진 변경을 한 PR/증거 묶음에 섞지 않는 것을 기본으로 한다.

## 3. 엔진 교체 Gate

`ENGINE_MIGRATION_REQUIRES_SEPARATE_REALITY_GATE`:

Unity/Cocos/기타 엔진의 MCP·CLI·Asset Store·LTS·AI 기능이 좋아졌다는 이유만으로 현재 프로젝트를 이전하지 않는다.

엔진 교체는 최소 다음을 비교해야 한다.

- 현재 프로젝트의 실제 Scene/Resource/script/test/build/runtime 종속량;
- Base/Notion/Codex handoff 및 CI/tooling 재작성 비용;
- 2D/3D 제작 속도와 editor 인지부하;
- AI agent / MCP / CLI의 실제 behavior E2E 성공률;
- build/export/platform/SDK 생태계;
- 장기 버전 정책과 migration risk;
- licensing / cost;
- 기존 reusable module/evidence 손실;
- 신규 프로젝트 기준 장기 생산성.

권장 검증은 **신규 또는 엔진 종속 구현이 낮은 canary 프로젝트**에서 먼저 수행한다. 기존 포트폴리오 일괄 이전은 canary 실측이 장기 총비용 우위를 명확히 증명한 뒤 별도 승인한다.

`MCP_IS_ADAPTER_CAPABILITY_NOT_ENGINE_SELECTION_AUTHORITY`: MCP 연결 성공이나 공식 MCP 존재만으로 엔진 채택을 결정하지 않는다. 실제 project identity → operation → persisted result → runtime/evidence까지 대표 E2E가 닫혀야 한다.

## 4. Chat / Work / Codex 작업면

Base의 역할 owner와 ChatGPT의 작업면을 구분한다.

```text
Chat
→ 빠른 질문 / 논의 / 선택지 비교 / 사용자 결정 정리

Work
→ 긴 multi-step 조사·분석·감사
→ 연결된 GitHub/Notion/파일을 넘나드는 비코딩 작업
→ Base·Notion·문서·표·보고서·검수·인수인계
→ 완료까지 이어지는 장기 프로젝트 작업

Codex
→ 실제 게임 프로젝트의 code / Scene / Resource / runtime / build / test 구현
→ project canon이 선택한 engine adapter를 사용
```

`Work는 실행 작업면이며 새 정본 저장소가 아니다`.

- `NOTION_HUMAN_FACING_CANON`: 사람이 읽고 비교·수정하는 Project Home, Flow, Visual, GDD, 표는 Notion 정본을 유지한다.
- `REPOSITORY_RUNTIME_TRUTH`: Markdown/JSON/game data/code/Scene/Resource/test/build/runtime evidence는 GitHub repository가 소유한다.
- `WORK_EXECUTION_SURFACE_NOT_CANON`: Work 대화/중간 상태만으로 새 결정이나 구현 완료를 정본으로 승격하지 않는다. 필요한 결과는 기존 Notion/GitHub owner에 기록하고 readback한다.

### 기본 선택

- 짧은 질문·논의·판단: Chat.
- 여러 단계의 프로젝트 기획·조사·검수·Notion/Base 작업: Work 우선.
- 실제 게임 구현: Codex.

Work에서 시작했더라도 실제 product implementation boundary에 도달하면 기존 GPT→Codex handoff를 유지한다.

## 5. 현재 적용 판정

- 현재 기존 게임 프로젝트: `KEEP_GODOT_CURRENT_BASELINE`.
- Godot 최신 릴리스: `OBSERVE_ONLY_UNLESS_UPDATE_TRIGGER`.
- Unity: `FUTURE_CANARY_CANDIDATE`, 현재 포트폴리오 migration authority 없음.
- ChatGPT Work: `DEFAULT_FOR_LONG_MULTISTEP_NONCODING_PROJECT_WORK`.
- Notion/GitHub: 기존 DOMAIN_SPLIT_CANON 유지.

## 6. 재검토 조건

다음 중 하나가 생기면 이 정책을 다시 비교한다.

- 현재 Godot baseline이 필수 플랫폼/스토어/보안 요구를 충족하지 못함;
- Godot adapter의 유지비가 반복적으로 feature 개발 비용을 초과함;
- Unity 또는 다른 엔진 canary가 동일한 2D 프로젝트에서 명확한 총작업량 절감을 실측함;
- 공식 AI/MCP/CLI stack의 안정성·비용·지원정책이 materially 변경됨;
- 프로젝트 방향이 3D/콘솔/특정 SDK 의존 중심으로 크게 바뀜.

재검토 전에는 현재 Godot baseline과 adapter 권위를 유지한다.
