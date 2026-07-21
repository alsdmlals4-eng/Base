# AI Skill Adoption Guide

외부 또는 내부 AI Skill을 채택·작성·검증할 때 사용하는 공용 기준이다. Skill은 도구 이름이 아니라 반복 가능한 판단과 작업 계약이다.

## 1. 우선순위

Skill과 외부 모델은 다음을 덮어쓸 수 없다.

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진 규칙
3. 승인된 책임 원본·Issue·Plan
4. 실제 파일과 실행 결과
5. Base 또는 외부 Skill·모델

플러그인 미설치나 실행 실패는 작업을 완료한 것으로 간주할 수 없지만, 동등한 일반 절차로 진행할 수 있다. 외부 벤치마크·리뷰·기사·모델 해석은 요구사항 권한이나 구현 사실의 정본이 아니다.

## 2. 채택 전 확인

- 실제 trigger와 맞는가?
- 기존 통합 Skill의 mode로 처리할 수 있는가?
- 독립된 입력·산출물·Quality Bar·검증 경로가 있는가?
- 기존 Base·프로젝트 규칙과 중복되거나 충돌하는가?
- 추가 파일 쓰기·네트워크·API 키·브라우저 데이터 권한이 필요한가?
- 실패 시 복구와 독립 검증이 가능한가?

새 Skill은 기존 Skill의 mode로 표현할 수 없고, 반복 빈도와 별도 검증 경계가 있을 때만 만든다. 벤치마크 조사와 작업 순서 설계는 각각 기존 기획 분석과 요청·계약 생명주기의 mode로 흡수한다.

## 3. 최소 라우팅

기본값은 통합 Foundation Skill 1개와 필요한 전문 Skill 1개 이하이다. 발행·검증·Handoff는 해당 단계에서만 실행한다.

| 작업 신호 | 우선 Skill·mode |
|---|---|
| 새 요청·모호성·작업 계약 | `managing-project-intake-and-work-contract: route → clarify → contract` |
| 작업 분해·의존성·순서·병렬화 | `managing-project-intake-and-work-contract: decompose-and-sequence` |
| 신규 프로젝트 설치 | `managing-game-project-operating-system: install` |
| 기존 프로젝트 구조 변경 | `managing-game-project-operating-system: audit → migrate → verify` |
| 기획 책임 원본·발행 | `managing-design-documents` |
| 프로젝트 Skill 통합·학습 | `evolving-project-discipline-skills` |
| 현재 상태·Handoff | `maintaining-project-context-and-handoff` |
| 핵심 컨셉·뾰족한 재미·DDD·SWOT·PoC | `analyzing-and-refining-game-concepts` |
| 경쟁작·플레이어 리뷰·유저 반응 | `analyzing-and-refining-game-concepts: benchmark-and-player-research` |
| 플레이테스트·이벤트·퍼널·A/B | `analyzing-and-refining-game-concepts: playtest-and-experiment` |
| 프로젝트 교훈·BCP | `managing-base-change-proposals` |
| 목표 품질·실제 플레이·파이프라인 | `designing-vertical-slices` |
| 대량 외부 AI 작업 | `orchestrating-deepseek-worktrees` |
| 변경·외부 AI 결과 통합 검증 | `reviewing-and-validating-project-changes` |
| 접근성 장벽 | `reviewing-and-validating-project-changes: accessibility-review` |
| 목표 플랫폼 성능 | `reviewing-and-validating-project-changes: performance-profile` |
| 정본·경로·ID·Schema 변경 전파 감사 | `auditing-canonical-reference-freshness` |
| 이미지 프롬프트·기술 카드 | `designing-art-prompts-and-technique-cards` |
| Godot·Web UI 결과 감사 | `auditing-and-refining-ui-art` |

통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`를 사용한다.

## 4. 실행 가능한 Skill 계약

```yaml
name:
skill_id:
discipline:
purpose:
use_when:
do_not_use_when:
trigger_tags:
load_by_default: false
modes: []
required_inputs:
read_first:
process:
outputs:
definition_of_ready:
definition_of_done:
validation:
failure_conditions:
related_skills:
learning_log:
review_triggers:
last_reviewed_at:
last_reviewed_commit:
knowledge_state:
```

하나의 생명주기를 단계별 Skill로 쪼개지 말고 하나의 Skill 내부 mode와 상태 머신으로 우선 표현한다. 반대로 생성 전 설계와 구현 후 감사처럼 입력·도구·승인 경계가 다르면 독립 Skill로 유지한다.

## 5. Skill 패키지 구조

```text
skills/<skill-name>/
├─ SKILL.md
├─ references/   # 고유한 상세 계약이 있을 때만
└─ scripts/      # 실제 자동화가 있을 때만
```

Method·Checklist·Template에 같은 실행 절차를 장문 복제하지 않는다.

- `SKILL.md`: 언제 사용하고 어떤 상태·mode로 실행하는가
- `references/`: 이유·배경·상세 Schema·판단 모델·공식 근거
- `templates/`: 복사할 출력 형식
- `scripts/`: 자동 검사·변환

## 6. 검증

새 Skill과 큰 수정은 다음을 검증한다.

1. Skill 없이 대표 작업을 수행했을 때의 누락·오판을 기록한다.
2. 그 실패를 막는 최소 계약을 작성한다.
3. 동일·변형·반례 시나리오에 적용한다.
4. 과도한 단계·잘못된 trigger·중복 mode를 수정한다.
5. Registry 경로·상태·Learning Log를 검증한다.
6. 실제 프로젝트에서 사용한 뒤 지식 상태를 갱신한다.

문서 존재는 적용 성공의 증거가 아니다.

### 작업 분해·순서 mode

- 활동이 아니라 검증 가능한 결과 단위인가?
- 선행·차단·출력 소비·공유 자원·독립 검증 관계가 있는가?
- 위험한 가설과 핵심 사용자 가치가 장식·후처리보다 앞서는가?
- 병렬 작업의 입력·출력·파일 경계와 통합 지점이 고정됐는가?
- 단계 실패·미검증 뒤 재계획 조건이 있는가?

### 기획 분석·외부 근거 mode

- 기능 목록과 핵심 컨셉을 구분하는가?
- 비교 대상이 장르 이름이 아니라 현재 결정의 비교 차원으로 선정됐는가?
- 제품 사실·플레이어 자기보고·행동 데이터·통제 실험·해석을 분리하는가?
- 긍정·부정·버전·플레이타임·플랫폼·언어와 표본 편향을 기록하는가?
- 벤치마크가 `ADOPT / ADAPT / AVOID / TEST / IGNORE` 개선 결정으로 연결되는가?
- SWOT을 SO·WO·ST·WT 행동으로 변환하는가?
- MDA·DDE·DDD·3C·루프 같은 분석축이 개선 결정으로 연결되는가?
- DDD가 첫 의미 있는 보상, 행동-피드백 지연, 보상 명료성·밀도, Micro→Session→Meta 보상 사다리, 다음 행동 의도와 피로·인플레이션으로 관찰되는가?
- 빠른 보상이 뾰족한 재미와 의미 있는 선택을 강화하고, 자극·팝업·손실 압박으로 대체하지 않는가?
- 외부 자료의 동명 `DDD`는 출처 정의 확인 전 임의 해석하지 않는가?
- 플레이테스트가 빌드·표본·과제·피드백·행동 이벤트·퍼널·성공 기준을 가지는가?
- A/B 테스트가 한 주요 가설과 사전 선언한 지표를 비교하는가?
- PoC가 가장 위험한 가설을 검증하는 최소 범위인가?

### 변경 검증 mode

변경 주체와 무관하게 계약 대조, 필요한 경우 정본·참조 최신성, 정적 검사, 가능한 런타임, 접근성 장벽, 목표 플랫폼 성능, 대표·경계·반례·회귀, 미실행과 롤백을 연결해야 한다.

- 접근성은 옵션 존재가 아니라 실제 핵심 경로의 장벽과 대안을 검수한다.
- 접근성 결과를 법적 준수 인증으로 표현하지 않는다.
- 성능은 같은 빌드·장면·하드웨어의 baseline과 frame time·CPU·GPU·메모리·네트워크·로딩을 비교한다.
- 평균 FPS나 에디터 빈 장면만으로 통과시키지 않는다.

## 7. 외부 AI·worktree

- main과 사용자의 활성 worktree를 직접 수정하게 하지 않는다.
- 저장소 전체 대신 Documentation Map·Active Context·allowlist를 제공한다.
- 결과는 구조화된 초안과 미확인 목록으로 회수한다.
- 실제 diff·참조·테스트를 `reviewing-and-validating-project-changes: external-source-review`로 독립 검수한다.
- 보안·저장·호환성·테스트는 토큰 절약 대상이 아니다.

## 8. 아트·UI Skill 경계

- 생성·편집 전 계약과 프롬프트: `designing-art-prompts-and-technique-cards`
- 구현된 화면의 구조·간격·타이포·상태 감사: `auditing-and-refining-ui-art`
- 플레이 장벽·입력·정보 채널의 접근성 판정: `reviewing-and-validating-project-changes: accessibility-review`

세 책임은 합치지 않는다. 한 번 성공한 프롬프트는 먼저 관찰·가설·패턴 상태의 기술 카드나 Case로 기록한다.

## 9. 학습과 통합

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출만 Learning Log에 기록한다.

Skill 통합 전에는 고유 입력·산출물·실패 조건·검증·Learning Log·Registry 참조를 대조한다. 이전 버전은 Git 이력으로 보존하고, 과거 ID는 `LEGACY_SKILL_ALIASES.md`로 연결한다. 통합·이름 변경·경로 이동 뒤에는 `auditing-canonical-reference-freshness`로 이전 경로와 untouched 소비자를 검사한다.
