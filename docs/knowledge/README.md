# 공용 기획 지식 베이스

이 폴더는 여러 프로젝트에서 재사용할 수 있는 **기획·아트 디자인·서사·연출·정보 수집·검수 방법과 실제 적용 사례**를 누적하는 공용 학습 데이터다.

Base의 작업 규칙은 “어떻게 협업할 것인가”를 정의한다. 이 지식 베이스는 “좋은 결과물을 만들기 위해 무엇을 관찰하고, 어떤 순서로 판단하며, 무엇을 검증할 것인가”를 정의한다.

## 1. 폴더 구분

```text
docs/knowledge/
├─ methods/   반복 가능한 설계·제작 판단 방법
├─ research/  정보 수집·벤치마킹·근거 평가 방법
├─ skills/    작업 유형별 입력·산출물·검수 능력 계약
└─ cases/     프로젝트·벤치마킹에서 추출한 사례 연구
```

- **methods:** 특정 프로젝트 이름 없이 재사용 가능한 설계 순서와 판단 기준.
- **research:** 어떤 자료를 찾고 신뢰도를 어떻게 평가하며 적용 결론을 어떻게 남길지 정의.
- **skills:** AI나 작업자가 특정 작업을 잘 수행하기 위해 필요한 입력, 과정, 결과물, 실패 기준.
- **cases:** 실제 프로젝트나 벤치마킹에서 어떤 문제를 어떤 이유로 해결했는지 기록한 학습 사례.

## 2. 책임 경계

Base에 둔다:

- 여러 프로젝트에서 재사용 가능한 방법.
- 실제 작업에서 검증된 체크리스트.
- 권리와 출처를 명확히 한 벤치마킹 관찰.
- 프로젝트 사례에서 추출한 일반 원칙과 실패 방지 교훈.
- 새 프로젝트가 복사해 사용할 수 있는 템플릿.

프로젝트 저장소에 둔다:

- 현재 프로젝트의 세계관·캐릭터·밸런스 수치.
- 활성 로드맵, 구현 상태, 정확한 엔진 버전과 파일 경로.
- 프로젝트 전용 아트 팔레트·스프라이트·사운드.
- 현재 Issue, Work Order와 승인된 구현 제안서.
- 비공개 원문이나 외부 공개가 허용되지 않은 자료.

사례 문서는 프로젝트 이름을 표시할 수 있지만 활성 기획서 전체를 복제하지 않는다. 사례에는 문제, 판단, 결과, 재사용 가능한 교훈만 남긴다.

## 3. 지식 상태

| 상태 | 의미 |
|---|---|
| `관찰` | 사례에서 발견했지만 아직 채택하지 않음 |
| `가설` | 적용 가치가 있어 PoC 또는 테스트가 필요함 |
| `채택` | 프로젝트에서 사용하기로 결정함 |
| `검증` | 실제 작업이나 플레이테스트에서 효과를 확인함 |
| `제외` | 현재 목적·비용·권리·기술 조건에 맞지 않아 사용하지 않음 |
| `폐기` | 이전에는 사용했지만 더 나은 기준으로 대체됨 |

검증되지 않은 관찰을 보편적 사실처럼 작성하지 않는다.

## 4. 공용 방법 라우팅

| 작업 | 먼저 읽을 문서 |
|---|---|
| 전체 기획 체계·상태·책임 원본 | `methods/PLANNING_SYSTEM_METHOD.md` |
| 프로젝트 인수인계·문서 구조 | `methods/PROJECT_HANDOFF_CONTEXT_METHOD.md` |
| 새 Codex 채팅·Plan Mode 작업 패키지 | `methods/CODEX_PLAN_MODE_WORK_PACKAGE_METHOD.md` |
| 장면·대사·선택·관계 | `methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` |
| 전장·유닛·구조물 아트 | `methods/ART_DIRECTION_METHOD.md` |
| 캐릭터·초상·서사형 아트 | `methods/CHARACTER_AND_NARRATIVE_ART_METHOD.md` |
| 전투 애니메이션·판정 연출 | `methods/ANIMATION_AND_PRESENTATION_METHOD.md` |
| 대화 UI·표정·컷인·이벤트 연출 | `methods/DIALOGUE_AND_EVENT_PRESENTATION_METHOD.md` |
| 조사·벤치마킹·근거 평가 | `research/DESIGN_RESEARCH_AND_EVIDENCE_METHOD.md` |
| 기획·조사·인수 실무 능력 | `skills/PLANNING_RESEARCH_HANDOFF_SKILL_MATRIX.md` |
| 기존 아트·애니메이션·인수 검수 | `skills/`의 분야별 매트릭스 |
| 실제 적용과 실패 사례 | `cases/README.md` |

## 5. 프로젝트에서 Base로 승격하는 흐름

```text
프로젝트 문제 발생
→ 프로젝트 전용 해결안 적용
→ 결과·실패·검증 기록
→ 공용성 판단
→ cases에 사례 추가
→ 여러 사례에서 반복 확인
→ methods 또는 skills로 승격
```

한 프로젝트에서 한 번 사용한 규칙은 우선 사례로 남긴다. 두 개 이상의 다른 맥락에서 같은 원리가 유효하거나, 강한 이론적 근거와 검증이 있을 때 공용 방법으로 승격한다.

## 6. 사례 문서 필수 항목

- 사례명과 출처.
- 해결하려던 문제.
- 당시 제약과 맥락.
- 관찰한 근거.
- 검토한 대안.
- 채택한 결정과 이유.
- 결과 또는 아직 검증하지 못한 항목.
- 다른 프로젝트에 재사용할 수 있는 원칙.
- 그대로 복사하면 안 되는 프로젝트 특화 요소.
- 검증 방법과 후속 질문.

새 사례는 `templates/KNOWLEDGE_CASE_STUDY.md`를 사용한다.

## 7. 전문 템플릿

| 템플릿 | 역할 |
|---|---|
| `templates/planning/PROJECT_DIRECTION_BRIEF.md` | 프로젝트 약속·핵심 경험·불변 조건 |
| `templates/planning/NARRATIVE_CONTENT_PLAN.md` | 장면·대사·선택·관계·데이터 경계 |
| `templates/planning/ART_DIRECTION_BRIEF.md` | 시각 약속·스타일 축·자산 티어·QA |
| `templates/planning/PRESENTATION_PLAN.md` | 시선 흐름·표정·컷인·접근성 |
| `templates/planning/HANDOFF_CONTEXT.md` | 현재 상태·책임 원본·다음 작업 |
| `templates/planning/CODEX_PLAN_MODE_WORK_ORDER.md` | 새 Codex 채팅의 읽기 순서·불변 조건·검토 범위·산출물·승인 게이트 |
| `templates/KNOWLEDGE_CASE_STUDY.md` | 공용 사례 기록 |

## 8. Codex 작업 문서 구분

```text
프로젝트 Work Order
→ Codex Plan Mode 제안서
→ 사용자 승인
→ 구현 결과와 PR
```

- Work Order는 Codex에 주는 입력이다.
- Plan Mode 제안서는 Codex가 실제 저장소를 조사해 만드는 출력이다.
- 구현은 사용자 승인 뒤 별도 실행이다.
- 사전 기술 추천은 Plan Mode 제안서가 아니며 검증 대상임을 표시한다.

## 9. 품질 원칙

- 추상적인 조언보다 입력, 출력, 검증 기준을 남긴다.
- “멋있게”, “재미있게”, “깔끔하게”처럼 측정할 수 없는 표현만으로 끝내지 않는다.
- 사례의 표면을 복제하지 않고 문제 해결 원리를 분리한다.
- 저작권이 있는 코드·아트·문구·UI를 그대로 저장하지 않는다.
- 외부 사실과 도구 정보는 변할 수 있으므로 출처와 확인 날짜를 남긴다.
- 같은 규칙을 여러 파일에 장문으로 복제하지 않고 책임 문서로 연결한다.
- 오래된 내용은 Git 이력으로 보존하고 활성 문서는 최신 기준만 유지한다.
