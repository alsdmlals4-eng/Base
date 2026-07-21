# 프로젝트 AI·GitHub 작업 흐름

## 1. 목적

사용자는 만들고 싶은 결과와 중요한 방향을 설명한다. 저장소 운영체계는 책임 원본, 최소 Skill, 개발 게이트, 검증과 인수인계를 기억한다.

```text
사용자 방향
→ managing-project-intake-and-work-contract
→ Definition of Ready
→ 사용자 승인
→ 실제 저장소 조사·Plan
→ Implementation
→ Verification
→ 책임 원본·발행·Active Context 동기화
→ PR Required Checks·리뷰
→ Learning Log·Base 제안
```

## 2. 공통 시작 순서

```text
최신 사용자 지시
→ 프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ Active Context·Documentation Map·Development Gates
→ Design Document Registry·현재 책임 원본
→ Skill Registry·필요한 통합 Skill과 mode
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
```

백업·보류·제거 후보와 전체 skills 폴더는 기본 읽기에서 제외한다.

## 3. 요청·Skill 라우팅

```yaml
request:
work_level: L0/L1/L2/L3/L4
project_mode: new/existing/operational
primary_discipline:
affected_disciplines:
change_types:
required_design_document_ids:
foundation_skills:
discipline_skills:
deferred_skills:
asset_impact:
publication_impact:
routing_reason:
```

`managing-project-intake-and-work-contract`의 `route → clarify → contract` 흐름에서 한 번만 판정한다.

- 전체 Skill 로드 금지
- 주 책임 분야 Skill 최대 하나
- trigger·비사용 조건 확인
- 발행·검증·Handoff는 해당 단계에서만 실행
- 저장소에서 확인할 사실을 사용자에게 다시 묻지 않음
- 기능·경험·아트 방향·구조·워크플로 변경은 사용자 확인 전 실행 금지
- Godot·Web UI 결과 감사는 `auditing-and-refining-ui-art`

## 4. 주요 실행 Skill

| 작업 | Skill·mode |
|---|---|
| 요청 접수·작업 계약 | `managing-project-intake-and-work-contract` |
| 신규 운영체계 | `managing-game-project-operating-system: install → verify` |
| 기존 구조 변경 | `managing-game-project-operating-system: audit → migrate → verify` |
| 기획 책임 원본·발행 | `managing-design-documents` |
| 프로젝트 Skill 학습·통합 | `evolving-project-discipline-skills` |
| 현재 상태·Handoff | `maintaining-project-context-and-handoff` |
| 프로젝트 교훈·Base 제안 | `managing-base-change-proposals` |
| Vertical Slice | `designing-vertical-slices` |
| 외부 AI 작업 공간 | `orchestrating-deepseek-worktrees` |
| 외부 AI 결과 검수 | `reviewing-external-ai-drafts` |
| 이미지 프롬프트 | `designing-art-prompts-and-technique-cards` |
| 구현된 UI 감사 | `auditing-and-refining-ui-art` |

## 5. Plan contract

```yaml
problem:
user_or_player_value:
primary_discipline:
affected_disciplines:
required_design_document_ids:
foundation_skills:
discipline_skills:
scope:
out_of_scope:
repository_findings:
protected_decisions_paths_assets:
files_to_change:
data_and_state_ownership:
asset_ui_audio_impact:
migration_and_compatibility:
risks_and_fallbacks:
acceptance_criteria:
validation:
document_skill_publication_updates:
rollback:
```

L2 이상은 실제 저장소 조사에 기반한 Plan과 사용자 승인을 우선한다.

## 6. 작업 실행 게이트

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation·Publication
→ Integration·Completion
→ Context·Learning
```

### Definition of Ready

- 목적·사용자 경험·범위·제외·보호 대상
- 책임 분야·의존성
- 저장·호환성·승인 자산 위험
- 관찰 가능한 완료 기준
- 자동·수동·사용자 검수
- 책임 원본·Skill·발행 영향

### Implementation

- 승인 Plan 범위만 변경
- 가장 작은 검증 가능한 변경
- 기능 추가와 대규모 리팩터링 분리
- 저장·인터페이스·사용자 흐름 보호
- 보류 항목·승인 이미지 임의 변경 금지

### Verification

```text
포맷·문법·정적 검사
→ 자동 테스트
→ 정상·실패·경계 경로
→ 저장·호환성
→ 실제 화면·플레이·오디오·성능
→ diff·승인 범위
→ 사용자 검수
```

실행하지 않은 검증은 `[미검증]`으로 기록한다.

## 7. 문서·발행 흐름

`managing-design-documents`가 책임 원본 작성·구조 변경·발행·검수를 하나의 생명주기로 처리한다.

Registry 발행 정책:

- `source_only`
- `milestone_sync`
- `always_sync`

정책이 요구할 때만 PDF·Manifest를 동기화하고 DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`와 사람 시각 검수 완료를 혼동하지 않는다.

## 8. 기존 프로젝트 마이그레이션

```text
Audit only
→ 기존 문서·이미지·참조·고유 정보 지도
→ 목표 책임 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ 보존·참조·발행·콜드 스타트 verify
```

## 9. GitHub 역할

- 책임 원본·코드·데이터·자산·발행본 이력
- Issue·PR 작업 계약
- CODEOWNERS 리뷰
- Governance Checker와 엔진 테스트
- Required Status Checks
- 릴리스·빌드·검증 증거

파일 존재, Workflow 실행, Required Check 강제를 별도 상태로 기록한다.

## 10. 완료 보고

```md
## 결과
- 주 책임·영향 분야:
- 변경한 책임 원본·실제 파일·Skill:
- 생성한 PDF·선택 DOCX·다이어그램·Manifest:
- 보호한 결정·동작·자산:
- 실행한 검증:
- 사람 시각 검수:
- 미검증·불일치·위험·롤백:
- Learning Log·Base 제안:
- 다음 작업·Active Context·Handoff:
```
