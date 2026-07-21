# 작업 시작·개발 게이트·종료 체크리스트

이 체크리스트는 `docs/OPERATING_MODEL.md`와 `DEVELOPMENT_GATES_METHOD.md`의 파생본이다. 상세 실행 절차를 반복하지 않는다.

## 1. Intake·Context

- [ ] 최신 사용자 지시와 프로젝트 `AGENTS.md`를 확인했다.
- [ ] START_HERE·Active Context·Documentation Map·Development Gates를 확인했다.
- [ ] Design Document Registry와 현재 책임 원본을 확인했다.
- [ ] Skill Registry에서 trigger가 일치하는 최소 Skill만 선택했다.
- [ ] 실제 코드·데이터·자산·테스트·최근 diff를 확인했다.
- [ ] 백업·보류·제거 후보를 기본 읽기에서 제외했다.

## 2. 요청 라우팅·작업 계약

`managing-project-intake-and-work-contract`로 다음을 한 번만 판정한다.

```yaml
work_level:
change_types:
primary_discipline:
affected_disciplines:
foundation_skills:
discipline_skills:
deferred_skills:
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
acceptance_criteria:
validation:
```

- [ ] 저장소에서 확인할 사실을 사용자에게 다시 묻지 않았다.
- [ ] 결과를 바꾸는 사용자 결정만 확인했다.
- [ ] 필요한 사용자 확인 전 실행 계약이나 구현으로 이동하지 않았다.

## 3. Definition of Ready

- [ ] 문제·목적·사용자 경험이 명확하다.
- [ ] 포함·제외·보호 범위가 있다.
- [ ] 선행 조건·의존성·보류 재개 조건이 해결됐거나 표시됐다.
- [ ] 실제 대상 파일·상태 소유자·호환성 위험이 확인됐다.
- [ ] 완료 기준이 `조건 → 행동 → 관찰 결과`다.
- [ ] 정상·실패·경계·회귀·사용자 검수 방법이 있다.

## 4. 기존 프로젝트 구조 변경

`managing-game-project-operating-system`을 사용한다.

- [ ] 첫 단계는 `audit`이며 읽기 전용이다.
- [ ] 승인 결정·세계관·수치·구현·자산·실패·보류를 보존 대상으로 등록했다.
- [ ] 고유 정보·중복·충돌·참조·위험을 기록했다.
- [ ] 사용자 승인 전 대량 삭제·이동·통합을 하지 않았다.
- [ ] `migrate`는 승인된 처리표 항목만 수행한다.
- [ ] 변경 전후 보존·참조·발행을 대조했다.
- [ ] 종료 전에 `verify`를 실행했다.

## 5. Implementation

- [ ] 승인 범위에 직접 관련된 파일만 변경했다.
- [ ] 가장 작은 검증 가능한 변경을 사용했다.
- [ ] 기능 추가와 대규모 리팩터링을 분리했다.
- [ ] 저장 형식·공개 인터페이스·사용자 흐름·승인 자산을 보호했다.
- [ ] 보류 항목을 별도 승인 없이 구현하지 않았다.
- [ ] 범위 밖 개선은 별도 제안으로 분리했다.

## 6. Verification

- [ ] 포맷·문법·타입·정적 검사
- [ ] 관련 자동 테스트
- [ ] 핵심 정상 경로
- [ ] 실패·취소·중복 입력·누락 데이터
- [ ] 저장·불러오기·호환성
- [ ] 실제 화면·플레이·오디오·성능·접근성
- [ ] diff와 승인 범위 대조
- [ ] 실행하지 못한 검증은 `[미검증]`

## 7. 기획 책임 원본·발행

`managing-design-documents`를 사용한다.

- [ ] 한 질문에 등록된 단일 Markdown 또는 JSON 책임 원본이 있다.
- [ ] 확정·구현·검증·미확정·보류를 분리했다.
- [ ] 실제 코드·데이터·자산·테스트 경로가 있다.
- [ ] 승인 이미지와 실제 캡처를 구분했다.
- [ ] Registry의 `publication_policy`를 확인했다.
- [ ] `source_only` 문서에 불필요한 PDF·DOCX를 강제하지 않았다.
- [ ] `milestone_sync`·`always_sync` 조건이면 PDF·Manifest를 갱신했다.
- [ ] 선언한 경우에만 DOCX·다이어그램을 생성했다.
- [ ] PDF 전 페이지 렌더와 잘림·겹침·한글을 확인했다.
- [ ] `CURRENT`와 사람 시각 검수 완료를 혼동하지 않았다.

## 8. Skill·Learning

- [ ] 기존 통합 Skill의 mode로 처리할 수 있는지 먼저 확인했다.
- [ ] 독립 입력·산출물·Quality Bar·검증이 있을 때만 새 Skill을 만들었다.
- [ ] 활성 Skill은 `load_by_default=false`다.
- [ ] Registry 경로·trigger·비사용 조건이 유효하다.
- [ ] 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과를 Learning Log에 기록했다.
- [ ] 이전 ID가 있으면 `LEGACY_SKILL_ALIASES.md`에 연결했다.

## 9. Documentation·Context

- [ ] 관련 책임 원본·Registry·Roadmap·Decision·Changelog를 갱신했다.
- [ ] Active Context가 실제 상태와 일치한다.
- [ ] 별도 Handoff를 두 번째 활성 상태 원본으로 만들지 않았다.
- [ ] 다음 작업·선행 조건·위험·롤백·읽기 순서가 있다.

## 10. GitHub Governance

- [ ] Documentation Governance 검사
- [ ] Skill Routing Governance 검사
- [ ] Design Publication Governance 검사
- [ ] 정상·실패 회귀 테스트
- [ ] 필요한 실제 DOCX/PDF 생성·렌더 테스트
- [ ] GitHub Actions 실제 실행
- [ ] Required Status Check·CODEOWNERS·브랜치 보호 실제 활성 상태 확인

## 11. Integration·Completion

- [ ] Acceptance Criteria가 증거와 함께 판정됐다.
- [ ] 실제 변경·검증·미검증·사용자 확인 대기를 분리했다.
- [ ] 제거·이동 파일의 잔여 참조가 없다.
- [ ] 다음 작업·선행 조건·Active Context가 있다.
- [ ] 새 AI가 저장소만으로 방향·상태·책임 원본·Skill·검증을 찾는다.
- [ ] 공용화 가치가 있으면 `managing-base-change-proposals`로 제안했다.
- [ ] 제안 PR과 승인된 구현 PR을 분리했다.
