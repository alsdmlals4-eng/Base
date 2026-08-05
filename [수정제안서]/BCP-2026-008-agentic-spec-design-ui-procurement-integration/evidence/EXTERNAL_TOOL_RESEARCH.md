# 외부 도구 공식 원본 조사

- 조사일: `2026-08-06`
- 조사 목적: 외부 프레임워크를 Base에 복제하지 않고 재사용 가능한 고유 원리·안정성·라이선스·적용 경계를 판정한다.
- 증거 상한: 공식 문서가 설명하는 기능과 상태만 기록한다. 실제 Base 적용·모델 행동·런타임 품질은 `NOT_RUN`이다.

## 1. Superpowers

### 공식 원본

- Repository: `https://github.com/obra/superpowers`
- License: MIT
- 핵심 설명: composable Skill과 초기 지시로 구성된 소프트웨어 개발 방법론. 구현 전 대화로 요구를 뽑고 설계를 사용자에게 검토받은 뒤 계획·TDD·검증으로 진행한다.

### Base 판정

- Base intake·Grill Me·PLAN/BUILD/REVIEW·적대적 검토·검증과 책임이 대부분 중복된다.
- 공식 패키지나 Skill 원문을 Base에 복제하지 않는다.
- 신규 기능이 아니라 현재 Superpowers 절차를 실제 호출·증거와 함께 유지한다.

### 상태

`KEEP_EXISTING`

## 2. GitHub Spec Kit

### 공식 원본

- Repository: `https://github.com/github/spec-kit`
- Core flow: `constitution → specify → plan → tasks → implement`
- Optional quality flow: `clarify`, `checklist`, `analyze`
- 실행 전 prerequisites와 task dependency를 검사하고 로컬 CLI 명령을 실행할 수 있다.

### Base 판정

- Base의 기획·실행 계약·작업 분해·검증 생명주기와 전면 도입이 중복된다.
- 유용한 차이는 spec·plan·tasks·implementation 사이 consistency/coverage를 명시적으로 대조하는 점이다.
- CLI·Workflow를 설치하지 않고 L2 이상 Requirement traceability Packet만 기존 owner에 흡수한다.
- 외부 Workflow가 실행하는 shell·network·secret 요구는 별도 권한 검토 없이 허용하지 않는다.

### 상태

`ADAPT_TRACEABILITY_ONLY`

## 3. BMAD Method

### 공식 원본

- Workflow map: `https://docs.bmad-method.org/reference/workflow-map/`
- Agent reference: `https://docs.bmad-method.org/reference/agents/`
- 주요 Phase: Analysis, Planning, Solutioning, Implementation
- Quick Flow: 작은 잘 이해된 작업에서 앞 단계를 단축
- 기본 Agent 예: Analyst, Product Manager, Architect, Developer, UX Designer, Technical Writer

### Base 판정

- Named Agent를 모두 설치하면 Base의 주 책임 Skill 하나, 단일 정본, 최소 로딩 정책과 충돌한다.
- Agent 역할을 독립 권위로 만들지 않고 다분야 적대 검토 Lens로 변환한다.
- 작은 작업은 기존 L0/L1, 복잡 작업은 L2 이상 분해·검증을 사용해 BMAD의 Quick/Full 분기를 중복 구현하지 않는다.

### 상태

`ADAPT_AS_REVIEW_LENSES`

## 4. Google Labs DESIGN.md

### 공식 원본

- Repository: `https://github.com/google-labs-code/design.md`
- Specification: `https://github.com/google-labs-code/design.md/blob/main/docs/spec.md`
- License: Apache-2.0
- 현재 format version: `alpha`
- 구조: YAML front matter의 normative token과 Markdown body의 rationale
- 주요 token: colors, typography, rounded, spacing, components
- CLI 기능 예: lint, diff, token export

### Base 판정

- Base의 GAME_UX_UI_SYSTEM은 경험·흐름·상태·접근성·Godot 계약을 소유하지만 기계 판독 가능한 시각 token 정본은 약하다.
- 프로젝트 선택형 Adapter로 채택하되 Base 루트 전역 브랜드 파일로 만들지 않는다.
- alpha 형식은 exact source identity를 기록하고 자동 업그레이드하지 않는다.
- DESIGN.md는 UX·게임 규칙·상태 소유권을 대체하지 않는다.

### 상태

`ADOPT_AS_OPTIONAL_PROJECT_ADAPTER`

## 5. shadcn/ui Registry·MCP

### 공식 원본

- Introduction: `https://ui.shadcn.com/docs`
- Registry: `https://ui.shadcn.com/docs/registry`
- MCP: `https://ui.shadcn.com/docs/mcp`
- 설명: component library 패키지보다 수정 가능한 open code와 flat-file schema/CLI를 통한 code distribution platform
- MCP 기능: Registry 탐색·검색·설치, public/private/third-party Registry 지원
- Registry item은 component 외 config·rules·docs·automation도 배포할 수 있다.

### Base 판정

- Godot UI를 대체하지 않는다.
- Web surface 또는 범용 config·rule 배포에만 선택적으로 사용한다.
- MCP 연결 성공과 code adoption 승인을 분리한다.
- Registry source, exact version/commit, hash, item license, dependency, script, secret, overwritten file, rollback을 설치 전에 기록한다.
- shadcn/ui 자체 라이선스와 개별 Registry item·font·icon·asset 라이선스를 별도로 검증한다.

### 상태

`OPTIONAL_PROCUREMENT_ADAPTER`

## 6. taste-skill

### 공식 원본

- Repository: `https://github.com/leonxlnx/taste-skill`
- License: MIT
- 기본 `design-taste-frontend` v2는 `experimental`
- 주요 개념: brief inference, Design Read, DESIGN_VARIANCE, MOTION_INTENSITY, VISUAL_DENSITY, anti-slop, pre-flight
- 여러 Web stack·font·icon·motion 구현에 대한 강한 선호 또는 금지 규칙을 포함한다.

### Base 판정

- 원문을 Base 공용 규칙으로 복제하지 않는다.
- Design Read, density/motion profile, generic repetition 탐지, 실제 렌더 preflight만 프로젝트 의도·접근성 기준으로 변환한다.
- 특정 font·icon·React·Tailwind 선호와 고정 dial baseline은 프로젝트 전용 또는 기각 대상으로 둔다.
- experimental 상태이므로 원격 최신본 자동 동기화를 금지한다.

### 상태

`EXTRACT_QUALITY_LENS_ONLY`

## 7. getdesign.md

### 공식 원본

- About: `https://getdesign.md/about`
- Terms: `https://getdesign.md/terms`
- 설명: 공개 웹사이트의 시각 패턴을 독립 분석한 DESIGN.md directory
- 명시된 한계: 해당 회사의 공식 문서나 보증이 아니며 reference/start point이다.
- Terms는 브랜드 사칭, 로고·상표·사진·저작물 복제, 소비자 혼동을 금지한다.

### Base 판정

- `REFERENCE_ONLY_WITH_PROVENANCE`
- 공식 브랜드 정본으로 표시하지 않는다.
- 채택한 일반 원리, 변환 축, 기각 요소, 상표·자산 제한, 확인일을 기록한다.
- 프로젝트 결과는 원본 브랜드와 혼동되지 않는 독립 표현이어야 한다.

## 8. 라이선스·복제 정책

이번 BCP는 외부 코드·Skill 원문·Template을 복사하지 않고 일반 작업 원리와 경계만 독립적으로 재작성한다.

| 원본 | 확인 라이선스·상태 | Base 처리 |
|---|---|---|
| Superpowers | MIT | 기존 실행 방법론 유지, 원문 복제 없음 |
| Spec Kit | 공식 GitHub 프로젝트 | traceability 개념만 독립 계약화 |
| BMAD | 공식 Docs | 역할을 검토 Lens로 변환 |
| DESIGN.md | Apache-2.0, alpha | 선택형 Adapter와 source identity |
| shadcn/ui | Open Code 플랫폼 | 외부 조달 Gate, item별 별도 검증 |
| taste-skill | MIT, v2 experimental | 품질 Lens만 독립 재작성 |
| getdesign.md | 독립 분석 directory | provenance 있는 참고 자료만 허용 |

## 9. 구현 전 재확인 조건

외부 도구의 기능·형식·라이선스는 변경될 수 있다. 승인된 구현 PR 시작 시 각 공식 URL, exact release/tag/commit, license, breaking change를 다시 확인한다.
