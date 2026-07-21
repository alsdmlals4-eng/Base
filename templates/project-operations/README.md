# 게임 프로젝트 운영체계 템플릿 키트

이 폴더는 Base 실행 Skill이 대상 프로젝트에 맞게 **분화해 설치**하는 공용 템플릿이다. 폴더 전체와 예시 경로를 그대로 복사하지 않는다.

## 사용 Skill

- 요청 라우팅·요구 확정·실행 계약: `skills/managing-project-intake-and-work-contract/SKILL.md`
- 신규 설치·기존 감사·승인된 마이그레이션·Health Review: `skills/managing-game-project-operating-system/SKILL.md`
- 기획 책임 원본 작성·발행: `skills/managing-design-documents/SKILL.md`
- 분야별 프로젝트 Skill 통합·학습: `skills/evolving-project-discipline-skills/SKILL.md`
- Active Context·Handoff: `skills/maintaining-project-context-and-handoff/SKILL.md`
- 프로젝트 교훈·Base 제안: `skills/managing-base-change-proposals/SKILL.md`

통합 전 ID는 `skills/LEGACY_SKILL_ALIASES.md`로 새 Skill과 mode에 연결한다.

## Base 기준 버전

```text
프로젝트에 동기화된 Base 기준 우선
→ docs/BASE_RULES_VERSION.md의 커밋 확인
→ 업데이트 조사 때만 Base 원격과 비교
```

프로젝트 작업 중 원격 Base의 최신 상태를 암묵적으로 적용하지 않는다.

## 가장 중요한 위치 규칙

신규 설치와 승인된 마이그레이션의 활성 기획서는 저장소 루트 바로 아래에 둔다.

```text
<repository-root>/[기획서]/
```

기존 프로젝트의 안정된 기획 폴더는 `audit`와 사용자 승인 없이 강제 이동하지 않는다.

## 템플릿 목록

### 프로젝트 허브

| 파일 | 역할 |
|---|---|
| `PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` | 신규 설치 계획 |
| `EXISTING_PROJECT_MIGRATION_AUDIT.md` | 기존 프로젝트 보존·참조 감사 |
| `PROJECT_START_HERE.md` | 사용자·새 AI용 대시보드 |
| `ACTIVE_CONTEXT.md` | 현재 상태의 기본 원본 |
| `HANDOFF.md` | 세션·담당자·브랜치·마일스톤 경계 스냅샷 |
| `ROADMAP.md` | 단계·우선순위·선행 조건·종료 기준 |
| `DECISION_LOG.md` | 결정·근거·재검토 조건 |
| `CHANGELOG.md` | 프로젝트 변경·검증·미검증 |
| `BASE_RULES_VERSION.md` | 적용 Base 커밋·동기화 차이 |
| `PROJECT_DOCUMENTATION_MAP.md` | 질문별 책임 원본·Skill·검증 라우터 |
| `INTERVIEW_REGISTRY.json` | 사용자 확인과 실행 계약 연결 |
| `INTERVIEW_RECORD.md` | 사실·결정·모호성·확인 기록 |
| `DEVELOPMENT_GATES.md` | 작업·제품 게이트 |
| `DOCUMENT_UPDATE_MATRIX.md` | 변경 유형별 갱신 책임 |
| `AI_WORKFLOW.md` | GPT·Codex·GitHub 흐름 |
| `LIFECYCLE_AREAS.md` | 현행·백업·보류·제거 후보 |
| `OPERATING_SYSTEM_HEALTH_REPORT.md` | `verify` 결과 보고 |

Active Context를 현재 상태의 기본 원본으로 사용한다. Handoff는 두 번째 활성 상태 원본으로 유지하지 않는다.

### 기획 책임 원본·Skill

| 파일 | 역할 |
|---|---|
| `DESIGN_DOCUMENT.md` | 서술 중심 Markdown 원본 템플릿 |
| `DESIGN_DOCUMENT.json` | 구조 검증·게임 데이터 JSON 원본 템플릿 |
| `DESIGN_DOCUMENT_REGISTRY.json` | 문서 ID·책임·원본·발행 정책 |
| `SKILL_REGISTRY.json` | 선택적 Skill 라우팅·상태·학습 |
| `PROJECT_SKILL_MAP.pdf` | 설정한 경우의 사람용 Skill Map |
| `PROJECT_SKILL_MAP.md/.docx/.assets` | 선택 파생본 |
| `SKILL_MAP_PUBLICATION_MANIFEST.json` | Skill Map 입력·출력·검수 상태 |
| `skills/FOUNDATION_SKILL.md` | 공용 실행 계약 템플릿 |
| `skills/DISCIPLINE_SKILL.md` | 분야 고유 판단·경로·검증 템플릿 |
| `skills/SKILL_LEARNING_LOG.md` | 실패·중요 결정·재사용 교훈·검증 기록 |

11개 분야는 선택 가능한 카탈로그다. 프로젝트에 필요하지 않은 분야를 강제로 설치하지 않는다.

## 발행 정책

각 문서는 Registry에서 하나를 선택한다.

- `source_only`: 운영·라우팅 문서, PDF·DOCX·Manifest 없음
- `milestone_sync`: 주요 게이트·정기 검토·외부 공유 시 발행
- `always_sync`: 원본 변경과 같은 작업에서 상시 발행

정책 선택 도구:

```text
tools/build_policy_driven_design_documents.py
→ 항상 always_sync 선택
→ --include-milestone일 때 milestone_sync 포함
→ source_only는 생성 대상에서 제외
→ tools/build_design_documents.py로 안전 생성
```

DOCX·다이어그램은 선언한 경우만 생성한다. `CURRENT`, 자동 렌더, Codex 검수, 사용자 검수는 독립 상태다.

## GitHub 운영

| 파일 | 역할 |
|---|---|
| `github/ISSUE_TEMPLATE.yml` | 작업 계약 Issue Form |
| `github/PULL_REQUEST_TEMPLATE.md` | 게이트·책임 원본·검증 PR 체크 |
| `github/CODEOWNERS.example` | 분야별 리뷰 예시 |
| `github/documentation-governance.json` | 루트·Registry·Skill·발행 강제 설정 |
| `github/check_documentation_governance.py` | 링크·경로·갱신 검사 |
| `github/check_skill_routing_governance.py` | Registry·Learning·Skill Map 검사 |
| `github/check_design_document_publications.py` | 정책 기반 책임 원본·발행 검사 |
| `github/documentation-governance.yml` | GitHub Actions 예시 |

파일 존재, Workflow 실제 실행, Required Status Check 강제를 서로 다른 상태로 기록한다.

## 권장 대상 구조

```text
AGENTS.md
README.md
docs/BASE_RULES_VERSION.md

tools/
├─ build_project_skill_map.py
├─ build_policy_driven_design_documents.py
├─ build_design_documents.py
├─ publication_v3.py
└─ *_governance.py

[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ HANDOFF.md                  # 경계 스냅샷
│  ├─ ROADMAP.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DEVELOPMENT_GATES.md
│  ├─ DESIGN_DOCUMENT_REGISTRY.json
│  ├─ SKILL_REGISTRY.json
│  ├─ INTERVIEW_REGISTRY.json
│  ├─ INTERVIEWS/
│  ├─ EXECUTABLE_PROMPTS/
│  ├─ PROJECT_SKILL_MAP.*         # 설정한 경우
│  ├─ DOCUMENT_UPDATE_MATRIX.md
│  ├─ DECISION_LOG.md
│  ├─ CHANGELOG.md
│  └─ AI_WORKFLOW.md
└─ 선택한 분야 폴더/

skills/
├─ foundation/
└─ 선택한 분야/
```

## 설치 순서

### 신규 프로젝트

```text
managing-game-project-operating-system: install
→ 루트·허브·Registry·게이트 설치
→ 선택한 책임 원본·Skill 설치
→ 정책 기반 발행·Governance 연결
→ verify
```

### 기존 프로젝트

```text
managing-game-project-operating-system: audit
→ 고유 정보·참조·보존·위험 제안
→ 사용자 승인
→ 승인된 처리표만 migrate
→ verify
```

사용자 승인 전 대량 삭제·이동·통합을 하지 않는다.

## 완료 검수

- [ ] 루트 `[기획서]`와 최초 읽기 경로가 명확하다.
- [ ] 질문별 단일 Markdown 또는 JSON 책임 원본이 Registry에 등록됐다.
- [ ] 발행 정책과 출력·Manifest 계약이 일치한다.
- [ ] Skill Registry가 최소 호출과 mode를 연결한다.
- [ ] 이전 ID가 Legacy Alias로 변환된다.
- [ ] 실제 코드·데이터·자산·테스트가 책임 원본과 연결된다.
- [ ] Governance·Actions·Required Check의 실제 상태가 구분된다.
- [ ] Active Context가 실제 상태와 일치한다.
- [ ] 새 작업자가 저장소만으로 방향·상태·다음 작업·보호 범위를 찾는다.
