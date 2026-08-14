# Base

여러 게임 프로젝트가 공유하는 **[학습형] [공용] AI 작업 규칙, 실행 스킬, 템플릿과 검증 사례**의 원본 저장소입니다.

Base는 `어떻게 판단하고 작업하며 검증할 것인가`를 관리합니다. 각 프로젝트의 세계관, 규칙, 수치, 엔진, 실제 경로, 승인 이미지와 구현 상태는 프로젝트 저장소가 책임집니다.

## 가장 먼저 읽기

```text
START_HERE.md
→ AGENTS.md
→ docs/OPERATING_MODEL.md
→ docs/DOCUMENTATION_MAP.md
→ skills/SKILL_REGISTRY.json
→ 현재 작업에 필요한 Skill·mode·reference·Template·Case
→ 대상 프로젝트의 책임 원본과 실제 파일
```

- [Base 시작 지점](START_HERE.md)
- [공용 실행 규칙](AGENTS.md)
- [통합 운영 모델](docs/OPERATING_MODEL.md)
- [문서·스킬 역할표](docs/DOCUMENTATION_MAP.md)
- [기획 작업순서·근거 정책](docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md)
- [근거 기반 게임 개발 지식 허브](docs/knowledge/game-development/README.md)
- [PC·Android 공용 코어·플랫폼 적응·단계 출시 Guide](docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md)
- [PC·Android Delivery Profile Template](templates/planning/PC_ANDROID_DELIVERY_PROFILE.md)
- [플랫폼 심사·자산 권리·참조 독립 제작 Guide](docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md)
- [게임 개발 Evidence Pack](templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md)
- [자산 권리·출처 Record](templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md)
- [게임 출시 Compliance Evidence Pack](templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md)
- [게임 개발 Case Card](templates/research/GAME_DEVELOPMENT_CASE_CARD.md)
- [통합 Vertical Slice 실행문 v9](templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md)
- [GPT 이미지 생성·검수 및 Sheet 정책](docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md)
- [프로젝트 Google Sheets Workbook 계약](templates/project-operations/PROJECT_GOOGLE_SHEET_WORKBOOK_CONTRACT.md)
- [프로젝트 GDD Google Sheets 정책](docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md)
- [GPT 이미지 생성·검수 Plan](templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md)
- [공용 스킬 Registry](skills/SKILL_REGISTRY.json)
- [공용 어댑터 Skill Route](skills/BASE_SHARED_SKILL_ROUTES.json)
- [프로젝트 어댑터 계약](docs/BASE_SHARED_SKILL_ADAPTER_CONTRACT.md)
- [PROJECT_BASE_ADAPTER v2 명시적 마이그레이션](docs/operations/PROJECT_BASE_ADAPTER_V2_MIGRATION.md)
- [로컬 Tool 공용 계약](tools/base-tool-contracts/README.md)
- [Base Tool Hub](tools/tool-hub/README.md)
- [PC 우선 QA Evidence Studio](tools/qa-evidence-studio/README.md)
- [무추가비용 Expression Studio](tools/expression-studio/README.md)
- [무추가비용 Sprite Animation Studio](tools/sprite-animation-studio/README.md)
- [이전 Skill ID 별칭](skills/LEGACY_SKILL_ALIASES.md)
- [공용 스킬 학습 기록](skills/SKILL_LEARNING_LOG.md)
- [Base 수정제안서]([수정제안서]/README.md)

PR #328/#329 baseline을 흡수한 `tools/tool-hub/` 하나가 QA Evidence, Expression, Sprite Animation Studio의 유일한 Hub 진입점이다. 2026-08-13 Linux smoke는 공백 경로의 두 committed project fixture에서 두 visual Studio씩 네 child를 고유 port/PID로 실행하고 Expression 후보, Sprite action, Sprite effect-stage의 import/export와 `provider_call_made=false`, cross-project output 부재를 확인했다. 이는 `subscription_handoff_import` 실행 증거이며 실제 AI 생성·live Figma upload·Windows·Android 증거가 아니다. QA의 Android 상태는 `DEFERRED_NOT_CONNECTED`로 유지하며 다음 독립 후보 `Balance & Scenario Lab`은 아직 Hub surface에 추가하지 않는다.

Tool Hub의 로컬 보안 경계는 동일 OS 사용자 계정과 기기 관리자를 신뢰한다. 브라우저·프로젝트 입력을 차단하고 최종 launch 검사까지 경로·설정 drift를 탐지하지만, 실행 중 Base·Studio runtime 동시 편집은 지원하지 않는다. 같은 계정의 동시 변경까지 격리하는 별도 OS 계정·컨테이너·서명된 읽기 전용 runtime은 `HARDENED_RUNTIME_DEFERRED`다. 상세 범위는 [Tool Hub README](tools/tool-hub/README.md)를 따른다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일과 스킬을 무작정 읽는다는 뜻이 아닙니다. Registry와 Documentation Map에서 현재 요청에 필요한 책임 원본과 최소 스킬만 선택합니다.

게임 기획·아트 기획·개발·AI 활용·벤치마킹·유저리서치·출시 판단을 외부 공식·현업·개발자·플레이어 근거로 개선할 때는 `docs/knowledge/game-development/README.md`에서 관련 Guide만 선택하고, `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`와 `templates/research/GAME_DEVELOPMENT_CASE_CARD.md`로 결정 질문·근거·성공/실패 사례·적용 판정·검증을 연결합니다. 이 허브는 새 Skill이 아니며 기존 Skill의 실행 책임을 대체하지 않습니다.

Windows PC와 Android 모바일을 처음부터 함께 고려하거나 STOVE·Google Play·Steam 출시 순서를 설계할 때는 `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`와 `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`를 사용합니다. 공용 게임 코어는 하나로 유지하되 입력·레이아웃·lifecycle·품질·상점 서비스는 플랫폼 어댑터로 분리하고, 실제 Android 기기·계정·테스터·지원 역량이 확인되지 않으면 동시 목표나 같은 날 공개를 강제하지 않습니다.

Steam·STOVE·Google Play의 등급·설문, 자산 상업 사용·게임 포함 배포, 오픈소스·AI·외주 계약과 이미지·사운드 등의 참조 기반 독립 제작은 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`를 사용합니다. 프로젝트별 증거는 두 project-operations Template에 기록하고, 미확인은 `RELEASE_BLOCKED_UNVERIFIED`로 유지합니다.

기존 정본 복원·작업 시작 인터뷰·Demo-First Vertical Slice·GPT→Codex·프로젝트 Sheet·중간 시각화 점검을 파일 하나로 실행하려면 `templates/prompts/VERTICAL_SLICE_INTEGRATED_EXECUTION_PROMPT_v9.md`를 사용합니다. 프로젝트 Sheet는 정확한 URL이 확인된 개별 프로젝트에서만 연결하며 Base 자체는 `BASE_EXCLUDED`입니다.

작업에 필요한 실행 파일·라이브러리·폰트·입력 파일·인증·권한이 없으면 필요한 이유, 설치·적용 방법, 확인 명령과 최소 권한을 안내합니다. 실행하지 않은 조사·검사·권한·도구는 통과로 보고하지 않습니다.

## 통합된 운영 구조

```text
요청 라우팅·요구 확정
→ 승인된 작업 계약·필요 시 실행 순서
→ 프로젝트 Sheet 의미 구조·기획 정본 연결
→ 결정 질문·분야 Coverage·외부 근거·성공/실패 Case
→ 기획 방향·GPT 시각화·이미지 검수 또는 구현·제작
→ Demo-First Vertical Slice·플레이테스트·AI Eval
→ 정본·정적·런타임·접근성·성능·회귀 검증
→ 플랫폼 등급·설문·자산 권리·참조 독립 제작 검증
→ 책임 원본·Sheet·자산 원장·현재 상태 동기화
→ 인수인계·학습·필요 시 Base 승격
```

자세한 공용 규칙과 상태·발행 정책은 [docs/OPERATING_MODEL.md](docs/OPERATING_MODEL.md)가 단일 설명 원본입니다.

## Active Skill Registry View

The current active-Skill count, list, owner, and positive/negative triggers are generated from the [Base Skill Map](docs/generated/BASE_ACTIVE_SKILLS.md). This entrypoint does not maintain a second Skill list.

- Machine authority: `skills/SKILL_REGISTRY.json` and each `SKILL.md` frontmatter
- Current human view: `docs/generated/BASE_ACTIVE_SKILLS.md`
- Historical identity: `.codex-plugin/plugin.json`, `base.lock.json`, and `skills/BASE_V9_SKILL_SNAPSHOT.json` are frozen v9.0 release derivatives, not the current routing authority
- Behavior evaluation: `skills/SKILL_BEHAVIOR_EVALS.json` and `tools/check_skill_behavior_evals.py`
- Legacy IDs: `skills/LEGACY_SKILL_ALIASES.md`

활성 Skill 수는 Registry 관찰값이며 설계 제약이 아니다. 독립 책임과 검증 경계가 확인되면 새 Skill을 추가하고, 기존 mode로 충분하면 통합한다.

## 프로젝트 GDD와 선택형 대시보드

일반 프로젝트 기획·상태 확인은 GitHub 정본과 **프로젝트 GDD Google Sheets**를 우선합니다. HTML 대시보드는 사용자가 명시적으로 요청하거나 기존 대시보드 유지보수가 필요한 경우에만 선택적으로 사용합니다.

## 프로젝트 책임 원본

```text
DESIGN_DOCUMENT_REGISTRY.json
→ 등록된 Markdown 또는 JSON 책임 원본
→ 실제 코드·데이터·자산·테스트
```

한 질문에는 현행 책임 원본 하나만 둡니다. 같은 서술을 Markdown과 JSON 양쪽에 독립 원본으로 복제하지 않습니다. 외부 벤치마크·리뷰·커뮤니티는 요구사항이나 구현 상태의 정본을 대체하지 않습니다.

각 문서는 Registry에서 발행 정책을 선택합니다.

- `source_only`: 원본과 직접 검증만 유지
- `milestone_sync`: 주요 게이트·공유 시 PDF·Manifest 동기화
- `always_sync`: 원본 변경과 같은 작업에서 PDF·Manifest 상시 동기화

DOCX와 다이어그램은 선언한 경우만 생성합니다. `CURRENT`, 자동 렌더, Codex 시각 검수, 사용자 시각 검수는 독립 상태입니다.

## 저장소 구조

```text
START_HERE.md      새 채팅·새 AI 최초 라우터
AGENTS.md          항상 적용되는 공용 실행 규칙
README.md          저장소 개요
docs/OPERATING_MODEL.md  공용 작업 구조 단일 설명 원본
docs/knowledge/game-development/  기획·아트·개발·AI·근거·플랫폼·자산 권리 공용 Guide
docs/              Method·Research·Case·체크리스트
skills/            실행 Skill·Registry·Learning Log·상세 reference
templates/research/ 근거 조사·사례 기록 템플릿
templates/project-operations/ 프로젝트 운영·자산 권리·출시 증빙 Template
templates/         프로젝트 분화·조사·실행·검증 템플릿
tools/             DOCX/PDF·다이어그램 생성기·Governance checker
tests/             운영체계·발행·라우팅·정본 최신성 회귀 테스트
[수정제안서]/      프로젝트발 Base 승격 후보·승인·구현 이력
```

## 라이선스와 보안

Base 자체는 [MIT License](LICENSE)로 배포됩니다. 저장소가 참조하거나 별도 고지한 제3자 코드·문서·자산의 라이선스는 해당 원출처와 고지를 따릅니다.

민감한 취약점은 공개 Issue에 내용을 남기지 말고 [Security Policy](SECURITY.md)의 지원 범위와 비공개 신고 경로를 따릅니다. 공개 저장소에는 unredacted 계약서·신분증·서명·개인정보를 올리지 않고 `secure_original_location`과 최소 증빙만 기록합니다.

## 개발 게이트

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval·Sequencing
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

## 로컬 검증

현재 브랜치의 전체 계약을 저장소 소유 임시 디렉터리 안에서 검증하려면 다음 단일 진입점을 사용합니다.

```bash
python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>
```

`<trusted-main-commit-sha>`에는 검증 전에 확인한 정확한 40자 main SHA를 넣고 이동 가능한 ref 이름은 넘기지 않습니다. 이 명령은 전체 회귀, 필수 CI topology, Base v9 생성물·무결성, Skill coverage, Git 공백·객체 검사를 순서대로 실행하고 첫 실패 코드를 그대로 반환합니다. LibreOffice·Poppler 또는 필수 regular/bold 폰트 중 하나라도 실제 실행 준비가 되지 않으면 발행 생성 테스트는 원인이 적힌 `SKIPPED`이며, 발행 검증이 통과한 것으로 해석하지 않습니다.
