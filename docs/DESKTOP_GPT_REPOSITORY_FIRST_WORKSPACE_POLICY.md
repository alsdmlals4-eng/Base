# Desktop GPT Repository-First 프로젝트 작업 정책

## 0. 상태·목적·적용 우선순위

- Policy ID: `DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE`
- 상태: `ACTIVE_DEFAULT`
- 발효일: `2026-08-28`
- 기계 계약: `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT_V4.json`
- 발행 계약: `docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`
- 이관 체크리스트: `templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md`

이 정책은 Desktop GPT Work를 중심으로 프로젝트 기획·조사·검수·시각자료 제작을 수행하는 1인 개발 흐름에서 불필요한 Notion 중간 복제와 이중 readback을 제거한다.

현재 프로젝트 기본값은 다음이다.

```text
REPOSITORY_PRIMARY_CANON
APPROVED_HUMAN_BLUEPRINT_PDF_CANON
AI_PRODUCTION_SPEC_MARKDOWN
CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON
CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA
APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST
NO_NEW_NOTION_WRITE_BY_DEFAULT
NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE
```

사용자의 최신 지시와 대상 프로젝트의 최신 `AGENTS.md`·승인 Decision·실제 구현 사실이 이 공용 정책보다 우선한다. 다만 프로젝트별 예외가 없다면 이 문서와 V4 machine contract가 새 작업의 기본 route다.

기존 `docs/operations/PROJECT_WORKSPACE_AUTHORITY_CONTRACT.json` V3와 과거 Notion 운영 문서는 삭제하지 않는다. 해당 자료는 `V3_COMPATIBILITY_AND_HISTORY_ONLY`이며 새 작업의 active authority가 아니다.

---

## 1. 정본과 작업면

| Surface | 현재 역할 | 정본 여부 | 필수 사용 |
|---|---|---:|---:|
| 프로젝트 GitHub repository | 기획·결정·데이터·승인 runtime asset·코드·Scene·Resource·Test·Evidence | **Primary canon** | 예 |
| 사용자용 상세 기획서 PDF | 사람이 전체 기획·핵심 시스템·콘텐츠·구현 원리를 검토하고 승인한 시각 baseline | **승인·등록 후 사람용 시각 정본** | 의미 있는 Gate에서 |
| AI용 상세 기획·구현 명세 Markdown | GPT/Codex가 이어받는 구조화 production spec | repository canon | 예 |
| Desktop GPT Work | 기획·조사·검수·문서·시각자료 제작 실행면 | 아님 | 기본 실행면 |
| ChatGPT Library | 시안·참고자료·원본 템플릿·PDF 보관 | 아님 | 선택 |
| Notion | 기존 고유 자료 발견·이관·감사를 위한 legacy source | 아님 | 기존 자료가 있을 때만 |
| Google Sheets | 미이관 고유 자료용 migration compatibility source | 아님 | 선택 |
| Figma/HTML dashboard | 명시적 프로젝트 예외가 있을 때의 보조 surface | 아님 | 아니오 |

### 1.1 `REPOSITORY_PRIMARY_CANON`

프로젝트에서 현재라고 주장하는 정보는 repository의 추적 가능한 파일과 exact commit으로 복원 가능해야 한다.

repository가 소유하는 범위:

- `AGENTS.md`, Start Here, Active Context, 승인 Decision
- 사람·AI가 공유하는 기획 의미와 구현 계약
- 구조화 표·밸런스·콘텐츠·Flow 데이터
- 승인된 실제 runtime asset과 asset manifest
- GDScript, Scene, Resource, runtime configuration
- automated test, runtime/play evidence, QA receipt
- Codex handoff와 구현 결과 readback

채팅, memory, Library-only candidate PDF, 미등록 PDF와 Notion preview에만 존재하는 정보는 current project canon으로 승격하지 않는다. 사용자 승인과 repository manifest 등록을 마친 PDF는 사람용 시각·검수 영역의 정본이다.

### 1.2 `CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON`

Desktop GPT Work는 로컬·연결 저장소 파일을 읽고 기획·검수·제작을 수행하는 실행면이다. Work 결과는 다음 중 하나로 materialize해야 지속 가능한 결과가 된다.

- repository의 Markdown·JSON·CSV·SVG·asset·test·evidence
- repository 정본에서 생성된 사용자용 PDF
- 정본이 아닌 참고자료로 명시된 Library 파일

채팅이 길어지거나 새 채팅으로 전환되어도 repository의 진입점만 fresh-read하면 같은 품질로 재개할 수 있어야 한다.

### 1.3 `CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON`

Library에 적합한 항목:

- 승인 전 이미지 시안과 비교 후보
- 제작 원본 또는 대용량 참고자료
- 생성된 사용자용 PDF
- 벤치마크 원문·일회성 분석 파일
- 반복 사용 템플릿

Library에만 두면 안 되는 항목:

- 현재 승인 Decision의 유일한 사본
- Codex가 구현에 소비할 runtime binary
- diff·rollback이 필요한 기획 정본
- 현재 구현 완료를 판정하는 유일한 evidence

---

## 2. 기본 작업 흐름

```text
Desktop GPT Work
→ targeted fresh-read: Project AGENTS / Active Context / Decisions / actual implementation
→ 최소 기획·필요한 benchmark·재사용 조사
→ 적대적 검토·IRG
→ repository 기획 정본과 구현 계약 갱신
→ PR·diff·test·readback
→ 필요 Gate에서 사용자용 상세 PDF 생성
→ 사용자 검토 결과를 repository 정본에 반영
→ exact repository SHA로 Codex 인계
→ Godot 구현·test·runtime/play evidence
→ GPT 최종 검수
→ repository 정본 상태 승격
```

삭제되는 기본 단계:

```text
Work 결과를 Notion에 중간 복제
→ Notion page/database/attachment readback
→ 같은 의미를 repository에 다시 작성
→ Codex가 GitHub와 Notion의 최신성을 재판정
```

### 2.1 필수 진입점

프로젝트 규모에 따라 경로는 조정할 수 있으나 다음 역할은 반드시 식별 가능해야 한다.

```text
AGENTS.md

docs/START_HERE.md
docs/ACTIVE_CONTEXT.md
docs/canon/CURRENT_CONFIRMED_DECISIONS.md
docs/design/PROJECT_AI_PRODUCTION_SPEC.md
docs/handoffs/CURRENT_CODEX_HANDOFF.md

assets/ASSET_MANIFEST.json
```

경로가 다르면 `AGENTS.md` 또는 `START_HERE.md`에서 actual owner를 명시한다. 빈 형식을 맞추기 위해 파일을 억지로 복제하지 않는다.

### 2.2 권장 repository 구조

```text
project-root/
├─ AGENTS.md
├─ docs/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ canon/
│  │  ├─ CURRENT_CONFIRMED_DECISIONS.md
│  │  └─ ...
│  ├─ design/
│  │  ├─ PROJECT_AI_PRODUCTION_SPEC.md
│  │  └─ ...
│  ├─ handoffs/
│  │  └─ CURRENT_CODEX_HANDOFF.md
│  ├─ research/
│  ├─ reviews/
│  └─ exports/
│     └─ [PROJECT]_MASTER_PRODUCTION_GDD_[DATE].pdf
├─ data/
├─ assets/
│  ├─ runtime/
│  └─ ASSET_MANIFEST.json
├─ scenes/
├─ scripts/
├─ tests/
└─ evidence/
```

이 구조는 역할 예시다. 실제 Godot 프로젝트의 기존 정상 구조와 importer 요구를 무시하고 강제 이동하지 않는다.

---

## 3. 두 발행 산출물

`docs/PROJECT_MASTER_GDD_TWO_ARTIFACT_POLICY.md`의 `EXACTLY_TWO_DELIVERABLES`를 전역 기본 발행 profile로 사용한다.

1. `HUMAN_MASTER_GDD_PDF`
2. `AI_PRODUCTION_SPEC_MARKDOWN`

코드·Scene·Resource·JSON·asset·test·evidence는 프로젝트 구현 정본이며 “사용자에게 전달하는 별도 기획 산출물” 수에 포함하지 않는다.

### 3.1 `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`

사용자용 PDF는 프로젝트 전체를 사람이 이해하고 중간점검하는 시각 중심 상세 기획서다. 사용자 승인과 manifest 등록을 마치면 사람용 시각·검수 영역의 불변 정본이다.

`APPROVED_PDF_IS_HUMAN_VISUAL_CANON`

PDF 필수 metadata:

```yaml
project:
document_type: HUMAN_MASTER_GDD_PDF
source_commit:
canon_version:
generated_at:
included_scope:
implementation_evidence_ceiling:
approval_status:
```

규칙:

- PDF는 exact `source_commit`의 repository 정본에서 생성한다.
- PDF에서 발견한 수정사항은 repository owner 문서·데이터에 반영한 뒤 다시 생성한다.
- PDF 주석은 `PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION`이며 repository owner에 반영하고 새 PDF를 승인·등록하기 전에는 current Decision을 변경하지 않는다. superseded 다운로드 파일은 current PDF canon으로 해석하지 않는다.
- 문서 생성 성공은 runtime·UX·player·release PASS가 아니다.
- 시각자료는 이해에 필요한 위치에 통합하며 별도 이미지 번들·부록을 기본 생성하지 않는다.

권장 생성 Gate:

- 코어 방향과 핵심 시스템 확정
- Codex 구현 인계 직전
- 의미 있는 Vertical Slice 또는 milestone 완료
- Release Candidate 점검

매 작은 수정마다 PDF를 재발행하지 않는다. repository diff가 일상 검토 수단이고 PDF는 통합 점검 수단이다.

### 3.2 `AI_PRODUCTION_SPEC_MARKDOWN`

AI용 상세 기획·구현 명세는 repository에 저장한다. 최소한 다음을 추적한다.

- player fantasy, 목표 감정, 의미 있는 선택, 보상과 기억
- core loop, session/meta loop, 실패·복구
- 시스템 ID, 규칙, 입력·출력, 상태·데이터 의미
- 핵심 콘텐츠 ID, 등장·해금·상호작용·밸런스 경계
- UI/UX Flow와 실제 화면 소비처
- Visual/Audio requirement와 승인 상태
- Godot 구현 책임 경계와 의존성
- acceptance, automated/runtime/UX evidence ceiling
- approved scope, non-scope, protected scope
- Decision·asset·test·Scene·script traceability

이 파일은 구현을 대신하지 않으며 실제 코드 구조와 충돌하면 current repository implementation을 읽고 reconciliation한다.

---

## 4. 이미지·시각자료·에셋

### 4.1 실제 소비처 기준

이미지 제작은 실제 화면·Scene·UI·오브젝트·상태에서 플레이어가 보고 판단하는 소비처를 먼저 식별한다. 캐릭터 한 장이 아니라 방향·애니메이션·피격·사망·선택 상태, UI 한 장이 아니라 기본·hover·pressed·disabled·locked·warning 상태처럼 실제 consumer family를 추적한다.

Flow map·Visual Bible·관계도·설명용 diagram은 제작/AI용 시각자료다. runtime asset과 혼동하지 않되 사람용 PDF와 AI spec에 필요한 이해 자료로 포함할 수 있다.

### 4.2 `APPROVED_REPOSITORY_PATH_SHA256_AND_MANIFEST`

Codex가 소비하는 승인 이미지는 다음을 만족해야 한다.

```text
actual approved binary
+ project-controlled repository_path
+ SHA-256
+ actual consumer
+ approval_status
+ implementation_status
+ provenance
+ readback
```

`assets/ASSET_MANIFEST.json`의 최소 필드:

```json
{
  "asset_id": "...",
  "consumer": "...",
  "repository_path": "...",
  "sha256": "...",
  "approval_status": "APPROVED",
  "implementation_status": "READY | INTEGRATED | VERIFIED",
  "provenance": "..."
}
```

상태 상한:

- 채팅이나 Library에 생성됨: `GENERATED_CANDIDATE`
- 사용자가 시각적으로 승인함: `APPROVED_VISUAL`
- repository binary·hash·manifest readback 완료: `IMPLEMENTATION_READY`
- Godot 실제 consumer에 연결됨: `INTEGRATED`
- 실행 화면·상태 전환 검증 완료: `RUNTIME_VERIFIED`

이전 단계가 다음 단계를 자동 보장하지 않는다.

### 4.3 대용량 제작 원본

대형 PSD·고해상도 source master·반복 후보를 무조건 일반 Git에 넣지 않는다.

- 실제 게임이 소비하는 최종 PNG/WebP/SVG/OGG/WAV 등: repository
- 대용량 제작 원본: 프로젝트 로컬 source 경로 또는 Library 등 명시적 non-canon 보관
- 구현에 필요 없는 후보: Library
- hash·provenance·원본 위치: manifest 또는 asset record

Git LFS나 별도 storage는 실제 크기·clone·build·협업 문제를 확인한 뒤 도입한다. 새 유료 저장공간이나 별도 과금은 사용자 승인 전 추가하지 않는다.

---

## 5. Codex 인계

`CODEX_REHYDRATE_REPOSITORY_AT_EXACT_SHA`

Codex 작업지시문은 최소 다음을 포함한다.

```yaml
repository:
base_branch:
exact_source_sha:
project_agents:
active_context:
confirmed_decisions:
ai_production_spec:
current_handoff:
asset_manifest:
approved_scope:
explicit_non_scope:
protected_scope:
acceptance:
required_runtime_evidence:
```

Codex는 다음을 하지 않는다.

- 채팅 기억을 repository보다 최신 정본으로 가정
- PDF만 읽고 구현 의미를 확정
- Library·Notion preview 이미지를 runtime asset으로 직접 소비
- missing asset을 임의 생성·대체
- exact SHA가 이동했는데 stale handoff로 구현 지속

필요한 시각물이 없으면 `GPT_VISUAL_REQUEST`로 반환한다. GPT가 제작·검수·사용자 승인 후 repository binary와 manifest를 materialize한 다음 Codex가 다시 소비한다.

---

## 6. Notion 퇴역·이관

### 6.1 기본 상태

`NO_NEW_NOTION_WRITE_BY_DEFAULT`

발효일 이후 신규 기획·결정·이미지 승인·Codex handoff를 완료하기 위해 Notion에 중간 복제하지 않는다.

`NOTION_LEGACY_READ_ONLY_MIGRATION_SOURCE`

기존 프로젝트에서 Notion에만 있는 고유 정보가 발견되면 해당 범위만 읽어 repository 또는 명시적 non-canon 보관소로 이관한다. 이관 중 Notion은 `LEGACY_READ_ONLY`로 유지한다.

다음은 금지한다.

- repository에 없는 자료가 남았는지 확인하지 않고 Notion 삭제
- 미리보기 이미지로 원본 binary 이관 완료 주장
- 표의 열·relation·상태 의미를 평문 요약으로 축소하고 완료 주장
- 오래된 Notion 항목을 current Decision으로 자동 승격
- 이관 편의를 이유로 신규 Notion DB·중간페이지를 다시 확장

### 6.2 이관 완료 Gate

프로젝트별로 다음 세 값이 모두 0이어야 active dependency 제거를 완료했다고 판정한다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

정의:

- `NOTION_UNIQUE_CANON_COUNT`: repository·명시적 보관소에 원문 의미와 provenance가 없는 고유 항목 수
- `CODEX_NOTION_DEPENDENCY_COUNT`: 구현 시작·재개·asset 회수에 Notion 조회가 필수인 경로 수
- `ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT`: 완료 계약이 여전히 Notion 쓰기/readback을 요구하는 활성 규칙 수

모두 0이 되면 상태를 `NOTION_RETIRED_FROM_ACTIVE_FLOW`로 기록할 수 있다.

`NO_DELETE_REQUIRED_FOR_RETIREMENT`

퇴역은 삭제와 다르다. 기존 workspace는 감사·rollback·누락 재검사를 위해 read-only로 남겨도 된다. 삭제는 별도 사용자 지시와 backup/readback 증거가 있을 때만 수행한다.

### 6.3 이관 대상별 기본 변환

| Notion 자료 | repository 또는 보관 대상 |
|---|---|
| 프로젝트 개요·핵심 시스템·콘텐츠 | AI production spec Markdown |
| 확정 Decision | CURRENT_CONFIRMED_DECISIONS 또는 decision log |
| 표·밸런스·콘텐츠 DB | JSON/CSV/Markdown table + schema 설명 |
| Flow·상태도 | Mermaid/SVG/Markdown + source 의미 |
| 이미지·파일 | 원본 binary + SHA-256 + manifest/provenance |
| Home 시각 요약 | 사람용 상세 PDF의 해당 장 |
| 작업 상태 | ACTIVE_CONTEXT / handoff |
| 구현 증거 | repository evidence 경로 |
| 중복·폐기 후보 | legacy audit receipt에 분류, 자동 승격 금지 |

---

## 7. 예외

Notion을 다시 active surface로 사용하는 프로젝트 예외는 다음을 모두 충족해야 한다.

1. 사용자 명시 승인
2. repository-first 방식으로 충족하기 어려운 실제 장기 가치
3. 대상 프로젝트·자료 범위·owner 명시
4. 정본 충돌 방지 규칙
5. 비용과 connector 의존성
6. 종료 또는 재검토 조건

유효할 수 있는 예:

- 외부 팀원·퍼블리셔와 실시간 공동편집이 필수
- 비개발자가 관계형 데이터베이스를 직접 유지
- 항상 최신인 공개 웹 프로젝트 페이지가 계약상 필요
- 명시적 프로젝트 고유 운영 계약

“예전에 사용했다”, “보기에 익숙하다”, “이미 페이지가 있다”만으로 기본 경로를 복원하지 않는다.

---

## 8. 기존 계약과의 compatibility

### 8.1 V3 Notion 계약

```text
NOTION_DEFAULT_PROJECT_WORKSPACE_RETIRED
V3_COMPATIBILITY_AND_HISTORY_ONLY
```

기존 V3 contract와 Notion 문서는 과거 결정·이관 source·회귀 보호를 위해 남긴다. 새 작업은 root `AGENTS.md`가 V4 contract로 라우팅한다.

`PROJECT_RELATION_REQUIRED`는 기존 Notion record 이관 시 project provenance를 보존하기 위한 legacy migration rule로 사용할 수 있으나 새 repository 정본의 필수 relation 모델이 아니다.

### 8.2 이전 postmerge alias

`POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP_RETIRED`는 과거 테스트·문서 호환을 위한 이름이다. 새 active loop는 다음이다.

`POSTMERGE_REPOSITORY_ARTIFACT_ADVERSARIAL_PROGRESS_LOOP`

검사 대상:

- merged repository exact SHA
- 정본 경로·Decision·asset manifest readback
- 파생 PDF의 source SHA와 evidence ceiling
- Codex handoff freshness
- runtime/test/UX evidence의 실제 상한
- Notion migration counter와 남은 고유 자료

Notion write/readback 자체는 완료 조건이 아니다.

---

## 9. 완료·증거·롤백

### 9.1 작업 완료 증거

Base 정책 교정 완료와 프로젝트별 이관 완료를 분리한다.

- Base 정책 교정: V4 owner·root routing·test·PR·postmerge readback
- 프로젝트 이관: 프로젝트별 inventory·binary/hash·canon/path·counter readback
- PDF 점검: exact source SHA·시각 검토·수정 반영
- 구현 완료: Codex exact SHA·test·runtime/play/UX evidence

하나의 PASS를 다른 층의 PASS로 확대하지 않는다.

### 9.2 장기 기대효과

- Work→Notion→repository 이중 작성 제거
- 최신성 판정 surface 감소
- exact SHA·diff·rollback 강화
- Codex 인계의 경로·asset 회수 안정화
- 새 채팅 재개 시 memory 의존 감소
- 사람용 시각 검토는 PDF milestone로 집중
- 기존 자료는 read-only migration gate로 손실 방지

### 9.3 Trade-off

- 기존 Notion-only 자료를 프로젝트별로 한 번 감사·이관해야 한다.
- 비개발자 실시간 공동편집은 repository/PDF만으로 불편할 수 있다.
- 대형 제작 원본의 보관 규칙을 프로젝트별로 명시해야 한다.
- PDF는 실시간 dashboard가 아니므로 source SHA 확인이 필수다.

### 9.4 Rollback

새 기본 경로에 blocking 문제가 확인되면 V4 active route를 단일 변경 단위로 revert한다. V3와 기존 Notion workspace를 삭제하지 않았으므로 rollback은 자료 손실 없이 가능해야 한다.

정책을 되돌리더라도 이미 repository에 이관한 정본·binary·hash·evidence를 삭제하거나 Notion-only 구조로 역이관하지 않는다.


<!-- FEDERATED_DUAL_CANON_CORE_CONTRACT -->

## Federated repository + approved PDF dual canon

```text
FEDERATED_DUAL_CANON_SINGLE_FACT_OWNER

REPOSITORY_EXECUTION_DATA_CANON
APPROVED_HUMAN_BLUEPRINT_PDF_CANON
ONE_EDITABLE_OWNER_PER_ATOMIC_FACT
```

`REPOSITORY_EXECUTION_DATA_CANON`는 코드·Scene·Resource·asset·구조화 데이터·ID·수치·공식·조건·상태 전이·Decision source·작업 상태·test·runtime·release evidence의 **편집 가능한 정본**이다. `APPROVED_HUMAN_BLUEPRINT_PDF_CANON`은 사용자가 실제로 검토·승인한 프로젝트/플레이어 경험 지도, 읽기 순서, Flow 구성, 정보 우선순위, 시스템 카드 표현, milestone 범위와 시각적 baseline의 **불변 정본**이다.

PDF는 두 번째 editable database가 아니다.

```text
PDF_STRUCTURED_CONTENT_IS_REPOSITORY_PROJECTION
PDF_PROGRESS_STATUS_IS_REPOSITORY_PROJECTION
PDF_ANNOTATION_IS_CHANGE_REQUEST_NOT_CANON_MUTATION
NO_PARALLEL_BLUEPRINT_STATUS_CANON
```

PDF에 표시되는 ID·수치·규칙·완료 상태·evidence locator는 repository owner에서 생성한다. PDF에서 직접 체크하거나 수치를 고친 것은 변경 요청이며, repository owner 반영 → 새 exact-SHA candidate 생성 → predecessor 비교 → 사용자 승인 → manifest 등록을 거쳐야 정본 변경이 완료된다.

### PDF 정본 승격

```text
GENERATED_CANDIDATE
→ USER_APPROVED_PENDING_REGISTRATION
→ USER_APPROVED_AND_MANIFEST_REGISTERED
→ CANON_ALIGNED
```

`CANDIDATE_PDF_NOT_CANON`. 승인 PDF는 최소 `source_commit`, `pdf_sha256`, `approval_ref`, `approved_at`, `canonical_status`, `supersedes_pdf_ref`, `pdf_canon_manifest_ref`, included scope와 evidence ceiling을 가진다. 프로젝트별 실제 locator는 `AGENTS.md` 또는 publication owner가 지정하며, 기본 예시는 `docs/blueprint/BLUEPRINT_CANON_MANIFEST.json`과 versioned `exports/*_APPROVED.pdf`다.

```text
APPROVED_PDF_IMMUTABLE_NEW_VERSION_REQUIRED
NEW_VERSION_NEW_HASH_KEEP_HISTORY
```

승인 PDF를 덮어쓰지 않는다. 새 승인본은 새 version·filename·SHA-256으로 등록하고 이전 승인본을 `SUPERSEDED`로 남긴다. 반복 candidate와 임시 render를 모두 Git에 보존할 의무는 없지만, current/superseded 승인 baseline의 locator와 hash history는 보존한다.

### 정본 정렬과 충돌

```text
CANON_ALIGNED
REPOSITORY_ADVANCED_PDF_REVIEW_REQUIRED
PDF_FEEDBACK_PENDING_REPOSITORY_REFLECTION
CANON_CONFLICT
SUPERSEDED
```

- 구조화 값이 다르면 repository owner가 해당 값을 소유하고 PDF를 current로 취급하지 않으며 재생성한다.
- 승인된 Flow·화면 hierarchy·정보 우선순위·사람용 표현과 구현이 다르면 구현을 자동 정본으로 승격하지 않는다. 구현을 교정하거나 새 PDF candidate의 delta를 사용자에게 보여 재승인한다.
- 동시에 해결되지 않은 차이는 `CANON_CONFLICT`다.
- `CANON_CONFLICT_BLOCKS_COMPLETION_AND_RELEASE`.
- 문서 생성, static test, machine test, runtime, UX/Human, PDF 사용자 승인과 release 승인은 서로 다른 evidence다.
