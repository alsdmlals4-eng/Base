# BCP-2026-042 · Work 최소 재개 입력 계약

## 상태

```yaml
proposal_id: BCP-2026-042
status: APPROVED_FOR_IMPLEMENTATION
approval_ref: USER_CHAT_2026-08-27_MINIMAL_BASE_PROJECT_RESTART
source_base_main: 0015159269f7f2dd89cdbb761b9c8b11832096a7
incremental_cost: 0
```

## 사용자 승인 목표

프로젝트 채팅마다 과거 장문 작업지시문 파일을 다시 첨부하지 않고 다음 한 문장만 입력해도 current Base와 프로젝트 고유 정본에서 작업을 복원해야 한다.

```text
[프로젝트명] 작업 재개. Base 최신 main과 프로젝트 고유 GitHub·Notion·actual implementation을 fresh-read하고, 현재 5단계 위치를 복원한 뒤 다음 안전 작업부터 진행해.
```

이 입력은 current approved Slice 안에서 이미 Base가 소유하는 다음 기능을 progressive-load해야 한다.

- 5단계 lifecycle과 프로젝트 native-state mapping
- 시작 정본 감사·선교정·남은 작업 재계산
- Grill Me·벤치마킹·재사용 우선 기획
- 안전한 Git fetch/pull/push·current-task PR·검증·squash merge·readback
- Incident/Solution/Lesson 기록과 Base 승격 판정
- Machine QA·다운로드 빌드·Human/Player evidence ceiling
- 사용자 검증 전 다음 Slice 자동 진입 금지

## 실제 확인한 현재 상태

Base current Router는 `WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md`와 5단계·체크리스트·QA·evidence owner를 순서대로 읽는다. Starter는 자동 Git, current-task merge, Incident/Solution/Lesson, Base promotion disposition과 완료 재검사를 이미 소유한다.

따라서 새로운 실행 알고리즘이 필요한 것이 아니다. 남은 gap은 다음이다.

1. **한 줄 fresh-read 입력이 충분하다는 사용자-facing 계약이 없음**
2. **프로젝트 채팅에 장문 지시문 파일을 매번 첨부하지 않아도 된다는 보증이 없음**
3. legacy 지시문을 단순 폐기할 때 아직 Project/Base 정본으로 이관되지 않은 고유 규칙이 조용히 유실될 위험
4. 위 경계의 회귀 테스트 부재

## 채택안

기존 `WORK_PROJECT_EXECUTION_CURRENT_ROUTER.md`에만 얇은 최소 입력 계약을 추가한다.

```text
MINIMAL_PROJECT_RESTART_ONE_LINE_ENTRY
BASE_AND_PROJECT_FRESH_READ_IS_ROUTING_INPUT
NO_PROJECT_CHAT_INSTRUCTION_FILE_ATTACHMENT_REQUIRED
CURRENT_BASE_ROUTER_AND_SPECIALIST_OWNERS_PROGRESSIVE_LOAD
EXACT_PROJECT_IDENTITY_REQUIRED
```

legacy 입력은 다음처럼 처리한다.

```text
LEGACY_INSTRUCTION_ATTACHMENT_NOT_ROUTINE_INPUT
LEGACY_INSTRUCTION_IS_DISCOVERY_ONLY_NOT_CURRENT_CANON
UNMIGRATED_UNIQUE_LEGACY_INSTRUCTION_CONTENT_MUST_BE_RECONCILED
NO_SILENT_DROP_OF_PROJECT_SPECIFIC_UNIQUE_RULES
```

### 의미

- exact 프로젝트가 식별되고 Base·Project 필수 source를 읽을 수 있으면 표준 한 줄이 routine 시작 입력으로 충분하다.
- Router가 current Starter와 전문 owner를 읽으므로 장문 지시문 내용을 채팅에 복사하지 않는다.
- 과거 지시문은 current truth가 아니다.
- 다만 과거 파일에만 남은 고유하고 유효한 프로젝트 규칙이 발견되면 한 번 Project/Base 정본으로 reconcile한 뒤 historical 처리한다.
- exact project identity 또는 필수 source가 불명확하면 추측하지 않고 `BLOCKED_UNVERIFIED`로 둔다.
- 한 줄 입력은 current approved Slice 범위를 확장하거나 이미지·권한·비용·공개 배포 등 별도 Gate를 우회하지 않는다.

## 비교안

| 안 | 판정 | 이유 |
|---|---|---|
| 프로젝트 채팅마다 기존 장문 파일 재첨부 | REJECT | 중복·stale·두 번째 정본·대화 용량 증가 |
| 장문 내용을 한 줄 prompt 안에 다시 내장 | REJECT | Router/전문 owner 중복, drift 위험 |
| Base Router를 한 줄 진입점으로 사용 | ADOPT | current owner를 항상 fresh-read하고 프로젝트 고유 정본 보존 |
| legacy 파일을 즉시 전부 삭제 | REJECT | 미이관 unique rule 유실 가능 |

## TDD

### RED

Exact test-only head `7f6891e5386afc8e34cf558909e19dd4ebfb5620`:

- Base v9 Operating Contracts: PASS
- docs / Ubuntu contract / publication: PASS
- whole core regression: FAIL
- exact new failures: 2
  - one-line restart markers and standard command absent
  - legacy instruction retirement/reconciliation markers absent

기존 자동 Git·Incident/Base promotion capability test는 계속 통과했다.

### GREEN 요구

- Router에 위 최소 진입·legacy reconciliation 경계 추가
- 기존 Starter 기능은 복제하지 않고 링크로 보존
- focused/core regression과 required CI
- open PR path overlap 0
- 최소 5회 full-scope adversarial review
- exact-head safe squash merge와 post-merge readback

## 범위 제외

- 프로젝트 AGENTS·Notion IA 일괄 수정 없음
- 과거 프로젝트 지시문 파일 자동 삭제 없음
- 제품 코드·게임 규칙·에셋·이미지 생성 없음
- 새 Skill·Tool·provider·dependency·유료 비용 없음
- direct main·force·ruleset/admin bypass 없음

## 동시성

- PR #746 및 모든 기존 open PR은 read-only다.
- 이번 예상 active path는 Router, 새 proposal/case, focused test뿐이며 #746 경로와 겹치지 않는다.
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 open PR #678 소유 중이므로 수정하지 않는다. Registry reconciliation은 해당 ownership 종료 뒤 별도 current-main 작업으로 남긴다.

## 롤백

구현 squash commit을 revert한다. 기존 Router→Starter→전문 owner 실행 구조와 프로젝트 정본은 그대로 유지된다.
