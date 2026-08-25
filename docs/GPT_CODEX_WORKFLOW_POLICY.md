# GPT–Codex 역할·구현 인계 정책

이 문서는 Base를 사용하는 게임 프로젝트에서 GPT와 Codex의 책임 경계를 정의하는 공용 정본이다.

핵심은 **Codex를 일반 GitHub 수정자나 모든 코드 파일의 담당자로 사용하지 않는 것**이다. Codex는 실제 게임 프로젝트의 Godot 제품 구현을 담당하고, 그 외 기획·검수·Notion·Base·문서·운영 정본은 GPT가 담당한다.

## 0. 현재 역할 계약

```text
GPT_NONCODING_PROJECT_OWNER
GPT_PLANNING_RESEARCH_REVIEW_VISUAL_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
PRODUCT_IMPLEMENTATION_HANDOFF_ONLY
CODEX_REHYDRATE_PROJECT_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_EXECUTION_ENVIRONMENT_FRESHNESS_REQUIRED
GPT_FINAL_IMPLEMENTATION_REVIEW
```

### 가장 중요한 구분

**GPT가 맡는다.**

- 게임 기획·조사·벤치마킹·시장/현업 비교
- 적대적 검토·Implementation Reality Gate
- 시스템·밸런스·데이터 설계와 사람용 표
- UI/UX·Flow·Storyboard·Art Direction
- 이미지 생성·편집·검수
- Notion Project Home / Domain / AI System 정리
- Base 정책·Skill·Guide·Template·Learning·문서 교정
- Base의 Registry/generated/계약 테스트/CI 정책 등 **공용 운영·검증 인프라** 교정
- GitHub의 비제품 문서·정본·운영 자료 교정
- Codex용 프로젝트 구현 작업지시문 작성
- Codex 결과 최종 검수와 Notion/GitHub 정본 반영

**Codex가 맡는다.**

- 실제 게임 프로젝트의 Godot 제품 구현
- GDScript 및 게임 실행 코드
- 실제 플레이에 사용되는 Scene / Resource / Autoload / runtime config
- 코드와 연결되는 runtime game data
- 저장·불러오기·migration의 제품 구현
- UI runtime wiring
- shader/VFX/code-driven feedback
- Godot build/export 설정
- 실제 게임 구현을 검증하는 automated/runtime/headless/play tests
- 구현 중 필요한 기술 리팩터링·오류 수정·성능/안정성 개선

`CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR`: **파일이 코드라는 이유만으로 Codex 담당이 되지 않는다.** Base의 Python test, CI contract, Registry/generated checker, 문서 자동화 같은 공용 운영 인프라는 이 작업 분담에서 GPT 책임이다. Codex는 게임 프로젝트의 제품/Godot 구현에만 기본 진입한다.

## 1. 기본 작업 흐름

```text
GPT
→ 프로젝트 GitHub + Notion 정본 복원
→ 최소 기획
→ 필요한 범위 벤치마킹·재사용 조사
→ 적대적 검토·IRG
→ 시스템 / 밸런스 / Flow / UI/UX / Visual / Acceptance 확정
→ 필요한 이미지 제작·검수·Notion 승인 전달
→ 비코딩 정본·문서·Notion 작업 완료

실제 Godot 제품 구현이 없음
→ GPT가 정본 readback 후 종료

실제 Godot 제품 구현이 있음
→ GPT가 프로젝트별 Codex 구현 작업지시문 작성
→ CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
→ Codex가 해당 프로젝트의 GitHub + Notion을 fresh-read
→ 실제 Godot 구조에 맞는 구현 방향·기술 방법 결정
→ Godot 제품 구현·코딩·테스트·runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ GPT가 기획 일치·회귀·증거·Visual 사용을 최종 검수
→ 필요 시 Codex에 REVISE 반환
→ 승인 후 병합·Notion/GitHub 정본 반영
```

## 2. GPT 책임

### 2.1 기획·비코딩 작업

GPT는 다음을 직접 수행하고 Codex에 넘기지 않는다.

- Base와 프로젝트의 Markdown 기획·정책·운영 문서
- Notion 생성·편집·표·데이터 정리·Flow·Visual 배치
- Base Skill/Guide/Template/Learning Log 교정
- Base Registry/generated/검증 계약·CI 정책과 그 paired test 유지보수
- 프로젝트 GDD·밸런스표·테크트리·병종·예산표·서사/설정·UX 명세
- 프로젝트의 비런타임 JSON/표/참고자료를 정본화하는 작업
- 문제→교훈 추출과 Base 승격
- 재사용 가능한 모듈/레퍼런스 조사와 채택 판단
- 이미지 제작·편집·검수와 승인 상태 관리

### 2.2 구현 준비

실제 게임 구현이 필요하면 GPT가 Codex에 다음을 전달한다.

```yaml
codex_work_instruction:
  project:
  repository:
  intended_player_outcome:
  approved_scope: []
  protected_scope: []
  acceptance_criteria: []
  notion_sources: []
  github_sources: []
  approved_visual_records: []
  required_runtime_or_play_checks: []
  forbidden_changes: []
  change_proposal_boundary: []
```

이 지시문은 구현 방법을 강제하는 스크립트가 아니다. **목표·승인 범위·보호 범위·Acceptance Criteria·정본 위치를 전달하는 실행 계약**이다.

## 3. Codex 책임 — 실제 Godot 제품 구현만

### 3.1 인계 Trigger

다음과 같이 **실제 게임이 돌아가는 구현 변경**이 필요할 때만 Codex로 인계한다.

- GDScript 또는 게임 실행 코드
- Scene / Resource / Autoload의 제품 변경
- 런타임에 소비되는 game data/resource 연결
- UI runtime wiring
- 저장·불러오기·제품 migration
- 실제 플레이에 영향을 주는 Godot config
- build/export
- Godot runtime/headless/play test를 위한 구현 변경

다음은 Codex trigger가 아니다.

- Base 문서/정책/Skill/Guide/Template 수정
- Notion 편집
- 기획서/GDD/밸런스표/Flow 작성
- 이미지 작업
- Base Registry/generated/CI/test contract 유지보수
- GitHub 문서 정리
- 조사·벤치마킹·검수·문제/교훈 승격

## 4. Codex 시작 Gate — 프로젝트 GitHub + Notion 재수화

Codex는 GPT 작업지시문을 그대로 기계 실행하지 않는다.

```text
GPT-reviewed Work Instruction
→ 정확한 게임 프로젝트/repository 확인
→ Project AGENTS.md / START_HERE / Active Context 확인
→ current branch / main / open workstream 확인
→ Notion Project Home / relevant Domain / AI System 확인
→ 승인 Visual의 current-use 승인·attach/readback 확인
→ 실제 Godot code/Scene/Resource/runtime data/test 상태 조사
→ Work Instruction과 current truth 대조
→ 승인된 결과를 보존하는 구현 방향·기술 방법 결정
→ IMPLEMENT
```

GPT가 예상 경로나 구조를 적었더라도 현재 Godot 프로젝트에 더 안전하고 단순한 방법이 있으면 Codex가 그 방법을 선택할 수 있다. 단, 프로젝트 방향을 바꿔서는 안 된다.

## 5. Codex가 기술적으로 자율 결정할 수 있는 것

승인된 플레이어 결과와 기획 의미를 유지하는 범위에서:

- Node/Scene/Resource 구조
- 함수·클래스·Signal·Autoload 구성
- 구현 순서
- 테스트 구조
- 내부 데이터 연결 방법
- 오류 처리와 edge case
- 성능·메모리·안정성 개선
- 동작 보존 리팩터링
- 실제 repository convention에 맞는 파일/명명 구조

## 6. `CHANGE_PROPOSAL` — GPT로 돌려보낼 것

다음이 필요하면 Codex가 임의 변경하지 않는다.

- 프로젝트 코어/Core Loop 변경
- 플레이 규칙·보상·실패 결과 변경
- 주요 UI/UX 흐름 변경
- 경제·성장·밸런스 의미 변경
- 서사·세계관·정사 변경
- Art Direction 변경
- 승인 기능의 추가/삭제나 범위 확대
- 저장 호환성을 깨는 제품 결정
- 새로운 비용·플랫폼·제품 경로 결정

```text
Codex finding
→ CHANGE_PROPOSAL
→ GPT 조사·기획·적대적 검토
→ 필요한 사용자 결정
→ 정본/작업지시문 갱신
→ Codex 구현 재개
```

## 7. 이미지 책임

### GPT

- 이미지 brief
- 생성·편집
- 정사/기획/스타일 검수
- Notion 정확한 프로젝트 위치에 업로드/attach
- current-use 승인 상태 기록
- readback

### Codex

`CODEX_IMAGE_GENERATION_FORBIDDEN`:

- AI 이미지 생성 금지
- 생성형 이미지 편집 금지
- 임의 AI placeholder 제작 금지
- 미승인 이미지 사용 금지

Codex가 사용할 수 있는 것은 현재 용도로 승인되고 Notion에 실제 업로드·attach·readback된 Visual뿐이다.

이미지가 부족하면:

```text
WAITING_GPT_VISUAL
→ GPT_VISUAL_REQUEST
→ GPT 제작·검수
→ Notion 승인 upload/attach/readback
→ Codex fresh-read
→ Godot 구현 재개
```

## 8. Base와 Notion 작업은 Codex 인계 대상이 아니다

이 항목은 현재 역할 분리의 중요 불변식이다.

```text
BASE_GOVERNANCE_WORK = GPT
NOTION_WORK = GPT
PROJECT_PLANNING_AND_REVIEW = GPT
PROJECT_VISUAL_WORK = GPT
GODOT_PRODUCT_IMPLEMENTATION = CODEX
```

예를 들어 Base의 역할 정책을 바꾸면서 Python contract test, Registry, generated index, CI validation을 함께 맞춰야 해도 **그 작업 전체는 GPT가 닫는다.** 이것을 “코드 파일이 있으므로 Codex 구현”으로 분류하지 않는다.

PR #674 같은 Base 운영 교정 workstream은 Codex 구현 대상이 아니다.

## 9. Codex 실행환경 freshness / wrong-target 안전성

실제 Godot 구현을 시작할 때 Codex는 현재 환경을 fresh-read한다.

```text
exact project/repository/worktree identity
→ branch/main/dirty/diverged 확인
→ project.godot 및 adopted authoring authority 확인
→ editor/runtime/addon/test readiness 확인
→ stale PID/session/port 불신
→ exact target 확인
→ persistent mutation
→ test/runtime/play
→ readback
```

보존 원칙:

- stale PID/session을 current truth로 쓰지 않음
- 다른 프로젝트 editor/server/process를 임의 조작하지 않음
- force push/history rewrite/destructive reset 금지
- 다른 open/draft/ready PR/worktree 기본 read-only
- 실제 Godot/runtime을 실행하지 않았으면 runtime PASS 아님

GPT→PowerShell→local Codex one-shot launcher는 기본 workflow가 아니다. Codex가 사용하는 shell/CLI/MCP/engine은 Codex 자신의 실제 Godot 구현 환경에 속한다.

## 10. Godot 구현 테스트·증거

Codex는 구현 범위에 맞게 다음을 실행한다.

- 정적/구문 검사
- Godot headless test
- 프로젝트 test suite
- 필요한 runtime smoke
- 실제 플레이 가능한 Slice 확인
- 성능/저장/입력/플랫폼 검증이 Acceptance에 있으면 해당 evidence

`NOT_RUN`, `SKIPPED`, `BLOCKED_UNVERIFIED`는 PASS가 아니다.

Base의 공용 문서/정책 validation suite는 GPT가 관리·실행한다. Codex의 이 섹션은 **게임 프로젝트 Godot 구현 증거**에 한정된다.

## 11. Codex 완료 반환

Codex는 게임 구현 완료 후 다음 형태로 GPT에 반환한다.

```yaml
codex_result:
  project:
  repository:
  baseline_commit:
  final_commit:
  changed_godot_files_and_reasons: []
  tests_passed: []
  tests_failed: []
  tests_not_run: []
  runtime_or_play_evidence: []
  approved_notion_visuals_consumed: []
  visual_requests_waiting: []
  technical_improvements: []
  change_proposals: []
  remaining_risks: []
  rollback:
  status: READY_FOR_GPT_REVIEW | BLOCKED | WAITING_GPT_VISUAL
```

## 12. GPT 최종 검수

GPT는 Codex 결과를 다음 기준으로 검수한다.

- 승인 기획과 실제 구현 일치
- 보호 범위 회귀 없음
- Notion 승인 Visual만 사용
- 이미지 생성 금지 준수
- 정상/실패/경계/회귀 test
- 실제 player outcome과 Acceptance 일치
- `NOT_RUN` 과장 없음
- 중복 구축·과설계·호환성 파괴 없음

필요하면 `REVISE`를 Codex에 반환한다. 제품 구현이 승인되면 GitHub와 Notion의 사람용/AI용 상태를 GPT가 정리한다.

## 13. 병합·동시작업 안전

- 현재 task의 구현 PR만 수정
- 다른 open/draft/ready PR은 기본 read-only
- current reviewed HEAD와 PR HEAD 일치 확인
- required checks와 review thread 확인
- force push/history rewrite/destructive reset 금지
- 병합 뒤 main readback
- Notion 구현 상태와 증거를 GPT가 후속 동기화

## 14. 완료 조건

- GPT의 기획·검수·비코딩 정본 작업이 닫혔다.
- 실제 Godot 제품 구현이 필요한 범위만 Codex에 전달됐다.
- Codex가 해당 프로젝트 GitHub + Notion을 fresh-read했다.
- Codex가 승인 범위 안에서 기술 구현 방향을 결정했다.
- Codex는 새 이미지를 만들지 않았다.
- Godot 구현·테스트·runtime/play evidence가 반환됐다.
- GPT가 최종 구현을 검수했다.
- Base/Notion/문서/운영 교정은 GPT가 직접 닫았다.

## 15. 폐기된 잘못된 해석

다음은 current workflow가 아니다.

- Codex = 모든 코드 파일 담당
- Codex = Base repository의 test/Registry/generated/CI 담당
- Codex = 모든 GitHub implementation executor
- Base/Notion 교정을 Codex에 넘김
- GPT가 Base 교정 중 Python test가 나온다는 이유로 Codex handoff
- GPT가 Godot 제품 코드를 직접 누적 구현
- Codex가 이미지 생성

현재 정본은 **`GPT = 비코딩·기획·검수·Base·Notion·Visual`, `Codex = 실제 게임 프로젝트의 Godot 제품 구현·코딩`**이다.


## 16. Consumer compatibility vocabulary

```text
Base Python test, CI contract, Registry/generated checker = GPT-owned Base governance
Base/Notion work not Codex trigger
actual game-project Godot product implementation = Codex product-build trigger
CODEX_PREFLIGHT_OPTIONAL
PLAN_REVIEW_ONLY
CONTINUOUS_WORK_EXECUTOR_HANDOFF
DEFERRED_EXTERNAL_EXECUTOR
APPROVED_ITEM_INHERITS_MERGE_AUTHORITY
AUTO_MERGE_AFTER_REQUIRED_CHECKS
AGENT_MERGE_REQUIRED
REPOSITORY_STRUCTURED_CANON
NOTION_HUMAN_FACING_CANON
```

이 vocabulary는 기존 consumer가 안전 의미를 잃지 않도록 유지하는 호환 계약이다. `CODEX_PREFLIGHT_OPTIONAL`은 고위험 Godot 제품 구현의 선택적 read-only technical preflight다. `CONTINUOUS_WORK_EXECUTOR_HANDOFF`와 `DEFERRED_EXTERNAL_EXECUTOR`는 실제 Godot product task에만 적용하며 Base/Notion task를 Codex로 넘기는 뜻이 아니다. `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`, `AUTO_MERGE_AFTER_REQUIRED_CHECKS`, `AGENT_MERGE_REQUIRED`의 exact-head/review/ruleset 병합 안전성은 유지한다.
