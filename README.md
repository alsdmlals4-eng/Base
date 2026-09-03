# Base

여러 게임·창작 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 실행 Skill, Template, 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 프로젝트의 세계관·규칙·수치·실제 구현·승인 자산·런타임 상태는 프로젝트 정본과 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md
→ docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ docs/generated/BASE_ACTIVE_SKILLS.md
→ 현재 작업에 필요한 Skill·mode·reference·Template·Case
→ 대상 프로젝트 AGENTS.md·START_HERE·Active Context·승인 Decision·실제 파일
→ 필요한 경우에만 legacy Notion/Sheet 고유 자료
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [Desktop GPT repository-first 프로젝트 작업 정책](docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md)
- [프로젝트 Workspace 권한 계약 V4](docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json)
- [Notion → Repository 안전 이관 체크리스트](templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [기획 작업순서·근거 정책](docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md)
- [장기 작업 실행 정책](docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md)
- [프로젝트 Workspace 권한 계약 V3 — compatibility/history](docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json)
- [Notion 시각 자산·Flow Workflow — legacy migration/reference](docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md)
- [시각 협업 정책](docs/VISUAL_COLLABORATION_TOOL_POLICY.md)
- [폐기 프로젝트 작업면 정책](docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md)
- [Google Sheets migration-only 정책](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [근거 기반 게임 개발 지식 허브](docs/knowledge/game-development/README.md)
- [게임 개발 Evidence Pack](templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md)
- [Game Development Case Card](templates/research/GAME_DEVELOPMENT_CASE_CARD.md)
- [PC/Android Cross-Platform Delivery Guide](docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md)
- [PC/Android Delivery Profile](templates/planning/PC_ANDROID_DELIVERY_PROFILE.md)
- [플랫폼 심사·자산 권리·참조 독립 제작 Guide](docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md)
- [통합 Vertical Slice 실행문 v9](templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md)
- [GPT 이미지 생성·검수 정책](docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md)
- [프로젝트 로컬 Asset Vault 정책](docs/PROJECT_LOCAL_ASSET_VAULT_POLICY.md)
- [공용 Skill Registry](skills/SKILL_REGISTRY.json)
- [활성 Skill 생성 Map](docs/generated/BASE_ACTIVE_SKILLS.md)
- [이전 Skill ID 별칭](skills/LEGACY_SKILL_ALIASES.md)
- [Base 수정제안서]([수정제안서]/README.md)

## 프로젝트 기본 작업면

새 프로젝트와 새 기획·시각 작업의 기본 계약은 `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`입니다.

```text
Desktop GPT Work
→ 대상 프로젝트 repository fresh-read
→ 기획·조사·검수·시각자료 제작
→ repository 정본·AI production spec·asset manifest 갱신
→ PR·diff·test·readback
→ 의미 있는 Gate에서 HUMAN_MASTER_GDD_PDF 생성
→ CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA로 Codex 인계
→ Godot 구현·runtime/play evidence
→ repository 정본 상태 승격
```

프로젝트 repository가 `REPOSITORY_PRIMARY_CANON`이며 다음을 소유합니다.

```text
AGENTS / START_HERE / ACTIVE_CONTEXT / confirmed decisions
planning and implementation contracts
structured system, content, balance and flow data
approved runtime assets and ASSET_MANIFEST
code / Scene / Resource / runtime configuration
tests / build / runtime and play evidence
Codex handoff and implementation readback
```

사람용 상세 기획서 PDF는 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`이며 exact `source_commit`을 가진 파생 snapshot입니다. AI용 상세 기획·구현 명세 Markdown은 repository에 저장합니다. ChatGPT Work와 Library는 실행·참조 surface이며 정본이 아닙니다.

`NO_NEW_NOTION_WRITE_BY_DEFAULT`: 신규 기획·결정·이미지 승인·Codex handoff를 완료하기 위해 Notion에 중간 복제하지 않습니다. 기존 `NOTION_DEFAULT_PROJECT_WORKSPACE`는 `NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED`입니다. Notion에만 고유 자료가 남은 프로젝트에서는 `NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE`로 읽고 다음 세 카운터를 0으로 만듭니다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

퇴역을 위해 기존 workspace를 삭제할 필요는 없습니다: `NO_DELETE_REQUIRED_FOR_RETIREMENT`.

기존 프로젝트 Google Sheet도 고유 unmigrated material이 남아 있을 때만 `GOOGLE_SHEETS_MIGRATION_ONLY_UNTIL_REMOVAL` source로 읽고, unique material을 repository 또는 명시적 non-canon 보관소로 이관·readback한 뒤 active route에서 제거합니다.

## 이미지·자산 Workflow

```text
actual runtime consumer / state family inventory
→ need / brief
→ generate or edit candidate
→ visual review and user approval
→ approved original binary 확보
→ project-controlled repository path
→ SHA-256 + consumer + provenance + approval/implementation status
→ ASSET_MANIFEST readback
→ Codex implementation task
→ Godot actual consumer integration
→ REPOSITORY_NATIVE_EVIDENCE_CAPTURE
```

채팅·Library·PDF·preview에 이미지가 보인다는 사실만으로 구현 준비가 완료되지 않습니다. Codex 입력은 `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`를 사용합니다. 대형 제작 원본과 반복 후보는 Library 또는 프로젝트 로컬 source에 non-canon으로 둘 수 있지만, 실제 게임이 소비하는 승인 binary는 repository 경로와 manifest로 회수 가능해야 합니다.

Reference와 Benchmark는 자산 정본이 아닙니다. 필요할 때 `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`로 적용 판정을 기록합니다.

## 폐기된 프로젝트 작업면

다음은 현재 active/default project surface가 아닙니다.

```text
NOTION_DEFAULT_PROJECT_WORKSPACE
Figma / Figma Bridge / project Figma route registry
external HTML workspace / dashboard / catalog
legacy Google Sheets after migration
project-management Tool Hub
QA Evidence Studio
localhost Expression / Sprite management surfaces
```

Git history와 과거 plan/test/evidence는 rollback·학습 기록으로 남을 수 있습니다. 고유 정보나 재사용 가능한 원리만 current repository owner·asset manifest·PowerShell/Loop owner로 흡수하고, 존재한다는 이유만으로 다시 기본 경로로 라우팅하지 않습니다.

검증은 별도 QA 관리 앱을 기본으로 두지 않고 `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`를 사용합니다.

```text
project/build identity
→ acceptance contract
→ existing tests / GUT / Godot·Hera runtime / logs / screenshots·video / CI artifacts
→ exact commit/PR identity
→ optional legacy migration locator
→ PASS | FAIL | BLOCKED | NOT_RUN + evidence ceiling
```

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 Skill을 무작정 읽는다는 뜻이 아닙니다. Registry와 Documentation Map에서 현재 요청에 필요한 책임 원본과 최소 Skill만 선택합니다.

## 통합 운영 흐름

```text
요청·현재 상태 조사
→ 최소 3개 실질 대안·벤치마킹·창의성 frontier·장기 적합성
→ 승인된 작업 계약
→ Desktop GPT Work에서 repository-first planning / asset / visual production
→ 필요 시 PROJECT_VISUALIZATION_NEED_MAP와 기획 시각화
→ repository 정본·AI production spec·asset manifest 갱신
→ 의미 있는 Gate에서 source-SHA-bound 사람용 상세 PDF
→ exact repository SHA로 Codex 제품 구현 인계
→ repository-native 구현
→ release-near Vertical Slice·playtest·eval
→ 정본·정적·runtime·접근성·성능·회귀 검증
→ 플랫폼·권리 검증
→ 구현 후보 전체 적대적 개선 루프 최소 5회, 이후 clean까지
→ exact-head PR / merge / POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP
→ REQUIRED_WORK_REMAINING 재계산
→ REQUIRED_WORK_REMAINING: 0 이면 COMPLETION_CANDIDATE
→ REMAINING_WORK_COMPLETION_GATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK → 구현·검증으로 복귀
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ 같은 final POST_CHANGE_MONITOR_LOOP에서 최종 후보 lineage의 적대적 검토·postmerge readback을 닫고 CLEAN_REVIEW_EXIT까지
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ 학습·필요 시 Base 승격
→ 완료 보고
```

병합 전 구현 후보 적대 검토는 유지합니다. `POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 그 검토를 무효화하거나 같은 상태에 대해 별도 5회를 기계적으로 추가하는 규칙이 아닙니다. 마지막 구현·교정과 merge/postmerge로 갱신된 final-state lineage를 기존 `POST_CHANGE_MONITOR_LOOP`로 계속 검증해 최소 5회 floor와 `CLEAN_REVIEW_EXIT` 조건을 충족합니다.

`REQUIRED_WORK_REMAINING: 0`은 전체 완료가 아니라 완료 후보입니다. 상세 완료 순서와 finding 재개방 권한은 `docs/OPERATING_MODEL.md`의 `REMAINING_WORK_COMPLETION_GATE`가 책임집니다.

## Active Skill Registry View

현재 Active Skill 수·목록·owner·positive/negative trigger는 [Base Skill Map](docs/generated/BASE_ACTIVE_SKILLS.md)에서 생성해서 봅니다. 이 README는 두 번째 Skill 목록을 유지하지 않습니다.

활성 Skill 수는 Registry 관찰값이며 설계 제약이 아니다. 새 Skill은 고정 개수 목표가 아니라 독립 입력·산출물·검증·승인 경계가 실제로 필요한지로 판단합니다.

현재 routing authority는 `skills/SKILL_REGISTRY.json`과 각 active `SKILL.md`입니다. Release lock과 고정 payload는 frozen v9.0 release derivatives이며 현행 Registry를 되돌리는 권한이 아닙니다.

This entrypoint does not maintain a second Skill list.

- Machine authority: `skills/SKILL_REGISTRY.json` + 각 `SKILL.md` frontmatter
- Human view: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Behavior eval: `skills/SKILL_BEHAVIOR_EVALS.json`
- Legacy ID: `skills/LEGACY_SKILL_ALIASES.md`

Skill 수 자체는 목표가 아닙니다. 기존 owner/mode/reference로 책임을 보존할 수 있으면 흡수하고, 독립 input/output/authority/validation boundary가 실제로 필요할 때만 새 Skill을 추가합니다.

## 프로젝트 책임 원본

```text
Project repository exact SHA
→ AGENTS / START_HERE / ACTIVE_CONTEXT / confirmed decisions
→ AI production spec / structured data / asset manifest / handoff
→ 실제 코드·Scene·Resource·runtime asset·테스트·evidence

Derived human view
→ HUMAN_MASTER_GDD_PDF with exact source_commit

Legacy discovery only
→ Notion / Google Sheets / old dashboard material with unique unmigrated data
```

한 질문에는 현행 책임 원본 하나만 둡니다. PDF·Notion 시각 자료·외부 벤치마크·리뷰·과거 대화는 실제 구현 상태나 repository canon을 대신하지 않습니다.

## 저장소 구조

```text
START_HERE.md             새 채팅·새 AI 최초 라우터
AGENTS.md                 항상 적용되는 공용 실행 규칙
docs/OPERATING_MODEL.md   공용 작업 구조 단일 설명 원본
docs/knowledge/           분야별 Guide·Reference
docs/operations/          machine/operational contract
skills/                   실행 Skill·Registry·Learning Log·reference
templates/                기획·실행·검증 Template
tools/                    생성기·검증기·역사/전문 도구 구현; 존재 자체가 active routing 권위는 아님
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

<!-- FEDERATED_DUAL_CANON_ROUTE -->

> V4 authority route: `FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER`. `REPOSITORY_EXECUTION_DATA_CANON` owns editable structured, execution, runtime, work-status, and evidence facts. Only a `USER_APPROVED_AND_MANIFEST_REGISTERED` `APPROVED_HUMAN_BLUEPRINT_PDF_CANON` owns the immutable human visual/review baseline. `ONE_EDITABLE_OWNER_PER_ATOMIC_FACT`; `CANDIDATE_PDF_NOT_CANON` and PDF annotations do not mutate repository-owned facts. See `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json` and `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`.
