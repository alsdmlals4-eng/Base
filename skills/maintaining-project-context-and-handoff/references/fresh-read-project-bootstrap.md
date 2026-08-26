# Fresh-Read Project Bootstrap

## Machine contract

```text
FRESH_READ_PROJECT_BOOTSTRAP
PROJECT_GITHUB_NOTION_ONLY
PAST_CONVERSATION_NOT_REQUIRED
CONTEXT_DRIFT_RECHECK_REQUIRED
```

새 채팅·새 담당자·새 AI가 과거 대화나 숨은 메모리 없이도 **해당 프로젝트의 현재 GitHub + 해당 Project Notion**만 fresh-read하여 현재 품질·경계·다음 안전 작업을 재구성하기 위한 `maintaining-project-context-and-handoff`의 companion reference다. 별도 Skill·두 번째 정본·cross-project dashboard를 만들지 않는다.

## Required reconstruction

```yaml
fresh_read_project_bootstrap:
  project_identity:
  current_goal:
  current_quality_and_stage:
  protected_scope: []
  next_safe_action:
  evidence_ceiling:
  instruction_surface:
  reconstruction_result: READY | CONTEXT_DRIFT_RECHECK_REQUIRED | BLOCKED_UNVERIFIED
```

## Read order

```text
exact Project identity
→ Notion Human Home / current Project domains
→ repository root AGENTS.md + nearest applicable AGENTS.md
→ PROJECT_START_HERE / Active Context / current decisions
→ current default branch/main + same-goal PR inventory
→ actual code/data/scene/resource/asset/tests/runtime evidence
→ compare GitHub ↔ Notion
→ reconstruct required fields
```

- `project_identity`: 정확한 repository, Project Key, Notion Human Home을 한 프로젝트로 결속한다.
- `current_goal`: 지금 무엇을 만드는지와 승인된 다음 milestone을 복원한다.
- `current_quality_and_stage`: 기획/Visual/구현/검증 중 어디까지 실제 evidence가 있는지 복원한다.
- `protected_scope`: 다른 채팅 workstream, 보호 Decision/파일/자산, 미승인 범위를 복원한다.
- `next_safe_action`: 중복 side effect 없이 바로 실행 가능한 첫 행동을 복원한다.
- `evidence_ceiling`: DESIGN/TECH/UI/HUMAN/PLAYER/RUNTIME 중 어디까지 증명됐는지 구분한다.
- `instruction_surface`: root/nearest AGENTS, project instruction, current Base adoption owner를 찾는다.

## Drift gate

Notion과 GitHub가 같은 현재 의미를 말하지 않거나 prepared handoff 이후 main/Decision/Visual/runtime이 변했으면 mutation 전에 `CONTEXT_DRIFT_RECHECK_REQUIRED`다.

```text
mismatch
→ identify changed owner
→ read current diff / Notion edit
→ classify CURRENT / HISTORICAL / SUPERSEDED / CONFLICT
→ rebuild fields
→ only then mutate
```

과거 대화·오래된 PR 번호·hard-coded historical SHA로 빈칸을 메우지 않는다.

## IRG / evidence ceiling

`Implementation Reality Gate`를 적용한다.

```text
files/pages discovered
≠ current meaning reconciled
≠ implementation verified
≠ runtime verified
≠ human usability verified
```

이 계약과 10개 Home의 정적/readback 검증은 cold-start reconstruction **구조**를 증명할 수 있지만 실제 새로운 인간/독립 agent가 동일 품질로 재개했다는 증거는 아니다. 독립 receiver test를 실행하지 않았으면:

```text
HUMAN_USABILITY_NOT_RUN
TRANSFER_ACCEPTED_NOT_CLAIMED
```

## Success / failure

`READY`는 과거 대화 없이 최소 다음을 설명할 수 있을 때만 허용한다.

1. 어떤 프로젝트인가.
2. 지금 목표와 현재 품질/단계는 무엇인가.
3. 무엇을 건드리면 안 되는가.
4. 다음 안전 작업은 무엇인가.
5. 무엇이 실제 구현/검증됐고 무엇이 NOT_RUN인가.
6. 적용 instruction surface와 책임 원본은 어디인가.

하나라도 현재 GitHub+Notion에서 복원되지 않으면 `BLOCKED_UNVERIFIED` 또는 `CONTEXT_DRIFT_RECHECK_REQUIRED`다.

## Why this is a reference, not a new Skill

현재 Handoff Skill의 `resume`, Project START_HERE cold-start router, Human Home self-contained contract가 이미 책임을 갖는다. 이 reference는 그 세 owner가 같은 복원 결과를 생산하도록 연결하는 최소 계약이다. 반복 사용 결과 독립 authority/input/output/validation boundary가 실제로 분리된다는 증거가 생길 때만 새 Skill 후보를 재검토한다.
