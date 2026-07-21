# 프로젝트 AI·GitHub 작업 흐름

## 1. 목적

사용자는 만들고 싶은 결과와 중요한 방향을 설명한다. 저장소 운영체계는 책임 원본, 최소 Skill, 실행 순서, 개발 게이트, 검증과 인수인계를 기억한다.

```text
사용자 방향
→ managing-project-intake-and-work-contract
→ Definition of Ready
→ 필요 시 decompose-and-sequence
→ 필요 시 analyzing-and-refining-game-concepts
→ 벤치마크·플레이어 반응·PoC·플레이테스트
→ 사용자 승인
→ Implementation
→ reviewing-and-validating-project-changes
→ 필요 시 reference-freshness·accessibility-review·performance-profile
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

`managing-project-intake-and-work-contract`의 `route → clarify → contract → 필요한 경우 decompose-and-sequence` 흐름에서 한 번만 판정한다.

- 전체 Skill 로드 금지
- 주 책임 분야 Skill 최대 하나
- trigger·비사용 조건 확인
- 발행·검증·Handoff는 해당 단계에서만 실행
- 저장소에서 확인할 사실을 사용자에게 다시 묻지 않음
- 기능·경험·아트 방향·구조·워크플로 변경은 사용자 확인 전 실행 금지
- 큰 작업은 검증 가능한 결과·의존성·게이트로 분해
- 외부 근거는 요구 권한이나 구현 정본으로 사용하지 않음
- Godot·Web UI 결과 감사는 `auditing-and-refining-ui-art`
- 정본·경로·ID·Schema·정책·생성기 변경은 `auditing-canonical-reference-freshness`를 검증 단계에 보류 등록

## 4. 주요 실행 Skill

| 작업 | Skill·mode |
|---|---|
| 요청 접수·작업 계약 | `managing-project-intake-and-work-contract: route → clarify → contract` |
| 작업 분해·의존성·순서 | `managing-project-intake-and-work-contract: decompose-and-sequence` |
| 신규 운영체계 | `managing-game-project-operating-system: install → verify` |
| 기존 구조 변경 | `managing-game-project-operating-system: audit → migrate → verify` |
| 핵심 컨셉·DDD·SWOT·PoC·재조정 | `analyzing-and-refining-game-concepts` |
| 경쟁작·플레이어 반응 조사 | `analyzing-and-refining-game-concepts: benchmark-and-player-research` |
| 플레이테스트·퍼널·A/B 실험 | `analyzing-and-refining-game-concepts: playtest-and-experiment` |
| 기획 책임 원본·발행 | `managing-design-documents` |
| 프로젝트 Skill 학습·통합 | `evolving-project-discipline-skills` |
| 현재 상태·Handoff | `maintaining-project-context-and-handoff` |
| 프로젝트 교훈·Base 제안 | `managing-base-change-proposals` |
| Vertical Slice | `designing-vertical-slices` |
| 외부 AI 작업 공간 | `orchestrating-deepseek-worktrees` |
| 변경·외부 AI 결과 검증 | `reviewing-and-validating-project-changes` |
| 접근성 장벽 | `reviewing-and-validating-project-changes: accessibility-review` |
| 목표 플랫폼 성능 | `reviewing-and-validating-project-changes: performance-profile` |
| 오래된 참조·정본 drift·변경 전파 누락 | `auditing-canonical-reference-freshness` |
| 이미지 프롬프트 | `designing-art-prompts-and-technique-cards` |
| 구현된 UI 감사 | `auditing-and-refining-ui-art` |

## 5. 작업 분해·순서 흐름

```text
승인 작업 계약
→ 독립 검증 가능한 결과 단위
→ BLOCKS·INFORMS·USES_OUTPUT·SHARES_RESOURCE 관계
→ 위험·가치·피드백 속도 기반 정렬
→ 안전한 병렬 묶음
→ 단계별 완료·검증·롤백
→ 게이트 실패 시 재계획
```

각 단계는 `outcome / inputs / files / dependencies / output / acceptance / validation / rollback`을 가진다. “코딩”, “문서 수정”처럼 동사만 있는 작업은 실행 단계로 인정하지 않는다.

기본 순서:

```text
환경·권한
→ 정본·인터페이스·Schema
→ 가장 위험한 가설
→ 핵심 사용자·플레이어 경로
→ 통합
→ 정상·실패·경계·회귀
→ 문서·발행·참조 최신성
→ 사용자 검수·인수인계
```

## 6. 핵심 컨셉·외부 근거·PoC 흐름

```text
frame: 한 문장 핵심 컨셉·플레이어 약속
→ constrain: 플레이·제작·기술·콘텐츠·시장 제약
→ sharpen: 뾰족한 재미와 반복 원동력
→ structure: GDD·레벨·캐릭터·스테이지·세계관 정렬
→ benchmark-and-player-research: 제품 사실·플레이어 반응·행동 근거
→ analyze: SWOT→SO/WO/ST/WT, MDA/DDE/DDD, 3C, 루프·동기·차별화·제작성
→ playtest-and-experiment: 빌드·표본·피드백·이벤트·퍼널·A/B 계약
→ poc-contract: 가장 위험한 가설의 최소 검증
→ recalibrate: KEEP/AMPLIFY/CHANGE/REMOVE/DEFER/RETEST
→ production-gate: PRODUCTION_READY/REPEAT_POC/HOLD/STOP
```

### 벤치마크·플레이어 반응

- 조사 전에 현재 결정을 바꿀 질문과 비교 차원을 고정한다.
- 공식 제품 사실, 플레이어 자기보고, 이벤트·퍼널 행동, 통제 실험, 해석을 분리한다.
- 긍정·부정·혼합, 최신·누적, 플레이타임·플랫폼·언어·패치 차이를 기록한다.
- 기능 복사가 아니라 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 개선 원리를 판정한다.
- 리뷰 폭탄·오프토픽·강한 표현을 중요도와 혼동하지 않는다.

### 플레이테스트·실험

- 빌드·버전·대상 집단·기존 노출·과제·피드백 채널을 고정한다.
- 관찰 행동, 이벤트·퍼널, 인터뷰·설문을 분리한다.
- A/B 테스트는 하나의 주요 가설, 통제군·변형, 사전 선언한 지표·가드레일로 비교한다.
- 결과를 본 뒤 성공 기준을 바꾸지 않는다.

Base 내부에서 `DDD`는 `Digital Dopamine Design`이다. 첫 의미 있는 보상, 행동-피드백 지연, 보상 명료성·밀도, Micro→Session→Meta 보상 사다리, 다음 행동 의도와 피로·인플레이션을 관찰한다. 외부 자료의 동명 약어는 출처 정의를 확인하기 전 임의 해석하지 않는다.

PoC는 전체 게임이나 Vertical Slice가 아니며, 목표 품질·실제 플레이 증거·제작 파이프라인 검증은 `designing-vertical-slices`로 넘긴다.

## 7. Plan contract

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
canonical_sources_and_consumers:
known_renames_aliases_and_replacements:
external_evidence_questions:
playtest_and_telemetry:
execution_steps:
dependencies:
parallel_batches:
gates:
accessibility_scope:
performance_budget:
risks_and_fallbacks:
acceptance_criteria:
validation:
document_skill_publication_updates:
rollback:
```

L2 이상은 실제 저장소 조사에 기반한 Plan과 사용자 승인을 우선한다. 여러 단계·분야·외부 의존성이 있으면 `decompose-and-sequence` 결과를 포함한다.

## 8. 작업 실행 게이트

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval·Sequencing
→ Implementation
→ Verification
→ Documentation·Publication
→ Integration·Completion
→ Context·Learning
```

### Definition of Ready

- 목적·사용자 경험·범위·제외·보호 대상
- 책임 분야·의존성·선행 조건
- 저장·호환성·승인 자산 위험
- 관찰 가능한 완료 기준
- 자동·수동·사용자 검수
- 책임 원본·Skill·발행 영향
- 정본 변경과 영향 소비자·참조·파생본 후보
- 필요한 외부 근거·플레이테스트·접근성·성능 범위

### Implementation

- 승인 Plan 범위만 변경
- 가장 작은 검증 가능한 변경
- 기능 추가와 대규모 리팩터링 분리
- 저장·인터페이스·사용자 흐름 보호
- 보류 항목·승인 이미지 임의 변경 금지
- 파일·ID·Schema·경로를 바꾸면 새 정본만 추가하지 말고 이전 참조와 소비자도 추적
- 단계·의존성·게이트 변경 시 실행 순서를 갱신

### Verification

`reviewing-and-validating-project-changes`를 사용한다.

```text
contract-check
→ 필요한 경우 external-source-review
→ 정본·경로·ID·Schema 변경 시 reference-freshness
→ static-validation
→ runtime-validation
→ 적용 시 accessibility-review
→ 적용 시 performance-profile
→ regression
→ evidence-report
```

`reference-freshness`는 `auditing-canonical-reference-freshness`를 호출해 활성 파일의 오래된 참조, untouched 소비자, 정책·상태 drift, 원본·생성기와 맞지 않는 PDF·Manifest·해시, 허용된 Legacy·Change Log·과거 case를 구분한다.

접근성은 텍스트·대비·핵심 정보 채널·입력·자막·오디오·난이도·시간·탐색·모션의 실제 장벽과 대안을 확인한다. 성능은 목표 플랫폼·빌드·대표·최악 장면에서 frame time·CPU·GPU·메모리·네트워크·로딩을 baseline과 같은 조건으로 비교한다.

검증 시 대표 정상·실패·경계·원래 실패 반례·저장 호환성·실제 화면과 인접 기능 회귀를 확인한다. 실행하지 않은 검증은 `UNVERIFIED`와 이유로 기록한다.

## 9. 문서·발행 흐름

`managing-design-documents`가 책임 원본 작성·구조 변경·발행·검수를 하나의 생명주기로 처리한다.

Registry 발행 정책:

- `source_only`
- `milestone_sync`
- `always_sync`

정책이 요구할 때만 PDF·Manifest를 동기화하고 DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`와 사람 시각 검수 완료를 혼동하지 않는다.

## 10. 기존 프로젝트 마이그레이션

```text
Audit only
→ 기존 문서·이미지·참조·고유 정보 지도
→ 목표 책임 구조·보존·롤백 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ 보존·참조·발행·콜드 스타트 verify
```

마이그레이션과 Skill 통합 뒤에는 이전 경로·ID가 활성 파일에 남지 않았는지 reference freshness 검사를 실행한다.

## 11. GitHub 역할

- 책임 원본·코드·데이터·자산·발행본 이력
- Parent Issue·sub-issue·dependency·milestone 작업 구조
- Issue·PR 작업 계약과 단계별 완료 증거
- CODEOWNERS 리뷰
- Governance Checker와 엔진 테스트
- Required Status Checks
- 릴리스·빌드·검증 증거

파일 존재, Workflow 실행, Required Check 강제를 별도 상태로 기록한다.

## 12. 완료 보고

```md
## 결과
- 주 책임·영향 분야:
- 실행 단계·의존성·게이트:
- 핵심 컨셉·DDD·벤치마크·플레이테스트·PoC:
- 변경한 책임 원본·실제 파일·Skill:
- 정본·참조 최신성·변경 전파 결과:
- 접근성 장벽·성능 예산 결과:
- 생성한 PDF·선택 DOCX·다이어그램·Manifest:
- 보호한 결정·동작·자산:
- 검증 판정·증거:
- 사람 시각·플레이 검수:
- 미검증·불일치·위험·롤백:
- Learning Log·Base 제안:
- 다음 작업·Active Context·Handoff:
```
