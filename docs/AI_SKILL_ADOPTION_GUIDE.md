# AI Skill Adoption Guide

외부 또는 내부 AI Skill을 채택·작성·검증할 때 사용하는 공용 기준이다. Skill은 도구 이름이 아니라 반복 가능한 판단과 작업 계약이다.

최신 프롬프트·Agent·Skill·작업구조 후보를 찾을 때는 `docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`의 `PROMPT_AND_AGENT_WORKFLOW`·`SKILL_AUTHORING_AND_EVOLUTION` Source Pool을 발견용으로 사용할 수 있다. 외부 제품의 기능·예시는 Base 정본이 아니며, 가능한 경우 공식 원출처와 실제 대표 작업 Eval로 다시 확인한다.

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

## 2A. REVERSE_ENGINEERED_SKILL_WORKFLOW_CANDIDATE

외부 Skill, Agent workflow, 프롬프트 체계, 작업구조, 제작 프로세스에서 재사용 가능한 부분을 발견한 경우 **패키지 전체를 모방하는 대신 `PATTERN_NOT_PACKAGE_COPY`를 기본값**으로 한다.

```text
OBSERVE REPRESENTATIVE TASKS
→ SOURCE / LICENSE / PERMISSION CHECK
→ CONTRACT EXTRACTION
→ VENDOR-SPECIFIC EXPRESSION REMOVAL
→ EXISTING OWNER / PLACEMENT COMPARISON
→ MINIMUM ABSORPTION OR BOUNDED REIMPLEMENTATION
→ EVAL_BEFORE_PROMOTION
→ PROJECT PILOT
→ BASE PROMOTION ONLY IF REPEATED AND DISTINCT
```

### 추출할 계약

외부 절차의 이름이나 마케팅 문구보다 다음을 기록한다.

```yaml
trigger:
goal:
required_inputs:
source_of_truth:
protected_constraints:
state_or_steps:
tool_and_permission_boundary:
output_contract:
failure_and_recovery:
validation_or_quality_bar:
handoff_or_stop_condition:
```

- 특정 공급자 persona, 브랜드 용어, 장식적인 “magic wording”은 핵심 계약으로 오인하지 않는다.
- 동일한 효과가 현재 Base instruction, Template, 기존 Skill mode, deterministic Tool로 가능하면 새 Skill을 만들지 않는다.
- 외부 프로세스가 독립 도메인 권한이 아니라 실행 방식만 바꾸면 `CAPABILITY_COMPOSITION_MAP.md`의 `EXTERNAL_PROCESS_OVERLAY`로 남길 수 있다.
- 직접 패키지를 설치·복사하는 것이 더 적합하면 라이선스, 출처, 버전 pin, 의존성, 권한, 보안·공급망과 rollback을 검토한 뒤 Existing Solution First로 처리한다.
- 제3자 proprietary instruction·코드·문구를 권한 없이 Base에 복사하지 않는다.

### 배치 우선순위

```text
기존 owner의 짧은 규칙 보강
→ 기존 Template/Reference 보강
→ 기존 Skill의 mode로 흡수
→ deterministic script/tool
→ EXTERNAL_PROCESS_OVERLAY
→ 독립 Skill/Agent (마지막 수단)
```

독립 Skill/Agent는 반복 빈도가 높다는 이유만으로 만들지 않는다. 고유 trigger, 입력, authority, 산출물, 실패 조건과 별도 검증 경계가 있어야 한다.

### EVAL_BEFORE_PROMOTION

역공학한 Workflow/Skill 패턴을 Base ACTIVE 계약으로 승격하기 전 다음을 비교한다.

1. 패턴 적용 전 대표 작업의 누락·오판·시간/Context 비용.
2. 패턴 적용 후 같은 대표 작업.
3. 입력을 변형한 시나리오.
4. 패턴을 **선택하면 안 되는** negative-routing 시나리오.
5. 실패·부분 입력·도구 불가·권한 부족 시나리오.
6. 기존 Skill/Workflow와의 중복, handoff 손실, 유지보수 비용.

문서가 그럴듯하거나 유명 팀/제품이 쓴다는 사실은 승격 증거가 아니다. 실제 개선이 확인되지 않으면 `REFERENCE_ONLY`, `TEST`, 또는 프로젝트 전용으로 유지한다.

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

## 5A. Prompt / Instruction / Skill / Agent / Tool 배치 결정

프롬프트 품질 문제를 모두 “프롬프트를 더 길게 쓴다”로 해결하지 않는다. 반복 지식과 실행 권한을 다음의 가장 작은 책임 단위에 둔다.

| 반복되는 필요 | 기본 배치 후보 | 사용 이유 |
|---|---|---|
| 거의 모든 요청에 적용되는 짧고 안정적인 규칙 | repository/global instruction | 항상 필요한 최소 context |
| 특정 경로·파일 종류에만 적용되는 규칙 | path/domain-specific instruction | unrelated context 오염 방지 |
| 입력값만 바뀌는 반복 요청 형식 | prompt/template | 재사용 가능한 요청 구조이며 독립 실행 책임이 없음 |
| 특정 작업의 절차·판단·reference·script를 필요할 때만 로드 | Skill | task-specific 전문성을 progressive disclosure로 제공 |
| 독립 persona·tool set·권한·context·handoff가 필요한 specialist | agent | 별도 실행 경계와 책임이 존재 |
| 정확히 반복돼야 하는 계산·검사·변환 | deterministic script/tool | 자연어 추론보다 재현성과 실패 가시성이 중요 |

### 배치 Gate

```text
이 정보가 거의 모든 요청에 필요한가?
→ YES: 짧은 global/repository instruction 후보
→ NO

특정 task에서 반복 호출하지만 독립 tool/permission 경계는 없는가?
→ YES: prompt/template 또는 Skill 후보

절차·reference·script·edge case를 on-demand로 묶어야 하는가?
→ YES: Skill 후보

독립 tool set·권한·persona·context isolation·handoff가 필요한가?
→ YES: agent 후보

정확히 같은 변환·검사가 반복되는가?
→ YES: deterministic script/tool 후보
```

### 프롬프트 작성 최소 계약

재사용 프롬프트는 장식적인 역할극보다 다음 연결을 먼저 가진다.

```yaml
goal:
source_of_truth:
required_inputs:
protected_constraints:
changeable_scope:
process_or_decision_steps:
output_contract:
edge_cases:
stop_or_handoff_conditions:
validation:
unverified_or_missing_input_behavior:
```

규칙:

- 목표·완료 기준·정본·보호 대상·출력 형식을 분명히 한다.
- 긴 문서에서 행동 가능한 절차를 추출할 때는 각 단계가 구체적인 행동 또는 산출물과 연결되게 한다.
- 예외·입력 누락·실패·중단·사용자 결정 필요 조건을 정상 경로와 함께 쓴다.
- 항상 필요한 context와 task-specific context를 분리하고, 후자는 필요할 때만 로드한다.
- 프롬프트를 파일 여러 개로 쪼갰다는 사실만으로 modular architecture가 된 것은 아니다. **독립적으로 변경·테스트·라우팅할 책임**이 있을 때만 분리한다.
- 반대로 서로 다른 책임·정책·tool 선택·검증이 한 거대 system prompt에 얽혀 부분 수정의 회귀 위험이 커지면 module·Skill·agent 경계를 검토한다.
- 특정 모델의 “잘 먹히는 문구”는 `PATTERN` 또는 `TEST`이며 모델·버전·도구·harness가 바뀌면 재검증한다.

### Agent / Skill 과분할 방지

- 하나의 agent가 명확한 tools와 instructions로 안정적으로 처리할 수 있으면 먼저 단일 agent를 강화한다.
- multi-agent는 복잡한 논리·충돌하는 context·겹치는 tool 선택·독립 reviewer처럼 **분리로 검증 가능성이 실제 개선될 때** 검토한다.
- Skill 수, agent 수, prompt 파일 수는 능력 지표가 아니다.
- 동일 책임을 instruction·prompt·Skill·agent에 동시에 복제하지 않는다. 한 owner를 두고 다른 surface는 링크·라우팅한다.
- runtime에서 자동 생성된 Skill이나 외부 Skill을 발견했다고 Base ACTIVE Skill로 자동 승격하지 않는다.

## 6. 검증

새 Skill과 큰 수정은 다음을 검증한다.

1. Skill 없이 대표 작업을 수행했을 때의 누락·오판을 기록한다.
2. 그 실패를 막는 최소 계약을 작성한다.
3. 동일·변형·반례 시나리오에 적용한다.
4. 과도한 단계·잘못된 trigger·중복 mode를 수정한다.
5. Registry 경로·상태·Learning Log를 검증한다.
6. 실제 프로젝트에서 사용한 뒤 지식 상태를 갱신한다.

문서 존재는 적용 성공의 증거가 아니다.

### Prompt·Agent 구조 검증

- 대표 prompt에서 변경 전·후 목표 성공과 실패 유형을 비교하는가?
- system/repository instruction만 바꾼 경우 unrelated task 회귀를 함께 검사하는가?
- Skill description 변경은 선택돼야 할 Prompt와 **선택되면 안 되는 Prompt**를 모두 검사하는가?
- agent 분할 전후에 tool 선택 오류·handoff 손실·context 충돌·비용/시간을 비교하는가?
- eval은 모델 이름만이 아니라 실제 harness·tool·permission·budget·configuration을 가능한 범위에서 고정·기록하는가?
- 평가 환경이나 product harness 변화가 모델 품질 변화처럼 보일 수 있음을 공격하는가?
- 사람의 목표·도메인 판단과 agent의 실행 결정을 구분하고, 사람이 넘기지 않은 제품 방향 권한을 agent에게 암묵적으로 주지 않는가?

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

## 10. Consumer surface·branch-state 검증

프롬프트·instruction·Skill·agent 기능은 제품 전체에 균일하게 지원된다고 가정하지 않는다. 같은 제품 안에서도 **consumer surface**(예: Chat, cloud agent, code review, IDE, CLI)별 지원 여부가 surface마다 다를 수 있다.

- 채택 전 현재 공식 compatibility/support matrix에서 실제 소비 surface가 해당 customization을 읽는지 확인한다.
- Preview 기능은 안정된 공용 계약처럼 고정하지 않고 version·surface와 함께 `TEST`로 둔다.
- PR 기반 AI review처럼 branch 내용의 영향을 받는 surface는 어떤 branch의 instruction/Skill을 읽는지 확인한다. 공식 문서가 **head branch**를 읽는다고 명시한 surface라면 같은 PR에서 변경을 시험할 수 있지만, 다른 surface의 base/head 동작까지 자동 일반화하지 않는다.
- 공식 문서끼리 branch semantics가 충돌하거나 시점 차이가 의심되면 현재 실제 surface에서 재현해 `PARTIALLY_VERIFIED` 또는 `UNVERIFIED`로 남긴다.
- Eval 기록에는 model뿐 아니라 consumer surface·client/version·branch/ref·harness·tool·permission·budget·configuration을 가능한 범위에서 포함한다.
