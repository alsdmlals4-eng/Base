# BCP-2026-016 Evidence — Coc-Fiction Reconciliation Frontier

## 1. 증거 목적

이 문서는 `BCP - Coc-Fiction`의 프로젝트 재현 근거와 외부 벤치마킹을 분리 보존한다.

공용화 대상은 작품의 설정·회차 숫자가 아니라 다음 네 가지다.

1. verified prefix와 legacy tail 사이의 moving frontier
2. unresolved migration boundary에서 derived continuity fail-closed
3. migration debt와 duplicate current authority를 구분
4. candidate migration state와 verified promotion state를 분리

## 2. 프로젝트 기준점

```yaml
repository: alsdmlals4-eng/Coc-Fiction
observed_main: e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0
observed_at: 2026-08-10
project_state_warning: CURRENT_MAIN_VALIDATION_FAILURE_OBSERVED
```

이 evidence는 current main이 Green이라고 주장하지 않는다. 오히려 PR #19의 merged state와 failed validation을 BCP-016의 반례로 사용한다.

## 3. 프로젝트 lineage

### PR #13 — operating integration

- current Base 구조와 Coc-Fiction 5-Skill 운영 구조 재대조
- stale PR 전체 branch는 부활시키지 않고 current-main 위 unique delta만 선택 흡수
- 새 여섯 번째 project Skill 생성 거절
- fixed `1~3 POV`의 Base-wide 승격 거절
- serial-arc revision mode는 기존 project owner에 흡수

의미:

- 프로젝트 고유 생산값과 공용 운영 원리를 분리하는 Existing Solution First가 실제로 작동했다.

### PR #14 — Canon sync + bounded legacy debt

- latest user Decision을 current Canon으로 승격
- 기존 legacy manuscript를 blind rewrite하지 않음
- strict-global 초기 시도에서 대량 legacy debt가 드러남
- `STRICT_NOW / FORBIDDEN_IN_NEW_OR_REVISED / BOUNDED_LEGACY_RECONCILIATION_DEBT / SCOPED_STRICT`로 lifecycle 분리
- exact legacy debt consumer set이 새 위치로 증가하면 fail-closed

이 단계가 BCP-012의 직접 출처다.

### PR #15 / #16 — continuation self-stale

PR #15는 Base proposal 상태를 live continuation 문서에 저장했다. 그러나 그 PR이 merge되자 문서가 기록한 `current main SHA`가 즉시 과거 값이 됐다.

PR #16은 다음 의미로 보정했다.

```text
stable default branch = main
+ last_observed_main_sha
+ last integrated PR / merge result
+ post-merge CI evidence
+ next resume fresh-read
```

이 문제는 BCP-013이 소유하므로 BCP-016의 새 Goal로 세지 않는다.

### PR #17 — Ch1~5 first external reconciliation

외부 최신 제1~5화를 GitHub legacy 저장 원고에 그대로 덮어쓰지 않고 source/Canon/user Decision/adjacent state로 대조했다.

판정 결과는 1~5 모두 APPLY였지만 새 제5화와 legacy 제6화는 정상 연속이 아니었다.

새 제5화가 legacy 제6화보다 사건상 더 뒤까지 진행돼 있어 다음 연결은 false continuity였다.

```text
latest Ch5
→ legacy Ch6
→ already-passed ship events repeat
```

따라서 프로젝트는 다음 mixed-migration 상태를 기록했다.

```yaml
reconciled_prefix_end: 5
legacy_tail_starts_at: 6
boundary_after_chapter: 5
whole_manuscript_continuity: NOT_YET_CLAIMED
next_bundle: 006-010
```

파생 reverse outline에서는 경계를 정상 `next/previous`로 만들지 않았다.

#### TDD evidence

PR #17 body에 기록된 exact-head 검증:

- final head: `31a4d959cef54ad77576672ff7cca8a53db72c42`
- workflow run: `31355669160`
- result: `SUCCESS`

post-merge checkpoint PR #18 기록:

- project main after PR #17: `9a7b2e2419465bd76daf0cf09b96ed7c0cd7d54c`
- post-merge push run: `31355813027`
- result: `SUCCESS`

### PR #17 duplicate ownership debugging

migration-boundary chapter를 일반 override와 boundary override가 동시에 소유하도록 만든 중간 시도에서 composed consumer가 duplicate chapter를 거부했다.

해결:

```text
duplicate ownership
→ do not weaken composer
→ remove overlapping owner
→ leave one current authority
→ regenerate
```

이 사례 때문에 다음 구분이 필요하다.

```text
KNOWN_LEGACY_DEBT
!= AMBIGUOUS_CURRENT_AUTHORITY
```

legacy debt는 선언적으로 허용할 수 있지만 current authority 중복은 fail-closed 대상이다.

### PR #19 — Ch6~10 frontier advance candidate + failed validation counterexample

PR #19는 외부 최신 제6~10화를 reconciliation하고 frontier를 다음처럼 이동시키는 변경을 merge했다.

```yaml
candidate_reconciled_prefix_end: 10
candidate_legacy_tail_starts_at: 11
candidate_boundary_after_chapter: 10
candidate_next_bundle: 011-015
```

그러나 검증 상태는 Green이 아니었다.

#### exact PR head

- head: `1b1b9abaf272c6f14ec8580d63236d3af83373e5`
- workflow: `Fiction operating system`
- run: `31357672645`
- conclusion: `FAILURE`

step-level observation:

- Validate fiction operating system: `SUCCESS`
- Validate active fiction canon and manuscript: `SUCCESS`
- Check reverse-outline reproducibility: `SUCCESS`
- Validate reverse-outline analysis: `SUCCESS`
- Validate completed scene passes: `FAILURE`

#### post-merge main

- main: `e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0`
- push workflow run: `31357858310`
- conclusion: `FAILURE`
- failing step: `Validate completed scene passes`

이 evidence가 보여주는 것은 failure의 구체 root cause가 아니다. root cause는 프로젝트 디버깅에서 별도로 확인해야 한다.

여기서 확실히 일반화할 수 있는 것은 다음 상태 분리다.

```text
CANDIDATE_FRONTIER_DATA_EXISTS
!= FRONTIER_VERIFIED_GREEN
```

따라서 derived data와 manuscript가 저장됐더라도 declared validation gate가 실패했다면 `verified_prefix_end=10` 또는 `reconciliation complete`를 최종 truth로 선언해서는 안 된다.

## 4. 외부 벤치마킹

### A. AWS Prescriptive Guidance — ADR best practices

Source:
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html

AWS guidance는 새 architecture decision이 이전 decision을 supersede하더라도 old ADR을 history에 남기고, legacy non-compliant code/artifact는 ADR 자체가 자동 해결하지 않으므로 점진 업데이트하거나 technical-debt task로 관리할 수 있다고 설명한다.

BCP-016과의 대응:

- 채택: decision authority와 artifact migration completion을 분리
- 채택: legacy artifact를 점진적으로 줄이는 lifecycle
- 비채택: software ADR 문서 형식이나 조직 승인 구조를 fiction에 그대로 복제

이는 BCP-012를 지지하며, BCP-016은 그 점진 migration에 **현재 검증 frontier와 파생 continuity 경계**를 더 구체적으로 제안한다.

### B. Martin Fowler / Danilo Sato — Parallel Change

Source:
https://martinfowler.com/bliki/ParallelChange.html

Parallel Change는 backward-incompatible 변경을 한 번에 모든 consumer에 강제하지 않고 `expand → migrate → contract`로 나눠 점진적으로 consumer를 옮긴다. migrate phase에서는 old/new가 한동안 함께 존재하며 모든 consumer가 이동한 뒤 old version을 제거한다.

BCP-016과의 대응:

- 채택: old/new artifact가 공존하는 migration 기간을 정상 상태로 모델링
- 채택: consumer를 bounded하게 점진 이동
- 채택: migration이 끝나기 전 old path 제거 완료를 주장하지 않음
- 비채택: API dual-write, feature flag, database schema를 fiction project에 그대로 강제

차이점:

Parallel Change는 interface compatibility 중심이고 BCP-016은 **narrative continuity와 derived consumer가 미검증 경계를 사실처럼 합성하는 문제**를 추가로 다룬다.

### C. GitHub Docs — three-dot comparison and merge base

Source:
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests

GitHub PR의 three-dot comparison은 base와 topic branch의 merge base 이후 topic branch가 도입한 delta를 중심으로 보여준다. GitHub는 base를 자주 동기화해 혼동을 줄이는 것도 권장한다.

BCP-016과의 대응:

- 채택: stale branch/history 전체보다 current baseline에 대해 실제로 도입하는 delta를 검토
- 채택: baseline이 움직이면 fresh comparison으로 race/staleness 확인
- 비채택: Git diff topology를 narrative chapter topology와 동일 개념으로 취급하지 않음

Coc-Fiction에서 stale PR #9 전체를 merge하지 않고 current main 위 unique delta만 PR #12/#13에서 재구성한 방식과 정합적이다.

## 5. 적대적 검토

### 공격 1 — BCP-012에 이미 전부 있지 않은가?

부분적으로 맞다.

BCP-012는 Canon Decision과 legacy migration debt lifecycle을 소유한다. 그러나 “debt consumer set”은 **어떤 위치가 legacy debt인가**를 말하며, BCP-016은 **어디까지 narrative adjacency가 검증됐고 어느 경계에서 derived continuity를 끊어야 하는가**를 다룬다.

따라서 새 broad Skill은 불필요하지만 검증 상태·파생 edge·frontier 이동을 독립 proposal evidence로 남길 material delta가 있다.

### 공격 2 — Coc-Fiction의 reverse-outline 구조를 Base에 강제하는 것 아닌가?

아니다.

Base 공용 후보는 field name이나 JSON path가 아니라 다음 invariant뿐이다.

```text
unverified migration edge must not become verified derived continuity
```

프로젝트가 이를 null, unknown, migration-boundary 등 어떤 schema로 표현할지는 구현 owner가 결정한다.

### 공격 3 — PR #19가 실패했는데 그것을 성공 사례로 일반화하는가?

아니다.

PR #19는 **실패 반례**다. 저장된 frontier candidate와 verified frontier를 분리해야 한다는 근거다.

현재 이 evidence는 PR #19의 exact-head와 post-merge validation을 Green으로 주장하지 않는다.

### 공격 4 — 5화 단위 작업을 Base 표준으로 만드는가?

아니다.

5화는 Coc-Fiction의 project production unit이며 `PROJECT_ONLY`다. Base에는 bounded scope라는 원리만 남긴다.

### 공격 5 — POV 1~3명, 조연/엑스트라 POV를 Base 규칙으로 넣는가?

아니다.

고정 숫자는 project-only다. 조연/엑스트라 POV가 동일 사건의 정보·감정·외부평가를 실제로 바꿀 때 가치가 있다는 점은 기존 serial-fiction POV/scene-boundary 원칙으로 충분해 새 BCP 범위에서 제외한다.

## 6. 공용 후보 / 프로젝트 전용 판정

| 항목 | 판정 |
|---|---|
| verified prefix / migration boundary / legacy tail | `BASE_CANDIDATE` |
| frontier advance requires declared validation Green | `BASE_CANDIDATE` |
| unresolved migration edge derived-continuity fail-closed | `BASE_CANDIDATE` |
| duplicate current authority fail-closed | `EVIDENCE_ONLY / NEEDS_MORE_PROJECTS` |
| external `최종` label automatic Canon authority 금지 | `REUSE_EXISTING_SERIAL_FICTION_RULES` |
| post-merge continuation self-stale | `REUSE_BCP_013` |
| stale branch whole-history revival 금지 | `REUSE_EXISTING_GIT/FRESHNESS` |
| exact Coc-Fiction override/registry filenames | `PROJECT_ONLY` |
| 5화 work unit | `PROJECT_ONLY` |
| 1~3 POV | `PROJECT_ONLY` |
| 캐릭터별 말투·관계·설정 제한 | `PROJECT_ONLY` |

## 7. 구현 전 필요한 검증

BCP-016이 `APPROVED_FOR_IMPLEMENTATION` 되더라도 다음을 먼저 해야 한다.

1. BCP-012와 owner overlap을 다시 읽는다.
2. 새 Skill 대신 existing serial-fiction owner absorption을 우선 검토한다.
3. fixture는 소설명·인물명·5화 숫자 없이 generic artifact A/B로 작성한다.
4. unresolved boundary가 normal adjacency로 합성되는 RED를 먼저 만든다.
5. candidate frontier with failed validation이 verified prefix로 승격되지 않는 RED를 만든다.
6. minimal Green 뒤 BCP-012/016 책임 중복을 adversarial review한다.
7. active implementation은 별도 승인·별도 PR에서만 한다.

## 8. 현재 판정

```yaml
proposal: BCP-2026-016-serial-fiction-reconciliation-frontier-and-derived-continuity-guard
human_title: BCP - Coc-Fiction
status: SUBMITTED
existing_solution_verdict: MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE
active_base_behavior_change: NONE
new_active_skill: NONE
project_main_validation: FAILURE_OBSERVED
project_failure_root_cause: NOT_DETERMINED_BY_THIS_BCP
```
