# GPT–Codex 역할·구현 인계 정책

이 문서는 Base를 사용하는 프로젝트에서 GPT와 Codex의 책임, GitHub·Notion 정본 재수화, 구현 인계, 이미지 제작 경계, 검증과 병합 경계를 정의하는 공용 정본이다.

## 0. 현재 역할 계약

```text
GPT_PLANNING_REVIEW_VISUAL_OWNER
CODEX_IMPLEMENTATION_EXECUTOR
PLANNING_ONLY_NO_CODEX_REQUIRED
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF
CODEX_REHYDRATE_GITHUB_AND_NOTION
CODEX_IMAGE_GENERATION_FORBIDDEN
CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY
GPT_VISUAL_REQUEST_REQUIRED_WHEN_ASSET_MISSING
APPROVED_VISUAL_NOTION_READBACK_REQUIRED
GPT_LOCAL_CODEX_ORCHESTRATION_RETIRED
CODEX_PREFLIGHT_OPTIONAL
AUTO_MERGE_AFTER_REQUIRED_CHECKS
AGENT_MERGE_REQUIRED
```

이 계약은 과거의 `GPT_GODOT_PREPRODUCTION_ALLOWED`, GPT가 PowerShell에서 로컬 Codex를 직접 부트스트랩하는 경로, 사용자 요청이 있어야만 구현을 Codex로 넘기는 `ON_DEMAND_CODEX_HANDOFF` 의미를 대체한다.

### 기본 흐름

```text
GPT
→ 프로젝트 정본 복원
→ 기획·조사·벤치마킹·대안 비교
→ 적대적 검토·Implementation Reality Gate
→ UI/UX·데이터·시스템·시각 요구 명세
→ 필요한 이미지 생성·편집·검수 및 Notion 승인 전달
→ IMPLEMENTATION_READY

구현·코딩이 필요 없음
→ GPT가 문서·Notion·검수 범위에서 종료

구현·코딩이 필요함
→ CODEX_IMPLEMENTATION_HANDOFF
→ Codex가 최신 GitHub + 최신 Notion + 승인 Visual을 직접 재수화
→ 필요할 때만 CODEX_PREFLIGHT_OPTIONAL
→ Codex가 코드·데이터·Scene·Resource·테스트·빌드·런타임 구현
→ 실제 실행·테스트·플레이 증거
→ GPT가 결과를 기획 의도·Acceptance Criteria·회귀 관점에서 최종 검수
→ 필수 게이트 통과 시 허용된 방식으로 병합
```

`IMPLEMENTATION_REQUIRES_CODEX_HANDOFF`는 모든 대화에서 Codex를 의무 호출한다는 뜻이 아니다. **실제 저장소 구현·코딩·테스트·런타임 변경이 필요한 단계에 진입하면 그 실행 책임을 Codex가 가진다**는 뜻이다. 조사·기획·검수·Notion 정리·이미지 제작만 필요한 작업은 GPT에서 끝낼 수 있다.

## 1. 권위와 정본

Codex는 GPT의 대화 요약을 구현 사실로 믿지 않는다. 구현 전에 반드시 현재 정본을 다시 읽는다.

```text
최신 사용자 결정
→ Project AGENTS.md / START_HERE / Active Context
→ Notion 사람용 프로젝트 기획·Flow·Visual·핵심 데이터
→ Notion AI/System 상세 작업면에서 필요한 구현 계약·승인 상태
→ GitHub Markdown/JSON/game data/code/Scene/Resource/Test
→ 현재 branch / commit / open workstream / runtime evidence
→ 구현 대상과 Acceptance Criteria 재대조
```

`DOMAIN_SPLIT_CANON`은 유지한다.

- **Notion**: 사람이 읽고 비교·수정하는 프로젝트 개요·기획·시각 방향·승인 Visual·사람용 데이터표·Flow/Storyboard의 정본.
- **GitHub repository**: Markdown·JSON·게임 데이터·코드·Scene·Resource·config·tests의 구조화·구현 정본.
- **Runtime evidence**: 실제 build·runtime·test·play 결과가 구현 사실의 증거.
- **Google Sheets**: 고유 미이관 자료가 남은 경우에만 migration compatibility source.

명세와 실제가 충돌하면 Codex는 임의로 한쪽을 덮어쓰지 않는다. 구현 사실 drift인지 기획 정본 drift인지 구분하고, 안전하게 해결 가능한 기술 drift는 승인된 범위에서 교정한다. 프로젝트 코어·플레이 규칙·주요 UX·경제·서사 의미·범위를 바꿔야 하면 `CHANGE_PROPOSAL`로 GPT에 반환한다.

## 2. GPT 책임

GPT의 기본 책임은 **기획·검수·시각 제작·구현 인계·최종 검수**다.

### 수행

- 현재 사용자 목표·프로젝트 코어·플레이어 약속 복원
- GitHub·Notion 최신 정본 대조와 충돌 탐지
- 필요한 범위의 최신 벤치마킹·시장·성공/실패 사례 조사
- 최소 3개 실질 대안 비교와 ADOPT / ADAPT / REJECT 판단
- 시스템 규칙·데이터 계약·UI/UX·Flow·Storyboard·콘텐츠 제작 문법 설계
- 밸런스 예산·조정 범위·Acceptance Criteria 설계
- 적대적 검토, Implementation Reality Gate, 구현 준비 판정
- 사용자가 요청한 이미지의 brief·생성·편집·검수
- 승인 이미지를 Notion의 정확한 프로젝트 Visual/Asset 위치에 전달하고 readback 확인
- Codex가 GitHub·Notion만 보고 이어받을 수 있는 구현 인계 명세 작성
- Codex 구현 결과의 기획 일치·회귀·미검증·증거 검수
- 필요한 사용자 결정·새 이미지 요청·기획 변경 제안 처리

### 기본 금지

GPT는 기본 프로젝트 작업에서 다음을 직접 구현 단계로 수행하지 않는다.

- GDScript 또는 제품 코드 작성·수정
- 실제 Scene·Resource·game data의 구현 변경
- Godot POC를 제품 구현으로 누적
- 빌드·런타임 구현을 대신 수행
- PowerShell에서 로컬 Codex를 실행하거나 로컬 Codex launcher를 사용자 기본 경로로 만드는 것
- Codex 대신 repository 구현 PR의 코드 변경을 떠맡는 것

GPT는 코드·Scene·Resource·diff를 **읽고 검수하거나 구현 명세를 만들 수는 있지만**, 구현 소유권을 가져오지 않는다.

Base 자체의 정책·기획 정본·Notion 운영 문서처럼 GPT 책임 범위인 문서 교정은 이 금지에 포함되지 않는다. 코드·테스트·자동화 변경이 필요해지는 순간 Codex 구현 인계로 전환한다.

## 3. 이미지 책임 경계

### 3.1 GPT

이미지 생성·편집은 GPT 책임이다. 실제 생성 시에는 `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`와 이미지 대화 승인 Gate를 따른다.

### 3.2 Codex

`CODEX_IMAGE_GENERATION_FORBIDDEN`:

Codex는 프로젝트 구현 중 다음을 하지 않는다.

- AI 이미지 생성
- 기존 이미지의 생성형 편집·스타일 변경
- 구현 편의를 위한 임의 캐릭터/배경/UI art 생성
- 승인되지 않은 임시 AI 이미지·placeholder를 새로 만들어 제품 경로에 넣기

Codex가 구현할 수 있는 것은 코드 기반 UI 레이아웃, shader/VFX, primitive drawing, animation wiring 등 **코드 구현 자체**다. 별도의 이미지 자산을 새로 만들어야 하는 경우에는 이미지 제작으로 간주하고 GPT에 반환한다.

### 3.3 Codex가 사용할 수 있는 이미지

`CODEX_VISUAL_INPUT_NOTION_APPROVED_ONLY`:

Codex는 현재 구현 용도가 승인되고 Notion에 실제 업로드·attach·readback된 Visual만 사용한다.

```yaml
approved_visual_input:
  project:
  notion_page_or_asset_record:
  visual_id_or_name:
  status:
  approved_for_current_use: true
  intended_use:
  attached_and_readback: true
  repository_target_if_promoted:
  rights_or_provenance_status:
```

프로토타입은 Notion에서 `APPROVED_CANDIDATE`이면서 현재 프로토타입 용도가 명시된 자산을 사용할 수 있다. 제품용 tracked asset 승격은 `PROJECT_ASSET_APPROVED`와 권리·경로 계약을 요구한다.

### 3.4 이미지가 부족할 때

Codex는 이미지를 직접 만들거나 임의 대체하지 않고 해당 자산 의존 task만 `WAITING_GPT_VISUAL`로 둔다.

```yaml
GPT_VISUAL_REQUEST:
  project:
  requester: CODEX
  implementation_task:
  why_required:
  player_or_ui_role:
  asset_type:
  target_screen_or_scene:
  required_dimensions_or_ratio:
  transparency_or_format:
  visual_constraints:
  existing_approved_references: []
  notion_destination:
  acceptance_criteria: []
  can_other_independent_implementation_continue: true | false
```

GPT가 brief·사용자 승인·이미지 제작/편집·검수를 거쳐 Notion에 승인 상태로 업로드하고 readback하면 Codex가 그 Visual을 다시 읽고 해당 구현을 재개한다.

## 4. 구현 인계 Gate

### 4.1 언제 인계하는가

다음 중 하나라도 실제 변경이 필요하면 `CODEX_IMPLEMENTATION_HANDOFF`로 전환한다.

- 제품 코드
- game data
- Scene / Resource / config
- 저장·불러오기·Schema migration 구현
- UI runtime wiring
- build/export 설정
- automated tests
- 실제 runtime·performance·device 검증을 위한 구현 변경

`USER_REQUESTED_CODEX_HANDOFF`는 호환 가능한 명시적 trigger로 남길 수 있지만 **필수 trigger는 아니다**. 구현 준비가 끝나고 구현 작업이 존재하면 인계가 정상 다음 단계다.

### 4.2 최소 인계 계약

```yaml
handoff_mode: CODEX_IMPLEMENTATION_HANDOFF
intent_and_player_outcome:
implementation_ready: true
actual_state_verification_required: true

notion_sources:
  project_home:
  relevant_domain_pages: []
  ai_system_detail_pages: []
  approved_visual_records: []

github_sources:
  repository:
  agents:
  active_context:
  structured_canon: []
  implementation_paths: []
  tests_and_runtime_evidence: []

known_problems_and_improvement_goals: []
protected_behavior_and_data_contracts: []
priority_order: []
acceptance_criteria: []
required_tests_and_runtime_checks: []
performance_size_structure_checks: []
forbidden_or_high_risk_changes: []

visual_policy:
  generation_by_codex: FORBIDDEN
  approved_notion_visuals_only: true
  missing_visual_action: GPT_VISUAL_REQUEST

change_proposal_boundary: []
completion_report_required:
  - changed_files_and_reasons
  - tests_run_failed_not_run
  - runtime_or_play_evidence
  - visual_inputs_consumed
  - remaining_risks
  - change_proposals_or_visual_requests
```

인계 문서는 구현 사실을 복제하지 않는다. **읽어야 할 정본의 위치, 승인된 요구, 금지 범위, 성공 기준**을 전달한다.

## 5. Codex 시작 Gate — 재수화

Codex는 구현 전 `CODEX_REHYDRATE_GITHUB_AND_NOTION`을 통과한다.

1. 정확한 프로젝트와 repository 확인
2. 최신 main/작업 branch와 현재 open workstream 확인
3. Project `AGENTS.md`, Active Context, 현재 결정 원본 확인
4. Notion Project Home 및 관련 Domain/AI System 페이지 확인
5. 현재 구현에 필요한 승인 Visual의 실제 attach/readback 상태 확인
6. 대상 code/data/Scene/Resource/test와 runtime evidence 확인
7. GPT 인계 명세와 current truth 대조
8. 보호 범위·Acceptance Criteria·rollback 확인
9. 충돌이 없거나 안전한 해결 경로가 확인된 뒤에만 persistent mutation 시작

다른 프로젝트 relation, stale branch, 오래된 handoff, 과거 대화, 로컬 캐시만으로 구현을 시작하지 않는다.

## 6. Codex Plan 책임 — 선택적 기술 preflight

`CODEX_PREFLIGHT_OPTIONAL`은 유지한다. 구현 그 자체는 Codex 책임이지만, 별도 읽기 전용 Plan을 매번 중복하지 않는다.

사용 조건:

- 저장·Schema·마이그레이션·플랫폼 설정 같은 고위험 변경
- GPT 명세와 실제 저장소의 drift 가능성이 큼
- 여러 Scene·Resource·공용 모듈의 경쟁 수정 위험
- 기술 대안을 구현 전에 비교할 가치가 큼
- 사용자가 별도 Plan 검토를 요청함

Plan 사용 시:

```yaml
mode: PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

Plan은 기술 위험·테스트·rollback·`CHANGE_PROPOSAL`을 분리한다. 명확한 저위험 작업은 재수화 Gate 뒤 바로 Build할 수 있다.

## 7. Codex Build 책임

Codex는 승인된 구현 범위에서 다음을 수행한다.

- GDScript와 프로젝트가 사용하는 다른 제품 코드
- Scene·Resource·Autoload·config
- runtime game data와 데이터 연결
- 저장·불러오기·migration 구현
- UI runtime wiring
- shader/VFX/code-driven feedback
- build/export 설정
- automated tests
- headless/runtime/device/play 검증에 필요한 구현
- 승인 범위의 구현 문서·manifest·구조화 데이터 동기화
- 독립 Commit·Push·현재 repository policy가 허용하는 PR 작업

### 범위 밖

- 프로젝트 코어·플레이어 약속을 임의 변경
- 중요 기획 결정을 새로 확정
- 승인되지 않은 기능 추가·삭제
- 승인 없는 데이터 호환성 파괴
- Notion Human Home을 AI metadata dump로 변경
- 이미지 생성·편집
- 다른 독립 open PR/worktree의 변경 흡수

## 8. 기술 변경과 기획 변경

### Codex 자동 반영 가능한 기술 변경

플레이어 결과와 승인 계약을 유지하는 경우:

- 동작 보존 리팩터링
- 성능·메모리·안정성 개선
- 적합한 Node·Scene·Resource·Signal 구조
- 테스트 가능성 개선
- 중복 제거·내부 파일 분리
- 오류 처리·방어 코드
- 승인 결과를 더 정확히 구현하는 세부 조정

### `CHANGE_PROPOSAL`

다음은 GPT 기획 단계로 반환한다.

- 프로젝트 코어·Core Loop 변경
- 플레이 규칙·보상·실패 결과 변경
- 신규 핵심 시스템·범위 추가
- MVP 포함·제외 변경
- 주요 UI/UX 흐름 변경
- 콘텐츠·서사 의미 변경
- 승인 기능 제거
- 저장 호환성을 깨는 Schema 변경
- 제작 범위·비용의 중대한 변경

Codex는 `CHANGE_PROPOSAL`과 무관한 독립 구현이 있으면 계속할 수 있다.

## 9. 구현 패키지

L2 이상·다중 의존성 작업은 하나의 통합 설계와 마스터 구현계획을 유지하고 검증 가능한 결과 단위로 분리한다.

```text
PKG-00 기반·테스트 하네스
PKG-01 핵심 상태·데이터
PKG-02 핵심 플레이 행동
PKG-03 성공·실패·복구
PKG-04 UI·피드백
PKG-05 저장·불러오기
PKG-06 콘텐츠 연결
PKG-07 Vertical Slice 통합
PKG-08 회귀·성능·접근성·마감
```

패키지는 파일 수가 아니라 플레이 가능한 결과, 명확한 입력·출력, 독립 검증·rollback, 경쟁 수정 최소화로 나눈다.

## 10. 구현 결과와 GPT 최종 검수

Codex 완료 보고에는 최소 다음이 있어야 한다.

```yaml
codex_result:
  baseline_and_final_commit:
  changed_files_and_reasons: []
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
```

GPT는 결과를 다음으로 검수한다.

- 구현이 승인 기획과 일치하는가
- Notion/GitHub 정본 drift가 생기지 않았는가
- 승인 Visual만 사용했는가
- Codex가 이미지를 생성하지 않았는가
- 정상·실패·경계·회귀 테스트가 충분한가
- 실제 플레이어 결과가 Acceptance Criteria와 맞는가
- `NOT_RUN`을 PASS로 과장하지 않았는가
- 과설계·중복 구축·호환성 파괴가 없는가

종료 상태:

- `PACKAGE_APPROVED`
- `PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES`
- `USER_REVIEW_REQUIRED`
- `CHANGE_PROPOSAL`
- `WAITING_GPT_VISUAL`
- `REVISE`
- `BLOCKED`
- `UNVERIFIED`

## 11. 병합 정책

`AUTO_MERGE_AFTER_REQUIRED_CHECKS`와 `AGENT_MERGE_REQUIRED`를 유지한다.

`APPROVED_ITEM_INHERITS_MERGE_AUTHORITY`: 명시적으로 승인된 동일 범위의 구현 PR은 검증을 통과하면 추가 확인·재승인·병합 승인 요청 없이 저장소가 허용한 방식으로 병합할 수 있다.

자동 병합/에이전트 병합 전에는 현재 repository에서 실제 required checks와 ruleset을 발견한다. 과거의 특정 check 이름을 공용 계약에서 무조건 가정하지 않는다.

필수 조건:

- PR이 현재 task의 승인된 범위
- Draft가 아님
- 검수 기준 HEAD와 현재 HEAD 일치
- 현재 Required Check 성공
- unresolved review thread 0
- `USER_REVIEW_REQUIRED`, `CHANGE_PROPOSAL`, `REVISE`, `BLOCKED`, `UNVERIFIED`, `WAITING_GPT_VISUAL` 없음

상태:

- `AUTO_MERGE_ELIGIBLE`
- `AUTO_MERGE_ENABLED`
- `AUTO_MERGE_BLOCKED`
- `UNVERIFIED_REPOSITORY_SETTING`

다른 독립 open/draft/ready PR은 read-only로 보호한다.

## 12. 중단·재개

중단 시 다음을 남긴다.

- 마지막 승인 범위와 현재 branch/commit
- GitHub/Notion에서 다시 읽을 정본 위치
- 구현 완료/미완료 패키지
- 테스트와 runtime evidence
- 승인 Visual 사용 목록
- `WAITING_GPT_VISUAL` 요청
- `CHANGE_PROPOSAL`·사용자 결정
- merge 차단 원인
- 다음 첫 행동과 rollback

재개 시 과거 대화가 아니라 최신 GitHub·Notion을 다시 읽는다.

## 13. 완료 조건

- GPT 단계에서 기획·검수·시각 요구·Implementation Ready가 실제로 닫혔다.
- 구현·코딩이 필요한 범위는 Codex로 인계되었다.
- Codex가 GitHub와 Notion을 fresh-read했다.
- Codex는 승인된 Notion Visual만 사용했고 새 이미지를 생성·편집하지 않았다.
- 이미지가 부족했다면 `GPT_VISUAL_REQUEST`로 반환되어 GPT 제작·승인·Notion upload/readback 뒤 재개되었다.
- 구현은 승인 범위와 current repository policy를 지켰다.
- 기술 개선과 기획 변경이 분리되었다.
- 실행한 테스트·런타임·플레이 증거와 `NOT_RUN`이 구분되었다.
- GPT가 최종 diff·증거·기획 일치를 검수했다.
- Required Check·HEAD·review thread·ruleset을 실제 현재 상태에서 확인했다.
- 사용자 결정이 필요한 상태를 자동 병합하지 않았다.

## 14. 폐기된 기본 경로

다음은 기본 운영에서 사용하지 않는다.

- GPT → PowerShell → local Codex를 매 작업마다 직접 구동
- GPT가 구현 POC/코드를 누적한 뒤 사용자가 원할 때만 Codex로 넘김
- Codex가 구현에 필요한 이미지를 직접 생성
- Notion에 승인·업로드되지 않은 이미지 자산을 임의 사용
- handoff 문서만 믿고 GitHub/Notion current truth 확인 생략

필요한 구현 shell·CLI·MCP·engine 사용은 **Codex 자신의 실행 환경에서 Codex가 책임지고 선택**한다. GPT는 그 로컬 실행 환경을 기본 사용자 절차로 관리하지 않는다.