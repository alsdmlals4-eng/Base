# 최근 6개월 Base 외부 Evidence Review — 2026-08-10

```yaml
review_role: initial-periodic-base-source-watchlist-bootstrap-evidence
review_window_start: 2026-02-10T00:00:00+09:00
review_window_end: 2026-08-10T23:59:59+09:00
checked_at: 2026-08-10
owner_watchlist: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
claim_ceiling: SOURCE_INDEX_AND_RELEVANT_ARTICLE_REVIEW_NOT_UNIVERSAL_FULLTEXT_CORPUS
source_domains:
  - GAME_DEVELOPMENT
  - PROMPT_AND_AGENT_WORKFLOW
  - SKILL_AUTHORING_AND_EVOLUTION
  - FICTION_AND_INTERACTIVE_NARRATIVE
  - YOUTUBE_AND_VIDEO_EDITING
```

## 1. 목적과 해석 제한

이 문서는 2026-02-10부터 2026-08-10까지 최근 6개월의 공개 자료를 이용해 Base와 향후 프로젝트 작업에 새로 필요한 공용 개선 요소가 있는지 검토한 초기 bootstrap 기록이다.

`FULL_INDEX_REVIEW`는 해당 Source의 **명시한 index/archive/changelog surface가 검토 기간 전체를 노출하고 그 index를 확인했다**는 뜻이다. 사이트의 모든 본문·영상·댓글·유료 자료를 전부 읽었다는 뜻이 아니다.

검색 색인·paywall·대량 게시물·무한 스크롤·영상·강의 본문 접근 제한 때문에 기간 전체 corpus를 증명할 수 없는 곳은 `PARTIAL_INDEX_REVIEW`로 기록한다. `PARTIAL_INDEX_REVIEW`를 “6개월치 전부 읽음”으로 표현하지 않는다.

정적이거나 6개월 밖의 자료라도 현재 설계의 장기 근거로 가치가 있으면 `STATIC_REFERENCE_REVIEW`로 분리한다. 최근성은 Evidence 강도를 자동으로 높이지 않는다.

## 2. Source Coverage — `GAME_DEVELOPMENT`

| Source | review coverage | 검토한 surface / 대표 원출처 | Base overlap | disposition |
|---|---|---|---|---|
| Godot Engine official | `FULL_INDEX_REVIEW` — release category index / period releases | 4.6 maintenance, 4.7 release/migration 관련 surface | safe migration·version pin·canary·regression 원칙이 이미 존재 | `NO_CHANGE` + Watchlist freshness |
| Valve Steamworks | `PARTIAL_INDEX_REVIEW` — 현재 관련 문서 중심 | Visibility, Demos, Wishlists, Update Visibility Rounds, SteamPipe | 공식 플랫폼 사실 우선은 이미 존재하나 주기 freshness 연결이 약함 | `LOW_RISK_BOUNDED_UPDATE` |
| Android Developers Games | `FULL_INDEX_REVIEW` — Games release-notes surface + 관련 performance docs | games release notes, performance, ADPF/Game Mode | PC·Android Delivery/성능 Evidence와 중복 | `EVIDENCE_ONLY_UPDATE` |
| Google Play developer policy / quality | `FULL_INDEX_REVIEW` — current policy deadlines/effective-date surface | policy deadlines, metadata/quality, migration/deprecation | 출시·compliance Guide에 이미 재검증 Gate 존재 | `EVIDENCE_ONLY_UPDATE` |
| Xbox Accessibility Guidelines | `PARTIAL_INDEX_REVIEW` — current guideline index + 관련 항목 | text, contrast, input, motion, audio, objectives, UI context | 접근성 owner가 이미 존재하고 별도 UI/UX PR이 상세 rule hardening 중 | `NO_CHANGE` / `DEFER_OPEN_PR_247` |
| GDC Vault | `FULL_INDEX_REVIEW` for GDC 2026 public session index; talk body `PARTIAL_INDEX_REVIEW` | postmortem, design, production, performance, AI, accessibility, narrative | T2 현업 사례 사용 원칙 이미 존재 | `EVIDENCE_ONLY_UPDATE` |
| Game Developer | `PARTIAL_INDEX_REVIEW` — design/production/marketing recent indexes | 2026 design·production·marketing articles and interviews | 현업 Evidence source로 적합 | `EVIDENCE_ONLY_UPDATE` |
| Games User Research | `PARTIAL_INDEX_REVIEW` — articles index + 최근 핵심 글 | 2026 playtest maturity / playtesting definition 자료 | research question·행동/자기보고 분리는 존재, playtest 용어 구분은 보강 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| GameDiscoverCo | `PARTIAL_INDEX_REVIEW` — public newsletter archive/recent posts | Steam/Next Fest/discovery market observations | 공식 Steam 규칙과 제3자 관찰 분리 필요 | `LOW_RISK_BOUNDED_UPDATE` |
| GameAnalytics | `PARTIAL_INDEX_REVIEW` — blog/docs recent relevant posts | retention/context/event-based cohort guidance | telemetry Evidence 원칙은 존재; universal benchmark 오용 방지 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| The Level Design Book | `STATIC_REFERENCE_REVIEW` | blockout, playtesting, process pages | 빠른 blockout·검증·iteration은 기존 데모/Vertical Slice와 중복 | `NO_CHANGE` |
| Game Accessibility Guidelines | `STATIC_REFERENCE_REVIEW` | full/basic/intermediate/advanced list, feedback guidance | 접근성 Evidence 후보로 유용하지만 공식 compliance가 아님 | `NO_CHANGE` / `DEFER_OPEN_PR_247` |
| 80 Level | `PARTIAL_INDEX_REVIEW` — technical-art/environment/gamedev recent indexes | 2026 technical artist and environment-production interviews | art/asset pipeline owner 이미 존재 | `EVIDENCE_ONLY_UPDATE` |
| SteamDB | `PARTIAL_INDEX_REVIEW` — blog/stats relevant recent changes | pricing/release/public Steam observations | 제3자 관찰이며 Valve 공식 정본이 아님 | `LOW_RISK_BOUNDED_UPDATE` guardrail only |
| Hada GeekNews | `PARTIAL_INDEX_REVIEW` — 2026 recent AI/dev workflow relevant feed/search | AI coding agents, skills/evals, harness, loop engineering, security summaries | Base의 Agent/Skill/continuous/adversarial 구조와 상당 부분 중복 | `NO_CHANGE` + discovery feed |
| How To Market A Game | `PARTIAL_INDEX_REVIEW` — 2026 public posts/benchmark pages | Next Fest, demo→wishlist, launch observations | indie Steam 실행 사례 보완 | `EVIDENCE_ONLY_UPDATE` + **new source** |
| Deconstructor of Fun | `PARTIAL_INDEX_REVIEW` — 2026 blog/category posts | mobile/F2P/business/AI operator perspectives | premium PC·Godot 프로젝트에는 맥락 변환 필요 | `REFERENCE_ONLY` + **new source** |
| AMD GPUOpen | `PARTIAL_INDEX_REVIEW` — 2026 tools/articles | GPU profiling/performance/crash-debug/tooling | 기술 성능 Reference 보완; AMD-specific | `EVIDENCE_ONLY_UPDATE` + **new source** |

## 3. Source Coverage — `PROMPT_AND_AGENT_WORKFLOW`

| Source | review coverage | 최근/현재 확인 내용 | Base overlap | disposition |
|---|---|---|---|---|
| OpenAI official docs / engineering / Academy | `PARTIAL_INDEX_REVIEW` | clear instructions, eval-driven refinement, agent workflow, safety boundary, long-running work/harness 사례 | Base의 work contract·validation·exact evidence와 강하게 중복 | `LOW_RISK_BOUNDED_UPDATE` — prompt placement/eval wording 보강 |
| Anthropic Engineering / Docs | `FULL_INDEX_REVIEW` for recent engineering index; article bodies `PARTIAL_INDEX_REVIEW` | long-running harness, context engineering, evals, tool design, agent safety | handoff·context·adversarial review와 중복 | `LOW_RISK_BOUNDED_UPDATE` — harness/configuration eval 명문화 |
| GitHub Copilot Docs | `PARTIAL_INDEX_REVIEW` — current customization docs | repository/path instructions, prompt files, custom agents, Agent Skills, hooks/MCP | Base의 global rule·Skill routing 경계와 직접 비교 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| Google Developers Blog / Google Cloud AI & ADK | `PARTIAL_INDEX_REVIEW` — 2026 relevant posts/docs | modular prompt architecture, context engineering, Agent Skills progressive disclosure, ADK | Base progressive-disclosure 방향과 일치 | `LOW_RISK_BOUNDED_UPDATE` |
| Microsoft Learn | `PARTIAL_INDEX_REVIEW` — current/recent Agent Skills docs | Skill task/steps/output/constraints/edge cases/tool refs, preview/test guidance | Base Skill contract와 높은 중복 | `EVIDENCE_ONLY_UPDATE` |
| Hada GeekNews | `PARTIAL_INDEX_REVIEW` | prompt/agent/harness/eval/security 원문 발견 | discovery feed only | `NO_CHANGE` + original-source backtrace |

## 4. Source Coverage — `SKILL_AUTHORING_AND_EVOLUTION`

| Source | review coverage | 핵심 패턴 | Base overlap | disposition |
|---|---|---|---|---|
| GitHub Copilot Agent Skills / customization | `PARTIAL_INDEX_REVIEW` | always-on instruction, reusable prompt, custom agent, task Skill의 역할 분리 | consolidation-first를 더 명확하게 설명하는 데 유용 | `LOW_RISK_BOUNDED_UPDATE` |
| Anthropic Agent Skills / Engineering | `PARTIAL_INDEX_REVIEW` | SKILL.md + references/scripts, progressive disclosure, iteration, security | Base package 구조와 유사 | `EVIDENCE_ONLY_UPDATE` |
| Google ADK Agent Skills | `PARTIAL_INDEX_REVIEW` | on-demand loading, progressive disclosure, inline/file/generated skill | runtime generation을 ACTIVE Skill 자동승격으로 오해할 위험 | `LOW_RISK_BOUNDED_UPDATE` guardrail |
| Microsoft Learn Agent Skills | `PARTIAL_INDEX_REVIEW` | clear task, steps, output format, constraints, edge cases, tools, preview/test | Base Skill contract와 중복 | `EVIDENCE_ONLY_UPDATE` |
| OpenAI workflow/eval guidance | `PARTIAL_INDEX_REVIEW` | smallest useful workflow, eval-driven refinement, human review | Base behavior-eval과 연결 | `LOW_RISK_BOUNDED_UPDATE` |

## 5. Source Coverage — `FICTION_AND_INTERACTIVE_NARRATIVE`

| Source | review coverage | 최근/현재 확인 내용 | Base overlap | disposition |
|---|---|---|---|---|
| Reedsy | `PARTIAL_INDEX_REVIEW` — 2026 recent craft/editing pages | developmental editing, structure/character, layered editing, line/copy/proof 구분 | 기존 Narrative Method에 단계형 퇴고가 부족 | `LOW_RISK_BOUNDED_UPDATE` |
| inkle / ink | `STATIC_REFERENCE_REVIEW` | branching text, choice/state, write→play/test→export workflow | 게임 narrative의 state/branch 경계에 유용 | `EVIDENCE_ONLY_UPDATE` |
| Yarn Spinner | `PARTIAL_INDEX_REVIEW` — current docs + 2026 updates | interactive dialogue, variables/choices, localization, Godot integration, test loop | 게임 대사 runtime 경계를 보완 | `EVIDENCE_ONLY_UPDATE` |
| IGDA Game Writing | `PARTIAL_INDEX_REVIEW` — current resources/events incl. 2026 | game writing, narrative design, dialogue, collaboration/직무 | 게임 story 현업 관점 보완 | `EVIDENCE_ONLY_UPDATE` |
| Emily Short’s Interactive Storytelling | `STATIC_REFERENCE_REVIEW` | interactive fiction, dialogue, storylets, player knowledge/agency | 장기 사례·반례 source | `REFERENCE_ONLY` |
| GDC Vault — narrative/game writing | `FULL_INDEX_REVIEW` for 2026 public session index; bodies `PARTIAL_INDEX_REVIEW` | shipped-game narrative postmortem/pipeline/collaboration | T2 적용 조건 필요 | `EVIDENCE_ONLY_UPDATE` |

## 6. Source Coverage — `YOUTUBE_AND_VIDEO_EDITING`

| Source | review coverage | 최근/현재 확인 내용 | Base overlap | disposition |
|---|---|---|---|---|
| YouTube Analytics / Studio Help / Creators | `PARTIAL_INDEX_REVIEW` — current analytics/help surfaces | Reach, impressions/CTR, watch time, audience retention, new/casual/regular audience, analytics UI/definition changes | 기존 YouTube Skill의 sample guardrail과 연결 | `LOW_RISK_BOUNDED_UPDATE` |
| Blackmagic Design DaVinci Resolve Training | `STATIC_REFERENCE_REVIEW` + current official training | edit, trim, audio/Fairlight, color, Fusion/VFX, delivery | 편집 tool 기능을 공용 미학 규칙과 분리할 필요 | `EVIDENCE_ONLY_UPDATE` |
| Frame.io Insider / Knowledge Center | `PARTIAL_INDEX_REVIEW` — 2026 review/workflow content | versioned review, comparison, approvals, collaboration, metadata | review round를 Episode workflow에 넣을 가치 | `LOW_RISK_BOUNDED_UPDATE` |
| vidIQ | `PARTIAL_INDEX_REVIEW` — recent research/blog | retention, title/thumbnail/channel benchmark observations | vendor/sample bias가 큼 | `REFERENCE_ONLY` / `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE` |
| GDC / Game Developer video-marketing cases | `PARTIAL_INDEX_REVIEW` | game trailer/devlog/marketing 사례 | 게임 marketing과 실제 build evidence 연결 | `EVIDENCE_ONLY_UPDATE` |

## 7. 최근 기간에서 반복 확인된 개선 Cluster

### 7.1 엔진 업데이트는 `latest = 즉시 채택`이 아니다

Godot의 유지보수·신버전 흐름은 기능 추가와 regression/migration을 함께 가져온다. Base의 exact version, canary, rollback, project-specific regression evidence가 이미 이를 다룬다.

**판정:** `NO_CHANGE`.

### 7.2 플랫폼 공식 사실과 시장/커뮤니티 관찰을 분리한다

Steamworks와 YouTube Help처럼 플랫폼이 직접 설명하는 기능·지표·정의는 T1 후보이고, GameDiscoverCo·SteamDB·vidIQ·How To Market A Game의 시장/creator 관찰은 가설·benchmark다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Source role + sample/window/method/percentile guardrail.

### 7.3 `playtest`라는 이름만으로 Evidence 강도를 판단하지 않는다

최근 Games User Research 자료는 QA, 동료 피드백, 구조화된 usability/research study, 행동 관찰을 같은 “playtest” 말로 뭉개는 위험을 반복해서 보여 준다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Evidence Method에 purpose/participant/build/task/behavior/self-report를 분리 기록.

### 7.4 모바일 성능은 단일 FPS 스크린샷이 아니다

Android 공식 자료는 CPU/GPU bound, device variability, loading, thermal/quality tradeoff, 같은 도구의 before/after 비교를 요구한다.

**Base overlap:** 이미 Delivery/성능 owner에 상당 부분 존재.

**판정:** `NO_CHANGE` / `EVIDENCE_ONLY_UPDATE`.

### 7.5 플랫폼 정책·SDK·Analytics 정의는 주기 재검증이 필요하다

Google Play policy/deprecation, YouTube Studio/Analytics UI·지표 설명, GitHub/Microsoft/Google Agent customization surface는 바뀔 수 있다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Watchlist의 주기 freshness 책임.

### 7.6 AI 작업구조는 “프롬프트를 더 길게”보다 책임 배치가 중요하다

최근 OpenAI·Anthropic·GitHub·Google·Microsoft 자료를 교차 비교하면 항상 필요한 짧은 규칙, 특정 작업의 prompt/template, on-demand Skill, 독립 tool/context를 가진 agent를 구분하는 방향이 반복된다. 모듈화의 이유는 파일 수가 아니라 **독립 변경·테스트·라우팅 가능한 책임**이어야 한다.

**Base overlap:** `AI_SKILL_ADOPTION_GUIDE`와 `evolving-project-discipline-skills`가 이미 consolidation-first를 소유.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — Prompt/Instruction/Skill/Agent/Tool 배치 Gate 추가. 새 ACTIVE Skill은 추가하지 않음.

### 7.7 Progressive disclosure는 Skill 수 증가가 아니라 context control 수단이다

Agent Skills 관련 여러 공식 자료는 task-specific instructions/references/scripts를 필요할 때 로드하는 progressive disclosure를 강조한다.

**위험:** Skill을 많이 만들수록 능력이 올라간다고 오해하거나, global instruction과 Skill에 같은 책임을 복제할 수 있다.

**판정:** `EVIDENCE_ONLY_UPDATE` + `REJECTED_OVERGENERALIZATION` for “more skills = better”.

### 7.8 Agent Eval은 모델 이름만 고정해서는 부족하다

최근 agent engineering/eval 자료는 실제 성능이 prompt, context, tools, permissions, harness, budget, retry/stop logic에 영향을 받는다는 점을 강조한다. 제품/harness 변경이 모델 품질 변화처럼 보일 수 있다.

**Base overlap:** behavior-eval identity와 독립 reviewer가 이미 존재.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — eval 비교 시 harness/tool/permission/budget/configuration을 가능한 범위에서 기록하도록 명문화.

### 7.9 인간은 목표·도메인 판단, Agent는 실행을 주로 맡는 경계가 안전하다

최근 agent workflow 자료는 사람의 계획·검수·도메인 판단과 AI 실행을 분리하는 실무 패턴을 보여 준다.

**Base overlap:** 사용자 결정 Gate, approval bundle, external-source review와 일치.

**판정:** `NO_CHANGE` + wording reinforcement.

### 7.10 소설 craft는 게임 스토리에 도움이 되지만 그대로 복제하지 않는다

Reedsy의 구조·인물·developmental editing과 ink/Yarn/GDC/IGDA의 interactive narrative 사례를 함께 보면 캐릭터 욕망, scene change, setup/payoff, 정보 공개, continuity, voice, staged revision은 공용으로 재사용 가능하다. 그러나 게임은 player agency, state, branch budget, replay, localization/runtime data가 추가된다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — `NARRATIVE_AND_RELATIONSHIP_METHOD`에 소설↔게임 전이 경계 추가.

### 7.11 문장 polish보다 구조·연속성 검수가 먼저다

최근 Reedsy editing 자료와 장기 연재 실무를 대조하면 developmental/structure 문제를 line/copy/proof 단계에서 해결하려 하면 비용이 커지고 회귀를 숨길 수 있다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — `CANON_AND_CONTINUITY → DEVELOPMENTAL_STRUCTURE → SCENE_AND_CHARACTER → DIALOGUE_AND_INFORMATION → LINE_AND_PROSE → COPY_AND_PROOF → CROSS_RANGE_RECONCILIATION` 순서 보강.

### 7.12 Interactive narrative는 선택 문구보다 state·validation·localization까지 설계한다

ink/Yarn Spinner의 실제 authoring/runtime 구조는 분기 대사만 쓰는 것이 아니라 variables/state, test loop, integration/localization까지 다룬다.

**Base overlap:** 기존 game narrative의 선택·상태·저장 경계와 일치.

**판정:** `EVIDENCE_ONLY_UPDATE`.

### 7.13 YouTube Retention graph는 관찰이지 자동 원인 판정이 아니다

YouTube 공식 Analytics는 key moments, watch time/AVD, audience segments 등으로 시청 행동을 보여 주지만 drop/spike 자체가 장면의 인과 원인을 증명하지 않는다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — drop/rewatch를 다음 영상 가설로 변환하고 vendor benchmark를 context-limited로 유지.

### 7.14 영상 편집은 story/evidence rough cut이 VFX보다 먼저다

DaVinci 공식 training과 Frame.io의 review workflow를 함께 보면 edit/trim/story clarity, dialogue/audio, versioned review가 polish보다 먼저 오는 구조가 재사용 가치가 높다.

**판정:** `LOW_RISK_BOUNDED_UPDATE` — YouTube Skill에 rough cut→clarity/pacing→audio→graphics/captions→color/VFX→export QC와 versioned review 추가.

### 7.15 Hada는 유용한 발견면이지만 정본은 아니다

최근 AI coding/agent 글은 rules/skills/context/evals/harness/security를 빠르게 발견하게 해 주지만, Hada 자체는 `DISCOVERY_FEED`다.

**판정:** `NO_CHANGE` + `ORIGINAL_SOURCE_BACKTRACE`.

## 8. 새로 추가·확장한 Source

### Game / market

- **How To Market A Game** — `PROFESSIONAL_PRACTICE`, indie Steam 실행·festival·demo 사례. self-selected sample과 상업 이해관계 기록.
- **Deconstructor of Fun** — `PROFESSIONAL_PRACTICE | CONTEXT_LIMITED`, mobile/F2P/liveops counterevidence.
- **AMD GPUOpen** — `AUTHORITY_TARGET` for AMD tool/hardware facts only.

### Prompt / Agent / Skill

- **OpenAI official docs / Engineering / Academy** — OpenAI 기능·workflow 사실에는 T1 후보; 일반 원리는 교차검증.
- **Anthropic Engineering / Docs** — Claude 기능·engineering facts에는 T1 후보; harness/context/eval 일반 원리는 교차검증.
- **GitHub Copilot Docs** — repository/path instructions, prompt files, custom agents, Agent Skills의 현재 지원 surface.
- **Google Developers Blog / Google Cloud AI & ADK** — modular prompt/context/Agent Skills/ADK.
- **Microsoft Learn** — Agent Skills/customization/preview/test guidance.

### Fiction / interactive narrative

- **Reedsy** — `PROFESSIONAL_PRACTICE`, structure/character/editing. marketplace/education 이해관계 기록.
- **inkle / ink** — `PROFESSIONAL_PRACTICE`, branching/state/write-test loop; tool grammar는 tool-specific.
- **Yarn Spinner** — `PROFESSIONAL_PRACTICE`, dialogue/state/localization/Godot integration.
- **IGDA Game Writing** — `PROFESSIONAL_PRACTICE`, game writing/narrative design 현업 자료.
- **Emily Short** — `PROFESSIONAL_PRACTICE | REFERENCE_ONLY`, interactive fiction 장기 사례.

### YouTube / editing

- **YouTube Analytics / Studio Help / Creators** — `AUTHORITY_TARGET` for YouTube metric/feature definitions.
- **Blackmagic Design DaVinci Resolve Training** — `AUTHORITY_TARGET` for Resolve tool capability/workflow facts.
- **Frame.io Insider / Knowledge Center** — `PROFESSIONAL_PRACTICE`, versioned review/collaboration.
- **vidIQ** — `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE`, creator benchmark/research; vendor/sample bias 기록.

## 9. `REJECTED_OVERGENERALIZATION`

- `REJECTED_OVERGENERALIZATION`: 특정 GameAnalytics retention 수치를 모든 게임의 목표 KPI로 고정.
- `REJECTED_OVERGENERALIZATION`: 특정 Steam Next Fest 회차의 평균·상위 percentile을 모든 프로젝트 성공 기준으로 고정.
- `REJECTED_OVERGENERALIZATION`: SteamDB·GameDiscoverCo 추정을 Steam visibility 공식 법칙처럼 서술.
- `REJECTED_OVERGENERALIZATION`: Hada 요약을 원출처 확인 없이 T1/T2 사실로 승격.
- `REJECTED_OVERGENERALIZATION`: 특정 모델의 prompt wording을 모든 모델의 영구 prompt 공식으로 고정.
- `REJECTED_OVERGENERALIZATION`: 프롬프트 파일·Skill·Agent 개수 증가를 architecture 개선 또는 능력 향상의 증거로 사용.
- `REJECTED_OVERGENERALIZATION`: runtime이 만든/generated Skill을 Base ACTIVE Skill로 자동 승격.
- `REJECTED_OVERGENERALIZATION`: GDC·80 Level·대형 agent 조직의 workflow를 소규모 프로젝트 필수 절차로 강제.
- `REJECTED_OVERGENERALIZATION`: 소설 3막/beat 구조 같은 단일 framework를 모든 소설·게임 스토리의 정답 구조로 강제.
- `REJECTED_OVERGENERALIZATION`: 게임의 선택/branch/state를 선형 소설 모든 장면에 강제.
- `REJECTED_OVERGENERALIZATION`: 좋은 소설 scene을 player agency 검증 없이 좋은 game scene으로 간주.
- `REJECTED_OVERGENERALIZATION`: YouTube CTR·retention·views를 게임 품질·판매·구매 의도의 직접 인과로 해석.
- `REJECTED_OVERGENERALIZATION`: vidIQ 같은 vendor benchmark를 채널 universal target으로 고정.
- `REJECTED_OVERGENERALIZATION`: 편집 transition/VFX/motion이 많을수록 영상 품질이 높다고 간주.
- `REJECTED_OVERGENERALIZATION`: 최근 6개월에 많이 언급됐다는 이유로 오래된 표준·원 연구·craft를 폐기.

## 10. Base 변경 판정 Summary

| Finding | Base overlap | Decision |
|---|---|---|
| 주기 Source freshness / delta scan | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — Watchlist |
| 조사 중 새 Source 추가 Gate | NONE | `LOW_RISK_BOUNDED_UPDATE` |
| 발견 글 → 원출처 역추적 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| 시장/vendor benchmark guardrail | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| playtest purpose/evidence type | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| Prompt/Instruction/Skill/Agent/Tool 배치 Gate | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — `AI_SKILL_ADOPTION_GUIDE` |
| monolithic prompt modularization 조건 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| eval harness/tool/permission/budget 기록 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| 새 ACTIVE Skill | NO_INDEPENDENT_BOUNDARY | `REJECTED_OVERGENERALIZATION` |
| 소설↔게임 스토리 공통 craft/매체 경계 | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — Narrative Method |
| staged revision / continuity-first | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| interactive dialogue state/localization | ALREADY_COVERED_PARTIAL | `EVIDENCE_ONLY_UPDATE` |
| YouTube official Analytics definitions | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` — YouTube Skill |
| story/evidence-first edit + versioned review | PARTIAL | `LOW_RISK_BOUNDED_UPDATE` |
| vendor CTR/retention universal target | CONFLICT | `REJECTED_OVERGENERALIZATION` |
| UI/UX/accessibility 상세 rule | OPEN_PR_OVERLAP | `NO_CHANGE` / `DEFER_OPEN_PR_247` |

## 11. 실제 적용 범위

이번 구현에서 활성 Base에 반영한 최소 범위:

1. Base-wide `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md` 추가.
2. 게임 Evidence Hub·Method·Planning Policy에서 one-hop 연결.
3. `AI_SKILL_ADOPTION_GUIDE.md`에 prompt/instruction/Skill/agent/tool 배치와 eval guardrail 보강.
4. `NARRATIVE_AND_RELATIONSHIP_METHOD.md`에 소설↔게임 story 전이 경계와 단계형 퇴고·연속성 검수 보강.
5. `NARRATIVE_CONTENT_PLAN.md`의 존재하지 않는 구형 Method 경로를 현행 owner로 수정.
6. `producing-game-development-youtube-videos`에 story/evidence-first editing, versioned review, official Analytics 우선 해석 보강.
7. 전용 repository contract와 read-only CI 연결.

반영하지 않는 범위:

- 새 ACTIVE Skill·Skill ID·owner 변경.
- Proposal Registry 변경.
- GitHub Actions write 권한.
- 특정 retention/wishlist/CTR/조회수 절대 목표.
- 특정 AI 모델·편집기·서사 framework의 영구 공용 공식화.
- UI/UX/accessibility 상세 rule — 별도 open PR과 중복 방지.

## 12. 향후 Scan 기준

첫 성공 scan 이후에는 `last_successful_scan` 이후의 새 글·수정 글을 우선 확인한다. 다음 조건에서는 재검토 기간을 확장한다.

- Godot major/minor migration 또는 compatibility policy 변화.
- Steamworks visibility/demo/store 설명 변화.
- Android/Google Play SDK deprecation·policy deadline 변화.
- OpenAI/Anthropic/GitHub/Google/Microsoft의 instruction/agent/Skill/eval architecture 변화.
- Skill discovery/runtime generation/security model 변화.
- 소설/게임 writing owner에서 반복 실패나 새 workflow 근거가 누적됨.
- Yarn/ink 등 narrative tool의 localization/state/runtime integration 변화.
- YouTube metric 정의·Studio surface·A/B 기능 변화.
- 편집/협업 도구의 review/versioning/export workflow 변화.
- Source ownership/sponsor/paywall/data methodology 변화.

의미 있는 신규 Evidence가 없으면 `NO_CHANGE`를 정상 결과로 기록한다.
