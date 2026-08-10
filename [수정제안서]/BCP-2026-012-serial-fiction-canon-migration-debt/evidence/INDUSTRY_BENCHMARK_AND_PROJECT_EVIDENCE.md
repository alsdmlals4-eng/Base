# BCP-2026-012 Evidence — Industry Benchmark + Coc-Fiction Case

## 1. 프로젝트 실증

### Source

- project: `alsdmlals4-eng/Coc-Fiction`
- integrated operating merge: PR #13
- Canon sync merge: PR #14
- verified project main: `c9c4fa647c833470759ada2514e45d1b2abb1e8b`

### Case timeline

1. 최신 사용자 Decision이 과거 독립 설정을 폐기하고 새 자기통제 규칙을 Canon으로 만들었다.
2. 2부 특정 인물축 제외와 다른 인물 허용도 최신 Canon으로 올려야 했다.
3. 첫 validator는 폐기 설정을 current manuscript strict-global ban으로 정의했다.
4. GitHub Actions run `31351564487`이 기존 DRAFT 여러 bundle의 legacy usage를 노출했다.
5. 이 실패를 기계 치환으로 해결하면 원본·Canon·앞뒤 continuity 직접 대조 절차를 우회하는 문제가 있었다.
6. strict-current / new-or-revised / bounded-debt / scoped-strict를 분리한 뒤 exact debt set을 고정했다.
7. final exact-head run `31351829221`과 merged-main run `31351884525`가 성공했다.
8. 실제 manuscript 파일은 이 Canon-sync PR에서 수정하지 않았다.

### 실패했던 접근

```text
NEW_CANON
→ put every superseded term into global current-manuscript forbidden list
→ fail every legacy DRAFT immediately
→ implied mass rewrite
```

실패 이유:

- Decision의 현재 유효성과 이전 DRAFT의 migration 완료 상태를 동일시했다.
- long-form prose에서 문자열 제거가 장면 인과·관계·설정 의미의 안전한 migration을 보장하지 않는다.
- source/canon reconciliation을 건너뛸 유인이 생긴다.

### 검증된 프로젝트 해결

```text
STRICT_NOW
FORBIDDEN_IN_NEW_OR_REVISED
BOUNDED_LEGACY_RECONCILIATION_DEBT
SCOPED_STRICT
```

bounded debt는 actual consumer set과 declared consumer set이 정확히 같아야 한다. debt가 새 위치로 퍼지면 CI가 실패하며, 기존 debt 제거는 별도 source/canon revision에서 수행한다.

## 2. 외부 벤치마킹

### A. AWS Prescriptive Guidance — ADR lifecycle

Source:
`https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html`

외부 방식:

- accepted Decision record는 history로 보존한다.
- 새 insight로 Decision이 바뀌면 새 ADR을 만들고 이전 ADR을 `Superseded`로 바꾼다.
- Decision log는 review와 implementation 판단의 기준으로 사용한다.

Base 현재 방식:

- 사용자 Decision·Canon·source priority를 먼저 고정한다.
- superseded project Canon과 legacy material을 구분한다.

차이:

- Base serial-fiction owner는 새 Decision 이후 기존 대량 DRAFT의 migration 상태를 별도 lifecycle로 명시하지 않는다.

채택:

- old Decision history를 삭제하지 않고 superseded 상태로 보존.
- new Decision authority와 artifact migration completion을 분리.

비채택:

- software architecture ADR의 문서 형식이나 승인 조직 구조를 fiction에 그대로 복제하지 않는다.

### B. AWS Prescriptive Guidance — legacy non-compliance

Source:
`https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/best-practices.html`

외부 방식:

- ADR process만으로 non-compliant legacy code는 자동 해결되지 않는다.
- legacy artifact는 새 변경과 함께 점진적으로 갱신하거나 별도 technical-debt task로 관리할 수 있다.

Base와의 차이:

- Coc-Fiction 사례에서 정확히 같은 종류의 문제가 prose artifact에서 발생했다. 새 Canon은 확정됐지만 이전 DRAFT가 즉시 모두 정리된 것은 아니었다.

채택:

- bounded legacy migration debt를 명시적으로 관리.
- debt 존재를 clean completion으로 과장하지 않음.

비채택:

- 일반 software technical debt taxonomy 전체를 fiction workflow에 추가하지 않는다.

### C. GitHub Docs — PR diff와 stale branch

Sources:

- `https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-comparing-branches-in-pull-requests`
- `https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch`

외부 방식:

- GitHub PR three-dot diff는 merge base부터 topic branch가 도입하는 변경에 초점을 둔다.
- base와 branch를 동기화해 conflicts와 test failure를 merge 전에 발견한다.

프로젝트 적용:

- stale PR #9 전체를 병합하지 않고 current-main 기반 #12와 patch를 비교해 unique delta만 PR #13에 흡수했다.

판정:

- 이 패턴은 Base의 stale/fresh evidence·adversarial 절차로 이미 충분히 커버된다. **별도 BCP 후보에서 제외 (`REUSE / NO_PROMOTION`)**.

### D. Reedsy — multiple POV

Source:
`https://reedsy.com/blog/guide/point-of-view/multiple-points-of-view/`

외부 방식:

- 추가 POV는 story understanding에 실제 필요성이 있어야 한다.
- scene/chapter break에서 새 viewpoint를 빠르게 식별한다.
- mid-scene head-hopping을 피한다.

프로젝트 적용:

- Coc-Fiction 1~105화 재퇴고에서 주연뿐 아니라 조연·엑스트라 POV를 새 정보·외부평가·직업 관찰을 줄 때만 사용했다.
- `1~3 POV`는 작품별 production value로 유지했다.

Base 현재 방식:

- `developing-and-revising-serial-fiction`은 이미 POV를 knowledge/attention/misreading/value/language filter로 정의한다.

판정:

- generic POV value gate는 **`REUSE / NO_PROMOTION`**.
- fixed 1~3 count는 **`PROJECT_ONLY`**.

## 3. Existing Solution First 판정표

| Finding | Base coverage | Verdict | Result |
|---|---|---|---|
| stale PR unique-delta recovery | GitHub diff + Base freshness/adversarial | REUSE | No BCP |
| post-merge main verification | Base operating rules | REUSE | No BCP |
| approval reuse | intake/continuous-work | REUSE | No BCP |
| exact-head evidence freshness | validation/reference freshness | REUSE | No BCP |
| 1~3 POV | project production value | NO_PROMOTION | Project only |
| supporting/extra POV value | serial-fiction POV filter | REUSE | No BCP |
| Coc-Fiction index/override/Scene Pass propagation | project-specific consumers | SPLIT | Project only exact paths |
| post-Decision legacy DRAFT migration lifecycle | owner exists, lifecycle gap remains | ABSORB | BCP-012 |

## 4. Generalization boundary

### Generalizable

- Decision authority and artifact migration completion are separate states.
- legacy active artifacts can be a bounded debt set instead of pretending either full compliance or unrestricted drift.
- new debt growth must fail closed.
- debt removal should be verified through the domain's real reconciliation process.
- scoped rules stay scoped.

### Project-only

- `복종인자`, `블랙킹`, Versilla aliases, Akim.
- exact chapter/bundle paths.
- 5-chapter production batch size.
- TRPG/PDF source names.
- exact Canon JSON schema used by Coc-Fiction.

## 5. Knowledge level

`Pattern`

Why not `Validated Pattern` yet:

- exact TDD evidence exists in Coc-Fiction.
- external ADR guidance provides a strong analogous lifecycle.
- however a second independent serial-fiction project has not yet piloted the rule.

Promotion to `Validated Pattern` requires at least a second fixture/project or comparable independent evidence that the lifecycle prevents both false mass rewrites and uncontrolled legacy spread.
