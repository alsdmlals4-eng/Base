# 프로젝트 저장소 운영체계 설치 계획

- 프로젝트:
- 대상 저장소:
- 작성일:
- 기준 브랜치·커밋:
- Base 기준 커밋:
- 프로젝트 유형: `신규 / 운영 중 기존 프로젝트`
- 설치 수준: `Audit only / Governance foundation / Approved migration / Enforcement`
- 상태: `감사 중 / 계획 검토 / 승인 대기 / 설치 중 / 구조 검증 / 완료`

운영 중 기존 프로젝트는 상세 감사에 `EXISTING_PROJECT_MIGRATION_AUDIT.md`를 사용한다. 사용자 승인 전 대규모 삭제·이동·통합·강제 개명을 수행하지 않는다.

## 1. 목적

- 사용자가 반복해서 기억하지 않아도 되는 규칙:
- 새 GPT·Codex가 복원해야 하는 상태:
- 이번 설치가 해결할 현재 문제:
- 이번 설치에서 해결하지 않는 범위:
- 보호할 프로젝트 고유 결정·자산·경로:
- 루트 `[기획서]` 목표 경로:
- Skill Registry·Map 목표 경로:
- 운영체계 Health Review 기준:

## 2. 현재 저장소 감사

### 2.1 최초 읽기

- [ ] `AGENTS.md`
- [ ] README·START_HERE
- [ ] 현재 활성 기획서 폴더와 중첩 복제본
- [ ] Base version·Documentation Map
- [ ] Active Context·Handoff
- [ ] 프로젝트 방향·전체 기획·Roadmap
- [ ] 분야별 본책·부록
- [ ] Development Gates
- [ ] Project Skill Map·Skill Registry·분야별 스킬·Learning Logs
- [ ] PDF·Publication Manifest
- [ ] Visual Source·Asset Manifest·승인 이미지·실제 캡처
- [ ] Issue·Goal·Plan·PR
- [ ] 실제 코드·Scene·데이터·테스트
- [ ] Governance Checker·Workflow·브랜치 보호
- [ ] 최근 커밋·이동·삭제 이력

### 2.2 인벤토리

| ID | 유형 | 현재 경로 | 주 책임 | 영향 분야 | 참조 위치 | 상태 | 고유 정보 | 처리 제안 | 위험 |
|---|---|---|---|---|---|---|---|---|---|
|  | 문서/스킬/Registry/Log/PDF/이미지/코드/데이터/테스트/템플릿 |  |  |  |  | 현행/보조/백업/보류/제거 후보 |  |  |  |

### 2.3 발견한 문제

- 활성 `[기획서]`가 루트가 아닌 위치에 있음:
- 중첩 현행 기획서 복제본:
- 중복 책임 원본:
- 오래된 경로·링크:
- 채팅에만 존재하는 결정:
- 문서·구현·검증 불일치:
- 누락된 작업·제품 게이트:
- 누락된 분야별 프로젝트 스킬:
- Skill Registry·Map·실제 경로 불일치:
- 사용·비사용 조건·trigger·Learning Log 누락:
- 전체 스킬 자동 로드·불필요한 과다 호출:
- 스킬 중복·공용 절차 복제:
- PDF 전체 과정·승인 이미지 누락:
- 이미지 등록·바이너리 누락:
- 승인 이미지·실제 캡처 차이:
- 수치·용어·데이터 계약 충돌:
- Roadmap·Issue·실제 상태 차이:
- 보류 항목의 활성 범위 혼입:
- 자동 검사·브랜치 보호 미설치 또는 미검증:

## 3. 목표 운영 구조

### 3.1 루트 기획서

신규·승인된 설치의 기본 목표:

```text
<repository-root>/[기획서]/
```

- [ ] 사용자가 저장소 첫 화면에서 `[기획서]`를 찾을 수 있다.
- [ ] `docs/[기획서]`, `src/[기획서]` 같은 중첩 현행 복제본이 없다.
- [ ] 기존 경로 이동은 감사·참조 조사·사용자 승인을 거쳤다.

### 3.2 프로젝트 허브

| 책임 | 기존 원본 | 목표 원본 | 생성/갱신 | 비고 |
|---|---|---|---|---|
| 최초 읽기 |  | START_HERE |  |  |
| 현재 상태 |  | ACTIVE_CONTEXT |  |  |
| 문서 지도 |  | DOCUMENTATION_MAP |  |  |
| 개발 게이트 |  | DEVELOPMENT_GATES |  |  |
| 사람용 스킬 지도 |  | PROJECT_SKILL_MAP |  |  |
| 기계 판독 스킬 라우터 |  | SKILL_REGISTRY.json |  |  |
| 갱신 매트릭스 |  | DOCUMENT_UPDATE_MATRIX |  |  |
| 결정·변경 기록 |  | DECISION_LOG·CHANGELOG |  |  |
| AI Workflow |  | AI_WORKFLOW |  |  |
| PDF 최신성 |  | PUBLICATION_MANIFEST |  |  |
| 출처·마이그레이션 감사 |  | SOURCE_AUDIT |  |  |
| 수명주기 |  | 현행·백업·보류·제거 후보 지도 |  |  |
| 운영체계 검수 |  | Health Review |  |  |

### 3.3 분야 구조

| 분야 | 독립 본책/통합 장 | 책임 원본 | Registry 진입 ID | 진입 프로젝트 스킬 | 실제 경로 | 검증 | Learning Log | PDF |
|---|---|---|---|---|---|---|---|---|
| 설정·내러티브 |  |  |  |  |  |  |  |  |
| 게임 디자인 |  |  |  |  |  |  |  |  |
| UX·UI·접근성 |  |  |  |  |  |  |  |  |
| 개발·엔지니어링 |  |  |  |  |  |  |  |  |
| 테크니컬 아트·파이프라인 |  |  |  |  |  |  |  |  |
| 아트 |  |  |  |  |  |  |  |  |
| 사운드 |  |  |  |  |  |  |  |  |
| QA |  |  |  |  |  |  |  |  |
| 프로덕션·PM |  |  |  |  |  |  |  |  |
| 분석·유저리서치 |  |  |  |  |  |  |  |  |
| 통합검수 |  |  |  |  |  |  |  |  |

### 3.4 Foundation 스킬

| 공용 작업 | 프로젝트 스킬 경로 | Base 원본 | trigger | 비호출 조건 | 입력·산출물·검증 | Learning Log |
|---|---|---|---|---|---|---|
| 요청·분야·스킬 라우팅 |  | routing-project-work-by-discipline |  |  |  |  |
| 요구 구체화 |  | transforming-requests-into-prompts |  |  |  |  |
| 영향도 분석 |  |  |  |  |  |  |
| 개발 게이트 |  | DEVELOPMENT_GATES_METHOD |  |  |  |  |
| 결정 기록 |  |  |  |  |  |  |
| 문서 수명주기 |  | writing-game-design-documents |  |  |  |  |
| 검증·완료 |  |  |  |  |  |  |
| PDF 발행 |  | publishing-discipline-bibles |  |  |  |  |
| Active Context·Handoff |  | maintaining-project-context-and-handoff |  |  |  |  |
| 운영체계 Health Review |  | verifying-game-project-operating-system |  |  |  |  |
| 외부 AI 검수 |  | reviewing-external-ai-drafts |  |  |  |  |
| 학습·Base 환류 |  | promoting-project-knowledge |  |  |  |  |

## 4. 파일 변경 계획

### 생성

| 경로 | 역할 | 근거 | 설치 단계 |
|---|---|---|---|
|  |  |  |  |

### 갱신

| 경로 | 변경 내용 | 유지할 기존 내용 | 검증 |
|---|---|---|---|
|  |  |  |  |

### 보존

| 경로 | 보존 이유 | Git 이력만으로 부족한 이유 | 활성 읽기 여부 |
|---|---|---|---|
|  |  |  | 제외/포함 |

### 보류

| 항목·경로 | 보류 이유 | 재개 조건 | 관련 원본 | 선행 작업 |
|---|---|---|---|---|
|  |  |  |  |  |

### 재분류·이동

| 기존 경로 | 목표 경로 | 고유 정보 보존 | 참조 갱신 | 위험 | 사용자 승인 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 제거 후보

| 경로 | 흡수된 원본 | 고유 정보 확인 | 참조 제거 | 보류·미검증 없음 | 복구 | 삭제 승인 |
|---|---|---|---|---|---|---|
|  |  |  |  |  | Git 이력/백업 |  |

모든 조건이 확인되기 전에는 삭제하지 않는다.

## 5. 개발 게이트 설치

### 작업 실행 게이트

- [ ] Intake·Context
- [ ] Definition of Ready
- [ ] Planning·Approval
- [ ] Implementation
- [ ] Verification
- [ ] Documentation
- [ ] Integration·Completion

### 제품 마일스톤

- [ ] Concept
- [ ] Prototype
- [ ] Graybox
- [ ] First Playable
- [ ] Vertical Slice
- [ ] Production
- [ ] Alpha
- [ ] Feature Complete
- [ ] Content Complete
- [ ] Beta
- [ ] Release Candidate

- 현재 단계:
- 다음 Greenlight:
- 실제 증거:
- 미검증:

## 6. 프로젝트 스킬 설치

| 분야·공용 | Registry ID | 진입 스킬 | 본책 | Foundation 의존성 | 실제 파일 | 검증 | Learning Log |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

- [ ] `SKILL_REGISTRY.json`과 `PROJECT_SKILL_MAP.md`를 함께 설치했다.
- [ ] `load_all_skills=false`, `default_selection=none`, `require_trigger_match=true`다.
- [ ] 활성 스킬은 `load_by_default=false`다.
- [ ] 공용 절차를 Foundation에 한 번만 둔다.
- [ ] 각 분야는 독립 진입 스킬 또는 명시적인 통합 책임을 가진다.
- [ ] 스킬에 사용·비사용 조건, trigger tags, 입력, 절차, 산출물, 검증, 실패 조건이 있다.
- [ ] 모든 활성 스킬에 Learning Log와 review trigger가 있다.
- [ ] 모든 의미 있는 호출은 결과를 기록한다.
- [ ] 스킬 본문은 근거가 있을 때만 갱신한다.
- [ ] 지식 상태를 관찰·가설·패턴·검증·승격 후보로 구분한다.
- [ ] 전체 skills 폴더가 아니라 작업에 필요한 스킬만 읽게 한다.

## 7. 이미지·자산 이관

| Asset ID | 현재 위치 | 캐노니컬 목표 | 상태 | 채택 요소 | 비채택 요소 | 실제 캡처 | PDF 포함 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

- [ ] 기존 승인 이미지가 있는 항목에 새 시안을 만들지 않는다.
- [ ] 콘셉트·방향 승인·제작 준비·구현·시각 검증을 구분한다.
- [ ] `MIGRATION_PENDING`과 실제 저장 완료를 구분한다.
- [ ] Visual DNA를 기록한다.
- [ ] 대용량 원본의 Git LFS 필요성을 검토한다.

## 8. 분야별 PDF 발행

| 분야 | 책임 Markdown | 활성 부록 | 승인 이미지 | 출력 PDF | Manifest 상태 | 생성·시각 검수 |
|---|---|---|---|---|---|---|
|  |  |  |  |  | NOT_BUILT/CURRENT/STALE |  |

- [ ] PDF가 분야의 목적부터 전체 과정·현재 상태·다음 작업을 포함한다.
- [ ] 승인 이미지·실제 캡처와 상태 캡션이 있다.
- [ ] PDF는 수동 독립 원본이 아니다.
- [ ] 재현 가능한 생성 명령이 있다.
- [ ] Publication Manifest에 입력·출력·해시가 있다.
- [ ] 파이프라인 미설치·렌더링 미확인은 완료로 표시하지 않는다.

## 9. GitHub 운영 설치

| 항목 | 목표 경로·설정 | 파일 존재 | 실행 확인 | 강제됨 | 검증 방법 |
|---|---|---|---|---|---|
| Issue template |  |  |  |  |  |
| PR template |  |  |  |  |  |
| Documentation Governance config |  |  |  |  |  |
| Documentation checker |  |  |  |  |  |
| Skill Routing checker |  |  |  |  |  |
| GitHub Actions |  |  |  |  |  |
| CODEOWNERS |  |  |  |  |  |
| 브랜치 보호 |  |  |  |  |  |

## 10. 필수 회귀 테스트

- [ ] 정상 프로젝트 구성 통과
- [ ] 중첩 `[기획서]` 실패
- [ ] 전체 스킬 자동 로드 실패
- [ ] 중복 Skill ID 실패
- [ ] 활성 스킬 경로·Learning Log 누락 실패
- [ ] 분야 진입 스킬 누락 실패
- [ ] 스킬 변경 후 Registry·Map·Log 미갱신 실패
- [ ] 금지 활성 버전 파일명 실패
- [ ] PDF 입력 hash·header·visual review 실패
- [ ] `[백업]`, `[보류]` 기본 검사 제외

## 11. 설치 순서

1. 프로젝트 유형 판정
2. 현재 저장소 감사와 인벤토리
3. 루트 `[기획서]` 목표·보존·이동 승인 판정
4. 책임 원본·분야 경계 승인
5. 프로젝트 허브·Development Gates 설치
6. Project Skill Registry·Map·Foundation·분야 스킬 설치
7. 기존 내용·이미지·자산 승계
8. PDF 발행 계약·Publication Manifest 설치
9. Issue·PR·두 Governance Checker·Actions 설치
10. 구조·회귀·추적성 검증
11. 콜드 스타트 테스트
12. 운영체계 Health Review
13. 완전히 흡수된 중복 파일 처리

## 12. 완료 기준

- [ ] 활성 `[기획서]`가 루트에서 명확히 보인다.
- [ ] 중첩 현행 기획서 복제본이 없다.
- [ ] GPT와 Codex의 최초 읽기 순서가 같다.
- [ ] 질문별 현행 책임 원본이 하나다.
- [ ] L1 이상 작업에 주 책임·영향 분야·변경 유형이 있다.
- [ ] 작업·제품 게이트와 증거가 연결됐다.
- [ ] 사람용 Skill Map과 기계 판독 Registry가 일치한다.
- [ ] 모든 11개 책임 분야의 진입 스킬 또는 통합 책임이 등록됐다.
- [ ] 전체 스킬 자동 로드가 금지됐다.
- [ ] 모든 의미 있는 스킬 호출에 Learning Log가 있다.
- [ ] 변경 유형별 필수 갱신 문서가 판정된다.
- [ ] 이미지에 캐노니컬 경로와 상태가 있다.
- [ ] 기존 승인 이미지 임의 교체 금지가 명시돼 있다.
- [ ] 분야 PDF가 전체 과정과 승인 이미지를 포함한다.
- [ ] 두 Governance Checker의 정상·실패 테스트가 통과했다.
- [ ] 파일 존재·실행 확인·강제 상태가 구분됐다.
- [ ] 새 작업자가 10분 안에 방향·상태·다음 작업·최소 스킬·검증을 찾는다.
- [ ] 수행하지 않은 런타임·PDF·브랜치 보호 검증을 완료로 표시하지 않았다.
- [ ] Health Review에 상태와 증거가 있다.

## 13. 검증 계획

### 구조 검증

- 루트 `[기획서]`:
- 필수 파일 존재:
- 링크 검사:
- Responsibility SSOT:
- Skill Registry·Map:
- Learning Logs:
- 이미지 경로:
- 금지 파일명:
- PDF Manifest:
- 변경 매트릭스 샘플:

### 추적성 샘플

| 결정 | 본책 | Issue·Plan | 구현·자산 | 테스트·캡처 | PDF·현재 상태 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### 스킬 라우팅 샘플

| 요청 | 주 책임 | Foundation 스킬 | 분야 스킬 | 불필요해 호출하지 않은 스킬 | 검증 | Learning Log |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

### 런타임 검증

- 실행 명령:
- 자동 테스트:
- 수동 플레이 경로:
- 미검증 항목:

### 콜드 스타트 테스트

- 수행자:
- 소요 시간:
- 답하지 못한 질문:
- 보강한 문서·Registry·스킬:

## 14. 운영체계 Health Review

- 보고서 경로:
- 루트·시작 문서 상태:
- 책임 원본·수명주기 상태:
- 스킬 Registry·학습 상태:
- 개발 게이트·추적성 상태:
- 이미지·PDF 상태:
- 자동화·브랜치 보호 상태:
- 콜드 스타트 상태:
- FAIL·PARTIAL 수정 우선순위:

## 15. 위험과 롤백

- 가장 큰 이관 위험:
- 보호할 경로:
- 되돌리는 방법:
- 자동화 실패 시 수동 절차:
- Registry·Learning Log 복구:
- Base와 프로젝트 후속 동기화:
