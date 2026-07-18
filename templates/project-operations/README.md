# 게임 프로젝트 운영체계 템플릿 키트

이 폴더는 Base 실행 스킬이 대상 프로젝트에 맞게 **분화해 설치**하는 공용 템플릿이다. 폴더 전체와 예시 경로를 그대로 복사하지 않는다.

## 사용 스킬

- 신규·미설치 프로젝트: `skills/installing-game-project-operating-system/SKILL.md`
- 기존 운영 프로젝트 재배치: `skills/migrating-existing-game-project-structure/SKILL.md`
- 분야별 프로젝트 스킬: `skills/evolving-project-discipline-skills/SKILL.md`
- 분야별 PDF 발행: `skills/publishing-discipline-bibles/SKILL.md`

## 템플릿 목록

### 프로젝트 허브·마이그레이션

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` | 신규 설치·Governance foundation 계획 |
| `EXISTING_PROJECT_MIGRATION_AUDIT.md` | 기존 프로젝트의 보존·참조·변경 전후 감사 |
| `PROJECT_START_HERE.md` | 사용자·새 AI가 보는 프로젝트 대시보드 |
| `PROJECT_DOCUMENTATION_MAP.md` | 질문·작업별 책임 원본·스킬·검증 라우터 |
| `DEVELOPMENT_GATES.md` | Ready·Implementation·Verification·Documentation·Completion과 마일스톤 Greenlight |
| `DOCUMENT_UPDATE_MATRIX.md` | 변경 유형별 필수 갱신 책임 |
| `AI_WORKFLOW.md` | GPT·Codex·GitHub 협업 흐름 |
| `LIFECYCLE_AREAS.md` | `[현행]`, `[백업]`, `[보류]`, `[제거 후보]` 운영 |

### 분야 본책·스킬

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `DISCIPLINE_BIBLE.md` | 분야별 활성 본책 공통 골격 |
| `PROJECT_SKILL_MAP.md` | Foundation·분야별 프로젝트 스킬 라우터 |
| `skills/FOUNDATION_SKILL.md` | 여러 분야가 공통 사용하는 실행 계약 |
| `skills/DISCIPLINE_SKILL.md` | 분야 고유 판단·실제 경로·검증 계약 |
| `skills/SKILL_LEARNING_LOG.md` | 관찰·가설·패턴·검증·승격 후보 학습 기록 |

### 이미지·PDF

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `VISUAL_SOURCE_OF_TRUTH.md` | 이미지 승인·일관성·실제 캡처 기준 |
| `ASSET_MANIFEST.yml` | 이미지·자산 상태와 캐노니컬 경로 |
| `DISCIPLINE_PDF_PUBLICATION.md` | 분야 전체 과정과 승인 이미지를 포함하는 PDF 발행 계획 |
| `PUBLICATION_MANIFEST.json` | PDF 입력·출력·해시·시각 검수·최신 상태 |

### GitHub 운영

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `github/ISSUE_TEMPLATE.yml` | 목표·분야·Ready·스킬·검증 Issue Form 예시 |
| `github/PULL_REQUEST_TEMPLATE.md` | 게이트·본책·스킬·Manifest·PDF·미검증 PR 체크 |
| `github/CODEOWNERS.example` | 분야별 문서·스킬·자동화 리뷰 예시 |
| `github/documentation-governance.json` | 필수 경로·변경 규칙·PDF 강제 수준 설정 |
| `github/check_documentation_governance.py` | 링크·파일명·자산·PDF·갱신 누락 검사기 |
| `github/documentation-governance.yml` | GitHub Actions 예시 |

## 권장 대상 구조

```text
AGENTS.md
README.md

[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DEVELOPMENT_GATES.md
│  ├─ PROJECT_SKILL_MAP.md
│  ├─ DOCUMENT_UPDATE_MATRIX.md
│  ├─ DECISION_LOG.md
│  ├─ CHANGELOG.md
│  ├─ AI_WORKFLOW.md
│  ├─ PUBLICATION_MANIFEST.json
│  └─ SOURCE_AUDIT.md
├─ 01_설정_내러티브/
├─ 02_게임_디자인/
├─ 03_UX_UI_접근성/
├─ 04_개발_엔지니어링/
├─ 05_테크니컬아트_파이프라인/
├─ 06_아트/
├─ 07_사운드/
├─ 08_QA/
├─ 09_프로덕션_PM/
├─ 10_분석_유저리서치/
└─ 11_통합검수/

skills/
├─ foundation/
├─ narrative/
├─ game-design/
├─ ux-ui-accessibility/
├─ engineering/
├─ technical-art/
├─ art/
├─ audio/
├─ qa/
├─ production/
├─ analytics-user-research/
└─ integrated-review/
```

프로젝트에 필요하지 않은 폴더를 억지로 만들지 않는다. 기존 경로가 동일 책임을 안정적으로 수행하면 유지하고 Documentation Map에서 연결한다.

## 책임 연결 계약

각 분야는 다음 경로를 제공한다.

```text
분야 진입 문서
→ 분야 활성 본책
→ 분야 프로젝트 스킬
→ 현재 Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산
→ 테스트·검수
→ 최신 PDF
```

여러 분야에서 공통으로 사용하는 절차는 foundation 스킬에 한 번만 둔다.

## 적용 규칙

1. 기존 저장소는 `Audit only`로 시작해 책임·참조·고유 정보를 먼저 확인한다.
2. 사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않는다.
3. 기존 경로가 같은 역할을 수행하면 유지한다.
4. 프로젝트 이름, 엔진, 실제 경로, 검증 명령과 팀 구조를 채운다.
5. 존재하지 않는 자동화·PDF·테스트를 설치 완료로 표시하지 않는다.
6. 기존 승인 이미지가 있으면 새 시안을 만들지 않고 Visual Source·Manifest에 등록한다.
7. Markdown을 책임 원본으로 사용하고 PDF·HTML·DOCX는 파생 열람본으로 둔다.
8. 분야 PDF는 전체 과정과 승인 이미지를 포함하고 Publication Manifest로 최신성을 추적한다.
9. GitHub 검사 템플릿은 실제 프로젝트 경로에 맞게 설정하고 정상·실패 시나리오를 테스트한다.
10. `[백업]`, `[보류]`, `[제거 후보]`는 기본 작업 컨텍스트에서 제외한다.

## 설치 상태 표기

| 상태 | 의미 |
|---|---|
| 설계됨 | 템플릿과 적용 계획만 존재 |
| 설치됨 | 프로젝트 파일과 실제 책임 원본 연결이 생성됨 |
| 실행 확인 | 실제 작업·PDF 빌드·PR에서 절차가 수행됨 |
| 강제됨 | 브랜치 보호의 Required Check·리뷰로 활성화됨 |
| 미검증 | 파일은 있으나 실제 실행·렌더링·보호 설정 미확인 |

GitHub Actions 파일이나 PDF 생성 계획이 존재한다는 사실만으로 `실행 확인` 또는 `강제됨`으로 기록하지 않는다.
