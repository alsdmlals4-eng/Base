# 최근 6개월 게임 개발 외부 Evidence Review — 2026-08-10

```yaml
review_role: initial-periodic-source-watchlist-bootstrap-evidence
review_window_start: 2026-02-10T00:00:00+09:00
review_window_end: 2026-08-10T23:59:59+09:00
checked_at: 2026-08-10
owner_watchlist: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
claim_ceiling: SOURCE_INDEX_AND_RELEVANT_ARTICLE_REVIEW_NOT_UNIVERSAL_FULLTEXT_CORPUS
```

## 1. 목적과 해석 제한

이 문서는 2026-02-10부터 2026-08-10까지 최근 6개월의 공개 자료를 이용해 Base에 새로 필요한 공용 개선 요소가 있는지 검토한 초기 bootstrap 기록이다.

`FULL_INDEX_REVIEW`는 해당 Source의 **명시한 index/archive/changelog surface가 검토 기간 전체를 노출하고 그 index를 확인했다**는 뜻이다. 사이트의 모든 본문·영상·댓글을 전부 읽었다는 뜻이 아니다.

검색 색인·paywall·대량 게시물·무한 스크롤·영상 본문 접근 제한 때문에 기간 전체 corpus를 증명할 수 없는 곳은 `PARTIAL_INDEX_REVIEW`로 기록한다. `PARTIAL_INDEX_REVIEW`를 “6개월치 전부 읽음”으로 표현하지 않는다.

정적이지만 여전히 유용한 Reference는 `STATIC_REFERENCE_REVIEW`로 분리한다.

## 2. Source Coverage

| Source | review coverage | 검토한 surface / 대표 원출처 | Base overlap | disposition |
|---|---|---|---|---|
| Godot Engine official | `FULL_INDEX_REVIEW` — release category index / period releases | 4.6.1·4.6.2·4.6.3, 4.7 RC/stable, migration pages | safe migration·version pin·canary·regression 원칙이 이미 존재 | `NO_CHANGE` + Watchlist freshness |
| Valve Steamworks | `PARTIAL_INDEX_REVIEW` — 현재 관련 문서 중심 | Visibility, Demos, Wishlists, Update Visibility Rounds, SteamPipe | 공식 플랫폼 사실 우선은 이미 존재하나 주기 freshness 연결이 약함 | `LOW_RISK_BOUNDED_UPDATE` |
| Android Developers Games | `FULL_INDEX_REVIEW` — Games release-notes surface + 관련 performance docs | games release notes, optimize game performance, APT/ADPF/Game Mode | PC·Android Delivery/성능 Evidence와 중복 | `EVIDENCE_ONLY_UPDATE` |
| Google Play developer policy / quality | `FULL_INDEX_REVIEW` — current policy deadlines/effective-date surface | policy deadlines, metadata/quality guidance, Play Games Services migration/deprecation | 출시·compliance Guide에 이미 권한/재검증 Gate 존재 | `EVIDENCE_ONLY_UPDATE` |
| Xbox Accessibility Guidelines | `PARTIAL_INDEX_REVIEW` — current guideline index + 관련 항목 | text, contrast, input, motion, audio, objectives, UI context | 접근성 owner가 이미 존재하고 PR #247이 상세 rule hardening 중 | `NO_CHANGE` / `DEFER_OPEN_PR_247` |
| GDC Vault | `FULL_INDEX_REVIEW` for GDC 2026 public session index; talk body `PARTIAL_INDEX_REVIEW` | postmortem, design, production, performance, AI, accessibility sessions | T2 현업 사례 사용 원칙 이미 존재 | `EVIDENCE_ONLY_UPDATE` |
| Game Developer | `PARTIAL_INDEX_REVIEW` — design/production/marketing recent indexes | 2026 design·production·marketing articles and interviews | 현업 Evidence source로 적합, 개별 오래된 플랫폼 추정은 원출처 재검증 필요 | `EVIDENCE_ONLY_UPDATE` |
| Games User Research | `PARTIAL_INDEX_REVIEW` — articles index + 최근 핵심 글 | 2026-02 Playtest Maturity Model, 2026-03 What do we mean by playtesting? | research question·행동/자기보고 분리는 존재, playtest 용어 구분은 보강 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| GameDiscoverCo | `PARTIAL_INDEX_REVIEW` — public newsletter archive/recent posts | Steam/Next Fest/discovery market observations | 공식 Steam 규칙과 제3자 관찰 분리 필요 | `LOW_RISK_BOUNDED_UPDATE` |
| GameAnalytics | `PARTIAL_INDEX_REVIEW` — blog/docs recent relevant posts | retention/context/event-based cohort guidance | telemetry Evidence 원칙은 존재; universal benchmark 오용 방지 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| The Level Design Book | `STATIC_REFERENCE_REVIEW` | blockout, playtesting, process pages | 빠른 blockout·검증·iteration은 기존 PoC/Vertical Slice와 중복 | `NO_CHANGE` |
| Game Accessibility Guidelines | `STATIC_REFERENCE_REVIEW` | full/basic/intermediate/advanced list, feedback guidance | 접근성 Evidence 후보로 유용하지만 공식 compliance가 아님 | `NO_CHANGE` / `DEFER_OPEN_PR_247` |
| 80 Level | `PARTIAL_INDEX_REVIEW` — technical-art/environment/gamedev recent indexes | 2026 technical artist and environment-production interviews | art/asset pipeline owner 이미 존재 | `EVIDENCE_ONLY_UPDATE` |
| SteamDB | `PARTIAL_INDEX_REVIEW` — blog/stats relevant recent changes | pricing/release/public Steam observations | 제3자 관찰이며 Valve 공식 정본이 아님 | `LOW_RISK_BOUNDED_UPDATE` guardrail only |
| Hada GeekNews | `PARTIAL_INDEX_REVIEW` — 2026 recent AI/dev workflow relevant search and feed | AI coding agents, skills/evals, harness, loop engineering, security summaries | Base의 Agent/Skill/continuous/adversarial 구조와 상당 부분 중복 | `NO_CHANGE` + discovery feed |
| How To Market A Game | `PARTIAL_INDEX_REVIEW` — 2026 recent public posts/benchmark pages | Next Fest, demo→wishlist, momentum/launch observations | indie Steam 실측 관찰을 보완 | `EVIDENCE_ONLY_UPDATE` + **new source** |
| Deconstructor of Fun | `PARTIAL_INDEX_REVIEW` — 2026 recent blog/category posts | mobile/F2P/business/AI operator perspectives | premium PC·Godot 프로젝트에는 맥락 변환 필요 | `REFERENCE_ONLY` + **new source** |
| AMD GPUOpen | `PARTIAL_INDEX_REVIEW` — 2026 recent tools/articles | GPU profiling/performance/crash-debug/tooling | 기술 성능 Reference 보완; AMD-specific | `EVIDENCE_ONLY_UPDATE` + **new source** |

## 3. 최근 기간에서 반복 확인된 Topic Cluster

### 3.1 엔진 업데이트는 `latest = 즉시 채택`이 아니다

**관찰:** Godot 4.6 유지보수 릴리스와 4.7 pre-release/stable 흐름은 기능 추가와 함께 regression 수정·migration 정보를 지속 제공한다. 프로젝트 업그레이드는 release headline보다 exact version, migration guide, known issue, backup/VCS, project-specific regression evidence가 중요하다.

**Base overlap:** Existing Solution First, exact pin, canary, rollback, 실제 테스트를 이미 요구한다.

**판정:** `NO_CHANGE`.

**추가 이유:** 새 엔진 업그레이드 Skill을 만들지 않는다. Watchlist가 release/migration freshness를 제공하면 충분하다.

### 3.2 플랫폼 공식 사실과 시장/커뮤니티 관찰을 분리해야 한다

**관찰:** Steamworks의 Visibility/Demo/Wishlist 문서는 플랫폼이 직접 설명하는 작동 범위를 제공한다. 반면 GameDiscoverCo·How To Market A Game·SteamDB는 festival/시장/판매 공개 데이터를 분석해 유용한 경험적 가설을 제공한다.

**위험:** 제3자 관찰을 “Steam 알고리즘의 공식 법칙”으로 승격하거나, 특정 festival의 평균·백분위·상관관계를 모든 게임의 목표로 고정할 수 있다.

**Base overlap:** Evidence tier는 이미 존재하지만 반복 Source scan에 숫자 benchmark guardrail이 명시적이지 않았다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Watchlist에 공식-vs-observational 분리와 sample/window/method/percentile guardrail 추가.

### 3.3 플레이테스트라는 단어 자체가 증거 유형을 숨길 수 있다

**관찰:** Games User Research의 최근 자료는 조직에서 “playtesting”이 QA, 동료/친구 피드백, 구조화된 usability/research study 등 서로 다른 활동을 가리킬 수 있음을 강조한다.

**Base overlap:** Base는 이미 research question, 행동, 자기보고, sample bias, human validation claim ceiling을 구분한다.

**Gap:** Evidence Pack에서 `playtest`라는 이름만 보고 어떤 증거인지 오해할 가능성은 남는다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` 후보 — 외부 조사/플레이테스트 기록 시 `test_purpose / participant_source / observation_or_self_report / build_or_task_scope`를 명시하는 원칙을 Method에 짧게 보강한다. 새 Skill·새 Template은 만들지 않는다.

### 3.4 모바일 성능은 단일 FPS 스크린샷이 아니다

**관찰:** Android Developers Games는 scene별 profile, CPU/GPU bound 구분, 동일 도구를 사용한 before/after 비교, loading, device variability, thermal/quality tradeoff를 함께 다룬다.

**Base overlap:** `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`와 Delivery Profile에 device·thermal·performance evidence가 이미 존재한다.

**판정:** `EVIDENCE_ONLY_UPDATE`; 새 성능 체계 추가 불필요.

### 3.5 플랫폼 정책·SDK deprecation은 “한 번 조사하고 끝”낼 수 없다

**관찰:** Google Play policy effective date/deadline, Play Games Services migration/deprecation, Android games release notes처럼 플랫폼 요구는 기간 내 계속 바뀐다.

**Base overlap:** 플랫폼 Guide가 출시 전 재검증과 `RELEASE_BLOCKED_UNVERIFIED`를 이미 요구한다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Watchlist가 release/policy/deprecation surface를 주기 scan 대상으로 유지한다.

### 3.6 접근성은 디자인-구현-테스트를 연결하지만 이 PR의 상세 owner가 아니다

**관찰:** XAG와 Game Accessibility Guidelines는 input, motion, audio, objective clarity, UI context 등 여러 장벽을 설계 단계부터 검토하도록 돕는다.

**Base overlap:** 현재 Base main에 접근성 owner가 존재하며, 별도 open PR #247이 shared UI/UX/accessibility rule hardening을 구현 중이다.

**판정:** `NO_CHANGE` + `DEFER_OPEN_PR_247`.

**보호:** 이 Source Watchlist PR에서 상세 UI/UX/accessibility Hard Rule을 중복 구현하지 않는다.

### 3.7 AI 개발 워크플로는 “더 많은 agent”보다 context·eval·isolation·verification이 핵심이다

**관찰:** Hada에서 최근 반복적으로 소개된 AI coding/agent 자료는 rules/skills, context, tests/evals, worktree/isolation, human verification, security 같은 주제를 묶어 보여 준다.

**원출처 문제:** Hada는 `DISCOVERY_FEED`다. 각 주장은 실제 tool/vendor/author 원문으로 `ORIGINAL_SOURCE_BACKTRACE`해야 한다.

**Base overlap:** Base는 이미 Skill routing, worktree/PR, continuous-work, adversarial review, exact-head validation, context/handoff를 강하게 갖고 있다.

**판정:** `NO_CHANGE` — Hada 자체를 새 권위로 승격하지 않고 discovery feed로만 추가한다.

### 3.8 Technical Art/production 사례는 역할·병목을 배우되 조직을 복제하지 않는다

**관찰:** 80 Level과 GPUOpen의 최근 자료는 artist-engineering 경계, tooling friction, profiling/crash analysis처럼 제작 파이프라인과 도구 가시성 문제를 반복해서 보여 준다.

**Base overlap:** art/asset planning과 technical production owner가 이미 존재한다.

**판정:** `EVIDENCE_ONLY_UPDATE`.

**반례:** AAA studio pipeline 또는 AMD-specific tool을 Base universal pipeline으로 강제하지 않는다.

### 3.9 Retention/시장 benchmark는 맥락 없는 목표값이 아니다

**관찰:** GameAnalytics의 retention 자료도 benchmark는 baseline일 뿐 genre/business model/context를 함께 보라고 설명한다. Steam/Next Fest 자료 역시 시기·표본·선정 방식에 따라 분포가 크게 달라진다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — 숫자에는 observation window, sample, method, percentile/distribution, segment, source-estimate-vs-platform-fact를 함께 보존한다.

## 4. 추가한 새 Source

### 4.1 How To Market A Game

```yaml
source_role: PROFESSIONAL_PRACTICE
expected_evidence_tier: T2_PROFESSIONAL_PRACTICE | CONTEXT_LIMITED
use_for: indie Steam demo, Next Fest, wishlist, launch 사례와 공개 설문·benchmark
why_added: 기존 GameDiscoverCo와 달리 소규모 indie 실행·festival·demo 운영 사례를 반복적으로 다룸
risk: self-selected sample, survey bias, event-to-event drift, commercial course/community interest
```

### 4.2 Deconstructor of Fun

```yaml
source_role: PROFESSIONAL_PRACTICE
expected_evidence_tier: T2_PROFESSIONAL_PRACTICE | CONTEXT_LIMITED
use_for: mobile/F2P/liveops/business/AI operator 관점의 사례와 반례
why_added: Base의 premium/PC 중심 시야에서 빠질 수 있는 live-service·mobile business counterevidence 제공
risk: mobile/F2P/operator bias, consulting/sponsor/commercial context
```

### 4.3 AMD GPUOpen

```yaml
source_role: AUTHORITY_TARGET
expected_evidence_tier: T1_PRIMARY_OFFICIAL for AMD tools/hardware; otherwise CONTEXT_LIMITED
use_for: GPU profiling, graphics performance, crash analysis, AMD tool capability
why_added: engine/vendor-neutral 기사보다 AMD-specific performance/tool 사실을 직접 확인할 수 있음
risk: AMD hardware/tool scope; Godot/other GPU universal rule로 확대 금지
```

## 5. `REJECTED_OVERGENERALIZATION`

다음은 최근 자료가 유용하더라도 Base 공용 Hard Rule로 채택하지 않는다.

- `REJECTED_OVERGENERALIZATION`: GameAnalytics의 특정 retention 수치를 모든 게임의 목표 KPI로 고정.
- `REJECTED_OVERGENERALIZATION`: 특정 Steam Next Fest 회차의 wishlist/traffic 평균·상위 percentile을 모든 프로젝트 성공 기준으로 고정.
- `REJECTED_OVERGENERALIZATION`: SteamDB·GameDiscoverCo·커뮤니티 추정으로 Steam visibility algorithm을 공식 설명처럼 서술.
- `REJECTED_OVERGENERALIZATION`: Hada 요약을 원출처 확인 없이 T1/T2 사실로 승격.
- `REJECTED_OVERGENERALIZATION`: GDC·80 Level의 AAA/대형팀 pipeline을 1인·소규모 프로젝트 필수 단계로 강제.
- `REJECTED_OVERGENERALIZATION`: AMD GPUOpen의 GPU-specific 권장사항을 모든 GPU·모든 엔진의 단일 prescription으로 고정.
- `REJECTED_OVERGENERALIZATION`: XAG 또는 Game Accessibility Guidelines 체크만으로 실제 장애 당사자 usability나 법적 compliance가 검증됐다고 주장.
- `REJECTED_OVERGENERALIZATION`: 최근 6개월에 많이 언급됐다는 이유로 오래된 표준·원 연구·현재 Base 검증을 대체.

## 6. Base 변경 판정 Summary

| Finding | Base overlap | Decision |
|---|---|---|
| 주기 Source freshness / delta scan | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — Watchlist 추가 |
| 새 Source 발견·추가 Gate | NONE | `LOW_RISK_BOUNDED_UPDATE` — Watchlist 추가 |
| 발견 글 → 원출처 역추적 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — `ORIGINAL_SOURCE_BACKTRACE` 명문화 |
| Steam official vs market observation | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — benchmark guardrail |
| playtest purpose/evidence type 명시 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — Method 짧은 보강 |
| Android thermal/device performance | ALREADY_COVERED | `NO_CHANGE` / `EVIDENCE_ONLY_UPDATE` |
| Godot migration/canary/rollback | ALREADY_COVERED | `NO_CHANGE` |
| UI/UX/accessibility 상세 rule | OPEN_PR_OVERLAP | `NO_CHANGE` / `DEFER_OPEN_PR_247` |
| AI agent rules/skills/evals | ALREADY_COVERED | `NO_CHANGE` |
| technical-art pipeline | ALREADY_COVERED | `EVIDENCE_ONLY_UPDATE` |
| universal KPI/Next Fest targets | CONFLICT_WITH_NEUTRAL_EVIDENCE | `REJECTED_OVERGENERALIZATION` |
| 새 ACTIVE Skill | NO_INDEPENDENT_BOUNDARY | `REJECTED_OVERGENERALIZATION` |

## 7. 실제 적용 범위

이번 구현에서 활성 Base에 반영할 최소 범위:

1. `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` 추가.
2. Knowledge Hub·Evidence Method·Planning Evidence Policy에서 one-hop 연결.
3. Evidence Method에 playtest 증거 유형 명시와 periodic discovery delegate를 작은 보강으로 추가.
4. 전용 repository contract test와 read-only Evidence Knowledge CI 연결.
5. Changelog/Learning Log에 "recurring discovery ≠ new authority" 원칙 기록.

반영하지 않는 범위:

- ACTIVE Skill·Skill ID·owner 변경.
- Proposal Registry 변경.
- GitHub Actions write 권한.
- UI/UX/accessibility 상세 rule — open PR #247과 중복 방지.
- 특정 retention/wishlist/매출 절대 목표.
- 플랫폼 정책을 2026-08-10 snapshot으로 영구 Hard Rule화.

## 8. 향후 Scan 기준

첫 성공 scan 이후에는 `last_successful_scan` 이후의 새 글·수정 글을 우선 확인한다. 다만 다음 조건에서는 재검토 범위를 늘린다.

- Godot major/minor migration 또는 compatibility policy 변화.
- Steamworks visibility/demo/store 정책 설명 변화.
- Android/Google Play SDK deprecation·policy deadline 변화.
- 접근성 guideline major revision.
- 시장/analytics 자료의 표본 정의 또는 방법론 변화.
- Source 자체의 ownership/sponsor/paywall/data methodology 변화.

의미 있는 신규 Evidence가 없으면 `NO_CHANGE`를 정상 결과로 기록한다.
