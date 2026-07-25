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
→ Base Shared Skill Route Registry
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
공용 어댑터 Skill route → skills/BASE_SHARED_SKILL_ROUTES.json
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
- 실행하지 않은 조사·테스트·렌더·권한을 통과로 표시
- 외부 벤치마크·리뷰를 요구사항 권한이나 구현 사실의 정본으로 사용

## 요청별 라우팅

### 요청 접수·요구 확정·실행 계약·작업 순서

`skills/managing-project-intake-and-work-contract/SKILL.md`

```text
route
→ 저장소 사실 조사
→ 필요한 경우 clarify
→ 사용자 마지막 확인
→ contract
→ 필요한 경우 decompose-and-sequence
```

오탈자·명확한 단일 파일 기계 수정·동일 검사 재실행은 예외다. `decompose-and-sequence`는 승인된 L2 이상 작업이나 여러 의존성이 있는 경우에만 사용하며, 결과·의존성·병렬 묶음·게이트·검증·롤백을 만든다.

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

### 핵심 컨셉·DDD·벤치마크·플레이테스트·기획 방향

`skills/analyzing-and-refining-game-concepts/SKILL.md`

```text
frame
→ constrain
→ sharpen
→ structure
→ 필요한 경우 benchmark-and-player-research
→ analyze
→ 필요한 경우 playtest-and-experiment
→ poc-contract
→ recalibrate
```
