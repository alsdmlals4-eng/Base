# BCP-008 적대적 구현 검토

## 기준과 권한

- 제안: `BCP-2026-008-agentic-spec-design-ui-procurement-integration`
- 제안 PR: `#190`
- 구현 승인: `https://github.com/alsdmlals4-eng/Base/pull/190#issuecomment-5198050799`
- 구현 PR: `#192`
- 기준 main: `cabbc59b170c5da2bb1df7e4d4d535857dd35495`
- 병합 권한: `NOT_GRANTED`
- 신규 ACTIVE Skill: `0`

## 실패 가정

1. 새 문서가 기존 책임 원본과 경쟁해 이중 정본을 만든다.
2. L0·L1 작업까지 무거운 명세 Packet과 다중 관점 검토가 강제된다.
3. BMAD식 역할이 주 책임 Skill의 결정 권한을 침범한다.
4. `DESIGN.md`가 게임 규칙·UX 행동·Godot 상태 소유권까지 차지한다.
5. MCP 연결 또는 외부 Registry 조회를 코드 채택·설치·품질 통과로 과장한다.
6. taste 계열 미적 선호가 프로젝트 의도보다 높은 공용 규칙이 된다.
7. 테스트 파일만 추가되고 필수 CI에서는 실행되지 않는다.
8. Skill 본문 팽창·Registry 재발행·릴리스 잠금 변경이 발생한다.
9. 실제 모델 행동과 사람 UI 품질을 실행하지 않고 성능 향상으로 보고한다.

## TDD와 계약 검증

- RED HEAD: `181f11c055ee89128891734d682be5c49e586711`
- RED run: `31052965191`
- RED 결과: 기존 333개 통과, BCP-008 누락 계약 1개 예상 실패, 구성된 15개 skip
- GREEN 적용 run: `31055246563`
- 집중 BCP-008 테스트: `10 PASS`
- 결합 소비자·거버넌스 검사: `73 PASS`
- 통합 계약·패키지·최신성 검사: `90 PASS`
- Skill behavior coverage: `29/29 primary`, `29/29 non-selection`
- 독립 모델 실행: `NOT_RUN`
- Registry·released lock 변경: `0`

## 실제 외부 UI 조달 Pilot

공식 `shadcn-ui/ui` 원본과 배포 CLI를 구분해 검증했다.

```yaml
source_repository: shadcn-ui/ui
source_commit: b1c580c637f4666890b25c69cdc315c93a892c5d
source_registry_item: button
source_component_sha256: cc36af0f8b5019c33cc039fbf03bb952a513072b15b55b53c592b78af3e5f4c4
license: MIT
source_declared_cli_version: 4.16.2
source_declared_cli_publication: NOT_PUBLISHED_ETARGET
published_cli_version_used: 4.16.1
disposable_fixture: Vite Web project
init: PASS
add_button: PASS
build: PASS
generated_component_sha256: 9ce417985b97956fbb3a73c84b0eb60230fd0a9844c5111df92e061731440a3f
target_project_installation: NOT_RUN
browser_render_review: NOT_RUN
accessibility_review: NOT_RUN
human_quality_review: HUMAN_NOT_RUN
adoption_decision: BLOCKED_UNVERIFIED
```

조달 실행은 격리된 Web fixture에서 실제 성공했지만, Base 또는 게임 프로젝트에 설치하지 않았다. 따라서 공급 경로 동작은 증명하지만 프로젝트 적합성·접근성·시각 품질은 증명하지 않는다.

## 공격 결과와 판정

### MUST_FIX — 필수 CI가 신규 테스트를 발견하지 않음

- 원인: Base 필수 Workflow가 명시된 테스트 집합만 실행함.
- 수정: `tools/check_skill_system_coverage.py`와 UI 전용 Workflow에 BCP-008 계약·영수증 검증을 연결함.
- 회귀 결과: 누락 시 fail-closed, 구현 후 집중·거버넌스 검사 통과.

### MUST_FIX — source package 버전이 npm에 없음

- 관찰: 원본 commit의 `shadcn` 버전 `4.16.2`는 npm에서 `ETARGET`.
- 수정: source identity와 실제 published CLI identity를 분리하고 배포된 `4.16.1`로 Pilot 실행.
- 판정: 원본 자체 결함으로 단정하지 않고 `SOURCE_PACKAGE_VERSION_NOT_PUBLISHED`로 기록.

### MUST_FIX — CLI가 비대화형 실행 중 preset을 질문함

- 수정: 공식 preset `nova`와 `--no-monorepo`를 명시.
- 회귀 결과: init·button 조달·Vite build 통과.

### MUST_FIX — 새 package reference가 소유 Skill에서 연결되지 않음

- 초기 수정: UI Skill의 상세 방법 목록에 reference 두 개를 링크함.
- 후속 판정: 링크만으로도 Skill 본문 변경과 Registry 재발행이 결합되는 과도한 비용이 확인됨.
- 최종 수정: 두 계약을 기존 `ux-ui-design-system-method.md`의 `6.1`·`6.2`로 통합하고 별도 reference를 제거함.
- 검증: package integrity·reference freshness·UI 계약 검사 통과.

### SHOULD_FIX — UI Skill 본문과 별도 reference가 책임을 과분할함

- 수정: 시각 토큰 Adapter와 외부 UI 조달 Gate를 기존 UI 디자인 시스템 방법론에 흡수함.
- 결과: `auditing-and-refining-ui-art/SKILL.md`, `skills/SKILL_REGISTRY.json`, released lock은 기준 main과 동일함.
- 보호: 기능 계약·테스트·조달 영수증·행동 fixture는 유지함.

### REJECTED_CRITIQUE — 별도 Spec Kit/BMAD/DESIGN/shadcn/taste Skill 필요

독립 입력·산출물·승인 권한이 아니라 기존 owner의 mode·reference 확장이므로 신규 Skill은 과분할이다.

### BLOCKED_UNVERIFIED — 실제 모델 성능 향상

행동 fixture와 기계 계약은 강화됐지만 독립 모델 runner를 실행하지 않았다. 따라서 실제 모델의 라우팅 정확도·완성도 향상을 통과로 보고하지 않는다.

### BLOCKED_UNVERIFIED — 실제 게임 UI 품질

외부 조달은 disposable Web fixture에서만 실행했다. Godot 프로젝트 설치, 실제 화면 렌더, 입력·포커스, 접근성, 사람 품질 평가는 수행하지 않았다.

## 회귀 보호

- L0·L1에는 Traceability Packet과 전체 Lens를 강제하지 않는다.
- 교차 분야 Lens는 Finding만 만들며 결정을 소유하지 않는다.
- `GAME_UX_UI_SYSTEM.md`가 플레이어 경험·행동·상태 소유권을 유지한다.
- 프로젝트 `DESIGN.md`는 시각 토큰만 소유한다.
- Registry 접근, source admission, 설치 승인, build, 렌더, 접근성, 사람 품질을 서로 다른 Gate로 유지한다.
- MCP 연결 성공을 설치·채택·품질 통과로 사용하지 않는다.
- 외부 코드는 Base에 기본 설치하지 않는다.
- UI Skill 본문과 Registry·released lock은 baseline과 동일하게 유지한다.

## 현재 판정

```yaml
contract_and_routing_improvement: VERIFIED
existing_skill_boundary_preservation: VERIFIED
consolidated_contract_tests: PASS_90
focused_and_governance_tests: PASS
external_ui_source_acquisition: PASS
external_ui_disposable_build: PASS
external_ui_target_project_adoption: BLOCKED_UNVERIFIED
independent_model_behavior_improvement: NOT_RUN
human_ui_quality: HUMAN_NOT_RUN
registry_and_release_lock_change: NONE
merge_authorization: NOT_GRANTED
```

최종 exact-HEAD GitHub Actions 상태는 PR `#192`의 check suite를 권위 근거로 사용한다.
