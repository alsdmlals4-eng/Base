# Base Skill Learning Log

## 2026-07-19 운영체계 감사에서 확인한 재사용 교훈

- 프로젝트 운영 문서의 최신성은 파일 존재 검사가 아니라 활성 참조와 설치 매핑을 함께 검사해야 한다.
- 발행본의 `CURRENT` 상태와 사람의 시각 검수 완료 상태는 서로 독립적으로 관리해야 한다.
- Learning Log는 모든 호출이 아니라 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있을 때 기록한다.
- 11개 분야는 공용 카탈로그이며 프로젝트가 선택하지 않은 분야를 필수 진입점으로 강제하지 않는다.
- 작업에 필요한 도구·파일·인증·권한이 없으면 사용자에게 이유와 설치·적용·확인 방법을 안내하고, 완료 통보 뒤 실제 환경을 다시 검증한다.

> Base 실행 스킬의 실제 적용 결과, 실패, 예외와 갱신 결정을 기록한다. 이 문서는 기본 작업 컨텍스트가 아니며 `skills/SKILL_REGISTRY.json`에서 특정 스킬의 학습 검토가 필요할 때만 읽는다.

## 기록 원칙

- 스킬을 호출했다는 이유만으로 본문을 매번 바꾸지 않는다.
- 실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있는 실행을 기록한다.
- 반복 실패, 새 예외, 경로·도구·검증 변경이 발생하면 스킬 계약을 검토한다.
- 한 번의 성공은 `관찰` 또는 `가설`이다.
- 여러 조건에서 재현되기 전에는 `검증`이나 공용 강제 규칙으로 승격하지 않는다.
- 프로젝트 고유 이름·수치·파일 경로·승인 자산은 Base 로그에 복사하지 않는다.

## 2026-07-19 schema v3 발행 검증 교훈

- LibreOffice의 자동 TOC 필드는 headless PDF 변환에서 빈 목차가 될 수 있으므로 고정 섹션 목록을 직접 생성해야 한다.
- 구조화 JSON의 목록 항목은 상세 객체뿐 아니라 간단 문자열도 안전하게 렌더할 수 있어야 한다.
- Mermaid는 고정 CLI와 lockfile만으로 부족하며 브라우저 실행 경로도 사전 점검해야 한다.
- 강제 LibreOffice 재빌드의 플랫폼별 바이너리 동일성을 과장하지 않고, 동일 입력 정상 재실행 무재작성·diff 0을 공식 결정성 계약으로 둔다.
- 생성 실패를 대표 fixture에서 재현해 기존 PDF·Manifest 해시 보존을 확인해야 한다.

## 실행 기록 템플릿

```md
### [날짜] [skill_id]
- 프로젝트·작업:
- 기준 스킬 커밋:
- 호출 트리거:
- 입력 범위:
- 실제 산출물:
- 실행한 검증:
- 결과: 성공 / 부분 성공 / 실패 / 미검증
- 성공 조건:
- 실패·예외·재현 조건:
- 사용자 피드백:
- 불필요하게 호출한 스킬:
- 누락된 스킬·검증:
- 스킬 본문 변경 필요: 예 / 아니오
- 변경하지 않는 이유:
- 지식 상태: 관찰 / 가설 / 패턴 / 검증 / 승격 후보
- 프로젝트 전용으로 유지할 내용:
- Base Method·Skill·Template·Test 환류 후보:
- 다음 검토 트리거:
```

## 학습 상태 승격 기준

| 상태 | 최소 근거 | 허용 사용 |
|---|---|---|
| 관찰 | 1회 실행·피드백 | 참고만 가능 |
| 가설 | 원인·적용 조건·실패 조건 제시 | 제한적 시험 적용 |
| 패턴 | 서로 다른 작업에서 반복 | 프로젝트 권장 절차 |
| 검증 | 여러 조건에서 재현·회귀 검증 | Base 공용 계약 후보 |
| 승격 후보 | 프로젝트 독립성과 중복 검수 완료 | Method·Skill·Template·Test 반영 검토 |

## 정기 Health Review

다음 중 하나가 발생하면 `verifying-game-project-operating-system` 또는 `evolving-project-discipline-skills`를 호출한다.

- 동일 실패가 두 번 이상 반복됨
- 90일 이상 검토 기록이 없음
- 등록된 Markdown 또는 JSON 책임 원본·실제 경로·검증 명령 변경
- 새 분야·반복 작업 유형 추가
- 스킬 절차 중복
- 새 채팅이 필요한 스킬·기획서를 찾지 못함
- 과도한 스킬 호출
- DOCX/PDF·다이어그램 발행본이 Registry보다 오래됨

## 기록

### 2026-07-19 structured design documents and human publication pipeline

- 프로젝트·작업: Base PR #8 — 모든 프로젝트·분야 기획서의 AI JSON + 사람용 DOCX/PDF + 다이어그램·승인 이미지 구조
- 기준 스킬 커밋: `51d3535afa3eea5b19d262e1fe87d06f183c2224`
- 호출 트리거: 스킬맵뿐 아니라 모든 기획서가 이미지 확인 가능한 사람용 문서를 가져야 한다는 사용자 피드백
- 입력 범위: Base 시작 규칙·운영 Method·기획서 작성·마이그레이션·발행·스킬 진화·Health Review·프로젝트 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: Design Document Registry·JSON 본책 템플릿·DOCX/PDF·다이어그램 생성기·승인 이미지 포함·세 번째 Governance Checker·실제 생성 통합 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Design Publication Governance, JSON 기획서와 Skill Registry의 DOCX/PDF·다이어그램 실제 생성, 승인 이미지 포함, PDF 전 페이지 렌더, 구조 회귀, whitespace
- 결과: 성공
- 성공 조건: 기획서·스킬맵 실제 생성, 세 Governance Checker, 구조 회귀, PDF 렌더와 whitespace가 최종 head의 GitHub Actions run #18에서 모두 통과
- 실패·예외·재현 조건: 초기 CI에서 pip 캐시 입력 파일 부재로 Python 설정이 실패해 캐시를 제거함. 다음 실행에서 스킬 진화 Method와 Health Review 스킬 연결 문구 누락이 구조 테스트에 검출돼 계약을 보완함.
- 사용자 피드백: AI는 JSON을 읽고 사람은 DOCX/PDF와 이미지·다이어그램을 한눈에 확인해야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 기존 구조에는 프로젝트 전체·분야 기획서용 구조화 Registry, 승인 이미지 포함 DOCX, 생성기 해시와 전 페이지 PDF 렌더 검사가 없었음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 실제 게임의 세계관·수치·구현 경로·승인 이미지·생성된 기획서 바이너리
- Base Method·Skill·Template·Test 환류 후보: 이번 PR의 JSON 계약·생성기·Checker·통합 테스트 전체
- 다음 검토 트리거: 첫 대상 프로젝트 실제 마이그레이션, DOCX/PDF 렌더 실패 반복, Registry와 발행본 불일치

### 2026-07-19 operating-system skill routing and learning audit

- 프로젝트·작업: Base PR #7 — 선택적 스킬 호출·지속 학습·루트 기획서 검수
- 기준 스킬 커밋: `c65ffe2e589caf8e38c546dbdfcd37e669b09f9f`
- 호출 트리거: 분야별·Foundation 스킬의 항상 학습, 필요한 경우에만 호출, 운영체계 연결 검증, 루트 `[기획서]` 요청
- 입력 범위: Base START_HERE·AGENTS·README·Documentation Map·운영체계 Method·Installer·Project Operations 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: 공용·프로젝트 Skill Registry, 라우팅·Handoff·Health Review 스킬, Learning Log 계약, 루트 기획서·Registry 자동 검사와 회귀 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Base 구조 테스트, `git diff --check`
- 결과: 성공
- 성공 조건: Registry·루트 기획서·동기화 실패 테스트와 whitespace 정상
- 실패·예외·재현 조건: `[기획서]` 대괄호 glob 해석 문제를 실제 폴더명 비교로 수정
- 사용자 피드백: 스킬이 항상 학습 가능하고 필요한 때만 호출되며 활성 기획서는 최상위 폴더에서 보여야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 요청 라우팅, Context·Handoff, Health Review와 Skill Registry 검사
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 대상 게임의 구체 스킬·실제 경로·승인 자산
- Base Method·Skill·Template·Test 환류 후보: Method·Skill·Registry·Health Report·Checker·회귀 테스트
- 다음 검토 트리거: 대상 프로젝트 첫 실제 적용, 동일 라우팅 실패 반복, 90일 이상 미검토

### 2026-07-21 project core and adversarial review foundations

- 프로젝트·작업: Base 직접 승인 요청 — 프로젝트 코어 확인·형성 절차와 범용 적대적 비평–검증–개선 루프 추가
- 기준 스킬 커밋: `3c78025e35d762e266414c9735d5557b4cac3c55`, `95e3dfd7645aed62ed438291912cebb417df6b96`
- 호출 트리거: 프로젝트 코어를 기준선으로 형성하는 절차와, 코어에 한정되지 않고 모든 분야 산출물을 개선하는 범용 검토 절차가 필요하다는 사용자 요청
- 입력 범위: Base README·AGENTS·Documentation Map·Skill Registry·외부 AI 검수 스킬·요청 프롬프트 변환 스킬·스킬 진화 계약·Learning Log
- 실제 산출물: `defining-and-verifying-project-core`, `running-adversarial-critique-validation-refinement`, 프로젝트 코어 계약 템플릿, 적대적 검토 보고서 템플릿, Registry 항목
- 실행한 검증: 신규 경로 GitHub 재조회, Registry JSON 로컬 파싱, `main` 대비 branch compare, 두 스킬의 사용·비사용 조건과 기존 외부 AI·UI·Health Review 스킬 책임 경계 수동 대조
- 결과: 부분 성공
- 성공 조건: 두 스킬과 템플릿이 별도 책임으로 등록되고, 적대적 검토가 프로젝트 코어 없이도 일반 개선에 독립 사용 가능하며 코어 영향 작업에서만 코어 스킬과 연결됨
- 실패·예외·재현 조건: 현재 환경에서 저장소 clone과 GitHub Actions·Governance Checker 실행은 불가능해 자동 검증은 PR CI에 남음
- 사용자 피드백: 적대적 검토 루프는 프로젝트 코어뿐 아니라 다른 모든 분야의 개선 스킬로 기능해야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 첫 실제 프로젝트 적용, 자동 Skill Routing Governance, 콜드 스타트에서 신규 trigger 선택 검증
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 관찰
- 프로젝트 전용으로 유지할 내용: 실제 프로젝트의 코어 계약, 고유 목표·수치·아트 방향·검토 finding과 결과
- Base Method·Skill·Template·Test 환류 후보: 실제 적용 후 반복되는 거짓 양성·누락 관점·종료 조건을 회귀 사례로 추가
- 다음 검토 트리거: 첫 대상 프로젝트 적용, CI 실패, 기존 분야 스킬과 책임 중복, 적대적 검토의 무한 반복 또는 코어 과잉 보호 발생
