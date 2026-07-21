# Base Skill System Optimization Report

## Scope and boundary decision

사용자가 제공한 1,201줄 학습 텍스트와 기존 활성 Skill 16개의 책임을 대조했다. 개념마다 파일을 만들지 않고 독립 입력·산출물·권한·검증 경계가 있는 책임만 9개 Skill로 분리했다.

요청 명세화·Issue/Goal·작업 분해, 플레이어 경험·벤치마킹·MVP·PoC, 문서 기억·컨텍스트 압축, 변경 검증은 기존 Skill에 이미 책임이 있어 중복 신설하지 않았다. 전체 매핑은 `skills/SKILL_COVERAGE.json`과 `docs/SKILL_COVERAGE_MAP.md`가 책임진다.

## New independent skills

- 구조 최적화: `pruning-stale-and-nonfunctional-material`, `simplifying-skill-bodies`, `refactoring-with-contract-preservation`.
- 작업 운영: `synchronizing-local-and-github-state`, `maintaining-long-running-task-continuity`.
- 기획·연구·학습: `governing-game-user-research-coverage`, `creating-user-learning-notes`.
- 전문 산출물·디버깅: `building-project-visual-dashboards`, `diagnosing-game-engine-runtime-failures`.

모든 새 Skill은 `load_by_default=false`이며 trigger·사용·비사용 조건을 가진다.

## Applied pruning

- 프로젝트 코어·적대적 검토·Skill 진화·게임 컨셉 Skill의 반복 설명과 상시 호출에 불필요한 상세 판정표를 본문에서 제거했다.
- 임시 적용 Workflow와 생성 스크립트는 결과 커밋에서 제거했다.
- 기존 책임이 있는 요청 명세화·MVP·벤치마킹·문서 기억·검증 Skill을 중복 생성하지 않았다.

## Applied simplification

다음 5개 기존 `SKILL.md`를 목적·권한 경계·mode·필수 입력·핵심 흐름·출력·품질 게이트 중심의 compact router로 재작성했다.

- `identifying-project-core`
- `establishing-project-core`
- `running-adversarial-review-and-refinement`
- `evolving-project-discipline-skills`
- `analyzing-and-refining-game-concepts`

상세 분류·상태 전이·공격 렌즈·Health Review·컨셉/PoC/DDD/플레이테스트 계약은 각 패키지의 명시적으로 연결된 `references/`로 이동했다.

## Applied refactoring

- 코어 판정의 읽기 전용 권한, 코어 확정의 사용자 승인 게이트, 적대적 검토의 공격→비판 검증→최소 개선→회귀 순서를 보존했다.
- 게임 컨셉 Skill의 BIG BLIND, SWOT·MDA/DDE/DDD, 벤치마크, 플레이테스트, PoC, Production gate를 패키지 안에 보존했다.
- Skill 진화는 생성·통합·등록·Health Review 오케스트레이션을 유지하고 가지치기·본문 간소화·행동 보존 구조 변경을 독립 Skill로 위임했다.
- 새 Skill 사이의 오라우팅을 막기 위해 기존 검증·문서·Learning Log·Git·인수인계 책임과의 경계를 명시했다.

## Adversarial findings and fixes

첫 회귀 검사에서 게임 컨셉 Skill 본문 압축으로 인해 mode 발견성, DDD 상세 경계, 플레이테스트 필드, 기존 상세 reference 연결을 본문만 읽는 테스트가 찾지 못하는 문제가 드러났다.

다음과 같이 수정했다.

- 빠진 세부 계약을 삭제하지 않고 조건부 reference에 복구했다.
- mode와 reference 읽기 조건을 compact body에서 명시했다.
- 테스트를 본문 한 파일이 아니라 `SKILL.md + references` 전체 패키지의 기능 계약을 검증하도록 변경했다.
- 코어·승인·적대적 검토·Skill 진화·게임 컨셉의 기존 고유 용어와 상태가 남아 있는지 no-loss 회귀 테스트를 추가했다.
- 새 checker와 no-loss 테스트를 임시 Workflow가 아니라 상시 PR Workflow의 경로 감지·문법 검사·회귀 실행에 편입했다.

## No-loss controls

- `skills/SKILL_COVERAGE.json`: 원문 책임 18개를 활성 Skill에 매핑한다.
- `tools/check_skill_system_coverage.py`: coverage 상태·ACTIVE target·Registry·파일·front matter·compact body·임시 파일 잔존을 검사한다.
- `tests/test_skill_system_coverage.py`: 새 9개 Skill의 독립성·선택적 호출, GUR 11영역, 기존 5개 Skill의 고유 기능 보존을 검사한다.
- 기존 구조·Registry·reference·정본 최신성·문서 발행 회귀 테스트와 Windows smoke test를 함께 실행한다.

## Result and remaining evidence

활성 Skill은 16개에서 25개로 증가했다. 새 Skill 수는 원문 제목 수가 아니라 책임 경계로 제한했으며, 전체 skills 폴더를 기본 로드하지 않는다.

저장소 구조와 자동 검증은 Base 자체 적용 증거다. 새 Skill의 여러 실제 프로젝트 반복 사용 결과가 쌓이기 전까지 Registry 지식 상태는 `HYPOTHESIS`로 유지한다.
