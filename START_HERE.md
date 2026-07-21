# Base 시작 지점

이 문서는 새 채팅, 새 GPT, 새 Codex 또는 새 작업자가 `Base`를 프로젝트 작업에 적용할 때 사용하는 최상위 라우터다.

## 사용자가 기억할 최소 요청

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 이 프로젝트를 작업해줘.`

`전부 살펴본다`는 모든 파일을 무작정 읽는 뜻이 아니다. 현재 작업에 필요한 책임 원본과 최소 스킬 집합을 Registry와 Documentation Map에서 선별한다.

```text
Base START_HERE
→ Base AGENTS
→ docs/OPERATING_MODEL.md
→ Base Documentation Map
→ Base Skill Registry
→ 대상 프로젝트 AGENTS
→ 루트 [기획서]/00_프로젝트_허브/START_HERE
→ Active Context·Documentation Map·Development Gates
→ Design Document Registry·Skill Registry
→ 현재 책임 원본·필요한 Skill mode
→ 실제 코드·데이터·자산·테스트
```

저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.

## Base 저장소 자체를 콜드 스타트할 때

`Base`는 프로젝트 운영 키트의 공용 원본이므로 프로젝트 전용 `ACTIVE_CONTEXT.md`, `DEVELOPMENT_GATES.md`, `ROADMAP.md`, `INTERVIEW_REGISTRY.json`을 활성 파일로 두지 않는다. 이 경로들은 `templates/project-operations/`에서 대상 프로젝트에 설치하는 템플릿이다.

Base 자체의 현재 상태는 다음 책임 원본에서 찾는다.

```text
확정된 운영 계약 → AGENTS.md·START_HERE.md·docs/OPERATING_MODEL.md·docs/DOCUMENTATION_MAP.md
완료된 변경 → docs/CHANGELOG.md
활성 스킬 → skills/SKILL_REGISTRY.json
이전 Skill ID → skills/LEGACY_SKILL_ALIASES.md
검토 대기 작업 → [수정제안서]/PROPOSAL_REGISTRY.json·개별 PROPOSAL.md
진행 중 구현 → GitHub PR·Actions
현재 인터뷰 → Base 변경 인터뷰가 실제 등록된 경우에만 해당 Registry·기록
```

활성 Base 인터뷰가 없으면 `등록 없음`, 제출된 제안의 우선순위가 승인되지 않았으면 `사용자 검토 대기·우선순위 미확정`으로 답한다. 프로젝트용 상태 파일이 Base 루트에 없다는 이유만으로 결함이나 누락으로 판정하지 않는다.

## 공용 운영 계약

공용 구조와 상태·발행 정책의 단일 설명 원본은 `docs/OPERATING_MODEL.md`다. 이 문서는 요청을 해당 실행 Skill로 라우팅하는 역할만 가진다.

금지:

- 전체 skills 폴더 기본 로드
- trigger와 무관한 스킬 호출
- 같은 요청의 수준·범위·상태를 여러 스킬에서 중복 판정
- 검증·발행·Handoff의 조기 실행
- `[보류]`, `[백업]`, `[제거 후보]` 스킬 호출
- 실행하지 않은 테스트·렌더·권한을 통과로 표시

## 요청별 라우팅

### 요청 접수·요구 확정·실행 계약

`skills/managing-project-intake-and-work-contract/SKILL.md`

```text
route
→ 저장소 사실 조사
→ 필요한 경우 clarify
→ 사용자 마지막 확인
→ contract
```

오탈자·명확한 단일 파일 기계 수정·동일 검사 재실행은 예외다.

### 신규 프로젝트 운영체계 설치

`skills/managing-game-project-operating-system/SKILL.md`의 `install` mode를 사용한다.

설치 뒤 같은 Skill의 `verify` mode로 Registry·발행·스킬·자동화·콜드 스타트를 검수한다.

### 기존 프로젝트 구조 감사·마이그레이션

`skills/managing-game-project-operating-system/SKILL.md`

```text
audit
→ 현행 책임·참조·고유 정보 조사
→ 목표 구조·보존·롤백 제안
→ 사용자 승인
→ migrate
→ verify
```

사용자 승인 전 대량 이동·삭제·통합을 하지 않는다.

### 핵심 컨셉·뾰족한 재미·기획 방향

`skills/analyzing-and-refining-game-concepts/SKILL.md`

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

SWOT은 SO·WO·ST·WT 행동으로 변환하고, MDA·DDE·3C·루프·동기·차별화·제작성을 교차 분석한다. `DDD`는 프로젝트가 의미를 정의하기 전에는 임의 해석하지 않는다.

### 기획 책임 원본 작성·발행

`skills/managing-design-documents/SKILL.md`

필요한 mode만 사용한다.

```text
author | update | restructure
→ Registry 발행 정책 확인
→ publish
→ validate
```

발행 정책:

- `source_only`
- `milestone_sync`
- `always_sync`

DOCX와 다이어그램은 선언한 경우만 생성한다. `CURRENT`와 사람 시각 검수 완료를 혼동하지 않는다.

### 프로젝트 스킬 생성·통합·학습

`skills/evolving-project-discipline-skills/SKILL.md`

Registry에 trigger가 일치하는 최소 스킬만 등록한다. 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출만 Learning Log에 기록한다.

### 현재 상태·인수인계

`skills/maintaining-project-context-and-handoff/SKILL.md`

Active Context는 현재 상태·다음 작업·위험·읽기 순서만 압축한다. 책임 원본 전문을 복제하지 않는다.

### 프로젝트 교훈의 Base 환류

`skills/managing-base-change-proposals/SKILL.md`

```text
extract
→ submit
→ review
→ 사용자 승인
→ 별도 구현 PR에서 implement
→ verify
```

제안 PR과 활성 Base 구현 PR을 합치지 않는다.

### Vertical Slice

`skills/designing-vertical-slices/SKILL.md`

대표 플레이 구간으로 핵심 경험·목표 품질·시스템 연결·제작 파이프라인을 함께 검증한다. 핵심 컨셉이나 뾰족한 재미가 미확정이면 먼저 `analyzing-and-refining-game-concepts`를 사용한다.

### 프로젝트 변경 검증

`skills/reviewing-and-validating-project-changes/SKILL.md`

```text
contract-check
→ 필요한 경우 external-source-review
→ static-validation
→ runtime-validation
→ regression
→ evidence-report
```

코드·데이터·문서·자산 변경은 승인 계약, 실제 diff, 정적·런타임·회귀 증거를 연결한다. 실행 환경이 없으면 `UNVERIFIED`로 기록한다.

### 외부 AI 대량 작업

- 작업 공간 운용: `skills/orchestrating-deepseek-worktrees/SKILL.md`
- 결과 검수: `skills/reviewing-and-validating-project-changes/SKILL.md`의 `external-source-review`

외부 AI 결과는 검수 대기 입력이며 실제 diff·근거·테스트 확인 전에는 기준 원본으로 인정하지 않는다.

### 아트·UI

- 생성 전 프롬프트·기술 카드: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- 구현된 Godot·Web UI 결과 감사: `skills/auditing-and-refining-ui-art/SKILL.md`

두 책임은 합치지 않는다. UI 감사는 사용자 승인 전 대상 파일을 수정하지 않으며 전후 실제 렌더로 재검수한다.

## 일반 프로젝트 작업 읽기 순서

```text
프로젝트 AGENTS
→ 루트 [기획서]/00_프로젝트_허브/START_HERE
→ ACTIVE_CONTEXT.md
→ DOCUMENTATION_MAP.md
→ DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json
→ 현재 책임 원본
→ SKILL_REGISTRY.json
→ 필요한 통합 Skill과 mode
→ Roadmap·Issue·Plan
→ 실제 파일·자산·테스트
```

변경 후 `DOCUMENT_UPDATE_MATRIX.md`로 영향 범위를 확인한다.

## 이전 Skill ID

통합 전 Skill ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 연결한다. 새 문서와 Registry에는 새 ID만 사용하고 과거 Issue·PR·Git 이력은 그대로 보존한다.
