# AI Skill Adoption Guide

외부 또는 내부 AI Skill을 채택·작성·검증할 때 사용하는 공용 기준이다. Skill은 도구 이름이 아니라 반복 가능한 판단과 작업 계약이다.

## 1. 우선순위

Skill과 외부 모델은 다음을 덮어쓸 수 없다.

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진 규칙
3. 승인된 책임 원본·Issue·Plan
4. 실제 파일과 실행 결과
5. Base 또는 외부 Skill·모델

플러그인 미설치나 실행 실패는 작업을 완료한 것으로 간주할 수 없지만, 동등한 일반 절차로 진행할 수 있다.

## 2. 채택 전 확인

- 실제 trigger와 맞는가?
- 기존 통합 Skill의 mode로 처리할 수 있는가?
- 독립된 입력·산출물·Quality Bar·검증 경로가 있는가?
- 기존 Base·프로젝트 규칙과 중복되거나 충돌하는가?
- 추가 파일 쓰기·네트워크·API 키·브라우저 데이터 권한이 필요한가?
- 실패 시 복구와 독립 검증이 가능한가?

새 Skill은 기존 Skill의 mode로 표현할 수 없고, 반복 빈도와 별도 검증 경계가 있을 때만 만든다.

## 3. 최소 라우팅

기본값은 통합 Foundation Skill 1개와 필요한 전문 Skill 1개 이하이다. 발행·검증·Handoff는 해당 단계에서만 실행한다.

| 작업 신호 | 우선 Skill·mode |
|---|---|
| 새 요청·모호성·작업 계약 | `managing-project-intake-and-work-contract` |
| 신규 프로젝트 설치 | `managing-game-project-operating-system: install` |
| 기존 프로젝트 구조 변경 | `managing-game-project-operating-system: audit → migrate → verify` |
| 기획 책임 원본·발행 | `managing-design-documents` |
| 프로젝트 Skill 통합·학습 | `evolving-project-discipline-skills` |
| 현재 상태·Handoff | `maintaining-project-context-and-handoff` |
| 핵심 컨셉·뾰족한 재미·SWOT·PoC | `analyzing-and-refining-game-concepts` |
| 프로젝트 교훈·BCP | `managing-base-change-proposals` |
| Vertical Slice | `designing-vertical-slices` |
| 대량 외부 AI 작업 | `orchestrating-deepseek-worktrees` |
| 변경·외부 AI 결과 통합 검증 | `reviewing-and-validating-project-changes` |
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
- `references/`: 이유·배경·상세 Schema·판단 모델
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

기획 분석 Skill은 특히 다음을 확인한다.

- 기능 목록과 핵심 컨셉을 구분하는가?
- SWOT을 SO·WO·ST·WT 행동으로 변환하는가?
- MDA·DDE·3C·루프 같은 분석축이 개선 결정으로 연결되는가?
- `DDD`처럼 다의적인 약어를 프로젝트 정의 없이 임의 해석하지 않는가?
- PoC가 가장 위험한 가설을 검증하는 최소 범위인가?

변경 검증 Skill은 변경 주체와 무관하게 계약 대조, 정적 검사, 가능한 런타임, 대표·경계·반례·회귀, 미실행과 롤백을 연결해야 한다.

## 7. 외부 AI·worktree

- main과 사용자의 활성 worktree를 직접 수정하게 하지 않는다.
- 저장소 전체 대신 Documentation Map·Active Context·allowlist를 제공한다.
- 결과는 구조화된 초안과 미확인 목록으로 회수한다.
- 실제 diff·참조·테스트를 `reviewing-and-validating-project-changes: external-source-review`로 독립 검수한다.
- 보안·저장·호환성·테스트는 토큰 절약 대상이 아니다.

## 8. 아트·UI Skill 경계

- 생성·편집 전 계약과 프롬프트: `designing-art-prompts-and-technique-cards`
- 구현된 화면의 구조·간격·타이포·상태 감사: `auditing-and-refining-ui-art`

두 책임은 합치지 않는다. 한 번 성공한 프롬프트는 먼저 관찰·가설·패턴 상태의 기술 카드나 Case로 기록한다.

## 9. 학습과 통합

실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출만 Learning Log에 기록한다.

Skill 통합 전에는 고유 입력·산출물·실패 조건·검증·Learning Log·Registry 참조를 대조한다. 이전 버전은 Git 이력으로 보존하고, 과거 ID는 `LEGACY_SKILL_ALIASES.md`로 연결한다.
