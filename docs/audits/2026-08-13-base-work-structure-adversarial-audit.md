# Base 작업 구조·Skill 동시작업 안전성 적대적 감사

## 0. 판정 요약

- 감사일: 2026-08-13
- 고정 기준: `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0`
- Work Mode: `PLAN → BUILD → REVIEW`
- 적용 Skill: `managing-project-intake-and-work-contract`, `synchronizing-local-and-github-state`, `running-adversarial-review-and-refinement`, `reviewing-and-validating-project-changes`
- Superpowers 절차: brainstorming, writing-plans, isolated-branch substitute for worktree, TDD, executing-plans, verification-before-completion, code-review gate, finishing/integration gate
- Existing Solution First: `ABSORB`
- 변경 결론: 새 Skill·새 Work Mode·별도 lock service를 만들지 않고, 기존 Git 동기화 Skill에 `CONCURRENT_CHANGE_PREFLIGHT`를 흡수한다.
- 동시작업 보호: 열린 PR #312의 변경 경로는 수정하지 않고 README 정합성 finding을 해당 PR comment로 전달했다.
- 감사 한계: connector 기반 정본·영향 지도와 GitHub Actions를 사용했다. 로컬 checkout이 없어 전체 tracked byte inventory, 로컬 full validation, 실제 worktree 생성은 `BLOCKED_UNVERIFIED`다.

## 1. 현재 운영 구조

### 1.1 권한 계층

```text
최신 사용자 요청
→ 프로젝트 AGENTS·보안·엔진·데이터 규칙
→ Active Context·확정 결정·승인 계약
→ 분야 정본·실제 코드·데이터·Scene·자산·Test
→ 프로젝트가 채택한 Base 사본
→ Base 원격 정본
→ 외부 공식 근거·사례
→ 과거 대화·추정
```

Base 내부의 공용 권한은 다음으로 분리되어 있다.

| 책임 | 정본 |
| --- | --- |
| 항상 적용 규칙 | `AGENTS.md` |
| 작업 생명주기·상태·증거 | `docs/OPERATING_MODEL.md` |
| PLAN/BUILD/REVIEW·Skill 라우팅 | `docs/WORK_MODE_AND_SKILL_ROUTING.md` |
| 문서·정본 역할 지도 | `docs/DOCUMENTATION_MAP.md` |
| ACTIVE Skill 기계 권한 | `skills/SKILL_REGISTRY.json` |
| 사람용 활성 Skill 파생 Map | `docs/generated/BASE_ACTIVE_SKILLS.md` |
| 변경 검증 | `reviewing-and-validating-project-changes`와 Tests/Actions |
| 적대 검토·사후 감시 | `running-adversarial-review-and-refinement` |
| Git 상태·전달 | `synchronizing-local-and-github-state` |

### 1.2 Work Mode

현행 Work Mode는 정확히 세 개다.

```text
PLAN   → 의도·근거·설계·범위·승인 고정
BUILD  → 승인 범위 최소 구현·단계 검증
REVIEW → 독립 공격·비판 검증·회귀·판정
```

Skill은 Work Mode가 아니며, Skill Mode는 한 Skill 안의 세부 절차다. 이번 변경은 네 번째 Work Mode를 만들지 않는다.

### 1.3 ACTIVE Skill 구조

Registry-derived Map의 관찰값은 ACTIVE Skill `30`개다. 수는 설계 제약이 아니며 trigger가 맞는 최소 Skill만 지연 로딩한다.

| 책임 군 | 대표 ACTIVE Skill |
| --- | --- |
| Foundation·프로젝트 운영 | intake/work-contract, game-project operating system, discipline evolution, design documents, context/handoff |
| 게임 기획·제작·연구 | concept refinement, vertical slice, project core 식별·확정, user research coverage, game-dev YouTube |
| 아트·UI | art prompt/technique cards, UI/art audit |
| 검토·정본·구조 | change validation, reference freshness, adversarial review, contract-preserving refactor, skill-body simplification, stale-material pruning, legacy/archive governance |
| 실행·도구·인프라 | Git sync, long-running continuity, DeepSeek worktrees, runtime failure diagnosis, Godot asset/plugin evaluation, AI model/prompt cost |
| 지식·발행·기타 | Base proposal, user learning notes, visual dashboard, serial fiction |

강점은 `Registry → 필요한 Skill만 선택 → reference를 필요할 때만 로드 → exact evidence`의 점진적 공개 구조다. 이 구조를 보존하는 것이 새 Skill 추가보다 우선한다.

## 2. 외부 현업·시장 비교

조사일은 2026-08-13이며 공식·1차 문서만 사용했다. 시장 점유율이나 매출 순위가 아니라 AI 개발 도구 시장의 운영 패턴과 검증 가능한 성공 조건을 비교했다.

| 비교 대상 | 공식 운영 패턴 | Base 현행 판정 | 채택·변형·제외 |
| --- | --- | --- | --- |
| OpenAI Codex | 저장소 루트부터 현재 작업 경로까지 지시를 계층적으로 주입하고, tool loop가 실제 파일·명령 결과를 다시 문맥에 넣는다. | `AGENTS.md` 권한 계층과 증거 우선은 정합 | 채택 유지: 지시 계층·도구 증거. 별도 복제 불필요 |
| GitHub Copilot Agent Skills | Skill 설명으로 관련 작업을 자동 선택하고, `SKILL.md` 전체는 선택 시 context에 주입한다. 보편 규칙은 custom instruction, 가끔 필요한 상세 절차는 Skill로 분리한다. | Registry trigger·최소 Skill 로딩과 정합 | 채택 유지: 새 broad Skill 대신 기존 owner reference에 흡수 |
| Claude Code | Skill은 on-demand로 전체 내용을 로드하며, 병렬 세션은 Git worktree로 파일 편집을 격리한다. | 점진 로딩은 강함. 일반 Git sync의 열린 PR·의미 자원 사전판정은 누락 | 변형 채택: worktree 원칙 + remote PR/path/semantic preflight |
| GitHub strict checks / merge queue | strict check는 최신 base와의 동기화를 요구한다. merge queue는 latest base와 queue 선행 변경을 합친 `merge_group`에서 required checks를 검증한다. | exact HEAD 규칙은 강함. 일반 sync Skill의 main freshness·same-goal 재검사는 누락 | 채택: PR·merge 직전 current main과 exact head 재검사. 설정 변경은 별도 승인 범위라 제외 |
| Google Cloud DORA | AI 시대에는 작고 독립적이며 testable한 batch와 짧은 Branch가 피드백·복구·통합 안전성을 높인다. | Base 최소 변경 원칙과 정합 | 채택 유지: PR #312와 비중첩인 1개 책임만 수정 |

Primary sources:

- OpenAI, *Unrolling the Codex agent loop* (2026-01-23): https://openai.com/index/unrolling-the-codex-agent-loop/
- GitHub Docs, *Adding agent skills for GitHub Copilot*: https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills
- GitHub Docs, *Available rules for rulesets*: https://docs.github.com/en/enterprise-cloud@latest/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Docs, *Managing a merge queue*: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue
- Anthropic, *How Claude Code works*: https://code.claude.com/docs/en/how-claude-code-works
- Anthropic, *Run parallel sessions with worktrees*: https://code.claude.com/docs/en/worktrees
- Google Cloud DORA, *Working in small batches*: https://dora.dev/capabilities/working-in-small-batches/
- Google Cloud DORA, *Continuous integration*: https://dora.dev/capabilities/continuous-integration/

## 3. 적대적 검토 finding

### F-01 — Human-facing ACTIVE Skill 수 drift

- 분류: `CONFLICTING_SOURCE / STALE_CONSUMER`
- 증거:
  - `docs/generated/BASE_ACTIVE_SKILLS.md`: Registry-derived ACTIVE Skill `30`
  - `README.md`: ACTIVE Skill `27`과 수동 목록을 복제
  - `docs/OPERATING_MODEL.md`: human-facing 문서가 활성 Skill 목록을 수동 복제하지 않도록 규정
- 위험: 새 Skill 병합 뒤 README가 이전 상태를 사실처럼 보여 cold-start와 감사 결과를 왜곡한다.
- 적대적 반례: README를 이 PR에서 바로 고치면 사실 정합성은 회복되지만, 열린 PR #312가 같은 파일을 소유하므로 동시작업 충돌을 만든다.
- 승인된 최소 조치: PR #312에 고정 수·수동 목록을 제거하고 생성 Map으로 연결하도록 coordination comment를 남겼다.
- 현재 상태: `WAITING_RESOURCE`. 이 PR에서는 README를 수정하지 않는다.

### F-02 — Loop-level lock과 일반 Git sync 사이의 consumer 누락

- 분류: `MISSING_CONSUMER / CONTRACT_GAP`
- 증거:
  - `docs/OPERATING_MODEL.md`의 Loop Control Plane은 `TASK_LEASE`, path lock, semantic resource lock, exact-SHA freshness를 정의한다.
  - 기존 `synchronizing-local-and-github-state/SKILL.md`는 DIRTY·ahead/behind·DIVERGED만 판정했다.
  - 기존 `safe-sync-protocol.md`는 열린 PR, same-goal, changed paths, semantic overlap, main 이동을 첫 write 전에 검사하지 않았다.
- 실패 시나리오:
  1. 서로 다른 채팅이 같은 Markdown을 수정한다.
  2. 파일은 다르지만 Registry/생성 Map, Schema/fixture, Scene/resource처럼 같은 의미 자원을 동시에 변경한다.
  3. 동일 Goal의 두 PR이 다른 해석으로 병렬 구현된다.
  4. 조사 기준 main과 병합 시점 main이 달라도 이전 CI를 재사용한다.
  5. PR/path 증거를 읽지 못한 상태를 충돌 없음으로 오판한다.
- 승인된 최소 조치: 기존 sync Skill의 `inspect`에 `CONCURRENT_CHANGE_PREFLIGHT`를 흡수하고 safe-sync reference에 write/PR/merge/post-merge 재검사를 추가했다.
- 상태: `IMPLEMENTED_PENDING_EXACT_HEAD_VERIFICATION`.

### F-03 — 새 broad Skill 또는 lock service 신설 제안

- 분류: `REJECTED_CRITIQUE / DUPLICATE_RESPONSIBILITY`
- 공격안: 동시작업 전용 ACTIVE Skill, 중앙 scheduler, 강제 lock server를 만든다.
- 반증:
  - Base에는 이미 Git sync owner와 Loop Control Plane의 lease/resource 개념이 있다.
  - 새 Skill은 Registry routing·문서·tests·학습·발행 소비자를 늘려 동일 책임을 중복한다.
  - lock server는 인증·가용성·복구·stale lease·운영 비용을 새로 만들며 이번 문서 계약 범위를 초과한다.
- 결론: 제외. 현행 owner에 cooperative preflight를 흡수한다. 실제 강제 mutex가 필요하다는 운영 증거가 누적될 때 별도 제안으로 재평가한다.

### F-04 — 감사 증거 범위 한계

- 분류: `BLOCKED_UNVERIFIED`
- 확인됨: 정본 지도, 30 ACTIVE Skill Map, 관련 Skill/reference, 주요 소비자 Test/Workflow, 열린 PR과 changed paths, exact-head Actions 결과.
- 확인하지 못함: 로컬 전체 tracked byte inventory, 로컬 `git fsck`, 전체 unittest discover, 실제 Godot/runtime/render, repository settings의 UI 상태.
- 방어: 전체 파일을 읽었다고 주장하지 않는다. 정본·Registry·참조·영향 지도로 범위를 확장하고 exact-head CI와 post-merge readback으로 보완한다.

## 4. 구현 전후

| 항목 | 변경 전 | 변경 후 |
| --- | --- | --- |
| 기준 SHA | 로컬/원격 HEAD와 ahead/behind 중심 | `source_main_sha`, `current_main_sha`, `expected_head_sha`를 분리 |
| 열린 PR 인식 | 일반 sync 계약에 없음 | open/recent same-goal PR과 changed paths 필수 증거 |
| 충돌 단위 | Git path/history 중심 | `PATH_OVERLAP`과 `SEMANTIC_OVERLAP` 분리 |
| 중복 구현 | 명시적 판정 없음 | `SAME_GOAL → DUPLICATE_WORK` |
| main 이동 | merge 전 일반적 재판정 불명확 | `STALE_BASE_SHA`, reconcile 후 preflight 재실행 |
| 증거 부재 | BLOCKED는 있으나 동시작업 evidence ceiling 불명확 | `UNKNOWN + BLOCKED_UNVERIFIED`, `CLEAR` 추정 금지 |
| 조정 | 충돌 뒤 merge/rebase/new branch | write 전 비중첩 축소·소유 PR comment·handoff·resource release |
| 병합 증거 | Required Checks·최종 동등성 | exact reviewed HEAD + current main freshness + PR/resource 재검사 |
| 병합 후 | 최종 HEAD 대조 | post-merge main readback + same-goal/정본/consumer 재감사 |
| 구조 복잡도 | 30 ACTIVE Skill, 3 Work Mode | 그대로 유지 |

## 5. TDD·검증 계약

### RED

- PR: #313
- exact RED head: `acb59559701f90ceb835a8a271c630058b863696`
- Workflow: `Validate Base v9 Operating Contracts`, run `31653620789`
- Job: `base-v9-contract`, job `94303084090`
- generated/integrity 단계: 통과
- focused suite: `327` tests, `2` failures, `1` skipped
- 실패 원인:
  - `CONCURRENT_CHANGE_PREFLIGHT`가 기존 sync Skill에 없음
  - `first persistent write` 재검사가 기존 safe-sync protocol에 없음
- 다른 기존 계약 실패: 관찰되지 않음

### GREEN acceptance gate

1. dedicated contract test가 `tests.test_v9_machine_contracts`를 통해 focused CI에서 실제 실행된다.
2. exact PR head의 적용 가능한 Actions가 성공한다.
3. PR #312와 changed-path 중첩이 없다.
4. 새 ACTIVE Skill, Work Mode, workflow, dependency, schema, generated artifact가 없다.
5. main·open PR 집합이 바뀌면 preflight와 CI freshness를 다시 판정한다.
6. 병합 뒤 새 main에서 핵심 token과 변경 경로를 read back한다.

로컬 checkout이 없는 세션이므로 로컬 `tools/run_local_validation.py` 실행은 주장하지 않는다. GitHub Actions가 exact-head의 fresh evidence를 제공한다.

## 6. 변경·보호 범위

### 변경 경로

```text
docs/superpowers/specs/2026-08-13-concurrent-sync-preflight-design.md
docs/superpowers/plans/2026-08-13-concurrent-sync-preflight.md
docs/audits/2026-08-13-base-work-structure-adversarial-audit.md
skills/synchronizing-local-and-github-state/SKILL.md
skills/synchronizing-local-and-github-state/references/safe-sync-protocol.md
tests/test_concurrent_git_sync_preflight_contract.py
tests/test_v9_machine_contracts.py
```

### 의도적으로 보호한 경로

```text
README.md
START_HERE.md
docs/DOCUMENTATION_MAP.md
skills/SKILL_REGISTRY.json
docs/generated/**
AGENTS.md
docs/OPERATING_MODEL.md
.github/workflows/**
schemas/**
base*.lock.json
PR #312가 변경하는 visual/Figma/shared-tool 경로
```

## 7. 기대 효과와 비용

### 기대 효과

- 다른 채팅·Agent가 이미 소유한 경로를 첫 write 전에 발견한다.
- 파일명이 달라도 같은 정본·Schema·생성물·Scene·자산 계열의 동시 writer를 차단한다.
- 같은 Goal의 경쟁 PR을 새로 만들지 않고 기존 작업에 보완을 집중한다.
- main 이동과 이전 HEAD의 CI 재사용을 명시적으로 차단한다.
- 증거를 읽지 못한 상태를 안전한 상태로 포장하지 않는다.
- 기존 3 Work Mode·30 ACTIVE Skill·Registry routing을 유지해 학습·context 비용을 늘리지 않는다.

### 비용·남은 위험

- write/PR/merge 전에 GitHub 조회와 조정 단계가 추가된다.
- cooperative 계약이므로 다른 도구·채팅이 이를 무시하면 강제 차단되지 않는다.
- semantic resource 선언 품질이 낮으면 false negative 또는 보수적 false positive가 생길 수 있다.
- README drift 해결은 PR #312 소유자 반영과 병합 순서에 의존한다.
- repository ruleset/merge queue 강제화는 이번 변경에 포함되지 않는다.

## 8. Rollback

이 PR의 squash merge commit 하나를 revert한다.

- 데이터·Schema migration 없음
- Registry·generated artifact migration 없음
- dependency·workflow·repository setting 변경 없음
- project-specific 동기화 없음

Rollback 뒤에는 기존 sync Skill/reference와 dedicated test·spec·plan·audit만 원상 복귀한다.

## 9. 승격 판정

- Base 공용 교훈: `동시 AI 작업에서는 Git topology + open PR path + semantic resource + same Goal + exact main freshness를 write 전에 함께 판정한다.`
- 프로젝트 고유 내용: 없음
- 후속 후보: 실제 충돌 사례가 누적될 때 semantic resource naming fixture 또는 machine-enforced lease를 별도 BCP로 평가한다. 현재는 증거 부족으로 구현하지 않는다.
