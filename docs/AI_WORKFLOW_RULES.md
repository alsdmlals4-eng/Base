# 공용 AI 작업 흐름

이 문서는 작업 순서를 빠르게 확인하는 라우터다. 전체 운영 계약은 `docs/OPERATING_MODEL.md`, 단계별 실행은 각 Skill이 책임진다.

## 1. 요청 접수

`skills/managing-project-intake-and-work-contract/SKILL.md`

```text
route
→ 저장소 사실 조사
→ 필요한 경우 clarify
→ 사용자 마지막 확인
→ contract
```

- `L0`: 오탈자·명백한 형식 변경
- `L1`: 범위가 명확한 작은 변경
- `L2`: 대안·시스템 영향
- `L3`: 여러 분야·핵심 구조·장기 방향
- `L4`: 여러 프로젝트에 재사용 가능한 방법

같은 요청의 작업 수준·분야·범위·검증을 여러 Skill에서 다시 판정하지 않는다.

## 2. 작업 실행 게이트

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
→ Context·Learning
```

세부 판정은 `docs/knowledge/methods/DEVELOPMENT_GATES_METHOD.md`를 따른다.

기획 방향 탐색은 다음 내부 루프를 사용할 수 있다.

```text
핵심 컨셉
→ 제약 조건
→ 뾰족한 재미
→ 기획 요소 정렬
→ PoC
→ 기획 재조정
→ Production·Vertical Slice 진입 판정
```

## 3. 실행 유형 라우팅

| 작업 | Skill |
|---|---|
| 운영체계 설치·기존 감사·마이그레이션·Health Review | `managing-game-project-operating-system` |
| 핵심 컨셉·뾰족한 재미·SWOT·PoC | `analyzing-and-refining-game-concepts` |
| 기획 책임 원본 작성·발행 | `managing-design-documents` |
| 프로젝트 Skill 생성·통합·학습 | `evolving-project-discipline-skills` |
| 현재 상태·Handoff | `maintaining-project-context-and-handoff` |
| 프로젝트 교훈·Base 수정제안서 | `managing-base-change-proposals` |
| Vertical Slice | `designing-vertical-slices` |
| 외부 AI 작업 공간 | `orchestrating-deepseek-worktrees` |
| 프로젝트 변경·외부 AI 결과 검증 | `reviewing-and-validating-project-changes` |
| 이미지 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` |
| 구현된 UI 감사·개선 | `auditing-and-refining-ui-art` |

이전 Skill ID는 `skills/LEGACY_SKILL_ALIASES.md`로 변환한다.

## 4. 기획 방향·PoC

`analyzing-and-refining-game-concepts`를 사용한다.

- `frame`: 한 문장 핵심 컨셉과 플레이어 약속
- `constrain`: 플레이·제작·기술·콘텐츠·시장 제약
- `sharpen`: 반복 플레이를 만드는 뾰족한 재미
- `structure`: GDD·레벨·캐릭터·스테이지·세계관 정렬
- `analyze`: SWOT→SO/WO/ST/WT, MDA/DDE, 3C, 루프·동기·차별화·제작성
- `poc-contract`: 가장 위험한 가설을 검증하는 최소 범위
- `recalibrate`: PoC 결과 기반 유지·수정·삭제·보류·재검증
- `production-gate`: 다음 제작 단계 진입 판정

`DDD`처럼 의미가 여러 개인 약어는 프로젝트 정의 없이 임의 해석하지 않는다.

## 5. 외부 AI 대량 작업

```text
승인된 작업 계약
→ 별도 branch·worktree
→ 제한된 입력 allowlist
→ 구조화된 초안·미확인 목록
→ reviewing-and-validating-project-changes: external-source-review
→ 승인된 최소 변경만 반영
```

외부 AI는 main 또는 사용자의 활성 worktree를 직접 수정하지 않는다. 외부 AI 결과는 검수 대기 입력이다.

## 6. 구현과 검증

일반 변경은 `reviewing-and-validating-project-changes`를 사용한다.

```text
contract-check
→ 필요한 경우 external-source-review
→ static-validation
→ runtime-validation
→ regression
→ evidence-report
```

- 가장 작은 검증 가능한 변경으로 완료 기준을 만족한다.
- 기존 기능·저장 데이터·공개 인터페이스·사용자 흐름을 보호한다.
- 기능 추가와 대규모 리팩터링을 가능한 한 분리한다.
- 실행하지 못한 검증은 `UNVERIFIED`와 사유로 기록한다.

최소 검증 순서:

```text
작업 계약·diff 대조
→ 포맷·문법·정적 검사
→ 관련 자동 테스트
→ 정상·실패·경계·반례
→ 저장·불러오기·호환성
→ 실제 화면·플레이·오디오·성능
→ 인접 기능 회귀
→ 판정·위험·롤백
```

## 7. 문서·발행·상태 동기화

방향, 수치, 용어, 기능, 구현 상태, 승인 자산, 검증 또는 일정이 바뀌면 같은 작업에서 관련 책임 원본과 Registry·Roadmap·Active Context를 갱신한다.

기획서 작업은 `managing-design-documents`가 문서 생명주기와 발행 정책을 함께 처리한다. `source_only`, `milestone_sync`, `always_sync` 중 Registry가 선언한 정책을 따른다.

## 8. 종료·인수인계·학습

1. 실제 변경과 검증 결과를 책임 원본에 반영한다.
2. `maintaining-project-context-and-handoff`로 현재 상태·다음 작업·위험을 압축한다.
3. 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 Skill 호출을 Learning Log에 기록한다.
4. 공용화 가치가 있으면 `managing-base-change-proposals`로 제안한다.
5. 완료 보고에서 변경·검증·미검증·사용자 확인·위험·롤백을 분리한다.
