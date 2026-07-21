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

## Base

- Repository: `alsdmlals4-eng/Base`
- Version record: `docs/BASE_RULES_VERSION.md`
- Local shared copy:
  - `docs/OPERATING_MODEL.md`
  - `docs/AI_SHARED_WORK_RULES.md`
  - `docs/AI_WORKFLOW_RULES.md`
  - `docs/MVP_WORKFLOW_CHECKLIST.md`
  - `docs/DOCUMENTATION_MAP.md`
  - 필요한 `skills/`, `templates/`, `docs/knowledge/`

일상 작업에서는 Base 원격보다 프로젝트 로컬 사본을 먼저 읽는다. 기준 커밋과 동기화 날짜를 기록한다.

## Priority

1. 최신 사용자 지시
2. 이 `AGENTS.md`
3. 프로젝트 보안·엔진·데이터 규칙
4. 프로젝트 Active Context와 승인된 작업 계약
5. 등록된 책임 원본과 실제 파일·테스트
6. Base 로컬 사본
7. Base 원격
8. 과거 대화와 추정

## Default reading order

작업 계약은 `github_issue` 또는 `approved_direct_request`다.

```text
AGENTS.md
→ BASE_RULES_VERSION.md와 Base 로컬 사본
→ 프로젝트 START_HERE·Active Context·Documentation Map
→ Development Gates·Roadmap
→ Design Document Registry·현재 책임 원본
→ Skill Registry·필요한 통합 Skill과 mode
→ 현재 Issue·Goal·Plan
→ 실제 수정 대상·참조·테스트
```

`모두 확인`은 저장소 전체를 읽는다는 뜻이 아니다. 백업·보류·제거 후보와 전체 skills 폴더는 기본 읽기에서 제외한다.

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

기능·게임 경험·아트 방향·구조·워크플로 변경은 `managing-project-intake-and-work-contract`를 사용한다.

```text
route
→ 저장소 사실 조사
→ 필요한 경우 clarify
→ 사용자 마지막 재진술 확인
→ contract
```

오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행은 예외다. 인터뷰 Registry를 사용하는 프로젝트는 `CONFIRMED`와 사용자 확인 근거가 있을 때만 실행 계약을 확정한다.

- Work contract type: `github_issue` / `approved_direct_request`
- Intake Skill: `managing-project-intake-and-work-contract`
- Intake mode/status:
- Interview ID·status·confirmation:
- Current executable contract:

## Core concept and PoC

핵심 컨셉·제약·뾰족한 재미·기획 요소 정렬·SWOT·MDA/DDE·PoC·기획 재조정은 `analyzing-and-refining-game-concepts`를 사용한다.

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

기존 프로젝트 구조 변경은 `managing-game-project-operating-system`을 사용한다.

```text
audit
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ verify
```

사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않는다.

## Design documents and publication

기획 책임 원본은 `managing-design-documents`로 작성·갱신·발행한다.

- `source_only`
- `milestone_sync`
- `always_sync`

한 질문에는 등록된 단일 Markdown 또는 JSON 책임 원본 하나만 둔다. DOCX·PDF를 독립 원본으로 수정하지 않는다.

## Validation

일반 변경은 `reviewing-and-validating-project-changes`로 작업 계약과 실제 diff·실행 증거를 대조한다.

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
- Rollback:

외부 AI 결과가 있으면 `external-source-review` mode를 추가한다. 실행하지 않은 검증은 `UNVERIFIED`와 사유로 기록한다.

## End-of-work and learning

1. 프로젝트 고유 결정·수치·구현 상태를 책임 원본·테스트·Roadmap에 반영한다.
2. Active Context를 최신화하고 필요 시 Handoff 스냅샷을 만든다.
3. Skill·Documentation Map·Issue·Plan 연결을 확인한다.
4. 실패·중요 결정·재사용 교훈·실제 검증 결과를 Learning Log에 기록한다.
5. 공용화 가치가 있으면 `managing-base-change-proposals`로 제안한다.
6. 제안 PR과 승인된 구현 PR을 분리한다.
7. 새 작업자가 콜드 스타트 질문에 답할 수 있는지 확인한다.

## Report format

```md
## 변경 파일과 이유
## 유지한 기존 동작·결정·자산
## 핵심 컨셉·PoC·기획 재조정
## 구현·문서·발행 변경
## 검증 판정과 증거
## 미검증·사용자 확인
## 남은 위험·롤백
## Active Context·Roadmap·Skill 최신화
## 콜드 스타트 검수
## 프로젝트 전용 최신화
## Base 공용 학습 데이터·제안 상태
```
