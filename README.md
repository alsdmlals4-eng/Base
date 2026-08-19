# Base

여러 게임·창작 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 실행 Skill, Template, 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 프로젝트의 세계관·규칙·수치·실제 구현·승인 자산·런타임 상태는 프로젝트 정본과 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/GPT_FIRST_PROJECT_WORKFLOW.md
→ docs/OPERATING_MODEL.md
→ docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 대상 프로젝트 GitHub + exact Project Notion Home
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [GPT-first 프로젝트 Workflow](docs/GPT_FIRST_PROJECT_WORKFLOW.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [장기 작업 실행 정책](docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [프로젝트 Workspace 권한 계약](docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json)
- [Notion 시각 자산·Flow Workflow](docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md)
- [시각 협업 정책](docs/VISUAL_COLLABORATION_TOOL_POLICY.md)
- [폐기 프로젝트 작업면 흡수·삭제 정책](docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md)
- [Google Sheets 일회성 이관 Stub](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [근거 기반 게임 개발 지식 허브](docs/knowledge/game-development/README.md)
- [플랫폼 심사·자산 권리·참조 독립 제작 Guide](docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md)
- [게임 개발 Evidence Pack](templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md)
- [게임 개발 Case Card](templates/research/GAME_DEVELOPMENT_CASE_CARD.md)
- [PC·Android Cross-platform Guide](docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md)
- [PC·Android Delivery Profile](templates/planning/PC_ANDROID_DELIVERY_PROFILE.md)
- [공용 Skill Registry](skills/SKILL_REGISTRY.json)
- [활성 Skill 생성 Map](docs/generated/BASE_ACTIVE_SKILLS.md)
- [이전 Skill ID 별칭](skills/LEGACY_SKILL_ALIASES.md)

## 기본 역할 분리

```text
GPT
→ 기획·조사·대안 비교·벤치마킹
→ 시스템/데이터/UX/UI/아트 설계
→ 이미지/시각 후보 검수
→ 최종 기획·구현 결과 검수

Notion
→ NOTION_HUMAN_FACING_CANON
→ Project Home / Visual·Story Bible / Flow·Storyboard
→ Asset / Reference / Benchmark / 사람용 확정표

GitHub repository
→ REPOSITORY_STRUCTURED_CANON
→ REPOSITORY_RUNTIME_TRUTH
→ Markdown / JSON / game data / code / Scene / Resource / tracked asset / tests / evidence

PowerShell + Codex
→ 실제 저장소·엔진 실행이 필요한 경우에만 선택적 보조 executor
```

Codex는 기본 주 책임자가 아닙니다. 기획과 검수는 GPT에서 끝내고, 다수 파일 구현·Godot mutation·runtime 재현처럼 실제 실행이 필요할 때만 `CODEX_OPTIONAL_SUB_EXECUTOR`로 사용합니다.

## 프로젝트 기본 작업면

새 프로젝트와 새 기획·시각 작업의 기본 인간 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`입니다.

```text
00 · PROJECT HUB
→ Project Registry

project page
  → PROJECT HOME
  → PROJECT CONTROL
  → VISUAL / STORY BIBLE
  → FLOW / STORYBOARD
  → ASSET / CHARACTER / REFERENCE
  → CORE SYSTEM / CONFIRMED TABLES
  → PRODUCTION / HANDOFF

90 · SYSTEM MASTERS
→ unfiltered master data sources
```

`PROJECT_RELATION_REQUIRED`와 project-scoped Record Key로 프로젝트 간 데이터를 분리합니다. 일반 프로젝트 페이지에는 다른 프로젝트의 unfiltered record를 노출하지 않습니다.

Visual Map은 `VISUAL_MAP_DERIVED`입니다. 코드·Scene·Resource·runtime config·tracked implementation asset·build/test는 repository-native runtime truth가 책임집니다.

## 이미지·UX/UI → PoC Workflow

이미지·UI·UX가 PoC/demo 판단에 영향을 주면 다음 순서를 기본으로 합니다.

```text
concept / system / player experience
→ representative UX/UI states
→ image / visual candidates
→ GPT visual + UX review
→ exact Project Notion attach
→ Notion readback
→ user approval
→ approved visuals feed PoC
→ repository implementation
→ runtime demo test
→ GPT final review
```

모든 production 화면을 PoC 전에 완성하라는 뜻은 아닙니다. 첫인상·주 플레이·핵심 선택·주요 feedback 등 테스트 판단에 필요한 대표 상태를 먼저 확보합니다.

승인 이미지를 PoC 입력으로 쓰기로 했다면 해당 이미지 또는 provenance가 유지된 구현용 파생 자산을 사용합니다. Notion preview 자체는 runtime 적용 증거가 아닙니다.

## 폐기된 프로젝트 작업면

다음은 새 작업의 active project surface가 아닙니다.

- Figma 및 전용 Figma Bridge/route
- localhost Expression/Sprite/Tool Hub 계열 프로젝트 앱
- standalone localhost/browser QA Evidence Studio
- 독립 HTML 프로젝트 dashboard/catalog
- Google Sheets GDD/workspace

폐기 순서는 `DEPRECATED_SURFACE_ABSORB_THEN_DELETE`입니다.

```text
unique material / reusable principle audit
→ human-facing meaning → Notion
→ structured/runtime meaning → repository-native owner
→ destination readback
→ active consumer/reference update
→ delete active surface
→ regression
```

Git history는 rollback과 감사 이력이지 active canon이 아닙니다. repository 내부에서 실제 CI/build/migration/validation이 소비하는 non-interactive script는 사용자-facing local tool과 구분합니다.

### Repository-native QA

별도 QA 앱 대신 다음 원리를 유지합니다.

- exact commit/PR head에 evidence 연결
- `PASS / FAIL / BLOCKED / NOT_RUN` 분리
- screenshot/video/log/Actions artifact 또는 PR evidence 사용
- critical FAIL을 성공으로 포장하지 않음
- Android 미연결은 `DEFERRED_NOT_CONNECTED`로 PC 검증과 분리

## Google Sheets

Google Sheets는 `RETIRED_MIGRATION_ONLY`입니다. 고유 미이관 정보가 실제로 남아 있을 때만 한 번 읽고 Notion/repository로 이사한 뒤 readback하고 active reference를 제거합니다. 새 GDD나 새 상태 관리에 사용하지 않습니다.

## 비용

```text
CURRENT_PAID_PLANS: GPT_PRO
PAID_PLAN_COUNT: 1
NOTION_PAID_ON_REQUEST_ONLY
```

현재 기본 유료 플랜은 GPT Pro 하나입니다. Notion은 무료/현재 사용 가능한 범위를 우선합니다. 유료 Notion 기능이 반복 병목을 실제로 줄이고 무료 대안보다 총비용이 낮다는 근거가 생기면 비용·효과·무료 대안을 먼저 설명하고 사용자 승인 후에만 결제 경로를 사용합니다.

## 통합 운영 흐름

```text
GitHub + Notion current-state audit
→ 최소 3개 실질 대안
→ benchmark / trade study / better-alternative search
→ GPT planning + review
→ Notion visual checkpoint when material
→ user approval
→ adversarial review
→ repository / Notion sync
→ optional Codex executor when needed
→ GPT final review
→ exact-head PR / merge
→ GitHub main + Notion postmerge readback
→ user-learning completion report
```

## Active Skill Registry View

현재 Active Skill 수·목록·owner·positive/negative trigger는 [Base Skill Map](docs/generated/BASE_ACTIVE_SKILLS.md)에서 생성해서 봅니다. 이 README는 두 번째 Skill 목록을 유지하지 않습니다.

- Machine authority: `skills/SKILL_REGISTRY.json` + 각 `SKILL.md` frontmatter
- Human view: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Behavior eval: `skills/SKILL_BEHAVIOR_EVALS.json`
- Legacy ID: `skills/LEGACY_SKILL_ALIASES.md`

## 저장소 구조

```text
START_HERE.md             새 채팅·새 AI 최초 라우터
AGENTS.md                 항상 적용되는 공용 실행 규칙
docs/                     운영·지식·정본·machine contract
skills/                   실행 Skill·Registry·Learning Log·reference
templates/                기획·실행·검증 Template
tools/                    repository-native 생성기·검증기·migration/CI helper
tests/                    운영·라우팅·정본·회귀 테스트
[수정제안서]/             Base 승격 후보·승인·구현 이력
```

## 검증

전체 로컬 검증은 exact trusted main SHA를 명시합니다.

```bash
python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>
```

실행하지 않은 테스트·런타임·렌더·권한은 통과로 보고하지 않습니다.

## 라이선스와 보안

Base 자체는 [MIT License](LICENSE)로 배포됩니다. 제3자 코드·문서·자산은 각 원출처 라이선스를 따릅니다. 민감한 취약점·계약서·개인정보는 공개 저장소에 넣지 않고 [Security Policy](SECURITY.md)를 따릅니다.