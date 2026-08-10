# 주기적 게임 개발 외부 Source Watchlist

```yaml
watchlist_role: periodic-external-game-development-source-discovery
owner_method: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
initial_bootstrap_window: 2026-02-10..2026-08-10
recommended_default_cadence: weekly
scheduler_authority: EXTERNAL_TO_BASE
```

## 1. 목적

이 Watchlist는 게임 기획·Godot 개발·UX·접근성·아트·프로덕션·플레이테스트·성능·출시·마케팅·AI 협업에 도움이 될 수 있는 외부 자료를 **주기적으로 발견**하기 위한 공용 Reference다.

이 문서는 새 Skill이 아니며 외부 글을 Base 정본으로 만드는 권한도 없다. 실제 판정은 `EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md`의 Evidence tier와 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`, 현행 Base Work Mode·Skill·적대적 검토·BCP 경계를 따른다.

Base는 scheduler·webhook·백그라운드 실행기가 아니다. 실제 주기 실행은 ChatGPT Automation, GitHub Actions 또는 사용자가 선택한 외부 scheduler가 소유한다. 실행되지 않은 scan을 완료로 보고하지 않는다.

## 2. Source role과 Evidence tier는 다르다

`source_role`은 **어디를 어떻게 훑을지**를 정한다. `source_tier`는 실제 후보 하나가 어느 정도 권위를 갖는지를 정한다.

| source_role | 의미 | 기본 취급 |
|---|---|---|
| `AUTHORITY_TARGET` | 플랫폼·엔진·표준·공식 정책·공식 SDK/도구 | 해당 제품·플랫폼 사실에는 T1 후보. 다른 플랫폼의 보편 법칙으로 확대 금지 |
| `PROFESSIONAL_PRACTICE` | 현업 발표·개발자 회고·전문 실무 가이드 | T2 후보. 팀 규모·장르·예산·도구 차이를 함께 기록 |
| `DISCOVERY_FEED` | 여러 원문을 빠르게 발견하는 큐레이션·뉴스·뉴스레터 | 발견 역할만 기본. 원출처 역추적 전 T1/T2 권위 없음 |
| `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE` | 시장 관찰·벤치마크·분석 도구·벤더 실무 자료 | 표본·기간·방법·이해관계와 함께 사용. 공식 플랫폼 사실로 과장 금지 |

## 3. 핵심 Source Pool

### 3.1 `AUTHORITY_TARGET`

| Source | scan surface | 주요 용도 | 한계·재검증 |
|---|---|---|---|
| **Godot Engine official docs / blog / releases** | `godotengine.org/blog`, release pages, migration docs | stable/RC/maintenance, breaking change, migration, editor/runtime 기능, 지원 정책 | 프로젝트 적용 전 exact Godot version·migration guide·known issue 재확인 |
| **Valve Steamworks Documentation / Blog** | `partner.steamgames.com/doc`, Steamworks news | Demo, Wishlist, Visibility, Store, SteamPipe, release/marketing 기능 | 제3자 Steam 알고리즘 추정보다 우선. 문서 변경 가능하므로 출시 전 재확인 |
| **Android Developers – Games** | `developer.android.com/games`, games release notes | Android performance, thermal/CPU/GPU, Play Games Services, SDK migration, controller, quality | 기기·Android version·SDK version에 따라 다름 |
| **Google Play Developer Policy / Policy Deadlines** | Play Console Help policy/deadline pages | 정책 효력일, metadata, 기능/UX, 계정·배포 요건 | 법률 자문 아님. 효력일·지역·계정 조건 재확인 |
| **Xbox Accessibility Guidelines** | Microsoft Game Dev accessibility guidelines | text, contrast, input, motion, objectives, audio, UI context, 접근성 검수 질문 | 접근성 아이디어·guardrail이며 법적 인증 체크리스트가 아님 |
| **AMD GPUOpen** *(2026 bootstrap에서 추가)* | `gpuopen.com` articles/tools | GPU profiling, graphics performance, crash debugging, AMD toolchain | AMD 하드웨어·도구에 대한 공식성만 T1. 범용 엔진/타 GPU 법칙으로 확대 금지 |

### 3.2 `PROFESSIONAL_PRACTICE`

| Source | scan surface | 주요 용도 | 한계·재검증 |
|---|---|---|---|
| **GDC Vault** | 연도·category index, postmortem/design/production talks | 실제 프로젝트 설계·생산·성능·AI·접근성·postmortem | 발표자의 프로젝트 조건을 보존하고 AAA 관행을 소규모 팀에 그대로 강제하지 않음 |
| **Game Developer** | design / production / marketing / business sections | 개발자 인터뷰, 디자인 의도, 제작 문제, 업계 변화 | 기사 요약과 개발자 원 발언 구분. 오래된 Steam 추정은 공식 Steamworks로 재검증 |
| **Games User Research** | articles / Playtest Masterclass | research question, 관찰, study timing, playtest maturity | 상업 서비스 이해관계가 있으므로 방법 원리와 서비스 홍보를 분리 |
| **80 Level** | gamedev / environment / technical-art interviews | technical art, asset pipeline, environment workflow, tool friction | 개별 artist/studio 사례가 많아 보편 규칙으로 승격 금지; sponsored 여부 기록 |
| **The Level Design Book** | process / blockout / playtesting pages | blockout, metrics, wayfinding, 빠른 in-engine iteration | 업데이트 빈도가 낮은 종합 Reference. 프로젝트 장르에 따라 적용성 다름 |
| **Game Accessibility Guidelines** | Basic/Intermediate/Advanced/full list | 접근성 아이디어, early feedback, 실무 체크 질문 | 공식 플랫폼 정책이나 법적 인증이 아님; 실제 장애 당사자 검증을 대신하지 않음 |
| **How To Market A Game** *(2026 bootstrap에서 추가)* | recent posts / benchmark pages / Next Fest tracker | Steam Next Fest·wishlist·demo·launch 실측 벤치마크와 indie 사례 | 설문 표본·자기선택 편향·시기별 Steam 변화 명시. 숫자를 universal target으로 고정 금지 |
| **Deconstructor of Fun** *(2026 bootstrap에서 추가)* | blog categories: AI, business, game mechanics, data | 모바일/라이브옵스/게임 비즈니스·AI 도입 사례, operator 관점 | mobile/F2P/컨설팅 관점이 강함. 1인 premium PC 게임에 직접 일반화 금지 |

### 3.3 `DISCOVERY_FEED`

| Source | scan surface | 주요 용도 | 한계·재검증 |
|---|---|---|---|
| **Hada GeekNews** | `news.hada.io` 최신/주제 | AI agent, 개발 생산성, UX, 도구, 보안, 새로운 원문 발견 | 큐레이션·요약 자체는 권위가 아님. 반드시 가능한 원출처로 `ORIGINAL_SOURCE_BACKTRACE` |
| **GameDiscoverCo newsletter** | archive / individual posts | Steam/PC/console discovery, 시장·festival 관찰, 사례 후보 발견 | 일부 자체 추정·유료 데이터·sponsor가 존재. 공식 Valve 규칙과 분리하고 표본/추정 표시 |

### 3.4 `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE`

| Source | scan surface | 주요 용도 | 한계·재검증 |
|---|---|---|---|
| **GameAnalytics** | blog / docs | retention, funnel, event-based cohort, analytics 질문 설계 | 벤더·F2P/mobile 사례 비중이 큼. `40/20/10` 같은 benchmark를 법칙으로 사용 금지 |
| **SteamDB** | blog / stats / release data | Steam 공개 데이터 관찰, release volume, pricing-change 탐색 | Valve 공식 서비스가 아님. 플랫폼 규칙·원인·wishlist를 추정하는 정본으로 사용 금지 |

## 4. 새 사이트 추가 Gate

조사 중 새 Source가 발견되면 추가할 수 있다. 단, 다음을 모두 만족해야 한다.

```yaml
repeat_value_confirmed: true
recent_relevant_material_found: true
source_role_declared: true
evidence_tier_is_not_inferred_from_popularity: true
current_pool_overlap_checked: true
commercial_or_vendor_interest_recorded: true
original_source_access_or_backtrace_value: true
```

다음이면 영구 Watchlist 추가를 보류한다.

- 단일 바이럴 글만 유용함
- 다른 Source의 재게시만 함
- SEO·affiliate·sponsor 목적과 독립 정보가 구분되지 않음
- 원출처가 더 직접적이고 Watchlist에서 이미 발견 가능함
- 현재 프로젝트와 관련 없는 대량 뉴스만 생산함

## 5. `ORIGINAL_SOURCE_BACKTRACE`

Hada·뉴스·뉴스레터·벤더 글에서 유용한 주장을 발견하면 다음 순서로 검증한다.

```text
발견 글/요약
→ 링크된 원문·공식 문서·원 발표·원 데이터
→ 게시/업데이트 날짜·버전·지역·플랫폼·표본 확인
→ Base REFERENCE_SOURCE_CATALOG와 현행 정본 대조
→ 같은 Goal의 열린/최근 PR 대조
→ Evidence tier·상태 확정
```

원출처가 없거나 접근할 수 없으면 `PARTIALLY_VERIFIED / CONTEXT_LIMITED / UNVERIFIED` 중 맞는 상태를 사용하고, 정책·Hard Rule로 승격하지 않는다.

## 6. Candidate capture

```yaml
candidate_id:
discovered_from:
original_url:
title:
published_or_updated_at:
checked_at:
source_role:
provisional_evidence_tier:
evidence_status:
topics: []
base_owner_candidate:
base_overlap: NONE | PARTIAL | ALREADY_COVERED | CONFLICT
same_goal_open_or_recent_pr:
why_it_might_change_a_decision:
original_source_backtrace:
sample_or_scope:
commercial_or_vendor_interest:
license_or_copying_notes:
```

원문 전체를 Base에 복제하지 않는다. 제목·URL·날짜·핵심 사실의 짧은 요약·적용 조건·판정만 기록한다.

## 7. 주기 Scan 실행 계약

```text
LAST_SUCCESSFUL_SCAN
→ SOURCE_INDEX_REFRESH
→ NEW_OR_CHANGED_CANDIDATES
→ DUPLICATE_AND_CURRENT_BASE_CHECK
→ ORIGINAL_SOURCE_BACKTRACE
→ SOURCE_ROLE_AND_EVIDENCE_TIER
→ FRESHNESS_AND_SCOPE_CHECK
→ DECISION_RELEVANCE_FILTER
→ EVIDENCE_PACK
→ ADVERSARIAL_ATTACK
→ CRITIQUE_VALIDATION
→ ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
→ NO_CHANGE | EVIDENCE_ONLY_UPDATE | LOW_RISK_BOUNDED_UPDATE | BCP_OR_USER_DECISION
→ REGRESSION_RECHECK
→ SCAN_CHECKPOINT
```

### 기본 cadence

- `weekly`: Hada, Godot release/blog, Steamworks, Android/Google Play release/policy, GameDiscoverCo, How To Market A Game, Game Developer, SteamDB blog처럼 빠르게 변하는 면.
- `monthly-or-on-demand`: GDC Vault, Games User Research, 80 Level, GameAnalytics, Deconstructor of Fun, GPUOpen.
- `quarterly-or-when-relevant`: The Level Design Book, Game Accessibility Guidelines처럼 상대적으로 정적인 Reference.

이는 권장 기본값이며 Base 불변 일정이 아니다.

## 8. 최근 6개월 Bootstrap 계약

초기 기준 범위:

```text
2026-02-10T00:00:00+09:00
→ 2026-08-10T23:59:59+09:00
```

Source의 공개 archive/index가 기간 전체 항목을 신뢰성 있게 노출하는 경우 `FULL_INDEX_REVIEW`를 사용할 수 있다. 검색 색인·paywall·무한 스크롤·대량 뉴스 때문에 기간 전체를 증명할 수 없으면 `PARTIAL_INDEX_REVIEW`로 둔다.

`PARTIAL_INDEX_REVIEW`를 `6개월치 전부 읽음`으로 표현하지 않는다. 대신 **현재 게임 작업과 연결되는 관련 항목을 기간 내 가능한 범위에서 전수 또는 고밀도로 검토**하고 미검증 범위를 남긴다.

이 bootstrap의 실제 결과는 `RECENT_EXTERNAL_EVIDENCE_REVIEW_2026-08-10.md`가 소유한다.

## 9. 시장·벤치마크 숫자 Guardrail

GameDiscoverCo·How To Market A Game·GameAnalytics·SteamDB 같은 자료에서 숫자를 사용할 때는 최소 다음을 같이 보존한다.

```yaml
observation_window:
platform_and_event:
sample_size_or_unknown:
collection_method:
percentile_or_distribution:
segment_or_bucket:
source_estimate_or_platform_fact:
known_bias:
```

- 평균/중앙값/백분위를 universal 목표로 바꾸지 않는다.
- 상관관계를 인과로 보고하지 않는다.
- Steam visibility 원인은 Steamworks 공식 설명을 우선한다.
- 특정 festival 한 회차의 변화는 다음 회차에도 유지된다고 가정하지 않는다.

## 10. 적대적 검토 Lens

- 높은 추천 수·조회 수를 사실성 점수로 사용했는가?
- 큐레이션 요약이 원문의 조건·반례·날짜를 잃었는가?
- AAA/F2P/mobile/UGC 사례를 현재 프로젝트에 과잉 일반화했는가?
- SteamDB 관찰값을 Valve 공식 사실로 썼는가?
- vendor benchmark를 제품 목표로 고정했는가?
- AI가 만든 통계·출처·요약을 원자료로 오인했는가?
- 최신 6개월에 집중한 나머지 오래됐지만 유효한 표준·연구를 버렸는가?
- 같은 원칙이 Base에 이미 있는데 새 Skill·Guide·Template를 만들었는가?
- 열린 PR이 같은 책임을 이미 수정 중인데 병렬로 중복 변경했는가?

## 11. 변경 권한

### `LOW_RISK_BOUNDED_UPDATE`

현재 승인 범위 또는 현행 저위험 자동승인 계약 안에서 다음을 모두 만족할 때만 최소 반영한다.

- 작은 가역 변경
- 기존 owner의 Reference/Evidence 보강
- Skill ID·owner·Schema·보안·권한·라이선스 의미 불변
- 원출처와 현행 Base 비교 완료
- 관련 테스트·적대적 재검토 실행 가능

### `BCP_OR_USER_DECISION`

다음은 자동 확정하지 않는다.

- 제품/게임 핵심 방향
- Base 공용 정책의 의미 변경
- ACTIVE Skill 추가·제거·ID·owner 변경
- GitHub Workflow write 권한·인증·보안 경계 변경
- 라이선스·법적 판단
- 대규모 구조 변경·migration
- 미검증 트렌드를 Hard Rule로 승격

## 12. 완료 보고

각 scan은 최소 다음을 보고한다.

```yaml
scan_window:
sources_checked:
full_index_review: []
partial_index_review: []
new_sources_added: []
material_candidates:
no_change_count:
evidence_only_updates:
low_risk_updates:
bcp_or_user_decisions:
rejected_overgeneralizations:
open_pr_conflicts_or_deferrals:
validation_run:
unverified_scope:
next_scan_from:
```
