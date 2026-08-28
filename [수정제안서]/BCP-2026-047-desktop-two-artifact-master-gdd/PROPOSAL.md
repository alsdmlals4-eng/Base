# BCP-2026-047 · Desktop GPT 2파일 통합 제작 기획서 프로필

## 출처와 상태

- 출처: Desktop GPT를 중심으로 프로젝트 정본을 재구성할 때 Notion 신규 출력 없이 사람용 PDF와 AI용 repository 명세만 유지하려는 사용자 운영 결정
- 기준 Base: `7cfc75d607d1ed4d0f8323d4389e64da93df00c8`
- 제출일: `2026-08-28`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `사용자 승인 운영 요구 + current Base 책임 충돌 확인 + 구현 전 계약`
- 승인 근거:
  - 사용자 메시지: `사용자용(사람) 기획서 pdf 파일과 ai용 기획서 2개만 만들면 될거같아`
  - 사용자 메시지: `사용자용 pdf파일만 다운 받을 수 있게하고 핵심 시스템 및 컨텐츠 그리고 그걸 어떻게 구현할지 상세하게 알 수 있어야해`
  - 후속 사용자 메시지: `좋아 base 교정도 진행해주고 작업지시문 다운 받을 수 있게 해줘`

## 관찰과 증거

현재 Base의 기본 `DOMAIN_SPLIT_CANON`은 프로젝트 일반 운영에서 다음을 전제한다.

- Notion은 사람이 읽고 비교·수정하는 프로젝트 개요·기획·시각·표·Flow/Storyboard의 기본 사람용 정본이다.
- Repository는 Markdown·JSON·game data·code·scene·resource·test·runtime evidence의 구조화·구현 정본이다.
- 등록된 publication policy가 PDF·선택 DOCX·Manifest를 파생 발행한다.

이 기본 모델은 지속적인 공동 편집과 Notion 중심 운영에는 유효하다. 그러나 Desktop GPT가 repository와 로컬 파일을 직접 다루고, 사용자가 프로젝트를 읽는 최종 surface를 하나의 상세 PDF로 고정하려는 작업에서는 다음 중복이 생긴다.

1. 사람용 Notion projection과 사람용 PDF가 같은 프로젝트 설명·시각·표를 중복 소유한다.
2. Notion 갱신·readback이 실제 필요 없이 master GDD 생성의 완료 조건이 된다.
3. DOCX·별도 부록·ZIP·이미지 묶음이 사용자에게 필요하지 않아도 관성적으로 산출물 후보가 된다.
4. 사용자용 문서가 소개·요약 수준으로 축소되면 핵심 시스템·콘텐츠·Godot 구현 원리를 이해할 수 없다.
5. AI용 문서가 단순 요약이면 Codex가 상태 전이·데이터·씬·스크립트·신호·테스트 계약을 복원할 수 없다.
6. PDF와 AI 명세의 시스템·콘텐츠 ID 또는 기준 SHA가 어긋나면 두 산출물이 같은 시점을 설명하지 못한다.

따라서 전역 Notion 권위를 제거하는 것이 아니라, 사용자가 명시적으로 선택한 master-GDD 작업에만 적용되는 bounded profile이 필요하다.

## 일반화 후보

### 1. `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`

사용자가 프로젝트 정본을 상세 통합 기획서로 정리하면서 2파일 구성을 명시하면 다음 profile을 사용한다.

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN
```

이 profile은 전체 프로젝트 운영체계의 Notion 사용을 자동 폐기하지 않는다. 적용 범위는 해당 master-GDD 생성·갱신 작업과 사용자가 명시적으로 같은 운영 방식을 채택한 프로젝트에 한정한다.

### 2. `HUMAN_MASTER_GDD_PDF`

사람용 PDF는 단순 소개서가 아니라 시각자료가 포함된 상세 제작 기획서다.

필수 내용:

- 프로젝트 비전·플레이어 약속·핵심 감정·선택·차별점·판매 포인트
- Core / Session / Meta Loop와 전체 game flow
- 핵심·서브 시스템의 목적, 규칙, 상태, 예외, 피드백, 의존성
- 핵심 콘텐츠의 역할, 등장 조건, 변주, 보상, 요구 에셋
- 각 시스템·콘텐츠를 Godot에서 구현하는 씬·노드·스크립트 책임·데이터 소유·신호·상태 전이·저장·로드·구현 순서
- UI/UX·입력·접근성·Visual Bible·runtime asset/audio consumer
- 현재 구현·자동 테스트·runtime·UX 검증 상태와 남은 범위
- benchmark `ADOPT / ADAPT / REJECT` 결과와 출처
- 기준 branch·repository SHA·문서 생성일

PDF는 특정 SHA 시점의 사람용 snapshot이며 독립 runtime canon이 아니다.

### 3. `AI_PRODUCTION_SPEC_MARKDOWN`

AI용 문서는 repository에 저장하는 구조화 기획·구현 계약이다. 기본 권장 경로는 다음이다.

```text
docs/design/PROJECT_AI_PRODUCTION_SPEC.md
```

필수 내용:

- Canon Snapshot과 Source Registry
- 공통 ID registry (`SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC`)
- 시스템·콘텐츠 규칙과 상태 머신
- 데이터 field/type/default/range/owner 계약
- scene·node·script responsibility map
- signal/event payload와 호출 흐름
- UI 상태·asset/audio consumer
- save/load·platform·performance 영향
- 구현 순서·의존성·Acceptance Criteria
- automated/integration/Godot runtime/UX verification 계약
- 구현·검증·출시 상태의 evidence ceiling

AI 문서는 기획·구현 명세의 active owner가 될 수 있지만 실제 code·scene·resource·game data·test·runtime evidence를 대신하지 않는다.

### 4. `NOTION_INPUT_ONLY_NO_OUTPUT`

이 profile에서 Notion은 신규 출력·갱신·readback 완료 조건이 아니다.

- 기존 Notion에 repository로 이관되지 않은 고유 정본이 남아 있으면 입력 자료로만 fresh-read한다.
- 같은 내용을 새 Notion page/database로 재생성하지 않는다.
- master GDD 완료를 위해 Notion write·upload·sync·readback을 요구하지 않는다.
- Notion-only 고유 정보가 사용되면 AI 명세의 Source Registry와 migration gap에 출처와 이관 필요성을 기록한다.
- 일반 프로젝트 작업에서 사용자가 Notion 정본 운영을 계속 요구하면 기존 `DOMAIN_SPLIT_CANON`이 유지된다.

### 5. `PDF_ONLY_USER_DOWNLOAD`

최종 사용자 응답의 다운로드 링크는 사람용 PDF 하나만 제공한다.

AI Markdown은 사용자 다운로드 링크를 제공하지 않고 다음만 보고한다.

- repository path
- branch
- commit SHA
- PR
- validation result

### 6. 산출물 제한

```text
NO_DOCX_NO_ZIP_NO_SEPARATE_APPENDIX
NO_SEPARATE_IMAGE_BUNDLE
NO_NOTION_OUTPUT
NO_AUTOMATIC_IMAGE_GENERATION
```

필요한 부록·traceability·benchmark·asset matrix는 두 파일 내부에 통합한다. 승인된 기존 이미지와 실제 build capture를 우선 사용하며, 승인 visual이 없으면 누락 상태를 표시한다. 새 이미지 생성은 사용자의 별도 명시적 요청이 있을 때만 진행한다.

### 7. 동일 시점·동일 ID 계약

```text
SHARED_ID_AND_SOURCE_SHA_REQUIRED
```

- PDF와 AI Markdown은 동일한 시스템·콘텐츠·UI·에셋 ID를 사용한다.
- 두 파일에 동일한 기준 branch와 source SHA를 기록한다.
- `DOCUMENTED`, `CONFIRMED`, `IMPLEMENTED`, `AUTOMATED_TEST_PASS`, `RUNTIME_VERIFIED`, `UX_VERIFIED`, `RELEASE_READY`를 분리한다.
- PDF 생성 시 AI 명세·실제 repository 상태와 충돌을 검사한다.

## 프로젝트 전용으로 남길 내용

- 프로젝트명·장르·세계관·인물·콘텐츠·수치·경제·밸런스
- 실제 repository path와 scene/script/resource/data/test 구조
- 프로젝트별 PDF 파일명·표지·시각 방향·승인 이미지
- 프로젝트별 시스템·콘텐츠 ID와 Acceptance Criteria
- 현재 open/draft PR, 구현 상태, runtime evidence
- 프로젝트가 Notion 운영을 완전히 중단할지 여부
- 프로젝트별 publication generator와 PDF 저장 경로

## 적용 조건과 비사용 조건

적용:

- 사용자가 사람용 PDF와 AI용 repository Markdown의 정확히 2개 결과를 요구할 때
- Desktop GPT가 프로젝트 정본·시각자료·구현 현실을 재구성해 master GDD를 만들 때
- 사용자에게 하나의 읽기용 PDF만 다운로드로 제공해야 할 때
- AI/Codex가 이어받을 상세 구현 계약이 repository에 필요할 때

비사용 또는 축소:

- 사용자가 Notion을 계속 사람용 정본·공동 편집면으로 유지하라고 명시한 일반 프로젝트 작업
- 단일 기능 Spec, 짧은 Decision 수정, 일반 handoff, runtime 버그 수정처럼 master GDD가 아닌 작업
- 외부 제출처가 DOCX·별도 ZIP·별도 appendix를 요구하는 경우
- repository나 기존 정본에 접근할 수 없어 두 산출물의 동일 SHA·ID·구현 상태를 검증할 수 없는 경우

## 반례와 위험

- 이 profile을 전역 Notion 폐기로 해석하면 기존 프로젝트의 미이관 사람용 정본과 승인 visual을 잃을 수 있다. 적용 범위를 명시적으로 제한한다.
- PDF만 남기면 변경 추적과 AI 구현 계약이 약해진다. AI Markdown을 repository active owner로 함께 유지한다.
- AI Markdown을 runtime truth로 과장하면 코드·씬·데이터와 drift가 생긴다. 실제 구현 파일과 테스트가 항상 최종 구현 사실이다.
- PDF가 시각적으로 풍부해도 시스템·콘텐츠의 구현 설명이 빠지면 제작 기획서 목적을 달성하지 못한다.
- PDF와 AI 문서가 서로 다른 SHA 또는 ID를 사용하면 같은 프로젝트 상태를 설명하지 않는다.
- 기존 승인 visual이 없다는 이유로 자동 이미지 생성을 시작하면 사용자의 이미지 승인 경계를 위반한다.
- 별도 부록을 금지한다는 이유로 중요한 traceability를 제거하지 않고 두 파일 내부에 통합해야 한다.

## 영향 범위와 검증

### 승인된 구현 범위

1. profile의 단일 책임 정책 문서 추가
2. 프로젝트별 채팅에 붙여 넣을 수 있는 작업지시문 템플릿 추가
3. project-operations README와 GPT custom-instructions bootstrap에 bounded route 노출
4. 정확히 2개 산출물, PDF-only download, Notion input-only, 상세 구현 설명, 동일 ID/SHA, evidence ceiling, 이미지 승인 경계를 보호하는 focused regression 추가

### 제외·보호 범위

- 전역 `DOMAIN_SPLIT_CANON` 제거 또는 모든 프로젝트의 Notion 폐기 없음
- 기존 Notion page/database 삭제·수정·migration 실행 없음
- 실제 게임 프로젝트 code·scene·resource·runtime data 변경 없음
- 새 provider·dependency·paid service·API 사용 없음
- DOCX·ZIP·별도 appendix를 요구하는 다른 publication profile 변경 없음
- 열린 다른 PR·branch는 read-only
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 기존 open PR #693이 소유하므로 이번 제안·구현에서 수정하지 않음

### 검증 계획

1. focused contract를 먼저 추가하고 current main에서 새 정책·템플릿 부재로 RED를 확인한다.
2. 승인 범위의 최소 owner·template·routing만 구현해 GREEN으로 전환한다.
3. `EXACTLY_TWO_DELIVERABLES`, `PDF_ONLY_USER_DOWNLOAD`, `NOTION_INPUT_ONLY_NO_OUTPUT`, `CORE_SYSTEM_AND_CONTENT_IMPLEMENTATION_DETAIL_REQUIRED`, `SHARED_ID_AND_SOURCE_SHA_REQUIRED`, `NO_AUTOMATIC_IMAGE_GENERATION`을 검사한다.
4. 기존 global Notion workflow와 publication profiles가 자동 폐기되지 않았는지 반례 검증한다.
5. AI spec이 runtime truth를 대체하지 않는지 검사한다.
6. exact-head CI, required checks, unresolved thread 0, 최소 5회 whole-state 적대적 검토 후 안전한 squash merge와 post-merge readback을 수행한다.
7. 실제 프로젝트 PDF 생성·Godot runtime·사용자 시각 검수는 이번 Base 계약 작업의 증거가 아니므로 별도 project execution에서 검증한다.

## 필요한 도구·파일·권한

- 필요 항목: GitHub connector, Base repository write/PR 권한, 기존 Python contract test runner
- 필요한 이유: 제안과 구현 PR 분리, test-first 계약 검증, exact-head CI와 post-merge readback
- 설치·적용 방법: 새 dependency 없이 현재 Base 도구와 GitHub Actions를 재사용
- 설치 후 확인 명령: focused unittest 및 repository required checks
- 최소 권한: branch/file/PR 생성과 안전한 squash merge 권한; ruleset bypass·admin bypass는 사용하지 않음

## 승인과 구현

- 사용자 승인 근거: 2026-08-28 현재 대화의 2파일 구조 확정과 Base 교정·작업지시문 제공 지시
- Proposal Registry: open PR #693의 경로 소유권 때문에 이번 작업에서는 갱신 보류. 해당 PR을 수정·흡수·종료하지 않는다.
- 구현 PR: 별도 current-task 구현 PR에서 진행
- 증거 한계: Base 계약·template·regression만 검증하며 프로젝트 PDF 품질, 실제 Godot runtime, 사용자 UX PASS를 주장하지 않는다.
- 롤백: 구현 PR에서 추가한 profile owner·template·routing·focused test를 한 단위로 revert한다. 전역 Notion 계약은 원래 상태로 유지한다.
