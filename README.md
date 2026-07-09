# Base

공용 AI 작업 규칙의 원본 저장소다.

이 저장소는 특정 게임, 엔진, 세계관에 종속되지 않는 작업 방식과 템플릿을 보관한다.
각 프로젝트 저장소는 이 저장소의 문서를 로컬 사본으로 동기화하고, 프로젝트 전용 규칙은 해당 프로젝트 저장소에 별도로 둔다.

## 목적

- 새 프로젝트에서도 같은 작업 방식으로 시작한다.
- 새 AI나 Codex가 공통 규칙을 빠르게 이해한다.
- 공용 규칙과 프로젝트 전용 규칙을 섞지 않는다.
- Base 변경이 진행 중인 프로젝트 규칙을 갑자기 바꾸지 않도록 각 프로젝트에는 고정 사본을 둔다.

## 권장 구조

```text
Base
├─ README.md
├─ AGENTS.md
├─ docs/
│  ├─ AI_SHARED_WORK_RULES.md
│  ├─ AI_WORKFLOW_CHECKLIST.md
│  └─ CHANGELOG.md
└─ templates/
   ├─ AGENTS.project.md
   ├─ copilot-instructions.md
   ├─ mvp-feature.yml
   └─ pull_request_template.md
```

각 프로젝트 저장소 권장 구조:

```text
project-repo
├─ AGENTS.md
├─ docs/
│  ├─ AI_SHARED_WORK_RULES.md
│  ├─ BASE_RULES_VERSION.md
│  └─ CODEX_SHARED_WORK_RULES.md
└─ .github/
   └─ copilot-instructions.md
```

## 사용 방식

1. Base에서 공용 규칙을 수정한다.
2. Base 변경 내용을 검토한다.
3. 각 프로젝트 저장소에 필요한 문서를 로컬 사본으로 동기화한다.
4. 프로젝트 저장소의 `docs/BASE_RULES_VERSION.md`에 Base 기준 커밋 SHA와 동기화 날짜를 기록한다.
5. 프로젝트 전용 규칙은 프로젝트 저장소의 `AGENTS.md`, `docs/CODEX_SHARED_WORK_RULES.md`, `README.md`, `PROJECT_BRIEF.md`, `DESIGN_INTENT.md`, `MVP_ROADMAP.md`, `TEST_CHECKLIST.md`에 둔다.

## 버전 정책

- 공용 규칙 변경은 Base에서 먼저 한다.
- 프로젝트는 의도적으로 동기화한다.
- Base 문서를 링크만 걸지 말고 프로젝트 저장소에 로컬 사본을 둔다.
- 새 프로젝트가 늘어나 동기화가 번거로워지면 스크립트나 GitHub Action을 추가한다.

## 문서 구분

공용:

- `AGENTS.md`
- `docs/AI_SHARED_WORK_RULES.md`
- `docs/AI_WORKFLOW_CHECKLIST.md`
- `templates/`

프로젝트 전용:

- 프로젝트 저장소의 `AGENTS.md`
- 프로젝트 저장소의 `docs/CODEX_SHARED_WORK_RULES.md`
- 프로젝트 저장소의 `README.md`
- 프로젝트 저장소의 `PROJECT_BRIEF.md`
- 프로젝트 저장소의 `DESIGN_INTENT.md`
- 프로젝트 저장소의 `MVP_ROADMAP.md`
- 프로젝트 저장소의 `TEST_CHECKLIST.md`
- 프로젝트 저장소의 `data/`, `scripts/`, `scenes/`
