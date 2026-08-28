# Custom Instructions Guide

이 문서는 ChatGPT, Codex, Copilot 같은 AI 도구의 맞춤형 지침을 **현재 Base·프로젝트 정본과 충돌하지 않는 bootstrap layer**로 설계하고 유지하는 공용 기준이다.

## 1. 핵심 원칙

맞춤형 지침은 짧고 안정적이며 장기간 유지되는 행동 기준만 담는다. 프로젝트 사실, 현재 상태나 Base의 세부 절차를 복제하는 두 번째 정본으로 만들지 않는다.

```text
Custom Instructions
→ stable user/work preferences + authority bootstrap

Memory
→ long-lived preference/context aid

latest user request
→ current task intent

project AGENTS + current repository canon + actual evidence
→ current project authority

adopted Base contract
→ current shared operating rules

legacy Notion / Sheets
→ migration discovery only when unique unmigrated material remains
```

맞춤설정이나 Memory와 현재 정본이 충돌하면 최신 사용자 지시와 현재 Base/프로젝트 authority를 우선한다.

## 2. Stable bootstrap에 넣을 것

다음은 여러 채팅과 프로젝트에서 장기간 재사용되므로 맞춤설정에 적합하다.

- 사용자 역할과 숙련도처럼 안정적인 작업 맥락.
- 기본 언어와 설명 깊이.
- 플레이어 가치, 핵심 경험, 차별점, 판매 포인트를 우선하는 기획 기준.
- 비용 경계: 무료·로컬·현재 연결된 도구 우선, 추가 유료비용은 사용자 승인 필요.
- 이미지 생성·편집은 명시적 요청이 있을 때만 진행한다는 capability boundary.
- 기억·과거 대화·PDF·Library·legacy workspace를 현재 정본으로 승격하지 않는 규칙.
- Base 작업은 최신 Base `AGENTS.md`, `START_HERE.md`, current owner와 실제 evidence를 다시 읽는 bootstrap.
- 프로젝트 작업은 최신 프로젝트 repository의 `AGENTS.md`, `START_HERE`, Active Context, confirmed decisions, registered owners와 실제 파일을 다시 읽는 bootstrap.
- `REPOSITORY_PRIMARY_PROJECT_CANON`과 `HUMAN_GDD_PDF_DERIVED_VIEW`처럼 장기적인 권한 경계.
- 통합 기획서의 기본 두 산출물과 PDF-only 사용자 전달 정책.
- 세부 Gate를 복제하지 않고 current Base contract를 dynamic lookup한다는 원칙.

## 3. 맞춤설정에 넣지 않을 것

다음은 쉽게 stale해지므로 프로젝트 또는 Base 정본에 둔다.

- 현재 진행률, milestone, blocker, 다음 작업.
- PR·Issue 번호와 open/merged 상태.
- 특정 시스템의 최신 수치, 밸런스 값, 구현 완료 여부.
- 긴 세계관·캐릭터·아이템·콘텐츠 명세.
- 구체 코드 파일 전체 목록이나 현재 branch/SHA.
- 일회성 작업 지시와 임시 오류/성공 로그.
- Base 세부 Gate 횟수와 체크리스트의 복사본.
- 폐기되었거나 migration-only인 도구를 기본 작업면으로 만드는 지시.
- 특정 프로젝트의 Notion URL이나 attachment locator.
- 장기간 유지할 이유가 없는 특정 벤치마크 목록.

맞춤설정은 current Base와 project owner를 읽는 방법을 소유하고, Base와 프로젝트 저장소가 실제 절차·정본·증거를 소유한다.

## 4. Repository-first authority bootstrap

프로젝트 작업의 기본 권위는 다음과 같다.

```text
latest user instruction
→ project AGENTS / security / engine / data rules
→ Active Context + approved work contract + confirmed decisions
→ registered repository canon + actual code/data/assets/tests/runtime evidence
→ adopted Base contract
→ Base remote
→ legacy migration sources
→ external references / memory / past conversation / inference
```

Base 자체 작업은 프로젝트 workspace를 억지로 거치지 않는다.

```text
latest user instruction
→ Base AGENTS.md + START_HERE.md
→ registered Base owner docs + actual repository evidence
→ external references / memory / past conversation / inference
```

### 4.1 Current project surfaces

```text
REPOSITORY_PRIMARY_PROJECT_CANON
→ Markdown / JSON / game data / code / scene / resource / config
→ approved implementation asset and ASSET_MANIFEST
→ tests / build / runtime evidence
→ exact commit / PR / rollback history

AI_DETAILED_PLANNING_IMPLEMENTATION_MARKDOWN
→ project meaning, systems, content, UX, data and implementation contract

HUMAN_GDD_PDF_DERIVED_VIEW
→ exact repository commit에서 생성된 사람용 상세 기획서 PDF

CHATGPT_WORK_EXECUTION_SURFACE_NOT_CANON
CHATGPT_LIBRARY_REFERENCE_STORAGE_NOT_CANON

LEGACY_READ_ONLY_MIGRATION_SOURCE
→ unique unmigrated Notion / Sheet material only
```

- PDF는 독립 정본이 아니다.
- Work와 Library는 실행·참고·후보·PDF 보관을 지원하지만 version control을 대체하지 않는다.
- Notion과 Sheets는 신규 기본 workspace가 아니며 새 write/upload/sync/readback을 완료 조건으로 만들지 않는다.
- 기존 고유 자료를 읽지 못하면 `BLOCKED_UNVERIFIED`로 남기며 중복·폐기로 추정하지 않는다.

## 5. Desktop GPT 2파일 통합 기획서 bootstrap

프로젝트 정본을 상세 통합 기획서로 정리할 때는 `DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD`를 사용한다.

```text
EXACTLY_TWO_DELIVERABLES
├─ HUMAN_MASTER_GDD_PDF
└─ AI_PRODUCTION_SPEC_MARKDOWN
```

맞춤설정에는 세부 목차 전체를 넣지 않고 다음 안정 규칙만 둔다.

- 사람용 PDF와 repository AI Markdown 두 종류를 기본 산출물로 한다.
- 사용자에게 기본 다운로드 링크로 제공하는 것은 PDF 하나다: `PDF_ONLY_USER_DOWNLOAD`.
- AI Markdown은 repository path·branch·exact commit SHA·PR·validation result로 보고한다.
- 두 산출물은 같은 `SYS / CNT / UI / UX / AST / AUD / DAT / QA / DEC` ID와 source SHA를 사용한다.
- 핵심 시스템·콘텐츠·UX/UI·데이터·실제 asset consumer·Godot 구현 원리·Acceptance와 evidence ceiling을 상세히 포함한다.
- DOCX·ZIP·별도 appendix·별도 image bundle·Notion output을 기본으로 만들지 않는다.
- 이미지 생성은 명시적 사용자 요청이 있을 때만 한다.

세부 실행 계약은 다음 owner가 가진다.

- `docs/REPOSITORY_FIRST_PROJECT_WORKSPACE_POLICY.md`
- `templates/project-operations/DESKTOP_GPT_TWO_ARTIFACT_MASTER_GDD_WORK_INSTRUCTION.md`
- `templates/project-operations/AI_PROJECT_CANON_SPEC.md`
- `templates/project-operations/HUMAN_GDD_PDF_EXPORT_CHECKLIST.md`

## 6. ChatGPT 맞춤설정 원본

ChatGPT용 공용 원본은 `templates/custom-instructions.gpt.md`다.

템플릿은 두 책임을 분리한다.

1. ChatGPT가 알아야 할 안정적인 사용자 맥락.
2. ChatGPT가 최신 Base·프로젝트 정본으로 진입하고 작업하는 방법.

UI가 두 입력란을 제공하면 각각 넣고, 단일 입력란이면 같은 순서로 합친다. 프로젝트별 실제 상태를 맞춤설정에 계속 덧붙이지 말고 해당 프로젝트의 current owner를 fresh-read한다.

현재 세션에서 GitHub, 파일, 웹, 연결 도구로 필요한 evidence를 직접 확인하거나 작업할 수 있으면 실제 Tool 실행을 우선한다. 수행 가능한 일을 추정이나 불필요한 다른 AI handoff로 대체하지 않는다. 반대로 filesystem/runtime/build 권위가 없는 작업은 완료했다고 주장하지 않는다.

## 7. Memory와 Project context

Memory와 프로젝트 대화는 발견·연속성 보조 수단이지 정본이 아니다.

### 유지 가치가 높은 예

- 장기적인 개발 숙련도와 선호 설명 방식.
- 주 개발 엔진·언어처럼 오래 유지되는 기본 환경.
- 비용 정책.
- 플레이어 경험 우선 기획 성향.
- 이미지 생성 승인 경계.
- repository-first 프로젝트 운영과 두 산출물 정책.

### 프로젝트에서 다시 확인해야 하는 예

- 현재 구현 상태와 다음 작업.
- PR/Issue 상태.
- 특정 시스템 최신 수치.
- 승인 asset의 최신 version과 hash.
- 최근 변경된 도구 정책.
- 일회성 작업 결과.

다른 프로젝트의 기억·대화·자료는 reuse 후보 discovery에는 사용할 수 있지만 현재 프로젝트 사실로 자동 승격하지 않는다. 현재 프로젝트 → 승인 Asset/Reference/Benchmark → Base reuse/knowledge → 직접 관련된 targeted cross-project evidence → 필요한 외부 benchmark 순으로 좁힌다.

제품의 Memory·Project·Work 기능과 제한은 바뀔 수 있다. 실제 설정 변경이나 제품 동작에 의존하는 결정을 내리기 전에는 현재 공식 문서를 다시 확인한다. 제품 설정은 repository authority를 바꾸지 않는다.

## 8. Codex/Copilot bootstrap

Codex용 stable bootstrap 원본은 `templates/custom-instructions.codex.md`, Copilot의 repository-wide bootstrap 원본은 `templates/copilot-instructions.md`다. 둘 다 current project `AGENTS.md`, exact repository commit과 최신 구현 계약보다 높은 authority가 아니다.

GPT·Codex·Copilot 제품 이름을 영구 역할과 동일시하지 않는다. 다만 현재 기본 역할 분리는 다음과 같다.

```text
GPT
→ planning / research / review / image generation when explicitly requested
→ repository canon and Codex handoff preparation

Codex
→ actual Godot product implementation for PLAY_MEANINGFUL_WORK_SLICE
→ tests / runtime / build evidence

Copilot
→ repository coding assistance under the same current owners
```

Codex handoff는 `docs/REPOSITORY_FIRST_GPT_CODEX_HANDOFF_POLICY.md`를 따른다. exact repository commit과 actual asset path/manifest/SHA를 사용하며 Notion 부재만으로 구현을 막지 않는다.

## 9. Legacy migration bootstrap

기존 Notion 또는 Sheets에 고유 자료가 남을 수 있는 프로젝트에서만 다음을 bootstrap에 적용한다.

```text
legacy inventory
→ UNIQUE | DUPLICATE | OBSOLETE | BLOCKED_UNVERIFIED
→ UNIQUE migration to repository canon / tracked runtime asset / non-canon Library reference
→ provenance
→ destination readback
→ consumer check
→ legacy read-only
```

프로젝트가 Notion dependency 제거를 주장하려면 다음이 모두 0이어야 한다.

```text
NOTION_UNIQUE_CANON_COUNT = 0
CODEX_NOTION_DEPENDENCY_COUNT = 0
ACTIVE_NOTION_WRITE_REQUIREMENT_COUNT = 0
```

세 count의 0은 runtime·UX·release PASS를 의미하지 않는다. 기존 page/database는 사용자 삭제 지시 없이 제거하지 않는다.

## 10. 검증과 유지보수

맞춤설정을 변경할 때 다음을 확인한다.

- [ ] current Base `AGENTS.md`, `START_HERE.md`, machine authority와 충돌하지 않는다.
- [ ] 프로젝트 사실이나 현재 PR 상태를 장기 지침으로 복제하지 않았다.
- [ ] repository-first authority와 PDF derived-view 경계가 있다.
- [ ] Work·Library·Memory·legacy workspace를 정본으로 승격하지 않는다.
- [ ] 새 Notion write나 이중 동기화를 기본 요구하지 않는다.
- [ ] 두 산출물·PDF-only·공통 ID/SHA 정책이 보존된다.
- [ ] 이미지 생성 명시적 승인 경계가 보존된다.
- [ ] 비용·보안·증거 상한이 보존된다.
- [ ] 실행하지 않은 test/runtime/UX를 PASS로 만들지 않는다.

Base 정책이 바뀌면 맞춤설정에 모든 세부 절차를 복사하지 않는다. bootstrap의 authority pointer와 장기 기본값만 교정하고, 상세 owner는 Base 문서에서 계속 유지한다.
