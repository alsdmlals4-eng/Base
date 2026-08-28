# Repository-First Project Workspace Policy

## 0. 현재 상태

```text
CURRENT_OWNER: docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json
AUTHORITY_MODEL: REPOSITORY_PRIMARY_CANON
PROJECT_WORKSPACE: REPOSITORY_PRIMARY_PROJECT_CANON
HUMAN_VIEW: HUMAN_GDD_PDF_DERIVED_VIEW
AI_CANON: AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
WORK_SURFACE: CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
LIBRARY_SURFACE: CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
NOTION: LEGACY_READ_ONLY_MIGRATION_SOURCE
```

이 문서는 데스크톱 ChatGPT Work, GitHub 프로젝트 저장소, ChatGPT Library와 중간점검용 상세 기획서 PDF를 사용하는 기본 프로젝트 운영 정책이다.

핵심 변경은 단순히 Notion을 생략하는 것이 아니다. **프로젝트 정본을 저장소로 통합하고, 사람이 보는 PDF를 저장소 정본에서 생성되는 파생 검토본으로 제한하며, 이미지와 Codex 인계를 정확한 경로·commit·hash로 재구성하는 것**이다.

## 1. 권한 순서

```text
latest user decision
→ project AGENTS.md and approved current work contract
→ repository canonical Markdown / JSON / tracked assets / tests / evidence
→ exact-commit HUMAN_GDD_PDF_DERIVED_VIEW
→ CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
→ CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
→ LEGACY_READ_ONLY_MIGRATION_SOURCE when unique material remains
→ external references / historical discussion / memory
```

- `REPOSITORY_PRIMARY_CANON`: 프로젝트 기획, 결정, 시스템·데이터 의미, asset manifest, 구현 계약과 실제 구현 증거는 저장소에서 버전 관리한다.
- `REPOSITORY_PRIMARY_PROJECT_CANON`: 신규 프로젝트와 신규 Slice는 Notion 페이지 생성·갱신을 기본 작업으로 요구하지 않는다.
- 대화 기록, Work 임시 문서, Project Memory, Library의 파일 존재만으로 정본 승격을 주장하지 않는다.

## 2. 기본 산출물은 두 개다

프로젝트 통합 정리의 기본 산출물은 다음 두 종류다.

1. **사용자용 상세 기획서 PDF** — `HUMAN_DETAILED_GDD_PDF`
2. **AI용 상세 기획·구현 명세 Markdown** — `AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN`

Notion용 별도 산출물은 기본 생성하지 않는다.

### 2.1 AI용 상세 기획·구현 명세

프로젝트 저장소의 `docs/canon/AI_GAME_SPEC.md` 또는 프로젝트가 선언한 동등 owner가 소유한다. 최소 포함 범위:

- 프로젝트 정의와 판매·차별 가치;
- 플레이어 행동, 감정, 의미 있는 선택과 trade-off;
- 핵심 loop, 시스템, 콘텐츠와 진행 구조;
- UX/UI Flow와 정보·피드백 규칙;
- 데이터 의미, 상태, 입력·출력과 호환성;
- 실제 게임 소비처가 있는 이미지·사운드·VFX 요구;
- Codex가 지켜야 할 의미·보호 범위와 기술 자율 범위;
- Acceptance Criteria, automated/runtime/play/UX evidence 구분;
- 명시적 제외 범위, 미해결 결정, 위험과 재검토 조건.

### 2.2 사용자용 상세 기획서 PDF

`HUMAN_GDD_PDF_DERIVED_VIEW`: **PDF는 정본이 아니다.** 정확한 repository commit에서 생성된 사람용 검토·전달 파생물이다.

PDF에는 다음 identity를 표시한다.

```yaml
project:
milestone:
source_commit:
canon_version:
generated_at:
included_scope:
approval_status:
implementation_status:
evidence_ceiling:
unresolved_decisions:
blockers:
```

사용자가 PDF를 보고 수정한 내용은 PDF 파일 안에서 독립 정본으로 장기 유지하지 않는다. 승인된 수정은 먼저 저장소 AI canon과 결정 기록에 반영하고 readback한 뒤 새 PDF를 생성한다.

권장 생성 Gate:

1. 핵심 방향·코어 시스템 승인;
2. Codex 구현 인계 직전;
3. 의미 있는 Slice 또는 Vertical Slice 완료;
4. Release Candidate 점검.

매 작은 변경마다 PDF를 다시 만들지 않는다. PDF 생성 비용과 drift를 줄이되, 구현 인계와 주요 승인 시점에는 오래된 파생본을 사용하지 않는다.

## 3. 권장 프로젝트 정본 묶음

```text
AGENTS.md
START_HERE.md
ACTIVE_CONTEXT.md
CURRENT_CONFIRMED_DECISIONS.md
docs/canon/AI_GAME_SPEC.md
docs/handoffs/CURRENT_CODEX_HANDOFF.md
assets/ASSET_MANIFEST.json
docs/exports/HUMAN_GDD_<milestone>_<source-sha>.pdf
```

프로젝트 구조가 다르면 동등 owner를 명시할 수 있다. 같은 질문에 두 정본을 만들지 않는다.

- `ACTIVE_CONTEXT.md`: 현재 목표, 진행 상태, blocker와 다음 작업.
- `CURRENT_CONFIRMED_DECISIONS.md`: 승인된 의미 결정과 supersession.
- `AI_GAME_SPEC.md`: 사람이 승인한 기획 의미와 구현 계약.
- `CURRENT_CODEX_HANDOFF.md`: 현재 Slice의 exact implementation entrypoint.
- `ASSET_MANIFEST.json`: 실제 소비 asset의 path·consumer·approval·hash·provenance.
- `HUMAN_GDD_*.pdf`: 특정 commit의 파생 review view.

## 4. ChatGPT Work와 Library

### 4.1 Work

`CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON`

Work는 로컬 프로젝트 파일을 읽고 기획·검수·문서·이미지·PDF를 만들 수 있다. 그러나 다음 중 하나가 없으면 완료가 아니다.

- 저장소 파일로 지속화;
- exact path readback;
- commit/PR identity;
- 해당 산출물에 필요한 검증 증거.

Work 채팅에만 남은 합의는 새 세션·Codex·rollback이 안정적으로 소비할 수 없는 임시 문맥이다.

### 4.2 Library

`CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`

Library에 적합한 자료:

- 승인 전 이미지 후보와 비교 시안;
- 대용량 제작 참고 원본;
- 생성한 사용자용 PDF;
- 외부 벤치마크 자료;
- 프로젝트 저장소에 넣을 필요가 없는 임시 분석 파일.

Library에만 두면 안 되는 자료:

- 현재 구현이 소비하는 유일한 asset;
- 최신 결정의 유일한 원문;
- Codex 구현 인계의 유일한 명세;
- diff·rollback이 필요한 현재 정본.

## 5. 이미지·에셋 전달

기존 Notion attachment gate를 `REPOSITORY_PATH_MANIFEST_SHA256_READBACK`으로 대체한다.

승인 visual의 최소 fields:

```text
asset_id
repository_path
actual_consumer
approval_status
version
sha256
source_or_provenance
rights_or_license_state
implementation_status
supersedes_or_replaced_by
```

완료 Gate:

1. 실제 game consumer가 확인됨;
2. 승인 상태가 현재 사용 목적과 일치함;
3. 저장소 path에서 binary 또는 source를 읽을 수 있음;
4. SHA-256이 manifest와 일치함;
5. superseded/rejected candidate와 혼동되지 않음;
6. Codex가 exact commit에서 동일 파일을 찾을 수 있음.

대형 PSD·고해상도 제작 master처럼 runtime에 필요하지 않은 파일은 local source storage 또는 Library에 둘 수 있다. 그러나 실제 게임이 소비하는 최종 PNG/WebP/SVG/OGG 등은 프로젝트 정책과 저장소 용량 경계 안에서 추적 가능한 경로를 가져야 한다.

## 6. 신규 작업 흐름

```text
GPT Work 기획·조사·재사용 preflight
→ 필요한 벤치마킹과 적대적 검토
→ AI_PROJECT_CANON_SPEC 갱신
→ 실제 소비처가 확정된 asset/audio 준비
→ repository path + manifest + readback
→ exact source commit
→ Codex 구현 handoff
→ runtime/test/play evidence
→ GPT 최종 검수
→ repository canon/evidence 갱신
→ 의미 있는 Gate에서 HUMAN_GDD_PDF_DERIVED_VIEW 생성
```

**새 Notion 쓰기**는 기본 경로에서 **금지**한다. 사용자가 특정 프로젝트에서 Notion을 계속 쓰기로 최신 명시 결정을 내린 경우에만 project-specific override로 유지한다.

## 7. Notion과 Google Sheets 이관

Notion과 기존 Sheets는 `LEGACY_READ_ONLY_MIGRATION_SOURCE`다. 즉시 삭제하지 않고 한 번만 다음으로 분류한다.

- `UNIQUE`: 현재 저장소나 Library에 없는 고유 의미·자료.
- `DUPLICATE`: 현재 정본과 의미가 같고 source identity가 확인됨.
- `OBSOLETE`: 명시적으로 superseded·폐기되었고 active consumer가 없음.
- `BLOCKED_UNVERIFIED`: 접근·출처·프로젝트 identity가 불충분함.

```text
legacy source inventory
→ UNIQUE | DUPLICATE | OBSOLETE | BLOCKED_UNVERIFIED
→ UNIQUE만 올바른 repository canon / tracked asset / non-canon Library reference로 이동
→ provenance 보존
→ destination_readback
→ active consumer 확인
→ legacy source를 read-only로 유지
```

자료를 읽지 못했다는 이유로 `DUPLICATE`나 `OBSOLETE`로 추정하지 않는다. 이관 증거가 없는 삭제는 금지한다.

### 7.1 프로젝트별 Notion 퇴역 완료 조건

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

세 값이 모두 0이고 destination readback이 완료되어야 해당 프로젝트가 Notion dependency를 제거했다고 보고한다.

Base 공용 정책 전환은 개별 프로젝트의 위 값이 0임을 자동 증명하지 않는다. 프로젝트를 다음에 작업할 때 targeted migration audit를 수행한다.

## 8. Legacy compatibility와 supersession

다음 과거 token과 문서는 이관·rollback·학습을 위한 `LEGACY_DISCOVERY_ONLY` 자료로 남을 수 있다.

```text
NOTION_DEFAULT_PROJECT_WORKSPACE
NOTION_HUMAN_FACING_CANON
CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP
```

과거 token이 검색된다는 이유만으로 **현재 기본값으로 복원하지 않는다**. 현재 root `AGENTS.md`와 `docs/operations/REPOSITORY_FIRST_PROJECT_WORKSPACE_CONTRACT.json`이 더 높은 current owner다.

`NOTION_DEFAULT_PROJECT_WORKSPACE_LEGACY_ALIAS`는 오래된 문서·테스트·인수인계의 의미를 찾기 위한 별칭이지 신규 write route가 아니다.

## 9. 검증과 완료

정적 계약 PASS와 실제 프로젝트 이관 완료는 별도 claim이다.

- Base policy/test PASS: 공용 기본 경로가 repository-first임을 증명.
- Project migration PASS: 해당 프로젝트 unique material과 dependency counts가 0임을 증명.
- Asset delivery PASS: path·manifest·SHA·consumer가 일치함을 증명.
- Runtime PASS: 실제 Godot 실행·test·play evidence가 증명.
- UX/Player PASS: 별도 사람 또는 허용된 관찰 evidence가 증명.

병합 후에는 `POSTMERGE_REPOSITORY_AND_DERIVED_VIEW_READBACK_LOOP`로 current main, owner path, template, tests와 남은 legacy migration을 다시 확인한다.

## 10. 비용·보안·롤백

- 기본 경로는 `ZERO_INCREMENTAL_COST`다.
- ChatGPT Pro 외 별도 유료 Notion·storage·API·SaaS를 필수화하지 않는다.
- 공개 저장소에 private source, 계약서, 개인정보나 비공개 asset master를 넣지 않는다.
- rollback은 machine contract, policy, templates, root routing, focused test를 한 단위로 revert한다.
- 이 전환은 기존 Notion 자료를 삭제하지 않으므로 Base 정책 rollback에 페이지 복원 작업이 필요하지 않다.
