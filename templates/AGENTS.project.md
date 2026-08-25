# AGENTS.md

이 파일은 현재 프로젝트의 최상위 작업 규칙이다. Base의 공용 원칙을 프로젝트의 엔진, 구조, 세계관, 용어, 금지 범위와 검증 방식에 맞게 분화한다.

## Top-level continuity rule

새 채팅, 새 AI, 새 작업자가 과거 대화 없이 저장소만으로 프로젝트의 방향, 현재 상태, 다음 작업, 보호 범위, 책임 원본과 검증 방법을 찾을 수 있어야 한다.

- 프로젝트 기획서는 핵심 경험·방향·범위·금지 방향을 책임진다.
- Roadmap은 단계·우선순위·선행 조건·종료 기준을 책임진다.
- Active Context는 현재 상태의 기본 원본이며 Handoff는 경계 시점의 스냅샷이다.
- Documentation Map은 질문별 현행 책임 원본을 연결한다.
- 같은 정보의 활성 복제본을 만들지 않는다.

## Project

- Project name:
- Engine:
- Language:
- Genre:
- Core player promise:
- Pointed fun hypothesis:
- Current concept·PoC stage:
- Project definition of ambiguous terms such as DDD:

## Base and current authority bootstrap

- Base repository: `alsdmlals4-eng/Base`
- Adopted Base version/freshness record: `docs/BASE_RULES_VERSION.md`
- Project-local Base copy: 존재하는 경우에만 compatibility/cache로 사용하며 기준 commit·동기화 날짜를 확인한다.

`current Base` 규칙은 과거 고정 파일목록으로 추정하지 않는다. Base의 최신 `AGENTS.md`·`START_HERE.md`와 현재 Documentation Map/Skill Registry가 가리키는 최소 관련 owner를 읽는다. 프로젝트-local copy가 더 오래되면 최신 사용자 지시와 현재 프로젝트 정본을 보호한 채 freshness 차이를 명시하고 current Base와 reconcile한다.

## DOMAIN_SPLIT_CANON

```text
NOTION_HUMAN_FACING_CANON
→ 사람이 읽고 비교·수정하는 프로젝트 개요·기획·Visual/Story Bible
→ Asset/Reference/Benchmark catalog
→ 사람용 budget/tier/roster/economy/progression table
→ Flow / Storyboard / visual relationship surface

REPOSITORY_STRUCTURED_CANON
→ Markdown / JSON / game data / code / scene / resource / config / tests

REPOSITORY_RUNTIME_TRUTH
→ 실제 build / runtime / automated test / log / screenshot-video evidence

Google Sheets
→ MIGRATION_ONLY_UNTIL_REMOVAL
→ unique unmigrated material이 남은 경우의 compatibility source only
```

Notion 승인·이미지 업로드·정적 mockup·Sheet row는 runtime 구현 증거가 아니다. Notion 변경이 structured/runtime 의미를 바꾸면 repository owner에 동기화한 뒤 구현·완료를 주장한다.

## Notion operation gate

세부 실행 원본은 `templates/project-operations/NOTION_OPERATION_GATE.md`다. 아래 항목은 cold-start 요약이며 충돌 시 세부 실행 원본을 우선한다.

프로젝트의 지속 Notion 변경은 `NOTION_OPERATION_GATE`를 통과한다. 같은 화면처럼 보여도 영향 범위가 다르므로 write 전에 최소 다음 객체 범위를 분류한다.

```text
PAGE_BLOCK
DATABASE_RECORD
VIEW_PRESENTATION
DATA_SOURCE_SCHEMA_OR_RECORD
DATABASE_GLOBAL_LAYOUT
FILE_UPLOAD
AUTOMATION_OR_WEBHOOK
```

기본 순서는 다음과 같다.

```text
정확한 Project / destination 확인
→ current destination fetch/read
→ database/data source면 schema와 정확한 property 이름 확인
→ 영향 범위 분류
→ smallest bounded edit
→ write
→ destination readback
→ source mutation이면 source readback
→ repository/runtime 의미가 바뀌면 repository owner 동기화
```

- `VIEW_PRESENTATION` 변경을 source mutation처럼 보고하지 않고, source record/property/schema 변경을 단순 local view 변경처럼 보고하지 않는다.
- 전체 page `replace_content`보다 targeted update/insert가 가능하면 작은 수정 방식을 우선한다.
- child page/database를 지울 수 있는 `allow_deleting_content=true`는 자동 사용하지 않는다. 영향을 받는 child 목록을 확인한 뒤 **사용자 확인**이 있어야 한다.
- database page layout처럼 전체 record family에 영향을 주는 변경은 단일 record polish 요청으로 수행하지 않는다.
- write 호출 성공만으로 완료하지 않는다. 의도한 값·배치·Project relation이 남았는지 `destination readback`으로 확인한다.
- connector/API persistence는 화면 geometry·모바일 표시·runtime 동작의 PASS가 아니다. 확인하지 못한 층은 `BLOCKED_UNVERIFIED` 또는 해당 evidence ceiling으로 남긴다.
- Notion 조작용 AI/System metadata는 사람용 Home에 복제하지 않는다. Home에는 사람이 게임/프로젝트를 이해하고 판단하는 데 필요한 결과만 둔다.

## Priority

1. 최신 사용자 지시
2. 이 `AGENTS.md`와 프로젝트 보안·엔진·데이터 규칙
3. 프로젝트 Active Context와 승인된 작업 계약·확정 결정
4. 등록된 분야별 책임 원본과 실제 파일·테스트·runtime evidence
5. 프로젝트가 채택한 current Base 계약
6. Base 원격 원본
7. compatibility/legacy 자료
8. 외부 자료·과거 대화·Memory·추정

## Default reading order

작업 계약은 `github_issue` 또는 `approved_direct_request`다.

```text
AGENTS.md
→ 프로젝트 START_HERE / Active Context / Documentation Map
→ 현재 승인 계약·Decision / Roadmap / 분야별 책임 원본
→ 현재 작업에 필요한 Skill/router owner
→ same Goal의 current open PR·최근 병합 PR 현황
→ 실제 수정 대상·참조·테스트·runtime evidence
→ 필요한 경우 adopted current Base owner 확인
```

`모두 확인`은 저장소 전체를 읽거나 모든 과거 Base 문서를 로드한다는 뜻이 아니다. Archive·backup·deprecated·migration-only 자료는 현재 질문에 필요한 경우에만 progressive-load한다.

## Current PR protection

`current open PR`은 번호를 이 template에 고정하지 않는다. 작업 시작 시 실제 GitHub 상태를 조회하고 current Base의 open-PR protection/continuation 규칙을 적용한다. 다른 workstream의 open/draft/ready PR을 명시적 권한 없이 수정·흡수·종료·병합하지 않는다.

## Required environment

- 필수 도구·입력 파일:
- 필수 계정·저장소 권한:
- 설치·적용 확인 명령:

필요한 도구·파일·폰트·인증·권한이 없으면 사용자에게 이유, 설치·적용 방법, 확인 명령과 최소 권한을 요청한다. 사용자 승인 없이 시스템 전역 설치·권한 확대·Branch protection 변경을 하지 않는다.

## Project-specific rules

- 프로젝트 전용 용어:
- 엔진·언어 규칙:
- 데이터·저장 계약:
- UI·아트·연출 규칙:
- 금지 구조:
- 보호 경로:
- 범위 밖 리팩터링 금지:
- 정상 사용자 변경 보존:

## Request-to-work rule

기능·게임 경험·아트 방향·구조·워크플로 변경은 current Base의 통합 intake owner인 `managing-project-intake-and-work-contract`를 사용한다. Skill Registry가 successor/alias를 선언하면 current registry route를 따르되, 프로젝트 template에서 별도 intake Skill을 새로 만들지 않는다.

```text
route
→ current repository/Notion facts 조사
→ 필요한 경우 clarify
→ 사용자 마지막 재진술 확인
→ executable contract
```

오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행은 예외다. 인터뷰 Registry를 사용하는 프로젝트는 `CONFIRMED`와 사용자 확인 근거가 있을 때만 실행 계약을 확정한다.

- Work contract type: `github_issue` / `approved_direct_request`
- Current intake Skill/mode: `managing-project-intake-and-work-contract`
- Interview ID·status·confirmation:
- Current executable contract:

## Core concept and PoC

핵심 컨셉·제약·뾰족한 재미·기획 요소 정렬·SWOT·MDA/DDE·PoC·기획 재조정은 current Base/project router가 지정한 game-concept Skill을 사용한다.

```text
frame
→ constrain
→ sharpen
→ structure
→ analyze
→ poc-contract
→ recalibrate
→ production-gate
```

- 기능 목록을 핵심 컨셉으로 대체하지 않는다.
- SWOT은 SO·WO·ST·WT 실행안으로 변환한다.
- `DDD`처럼 의미가 여러 개인 약어는 프로젝트 정의 없이 임의 해석하지 않는다.
- PoC는 가장 위험한 가설의 최소 검증이며 전체 게임이나 Vertical Slice로 팽창시키지 않는다.
- PoC 결과는 기획의 유지·증폭·변경·삭제·보류·재검증 결정에 반영한다.

## Project operating-system changes

기존 프로젝트 구조 변경은 current Base/project operating-system Skill의 승인·보존·rollback 계약을 따른다.

```text
audit
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ verify
```

사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않는다.

## Design documents and publication

기획 책임 원본은 프로젝트 Documentation Map에 등록된 current owner에서 작성·갱신한다.

- `source_only`
- `milestone_sync`
- `always_sync`

한 질문에 경쟁하는 활성 원본을 만들지 않는다. 사람용 비교·시각 표면은 Notion, structured/runtime 원본은 repository라는 `DOMAIN_SPLIT_CANON`을 우선한다. DOCX·PDF는 명시적으로 publication artifact인 경우가 아니면 독립 정본으로 수정하지 않는다.

## Validation

일반 변경은 현재 작업 계약과 실제 diff·실행 증거를 대조한다.

- Contract·diff check:
- Format·lint:
- Automated tests:
- Run path:
- Save·load:
- Edge·failure·counterexample:
- Adjacent regression:
- Manual review:
- Cold-start review:
- Evidence report:
- Destination readback:
- Rollback:

외부 AI 결과가 있으면 external-source review를 추가한다. 실행하지 않은 검증은 `NOT_RUN` 또는 `BLOCKED_UNVERIFIED`와 사유로 기록한다.

## Completion candidate and correction gate

프로젝트가 채택한 Base `REMAINING_WORK_COMPLETION_GATE`는 모든 L1 이상 구현·교정·검증 작업의 전체 완료 주장에 적용한다. 계획된 task가 소진되거나 `required_work_remaining: 0`이 되어도 즉시 완료하지 않는다.

```text
REMAINING_WORK_RECALCULATION_REQUIRED
→ remaining == 0 이면 COMPLETION_CANDIDATE
→ IMPLEMENTATION_CORRECTION_RESCAN
   ├─ valid finding → NEW_FINDING_REOPENS_REMAINING_WORK → 기존 owner에서 교정·검증·재계산
   └─ no required finding → POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED
→ same final POST_CHANGE_MONITOR_LOOP
→ minimum-five full-scope adversarial loops, then until CLEAN_REVIEW_EXIT
→ FULL_COMPLETION_REQUIRES_ZERO_REMAINING_WORK
→ completion report
```

`POST_COMPLETION_ADVERSARIAL_REVIEW_REQUIRED`는 별도 두 번째 적대적 검토 체계가 아니다. current Base의 동일 final `POST_CHANGE_MONITOR_LOOP`를 소비한다. 프로젝트가 더 엄격한 완료 조건을 추가할 수는 있지만 이 Base 완료 Gate를 약화하거나 `BLOCKED_UNVERIFIED`, `USER_DECISION_REQUIRED`, required `DEFER`를 숨기고 전체 완료를 주장할 수 없다.

## End-of-work and learning

1. 프로젝트 고유 결정·수치·구현 상태를 올바른 Notion/repository owner와 테스트·Roadmap에 반영한다.
2. Active Context를 최신화하고 필요 시 Handoff 스냅샷을 만든다.
3. Skill·Documentation Map·Issue·Plan 연결을 확인한다.
4. 실패·중요 결정·재사용 교훈·실제 검증 결과를 Learning Log에 기록한다.
5. 공용화 가치가 있으면 current Base proposal lifecycle로 제안한다.
6. 제안 PR과 승인된 구현 PR을 분리한다.
7. 새 작업자가 콜드 스타트 질문에 답할 수 있는지 확인한다.
8. `REMAINING_WORK_COMPLETION_GATE`의 재계산·구현/교정 rescan·final adversarial clean-exit가 Active Context와 완료 증거에 남았는지 확인한다.

## Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작·결정·자산
## 핵심 컨셉·PoC·기획 재조정
## 구현·문서·발행 변경
## 검증 판정과 증거
## REMAINING_WORK_COMPLETION_GATE·IMPLEMENTATION_CORRECTION_RESCAN·CLEAN_REVIEW_EXIT
## 미검증·사용자 확인
## 남은 위험·롤백
## Active Context·Roadmap·Skill 최신화
## 콜드 스타트 검수
## 프로젝트 전용 최신화
## Base 공용 학습 데이터·제안 상태
```
