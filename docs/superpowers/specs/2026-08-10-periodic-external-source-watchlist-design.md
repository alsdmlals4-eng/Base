# Periodic External Source Watchlist Design

## Goal

Base가 외부 변화와 현업 지식을 정기적으로 발견하되 트렌드를 정본으로 오인하지 않도록, **Base-wide Source Watchlist → 원출처 역추적 → Existing Solution First → 적대적 검토 → 기존 owner 흡수/BCP** 구조를 만든다.

초기 bootstrap은 2026-02-10 ~ 2026-08-10의 공개 자료를 가능한 범위에서 검토한다. 공개 index/archive가 기간 전체를 입증하지 못하면 `PARTIAL_INDEX_REVIEW`로 명시하며 “6개월치 전부 읽음”이라고 주장하지 않는다.

## Source domains

```text
GAME_DEVELOPMENT
PROMPT_AND_AGENT_WORKFLOW
SKILL_AUTHORING_AND_EVOLUTION
FICTION_AND_INTERACTIVE_NARRATIVE
YOUTUBE_AND_VIDEO_EDITING
```

각 domain은 Source를 직접 실행 권위로 만들지 않는다. 기존 Base owner가 실행과 적용을 소유한다.

## Existing Solution First

판정: `ABSORB` 중심.

- 새 ACTIVE Skill: `0`
- 새 Work Mode: `0`
- 새 독립 scheduler: `0`
- 새 BCP: `0` — 사용자가 이번 bounded Base 변경을 직접 승인함
- 보호: `skills/SKILL_REGISTRY.json`, `[수정제안서]/PROPOSAL_REGISTRY.json`, release lock/frozen artifacts

### Owner map

| Domain | 기존 owner / consumer |
|---|---|
| 게임 외부 Evidence | `docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md` |
| 공용 기획 Evidence | `docs/PLANNING_SEQUENCE_AND_EVIDENCE_POLICY.md` |
| Prompt/Instruction/Skill/Agent 배치 | `docs/AI_SKILL_ADOPTION_GUIDE.md` |
| Skill 생성·통합·behavior eval | `skills/evolving-project-discipline-skills` |
| 소설·게임 서사 공통 craft | `docs/knowledge/methods/NARRATIVE_AND_RELATIONSHIP_METHOD.md` |
| 게임 narrative 작업면 | `templates/planning/NARRATIVE_CONTENT_PLAN.md` |
| YouTube 기획·편집·분석 | `skills/producing-game-development-youtube-videos` + `templates/game-development-youtube/EPISODE_PACKET.md` |
| 실패 가정 공격 | `running-adversarial-review-and-refinement` |
| 공용 정책/Skill 의미 승격 | `managing-base-change-proposals` |

## Source roles

`source_role`은 수집 단계 역할이며 Evidence tier와 다르다.

- `AUTHORITY_TARGET`: 공식 제품·플랫폼·엔진·표준·원 연구. 자기 제품/표준 사실에만 높은 권위.
- `PROFESSIONAL_PRACTICE`: 현업 발표·전문가·작가·편집자·개발자 사례. 맥락 제한 보존.
- `DISCOVERY_FEED`: Hada 같은 원문 발견면. 직접 권위 아님.
- `OBSERVATIONAL_DATA_OR_VENDOR_GUIDE`: 시장·creator·analytics vendor 관찰. 표본·이해관계 보존.

## Core source families

### Game

Godot, Steamworks, Android Developers Games, Google Play policy, Xbox Accessibility Guidelines, GDC Vault, Game Developer, Games User Research, GameDiscoverCo, GameAnalytics, 80 Level, The Level Design Book, Game Accessibility Guidelines, SteamDB, How To Market A Game, Deconstructor of Fun, GPUOpen, Hada GeekNews.

### Prompt / agent / Skill

OpenAI official docs/Engineering/Academy, Anthropic Engineering/Docs, GitHub Copilot Docs, Google Developers Blog/Google Cloud AI/ADK, Microsoft Learn, Hada GeekNews.

### Fiction / interactive narrative

Reedsy, inkle/ink, Yarn Spinner, IGDA Game Writing, Emily Short, GDC narrative/game-writing sessions.

### YouTube / editing

YouTube Analytics/Studio Help/Creators, Blackmagic DaVinci Resolve Training, Frame.io Insider/Knowledge Center, vidIQ, GDC/Game Developer video-marketing cases.

## Adding new sites

조사 중 새 사이트 추가를 허용한다. 다음을 모두 요구한다.

```yaml
repeat_value_confirmed: true
recent_relevant_material_found_or_durable_reference_value: true
source_domain_declared: true
source_role_declared: true
current_pool_overlap_checked: true
commercial_or_vendor_interest_recorded: true
original_source_access_or_backtrace_value: true
owner_or_consumer_candidate_identified: true
```

단일 바이럴 글, 재게시 위주, SEO/affiliate 목적과 정보 가치가 분리되지 않는 Source, 기존 Source로 동일 원출처를 더 직접 확인할 수 있는 경우는 영구 Watchlist 추가를 보류한다.

## Processing pipeline

```text
SOURCE_INDEX_REFRESH
→ CANDIDATE_CAPTURE
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

## Domain-specific design decisions

### Prompt / agent / Skill

외부 자료에서 반복 확인되는 책임 배치 원리는 다음처럼 흡수한다.

```text
짧고 거의 항상 필요한 규칙 → global/repository instruction 후보
입력만 바뀌는 반복 요청 구조 → prompt/template 후보
특정 작업의 절차·reference·script를 on-demand로 로드 → Skill 후보
독립 tool/permission/persona/context/handoff → agent 후보
정확한 반복 검사·변환 → deterministic script/tool 후보
```

파일 수·Skill 수·agent 수 증가는 품질 지표가 아니다. 분리는 독립적으로 변경·테스트·라우팅 가능한 책임이 있을 때만 허용한다.

Eval은 모델 이름뿐 아니라 가능한 범위에서 harness, prompt, context, tools, permission, budget, retry/stop configuration을 기록한다.

### Fiction → game narrative

공통 재사용:

- character desire/conflict/action causality
- scene purpose/change
- setup/payoff
- information release
- voice/subtext/relationship
- continuity
- staged revision

게임 전용 추가:

- player agency/choice/state
- branching budget/convergence/replay/save-load
- system/quest/UI/input coupling
- localization/VO/runtime IDs

소설 craft는 게임 스토리에 `ADAPT` 후 실제 player/state context에서 `TEST`한다. 게임 branch/state 규칙을 선형 소설에 자동 강제하지 않는다.

### YouTube / editing

편집 순서는 기본적으로 다음을 따른다.

```text
STORY_AND_EVIDENCE_ROUGH_CUT
→ CLARITY_AND_PACING_TRIM
→ DIALOGUE_AND_AUDIO_CLEANUP
→ GRAPHICS_CAPTIONS_AND_CONTEXT
→ COLOR_VFX_AND_POLISH
→ EXPORT_AND_PLAYBACK_QC
```

Review는 versioned finding으로 추적한다. Retention drop/spike/rewatch와 CTR은 관찰이며 단독 인과 증거가 아니다. YouTube metric 정의는 공식 Help를 우선하고 vendor benchmark는 context-limited로 둔다.

## Recent-six-month bootstrap

```text
2026-02-10T00:00:00+09:00
→ 2026-08-10T23:59:59+09:00
```

- `FULL_INDEX_REVIEW`: 명시한 공개 index/archive/changelog 전체를 해당 기간에 대해 확인함.
- `PARTIAL_INDEX_REVIEW`: 검색/paywall/대량 콘텐츠/영상·강의 제한으로 기간 전체 corpus를 증명할 수 없음.
- `STATIC_REFERENCE_REVIEW`: 기간 밖 또는 정적이지만 장기 가치가 있는 Reference.

글 개수 집계보다 반복되고 서로 독립적으로 확인되는 공용 원리를 찾는다.

## Scheduler boundary

Base는 scheduler·webhook·background runner가 아니다. 실제 cadence는 ChatGPT Automation 또는 다른 외부 scheduler가 소유한다.

- 변화가 빠른 AI/플랫폼/Hada: daily-or-weekly 후보
- 게임 시장·creator·현업 blog: weekly 후보
- GDC/전문 archive/tooling: monthly/on-demand 후보
- 정적 craft/reference: quarterly/when-relevant 후보

주기 scan은 마지막 성공 scan 이후 delta를 우선한다. major policy/version/methodology 변화 시 범위를 확장한다.

## Adversarial lenses

- popularity를 truth로 오인했는가?
- 발견 글이 원출처 조건을 왜곡했는가?
- AAA/F2P/mobile/대형 creator/대형 agent 사례를 소규모 프로젝트에 과잉 일반화했는가?
- vendor benchmark를 공식 플랫폼 사실로 바꿨는가?
- 특정 prompt wording을 모델 불문 영구 공식으로 만들었는가?
- monolithic prompt를 파일로 나눈 것만으로 modularity를 주장했는가?
- Skill/agent 수 증가를 능력 향상으로 오인했는가?
- 소설의 선형 규칙과 게임 agency/state를 혼동했는가?
- YouTube retention/CTR을 판매·품질의 인과로 오인했는가?
- 최신 6개월에 집중해 오래된 유효한 원리·표준·craft를 버렸는가?
- 열린 PR이 같은 owner를 수정 중인데 중복 구현했는가?

## Change authority

`LOW_RISK_BOUNDED_UPDATE`는 작은 가역 변경, 기존 owner의 Reference/Evidence/stale link 보강, 권한·Schema·Skill identity 불변, 원출처/현재 Base/열린 PR 비교, 실제 검증 가능 조건을 모두 만족할 때만 허용한다.

다음은 `BCP_OR_USER_DECISION`이다.

- 제품/게임/소설/채널 핵심 방향
- Base 공용 정책 의미
- ACTIVE Skill 추가·제거·ID·owner 변경
- behavior-result schema/eval identity 비호환 변경
- workflow write 권한·보안·인증
- 라이선스·법적 판단
- 대규모 migration
- 특정 창작자 표현 복제

## Validation

Repository contract는 최소 다음을 확인한다.

- Watchlist와 recent review 존재.
- 5개 domain과 핵심 Source가 존재.
- Watchlist가 Hub/Method/Planning/AI Skill Guide/Narrative Method/YouTube Skill에서 one-hop 발견된다.
- narrative template가 존재하지 않는 legacy method를 참조하지 않는다.
- discovery feed가 권위로 승격되지 않는다.
- original-source backtrace, FULL/PARTIAL/STATIC review, new-site gate, adversarial lenses, change authority가 존재한다.
- 새 ACTIVE Skill은 추가되지 않는다.
- CI는 read-only를 유지하고 전용 contract를 실행한다.
