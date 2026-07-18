# 분야별 프로젝트 스킬 학습·진화 방법

- 상태: 공용 Method
- 목적: 공용 절차는 Foundation에 한 번만 두고, 각 제작 분야는 독립 실행 가능한 프로젝트 스킬을 통해 반복 작업의 품질과 인수인계를 개선한다.

## 1. 핵심 원칙

스킬은 조언 모음이 아니라 다음을 고정하는 반복 실행 계약이다.

```text
사용 조건 → 비사용 조건 → 필수 입력 → JSON 책임 원본 → 절차 → 산출물 → 완료 → 검증 → 실패 → 학습
```

**항상 학습**은 스킬 본문을 매번 무조건 수정한다는 뜻이 아니다.

```text
스킬 호출
→ 결과·실패·예외·사용자 피드백 기록
→ 변경 필요성 판정
→ 근거가 있을 때만 계약 갱신
→ 반복 검증
```

모든 의미 있는 호출은 Learning Log에 남긴다. 변경 근거가 없으면 `변경 없음`과 이유를 기록한다.

## 2. 스킬 계층

### Foundation·공용

- 요청·컨텍스트 라우팅
- 영향도 분석
- 개발 게이트 판정
- Decision·추적성
- JSON 기획서·발행 Governance
- 검증·완료 선언
- Context·Handoff
- 외부 AI 결과 검수
- 프로젝트 교훈·Base 환류

공용 절차를 각 분야 스킬에 장문 복사하지 않는다.

### 분야별

| 분야 | 고유 스킬 책임 |
|---|---|
| 설정·내러티브 | 정사·용어·시나리오·캐릭터·대사 |
| 게임 디자인 | 핵심 루프·전투·경제·진행·밸런스 |
| UX·UI·접근성 | 정보 구조·화면 흐름·입력·피드백·접근성 |
| 개발·엔지니어링 | 아키텍처·상태·데이터·AI·저장·성능·빌드 |
| 테크니컬 아트·파이프라인 | 자산 규격·Import·피벗·도구·예산 |
| 아트 | 시각 언어·캐릭터·환경·UI 그래픽·VFX |
| 사운드 | BGM·SFX·음성·이벤트·믹싱 |
| QA | 자동·수동·회귀·성능·호환성 |
| 프로덕션·PM | 범위·일정·의존성·위험·마일스톤 |
| 분석·유저리서치 | 벤치마킹·플레이테스트·텔레메트리 |
| 통합검수 | JSON·구현·자산·발행·검증·게이트 일치 |

하위 스킬은 반복 빈도와 Quality Bar·검증 경로가 별도일 때만 만든다.

## 3. AI용 Registry와 사람용 Skill Map

```text
AI·자동 검사 → SKILL_REGISTRY.json
사람 기본 열람 → PROJECT_SKILL_MAP.pdf
사람 문서 검토 → PROJECT_SKILL_MAP.docx
시각 관계 → PROJECT_SKILL_MAP.assets/
최신성 → SKILL_MAP_PUBLICATION_MANIFEST.json
```

`PROJECT_SKILL_MAP.md`는 사용하지 않는다.

기본 정책:

```json
{
  "load_all_skills": false,
  "default_selection": "none",
  "require_trigger_match": true,
  "max_primary_discipline_skills": 1,
  "max_foundation_skills": 3
}
```

작업 시작 시 `routing-project-work-by-discipline`가 주 책임 분야 하나, 영향 분야, 필요한 Foundation, 분야 진입 스킬과 후속 단계 스킬을 판정한다.

금지:

- 전체 skills 폴더 기본 로드
- Trigger와 무관한 호출
- 같은 책임의 중복 스킬 동시 호출
- 보류·백업·제거 후보 호출
- 발행·검증·Handoff 스킬 조기 호출

## 4. 최소 스킬 계약

```yaml
name:
skill_id:
discipline:
purpose:
use_when:
do_not_use_when:
trigger_tags:
load_by_default: false
required_inputs:
read_first_design_document_ids:
foundation_dependencies:
project_rules:
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

- `read_first_design_document_ids`는 Design Document Registry의 JSON 본책을 가리킨다.
- `trigger_tags`와 사용·비사용 조건은 선택적 호출의 근거다.
- 활성 스킬도 `load_by_default=false`다.
- 프로젝트 고유 명칭·수치·경로·승인 자산은 프로젝트 스킬과 JSON에 둔다.

## 5. 학습 상태

| 상태 | 의미 | 사용 방식 |
|---|---|---|
| 관찰 | 한 번 발견 | 참고만 함 |
| 가설 | 적용·실패 조건 제시 | 제한적 시험 |
| 패턴 | 여러 작업에서 반복 | 프로젝트 권장 절차 |
| 검증 | 여러 조건에서 재현 | 공용 계약 후보 |
| 승격 후보 | 프로젝트 독립성과 중복 검수 완료 | Base 반영 검토 |

## 6. 실행 기록

```md
### [날짜] [skill_id]
- 작업·PR:
- 기준 커밋:
- 호출 Trigger:
- 입력 JSON·실제 범위:
- 산출물:
- 실행한 검증:
- 결과: 성공/부분 성공/실패/미검증
- 실패·예외·재현 조건:
- 사용자 피드백:
- 불필요하게 호출한 스킬:
- 누락된 스킬·검증:
- 스킬 변경 필요: 예/아니오
- 변경하지 않는 이유:
- 지식 상태:
- 프로젝트 전용 유지:
- Base 환류 후보:
- 다음 검토 Trigger:
```

실패 기록은 삭제하지 않는다. 장문 로그 대신 재현 조건·원인·수정 계약·재발 방지를 보존한다.

## 7. 사람용 Skill Map 생성

Registry 변경 후 실행한다.

```text
python tools/build_project_skill_map.py \
  --registry "[기획서]/00_프로젝트_허브/SKILL_REGISTRY.json" \
  --output-dir "[기획서]/00_프로젝트_허브" \
  --project-name "프로젝트명" \
  --source-commit <commit>
```

생성 결과:

- `PROJECT_SKILL_MAP.docx`
- `PROJECT_SKILL_MAP.pdf`
- `PROJECT_SKILL_MAP.assets/skill-flow.png`
- `PROJECT_SKILL_MAP.assets/discipline-routing.png`
- `PROJECT_SKILL_MAP.assets/skill-matrix.png`
- `SKILL_MAP_PUBLICATION_MANIFEST.json`

사람용 문서는 Registry의 독립 복제 원본이 아니라 파생본이다.

## 8. 자동·수동 검수

자동 검수:

- Registry JSON 문법·중복 ID
- 활성 스킬 경로·Trigger·비사용 조건
- `load_by_default=false`
- Learning Log·분야 진입 등록
- 보류·백업 기본 제외
- 사람용 DOCX/PDF·다이어그램·Manifest 해시
- Registry 변경 후 미재생성
- Markdown Skill Map 재생성

수동 검수:

- 실제 작업과 스킬 책임 일치
- 호출 집합의 과다 여부
- JSON 본책·실제 경로·검증 연결
- 학습 기록의 의미
- Foundation·분야 중복
- 사람용 Skill Map 가독성

## 9. 검토 Trigger와 Health Review

다음 중 하나가 발생하면 스킬을 검토한다.

- 동일 실패 반복
- 사용자 피드백과 Done 불일치
- JSON 본책·실제 경로·검증 명령 변경
- 새 예외·폴백 필요
- 여러 분야에 같은 절차 복제
- 새 작업 유형에 대응할 스킬 없음
- 새 채팅이 필요한 스킬을 찾지 못함
- 90일 이상 활성 스킬 미검토
- Registry와 DOCX/PDF 불일치

스킬 구조를 설치·통합·대규모 변경한 뒤에는 `verifying-game-project-operating-system`을 호출해 Registry, 사람용 Skill Map, Learning Log, 분야 진입점, 선택적 호출과 Governance 파이프라인이 실제로 연결됐는지 검수한다.

## 10. 통합·Base 환류

통합 전 고유 입력·출력·실패 조건·Learning Log·Registry 참조를 대조한다. 단순 이전 버전은 Git 이력으로 보존하고, 외부 감사 원본은 `[백업]`, 미래 스킬은 `[보류]`로 둔다.

프로젝트 전용 세계관·수치·경로·승인 자산은 Base에 승격하지 않는다. 반복 가능한 판단·절차·검증·회귀 테스트만 후보로 분리한다.
