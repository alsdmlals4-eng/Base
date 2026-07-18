# 게임 프로젝트 운영체계 템플릿 키트

이 폴더는 Base 실행 스킬이 대상 프로젝트에 맞게 **분화해 설치**하는 공용 템플릿이다. 폴더 전체와 예시 경로를 그대로 복사하지 않는다.

## 사용 스킬

- 작업 분야·최소 스킬 라우팅: `skills/routing-project-work-by-discipline/SKILL.md`
- 신규·미설치 프로젝트: `skills/installing-game-project-operating-system/SKILL.md`
- 기존 운영 프로젝트 재배치: `skills/migrating-existing-game-project-structure/SKILL.md`
- 분야별 프로젝트 스킬: `skills/evolving-project-discipline-skills/SKILL.md`
- Active Context·Handoff: `skills/maintaining-project-context-and-handoff/SKILL.md`
- 분야별 PDF 발행: `skills/publishing-discipline-bibles/SKILL.md`
- 운영체계 Health Review: `skills/verifying-game-project-operating-system/SKILL.md`

## Base 기준 버전 확인 순서

```text
프로젝트에 동기화된 Base 기준 우선
→ docs/BASE_RULES_VERSION.md의 커밋 확인
→ 업데이트를 조사할 때만 Base 원격과 비교
```

프로젝트 작업 중 원격 Base의 최신 상태를 매번 암묵적으로 적용하지 않는다. 프로젝트가 승인해 기록한 Base 커밋과 프로젝트별 차이가 재현 가능한 기준이다.

## 가장 중요한 위치 규칙

`[기획서]`는 사용자가 저장소를 열었을 때 바로 찾을 수 있도록 **저장소 루트 바로 아래**에 둔다.

```text
<repository-root>/[기획서]/
```

다음 위치는 사용하지 않는다.

```text
docs/[기획서]/
project/docs/[기획서]/
src/[기획서]/
```

기존 프로젝트의 안정된 기획 폴더가 다른 이름이라면 감사와 사용자 승인 없이 강제 이동하지 않는다. 신규 설치와 승인된 마이그레이션의 기본 목표 위치는 루트 `[기획서]`다.

## 템플릿 목록

### 프로젝트 허브·마이그레이션

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `PROJECT_OPERATING_SYSTEM_INSTALLATION_PLAN.md` | 신규 설치·Governance foundation 계획 |
| `EXISTING_PROJECT_MIGRATION_AUDIT.md` | 기존 프로젝트의 보존·참조·변경 전후 감사 |
| `PROJECT_START_HERE.md` | 사용자·새 AI가 보는 프로젝트 대시보드 |
| `ACTIVE_CONTEXT.md` | 현재 목표·상태·다음 작업·위험을 연결하는 압축 라우터 |
| `HANDOFF.md` | 다음 작업자의 첫 행동과 미완료·보호 범위를 전달하는 인수 문서 |
| `ROADMAP.md` | 단계별 가치·진입·종료 기준과 현재 우선순위 |
| `DECISION_LOG.md` | 결정·근거·대안·재검토 조건 기록 |
| `CHANGELOG.md` | 프로젝트 변경·검증·미검증 기록 |
| `BASE_RULES_VERSION.md` | 적용 Base 커밋·동기화 날짜·프로젝트 차이 기록 |
| `PROJECT_DOCUMENTATION_MAP.md` | 질문·작업별 책임 원본·스킬·검증 라우터 |
| `DEVELOPMENT_GATES.md` | Ready·Implementation·Verification·Documentation·Completion과 마일스톤 Greenlight |
| `DOCUMENT_UPDATE_MATRIX.md` | 변경 유형별 필수 갱신 책임 |
| `AI_WORKFLOW.md` | GPT·Codex·GitHub 협업 흐름 |
| `LIFECYCLE_AREAS.md` | `[현행]`, `[백업]`, `[보류]`, `[제거 후보]` 운영 |
| `OPERATING_SYSTEM_HEALTH_REPORT.md` | 구조·스킬·PDF·자동화·콜드 스타트 검수 보고서 |

### 분야 본책·스킬

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `DESIGN_DOCUMENT.json` | 현재 JSON 기획 본책 공통 골격; schema v3에서 Markdown 기본 템플릿과 병행 |
| `DESIGN_DOCUMENT_REGISTRY.json` | 문서 ID·분야·경로·발행 상태 라우터 |
| `SKILL_REGISTRY.json` | AI가 판독하는 선택적 호출·상태·학습 책임 원본 |
| `PROJECT_SKILL_MAP.pdf` | 사람이 가장 먼저 보는 이미지 포함 최신 스킬맵 |
| `PROJECT_SKILL_MAP.docx` | PDF와 함께 자동 생성되는 문서 열람·검토본 |
| `PROJECT_SKILL_MAP.assets/` | 호출 흐름·분야 라우팅·상태 매트릭스 이미지 |
| `SKILL_MAP_PUBLICATION_MANIFEST.json` | Registry와 DOCX·PDF·이미지의 해시·검수 상태 |
| `skills/FOUNDATION_SKILL.md` | 여러 분야가 공통 사용하는 실행 계약 |
| `skills/DISCIPLINE_SKILL.md` | 분야 고유 판단·실제 경로·검증 계약 |
| `skills/SKILL_LEARNING_LOG.md` | 실패·중요 결정·재사용 가능한 교훈·검증 결과 기록 |

`PROJECT_SKILL_MAP.md`는 만들지 않는다. 스킬 정보는 `SKILL_REGISTRY.json`에서 편집하고 `tools/build_project_skill_map.py`로 DOCX·PDF와 다이어그램을 재생성한다.

### 이미지·PDF

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `VISUAL_SOURCE_OF_TRUTH.md` | 이미지 승인·일관성·실제 캡처 기준 |
| `ASSET_MANIFEST.yml` | 이미지·자산 상태와 캐노니컬 경로 |
| `DESIGN_DOCUMENT_REGISTRY.json` | 기획서별 책임 원본·PDF·자산·Manifest 경로 |
| `*_PUBLICATION_MANIFEST.json` | 기획서별 입력·출력·해시·렌더·사람 검수 상태 |
| `SKILL_MAP_PUBLICATION_MANIFEST.json` | 프로젝트 스킬맵의 Registry·DOCX·PDF·다이어그램 최신성 |

### GitHub 운영

| 파일 | 대상 프로젝트 역할 |
|---|---|
| `github/ISSUE_TEMPLATE.yml` | 목표·분야·Ready·스킬·검증 Issue Form 예시 |
| `github/PULL_REQUEST_TEMPLATE.md` | 게이트·본책·스킬·Manifest·PDF·학습·미검증 PR 체크 |
| `github/CODEOWNERS.example` | 분야별 문서·스킬·자동화 리뷰 예시 |
| `github/documentation-governance.json` | 루트 기획서·필수 경로·Skill Registry·스킬맵·분야 PDF 강제 설정 |
| `github/check_documentation_governance.py` | 링크·파일명·자산·분야 PDF·갱신 누락 검사기 |
| `github/check_skill_routing_governance.py` | Registry·분야 진입·Learning Log·스킬맵 파생본 검사기 |
| `github/documentation-governance.yml` | GitHub Actions 예시 |

## 권장 대상 구조

```text
AGENTS.md
README.md
docs/BASE_RULES_VERSION.md

tools/
├─ build_project_skill_map.py
└─ skill_map_diagrams.py

[기획서]/
├─ 00_프로젝트_허브/
│  ├─ START_HERE.md
│  ├─ ACTIVE_CONTEXT.md
│  ├─ HANDOFF.md
│  ├─ ROADMAP.md
│  ├─ DOCUMENTATION_MAP.md
│  ├─ DEVELOPMENT_GATES.md
│  ├─ SKILL_REGISTRY.json
│  ├─ PROJECT_SKILL_MAP.docx
│  ├─ PROJECT_SKILL_MAP.pdf
│  ├─ PROJECT_SKILL_MAP.assets/
│  │  ├─ skill-flow.png
│  │  ├─ discipline-routing.png
│  │  └─ skill-matrix.png
│  ├─ SKILL_MAP_PUBLICATION_MANIFEST.json
│  ├─ DOCUMENT_UPDATE_MATRIX.md
│  ├─ DECISION_LOG.md
│  ├─ CHANGELOG.md
│  ├─ AI_WORKFLOW.md
│  └─ SOURCE_AUDIT.md
├─ 01_설정_내러티브/          # 프로젝트가 선택한 분야만 설치
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

11개 분야는 공용 카탈로그다. 프로젝트에 필요하지 않은 폴더를 억지로 만들지 않는다. 선택한 분야마다 독립 진입 스킬 또는 명시적인 통합 책임을 둔다. 기존 경로가 동일 책임을 안정적으로 수행하면 감사·승인 후 유지할 수 있지만, 사용자가 찾는 활성 기획서 진입점은 루트에서 명확히 보여야 한다.

## 책임 연결 계약

각 분야는 다음 경로를 제공한다.

```text
분야 진입 문서
→ 분야 활성 본책
→ SKILL_REGISTRY의 분야 진입 스킬
→ 사람용 PROJECT_SKILL_MAP.pdf
→ 현재 Roadmap·Issue·Goal·Plan
→ 실제 코드·데이터·자산
→ 테스트·검수
→ 최신 분야 PDF
→ Learning Log
```

여러 분야에서 공통으로 사용하는 절차는 foundation 스킬에 한 번만 둔다.

## 사람용·AI용 스킬맵 경계

```text
AI·자동 검사 → SKILL_REGISTRY.json
사람의 빠른 열람 → PROJECT_SKILL_MAP.pdf
사람의 문서 검토 → PROJECT_SKILL_MAP.docx
그림 원본 확인 → PROJECT_SKILL_MAP.assets/
최신성 판정 → SKILL_MAP_PUBLICATION_MANIFEST.json
```

DOCX와 PDF는 독립 책임 원본이 아니다. 사람이 DOCX를 수정했더라도 Registry에 반영되지 않았다면 공식 변경으로 인정하지 않는다.

## 선택적 호출과 항상 학습

- 전체 skills 폴더를 기본 로드하지 않는다.
- `routing-project-work-by-discipline`가 현재 요청에 맞는 최소 스킬 집합을 선택한다.
- 활성 스킬도 `load_by_default=false`를 사용한다.
- 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있는 호출을 Learning Log에 기록한다.
- 스킬 본문은 반복 실패·새 예외·책임·경로·검증 변경이 있을 때만 갱신한다.
- 변경 근거가 없으면 `스킬 변경 없음`과 이유를 기록한다.
- Registry의 스킬·분야 진입·상태·호출 조건이 바뀌면 DOCX·PDF·다이어그램을 재생성한다.

## 적용 규칙

1. 기존 저장소는 `Audit only`로 시작해 책임·참조·고유 정보를 먼저 확인한다.
2. 사용자 승인 전 대량 삭제·이동·통합·강제 개명을 하지 않는다.
3. 신규·승인된 설치의 `[기획서]`는 저장소 루트 바로 아래에 둔다.
4. 기존 경로가 같은 역할을 수행하면 감사와 승인 후 유지한다.
5. 프로젝트 이름, 엔진, 실제 경로, 검증 명령과 팀 구조를 채운다.
6. 존재하지 않는 자동화·PDF·테스트를 설치 완료로 표시하지 않는다.
7. 기존 승인 이미지가 있으면 새 시안을 만들지 않고 Visual Source·Manifest에 등록한다.
8. 일반 기획서는 Markdown·구조화 데이터가 책임 원본이고 PDF·HTML·DOCX는 파생 열람본이다.
9. 프로젝트 스킬맵은 `SKILL_REGISTRY.json`이 책임 원본이며 DOCX·PDF·PNG와 선택적 Markdown 요약은 자동 생성 파생본으로만 사용한다.
10. 분야 PDF는 전체 과정과 승인 이미지를 포함하고 Publication Manifest로 최신성을 추적한다.
11. GitHub 검사 템플릿은 실제 프로젝트 경로에 맞게 설정하고 정상·실패 시나리오를 테스트한다.
12. `[백업]`, `[보류]`, `[제거 후보]`는 기본 작업 컨텍스트에서 제외한다.
13. 설치·마이그레이션·주요 게이트 후 운영체계 Health Review를 수행한다.
14. 작업에 필요한 도구·파일·폰트·인증·권한이 없으면 이유, 설치·적용·확인 방법과 최소 권한 범위를 사용자에게 요청하고, 완료 통보 후 실제 환경을 다시 확인한다.
15. 사용자 승인 없이 시스템 전역 설치·권한 확대·보안 또는 Branch protection 설정을 변경하지 않으며, 누락된 도구 때문에 건너뛴 검증을 통과로 표시하지 않는다.

## 설치 상태 표기

| 상태 | 의미 |
|---|---|
| 설계됨 | 템플릿과 적용 계획만 존재 |
| 설치됨 | 프로젝트 파일과 실제 책임 원본 연결이 생성됨 |
| 실행 확인 | 실제 작업·스킬 라우팅·학습 기록·DOCX/PDF 빌드·PR에서 절차가 수행됨 |
| 강제됨 | 브랜치 보호의 Required Check·리뷰로 활성화됨 |
| 미검증 | 파일은 있으나 실제 실행·렌더링·보호 설정 미확인 |

GitHub Actions 파일, Skill Registry 또는 DOCX/PDF 생성 계획이 존재한다는 사실만으로 `실행 확인` 또는 `강제됨`으로 기록하지 않는다.
