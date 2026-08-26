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
PLAY_MEANINGFUL_WORK_SLICE
TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT
GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING
EXISTING_SOLUTION_FIRST
PRE_HANDOFF_GPT_STOP
IMPACT_BOUNDED_REVALIDATION
CANON_SYNC_AFTER_VALIDATION
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
→ 현재 PLAY_MEANINGFUL_WORK_SLICE 정의
→ TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT
→ GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING
→ EXISTING_SOLUTION_FIRST
→ 필요한 범위 벤치마킹·재사용 조사
→ 적대적 검토·IRG
→ Player Outcome / Scope / Non-Scope / Acceptance / Evidence 확정
→ 필요한 이미지·사운드·Visual 요구를 실제 소비처 기준으로 확정
→ 비코딩 정본·문서·Notion 준비
→ PRE_HANDOFF_GPT_STOP

실제 Godot 제품 구현이 없음
→ GPT가 검증 가능한 비코딩 결과를 readback
→ CANON_SYNC_AFTER_VALIDATION
→ 종료

실제 Godot 제품 구현이 있음
→ GPT가 프로젝트별 Codex 구현 작업지시문 작성
→ CODEX_GODOT_PRODUCT_IMPLEMENTATION_HANDOFF
→ Codex가 해당 프로젝트의 GitHub + Notion을 fresh-read
→ 실제 Godot 구조에 맞는 구현 방향·기술 방법 결정
→ Godot 제품 구현·코딩·테스트·runtime/play evidence
→ READY_FOR_GPT_REVIEW
→ GPT가 구현 일치·runtime·실제 play/UX/Visual/Audio를 검수
→ finding을 FIX | TUNE | REDESIGN으로 분류
→ 필요한 수정 후 IMPACT_BOUNDED_REVALIDATION
→ 승인 후 병합
→ CANON_SYNC_AFTER_VALIDATION
```

### 1.1 `PLAY_MEANINGFUL_WORK_SLICE` — GPT의 기본 작업 단위

프로젝트 작업은 기본적으로 **플레이어가 구분 가능한 결과·선택·피드백을 한 번에 검증할 수 있는 가장 작은 의미 단위**로 자른다. 기능 파일 수나 문서 장 수가 아니라 플레이 의미를 기준으로 한다.

- 예: 소환 선택 → 배치 → 전투 결과 → 보상 피드백처럼 하나의 판단이 닫히는 범위.
- 여러 시스템이 필요하더라도 이번 플레이 결과에 직접 필요하지 않으면 `explicit_non_scope`로 둔다.
- 먼 미래 콘텐츠, 전체 장기 경제, 아직 소비되지 않을 설정을 구현 준비 명목으로 미리 완성하지 않는다.
- 이 `work slice`는 항상 release-near Vertical Slice라는 뜻이 아니다. 전체 대표 경험·판매력·제작 파이프라인까지 증명해야 하는 마일스톤은 `designing-vertical-slices`의 별도 shipping-intent 품질 Gate를 적용한다.

### 1.2 `TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT`

매 작업마다 프로젝트 전체를 다시 전수검사하지 않는다. 현재 Slice의 판단과 구현에 영향을 주는 정본·구현·증거만 targeted recovery한다.

기본 읽기 범위:

1. 최신 사용자 지시와 Project `AGENTS.md` / Active Context.
2. 현재 Slice에 관련된 승인 Decision과 분야별 정본.
3. 현재 Slice와 직접 연결된 실제 code/data/Scene/Resource/assets/tests.
4. 사람이 판단해야 하는 해당 Notion Home/Domain/AI System의 관련 surface.
5. 같은 Goal의 open/recent PR read-only reconciliation.
6. 직접 의존하는 인접 시스템과 기존 runtime/play evidence.

다음 때만 범위를 넓힌다.

- 증거가 cross-system 회귀나 정본 충돌을 가리킴.
- 공용 schema/interface/경제/저장 호환성처럼 실제 영향 범위가 프로젝트 전반임.
- 사용자가 명시적으로 프로젝트 전체 감사·전수검사를 요청함.

즉, 기존 선행 감사 의무는 유지하되 **현재 Slice의 영향 범위 안에서 수행**한다. 근거 없이 매 Slice마다 Base·Notion·GitHub 전체를 처음부터 다시 읽는 것은 검증이 아니라 중복 작업이다.

### 1.3 `GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING`

GPT는 Codex가 실제 구현을 시작하고, 구현 후 플레이 결과를 판정할 수 있을 만큼만 기획한다. 최소 산출물은 다음이다.

- 플레이어 행동: 무엇을 입력·선택·조작하는가.
- 목적과 기대 감정: 왜 이 행동을 하며 무엇을 느끼게 하려는가.
- 의미 있는 선택: 선택지와 trade-off가 무엇인가.
- 결과·실패·보상·피드백: 선택이 어떻게 되돌아오는가.
- 기존 시스템 의존성과 보호해야 할 규칙.
- UI/UX Flow와 플레이어가 알아야 할 정보.
- 필요한 데이터, 상태, 입력·출력의 의미.
- 필요한 이미지·사운드·Visual/VFX와 실제 게임 소비처.
- 주요 edge case와 실패 조건.
- Acceptance Criteria와 구현 후 runtime/play 검증법.
- 이번 Slice의 명시적 제외 범위.

구현 방법의 Node/Scene/함수 구조까지 GPT가 선행 고정하지 않는다. 그것은 current project truth를 읽는 Codex의 기술 자율 영역이다.

### 1.4 `EXISTING_SOLUTION_FIRST`

새 설계·에셋·모듈·도구를 만들기 전에 Base의 `REUSE_FIRST_PREFLIGHT_REQUIRED` evidence를 소비한다. 별도 중복 조사 파이프라인을 만들지 않는다.

```text
현재 프로젝트 구현/데이터/Scene/Resource
→ 현재 용도로 승인된 Asset / Reference
→ 검증된 Base module / knowledge / case
→ 직접 관련된 다른 프로젝트의 검증 evidence
→ 현재 결정에 필요한 외부 benchmark
→ 마지막에 BUILD_NEW
```

외부 사례는 표면 복사가 아니라 `ADOPT / ADAPT / REJECT`로 판정한다. 동일 Slice에 이미 유효한 benchmark/reuse evidence가 있으면 재사용하고, 새 uncertainty가 생긴 부분만 추가 조사한다.

### 1.5 적대적 검토와 구현 준비 판정

Slice의 최소 기획이 만들어지면 적대적 검토·IRG를 수행한다. root의 `ADVERSARIAL_REVIEW_UNTIL_CLEAN` 최소 반복 요구는 유지하지만, 각 반복에서 프로젝트 전체 기획을 다시 시작하지 않고 **현재 Slice 산출물과 직접 영향 범위**를 공격·수정·회귀검사한다.

최소 공격 질문:

- 플레이어의 의미 있는 선택이 실제로 존재하는가, 정답 하나로 수렴하지 않는가.
- 기능 존재가 플레이어 가치·재미의 대리 지표가 되고 있지 않은가.
- 설명 없이 이해해야 할 정보와 피드백이 충분한가.
- 기존 시스템·정본·에셋을 재사용할 수 있는데 새로 만들고 있지 않은가.
- 구현 비용 대비 체감 가치가 낮은 요소가 포함됐는가.
- UI/UX·데이터·Visual·Audio requirement가 실제 소비처와 연결되는가.
- Acceptance가 automated test와 실제 runtime/play 증거를 구분하는가.
- 이번 Slice와 무관한 미래 범위를 끌어오고 있지 않은가.

### 1.6 `PRE_HANDOFF_GPT_STOP`

다음이 충족되면 GPT의 **구현 전 기획 작업은 종료**한다.

- 현재 Slice의 player outcome과 의미 있는 선택이 명확함.
- approved scope와 explicit non-scope가 분리됨.
- 관련 정본·재사용·benchmark·적대적 검토가 현재 Slice 수준에서 닫힘.
- 필요한 data/UI/UX/asset/audio requirement와 Acceptance가 있음.
- 사용자 결정이 필요한 core/UX/경제/서사/Art Direction 충돌이 남지 않음.
- 구현 방법을 Codex가 current repository truth에서 선택할 수 있을 만큼 실행 계약이 명확함.

이 Gate 이후 GPT는 구현 방법을 더 세분화하며 문서를 계속 키우지 않는다. 실제 구현에서 새 사실이 나오면 Codex의 `CHANGE_PROPOSAL` 또는 구현 후 검수 결과로 다시 진입한다.

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
  work_slice_id:
  intended_player_outcome:
  player_action_and_choice:
  approved_scope: []
  explicit_non_scope: []
  protected_scope: []
  required_data_and_inputs: []
  ui_ux_flow: []
  asset_audio_dependencies: []
  acceptance_criteria: []
  review_evidence_expected: []
  notion_sources: []
  github_sources: []
  approved_visual_records: []
  required_runtime_or_play_checks: []
  forbidden_changes: []
  change_proposal_boundary: []
```

이 지시문은 구현 방법을 강제하는 스크립트가 아니다. **목표·승인 범위·보호 범위·Acceptance Criteria·정본 위치를 전달하는 실행 계약**이다. `PRE_HANDOFF_GPT_STOP` 이후 Node/Scene/함수 수준의 기술 설계를 GPT가 계속 확장하지 않는다.

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

### 12.1 구현 후 검수 순서

GPT는 코드 존재나 자동 테스트 PASS만 보고 승인하지 않는다.

```text
IMPLEMENTATION_MATCH_REVIEW
→ RUNTIME_REVIEW
→ ACTUAL_PLAY_UX_VISUAL_AUDIO_REVIEW
→ FIX | TUNE | REDESIGN
→ CORRECTION
→ IMPACT_BOUNDED_REVALIDATION
→ CANON_SYNC_AFTER_VALIDATION
```

1. **IMPLEMENTATION_MATCH_REVIEW**: 승인 규칙·데이터 의미·UI/UX Flow·Visual/Audio requirement와 실제 구현이 일치하는지 본다.
2. **RUNTIME_REVIEW**: 실제 실행에서 입력·상태변화·실패·저장·경계 동작이 의도대로 작동하는지 본다. test PASS와 runtime PASS를 분리한다.
3. **ACTUAL_PLAY_UX_VISUAL_AUDIO_REVIEW**: 실제 플레이에서 선택이 전달되는지, 정보가 읽히는지, 피드백·타이밍·가독성·감정·이미지·사운드가 의도한 역할을 수행하는지 본다.

### 12.2 `FIX | TUNE | REDESIGN`

모든 finding을 전체 재기획으로 돌리지 않는다.

- `FIX`: 기획·승인 의미는 맞지만 구현이 잘못됐거나 결함·회귀가 있다. Codex 수정으로 반환한다.
- `TUNE`: 구조와 의미는 맞지만 수치·속도·타이밍·배치·크기·가독성·피드백 강도 조정이 필요하다. 작은 조정 후 재검증한다.
- `REDESIGN`: 실제 플레이 증거가 현재 기획 가설·선택 구조·보상 구조·UX 의미 자체를 부정한다. **현재 Slice만** `GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING`으로 되돌린다. 프로젝트 코어·주요 UX·경제 의미·서사·Art Direction을 바꾸면 기존 `USER_DECISION_REQUIRED` 경계를 적용한다.

### 12.3 `IMPACT_BOUNDED_REVALIDATION`

수정 뒤에는 **바뀐 Slice + 실제 영향받은 직접 의존성**을 재검증한다. 작은 FIX/TUNE 때문에 프로젝트 전체 벤치마킹·적대검토·Notion/GitHub 전수검사를 처음부터 반복하지 않는다.

범위를 넓히는 조건:

- regression evidence가 인접 시스템 밖으로 전파됨.
- 공용 schema/interface/save/economy 규칙이 바뀜.
- REDESIGN이 core/player promise에 영향을 줌.
- 사용자가 전체 재검증을 명시적으로 요청함.

### 12.4 `CANON_SYNC_AFTER_VALIDATION`

검증을 통과한 결과만 current canon으로 승격한다.

- Notion: 사람이 이해·비교·수정해야 하는 시스템/Flow/UI/Visual/표/현재 플레이 상태.
- GitHub: Markdown/JSON/game data와 실제 구현·test/runtime truth.
- AI Workspace: 검증 기록, evidence ceiling, 실패 가설, 미해결 risk, 폐기한 대안.
- Base: 프로젝트에서 실제 검증된 뒤 여러 프로젝트에 재사용 가치가 있는 workflow/교훈만 일반화해 승격한다.

`IMPLEMENTED`만 있고 runtime/play 검증이 없으면 플레이어 경험을 canon PASS로 올리지 않는다.

## 13. 병합·동시작업 안전

- 현재 task의 구현 PR만 수정
- 다른 open/draft/ready PR은 기본 read-only
- current reviewed HEAD와 PR HEAD 일치 확인
- required checks와 review thread 확인
- force push/history rewrite/destructive reset 금지
- 병합 뒤 main readback
- Notion 구현 상태와 증거를 GPT가 후속 동기화

## 14. 완료 조건

- 현재 `PLAY_MEANINGFUL_WORK_SLICE`의 기획·검수·비코딩 정본 작업이 필요한 범위에서 닫혔다.
- `PRE_HANDOFF_GPT_STOP`을 넘기기 전에 approved scope / explicit non-scope / Acceptance / evidence plan이 정리됐다.
- 실제 Godot 제품 구현이 필요한 범위만 Codex에 전달됐다.
- Codex가 해당 프로젝트 GitHub + Notion을 fresh-read했다.
- Codex가 승인 범위 안에서 기술 구현 방향을 결정했다.
- Codex는 새 이미지를 만들지 않았다.
- Godot 구현·테스트·runtime/play evidence가 반환됐다.
- GPT가 최종 구현을 검수하고 finding을 `FIX | TUNE | REDESIGN`으로 처리했다.
- 필요한 수정 뒤 `IMPACT_BOUNDED_REVALIDATION`이 끝났다.
- 검증된 결과만 `CANON_SYNC_AFTER_VALIDATION`으로 GitHub/Notion에 반영됐다.
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
- 매 작은 Slice마다 프로젝트 전체 정본·벤치마킹·적대검토를 이유 없이 처음부터 반복
- 구현 준비가 끝났는데도 GPT가 Node/Scene/함수 수준까지 계속 설계해 Codex 기술 자율성을 침범
- 작은 FIX/TUNE를 전체 REDESIGN으로 확대

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
PLAY_MEANINGFUL_WORK_SLICE
TARGETED_CONTEXT_RECOVERY_NOT_FULL_PROJECT_REAUDIT
GPT_MINIMUM_IMPLEMENTATION_READY_PLANNING
EXISTING_SOLUTION_FIRST
PRE_HANDOFF_GPT_STOP
IMPACT_BOUNDED_REVALIDATION
CANON_SYNC_AFTER_VALIDATION
```

이 vocabulary는 기존 consumer가 안전 의미를 잃지 않도록 유지하는 호환 계약이다. `CODEX_PREFLIGHT_OPTIONAL`은 고위험 Godot 제품 구현의 선택적 read-only technical preflight다. `CONTINUOUS_WORK_EXECUTOR_HANDOFF`와 `DEFERRED_EXTERNAL_EXECUTOR`는 실제 Godot product task에만 적용하며 Base/Notion task를 Codex로 넘기는 뜻이 아니다. `APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`, `AUTO_MERGE_AFTER_REQUIRED_CHECKS`, `AGENT_MERGE_REQUIRED`의 exact-head/review/ruleset 병합 안전성은 유지한다.
