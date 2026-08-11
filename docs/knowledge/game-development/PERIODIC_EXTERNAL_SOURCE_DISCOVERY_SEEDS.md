# 주기적 Base 외부 Source — Active Discovery Seeds

```yaml
seed_role: periodic-base-improvement-active-discovery-seeds
owner_policy: docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
status: ACTIVE_DISCOVERY_SEED
scheduler_authority: EXTERNAL_TO_BASE
promotion_target:
  - docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md
  - docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json
```

## 1. 목적과 권위 경계

이 파일은 사용자가 직접 지정했거나, 아직 `repeat_value_confirmed: true`를 충분히 입증하지 못했지만 **지금부터 주기 스캔에서 참고할 가치가 있는 Source seed**를 기록한다.

이 파일은 `PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md`를 대체하는 두 번째 Source canon이 아니다. 모든 seed는 기존 Watchlist의 Source role, Evidence tier, `ORIGINAL_SOURCE_BACKTRACE`, Existing Solution First, 적대적 검토, 새 사이트 추가 Gate를 그대로 따른다.

`ACTIVE_DISCOVERY_SEED`는 **스캔 대상에는 즉시 포함**하지만 Evidence 권위를 자동 상승시키지 않는다는 뜻이다. 반복적으로 material candidate를 만들고 기존 Gate를 통과했을 때만 durable Watchlist와 `PERIODIC_SOURCE_OPERATIONS_LEDGER.json`의 고유 Source family로 승격한다.

## 2. GitHub — repository discovery surface

```yaml
seed_id: github-repositories-discovery
name: GitHub repositories / releases / issues / pull requests / discussions
url: https://github.com/
status: ACTIVE_DISCOVERY_SEED
source_role: DISCOVERY_FEED
domains:
  - GAME_DEVELOPMENT
  - CODE_ENGINEERING
  - PROMPT_AND_AGENT_WORKFLOW
  - SKILL_AUTHORING_AND_EVOLUTION
recommended_cadence: daily-or-weekly
scan_surfaces:
  - repositories
  - repository search and topics
  - releases and tags
  - issues
  - pull requests
  - discussions
  - examples and templates
  - linked documentation
```

### 2.1 무엇을 찾는가

GitHub에서는 다음과 같은 기존 해법과 원출처 후보를 찾는다.

- Godot addon/plugin/tool과 실제 source repository
- game-development utilities, templates, demos, build/export tooling
- 코드·테스트·CI·보안·dependency tooling
- prompt/agent/Skill 구현 사례와 evaluation harness
- 프로젝트가 이미 사용하는 dependency의 release, issue, pull request, migration 정보

### 2.2 GitHub evidence ceiling

GitHub는 **호스팅 플랫폼**이므로 GitHub에 존재한다는 사실만으로 권위가 생기지 않는다.

- `stars`, forks, contributors 수, `trending` 노출, 조회수성 popularity signal은 Evidence tier가 아니다.
- official upstream repository라면 **그 프로젝트 자신의** code/release/tag 상태에 한해서 owner와 repository identity, branch/tag/release, exact version을 확인한 뒤 primary evidence 후보가 될 수 있다.
- third-party repository는 maintenance, license, permissions, engine/runtime compatibility, security provenance, tests, actual consumer fit를 별도로 확인한다.
- open `issues`, `pull requests`, `discussions`는 shipped behavior 또는 fixed behavior가 아니다.
- README의 claim과 실제 release/source/test가 충돌하면 실제 versioned source와 실행 증거를 우선 확인한다.
- 기존 Watchlist의 `GitHub Copilot Docs`와 `GitHub Actions / Code Security Docs`는 GitHub 제품 사실의 `AUTHORITY_TARGET` owner를 계속 유지한다. 이 seed가 그 책임을 대체하지 않는다.

판정 흐름:

```text
GitHub discovery
→ official upstream / third-party / fork / archive 구분
→ exact owner + repository + version/tag/commit
→ release / source / issue / PR / discussion lifecycle 구분
→ license + maintenance + permissions + compatibility + security provenance
→ existing Base/project owner overlap
→ ADOPT | ADAPT | TEST | AVOID | IGNORE | REFERENCE_ONLY
```

## 3. 1인 개발자 YouTube — `@zang_gamedev`

```yaml
seed_id: youtube-solo-gamedev-zang
name: Zang Gamedev YouTube
url: https://www.youtube.com/@zang_gamedev
status: ACTIVE_DISCOVERY_SEED
source_roles:
  - PROFESSIONAL_PRACTICE
  - DISCOVERY_FEED
domains:
  - GAME_DEVELOPMENT
  - YOUTUBE_AND_VIDEO_EDITING
recommended_cadence: weekly
scan_surfaces:
  - Shorts
  - long-form videos
  - playlists when available
  - descriptions and linked project/source pages
```

이 채널은 사용자가 직접 지정한 **1인 개발자 참고 seed**다. 현재 작업 환경에서는 채널 corpus를 안정적으로 fetch/index하지 못했기 때문에 다음은 이번 등록만으로 사실 확정하지 않는다.

```text
구독자 수
업로드 수
실제 1인/팀 규모의 세부 상태
개발 중인 프로젝트명·출시 상태
특정 영상의 주장·성과
조회수·CTR·retention·매출 효과
```

위 항목은 실제 해당 surface를 읽은 scan에서만 채우며, 그 전에는 `BLOCKED_UNVERIFIED`다.

### 3.1 Shorts와 long-form을 분리해서 본다

**Shorts**는 빠른 discovery에 사용한다.

- 짧은 hook와 문제 제시 방식
- 개발 진행 beat와 before/after
- 짧은 gameplay·UI·tool demonstration
- 빠르게 반복되는 제작/마케팅 가설 후보
- 더 긴 설명이나 repository/project page로 따라갈 원출처 단서

Shorts 하나만 보고 복잡한 개발 원인, 상업적 성공 원인, 보편적인 제작 규칙을 확정하지 않는다.

**long-form videos / devlogs**는 더 긴 맥락 후보로 사용한다.

- 제작 의도와 실제 constraint
- scope trade-off와 우선순위
- 구현 과정과 실패·수정 chronology
- 개발 workflow와 tool 선택 이유
- launch/marketing/postmortem self-report

long-form도 단일 creator의 `PROFESSIONAL_PRACTICE` 또는 self-report 맥락이며 Base 공용 Hard Rule이 아니다. 중요한 기술 사실은 repository, engine/platform official docs, release note 등으로 `ORIGINAL_SOURCE_BACKTRACE`한다.

### 3.2 format별 성과를 한 숫자로 섞지 않는다

YouTube official Analytics는 Videos와 Shorts를 별도 content type으로 볼 수 있고, 공식 Shorts analytics guidance는 audience behavior가 format마다 다르므로 **같은 format끼리 비교**하는 것이 중요하다고 설명한다.

따라서 periodic scan에서도 다음을 금지한다.

```text
Shorts 조회수 > long-form 조회수
→ Shorts 전략이 보편적으로 우월하다

long-form 평균 시청시간 > Shorts 평균 시청시간
→ long-form이 채널 성장에 항상 더 좋다

구독자·조회수 증가
→ 게임 수요·구매 의도·개발 방식의 우월성이 증명됐다
```

관련 current official starting points:

- YouTube Help — Content tab analytics tips: Shorts
  - https://support.google.com/youtube/answer/12942217?co=YOUTUBE._YTVideoType%3Dshorts&hl=en
- YouTube Help — Content tab analytics tips: Video
  - https://support.google.com/youtube/answer/12942217?co=YOUTUBE._YTVideoType%3Dvideo&hl=en
- YouTube Help — Understand your YouTube content performance
  - https://support.google.com/youtube/answer/12220281

## 4. 다른 1인 개발자 유튜버 확장 Gate

`@zang_gamedev`만 참고하는 것으로 고정하지 않는다. periodic scan에서 다른 1인/소규모 게임 개발 creator가 발견되면 **후보 seed**로 비교할 수 있다.

영구 Watchlist/Ledger 승격 전에는 기존 새 사이트 Gate와 함께 최소 다음을 확인한다.

```yaml
repeat_value_confirmed: true
recent_relevant_material_found_or_durable_reference_value: true
solo_or_small_team_context_identified: true
shorts_or_long_form_surface_identified: true
source_domain_declared: true
source_role_declared: true
current_pool_overlap_checked: true
commercial_or_sponsor_interest_recorded: true
original_source_access_or_backtrace_value: true
owner_or_consumer_candidate_identified: true
popularity_is_not_authority: true
```

다음은 영구 source 확장 근거로 쓰지 않는다.

- viral Short 하나만 유용함
- 구독자·조회수가 높다는 이유만으로 선정
- 다른 개발자의 내용을 재가공만 함
- sponsor/affiliate와 독립 경험을 구분하기 어려움
- 실제 개발 project/source를 확인할 수 없음
- creator 수를 늘리는 것 자체가 목표가 됨

## 5. Seed scan 결과

각 scan은 seed마다 다음 중 하나로 닫는다.

```text
MATERIAL_CANDIDATE
REFERENCE_ONLY
NO_CHANGE
PROMOTION_CANDIDATE
BLOCKED_UNVERIFIED
```

`PROMOTION_CANDIDATE`는 자동 승격이 아니다. 기존 Watchlist의 new-site Gate, Existing Solution First, 적대적 검토, owner/consumer 연결, 실제 PR/exact-head 검증을 통과해야 한다.

실질적인 개선이 없으면 `NO_CHANGE`로 닫고, seed를 추가했다는 이유만으로 새 Skill·규칙·문서 변경을 계속 만들지 않는다.
