# 작업 시작·개발 게이트·종료 체크리스트

실제 게임 프로젝트 작업에서 사용하는 공용 체크리스트다. 존재하지 않는 자동화·테스트·PDF·브랜치 보호를 실행한 것처럼 표시하지 않는다.

관련 스킬:

- 새 요청 라우팅: `skills/routing-project-work-by-discipline/SKILL.md`
- 신규 운영체계: `skills/installing-game-project-operating-system/SKILL.md`
- 기존 프로젝트 재배치: `skills/migrating-existing-game-project-structure/SKILL.md`
- 분야 스킬: `skills/evolving-project-discipline-skills/SKILL.md`
- Active Context·Handoff: `skills/maintaining-project-context-and-handoff/SKILL.md`
- 분야 PDF: `skills/publishing-discipline-bibles/SKILL.md`
- 운영체계 Health Review: `skills/verifying-game-project-operating-system/SKILL.md`

## 1. 작업 수준·프로젝트 모드

| 수준 | 예시 | 기본 경로 |
|---|---|---|
| L0 | 오탈자·명확한 형식 | 대상 확인→수정→최소 검증 |
| L1 | 단일 데이터·작은 UI | 영향도·Ready→수정→검증 |
| L2 | 시스템 선택·여러 파일 | 기획·Plan·승인→구현 |
| L3 | 핵심 구조·대형 마이그레이션 | 감사→계획→승인→단계 실행 |
| L4 | 공용화 가능한 방법 | 프로젝트 검증→Base 환류 판단 |

프로젝트 모드:

- [ ] 일반 운영 작업
- [ ] 신규 운영체계 설치
- [ ] 기존 프로젝트 Audit only
- [ ] 승인된 마이그레이션
- [ ] Enforcement 설치·검증

## 2. Intake·Context Gate

- [ ] 최신 사용자 지시를 확인했다.
- [ ] Base URL 요청이면 Base START_HERE·Documentation Map·Skill Registry를 확인했다.
- [ ] 프로젝트 `AGENTS.md`를 확인했다.
- [ ] 활성 `[기획서]`가 저장소 루트에서 명확히 보이는지 확인했다.
- [ ] 중첩 `docs/[기획서]`, `src/[기획서]` 같은 현행 복제본이 없는지 확인했다.
- [ ] 루트 `[기획서]/00_프로젝트_허브/START_HERE.md`, Active Context·Handoff를 확인했다.
- [ ] 프로젝트 Documentation Map과 Development Gates를 확인했다.
- [ ] 관련 분야 본책을 확인했다.
- [ ] 프로젝트 Skill Registry와 Project Skill Map을 확인했다.
- [ ] Roadmap·Issue·Goal·Plan·PR을 확인했다.
- [ ] 실제 코드·데이터·자산·테스트·최근 diff를 확인했다.
- [ ] `[백업]`, `[보류]`, `[제거 후보]`는 기본 읽기에서 제외했다.
- [ ] 해결할 문제와 사용자·플레이어 가치를 한 문장으로 설명할 수 있다.

## 3. 분야·스킬 라우팅

```yaml
primary_discipline:
affected_disciplines:
change_type:
foundation_skills:
discipline_skills:
deferred_skills:
routing_reason:
```

- [ ] 주 책임 분야를 하나 지정했다.
- [ ] 영향 분야를 빠짐없이 지정했다.
- [ ] Registry의 trigger·사용·비사용 조건을 확인했다.
- [ ] 전체 skills 폴더를 기본 로드하지 않았다.
- [ ] 주 책임 분야 스킬은 최대 하나다.
- [ ] Foundation 스킬은 필요한 최소 개수다.
- [ ] 검증·PDF·Handoff 스킬은 해당 단계에서만 호출한다.
- [ ] 보류·백업·제거 후보 스킬을 호출하지 않았다.
- [ ] 호출하지 않은 후속 스킬과 호출 조건을 기록했다.

## 4. 영향도 분석

```yaml
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
asset_impact:
data_impact:
pdf_impact:
skill_registry_impact:
learning_log_impact:
lifecycle_impact:
acceptance_criteria:
validation:
```

- [ ] `DOCUMENT_UPDATE_MATRIX.md`에서 필수 갱신 대상을 확인했다.
- [ ] 보호할 승인 결정·동작·데이터·자산·경로를 적었다.
- [ ] 이미지·사운드·PDF·스킬·수명주기 영향을 판정했다.
- [ ] 스킬 변경 시 Registry·Map·Learning Log 동기화 계획이 있다.

## 5. 기존 프로젝트 안전 마이그레이션

운영 중인 프로젝트 구조를 바꾸는 경우:

- [ ] 첫 단계는 Audit only다.
- [ ] 승인 결정, 세계관·수치·용어, 구현 상태, 승인 자산, 테스트·실패, Roadmap·Issue·Plan, 보류·미검증을 보존 대상으로 등록했다.
- [ ] 문서·코드·설정·테스트·Issue·PR·스킬·Registry·PDF·자동화 참조를 조사했다.
- [ ] 파일별 현재 역할·고유 내용·중복·상태·위험을 기록했다.
- [ ] 루트 `[기획서]`로 이동할 필요와 참조 위험을 조사했다.
- [ ] 중복·충돌·누락과 변경 전후 구조를 제안했다.
- [ ] 사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않았다.
- [ ] 변경 전후 보존 대조표를 작성했다.
- [ ] 제거 후보는 고유 정보·참조·복구·사용자 승인 조건을 확인했다.

## 6. Definition of Ready

- [ ] 프로젝트 방향과 핵심 경험에 기여하는 방식이 명확하다.
- [ ] 포함·제외 범위가 분리돼 있다.
- [ ] 선행 결정·의존성과 보류 재개 조건이 해결됐다.
- [ ] 책임 원본·영향 분야·실제 대상 파일이 확인됐다.
- [ ] 기존 데이터·인터페이스·사용자 흐름·승인 자산 보호 범위가 있다.
- [ ] 저장·호환성·이관 위험이 있다.
- [ ] 완료 기준이 `조건 → 행동 → 관찰 결과`다.
- [ ] 정상·예외·회귀·사용자 검수 방법이 있다.
- [ ] 관련 Base 스킬과 프로젝트 스킬이 Registry에 연결됐다.

준비되지 않은 작업은 구현자에게 넘기지 않고 조사·기획·결정으로 분리한다.

## 7. Planning·Approval Gate

- [ ] Plan이 실제 저장소 조사 결과를 포함한다.
- [ ] 변경 파일·보호 파일·상태 소유자가 명확하다.
- [ ] 이미지·UI·사운드·데이터·저장 영향이 있다.
- [ ] 실패·취소·폴백·롤백이 있다.
- [ ] Acceptance Criteria와 검증 순서가 있다.
- [ ] 본책·게이트·Registry·스킬·Learning Log·Manifest·PDF 갱신 계획이 있다.
- [ ] L2 이상 또는 대형 마이그레이션은 사용자 구현 승인을 받았다.

## 8. 본책·Roadmap·게이트

- [ ] 분야 본책만으로 목적·가치·Quality Bar·금지 방향·현재 상태를 이해할 수 있다.
- [ ] 분야의 전체 작업 과정이 입력→판단→산출물→검증→다음 게이트로 연결된다.
- [ ] 질문별 현행 책임 원본이 하나다.
- [ ] 승인·구현·검증·미확정·보류·불일치를 구분했다.
- [ ] Roadmap과 Development Gates에 현재 단계·다음 Greenlight·증거가 있다.
- [ ] 작업 완료와 Vertical Slice·Alpha·Beta 통과를 혼동하지 않았다.
- [ ] Issue·Goal·Plan이 본책·Roadmap의 현재 범위와 일치한다.

## 9. 분야별·Foundation 스킬과 항상 학습

- [ ] 공용 절차는 Foundation 스킬에 한 번만 있다.
- [ ] 주 책임 분야에 Registry 진입 스킬이 있다.
- [ ] 스킬이 분야 본책·실제 경로·산출물·검증을 연결한다.
- [ ] 사용·비사용 조건, trigger tags, Ready·Done, 실패 조건이 있다.
- [ ] 활성 스킬은 `load_by_default=false`다.
- [ ] 모든 의미 있는 호출 후 Learning Log에 결과·실패·예외·사용자 피드백을 기록했다.
- [ ] 불필요하게 호출한 스킬과 누락된 스킬·검증을 기록했다.
- [ ] 스킬 변경 필요 여부를 판정했다.
- [ ] 변경하지 않으면 그 이유를 기록했다.
- [ ] 지식 상태를 관찰·가설·패턴·검증·승격 후보로 구분했다.
- [ ] 한 번 성공한 방법을 공용 강제 규칙으로 과장하지 않았다.
- [ ] 스킬 변경 시 Registry·Map·Log가 함께 갱신됐다.

## 10. 이미지·자산·사운드

- [ ] Visual Source와 Asset Manifest를 확인했다.
- [ ] 기존 승인 이미지가 있는 항목에 별도 지시 없이 새 시안을 만들지 않았다.
- [ ] 이미지의 채택·비채택 요소를 기록했다.
- [ ] 항목별 캐노니컬 경로가 하나다.
- [ ] REFERENCE·DIRECTION_APPROVED·PRODUCTION_READY·IMPLEMENTED·VISUALLY_VALIDATED를 구분했다.
- [ ] `MIGRATION_PENDING`과 실제 파일 저장 완료를 구분했다.
- [ ] Visual DNA, Import, 피벗, 해상도·프레임·성능 예산을 확인했다.
- [ ] 콘셉트·실제 캡처·골든 스크린샷을 구분했다.
- [ ] 오디오 제작·이벤트 연결·믹싱·검증 상태를 구분했다.

## 11. 분야별 PDF

- [ ] PDF가 요약이 아니라 분야 목적부터 전체 작업 과정·현재 상태·다음 작업까지 포함한다.
- [ ] 관련 개발 게이트와 프로젝트 스킬을 포함한다.
- [ ] 승인 이미지·실제 캡처와 상태·Asset ID·채택 범위 캡션이 있다.
- [ ] 책임 Markdown과 수치·용어·상태가 일치한다.
- [ ] PDF를 독립 원본으로 수동 수정하지 않았다.
- [ ] 재현 가능한 생성 명령이 있다.
- [ ] Publication Manifest에 입력·출력·해시·생성기·시각 검수를 기록했다.
- [ ] PDF 헤더·목차·링크·표·이미지·한글 렌더링을 확인했다.
- [ ] 미설치·오래됨·실패를 `NOT_BUILT/STALE/FAILED`로 정확히 표시했다.

## 12. Implementation Gate

- [ ] 요청과 승인 Plan에 직접 관련된 파일만 변경했다.
- [ ] 가장 작은 검증 가능한 변경을 사용했다.
- [ ] 기능 추가와 대규모 리팩터링을 분리했다.
- [ ] 기존 호출·데이터·저장·UI 흐름을 확인했다.
- [ ] 공개 인터페이스·저장 형식·사용자 흐름을 승인 없이 변경하지 않았다.
- [ ] 보류 항목을 별도 승인 없이 구현하지 않았다.
- [ ] 범위 밖 개선은 별도 제안으로 분리했다.

## 13. 파일·수명주기 변경

- [ ] 생성·수정·삭제·이동·이름 변경 이유가 명확하다.
- [ ] Markdown·README·Map·AGENTS·코드·Issue·PR·Registry·스킬·PDF 참조를 확인했다.
- [ ] `v2`·`final`·`latest`·날짜별 활성 복제본을 만들지 않았다.
- [ ] 단순 이전 버전은 Git 이력으로 보존했다.
- [ ] `[백업]`은 Git 이력만으로 부족한 보존 사유가 있다.
- [ ] `[보류]`에 이유·재개 조건·책임 원본·선행 작업이 있다.
- [ ] `[제거 후보]`는 검증·승인 전 삭제하지 않았다.
- [ ] 변경 전후 고유 정보와 참조를 대조했다.

## 14. Verification Gate

- [ ] 포맷·문법·타입·정적 검사
- [ ] 관련 자동 테스트
- [ ] 핵심 정상 경로
- [ ] 실패·취소·중복 입력·누락 데이터
- [ ] 저장·불러오기·호환성
- [ ] 실제 화면·플레이·오디오·성능·접근성
- [ ] diff가 승인 범위 안인지 확인
- [ ] 사용자 수동 검수 순서
- [ ] 실행하지 못한 검증을 `[미검증]`으로 표시

## 15. Documentation Gate

- [ ] 관련 분야 본책
- [ ] Roadmap·Development Gates
- [ ] Documentation Map·Active Context·Handoff
- [ ] Decision Log·Changelog
- [ ] Project Skill Map·Skill Registry·분야 스킬·Learning Log
- [ ] Visual Source·Asset Manifest
- [ ] 테스트·QA·통합검수
- [ ] PDF·Publication Manifest
- [ ] README·Issue·Goal·Plan
- [ ] Base version·후속 동기화

## 16. GitHub·자동 검사

- [ ] Documentation Governance Checker의 정상·실패 회귀 테스트가 있다.
- [ ] Skill Routing Governance Checker의 정상·실패 회귀 테스트가 있다.
- [ ] 루트 `[기획서]`와 중첩 복제본을 검사한다.
- [ ] Registry JSON·중복 ID·활성 경로·trigger·Learning Log를 검사한다.
- [ ] 모든 11개 책임 분야의 진입 스킬을 검사한다.
- [ ] 전체 스킬 자동 로드 금지를 검사한다.
- [ ] 스킬 변경 시 Registry·Map·Log 동기화를 검사한다.
- [ ] PDF 입력 hash·header·visual review를 검사한다.
- [ ] Workflow가 실제로 성공했다.
- [ ] Required Status Check·CODEOWNERS·브랜치 보호 실제 상태를 구분했다.

## 17. Integration·Completion Gate

- [ ] Acceptance Criteria를 증거로 판정했다.
- [ ] 구현·검증·사용자 확인 상태를 분리했다.
- [ ] 본책·게이트·Registry·스킬·Learning Log·Manifest·PDF가 최신이다.
- [ ] 미검증·불일치·위험을 분리했다.
- [ ] 이동·제거 잔여 참조가 없다.
- [ ] PR Required Checks·리뷰를 통과했다.
- [ ] 다음 작업·선행 조건·Handoff가 있다.
- [ ] 프로젝트 전용 교훈과 Base 환류 후보를 분리했다.

## 18. 콜드 스타트·Health Review

- [ ] 새 작업자가 루트 `[기획서]`를 찾는다.
- [ ] 프로젝트 방향·현재 상태·다음 작업·보호 범위를 찾는다.
- [ ] 분야 본책·Registry 진입 스킬·최소 호출 스킬을 찾는다.
- [ ] 실제 코드·데이터·자산·테스트·PDF를 찾는다.
- [ ] 보류·미검증·위험을 찾는다.
- [ ] 작업 종료 갱신·Learning Log 경로를 찾는다.
- [ ] 설치·마이그레이션·큰 구조 변경·주요 게이트 후 Health Review를 수행했다.
- [ ] Health Review 결과를 `PASS/PARTIAL/FAIL/NOT_RUN`과 증거로 기록했다.

## 19. Base 학습 환류

- [ ] 프로젝트 고유 내용과 공용 원리를 분리했다.
- [ ] 반복 검증된 판단·절차·템플릿·실패 방지·회귀 테스트만 Base 후보로 삼았다.
- [ ] 기존 Base Method·Skill·Template·Case·Test와 중복을 확인했다.
- [ ] 한 번의 성공을 관찰·가설로 남기고 검증으로 과장하지 않았다.
- [ ] Base Changelog·Documentation Map·Skill Registry·Learning Log를 갱신했다.
- [ ] 프로젝트 `BASE_RULES_VERSION.md` 후속 동기화를 기록했다.

공용화할 내용이 없으면 `공용 학습 데이터 없음 — 프로젝트 전용 또는 단발성 작업`으로 보고한다.
