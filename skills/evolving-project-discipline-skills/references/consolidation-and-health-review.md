# Skill 통합·Health Review 상세표

## 인벤토리

Skill, mode, 분야, trigger, 입력, 산출물, 검증, 고유 책임, 중복, 상태를 한 표에서 비교한다.

다음을 찾는다.

- 기존 통합 Skill mode와 중복되는 절차.
- 라우팅·조사·상태 판정의 반복.
- Method·Checklist·Skill에 복제된 실행 계약.
- 설명만 있고 입력·산출물·검증이 없는 파일.
- 등록된 책임 원본·실제 경로·trigger·비사용 조건이 없는 Skill.
- `load_by_default=true`, 전체 폴더 로드, 보류·백업·제거 후보의 기본 읽기 혼입.
- Learning Log·review trigger·사람용 발행본 최신성 누락.

## 독립 Skill 계약

새 Skill을 유지하려면 다음이 필요하다.

- Skill ID·분야·상태, 목적·사용·비사용 조건.
- `trigger_tags`, `load_by_default=false`, mode와 상태 흐름.
- 필수 입력, 먼저 읽을 책임 원본, 실제 경로와 절차.
- 관찰 가능한 산출물, Definition of Ready·Done.
- 자동·수동 검증, 실패·중단 조건, 승인 경계.
- 관련 Skill·Learning Log·review trigger·마지막 검토일·기준 커밋·지식 상태.

시점·입력·도구·승인 경계 또는 독립 자동 증거가 다르면 억지로 합치지 않는다.

## 선택적 라우팅

Registry에는 활성 Skill만 등록한다. 통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 연결한다.

```json
{
  "load_all_skills": false,
  "automatic_selection": true,
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

주 책임 분야 Skill은 최대 하나다. 발행·검증·Handoff는 해당 단계에서만 실행한다.

## 통합 전 보존

고유 입력·산출물·실패 조건·검증, 프로젝트 전용 규칙과 실제 경로, 책임 원본·Documentation Map·Issue·PR 참조, Learning Log와 지식 상태, scripts·references·templates, Registry와 사람용 발행본을 추출한다.

고유 절차는 새 Skill 또는 연결된 `references/`로 승계한다. 이전 활성 사본을 백업 파일로 복제하지 않고 Git 이력으로 보존한다.

## 적용·학습

```text
통합·수정안
→ Registry·Skill·alias 갱신
→ 문서·템플릿·검사·발행본 갱신
→ canonical reference freshness 감사
→ 대표·변형·반례 검증
→ 결과·실패·예외·사용자 피드백 기록
→ OBSERVATION → HYPOTHESIS → PATTERN → VERIFIED → PROMOTION_CANDIDATE 판정
```

한 번의 성공은 관찰 또는 가설이며 실제 반복 결과 없이 지식 상태를 승격하지 않는다.

## Health Review

- Registry 경로·trigger·do-not-use와 실제 패키지의 1:1 일치.
- 활성 Skill 수, 중복 mode, 과도한 Foundation 연쇄 호출.
- Legacy alias, 오래된 ID·경로·설명, 변경 전파 누락과 untouched 소비자.
- reference·script의 고아 파일, 깨진 링크, 생성기와 파생본 drift.
- START_HERE·Documentation Map·템플릿·테스트·사람용 Skill Map·Manifest 최신성.
- Governance checker, 정본 최신성, 대표·변형·반례 회귀 테스트와 GitHub Actions.
- 새 채팅이 전체 Skill을 읽지 않고 필요한 최소 Skill을 찾아 실행할 수 있는지.
