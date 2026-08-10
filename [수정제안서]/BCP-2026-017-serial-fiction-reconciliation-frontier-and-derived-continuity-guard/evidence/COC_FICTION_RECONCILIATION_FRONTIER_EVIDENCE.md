# BCP-2026-017 Evidence — Coc-Fiction Reconciliation Frontier

## 증거 목적

공용화 대상은 작품의 설정·회차 숫자가 아니라 다음 네 가지다.

1. verified prefix와 legacy tail 사이의 moving frontier
2. unresolved migration boundary에서 derived continuity fail-closed
3. migration debt와 duplicate current authority 구분
4. candidate migration state와 verified promotion state 분리

## 프로젝트 기준점

```yaml
repository: alsdmlals4-eng/Coc-Fiction
observed_main: e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0
observed_at: 2026-08-10
project_state_warning: CURRENT_MAIN_VALIDATION_FAILURE_OBSERVED
```

현재 main을 Green으로 주장하지 않는다. PR #19의 merged state와 failed validation 자체가 BCP-017의 중요한 반례다.

## 프로젝트 lineage

### PR #13 — operating integration

- current Base와 Coc-Fiction 운영 구조 재대조
- stale PR 전체 branch 대신 current-main 위 unique delta만 선택 흡수
- 새 여섯 번째 project Skill 생성 거절
- fixed `1~3 POV`의 Base-wide 승격 거절

### PR #14 — Canon sync + bounded legacy debt

- latest user Decision을 current Canon으로 승격
- 기존 legacy manuscript blind rewrite 금지
- strict-global 초기 시도에서 legacy debt 노출
- `STRICT_NOW / FORBIDDEN_IN_NEW_OR_REVISED / BOUNDED_LEGACY_RECONCILIATION_DEBT / SCOPED_STRICT`로 lifecycle 분리

이 단계가 BCP-012의 직접 출처다.

### PR #15 / #16 — continuation self-stale

PR #15가 live continuation 문서에 당시 main SHA를 저장했지만 merge 순간 그 값이 historical snapshot이 됐다. PR #16에서 stable `main`과 `last_observed_main_sha`, last integrated PR, post-merge CI, resume-time fresh read 의미를 분리했다.

이 문제는 BCP-013이 소유하므로 BCP-017에서 중복 일반화하지 않는다.

### PR #17 — Ch1~5 first external reconciliation

외부 최신 제1~5화를 GitHub legacy 저장 원고에 그대로 덮어쓰지 않고 source/Canon/user Decision/adjacent state로 대조했다.

새 제5화가 legacy 제6화보다 사건상 더 뒤까지 진행돼 있어 정상 5→6 연결은 사건 되감기였다.

```yaml
reconciled_prefix_end: 5
legacy_tail_starts_at: 6
boundary_after_chapter: 5
whole_manuscript_continuity: NOT_YET_CLAIMED
next_bundle: 006-010
```

파생 reverse outline에서도 경계를 정상 `next/previous`로 만들지 않았다.

검증 evidence:

- PR #17 final head: `31a4d959cef54ad77576672ff7cca8a53db72c42`
- exact-head run: `31355669160` → `SUCCESS`
- project main after merge: `9a7b2e2419465bd76daf0cf09b96ed7c0cd7d54c`
- post-merge run: `31355813027` → `SUCCESS`

### duplicate ownership debugging

migration boundary와 일반 override가 같은 chapter를 동시에 소유한 중간 시도에서 composed consumer가 duplicate chapter를 거부했다.

```text
duplicate ownership
→ guard 유지
→ overlapping owner 제거
→ current authority 하나만 남김
→ regenerate
```

따라서:

```text
KNOWN_LEGACY_DEBT
!= AMBIGUOUS_CURRENT_AUTHORITY
```

### PR #19 — Ch6~10 candidate frontier advance + failed validation

PR #19는 외부 최신 제6~10화를 적용하고 의도상 frontier를 다음처럼 이동시켰다.

```yaml
candidate_reconciled_prefix_end: 10
candidate_legacy_tail_starts_at: 11
candidate_boundary_after_chapter: 10
candidate_next_bundle: 011-015
```

하지만 validation은 Green이 아니었다.

exact PR head:

- `1b1b9abaf272c6f14ec8580d63236d3af83373e5`
- run `31357672645`
- conclusion `FAILURE`

step observation:

- Validate fiction operating system: `SUCCESS`
- Validate active fiction canon and manuscript: `SUCCESS`
- Check reverse-outline reproducibility: `SUCCESS`
- Validate reverse-outline analysis: `SUCCESS`
- Validate completed scene passes: `FAILURE`

post-merge:

- main `e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0`
- run `31357858310`
- conclusion `FAILURE`
- failing step `Validate completed scene passes`

이 evidence는 failure의 root cause를 추정하지 않는다. 확정 가능한 일반화는 다음뿐이다.

```text
CANDIDATE_FRONTIER_DATA_EXISTS
!= FRONTIER_VERIFIED_GREEN
```

따라서 declared validation gate가 실패하면 candidate data가 저장돼 있어도 verified-prefix 또는 reconciliation-complete를 최종 truth로 승격하지 않는다.

## 외부 벤치마킹

### AWS Prescriptive Guidance — ADR best practices

Source:
https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html

AWS는 새 Decision이 이전 것을 supersede해도 non-compliant legacy code/artifact가 자동 해결되지 않으며, 점진 업데이트 또는 technical-debt task로 별도 관리할 수 있다고 설명한다.

채택:
- decision authority와 artifact migration completion 분리
- legacy artifact 점진 축소 lifecycle

비채택:
- software ADR 양식을 fiction에 그대로 강제

### Martin Fowler / Danilo Sato — Parallel Change

Source:
https://martinfowler.com/bliki/ParallelChange.html

Parallel Change는 backward-incompatible change를 `expand → migrate → contract` 단계로 나눠 old/new consumer를 일정 기간 함께 지원하며 점진 migration한다.

채택:
- migration 기간의 old/new coexistence
- bounded consumer migration
- migration 완료 전 old path 제거 완료를 주장하지 않음

비채택:
- API dual-write, feature flag, database schema를 fiction에 그대로 강제

BCP-017의 추가 edge는 software interface compatibility가 아니라 **narrative continuity consumer가 미검증 경계를 사실처럼 합성하지 않도록 하는 것**이다.

### GitHub Docs — three-dot comparison

Source:
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests

GitHub PR의 three-dot comparison은 merge base 이후 topic branch가 도입한 delta를 중심으로 보여준다. base가 이동하면 baseline을 다시 동기화해 차이를 명확히 하는 것을 권장한다.

채택:
- stale history 전체보다 current baseline에 대한 unique delta 검토
- baseline 이동 시 fresh comparison

비채택:
- Git graph와 narrative graph를 동일 schema로 취급

## 적대적 검토

### “BCP-012에 이미 전부 있지 않은가?”

BCP-012는 Canon Decision과 legacy migration debt lifecycle을 소유한다. BCP-017은 **현재 어느 adjacency까지 검증됐고 어떤 derived edge를 차단해야 하는지**, candidate frontier가 verification 실패했을 때 어떤 claim을 금지하는지를 추가한다.

### “Coc-Fiction reverse-outline 구조를 Base에 강제하는가?”

아니다. 공용 후보는 다음 invariant뿐이다.

```text
unverified migration edge must not become verified derived continuity
```

### “PR #19 실패를 성공 사례로 포장하는가?”

아니다. PR #19는 실패 반례다. 정확히 그 때문에 candidate state와 verified state 분리가 필요하다.

### “5화 단위, 1~3 POV를 Base 표준화하는가?”

아니다. 둘 다 project-only다.

## 공용 후보 / 프로젝트 전용 판정

| 항목 | 판정 |
|---|---|
| verified prefix / migration boundary / legacy tail | `BASE_CANDIDATE` |
| frontier advance requires declared validation Green | `BASE_CANDIDATE` |
| unresolved migration edge derived-continuity fail-closed | `BASE_CANDIDATE` |
| duplicate current authority fail-closed | `EVIDENCE_ONLY / NEEDS_MORE_PROJECTS` |
| external `최종` label automatic Canon authority 금지 | `REUSE_EXISTING_SERIAL_FICTION_RULES` |
| post-merge continuation self-stale | `REUSE_BCP_013` |
| stale branch whole-history revival 금지 | `REUSE_EXISTING_GIT/FRESHNESS` |
| Coc-Fiction 구체 data file paths | `PROJECT_ONLY` |
| 5화 work unit | `PROJECT_ONLY` |
| 1~3 POV | `PROJECT_ONLY` |
| 캐릭터별 규칙 | `PROJECT_ONLY` |

## 구현 전 필요한 검증

1. BCP-012 owner overlap 재확인
2. 새 Skill보다 existing serial-fiction owner absorption 우선
3. generic artifact A/B fixture 사용
4. unresolved boundary가 normal adjacency로 합성되는 RED 작성
5. candidate frontier with failed validation이 verified prefix로 승격되는 RED 작성
6. minimal Green 후 BCP-012/017 책임 중복 적대적 검토
7. 별도 구현 승인·별도 구현 PR

## 현재 evidence 판정

```yaml
proposal: BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard
human_title: BCP - Coc-Fiction
status: SUBMITTED
existing_solution_verdict: MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE
active_base_behavior_change: NONE
new_active_skill: NONE
project_main_validation: FAILURE_OBSERVED
project_failure_root_cause: NOT_DETERMINED_BY_THIS_BCP
```
