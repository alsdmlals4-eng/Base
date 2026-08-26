# 2026-08-26 Fresh-Read Project Portfolio Audit

## Status

```text
LIVE_NOTION_READBACK_2026_08_26
PHYSICAL_IA_REUSE_NO_REMIGRATION
FRESH_READ_RECONSTRUCTION_AUDITED
```

목적은 2026-08-24에 이미 검증된 `Project Hub → Human Home → Project Domain → Detail/Record` 물리 IA를 다시 뜯어고치는 것이 아니라, 현재 10개 Project Human Home과 각 프로젝트 GitHub를 fresh-read하여 새 채팅이 과거 대화 없이 현재 품질·보호선·다음 안전 작업·evidence ceiling을 복원할 수 있는지 확인하는 것이다.

## 방법 비교

1. 모든 Project Home을 다시 reparent/remigrate — 기각. 2026-08-24 migration/readback을 불필요하게 반복하고 링크·relation·사람의 탐색 기억을 깨뜨릴 위험이 크다.
2. 새 중앙 resume dashboard를 만들어 10개 프로젝트 상태를 복제 — 기각. cross-project second canon과 stale snapshot을 만든다.
3. 기존 IA를 유지하고 Handoff owner의 Fresh-Read Bootstrap을 각 Human Home의 진입 계약으로 연결한 뒤 결함만 bounded correction — 채택.

## Live portfolio

| Project | GitHub latest observed | Notion Human Home | IA | Fresh-read finding |
|---|---|---|---|---|
| COC-Fiction | `677ff14d965a1a38b9d74b1fff98751d198bb188` | `3c41b237-eb1c-811d-9579-e5c8ce05daab` | REUSE | pause/resume handoff가 이미 존재하며 공용 bootstrap 진입문만 표준화 필요 |
| 괴이기록국 | `4c1a7a51edc46a71af2a180a05220cae9254faca` | `3c41b237-eb1c-81dc-9bda-d72bf2d5978d` | REUSE | cold-start handoff와 Recovery current decision 존재; 공용 bootstrap 표준화 필요 |
| 오멘워드 | `74a521a0a4b330ca59334cd38d05e978489a9898` | `3c41b237-eb1c-816f-bbc8-e2dddc18b6eb` | REUSE | mutable current-main routing을 fresh-read하도록 이미 교정됨; 공용 bootstrap 표준화 필요 |
| GRIMOIRE | `829094fd87433e14fe42b23f9b7bec6321f5048d` | `3c41b237-eb1c-816c-80d0-dfcfe28ec973` | REUSE | visual approval-boundary learning 최신화됨; 공용 bootstrap 표준화 필요 |
| 닌자 서바이벌 | `3c3e622aa8932cda7e9e926bf95aba3bd5122631` | `3c41b237-eb1c-81aa-a4e0-e208ba4fb15e` | REUSE | fresh main/current pointer self-staleness 방지가 이미 적용됨; 공용 bootstrap 표준화 필요 |
| 블랙스미스 | `5c29af1e0bb633f8d4513aee16987a3ff9889a4b` | `3c41b237-eb1c-813f-a481-e415e3250d1c` | REUSE | cold-start handoff는 있으나 product runtime은 blocked라는 evidence ceiling 유지 필요 |
| 십보강호 | `aec000790c416dd449eaa01b7e52187b35120ecc` | `3c41b237-eb1c-8105-a254-d860f3c21638` | REUSE | visual handoff postmerge와 다음 3-image batch가 current next work; 공용 bootstrap 표준화 필요 |
| Tetris | `5f52c1c60bc12b2b4b49c7b39054921c048f2d6b` | `3c41b237-eb1c-8199-85b3-e798e938c80b` | REUSE | Living GDD Home architecture가 이미 새 IA를 소유; Draft BUILD PR 격리 유지 필요 |
| Switchy Express | `4219f4e5e342c09024190e3fdaefa7a20051c988` | `3c41b237-eb1c-8103-9537-ede6dfc5f07e` | REUSE | fresh-chat visual handoff가 이미 구현됨; visual reference를 runtime proof로 올리지 않음 |
| 마이 리틀 보트 | `d5482ca7b4b38a3d45932fe354a64f8f33eebc` | `3c41b237-eb1c-8194-8b8e-d88362cafafa` | REUSE | visual closeout/handoff evidence가 postmerge correction됨; 공용 bootstrap 표준화 필요 |

## Notion correction disposition

`PHYSICAL_IA_REUSE_NO_REMIGRATION`: 10개 모두 L1 Human Home과 하위 Project Domain 구조가 존재하고 최근 프로젝트 내용이 반영되어 있으므로 물리 reparent/remigration은 하지 않는다.

공통 bounded correction은 각 Human Home 상단에 다음 의미를 한 번만 노출하는 것이다.

```text
FRESH-READ BOOTSTRAP
→ past conversation not required
→ exact Project GitHub + this Notion Home
→ reconstruct project identity / current goal / current quality and stage / protected scope / next safe action / evidence ceiling
→ GitHub↔Notion mismatch => CONTEXT_DRIFT_RECHECK_REQUIRED before mutation
```

기존 프로젝트 고유 Home 내용·Visual·Domain link·현재 Decision을 덮어쓰지 않는다.

## Post-write destination readback

`NOTION_BOOTSTRAP_DESTINATION_READBACK_10_OF_10_PASS`

2026-08-26 bounded insert 뒤 workspace search로 10개 대상 Human Home 모두에서 `FRESH-READ BOOTSTRAP`과 reconstruction chain을 다시 확인했고, 이어서 각 exact page ID를 직접 fetch해 상단 callout과 기존 프로젝트별 Living GDD/Visual/current decision 본문이 함께 보존되어 있음을 확인했다.

| Project | exact destination fetch | Bootstrap at top | Existing project-specific content preserved |
|---|---|---|---|
| COC-Fiction | PASS | PASS | PASS |
| 괴이기록국 | PASS | PASS | PASS |
| 오멘워드 | PASS | PASS | PASS |
| GRIMOIRE | PASS | PASS | PASS |
| 닌자 서바이벌 | PASS | PASS | PASS |
| 블랙스미스 | PASS | PASS | PASS |
| 십보강호 | PASS | PASS | PASS |
| Tetris | PASS | PASS | PASS |
| Switchy Express | PASS | PASS | PASS |
| 마이 리틀 보트 | PASS | PASS | PASS |

이 PASS는 **Notion destination content readback**이다. 독립 사용자가 실제로 blind cold-start를 수행해 같은 판단 품질을 재현했다는 Human usability 증거로 승격하지 않는다.

## Implementation Reality Gate

- GitHub: 10개 repository의 latest observed commit/current handoff direction을 fresh-read했다.
- Notion: 10개 Human Home의 current content/IA를 live-read했고, bounded insert 뒤 10/10 exact destination fetch readback을 완료했다.
- 구조 판정: 기존 physical IA를 재사용해도 된다는 evidence가 있다.
- Fresh-Read Bootstrap: Base reference + owning Skill direct discovery + Handoff template + 10개 Home callout의 실제 readback으로 검증한다.
- Runtime/player evidence: 이 작업은 project runtime을 변경하지 않는다.
- `HUMAN_USABILITY_NOT_RUN`: 완전히 독립된 새 인간/agent가 10개 프로젝트를 blind cold-start하여 동일 품질로 수행하는 실험은 이번 scope에서 실행하지 않았다.
- 따라서 `TRANSFER_ACCEPTED`나 인간 사용성 PASS를 과장하지 않는다.

## Revisit conditions

다음 중 하나가 실제로 발생할 때만 물리 IA 재설계를 다시 검토한다.

- Home을 읽어도 core loop/current state/next work/protected scope를 복원할 수 없는 프로젝트가 반복적으로 발생
- Project Domain이 4~6개 범위를 크게 벗어나 탐색비용이 증가
- cross-project relation leakage/duplicate-key conflict가 재발
- 실제 receiver cold-start test에서 동일 유형의 navigation failure가 2개 이상 프로젝트에서 반복

그 전까지는 `reuse IA + bounded correction`이 장기 총비용이 가장 낮은 기본안이다.
