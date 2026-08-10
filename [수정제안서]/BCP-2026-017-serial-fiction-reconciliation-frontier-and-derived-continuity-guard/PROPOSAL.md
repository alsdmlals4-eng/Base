# BCP - Coc-Fiction

## 출처와 상태

- Proposal ID: `BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard`
- 사용자 표시명: `BCP - Coc-Fiction`
- 출처 프로젝트: `alsdmlals4-eng/Coc-Fiction`
- 출처 프로젝트 관측 main: `e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0`
- 제출일: `2026-08-10`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `Pattern + Counterexample`
- Existing Solution Verdict: `MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE`
- 활성 Base 구현 승인: `NOT_GRANTED_IN_THIS_STAGE`

이 제안은 Coc-Fiction의 최신 외부 원고와 GitHub legacy 장편 원고를 실제로 묶음 단위 reconciliation하는 과정에서 확인된 **이동하는 reconciliation frontier와 미검증 경계의 파생 연속성 보호 계약**을 Base에 제안한다.

BCP-012 `serial-fiction-canon-migration-debt`는 새 Canon의 즉시 권위와 기존 DRAFT migration debt를 분리하는 공용 lifecycle을 이미 소유한다. BCP-017은 이를 대체하지 않는다. 이번 프로젝트에서 추가로 드러난 것은 다음 edge다.

```text
legacy debt를 bounded하게 알고 있다
!=
현재 어느 지점까지 narrative continuity가 검증되었는지 알고 있다
```

외부 최신 원고와 legacy 저장 원고가 같은 chapter 번호를 공유해도 사건 배치가 다를 수 있으므로, 검증되지 않은 경계를 index·reverse outline·scene graph 같은 파생 consumer가 정상 `previous/next` 관계로 자동 연결하면 사건 되감기나 거짓 continuity가 생성될 수 있다.

BCP-017은 새 broad Skill을 만들자는 제안이 아니다. 승인 후 구현이 필요하다면 기존 `developing-and-revising-serial-fiction: canon-and-continuity`와 `auditing-canonical-reference-freshness` owner에 흡수하는 것을 우선한다.

## 관찰과 증거

### 1. BCP-012 이후 실제 migration에서 frontier가 필요했다

Coc-Fiction PR #14는 새 Canon과 기존 대량 DRAFT 충돌을 즉시 전수 치환하지 않고 bounded legacy reconciliation debt로 분리했다. 이후 외부 최신 제1~105화와 GitHub legacy 저장 원고를 실제 비교하면서 debt 목록만으로는 다음 사실을 표현하기 부족했다.

- 어느 회차까지 source/Canon/adjacent-state 대조가 끝났는가
- 바로 다음 legacy 회차를 정상 연속으로 읽어도 되는가
- 파생 index/reverse outline이 경계 너머를 연결해도 되는가
- 다음 reconciliation 묶음이 통과했을 때 어떤 경계를 앞으로 이동시켜야 하는가

PR #17에서 제1~5화 reconciliation 후 프로젝트는 다음 상태를 사용했다.

```yaml
reconciled_prefix_end: 5
legacy_tail_starts_at: 6
boundary_after_chapter: 5
whole_manuscript_continuity: NOT_YET_CLAIMED
next_bundle: 006-010
```

새 제5화는 legacy 제6화보다 사건이 더 진행된 상태여서 제5→legacy 제6화를 정상 연속으로 두면 이미 지나간 사건이 다시 시작되는 회귀가 생겼다. 프로젝트는 경계를 억지로 연결하지 않고 migration boundary로 차단했다.

### 2. 다음 묶음이 검증되면 frontier는 앞으로 이동한다

PR #19는 제6~10화 external reconciliation을 적용해 의도상 다음 topology로 전진시켰다.

```yaml
reconciled_prefix_end: 10
legacy_tail_starts_at: 11
boundary_after_chapter: 10
next_bundle: 011-015
```

핵심은 `5→6` 경계가 정상 연결 가능한 검증 영역으로 편입되고, 미검증 경계가 `10→11`로 이동한다는 점이다.

따라서 migration debt는 다음 **reconciliation frontier**로도 표현할 수 있다.

```text
VERIFIED_PREFIX
+ DECLARED_MIGRATION_BOUNDARY
+ LEGACY_TAIL
```

다음 bounded pass가 성공하면 prefix는 늘고, boundary는 이동하고, legacy tail은 감소한다.

### 3. 파생 consumer는 unresolved boundary를 정상 continuity로 추론하면 안 된다

프로젝트의 실제 JSON 파일명과 composer 구조는 Coc-Fiction 전용이지만 공용 원리는 다음과 같다.

```text
IF A is reconciled
AND B is legacy/unreconciled
AND A→B continuity is not verified
THEN derived consumers MUST NOT invent normal A→B continuity.
```

동등한 표현은 프로젝트별로 `null`, `UNKNOWN`, `MIGRATION_BOUNDARY`, `UNVERIFIED_EDGE` 등이 될 수 있다. Base가 특정 schema 이름을 강제할 필요는 없다.

### 4. migration debt를 허용해도 canonical ownership ambiguity를 허용해서는 안 된다

PR #17 디버깅에서 한 chapter를 일반 override와 migration-boundary override가 동시에 소유해 composed reverse-outline가 실패했다. 프로젝트는 duplicate guard를 느슨하게 하지 않고 한 current owner만 남도록 overlap을 제거했다.

```text
migration debt allowed
!= duplicate current authority allowed
```

이 항목은 현재 한 프로젝트에서 강하게 확인된 evidence이므로 독립 공용 규칙으로 즉시 승격하지 않고 BCP-017 구현 검토용 반례로 보존한다.

### 5. `최종`이라고 적힌 외부 artifact도 자동 Canon authority가 아니다

외부 최신 원고를 파일명만 보고 blind overwrite하지 않고 bounded bundle마다 다음 순서를 사용했다.

```text
external latest artifact
→ latest user Decision
→ active project Canon
→ available source/original event evidence
→ current manuscript + adjacent state comparison
→ KEEP / APPLY / REWORK / REJECT
→ approved delta promotion
→ coupled consumer update
→ exact-head verification
```

이는 기존 serial-fiction source/Canon priority와 정합적이며 새 Skill을 요구하지 않는다.

### 6. PR #19는 frontier promotion의 중요한 실패 반례다

PR #19는 merged 상태지만 final PR head와 merge 후 main의 `Fiction operating system`이 모두 실패했다.

- PR #19 final head: `1b1b9abaf272c6f14ec8580d63236d3af83373e5`
- exact-head workflow run: `31357672645` → `FAILURE`
- merge 후 main: `e829fecf7e52d2b2aefaa13d0b1e1e689f69dac0`
- post-merge push workflow run: `31357858310` → `FAILURE`
- 실패 단계: `Validate completed scene passes`
- 같은 run에서 operating-system / active Canon+manuscript / reverse-outline reproducibility / reverse-outline analysis는 성공

따라서 “새 prefix 데이터를 저장했다”와 “그 prefix가 strict-clean으로 검증 완료됐다”를 분리해야 한다.

```text
FRONTIER_DATA_UPDATED
!= RECONCILIATION_VERIFIED
```

BCP-017은 candidate frontier가 저장되더라도 **declared validation gate가 Green이 아니면 verified-prefix / reconciliation-complete를 주장하지 않는** fail-closed invariant를 제안한다.

실패 root cause는 이 proposal이 추정하지 않는다. 현재 확인된 사실은 completed scene-pass validator 실패다. Coc-Fiction의 해당 failure 수정은 별도 프로젝트 작업이다.

## Existing Solution First

### BCP-012와의 관계

BCP-012가 이미 소유하는 것:

- 새 Canon Decision과 legacy artifact migration 완료 상태 분리
- `STRICT_NOW`
- `FORBIDDEN_IN_NEW_OR_REVISED`
- `BOUNDED_LEGACY_RECONCILIATION_DEBT`
- `SCOPED_STRICT`
- debt consumer set 증가 fail-closed
- bounded source/canon/continuity reconciliation

BCP-017이 추가하는 material edge:

- 검증 완료 영역과 legacy 영역 사이의 **이동하는 frontier topology**
- unresolved frontier를 파생 consumer가 정상 continuity로 오인하지 않는 계약
- frontier가 이동할 때 이전 경계는 검증 후에만 정상 연결로 승격
- candidate frontier update와 verified-prefix claim 분리
- duplicate current authority를 migration debt와 혼동하지 않는 반례

따라서 BCP-012에 단순 문장 하나 추가하는 수준보다 검증 시나리오와 실패 상태가 독립적이어서 별도 project-source BCP로 보존할 가치가 있다. 구현 단계에서는 BCP-012와 함께 같은 serial-fiction owner에 흡수할 수 있다.

### BCP-013과의 관계

Coc-Fiction PR #15→#16에서 live `ACTIVE_CONTEXT/HANDOFF`가 자기 자신을 운반하는 merge 뒤 즉시 stale해지는 현상도 재현됐다. 이는 이미 BCP-013 `post-merge-continuation-state-reconciliation`이 소유하므로 중복 제안하지 않는다.

### BCP-009와의 관계

BCP-009는 집필·퇴고 품질, source/Canon, POV, continuity discipline의 광역 owner다. 그러나 대량 legacy 저장 원고의 **부분 migration topology와 derived consumer boundary**는 BCP-012 이후 새로 드러난 운영 edge이므로 BCP-017에서 proposal evidence로 분리한다.

### Existing Solution Verdict

`MATERIAL_SCOPE_EXTENSION_NOT_DUPLICATE`

- 신규 broad ACTIVE Skill: `0`
- 구현 후보 owner: 기존 serial-fiction canon/continuity owner
- supporting owner: canonical reference freshness / handoff reconciliation

## 일반화 후보

### Reconciliation Frontier Contract

```text
VERIFIED_PREFIX
DECLARED_MIGRATION_BOUNDARY
LEGACY_TAIL
FRONTIER_VERIFICATION_STATUS
```

### Frontier invariants

1. `VERIFIED_PREFIX`는 선언된 validation gate를 통과한 범위만 포함한다.
2. unresolved boundary 양쪽의 narrative continuity를 자동 확정하지 않는다.
3. 다음 bounded migration 성공 후에만 boundary를 앞으로 이동하고 이전 edge를 normal continuity로 승격한다.
4. legacy tail이 남아 있으면 whole-manuscript reconciliation complete를 주장하지 않는다.
5. current authority ownership이 중복되면 legacy debt 여부와 무관하게 fail-closed한다.
6. external artifact의 라벨·파일명은 Canon authority를 자동 부여하지 않는다.
7. candidate state와 verified state를 구분한다.

필드명과 numeric scope는 예시이며 Base 공용 schema로 강제하지 않는다.

## 프로젝트 전용으로 남길 내용

Base에 올리지 않는다.

- Coc-Fiction의 등장인물·설정·금지 설정명
- 실제 1부/2부/외전 편성
- `001-005`, `006-010` 같은 5화 고정 work unit
- 프로젝트의 구체 index/reverse-outline/scene-pass 파일 경로
- legacy storage의 특정 총 회차수
- 특정 PDF/스프레드시트 파일명과 셀 주소
- 한 화 `1~3 POV` 고정값
- 조연·엑스트라 POV 사용 빈도
- 캐릭터별 대사·관계·능력 제한
- Coc-Fiction PR/run 번호를 Base runtime의 필수 값으로 강제하는 것

POV·후크·캐릭터 QA의 고정 숫자는 project-only다. 조연/엑스트라 POV가 동일 사건의 정보·감정·외부평가를 실제로 바꿀 때 가치가 있다는 점은 기존 Base POV 가치/scene-boundary 필터로 충분해 이 BCP의 공용 승격 범위에서 제외한다.

## 적용 조건과 비사용 조건

### Use When

- 장편/연재 artifact가 많이 존재하고 최신 Canon 또는 편성으로 단계적 migration 중이다.
- 새 artifact와 legacy artifact의 동일 번호가 동일 사건 위치를 보장하지 않는다.
- index, reverse outline, graph, synopsis, scene registry 등 파생 consumer가 adjacent continuity를 자동 생성한다.
- 모든 artifact를 한 번에 안전하게 migration할 수 없어 bounded pass가 필요하다.
- current clean 범위와 unresolved tail을 명확히 분리해야 한다.

### Do Not Use When

- legacy active artifact가 없다.
- migration을 한 번에 안전하게 완료하고 전체 검증할 수 있다.
- old artifact가 archive/reference-only이며 current consumer가 아니다.
- adjacent continuity가 이미 source/canon 대조로 검증됐다.
- 단순 오탈자나 schema key처럼 문맥과 무관한 전수 치환이 안전하게 검증됐다.
- 단지 프로젝트의 work-unit 크기를 Base에 강제하고 싶을 뿐이다.

## 반례와 위험

### Counterexample — 작은 안전 migration

세 개 metadata 파일의 단순 key 이름만 바뀌고 schema migration test가 전부 통과한다면 frontier/legacy tail을 만들 필요가 없다. 한 번에 migration 후 `STRICT_NOW`로 닫는 편이 낫다.

### Risk — frontier가 영구 미완료 상태가 됨

- next bounded scope를 명시한다.
- prefix 증가 / legacy tail 감소를 추적한다.
- failed validation을 PASS_WITH_KNOWN_DEBT로 오인하지 않는다.

### Risk — boundary가 실제 narrative break로 오인됨

migration boundary는 작품 내용의 의도된 장절 경계가 아니다. 데이터 migration 상태임을 명시한다.

### Risk — 파생 consumer마다 다른 authority를 주장함

현재 authority는 하나만 두고 duplicate ownership을 fail-closed한다.

### Risk — validation 일부 성공을 전체 Green으로 오인함

PR #19처럼 여러 검사 중 하나가 실패하면 declared promotion gate 기준으로 전체 verified claim을 중단한다. 어떤 검사가 blocking인지는 각 프로젝트 계약이 정한다.

## 벤치마킹

상세 근거는 `evidence/COC_FICTION_RECONCILIATION_FRONTIER_EVIDENCE.md`가 책임진다.

- AWS ADR guidance: Decision이 supersede되어도 legacy non-compliant artifact는 자동 해결되지 않으며 점진 migration 또는 debt task로 별도 관리할 수 있다.
- Martin Fowler / Danilo Sato의 Parallel Change: backward-incompatible change를 `expand → migrate → contract`로 나눠 consumer를 점진 이동한다.
- GitHub Docs의 three-dot comparison: merge base 이후 topic branch가 도입한 delta를 중심으로 검토한다.

이 원칙들은 BCP-017과 방향이 유사하지만 software ADR/API/Git diff schema 자체를 fiction에 복제하지 않는다.

## 영향 범위와 검증

이번 단계는 proposal storage만 수행한다.

변경 허용:

- `[수정제안서]/BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard/PROPOSAL.md`
- `[수정제안서]/BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard/evidence/COC_FICTION_RECONCILIATION_FRONTIER_EVIDENCE.md`
- `[수정제안서]/PROPOSAL_REGISTRY.json`

변경 금지:

- `skills/**`
- `templates/**`
- `tests/**`
- `.github/workflows/**`
- active methods/guides
- `START_HERE.md`
- release lock/frozen snapshot
- Coc-Fiction repository files

### 향후 구현 시 우선 검토할 기존 owner

1. `developing-and-revising-serial-fiction: canon-and-continuity`
2. `auditing-canonical-reference-freshness`
3. BCP-012 implementation contract와의 결합
4. BCP-013은 post-merge live continuation truth에만 supporting link

### 검증 시나리오

#### Scenario A — frontier advances only after Green

Given prefix 1~5 is verified and 6~10 is candidate migration,
when the declared validation gate passes,
then prefix may advance to 10 and boundary moves after 10.

If validation fails, stored candidate data may exist but `VERIFIED_PREFIX_END=10` 또는 `RECONCILIATION_COMPLETE`를 주장하지 않는다.

#### Scenario B — unresolved boundary blocks false continuity

Given chapter A is reconciled and chapter B is legacy with unverified event placement,
when derived continuity is generated,
then A→B normal next/previous relation is not asserted.

#### Scenario C — duplicate authority fails

Given two active migration consumers claim current authority over the same artifact,
when composed state is built,
then validation fails until one owner remains.

#### Scenario D — external final label is insufficient

Given an external file labelled `최종`,
when event placement differs from current storage,
then promotion requires current user Decision + Canon + source/adjacent-state comparison.

#### Scenario E — full migration completion

Given legacy tail reaches zero and all declared consumers pass validation,
then and only then may whole-artifact migration complete be claimed.

### Compatibility / security / cost

- migration이 없는 프로젝트에는 영향 없음
- BCP-012/013을 supersede하지 않음
- existing archive/history rewrite 강제 없음
- 특정 fiction data schema 도입 강제 없음
- secret·권한·runtime write 추가 없음
- 너무 작은 migration까지 frontier로 모델링하면 비용이 커지므로 Do Not Use 조건 유지

### 롤백

이번 proposal-only PR은 `[수정제안서]/**` 세 파일만 변경한다. 문제가 있으면 proposal/Registry delta만 revert할 수 있으며 Base active behavior와 프로젝트 원고에는 영향이 없다.

## 승인과 구현

- `BCP - Coc-Fiction` proposal storage와 `[수정제안서]` 병합: 사용자 직접 요청으로 승인됨
- proposal status: `APPROVED_FOR_IMPLEMENTATION`
- Registry 등록: 이번 proposal storage 범위에 포함
- active Base implementation: `AUTHORIZED_WITH_BCP_012_MINIMAL_ABSORB_2026_08_10`
- approval_ref: `[수정제안서]/BCP-2026-017-serial-fiction-reconciliation-frontier-and-derived-continuity-guard/PROPOSAL.md#승인과-구현`
- BCP-013 active implementation 승인으로 해석하지 않음
- 사용자는 2026-08-10 KST 대화에서 `좋아 다 승인할게 [연속작업] 진행해`로 BCP-012와 결합한 기존 serial-fiction/freshness owner 최소 흡수를 승인했다. 프로젝트별 work-unit 수, Canon, 파일 경로, 원고 내용은 제외한다.
