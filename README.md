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
→ 대상 프로젝트 AGENTS.md·START_HERE·Active Context·AI canon
→ 실제 코드·데이터·자산·테스트와 exact commit
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [기획 작업순서·근거 정책](docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md)
- [장기 작업 실행 정책](docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md)
- [Repository-first 프로젝트 Workspace 정책](docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md)
- [Repository-first machine 권한 계약](docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json)
- [Repository-first GPT–Codex 인계 정책](docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md)
- [AI 프로젝트 상세 기획·구현 명세 Template](templates/project-operations/AI_PROJECT_CANON_SPEC.md)
- [사람용 상세 기획서 PDF Export Checklist](templates/project-operations/HUMAN_GDD_PDF_EXPORT_CHECKLIST.md)
- [Notion 퇴역·저장소 이관 Checklist](templates/project-operations/NOTION_RETIREMENT_AND_REPOSITORY_MIGRATION_CHECKLIST.md)
- [Legacy Project Workspace 권한 계약](docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json)
- [Legacy Notion 시각 자산·Flow Workflow](docs/knowledge/game-development/NOTION_VISUAL_ASSET_AND_FLOW_WORKFLOW.md)
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

새 프로젝트와 신규 Slice의 기본 정본은 `REPOSITORY_PRIMARY_PROJECT_CANON`입니다.

```text
project repository
├─ AGENTS.md
├─ START_HERE.md
├─ ACTIVE_CONTEXT.md
├─ CURRENT_CONFIRMED_DECISIONS.md
├─ docs/canon/AI_GAME_SPEC.md
├─ docs/handoffs/CURRENT_CODEX_HANDOFF.md
├─ assets/ASSET_MANIFEST.json
├─ 실제 코드·데이터·Scene·Resource·asset·test·evidence
└─ docs/exports/HUMAN_GDD_<milestone>_<source-sha>.pdf
```

프로젝트마다 경로가 다르면 `AGENTS.md`와 registry에서 동등 owner를 명시합니다. 같은 질문에 여러 활성 정본을 만들지 않습니다.

기본 기획 산출물은 두 개입니다.

1. `AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN` — 저장소의 상세 AI 기획·구현 명세 정본
2. `HUMAN_GDD_PDF_DERIVED_VIEW` — exact source commit에서 생성한 사용자용 상세 기획서 PDF

PDF는 독립 정본이 아닙니다. PDF 검토에서 승인된 수정은 repository canon으로 되돌린 뒤 다음 의미 있는 Gate에서 새 PDF를 생성합니다.

데스크톱 GPT Work는 `CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON`, ChatGPT Library는 `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`입니다. Work와 Library는 작업·이미지 후보·참고 자료·PDF 보관을 지원하지만 repository version control을 대체하지 않습니다.

기존 Notion의 `NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS`와 Google Sheets는 `LEGACY_READ_ONLY_MIGRATION_SOURCE`입니다. `PROJECT_RELATION_REQUIRED`를 유지하며 고유 자료만 repository canon, tracked asset 또는 비정본 Library reference로 이관하고 destination readback을 검증합니다. 기존 페이지·DB는 사용자 삭제 지시 없이 제거하지 않습니다.

`VISUAL_MAP_DERIVED`와 사람용 PDF는 이해·검토를 위한 파생물입니다. 코드·Scene·Resource·runtime config·tracked implementation asset·build/test는 repository runtime truth가 책임집니다.

## 이미지·자산 Workflow

```text
actual game consumer / screen / scene / state inventory
→ need / bounded brief
→ generate or edit candidate
→ approval or rejection
→ repository implementation path
→ ASSET_MANIFEST identity / version / provenance / rights / consumer
→ REPOSITORY_PATH_MANIFEST_SHA256_READBACK
→ Codex implementation task
→ runtime consumption and REPOSITORY_NATIVE_EVIDENCE_CAPTURE
```

승인 asset은 최소한 `asset_id`, `repository_path`, `actual_consumer`, `approval_status`, `version`, `sha256`, `source_or_provenance`, `rights_or_license_state`, `implementation_status`를 추적합니다.

대형 editable master나 비교 시안은 Library/local source에 둘 수 있지만 실제 게임이 소비하는 입력은 Codex가 exact commit에서 찾을 수 있는 repository path와 manifest를 가져야 합니다. Notion attachment 부재는 구현 blocker가 아니며, repository asset 또는 manifest가 없으면 Notion에 preview가 보여도 구현 준비 완료가 아닙니다.

Reference와 Benchmark는 자산 정본이 아닙니다. 필요할 때 `ADOPT / ADAPT / TEST / REFERENCE_ONLY / AVOID / IGNORE`로 적용 판정을 기록합니다.

## Legacy·폐기 프로젝트 작업면

다음은 현재 active/default project surface가 아닙니다.

```text
Notion mandatory intermediate writing / attachment gate after migration
Figma / Figma Bridge / project Figma route registry
external HTML workspace / dashboard / catalog
legacy Google Sheets after migration
project-management Tool Hub
QA Evidence Studio
localhost Expression / Sprite management surfaces
```

기존 Notion은 프로젝트별 `NOTION_UNIQUE_CANON_COUNT`, `CODEX_NOTION_DEPENDENCY_COUNT`, `ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT`가 모두 0이 될 때까지 read-only migration source로 남을 수 있습니다. 이 count가 0이라는 사실은 runtime·UX·release PASS를 의미하지 않습니다.

Git history와 과거 plan/test/evidence는 rollback·학습 기록으로 남을 수 있습니다. 고유 정보나 재사용 가능한 원리만 current repository owner로 흡수하고, 과거 문서가 존재한다는 이유만으로 `NOTION_DEFAULT_PROJECT_WORKSPACE`, `NOTION_HUMAN_FACING_CANON`, `CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION` 같은 legacy route를 다시 기본값으로 복원하지 않습니다.

검증은 별도 QA 관리 앱을 기본으로 두지 않고 `REPOSITORY_NATIVE_EVIDENCE_CAPTURE`를 사용합니다.

```text
project/build identity
→ acceptance contract
→ existing tests / GUT / Godot·Hera runtime / logs / screenshots·video / CI artifacts
→ exact commit/PR identity
→ optional legacy provenance locator
→ PASS | FAIL | BLOCKED | NOT_RUN + evidence ceiling
```

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 Skill을 무작정 읽는다는 뜻이 아닙니다. Registry와 Documentation Map에서 현재 요청에 필요한 책임 원본과 최소 Skill만 선택합니다.

## 통합 운영 흐름

```text
요청·현재 상태 조사
→ 프로젝트 repository canon과 actual implementation fresh-read
→ 최소 3개 실질 대안·벤치마킹·창의성 frontier·장기 적합성
→ 승인된 작업 계약
→ AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN 갱신·readback
→ 실제 소비처 기준 asset/audio 준비
→ REPOSITORY_PATH_MANIFEST_SHA256_READBACK
→ exact planning commit
→ 필요 시 Codex repository-first Godot 구현 인계
→ release-near Vertical Slice·playtest·eval
→ 정본·정적·runtime·접근성·성능·회귀 검증
→ 플랫폼·권리 검증
→ 의미 있는 Gate에서 HUMAN_GDD_PDF_DERIVED_VIEW 생성·render readback
→ 구현 후보 전체 적대적 개선 루프 최소 5회, 이후 clean까지
→ exact-head PR / merge / POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP
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

활성 Skill 수는 Registry 관찰값이며 설계 제약이 아닙니다. 새 Skill은 고정 개수 목표가 아니라 독립 입력·산출물·검증·승인 경계가 실제로 필요한지로 판단합니다.

현재 routing authority는 `skills/SKILL_REGISTRY.json`과 각 active `SKILL.md`입니다. Release lock과 고정 payload는 frozen v9.0 release derivatives이며 현행 Registry를 되돌리는 권한이 아닙니다.

This entrypoint does not maintain a second Skill list.

- Machine authority: `skills/SKILL_REGISTRY.json` + 각 `SKILL.md` frontmatter
- Human view: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Behavior eval: `skills/SKILL_BEHAVIOR_EVALS.json`
- Legacy ID: `skills/LEGACY_SKILL_ALIASES.md`

Skill 수 자체는 목표가 아닙니다. 기존 owner/mode/reference로 책임을 보존할 수 있으면 흡수하고, 독립 input/output/authority/validation boundary가 실제로 필요할 때만 새 Skill을 추가합니다.

## 프로젝트 책임 원본

```text
project AGENTS.md / START_HERE.md
→ ACTIVE_CONTEXT.md / CURRENT_CONFIRMED_DECISIONS.md
→ AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
→ registered Markdown / JSON / tracked asset owners
→ 실제 코드·데이터·Scene·Resource·자산·테스트·evidence

HUMAN_GDD_PDF_DERIVED_VIEW
→ exact source commit의 사람용 검토 파생물
```

한 질문에는 현행 책임 원본 하나만 둡니다. PDF, Library, legacy Notion 시각 자료, 외부 벤치마크, 리뷰와 과거 대화는 실제 구현 상태나 repository canon을 대신하지 않습니다.

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