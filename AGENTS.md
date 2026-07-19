# Base 공용 AI 작업 규칙

Base는 여러 게임 프로젝트가 공유하는 **[학습형] [공용]** Method·Skill·Template·Case·Test의 원본이다. 프로젝트는 Base를 그대로 복제하지 않고 자신의 세계관, 수치, 엔진, 실제 경로, 승인 자산과 구현 상태에 맞게 분화·적용·검증한다.

## 1. Base URL 호출

사용자가 다음처럼 요청하면 먼저 `START_HERE.md`를 읽는다.

> `https://github.com/alsdmlals4-eng/Base 를 전부 살펴보고 참고해서 작업해줘.`

모든 파일과 스킬을 무작정 읽지 않는다. `START_HERE.md`, `docs/DOCUMENTATION_MAP.md`, `skills/SKILL_REGISTRY.json`으로 현재 작업에 필요한 책임 원본과 최소 스킬 집합만 선택한다.

대상 프로젝트 읽기 순서:

```text
프로젝트 AGENTS.md
→ 루트 [기획서]/00_프로젝트_허브/START_HERE.md
→ ACTIVE_CONTEXT.md·DOCUMENTATION_MAP.md·DEVELOPMENT_GATES.md
→ DESIGN_DOCUMENT_REGISTRY.json·SKILL_REGISTRY.json
→ 현재 분야의 Markdown 또는 JSON 책임 원본·필요한 스킬
→ 사람 열람이 필요하면 최신 PDF·선택적 DOCX·다이어그램·승인 이미지
→ Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산·테스트
```

저장소 접근 없이 설치·마이그레이션·검수 완료를 주장하지 않는다.

### 필요한 작업 환경 요청

- 작업·최적화·검증에 필요한 실행 파일, 라이브러리, 폰트, 기준 파일, 계정 인증 또는 저장소·브랜치 권한이 없으면 우회 결과를 정상 완료로 처리하지 않는다.
- 사용자에게 `필요 항목`, `필요한 이유`, `권장 설치·설정 방법`, `적용 또는 재시작 방법`, `설치 후 확인 명령`, `요청하는 최소 권한 범위`를 구체적으로 안내하고 요청한다.
- 사용자 승인 없이 시스템 전역 설치, 계정·보안 설정 변경, 권한 확대, Branch protection 변경을 수행하지 않는다.
- 사용자가 설치·권한 부여를 완료했다고 알려도 실제 경로·버전·인증·쓰기 가능 여부를 확인한 뒤 사용한다.

## 2. 루트 기획서와 책임 원본

신규 프로젝트와 승인된 마이그레이션의 활성 기획서는 저장소 루트 아래에 둔다.

```text
<repository-root>/[기획서]/
```

기획 본책의 책임 구조:

```text
AI·자동 검사 → 문서별 단일 Markdown 또는 JSON 책임 원본
사람 기본 열람 → 기획서 PDF
Word 검토가 필요할 때 → 선택적 기획서 DOCX
시각 자료가 필요할 때 → Mermaid + 기획서.assets/generated + approved
최신성 → 기획서_PUBLICATION_MANIFEST.json
전체 라우팅 → DESIGN_DOCUMENT_REGISTRY.json
```

- 서술 중심 기획 본책은 Markdown을 기본으로 하고, Registry·Manifest·상태·ID·경로·게임 데이터는 JSON을 사용한다.
- 각 문서는 Registry에 `source_format: markdown | json`으로 단일 책임 원본을 선언한다.
- PDF는 원본 변경과 같은 작업에서 항상 최신 동기화하며 DOCX·다이어그램은 선택 파생본이다.
- DOCX·PDF를 별도 원본으로 수동 유지하지 않는다.
- 같은 서술을 Markdown과 JSON 양쪽에 중복 책임 원본으로 만들지 않는다.
- 기존 프로젝트의 안정된 경로와 본책은 감사·보존 대조·사용자 승인 없이 강제 이동·변환하지 않는다.

## 3. 프로젝트 스킬맵

```text
SKILL_REGISTRY.json
→ AI 선택적 호출 책임 원본

PROJECT_SKILL_MAP.pdf
→ 사람이 보는 이미지 포함 최신본

PROJECT_SKILL_MAP.md
→ 설정한 프로젝트에서만 자동 생성하는 선택 요약 파생본

PROJECT_SKILL_MAP.docx
→ Word 검토가 필요할 때만 생성하는 선택 파생본

PROJECT_SKILL_MAP.assets/
→ 호출 흐름·분야 라우팅·상태 매트릭스
```

자동 생성한 `PROJECT_SKILL_MAP.md`는 파생본 헤더와 Registry 해시를 포함하며 수동 책임 원본으로 사용하지 않는다.

## 4. 작업 유형·스킬 라우팅

새 L1 이상 요청은 `skills/routing-project-work-by-discipline/SKILL.md`로 다음을 판정한다.

- 작업 수준 L0~L4
- 주 책임 분야 하나
- 영향 분야
- 변경 유형
- 필요한 Foundation 스킬
- 주 책임 분야 진입 스킬
- 후속 단계에서만 호출할 검증·발행·Handoff 스킬

주요 라우팅:

- 운영체계 신규 설치: `installing-game-project-operating-system`
- 기존 프로젝트 안전 재배치: `migrating-existing-game-project-structure`
- 분야별 스킬 생성·학습: `evolving-project-discipline-skills`
- Markdown·JSON 기획서와 PDF 발행: `publishing-discipline-bibles`
- Active Context·Handoff: `maintaining-project-context-and-handoff`
- 운영체계 Health Review: `verifying-game-project-operating-system`
- Vertical Slice: `designing-vertical-slices`
- 기획 책임 구조: `writing-game-design-documents`
- 외부 AI 결과 검수: `reviewing-external-ai-drafts`
- 프로젝트 교훈 환류: `promoting-project-knowledge`

금지:

- 전체 skills 폴더 기본 로드
- `load_by_default=true`인 활성 스킬
- trigger와 무관한 호출
- 같은 책임의 중복 스킬 동시 호출
- `[백업]`, `[보류]`, `[제거 후보]` 스킬 호출
- 검증·발행·Handoff 스킬의 조기 호출

## 5. 우선순위

충돌 시 다음을 따른다.

1. 사용자의 최신 지시
2. 프로젝트 `AGENTS.md`와 보안·엔진 규칙
3. 프로젝트 Active Context·Handoff
4. 승인된 기획서와 `GitHub Issue` 또는 사용자가 승인한 직접 요청·Goal·Plan
5. 실제 구현·데이터·자산·테스트 증거
6. 프로젝트에 동기화된 Base 기준
7. Base 원격 원본
8. 과거 대화·초안·추정

실제 파일과 기획서가 다르면 차이를 보고한다. 정상 동작 중인 사용자 변경을 임의로 되돌리지 않는다.

## 6. 프로젝트 지속성 계약

새 채팅과 새 AI가 저장소만으로 다음을 찾을 수 있어야 한다.

- 프로젝트 목적과 핵심 플레이어 경험
- 현재 개발 단계·다음 게이트·최우선 작업
- 확정·구현·검증·미확정·보류
- 변경하면 안 되는 결정과 보호 경로
- 프로젝트 전체·분야별 Markdown 또는 JSON 본책
- 사람용 최신 PDF·선택적 DOCX와 승인 이미지
- 분야별 프로젝트 스킬과 최소 호출 스킬
- 실제 코드·데이터·자산·테스트
- 작업 종료 갱신 대상과 Base 환류 경계

Active Context·Handoff는 본책을 복제하지 않고 현재 상태와 읽기 순서만 연결한다.

## 7. 작업 시작 계약

```yaml
work_contract_type: github_issue/approved_direct_request
primary_discipline:
affected_disciplines:
change_type:
goal:
user_or_player_value:
scope:
out_of_scope:
protected_paths:
required_tools_and_files:
required_permissions:
required_design_document_ids:
foundation_skills:
discipline_skills:
deferred_skills:
asset_impact:
publication_impact:
acceptance_criteria:
validation:
```

직접 요청 작업은 Issue가 없어도 된다. 대신 승인된 요청이나 PR 본문·Goal에 목표, 배경, 범위, 제외 범위, 보호 대상, 완료 기준과 검증 증거를 남긴다. 여러 시스템·장기 추적·여러 PR이 필요한 작업은 Issue를 권장한다.

작업 실행 게이트:

```text
Intake·Context
→ Definition of Ready
→ Planning·Approval
→ Implementation
→ Verification
→ Documentation
→ Integration·Completion
```

- Ready 전에는 구현하지 않는다.
- L2 이상은 실제 저장소 조사에 근거한 Plan과 사용자 승인을 우선한다.
- 실행하지 않은 검증은 `[미검증]`으로 기록한다.
- 작업 완료와 Vertical Slice·Alpha·Beta 통과를 혼동하지 않는다.

## 8. 기존 프로젝트 안전 마이그레이션

```text
기존 내용 보존
→ 책임·참조·고유 정보 감사
→ Markdown·DOCX·PDF·이미지·코드 경로 조사
→ 문서 역할에 맞는 Markdown·JSON 책임 구조와 발행 구조 제안
→ 변경 전후 보존 대조
→ 사용자 승인
→ 승인 범위만 변경
→ DOCX/PDF·링크·스킬·콜드 스타트 검증
→ 기존 원본 제거 후보 별도 승인
```

사용자 승인 전 금지:

- 파일·폴더 대량 삭제·이동
- 기존 책임 문서 대규모 축약
- 여러 문서를 합친 뒤 원본 제거
- 승인 이미지·자산 제거 또는 임의 교체
- 프로젝트 용어·수치·결정 변경
- `[보류]` 폐기
- Base 구조에 맞춘 강제 개명

## 9. 책임 원본·수명주기·토큰 효율

- 한 질문에는 현행 책임 원본 하나를 둔다.
- 같은 내용을 Markdown·JSON·Skill·운영 문서에 장문 복사하지 않는다.
- `v2`, `final`, `latest`, 날짜별 활성 복제본을 만들지 않는다.
- 단순 이전 버전은 Git 이력으로 보존한다.
- `[백업]`은 Git 이력만으로 부족한 외부 원본·감사·승인 근거에만 사용한다.
- `[보류]`에는 이유·재개 조건·관련 책임 원본·선행 작업을 기록한다.
- `[제거 후보]`는 고유 정보·참조·복구·사용자 승인 전 삭제하지 않는다.
- 백업·보류·제거 후보는 기본 읽기에서 제외한다.

## 10. 분야별·Foundation 스킬의 학습

실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있는 의미 있는 스킬 호출을 Learning Log에 기록한다. 사소한 조회와 반복 호출을 의무 기록하지 않는다.

- 호출 트리거와 실제 범위
- 성공·부분 성공·실패·미검증
- 실패·예외·사용자 피드백
- 불필요하게 호출한 스킬
- 누락된 스킬·검증
- 스킬 변경 필요 여부와 변경하지 않는 이유
- 지식 상태와 다음 검토 트리거

스킬 본문은 반복 실패, 새 예외, 책임·경로·검증 변경처럼 근거가 있을 때만 갱신한다. 한 번의 성공을 즉시 공용 강제 규칙으로 만들지 않는다.

## 11. Markdown·JSON 기획서 발행

관련 스킬: `publishing-discipline-bibles`

```text
DESIGN_DOCUMENT_REGISTRY.json에서 활성 문서 선택
→ 문서별 Markdown 또는 JSON 책임 원본 갱신
→ 필요한 문서에서만 Mermaid·생성 다이어그램 처리
→ 승인 이미지·실제 캡처 포함
→ 임시 또는 선택적 DOCX 생성
→ PDF 변환
→ 전 페이지 렌더 검수
→ 입력·출력·생성기·이미지 해시 Manifest
→ Governance 검사
```

책임 원본, 승인 이미지, Mermaid 또는 생성기가 바뀌면 PDF와 Manifest를 같은 작업에서 재생성한다. 선택한 DOCX·다이어그램도 함께 동기화한다. PDF 최신성과 사람 시각 검수 상태는 분리한다.

## 12. 이미지·자산 계약

- 기존 승인 이미지가 있으면 별도 지시 없이 새 시안을 만들지 않는다.
- 활성 항목에는 캐노니컬 경로 하나만 사용한다.
- 콘셉트·방향 승인·제작 준비·구현·실제 화면 검증을 구분한다.
- Asset ID·출처·승인 상태·캡션·채택 요소·비채택 요소·실제 캡처를 책임 원본 또는 구조화 Asset Manifest에 연결한다.
- 이미지 안 임시 수치·문구를 공식 기획값으로 해석하지 않는다.

## 13. 검증과 완료

작업은 다음이 끝나야 완료다.

1. 실제 결과와 승인·구현·검증 상태가 일치한다.
2. 관련 Markdown 또는 JSON 책임 원본·Design Document Registry가 최신이다.
3. 관련 Skill Registry·Learning Log가 최신이다.
4. 책임 원본·이미지 변경 시 PDF·Manifest와 선택 파생본이 재생성됐다.
5. Development Gates·Roadmap·Active Context·Documentation Map이 최신이다.
6. 자동·수동·시각 검증과 미검증이 분리됐다.
7. PR Required Checks와 리뷰가 통과했다.
8. 다음 작업·선행 조건·Handoff가 존재한다.
9. 새 AI가 저장소만으로 방향·상태·기획서·스킬·검증을 찾는다.

## 14. 로컬과 GitHub

GitHub와 로컬 파일은 자동 양방향 동기화가 아니다.

- 작업 전 원격·로컬 상태를 확인한다.
- 로컬 변경은 검증 후 commit·push한다.
- 원격 변경은 fetch·pull한다.
- Workflow 파일 존재와 실제 실행·Required Check 강제를 구분한다.
- 생성 실패나 미검증 바이너리를 자동 push하지 않는다.

## 15. 완료 보고

- 주 책임·영향 분야
- 변경한 JSON·코드·자산·스킬
- 생성한 DOCX·PDF·다이어그램·Manifest
- 유지한 기존 결정·동작·자산
- 실행한 검증과 결과
- 미검증·불일치·남은 위험
- 보존·통합·백업·보류·제거 후보
- 콜드 스타트 결과
- Base 환류와 다음 작업

실행하지 않은 테스트, 렌더링, 구현, 브랜치 보호를 완료로 보고하지 않는다.
