# Fresh-Read Project Bootstrap

## Machine contract

```text
FRESH_READ_PROJECT_BOOTSTRAP
PROJECT_REPOSITORY_EXACT_SHA_PRIMARY
LEGACY_NOTION_OPTIONAL_MIGRATION_SOURCE
PAST_CONVERSATION_NOT_REQUIRED
CONTEXT_DRIFT_RECHECK_REQUIRED
```

새 채팅·새 담당자·새 AI가 과거 대화나 숨은 메모리 없이도 **해당 프로젝트 repository의 exact SHA**를 fresh-read하여 현재 품질·경계·다음 안전 작업을 재구성하기 위한 `maintaining-project-context-and-handoff` companion reference다. 별도 Skill·두 번째 정본·cross-project dashboard를 만들지 않는다.

Notion은 active reconstruction의 필수 입력이 아니다. `NOTION_UNIQUE_CANON_COUNT > 0`인 기존 프로젝트에서만 GPT가 `LEGACY_READ_ONLY` migration source로 읽고 repository receipt를 만든다.

## Required reconstruction

```yaml
fresh_read_project_bootstrap:
  project_identity:
  repository:
  exact_source_sha:
  current_goal:
  current_quality_and_stage:
  protected_scope: []
  next_safe_action:
  evidence_ceiling:
  instruction_surface:
  asset_manifest:
  legacy_migration_status: NOT_APPLICABLE | IN_PROGRESS | BLOCKED | COMPLETE
  reconstruction_result: READY | CONTEXT_DRIFT_RECHECK_REQUIRED | BLOCKED_UNVERIFIED
```

## Read order

```text
exact Project identity / repository
→ repository root AGENTS.md + nearest applicable AGENTS.md
→ PROJECT_START_HERE / Active Context / current decisions
→ AI production spec / current handoff / ASSET_MANIFEST
→ current default branch/main exact SHA + same-goal PR inventory
→ actual code/data/scene/resource/asset/tests/runtime evidence
→ derived Human Master GDD PDF가 필요하면 source SHA 대조
→ actual migration scope일 때만 legacy Notion/Sheet source와 repository receipt 대조
→ reconstruct required fields
```

- `project_identity`: 정확한 repository와 Project Key를 한 프로젝트로 결속한다.
- `exact_source_sha`: 현재 reconstruction의 commit identity를 고정한다.
- `current_goal`: 지금 무엇을 만드는지와 승인된 다음 milestone을 복원한다.
- `current_quality_and_stage`: 기획/Visual/구현/검증 중 어디까지 실제 evidence가 있는지 복원한다.
- `protected_scope`: 다른 채팅 workstream, 보호 Decision/파일/자산, 미승인 범위를 복원한다.
- `next_safe_action`: 중복 side effect 없이 바로 실행 가능한 첫 행동을 복원한다.
- `evidence_ceiling`: DESIGN/TECH/UI/HUMAN/PLAYER/RUNTIME 중 어디까지 증명됐는지 구분한다.
- `instruction_surface`: root/nearest AGENTS, project instruction, current Base adoption owner를 찾는다.
- `asset_manifest`: 승인 runtime asset의 repository path·SHA-256·consumer·상태를 확인한다.
- `legacy_migration_status`: Notion/Sheet 고유 자료가 실제로 남은 경우에만 계산한다.

## Drift gate

repository main·Decision·AI production spec·asset manifest·runtime evidence가 prepared handoff 이후 변했으면 mutation 전에 `CONTEXT_DRIFT_RECHECK_REQUIRED`다.

```text
mismatch
→ identify changed owner
→ read current diff / commit / manifest receipt
→ classify CURRENT / HISTORICAL / SUPERSEDED / CONFLICT
→ rebuild fields
→ only then mutate
```

legacy migration source와 repository가 다른 의미를 말하면 repository를 조용히 덮어쓰지 않는다. source authority·date·provenance를 기록하고 GPT migration path에서 conflict를 해결한다.

과거 대화·오래된 PR 번호·hard-coded historical SHA·source SHA 없는 PDF로 빈칸을 메우지 않는다.

## IRG / evidence ceiling

`Implementation Reality Gate`를 적용한다.

```text
files/pages discovered
≠ current meaning reconciled
≠ implementation verified
≠ runtime verified
≠ human usability verified
```

이 계약과 정적/readback 검증은 cold-start reconstruction **구조**를 증명할 수 있지만 실제 새로운 인간/독립 agent가 동일 품질로 재개했다는 증거는 아니다. 독립 receiver test를 실행하지 않았으면:

```text
HUMAN_USABILITY_NOT_RUN
TRANSFER_ACCEPTED_NOT_CLAIMED
```

## Success / failure

`READY`는 과거 대화 없이 최소 다음을 설명할 수 있을 때만 허용한다.

1. 어떤 프로젝트·repository·exact SHA인가.
2. 지금 목표와 현재 품질/단계는 무엇인가.
3. 무엇을 건드리면 안 되는가.
4. 다음 안전 작업은 무엇인가.
5. 무엇이 실제 구현/검증됐고 무엇이 NOT_RUN인가.
6. 적용 instruction surface와 책임 원본은 어디인가.
7. 승인 asset이 manifest로 회수 가능한가.
8. legacy migration blocker가 있는가.

하나라도 current repository에서 복원되지 않으면 `BLOCKED_UNVERIFIED` 또는 `CONTEXT_DRIFT_RECHECK_REQUIRED`다. Notion을 조회하지 않았다는 이유만으로 block하지 않는다. 다만 고유 자료가 남았다는 evidence가 있으면 `legacy_migration_status`를 정직하게 남긴다.

## Why this is a reference, not a new Skill

현재 Handoff Skill의 `resume`, Project START_HERE cold-start router, repository authority contract가 이미 책임을 갖는다. 이 reference는 그 owner가 같은 복원 결과를 생산하도록 연결하는 최소 계약이다. 반복 사용 결과 독립 authority/input/output/validation boundary가 실제로 분리된다는 증거가 생길 때만 새 Skill 후보를 재검토한다.

## Retired compatibility vocabulary

```text
PROJECT_GITHUB_NOTION_ONLY_RETIRED
Notion Human Home = legacy migration discovery surface only
compare GitHub ↔ Notion = migration conflict check only
```

구형 토큰은 consumer compatibility를 위해 남긴 것이며 dual-canon reconstruction을 복원하지 않는다.
