# 프로젝트 저장소 운영체계 설치 계획

- 프로젝트:
- 대상 저장소:
- 작성일:
- 기준 브랜치·커밋:
- Base 기준 커밋:
- 프로젝트 유형: `신규 / 운영 중 기존 프로젝트`
- 설치 수준: `Audit only / Governance foundation / Approved migration / Enforcement`
- 상태: `감사 중 / 승인 대기 / 설치 중 / 구조 검증 / 완료`

운영 중 기존 프로젝트는 사용자 승인 전 대규모 삭제·이동·통합·강제 개명을 수행하지 않는다.

## 1. 목적·보호 범위

- 사용자가 반복해서 기억하지 않아도 되는 규칙:
- 새 GPT·Codex가 복원해야 하는 상태:
- 해결할 문제:
- 해결하지 않는 범위:
- 보호할 결정·수치·자산·경로:
- 루트 `[기획서]` 목표 경로:
- 사람용 최신 문서를 찾는 경로:

## 2. 현재 저장소 감사

### 최초 읽기

- [ ] AGENTS·README·START_HERE
- [ ] 현재 기획서 폴더와 중첩 복제본
- [ ] Active Context·Handoff·Roadmap
- [ ] Markdown·JSON·DOCX·PDF 기획서와 부록
- [ ] Skill Registry·스킬·Learning Log
- [ ] 승인 이미지·실제 캡처·Asset Manifest
- [ ] Issue·Goal·Plan·PR
- [ ] 실제 코드·Scene·데이터·테스트
- [ ] Governance Checker·Workflow·브랜치 보호
- [ ] 최근 커밋·이동·삭제 이력

### 인벤토리

| ID | 유형 | 현재 경로 | 책임 | 참조 | 상태 | 고유 정보 | 목표 처리 | 위험 |
|---|---|---|---|---|---|---|---|---|
|  | 문서/JSON/DOCX/PDF/이미지/스킬/코드/테스트 |  |  |  | 현행/보조/백업/보류/제거 후보 |  |  |  |

### 발견한 문제

- 루트가 아닌 활성 `[기획서]`:
- 중첩 현행 복제본:
- 중복 책임 원본:
- Markdown·DOCX·PDF에만 남은 고유 정보:
- 실제 구현과 기획서 불일치:
- 누락된 분야 책임·게이트·스킬:
- 승인 이미지·실제 캡처 누락:
- 오래된 사람용 문서·Manifest:
- 자동 검사·브랜치 보호 미설치 또는 미검증:

## 3. 목표 루트 구조

```text
[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DEVELOPMENT_GATES.md
│  ├─ DESIGN_DOCUMENT_REGISTRY.json
│  ├─ SKILL_REGISTRY.json
│  ├─ PROJECT_SKILL_MAP.docx
│  ├─ PROJECT_SKILL_MAP.pdf
│  ├─ PROJECT_SKILL_MAP.assets/
│  └─ SKILL_MAP_PUBLICATION_MANIFEST.json
└─ 분야별 폴더/
```

운영 라우터는 Markdown을 유지할 수 있다. 프로젝트·분야 기획 본책은 JSON이다.

## 4. Design Document Registry 계획

| 문서 ID | 책임 범위 | 상태 | JSON | DOCX | PDF | assets | Manifest |
|---|---|---|---|---|---|---|---|
| project-master-plan | 프로젝트 전체 |  |  |  |  |  |  |
|  | 설정·내러티브 |  |  |  |  |  |  |
|  | 게임 디자인 |  |  |  |  |  |  |
|  | UX·UI·접근성 |  |  |  |  |  |  |
|  | 개발·엔지니어링 |  |  |  |  |  |  |
|  | 테크니컬 아트·파이프라인 |  |  |  |  |  |  |
|  | 아트 |  |  |  |  |  |  |
|  | 사운드 |  |  |  |  |  |  |
|  | QA |  |  |  |  |  |  |
|  | 프로덕션·PM |  |  |  |  |  |  |
|  | 분석·유저리서치 |  |  |  |  |  |  |
|  | 통합검수 |  |  |  |  |  |  |

통합 본책은 `responsibility_coverage`에 담당 분야를 모두 기록한다.

## 5. JSON 본책 계약

각 활성 본책:

- 문서 ID·종류·분야·책임·상태
- 목적·플레이어 가치·현재 목표
- Quality Bar·금지 방향
- 책임·비책임·협업 계약
- 분야 전체 작업 과정
- 작업·제품 게이트
- Foundation·분야 스킬
- 확정·구현·검증·확인 필요·보류
- 결정·실제 경로·검증 증거
- 상세 기획
- 승인 이미지·실제 캡처
- 위험·다음 작업·Ready·Done
- 부록·변경·학습 이력

## 6. 사람용 발행 계획

```text
기획서 JSON
→ 자동 workflow·status·responsibility 다이어그램
→ 승인 이미지·실제 캡처 포함
→ DOCX
→ PDF
→ PDF 전 페이지 렌더 검수
→ 기획서_PUBLICATION_MANIFEST.json
```

| 문서 ID | 생성 명령 | 자동 렌더 | 사람 시각 검수 | 상태 | 재생성 트리거 |
|---|---|---|---|---|---|
|  |  |  |  | NOT_BUILT/CURRENT/STALE/FAILED |  |

## 7. 프로젝트 스킬 설치

| 분야·공용 | Registry ID | 진입 스킬 | 관련 JSON | 실제 파일 | 검증 | Learning Log |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

- [ ] `SKILL_REGISTRY.json`을 설치했다.
- [ ] 사람용 `PROJECT_SKILL_MAP.docx/.pdf/.assets`를 생성했다.
- [ ] `PROJECT_SKILL_MAP.md`를 만들지 않았다.
- [ ] 전체 스킬 자동 로드가 꺼져 있다.
- [ ] 각 분야에 진입 스킬 또는 명시적 통합 책임이 있다.
- [ ] 모든 의미 있는 호출은 Learning Log에 기록한다.

## 8. 개발 게이트

```text
Intake·Context → Ready → Approval → Implementation → Verification → Documentation → Completion
```

```text
Concept → Prototype → Graybox → First Playable → Vertical Slice → Production → Alpha → Feature Complete → Content Complete → Beta → Release Candidate
```

- 현재 단계:
- 다음 Greenlight:
- 실제 증거:
- 미검증:

## 9. 이미지·자산 이관

| Asset ID | 현재 위치 | 캐노니컬 목표 | 상태 | 채택 | 비채택 | 실제 캡처 | 포함 기획서 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

- [ ] 기존 승인 이미지가 있는 항목에 새 시안을 만들지 않았다.
- [ ] 콘셉트·승인·제작·구현·시각 검증을 구분했다.
- [ ] 이미지 경로를 JSON `approved_visuals`에 연결했다.

## 10. 파일 변경 계획

### 생성·갱신

| 경로 | 역할 | 유지할 기존 내용 | 검증 |
|---|---|---|---|
|  |  |  |  |

### 보존·보류·제거 후보

| 경로 | 분류 | 이유·재개 조건 | 고유 정보·참조 | 복구 | 사용자 승인 |
|---|---|---|---|---|---|
|  | 백업/보류/제거 후보 |  |  | Git 이력/백업 |  |

모든 고유 정보와 참조가 검증되기 전에는 삭제하지 않는다.

## 11. GitHub Enforcement

| 항목 | 파일 존재 | 실행 확인 | 강제됨 | 검증 방법 |
|---|---|---|---|---|
| Issue·PR Template |  |  |  |  |
| CODEOWNERS |  |  |  |  |
| Documentation Checker |  |  |  |  |
| Skill Routing Checker |  |  |  |  |
| Design Publication Checker |  |  |  |  |
| DOCX/PDF 생성 통합 테스트 |  |  |  |  |
| GitHub Actions |  |  |  |  |
| Branch Protection |  |  |  |  |

## 12. 변경 전후 보존 대조

| 기존 내용 | 기존 위치 | JSON 위치 | 사람용 출력 | 보존 | 참조 검증 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## 13. 콜드 스타트·Health Review

새 AI가 저장소만으로 다음을 찾는다.

- 프로젝트 목적·핵심 경험
- 현재 구현·검증 상태
- 다음 작업·게이트
- 변경 금지 결정·자산
- 프로젝트 전체·분야별 JSON 본책
- 사람용 최신 DOCX/PDF·승인 이미지
- 분야별 스킬·검증 방법
- 보류·확인 필요·미검증

| 영역 | PASS/PARTIAL/FAIL/NOT_RUN | 증거 | 수정 |
|---|---|---|---|
| 루트·시작 |  |  |  |
| Design Registry·JSON |  |  |  |
| DOCX/PDF·자산 |  |  |  |
| Skill Registry·Learning |  |  |  |
| Gates·Traceability |  |  |  |
| Governance·GitHub |  |  |  |
| Cold Start |  |  |  |

## 14. 완료 조건

- [ ] 루트 `[기획서]`가 있다.
- [ ] Design Document Registry가 프로젝트 전체와 모든 분야를 책임진다.
- [ ] 모든 활성 본책에 JSON·DOCX·PDF·다이어그램·Manifest가 있다.
- [ ] Skill Registry와 사람용 스킬맵이 일치한다.
- [ ] Development Gates·Roadmap·Active Context가 연결된다.
- [ ] 승인 이미지와 실제 캡처가 추적된다.
- [ ] 세 Governance Checker와 생성 통합 테스트가 통과한다.
- [ ] 새 채팅이 저장소만으로 작업을 재개한다.
- [ ] 실행하지 않은 렌더링·테스트·브랜치 보호를 완료로 표시하지 않았다.
