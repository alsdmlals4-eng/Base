# Base

여러 게임·창작 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 실행 Skill, Template, 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 프로젝트의 세계관·규칙·수치·실제 구현·승인 자산·런타임 상태는 프로젝트 정본과 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ docs/generated/BASE_ACTIVE_SKILLS.md
→ 현재 작업에 필요한 Skill·mode·reference·Template·Case
→ 대상 프로젝트 정본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [기획 작업순서·근거 정책](docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md)
- [장기 작업 실행 정책](docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md)
- [프로젝트 Workspace 권한 계약](docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json)
- [Notion 시각 자산·Flow Workflow](docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md)
- [시각 협업 정책](docs/VISUAL_COLLABORATION_TOOL_POLICY.md)
- [Google Sheets compatibility 정책](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [근거 기반 게임 개발 지식 허브](docs/knowledge/game-development/README.md)
- [게임 개발 Evidence Pack](templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md)
- [Game Development Case Card](templates/research/GAME_DEVELOPMENT_CASE_CARD.md)
- [PC/Android Cross-Platform Delivery Guide](docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md)
- [PC/Android Delivery Profile](templates/planning/PC_ANDROID_DELIVERY_PROFILE.md)
- [플랫폼 심사·자산 권리·참조 독립 제작 Guide](docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md)
- [통합 Vertical Slice 실행문 v9](templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md)
- [GPT 이미지 생성·검수 정책](docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md)
- [PC 우선 QA Evidence Studio](tools/qa-evidence-studio/README.md)
- [프로젝트 로컬 Asset Vault 정책](docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md)
- [공용 Skill Registry](skills/SKILL_REGISTRY.json)
- [활성 Skill 생성 Map](docs/generated/BASE_ACTIVE_SKILLS.md)
- [이전 Skill ID 별칭](skills/LEGACY_SKILL_ALIASES.md)
- [Base 수정제안서]([수정제안서]/README.md)

## 프로젝트 기본 작업면

새 프로젝트와 새 기획·시각 작업의 기본 인간 작업면은 `NOTION_DEFAULT_PROJECT_WORKSPACE`입니다.

```text
00 · PROJECT HUB
→ Project Registry

project page
  → 사람용 PROJECT HOME
  → 01 PROJECT CONTROL
  → 02 VISUAL / STORY BIBLE
  → 03 FLOW / STORYBOARD
  → 04 ASSET / CHARACTER LIBRARY
  → 05 REFERENCE / BENCHMARK
  → 06+ PRODUCTION / SPECIALIZED PAGES

90 · SYSTEM MASTERS
→ unfiltered master data sources
```

`PROJECT_RELATION_REQUIRED`로 프로젝트 간 Work·Asset·Component·Screen·Reference·Benchmark를 분리합니다. 일반 프로젝트 페이지에는 다른 프로젝트의 unfiltered record를 노출하지 않습니다.

Visual Map은 `VISUAL_MAP_DERIVED`이며 두 번째 정본이 아닙니다. 코드·Scene·Resource·runtime config·tracked implementation asset·build/test는 repository-native runtime truth가 책임집니다.

기존 프로젝트 Google Sheet는 고유 unmigrated material이 남아 있을 때만 `COMPATIBILITY_ONLY` migration source로 사용합니다.

## 이미지·자산 Workflow

```text
need / brief
→ generate or edit candidate
→ correct Project record
→ attach / upload
→ readback
→ approval or rejection
→ version / replacement
→ repository implementation task
→ runtime QA
```

사람용 Gallery에는 Preview·Name·Usage·Style·Approved·Reuse처럼 판단에 필요한 정보만 보여주고, AI/System view에는 Asset ID·Version·Status·Prompt·source provenance·Rights/License·Hash·Implementation Path 등을 보존할 수 있습니다.

Reference와 Benchmark는 자산 정본이 아닙니다. 필요할 때 `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`로 적용 판정을 기록합니다.

## 폐기된 시각 실행면

Figma Bridge, project Figma route registry, localhost Expression Studio, localhost Sprite Animation Studio, visual-delivery Tool Hub는 현재 active project surface가 아닙니다. Git history가 복구 기록을 보존합니다.

그 구현에서 검증된 다음 원칙만 현재 Workflow에 흡수했습니다.

- 정확한 Project identity
- source provenance
- identity-preserving bounded edit
- candidate review와 명시적 approval
- version / replacement
- reuse classification
- screen/flow ID
- upload 이후 readback
- repository handoff와 runtime evidence 분리

QA Evidence Studio는 Figma/Notion과 독립적인 실제 PC 런타임 증거 도구이므로 유지합니다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 Skill을 무작정 읽는다는 뜻이 아닙니다. Registry와 Documentation Map에서 현재 요청에 필요한 책임 원본과 최소 Skill만 선택합니다.

## 통합 운영 흐름

```text
요청·현재 상태 조사
→ 최소 3개 실질 대안·벤치마킹·장기 적합성
→ 승인된 작업 계약
→ Notion Project-filtered planning / asset / visual workspace
→ repository-native 구현
→ Demo-First Vertical Slice·playtest·eval
→ 정본·정적·runtime·접근성·성능·회귀 검증
→ 플랫폼·권리 검증
→ exact-head PR / merge / postmerge readback
→ 학습·필요 시 Base 승격
```

## Active Skill Registry View

현재 Active Skill 수·목록·owner·positive/negative trigger는 [Base Skill Map](docs/generated/BASE_ACTIVE_SKILLS.md)에서 생성해서 봅니다. 이 README는 두 번째 Skill 목록을 유지하지 않습니다.

활성 Skill 수는 Registry 관찰값이며 설계 제약이 아니다. 새 Skill은 고정 개수 목표가 아니라 독립 입력·산출물·검증·승인 경계가 실제로 필요한지로 판단합니다.

현재 routing authority는 `skills/SKILL_REGISTRY.json`과 각 active `SKILL.md`입니다. Release lock과 고정 payload는 frozen v9.0 release derivatives이며 현행 Registry를 되돌리는 권한이 아닙니다.

This entrypoint does not maintain a second Skill list.

- Machine authority: `skills/SKILL_REGISTRY.json` + 각 `SKILL.md` frontmatter
- Human view: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Behavior eval: `skills/SKILL_BEHAVIOR_EVALS.json`
- Legacy ID: `skills/LEGACY_SKILL_ALIASES.md`

## 프로젝트 책임 원본

```text
Notion Project page
→ Project-filtered planning / asset / visual records

DESIGN_DOCUMENT_REGISTRY.json
→ 등록된 Markdown/JSON 책임 원본
→ 실제 코드·데이터·자산·테스트
```

한 질문에는 현행 책임 원본 하나만 둡니다. Notion 시각 자료·외부 벤치마크·리뷰·과거 대화는 실제 구현 상태를 대신하지 않습니다.

## 저장소 구조

```text
START_HERE.md             새 채팅·새 AI 최초 라우터
AGENTS.md                 항상 적용되는 공용 실행 규칙
docs/OPERATING_MODEL.md   공용 작업 구조 단일 설명 원본
docs/knowledge/           분야별 Guide·Reference
docs/operations/          machine/operational contract
skills/                   실행 Skill·Registry·Learning Log·reference
templates/                기획·실행·검증 Template
tools/                    생성기·검증기·독립 QA 도구
tests/                    운영·라우팅·정본·회귀 테스트
[수정제안서]/             Base 승격 후보·승인·구현 이력
```

## 검증

전체 로컬 검증은 exact trusted main SHA를 명시합니다.

```bash
python -m pip install --requirement .github/validation-requirements.txt
python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>
```

검증기는 pinned dependency가 누락되면 `LOCAL_VALIDATION_DEPENDENCY_MISSING`으로 먼저 중단하고 설치 명령을 표시합니다. 의존성 누락으로 생긴 import failure를 제품 회귀와 섞어 보고하지 않습니다.

실행하지 않은 테스트·런타임·렌더·권한은 통과로 보고하지 않습니다.

## 라이선스와 보안

Base 자체는 [MIT License](LICENSE)로 배포됩니다. 제3자 코드·문서·자산은 각 원출처 라이선스를 따릅니다. 민감한 취약점·계약서·개인정보는 공개 저장소에 넣지 않고 [Security Policy](SECURITY.md)를 따릅니다.
