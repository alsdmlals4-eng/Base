# 게임 프로젝트 운영체계 템플릿 키트

이 폴더는 `skills/installing-game-project-operating-system/SKILL.md`가 대상 프로젝트에 맞게 **분화해 설치**하는 공용 템플릿이다. 폴더 전체를 그대로 복사하지 않는다.

## 템플릿 목록

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` | 최초 감사·이관·설치 Work Order |
| `PROJECT_START_HERE.md` | 사용자가 보는 프로젝트 대시보드 |
| `DISCIPLINE_BIBLE.md` | 분야별 활성 본책 공통 골격 |
| `DOCUMENT_UPDATE_MATRIX.md` | 변경 유형별 필수 갱신 책임 |
| `AI_WORKFLOW.md` | GPT·Codex·GitHub 협업 흐름 |
| `VISUAL_SOURCE_OF_TRUTH.md` | 이미지 승인·일관성·실제 캡처 기준 |
| `ASSET_MANIFEST.yml` | 이미지·자산 상태와 캐노니컬 경로 |
| `github/PULL_REQUEST_TEMPLATE.md` | 영향 분야·문서·검증 PR 체크 |
| `github/ISSUE_TEMPLATE.yml` | 작업 요청 구조화 Issue Form 예시 |
| `github/documentation-governance.json` | 자동 검사 경로·갱신 규칙 설정 |
| `github/check_documentation_governance.py` | 문서·이미지·변경 영향 검사기 |
| `github/documentation-governance.yml` | GitHub Actions 예시 |

## 권장 대상 구조

```text
[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DOCUMENTATION_SYSTEM_POLICY.md
│  ├─ DOCUMENT_UPDATE_MATRIX.md
│  ├─ DECISION_LOG.md
│  ├─ CHANGELOG.md
│  ├─ MILESTONE_GATES.md
│  ├─ GLOSSARY.md
│  ├─ AI_WORKFLOW.md
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
```

프로젝트 규모가 작으면 분야 문서를 통합할 수 있다. 예를 들어 `QA·프로덕션`을 한 폴더에서 별도 장으로 관리하거나 `테크니컬 아트`를 아트와 개발의 공동 계약 장으로 둘 수 있다. 책임과 변경 매트릭스는 삭제하지 않는다.

## 적용 규칙

1. 기존 저장소를 감사하고 현재 책임 원본을 먼저 확인한다.
2. 기존 경로가 안정적으로 같은 역할을 수행하면 유지한다.
3. 프로젝트 이름, 엔진, 실제 경로, 검증 명령과 팀 구조를 채운다.
4. 존재하지 않는 자동화·열람본·테스트를 설치 완료로 표시하지 않는다.
5. 기존 승인 이미지가 있으면 새 시안을 만들지 않고 Manifest에 등록한다.
6. Markdown을 책임 원본으로 사용하고 PDF·HTML·DOCX는 파생 열람본으로 둔다.
7. GitHub 검사 템플릿은 프로젝트 경로에 맞게 설정한 뒤 테스트한다.

## 설치 상태 표기

| 상태 | 의미 |
|---|---|
| 설계됨 | 템플릿과 적용 계획만 존재 |
| 설치됨 | 프로젝트 파일과 연결이 생성됨 |
| 실행 확인 | 실제 작업·PR에서 절차가 수행됨 |
| 강제됨 | 브랜치 보호의 필수 검사로 활성화됨 |
| 미검증 | 파일은 있으나 실제 실행 또는 보호 설정 미확인 |

GitHub Actions 파일이 존재한다는 사실만으로 `강제됨` 상태로 기록하지 않는다.
