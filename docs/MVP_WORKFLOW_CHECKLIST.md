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
- [ ] 정본·경로·ID·Schema 변경과 영향 소비자 후보를 확인했다.

## 4. 핵심 컨셉·기획 방향·PoC

`analyzing-and-refining-game-concepts`가 필요한 작업인지 확인한다.

- [ ] 한 문장 핵심 컨셉에 대상 플레이어·핵심 행동·감정·차별화가 있다.
- [ ] 플레이·제작·기술·콘텐츠·시장 제약을 확인했다.
- [ ] 뾰족한 재미가 홍보 문구가 아니라 반복 행동·선택·피드백·다음 동기다.
- [ ] GDD·레벨·등장인물·캐릭터 스타일·스테이지·세계관을 핵심 컨셉에 정렬했다.
- [ ] 요소를 `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN`으로 판정했다.
- [ ] SWOT을 SO·WO·ST·WT 실행 방향으로 변환했다.
- [ ] MDA·DDE·DDD·3C·루프·동기·차별화·제작성을 필요한 만큼 분석했다.
- [ ] Base 내부 DDD를 `Digital Dopamine Design`으로 적용했다.
- [ ] 첫 의미 있는 보상까지의 시간과 행동 → 피드백 지연을 관찰했다.
- [ ] 보상 원인·결과의 명료성과 짧은 구간의 의미 있는 보상 밀도를 확인했다.
- [ ] Micro → Session → Meta 보상 사다리와 다음 행동 의도를 확인했다.
- [ ] 반복 피로·무감각·보상 인플레이션을 확인했다.
- [ ] DDD가 의미 있는 선택을 이펙트·팝업·숫자·알림·손실 압박으로 대체하지 않는다.
- [ ] 외부 자료의 동명 DDD는 출처 정의를 확인하기 전 임의 해석하지 않았다.
- [ ] PoC가 가장 위험한 가설을 검증하는 최소 범위다.
- [ ] PoC 성공·실패·중단 기준과 다음 결정이 있다.
- [ ] 결과에 따라 `KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST`를 판정했다.
- [ ] Production·Vertical Slice 진입 또는 PoC 반복·보류·중단을 결정했다.

## 5. 기존 프로젝트 구조 변경

`managing-game-project-operating-system`을 사용한다.

- [ ] 첫 단계는 `audit`이며 읽기 전용이다.
- [ ] 승인 결정·세계관·수치·구현·자산·실패·보류를 보존 대상으로 등록했다.
- [ ] 고유 정보·중복·충돌·참조·위험을 기록했다.
- [ ] 사용자 승인 전 대량 삭제·이동·통합을 하지 않았다.
- [ ] `migrate`는 승인된 처리표 항목만 수행한다.
- [ ] 변경 전후 보존·참조·발행을 대조했다.
- [ ] 이전 경로·ID와 변경 전파 누락을 `auditing-canonical-reference-freshness`로 확인했다.
- [ ] 종료 전에 `verify`를 실행했다.

## 6. Implementation

- [ ] 승인 범위에 직접 관련된 파일만 변경했다.
- [ ] 가장 작은 검증 가능한 변경을 사용했다.
- [ ] 기능 추가와 대규모 리팩터링을 분리했다.
- [ ] 저장 형식·공개 인터페이스·사용자 흐름·승인 자산을 보호했다.
- [ ] 보류 항목을 별도 승인 없이 구현하지 않았다.
- [ ] 범위 밖 개선은 별도 제안으로 분리했다.
- [ ] 파일·경로·ID·Schema·정본·생성기 변경 시 예상 소비자와 파생본을 기록했다.

## 7. Verification

`reviewing-and-validating-project-changes`를 사용한다.

- [ ] 승인 작업 계약과 실제 diff를 대조했다.
- [ ] 정본·경로·ID·Schema·정책·생성기 변경 시 `reference-freshness`를 실행했다.
- [ ] 활성 파일의 오래된 경로·ID·명령을 확인했다.
- [ ] 변경됐어야 하지만 untouched인 소비자·템플릿·테스트·Workflow를 판정했다.
- [ ] 중복 현행 정본과 정책·상태 content drift를 확인했다.
- [ ] PDF·Manifest·해시·렌더 등 파생본 최신성을 확인했다.
- [ ] 허용된 Legacy·Change Log·과거 case와 실행 stale reference를 구분했다.
- [ ] 포맷·문법·타입·정적 검사
- [ ] 관련 자동 테스트
- [ ] 핵심 정상 경로
- [ ] 실패·취소·중복 입력·누락 데이터·원래 실패 반례
- [ ] 저장·불러오기·호환성
- [ ] 실제 화면·플레이·오디오·성능·접근성
- [ ] 인접 기존 기능 회귀
- [ ] 외부 AI 결과가 있으면 `external-source-review`
- [ ] 실행하지 못한 검증은 `UNVERIFIED`와 이유로 기록
- [ ] 판정·증거·남은 위험·롤백을 연결했다.

## 8. 기획 책임 원본·발행

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

## 9. Skill·Learning

- [ ] 기존 통합 Skill의 mode로 처리할 수 있는지 먼저 확인했다.
- [ ] 독립 입력·산출물·Quality Bar·검증이 있을 때만 새 Skill을 만들었다.
- [ ] 활성 Skill은 `load_by_default=false`다.
- [ ] Registry 경로·trigger·비사용 조건이 유효하다.
- [ ] 실패·중요 결정·재사용 가능한 교훈·실제 검증 결과를 Learning Log에 기록했다.
- [ ] 이전 ID가 있으면 `LEGACY_SKILL_ALIASES.md`에 연결했다.
- [ ] 통합·이름 변경·경로 이동 뒤 정본·참조 최신성과 untouched 소비자를 감사했다.

## 10. Documentation·Context

- [ ] 관련 책임 원본·Registry·Roadmap·Decision·Changelog를 갱신했다.
- [ ] Active Context가 실제 상태와 일치한다.
- [ ] 별도 Handoff를 두 번째 활성 상태 원본으로 만들지 않았다.
- [ ] 다음 작업·선행 조건·위험·롤백·읽기 순서가 있다.

## 11. GitHub Governance

- [ ] Documentation Governance 검사
- [ ] Skill Routing Governance 검사
- [ ] Design Publication Governance 검사
- [ ] Canonical Reference Freshness 검사
- [ ] 정상·실패 회귀 테스트
- [ ] 필요한 실제 DOCX/PDF 생성·렌더 테스트
- [ ] GitHub Actions 실제 실행
- [ ] Required Status Check·CODEOWNERS·브랜치 보호 실제 활성 상태 확인

## 12. Integration·Completion

- [ ] Acceptance Criteria가 증거와 함께 판정됐다.
- [ ] 실제 변경·검증·미검증·사용자 확인 대기를 분리했다.
- [ ] 제거·이동 파일의 잔여 참조가 없다.
- [ ] 변경됐어야 하지만 갱신되지 않은 활성 소비자가 없다.
- [ ] 다음 작업·선행 조건·Active Context가 있다.
- [ ] 새 AI가 저장소만으로 방향·상태·책임 원본·Skill·검증을 찾는다.
- [ ] 공용화 가치가 있으면 `managing-base-change-proposals`로 제안했다.
- [ ] 제안 PR과 승인된 구현 PR을 분리했다.
