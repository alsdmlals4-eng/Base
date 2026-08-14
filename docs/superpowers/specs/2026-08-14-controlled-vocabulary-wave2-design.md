# Base Controlled Vocabulary Wave 2 Design

## 상태

- 승인 근거: 2026-08-14 사용자의 1차 용어집 병합 후 직접 `좋아 진행해`
- 기준 main: `6256a6bd88fad4b380f5b7dac06013b51a20b1e2`
- 변경 등급: L1 공용 용어 계약 확장
- Existing Solution First: `ABSORB`
- 신규 ACTIVE Skill·Work Mode·Skill Mode·Schema·실행 Framework: 추가하지 않음

## 목표

이미 병합된 `docs/CONTROLLED_VOCABULARY.md`를 두 번째 용어군으로 확장한다. 초보 개발자가 프로젝트 관리, 출시 단계, 테스트, 유지보수, Git/versioning에서 자주 혼동하는 용어를 한 단계로 찾게 하되, 외부 표준과 조직별 관행과 Base-local alias를 구분한다.

## 범위

### 프로젝트 관리·작업 단위

- Milestone
- Sprint
- Product Backlog
- Backlog
- Epic
- User Story

### 출시 단계·배포 상태

- Alpha
- Beta
- Early Access
- 기존 Release Candidate와의 관계
- Gold / Gold Master

### 테스트 범위·목적

- Component / Unit Test
- Integration Test
- End-to-End / E2E Test
- Smoke Test
- Sanity Test
- User Acceptance Testing / UAT
- Regression Testing
- 기존 Base-local `Regression Recheck`

### 코드 유지보수

- Code Smell
- Technical Debt
- Refactor
- Rewrite

### Git·버전 관리

- Branch
- Merge
- Rebase
- Cherry-pick
- Hotfix
- Semantic Versioning / SemVer

## 핵심 설계 경계

### Scrum과 일반 작업 관리

Scrum Guide가 직접 정의하는 `Sprint`, `Product Backlog`와 일반 현업에서 널리 쓰이는 `Milestone`, `Backlog`, `Epic`, `User Story`를 같은 표준성으로 다루지 않는다.

```text
Sprint ≠ Milestone
Product Backlog ≠ 모든 Backlog
Epic과 User Story는 Scrum Guide의 필수 Artifact가 아니다.
User Story ≠ 전체 명세
```

User Story는 대화와 상세화의 출발점일 수 있지만 Acceptance Criteria, 상세 요구, UX·데이터·오류·검증 계약을 자동 포함하지 않는다.

### 출시 상태

Alpha/Beta/Gold는 조직별 경계가 큰 `INDUSTRY_COMMON`으로 둔다. 프로젝트는 실제 Entry/Exit Criteria와 대상 사용자, 콘텐츠·안정성 범위를 별도로 고정한다.

Early Access는 내부 품질 단계 하나가 아니라 플랫폼 정책이 결합되는 배포·상업 상태가 될 수 있으므로 Alpha/Beta와 같은 축으로 강제하지 않는다.

```text
Early Access ≠ Beta
Early Access ≠ Pre-Purchase
Gold / Gold Master ≠ Release Candidate
```

### 테스트

테스트 이름은 테스트 파일의 크기나 실행 시간보다 검증 경계·목적·수용 주체를 우선한다.

`Smoke`와 `Sanity`는 조직별 편차가 큰 표현이므로 Base가 세계 공통 절대 정의를 만들지 않는다. 반면 `Regression Recheck`는 Base의 적대적 검토 절차를 부르는 `BASE_LOCAL_ALIAS`이므로 일반 `Regression Testing` 전체와 분리한다.

```text
UAT ≠ 일반 QA
Regression Testing ≠ Regression Recheck
Smoke PASS ≠ 전체 Regression PASS
```

### 유지보수

Code Smell은 조사 신호이지 버그나 Technical Debt의 확정 판정이 아니다. Technical Debt는 미래 변경·검증·운영 비용과 위험이 누적된 상태를 뜻한다.

Refactor는 외부 관찰 가능한 동작·계약 보존을 전제로 하고, Rewrite는 기존 구현의 상당 부분을 대체하는 새 구현 계보다. Rewrite가 같은 목표를 가진다는 이유만으로 기존 테스트·런타임 Evidence를 자동 승계하지 않는다.

```text
Code Smell ≠ Bug / Technical Debt 확정
Refactor ≠ Rewrite
```

### Git과 versioning

Git primitive와 팀 운영 라벨을 분리한다.

```text
Rebase ≠ Merge
Cherry-pick ≠ Branch Merge
Hotfix ≠ Git 명령
```

SemVer는 `X.Y.Z` 모양 자체가 아니라 선언된 public API와 그 호환성 의미를 전제로 한다. 게임 스토어 버전, 내부 build number, save schema, protocol version이 같은 축이어야 한다고 강제하지 않는다.

## ADOPT / ADAPT / AVOID

| 외부 근거 | 판정 | Base 적용 |
|---|---|---|
| Scrum Guide | `ADOPT` | Sprint·Product Backlog의 공식 Scrum 문맥과 Artifact 경계를 보존한다. |
| Steam Early Access 문서 | `ADAPT` | Early Access를 미완성 플레이 가능 제품의 배포 상태로 구분하되 모든 플랫폼의 동일 정책으로 일반화하지 않는다. |
| ISTQB Glossary / CTFL | `ADOPT/ADAPT` | 테스트 공통 언어의 권위 있는 참고축으로 사용하되 Smoke/Sanity의 조직 편차는 별도 표시한다. |
| Git 공식 문서 | `ADOPT` | Branch/Rebase/Cherry-pick 등 Git operation 의미를 팀 workflow 라벨과 분리한다. |
| Semantic Versioning 2.0.0 | `ADOPT` | public API 전제가 없는 `X.Y.Z`를 SemVer라고 과장하지 않는다. |
| Alpha/Beta/Gold의 고정 퍼센트 모델 | `AVOID` | 조직별 Entry/Exit Criteria 없이 50%/80% 같은 보편적 완성도로 고정하지 않는다. |

## 구현 범위

### 수정

- `docs/CONTROLLED_VOCABULARY.md`
- `tests/test_controlled_vocabulary_contract.py`
- `docs/CHANGELOG.md`

### 생성

- `docs/superpowers/specs/2026-08-14-controlled-vocabulary-wave2-design.md`
- `docs/superpowers/plans/2026-08-14-controlled-vocabulary-wave2.md`

### 보호

- `AGENTS.md`
- `START_HERE.md`
- `docs/DOCUMENTATION_MAP.md`
- `skills/**`
- `skills/SKILL_REGISTRY.json`
- `schemas/**`
- `.github/workflows/**`
- released lock·frozen/generated release artifact
- 프로젝트 코드·데이터·Scene·Resource·자산

Wave 1에서 이미 발견성과 CI consumer가 연결됐으므로 Wave 2는 같은 정본과 같은 semantic regression을 확장한다. 새 route나 새 test consumer를 만들지 않는다.

## TDD 계약

### RED

semantic regression에 다섯 용어군과 핵심 금지 경계를 먼저 추가한다. 현재 용어집에서 정확히 새 다섯 test가 실패하고 기존 용어 계약은 통과해야 한다.

실제 RED receipt:

- commit: `9c4a4385032138f53fe66735362a9da98b41a4a2`
- PR: `#347`
- Game Project OS run: `31762443963`
- `ubuntu-contract`: FAILURE
- contract regression: `420 tests`, `5 failures`, `15 skipped`
- 실패 원인: `Milestone`, `Alpha`, `Component / Unit Test`, `Code Smell`, `Branch` 누락
- 기존 Wave 1 vocabulary tests: PASS

### GREEN

정본에 각 용어의 Class, 압축 정의, 금지 의미, 혼동 방지를 최소 추가하고 동일 regression을 통과시킨다.

## 적대적 검토 MUST_FIX

- Epic/User Story를 Scrum 필수 Artifact로 보고하는가
- Sprint를 일반 1~2주 deadline이나 Milestone과 동일시하는가
- Alpha/Beta를 고정 완성도 퍼센트로 제시하는가
- Early Access를 Beta·Pre-Purchase·Crowdfunding과 동일시하는가
- Gold를 RC와 동일시하는가
- Smoke/Sanity를 조직 무관 절대 정의로 고정하는가
- UAT를 모든 QA의 동의어로 쓰는가
- Regression Testing과 Base Regression Recheck를 합치는가
- Code Smell을 Bug/Debt 확정으로 승격하는가
- Refactor에 의도적 외부 동작 변경을 숨기는가
- Rewrite를 큰 Refactor로 낮춰 기존 Evidence를 자동 승계하는가
- Rebase를 Merge와 같은 operation으로 설명하는가
- Cherry-pick을 Branch merge로 설명하는가
- Hotfix를 Git 명령/객체로 설명하는가
- public API 없이 `X.Y.Z`만 보고 SemVer 준수를 주장하는가

## 완료 기준

1. 다섯 용어군이 기존 Controlled Vocabulary 안에서 한 단계로 검색된다.
2. 표준 문맥·현업 공통·Base-local alias 경계가 유지된다.
3. 다섯 새 semantic regression과 기존 회귀가 exact PR HEAD에서 PASS한다.
4. 새 Skill/Registry/Schema/route/workflow가 생기지 않는다.
5. 같은 Goal·동시 PR path overlap을 재검사한다.
6. P0/P1 0, unresolved review thread 0, current-main freshness를 확인한다.
7. reviewed exact HEAD만 squash merge한다.
8. merge SHA가 새 main이고 post-merge semantic/CI readback이 PASS한다.

## 롤백

단일 squash merge를 revert한다. 런타임·Schema·Registry·프로젝트 데이터 마이그레이션이 없으므로 용어 정본·회귀·기록만 함께 되돌린다.
