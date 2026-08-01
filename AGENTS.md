# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** Skill·Template·Case·Test의 원본이다. 이 파일은 모든 Base 작업에 항상 적용되는 불변 규칙만 책임진다. 요청별 탐색은 `START_HERE.md`, 전체 운영 생명주기는 `docs/OPERATING_MODEL.md`, Work Mode·Skill 선택과 병합 게이트는 `docs/WORK_MODE_AND_SKILL_ROUTING.md`, 문서 위치는 `docs/DOCUMENTATION_MAP.md`가 책임진다.

## 1. 권한과 읽기 순서

우선순위는 다음과 같다.

1. 사용자의 최신 지시
2. 대상 프로젝트 `AGENTS.md`와 보안·엔진·데이터 규칙
3. 프로젝트 Active Context와 승인된 작업 계약
4. 등록된 책임 원본과 실제 코드·데이터·자산·테스트
5. 프로젝트가 채택한 Base 계약
6. Base 원격 원본
7. 외부 사례·리뷰·과거 대화·초안·추정

- 정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다.
- 외부 벤치마크·리뷰·커뮤니티·모델 해석은 요구사항 권한이나 구현 사실의 정본이 아니다.
- 저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.
- 모든 파일과 전체 `skills/`를 기본 로드하지 않는다. `skills/SKILL_REGISTRY.json`의 trigger로 최소 Skill만 고르고, 현행 목록은 `docs/generated/BASE_ACTIVE_SKILLS.md`에서 확인한다.

## 2. 작업 진입 게이트

- L1 이상 작업은 최신 main, 현재 결정, 분야 정본, 같은 Goal의 열린·최근 병합 PR, 실제 구현을 비교해 중복·누락·충돌·구형 참조·미반영을 먼저 판정한다.
- 새 정책·Template·Skill·경로·ID는 파일 존재가 아니라 README·`START_HERE.md`·운영 정본·Registry·프로젝트 Template·활성 소비자·Test 연결을 확인한다.
- 필요한 실행 파일, 라이브러리, 폰트, 입력, 인증, 저장소·브랜치 권한을 작업과 검증 전에 확인한다.
- 누락 환경은 `필요 항목 / 이유 / 설치·설정 / 적용 / 확인 명령 / 최소 권한`으로 안내한다. 사용자 승인 없이 시스템 전역 설치, 계정·보안 설정, 권한 확대, Branch protection 변경을 수행하지 않는다.
- 사용자가 설치·권한 부여를 알렸어도 실제 경로·버전·인증·쓰기 가능 여부를 다시 확인한다.
- 실행하지 않은 조사·검사·테스트·렌더·빌드·권한을 통과로 보고하지 않는다.
- 문서·Skill의 줄 수·문자 수·분량 상한보다 내용 보존, 실행 가능성, 한 단계 발견성을 우선한다.

## 3. Work Mode·Skill·사용자 결정

새 L1 이상 요청은 `managing-project-intake-and-work-contract`에서 한 번만 접수한다. 사용자는 Skill이나 Skill Mode를 고를 필요가 없다.

- 현재 단계에 주 Work Mode `PLAN / BUILD / REVIEW` 하나와 주 책임 분야 하나를 둔다.
- Registry의 `automatic-trigger-match`로 필요한 최소 Skill·Skill Mode만 선택한다. `load_by_default=false`는 자동 선택 금지가 아니라 비관련 기본 로드 금지다.
- 오탈자, 명확한 단일 파일 기계 수정, 입력이 같은 검사 재실행 외에는 저장소 사실을 조사하고 범위·제외·보호 대상·완료 기준·검증·롤백을 확정한다.
- 프로젝트 코어, 플레이어 경험, 주요 UX, 콘텐츠 의미, 비용·범위를 바꾸는 충돌만 사용자 결정으로 올린다. 저장소·정본·테스트로 판단 가능한 오류나 누락을 사용자에게 전가하지 않는다.
- 사용자 확인 전 실행 계약을 확정하거나 구현하지 않는다. 사용자가 승인한 범위에서는 단계별 구현·검증·적대적 재검토를 끝까지 수행한다.
- 상세 라우팅·권한 전환·리뷰·GPT→Codex·병합 절차는 `docs/WORK_MODE_AND_SKILL_ROUTING.md`를 따른다.

금지:

- 사용자에게 Skill·Skill Mode 선택 전가
- 전체 Skill 자동 로드, trigger 없는 호출, 주 책임 분야 Skill 중복
- Skill 파일을 읽은 사실을 실제 Skill 실행으로 보고
- 사용자 확인 전 범위 확대·대량 병렬화
- 같은 파일·Schema·자산의 소유 경계 없이 병렬 작업
- 검증·발행·Handoff 조기 실행
- `[백업]`, `[보류]`, `[제거 후보]` Skill 호출
- 근거 없는 일정·수치 발명

## 4. 책임 원본·프로젝트·발행 경계

- 한 질문에는 Registry에 등록된 Markdown 또는 JSON 책임 원본 하나만 둔다. DOCX·PDF·대시보드·과거 대화는 독립 정본이 아니다.
- 신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 `[기획서]/` 아래에 둔다. `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 상세 책임 원본, 상태 축, 발행 정책, 완료 조건은 `docs/OPERATING_MODEL.md`를 따른다.
- Base 자체는 프로젝트 Google Sheets 동기화 대상이 아니다. 구성된 프로젝트 Sheet는 `USER_FACING_GDD_WORKSPACE`이며 `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`를 따른다. 사용자 편집은 `PROPOSED_SHEET_CHANGE`로 보존하고 GitHub 정본·실제 구현과 비교한다.
- 일반 기획·상태 확인은 GitHub 정본과 구성된 프로젝트 GDD Sheet를 우선한다. HTML 대시보드는 사용자 명시 요청 또는 기존 유지보수에만 사용한다.
- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들거나 제거·교체하지 않는다. UI 설계·폴리싱·구현 결과 감사는 `auditing-and-refining-ui-art`로 라우팅하고, 사용자 승인 finding만 실제 렌더로 재검수한다.
- 접근성·성능·플레이테스트·벤치마크 결과는 실제 적용된 경우만 보고하며 법적 인증이나 제품 구현 사실로 과장하지 않는다.

## 5. 기존 자료와 Base 변경 안전

- 기존 프로젝트 감사·정리는 `managing-game-project-operating-system`의 현재 mode를 사용한다.
- 사용자 승인 전 파일·폴더 대량 삭제·이동·통합, 구형 이름만 근거로 한 삭제, 기존 책임 문서 대규모 축약, 승인 자산 제거, 프로젝트 용어·수치·결정 변경, `[보류]` 폐기, Base 구조에 맞춘 강제 개명을 하지 않는다.
- 고유 정보·활성 참조·파생본·복구·사용자 승인이 확인되지 않은 항목은 보존한다. Legacy·archive의 상세 판정은 운영 모델과 `governing-legacy-retention-and-archives`가 책임진다.
- 프로젝트 교훈의 Base 승격은 `managing-base-change-proposals`를 사용한다. `[수정제안서]` 제출·검토와 사용자 승인 뒤 별도 구현 PR에서 반영하며, 신규 제안 PR과 활성 Base 구현 PR을 섞지 않는다. 사용자가 직접 승인한 Base 변경 요청은 별도 제안서 없이 작업 계약이 될 수 있다.
- 새 Skill보다 기존 통합 Skill의 mode·reference 확장을 먼저 검토한다. 독립 입력·산출물·권한·검증 경계가 있을 때만 새 Skill을 만든다.
- 실패·중요 결정·재사용 가능한 교훈·실제 검증을 Learning Log에 기록하되 한 번의 성공을 공용 강제 규칙으로 승격하지 않는다.

## 6. 검증·GitHub·보호 표면

- 일반 변경은 `reviewing-and-validating-project-changes`, 실패 가정 공격은 `running-adversarial-review-and-refinement`, 정본·경로·ID·Schema 전파는 필요할 때 `auditing-canonical-reference-freshness`로 검증한다.
- 계약·diff 대조, 포맷·정적 검사, 관련 테스트, 가능한 런타임·렌더·빌드, 정상·실패·경계·회귀, 미검증·위험·롤백을 분리한다.
- 전체 로컬 계약은 `python tools/run_local_validation.py --trusted-history-commit <trusted-main-commit-sha>`로 실행한다. 인자는 검증 전에 확인한 정확한 40자 main SHA이며, 이동 가능한 ref 이름을 넘기지 않는다. 환경 미준비 skip을 pass로 바꾸지 않는다.
- 작업 전 원격·로컬 상태를 확인하고, 검증된 변경만 commit·push한다. Workflow 파일 존재와 실제 Actions 실행·Required Check 강제를 구분한다.
- 병합은 검토한 정확한 HEAD, 필수 검사, 독립 검토, unresolved thread 0, 결정 게이트를 다시 확인한 뒤 저장소가 허용한 방식으로 수행한다.
- `skills/SKILL_REGISTRY.json`, released lock, frozen/generated release artifact, 보호 경로를 변경하려면 해당 전용 계약과 검증을 먼저 충족한다. 범위 밖에서는 bytes를 보존한다.
- 생성 실패·미검증 바이너리·로컬 임시 산출물을 자동 push하지 않는다.

## 7. 완료 보고

L1 이상 완료 보고에는 다음을 실제 수행 증거와 함께 포함한다.

- 사용한 Work Mode·Skill·Skill Mode와 선택 이유
- 주 책임·영향 분야, 승인 범위·제외·보호 대상
- 변경한 문서·코드·데이터·자산·Skill과 유지한 기존 결정
- 실행 단계·의존성·게이트와 실제 결과
- 테스트·런타임·렌더·접근성·성능·참조 최신성·정확한 HEAD 증거
- 실행하지 않은 항목, 불일치, 남은 위험, 롤백, 다음 작업
- 보존·통합·보류·제거 후보, Base 환류 여부

실행하지 않은 Skill, 조사, 테스트, 렌더, 구현, 접근성·성능 검증, 브랜치 보호를 완료로 보고하지 않는다.
