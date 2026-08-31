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

## 5. Pixel Art / low-resolution 2D game art

픽셀아트·도트·저해상도 2D를 프로젝트가 선택한 경우, 단순 이미지 레퍼런스뿐 아니라 **제작 기법 → 도구/내보내기 → Godot 표시/임포트 → 실제 용량·가독성 검증**까지 한 흐름으로 조사한다. Pixel art is not a Base-wide default. 실제 프로젝트의 아트 방향은 기존 `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`가 계속 소유한다.

```yaml
seed_group: pixel-art-low-resolution-2d
status: ACTIVE_DISCOVERY_SEED
domains:
  - GAME_DEVELOPMENT
  - CODE_ENGINEERING
recommended_cadence: weekly-or-when-art-direction-active
existing_consumers:
  art_direction_and_project_fit: docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md
  technique_cards_and_visual_qa: skills/designing-art-prompts-and-technique-cards/SKILL.md
  godot_render_import_behavior: existing Godot AUTHORITY_TARGET + target project implementation owner
  size_and_delivery_claims: docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
```

### 5.1 Aseprite — 공식 도구·production workflow

```yaml
seed_id: aseprite-official
name: Aseprite official docs + official repository
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
urls:
  docs: https://www.aseprite.org/docs/
  repository: https://github.com/aseprite/aseprite
scan_surfaces:
  - animation, frames, cels, layers and tags
  - tilemap and tileset workflows
  - indexed color and palette workflows
  - sprite sheet export and metadata
  - slices and reusable export structure
  - CLI and scripting/automation
  - releases and source repository
```

Aseprite는 **Aseprite 자체 기능·동작·workflow**에 대해서만 `AUTHORITY_TARGET`이다. Aseprite에서 가능한 방식이 모든 픽셀아트의 보편 법칙이라는 뜻은 아니다.

- 실제 사용 version과 문서/release 상태를 확인한다.
- source repository와 배포 binary의 라이선스·사용 조건을 혼동하지 않는다.
- Aseprite가 편리하다는 이유로 모든 프로젝트의 필수 도구로 강제하지 않는다.
- stars, forks, community popularity는 Evidence 권위를 올리지 않는다.

### 5.2 Godot — 기존 공식 authority의 pixel-art surface 재사용

Godot은 새 Source family를 만들지 않고 기존 Watchlist의 `Godot Engine official docs / blog / releases` `AUTHORITY_TARGET`을 재사용한다. pixel-art 작업에서는 현재 stable/versioned 문서에서 다음을 우선 확인한다.

```text
multiple resolutions for pixel art
→ viewport stretch
→ integer scaling
→ nearest texture filtering
→ 2D texture import / compression / mipmap behavior
→ Sprite2D / atlas / sprite sheet integration
→ TileSet / TileMap integration
```

- `nearest`는 픽셀 경계를 보존해야 하는 대상의 후보이지 모든 2D texture에 자동 적용하는 규칙이 아니다.
- `integer scaling`과 viewport/base resolution은 목표 화면비·카메라·UI·플랫폼을 함께 본다.
- 특정 문서의 예시 base resolution을 Base-wide 고정값으로 승격하지 않는다.
- stable/RC/dev와 exact Godot version을 구분하고, 미출시 문서를 현재 shipped behavior처럼 쓰지 않는다.

### 5.3 Saint11 / Pedro Medeiros — 픽셀 제작 기법

```yaml
seed_id: saint11-pixel-art-techniques
name: Saint11 / Pedro Medeiros Pixel Art Tutorials
status: ACTIVE_DISCOVERY_SEED
source_role: PROFESSIONAL_PRACTICE
url: https://saint11.org/blog/pixel-art-tutorials/
scan_surfaces:
  - beginner series and compact tutorials
  - pixel clusters and cluster economy
  - shading and value grouping
  - anti-aliasing, dithering and banding
  - line work and shape readability
  - color and palette decisions
  - animation and motion readability
  - export habits and production examples
  - original tutorial repository when provenance is useful
```

Saint11 자료는 원저자의 교육·실무 기법을 이해하는 `PROFESSIONAL_PRACTICE`다. 한 튜토리얼을 필수 제작 법칙으로 만들지 않고, 프로젝트의 sprite size·시점·장르·팔레트·animation budget에 맞게 `ADAPT` 또는 `TEST`한다. 완성 예시나 식별 가능한 디자인·특정 작가의 signature style을 그대로 복제하지 않는다.

### 5.4 Lospec — palette·tutorial·tool discovery

```yaml
seed_id: lospec-pixel-art-discovery
name: Lospec
status: ACTIVE_DISCOVERY_SEED
source_roles:
  - DISCOVERY_FEED
  - PROFESSIONAL_PRACTICE_WHEN_LOSPEC_AUTHORED
url: https://lospec.com/
scan_surfaces:
  - tutorial index and original-author links
  - palette list
  - pixel-art software/tool list
  - pixel editor and restrictive-art utilities
  - scaler / rotator and related tools
```

Lospec은 여러 튜토리얼·팔레트·도구를 찾는 데 유용하지만, aggregation 자체가 원저자 권위를 대체하지 않는다. 제3자 tutorial은 가능한 경우 `ORIGINAL_SOURCE_BACKTRACE`한다.

- palette 인기·좋아요·노출은 프로젝트 적합성 증거가 아니다.
- palette page에 있다는 이유만으로 제품 사용 권리·라이선스가 자동 확인된 것으로 보지 않는다.
- 도구 출력이 pixel-art readability·identity·성능을 자동 증명하지 않는다.

### 5.5 PixelJoint — community visual reference

```yaml
seed_id: pixeljoint-community-reference
name: PixelJoint
status: ACTIVE_DISCOVERY_SEED
source_role: DISCOVERY_FEED
observational_role: COMMUNITY_VISUAL_REFERENCE
url: https://pixeljoint.com/
scan_surfaces:
  - gallery and artist pages
  - weekly challenges
  - forums and critique comments
  - cluster, palette, animation and readability comparisons
```

PixelJoint는 시각 어휘·비교·반례·critique 질문을 발견하는 community reference다. ratings, favorites, featured 여부, 조회 반응은 품질 권위나 시장 성과 증거가 아니다. 특정 작품의 실루엣·캐릭터·구도·palette 조합·signature style을 복제하지 않는다.

### 5.6 Pixel-art technique scan route

실제 프로젝트의 pixel-art 관련 의사결정이 있을 때 다음 질문을 우선 조사한다.

```text
canvas / base resolution
→ sprite scale + viewing distance + silhouette
→ pixel clusters + line economy
→ palette + value grouping
→ shading + dithering + anti-aliasing + banding
→ tile/grid reuse + seam/variation
→ frame count + timing + animation readability
→ layer/tag/slice + sprite sheet export
→ Godot nearest + integer scaling + render/import settings
→ actual build / installed / runtime evidence
→ rights + provenance + similarity QA
```

소스별 결과는 기존 owner로 보낸다.

```text
아트 방향·가독성·제작성 적합성
→ ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md

기법 정리·프롬프트·후보 제작·visual QA
→ designing-art-prompts-and-technique-cards

Godot filtering·scaling·import·TileMap 구현 사실
→ 기존 Godot AUTHORITY_TARGET + 프로젝트 구현 owner

용량·메모리·전달 효과
→ GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md
```

### 5.7 픽셀아트 과장 방지 Gate

다음은 이번 source 추가만으로 사실이 되지 않는다.

```text
pixel art does not automatically prove a smaller shipped build
fewer colors do not automatically prove better readability
nearest is not correct for every 2D texture
one low base resolution is not universally optimal
Aseprite is not mandatory for pixel-art production
Lospec palette availability does not prove project fit or product-use rights
PixelJoint popularity does not prove quality or market demand
one Saint11 technique is not a universal hard rule
tutorial/gallery reference does not grant permission to copy identifiable artwork or a creator's signature style
```

특히 용량 절감이 선택 이유에 포함되면 `GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`의 기존 측정 계약으로 **actual build**를 비교한다. `sprite_and_2d_art` bytes, 필요한 경우 DOWNLOAD / INSTALLED / RUNTIME / PATCH 영향, atlas/import 설정, 중복 variant, 품질·가독성 회귀를 확인하기 전에는 용량 이득을 `BLOCKED_UNVERIFIED`로 둔다.

낮은 source resolution, 제한 palette, indexed authoring이 일부 source/texture data를 줄일 가능성은 **가설**일 수 있으나, engine resource·atlas padding·lossless compression·import 설정·audio/video·package 구조가 전체 용량을 지배할 수 있으므로 실제 빌드 측정 없이 성과로 승격하지 않는다.

## 6. Backend / API engineering

백엔드·API를 실제 구현할 때는 framework 하나를 정답으로 고정하지 않고 **계약 → 상태/트랜잭션 → 인증/인가 → 보안 → 운영/관측 → 프로젝트 테스트** 순으로 조사한다. 설계·배포 판정의 기존 owner는 `GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`다.

```yaml
seed_group: backend-api-engineering
status: ACTIVE_DISCOVERY_SEED
domains:
  - CODE_ENGINEERING
  - GAME_DEVELOPMENT
recommended_cadence: weekly-or-when-backend-active
existing_consumers:
  backend_architecture_and_deployment: docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md
  implementation_and_tests: target project backend implementation owner
```

### 6.1 OpenAPI Specification — API 계약 표준

```yaml
seed_id: openapi-specification
name: OpenAPI Specification
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://spec.openapis.org/oas/latest.html
scan_surfaces:
  - paths and operations
  - request and response schemas
  - components and reusable schemas
  - security schemes
  - versioned specification releases
```

OpenAPI Specification은 OAS 자체의 구조·의미에 대한 authority다. API 문서가 존재한다는 사실만으로 실제 서버 구현, 인증, 호환성, 성능 또는 보안이 검증됐다고 보지 않는다.

### 6.2 FastAPI official — Python API framework behavior

```yaml
seed_id: fastapi-official
name: FastAPI official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://fastapi.tiangolo.com/
scan_surfaces:
  - OpenAPI and JSON Schema generation
  - validation and dependency injection
  - authentication and security helpers
  - async and WebSocket behavior
  - testing and deployment guidance
  - release and migration notes when relevant
```

FastAPI official 문서는 FastAPI 자체 동작과 지원 workflow에 대해서만 authority다. **FastAPI official** 자료가 유용하더라도 FastAPI를 모든 Base 프로젝트의 mandatory backend framework로 만들지 않는다.

### 6.3 PostgreSQL / Redis official — durable state와 조건부 data services

```yaml
seed_id: postgresql-official
name: PostgreSQL official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://www.postgresql.org/docs/current/
scan_surfaces:
  - transactions and isolation
  - indexing and query behavior
  - constraints and concurrency
  - backup / restore and operations
  - supported-version release notes

seed_id: redis-official
name: Redis official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET_WHEN_SELECTED
url: https://redis.io/docs/latest/
scan_surfaces:
  - data types
  - persistence
  - caching and expiration
  - streams / queues when selected
  - clustering and operations when selected
```

**PostgreSQL official**과 Redis official은 각 제품 동작의 authority일 뿐, 둘을 함께 쓰거나 특정 data architecture를 채택해야 한다는 뜻이 아니다. 실제 schema, transaction, cache, queue 선택은 프로젝트 요구·복잡도·운영비·복구 요구로 판단한다.

### 6.4 OWASP API Security — 공격 surface와 검토 질문

```yaml
seed_id: owasp-api-security
name: OWASP API Security Project
status: ACTIVE_DISCOVERY_SEED
source_role: PROFESSIONAL_SECURITY_GUIDANCE
url: https://owasp.org/API-Security/
scan_surfaces:
  - API Security Top 10
  - authorization and authentication risks
  - resource consumption and rate-limit risks
  - inventory and version management
  - unsafe third-party API consumption
```

**OWASP API Security**는 위협과 검토 질문을 제공하지만 checklist를 읽거나 static scan이 통과했다는 사실은 security/compliance PASS가 아니다. 실제 프로젝트에서는 threat model, authz tests, abuse/rate-limit tests, secret handling, dependency 상태와 runtime evidence를 별도로 확인한다.

FastAPI / PostgreSQL / Redis는 후보 stack이지 Base-wide 필수 조합이 아니다.

## 7. AI coding / coding agents

AI 코딩 Source는 기능 discovery와 tool-specific authority를 제공하지만 모델 이름·vendor marketing·leaderboard가 프로젝트 품질을 대신하지 않는다. 기존 owner는 `AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md`이며 실제 merge 판단은 repository diff·테스트·보안·review evidence가 담당한다.

```yaml
seed_group: ai-coding-agents
status: ACTIVE_DISCOVERY_SEED
domains:
  - CODE_ENGINEERING
  - PROMPT_AND_AGENT_WORKFLOW
  - SKILL_AUTHORING_AND_EVOLUTION
recommended_cadence: weekly-or-when-tool-selection-active
existing_consumers:
  ai_work_package_and_evals: docs/knowledge/game-development/AI_ASSISTED_GAME_DEVELOPMENT_GUIDE.md
  repository_validation: target project tests + review + exact-head CI
```

### 7.1 Vendor official coding-agent sources

```yaml
seed_id: openai-codex-official
name: OpenAI Developers / Codex official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://developers.openai.com/

seed_id: anthropic-claude-code-official
name: Anthropic Claude Code official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://docs.anthropic.com/en/docs/claude-code/overview

seed_id: google-gemini-coding-official
name: Gemini CLI / Gemini Code Assist official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
urls:
  gemini_cli: https://geminicli.com/docs/
  gemini_code_assist: https://developers.google.com/gemini-code-assist/docs
```

`OpenAI Developers / Codex`, `Claude Code`, `Gemini CLI`/Gemini Code Assist 자료는 각 제품의 현재 기능·설정·권한·workflow·제한에 대해서만 authority다. 기존 Watchlist의 GitHub Copilot Docs `AUTHORITY_TARGET`은 그대로 재사용하며 새 중복 family를 만들지 않는다.

### 7.2 aider — open-source terminal workflow reference

```yaml
seed_id: aider-official
name: aider official docs + repository
status: ACTIVE_DISCOVERY_SEED
source_roles:
  - PROFESSIONAL_PRACTICE
  - DISCOVERY_FEED
urls:
  docs: https://aider.chat/docs/
  repository: https://github.com/Aider-AI/aider
scan_surfaces:
  - repository mapping and context
  - git integration
  - lint / test workflow
  - model/provider support
  - release and compatibility notes
```

`aider`에서 유용한 workflow가 발견돼도 현재 Base/Codex 권한 모델을 자동 대체하지 않고 Existing Solution First로 ADAPT/TEST한다.

### 7.3 SWE-bench — benchmark evidence ceiling

```yaml
seed_id: swe-bench
name: SWE-bench official benchmark / leaderboard / papers
status: ACTIVE_DISCOVERY_SEED
source_role: OBSERVATIONAL_BENCHMARK
url: https://www.swebench.com/
scan_surfaces:
  - benchmark definitions and variants
  - verified task sets
  - evaluation harness
  - leaderboard and paper methodology
```

SWE-bench는 coding-agent 성능 비교를 위한 benchmark/discovery evidence다. **benchmark score does not prove project correctness**. leaderboard 순위나 vendor 발표만으로 생산성·보안·유지보수성·현재 Base 적합성·merge readiness를 확정하지 않는다. 실제 프로젝트의 Golden Set, representative task, diff review, focused/regression tests, security checks와 exact-head CI를 우선한다.

모델·제품 기능·가격·quota·preview/GA 상태는 변동 가능성이 높으므로 도입 시점의 공식 문서를 다시 확인한다.

## 8. Deployment / WAS / cloud runtime

배포 provider는 단일 순위로 고르지 않는다. 현재 Base의 backend owner가 이미 Cloud Run을 적합한 stateless HTTPS/container workload의 기본 후보로 다루므로 이를 유지하고, workload가 달라질 때의 비교 Source를 추가한다. **Cloud Run is not universally better**.

```yaml
seed_group: deployment-was-cloud-runtime
status: ACTIVE_DISCOVERY_SEED
domains:
  - CODE_ENGINEERING
  - GAME_DEVELOPMENT
recommended_cadence: weekly-or-before-provider-decision
existing_consumers:
  architecture_and_provider_fit: docs/knowledge/game-development/GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md
```

### 8.1 Google Cloud Run — 기존 owner 기본 후보 유지

Google Cloud Run 공식 docs는 기존 `GAME_BACKEND_CLOUD_RUN_AND_ONLINE_SERVICES_GUIDE.md`의 source authority를 재사용한다. service/job/worker-pool, container runtime, IAM, scaling, request timeout, WebSocket, secrets, observability와 비용 관련 current behavior를 구현 전에 재확인한다.

### 8.2 Cloudflare Workers — edge/serverless 후보

```yaml
seed_id: cloudflare-workers-official
name: Cloudflare Workers official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://developers.cloudflare.com/workers/
scan_surfaces:
  - Workers runtime and limits
  - bindings
  - Durable Objects
  - KV / D1 / R2 integration when relevant
  - Queues / Workflows / scheduled work
  - observability and deployment
```

**Cloudflare Workers**는 edge/global request handling이나 Cloudflare-native bindings가 중요한 경우 비교 후보지만, 모든 container workload의 drop-in replacement라고 가정하지 않는다.

### 8.3 Fly.io Machines — lower-level VM/runtime control 후보

```yaml
seed_id: fly-machines-official
name: Fly.io Machines official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://fly.io/docs/machines/
scan_surfaces:
  - Machines lifecycle
  - regions and placement
  - volumes and persistent cases
  - networking
  - scaling and API control
```

**Fly.io Machines**는 region placement, VM lifecycle, lower-level runtime control이나 조건부 persistent volume이 필요한 경우 비교한다. 운영 책임과 복구/업데이트 복잡도가 증가할 수 있으므로 실제 workload로 판단한다.

### 8.4 Railway / Render — simple PaaS 비교 후보

```yaml
seed_id: railway-official
name: Railway official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://docs.railway.com/
scan_surfaces:
  - services and deployments
  - GitHub / Docker deployment
  - variables and environments
  - scheduled jobs
  - volumes / databases when selected
  - observability and rollback

seed_id: render-official
name: Render official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://render.com/docs
scan_surfaces:
  - web and private services
  - background workers and cron jobs
  - Docker / Git deployment
  - managed datastores when selected
  - health checks and operations
```

**Railway**와 **Render**는 작은 팀의 배포 편의·managed service 운영비를 줄일 가능성이 있는 비교 후보지만, vendor convenience 자체가 성능·가용성·가격 우월성을 증명하지 않는다.

### 8.5 Provider comparison Gate

```text
workload shape + protocol
→ durable state / consistency
→ latency + region placement
→ request / connection / background lifetime
→ scaling + cold start
→ operational burden + observability
→ quotas + abuse/failure behavior
→ portability + provider lock-in + exit path
→ measured cost
→ project runtime/load/failure evidence
```

Cloud Run, Workers, Fly.io, Railway, Render 가운데 어느 것도 글로벌 winner로 두지 않는다. 실제 provider 채택은 기존 backend owner의 `CLOUD_RUN_RECOMMENDED | CLOUD_RUN_CONDITIONAL | ALTERNATIVE_ARCHITECTURE_REQUIRED | SERVER_NOT_REQUIRED | BLOCKED_UNVERIFIED` 판정을 따른다.

## 9. PC capture and AI-assisted media editing

게임 플레이·개발 화면 촬영과 편집 Source는 **capture → local processing → story/evidence edit → image/thumbnail edit → export/QC**로 조사한다. 영상 제작 owner는 `producing-game-development-youtube-videos`, 이미지·썸네일 후보는 `designing-art-prompts-and-technique-cards`와 art-direction owner에 연결한다.

```yaml
seed_group: pc-capture-ai-media-editing
status: ACTIVE_DISCOVERY_SEED
domains:
  - YOUTUBE_AND_VIDEO_EDITING
  - GAME_DEVELOPMENT
recommended_cadence: weekly-or-when-video-production-active
existing_consumers:
  video_story_capture_edit_publish: skills/producing-game-development-youtube-videos/SKILL.md
  image_thumbnail_and_visual_qa: skills/designing-art-prompts-and-technique-cards/SKILL.md + art-direction owner
```

### 9.1 OBS Studio / FFmpeg — capture와 local media pipeline

```yaml
seed_id: obs-studio-official
name: OBS Studio official Knowledge Base
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://obsproject.com/kb
scan_surfaces:
  - Game Capture / Window Capture / Display Capture
  - recording settings and encoders
  - multiple audio tracks and application audio
  - troubleshooting and performance guidance

seed_id: ffmpeg-official
name: FFmpeg official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://ffmpeg.org/documentation.html
scan_surfaces:
  - capture inputs
  - codecs and containers
  - filters
  - transcode / remux / proxy generation
  - automation and metadata
```

**OBS Studio**와 **FFmpeg**는 각 도구의 기능 authority다. 지원 기능이 있다는 사실만으로 실제 게임과 동시에 녹화했을 때의 frame pacing, audio sync, encoder overhead, dropped frames, 저장장치 부하, 파일 크기 또는 시각 품질이 적합하다고 확정하지 않는다. 해당 PC와 실제 build에서 **actual PC capture measurement**를 수행한다.

### 9.2 Windows / NVIDIA low-friction capture 후보

```yaml
seed_id: windows-game-capture-official
name: Microsoft Xbox Game Bar / Snipping Tool official support
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://support.microsoft.com/windows

seed_id: nvidia-shadowplay-official
name: NVIDIA App / ShadowPlay official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET_WHEN_HARDWARE_APPLICABLE
url: https://www.nvidia.com/en-us/software/nvidia-app/
```

**Xbox Game Bar**는 빠른 Windows 캡처의 fallback 후보이며, **NVIDIA App / ShadowPlay**는 해당 NVIDIA hardware/driver 조건에서 비교한다. 편의성이 OBS의 scene/audio/automation 제어를 자동 대체하지 않는다.

### 9.3 DaVinci Resolve — desktop NLE / color / audio / VFX

```yaml
seed_id: davinci-resolve-official
name: DaVinci Resolve official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://www.blackmagicdesign.com/products/davinciresolve
scan_surfaces:
  - edit and delivery
  - Fairlight audio
  - color
  - Fusion VFX / motion
  - current Neural Engine / AI-assisted features
  - supported formats and system requirements
```

**DaVinci Resolve**의 AI/Neural Engine 기능도 제품 기능 authority일 뿐, 해당 기능이 항상 편집시간을 줄이거나 결과 품질을 높인다는 뜻은 아니다.

### 9.4 Adobe Premiere / Photoshop / Firefly — video + image AI editing

```yaml
seed_id: adobe-media-ai-official
name: Adobe Premiere / Photoshop / Firefly official documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
urls:
  premiere: https://helpx.adobe.com/premiere-pro/
  photoshop: https://helpx.adobe.com/photoshop/
  firefly: https://www.adobe.com/products/firefly.html
scan_surfaces:
  - text-based video editing and search
  - audio cleanup and caption workflows
  - generative extend / video features when currently available
  - Generative Fill / image retouching
  - Firefly image/video editing surfaces
  - availability, credits, model and plan requirements
```

**Adobe Premiere / Photoshop / Firefly**의 vendor feature claim은 Adobe 제품 동작 확인에만 사용한다. pricing, credits, commercial terms, model availability와 beta/GA 상태는 사용 시점에 다시 확인한다.

### 9.5 Runway — generative/editing workflow discovery

```yaml
seed_id: runway-media-editing-official
name: Runway official help / editing documentation
status: ACTIVE_DISCOVERY_SEED
source_role: AUTHORITY_TARGET
url: https://help.runwayml.com/hc/en-us
scan_surfaces:
  - current video editing / transformation tools
  - image editing tools
  - model availability and deprecations
  - upload/export constraints
  - plan / credit requirements when adoption is considered
```

**Runway**는 현재 제공되는 생성·편집 기능의 authority다. 빠르게 바뀌는 model/tool/deprecation 상태를 과거 튜토리얼로 추정하지 않는다.

### 9.6 Media evidence and rights Gate

```text
actual game/build + public boundary
→ capture method + encoder + resolution/FPS/audio tracks
→ actual PC capture measurement
→ rough cut / story evidence
→ AI-assisted edit only where it solves a defined task
→ output comparison + time/cost measurement
→ rights + provenance + similarity
→ export/playback QC
→ publish gate
```

AI 영상·이미지 편집 기능의 존재는 source asset 사용권이나 생성 결과의 제품 사용 가능성을 자동 보장하지 않는다. 음악·폰트·게임 asset·외부 footage·업로드 이미지의 권리와 vendor 약관을 확인하고, 식별 가능한 third-party work 또는 creator signature style 유사성은 기존 art/reference QA에서 재검토한다.

OBS/FFmpeg/DaVinci/Adobe/Runway 기능 설명이나 vendor demo만으로 실제 제작시간 절감, 품질 개선, 저비용, 저오버헤드 또는 수익 개선을 성과로 기록하지 않는다. 실제 프로젝트의 capture/edit 시간, dropped frames, file size, export time, correction 횟수와 human viewing evidence가 필요하다.

## 10. 공통 과장 방지와 freshness Gate

다음은 모든 신규 source group에 적용한다.

```text
framework availability != mandatory architecture
security guidance or static scan != security/compliance PASS
AI coding benchmark or vendor demo != project correctness / productivity / merge readiness
cloud provider feature list != workload fit / reliability / lowest cost
capture feature support != acceptable recording performance
AI edit feature availability != rights clearance or output quality
```

vendor pricing, quota, region, model, plan, preview/GA/deprecation 상태는 변동 가능성이 높다. 실제 채택 직전에 current official source를 다시 읽고 `SOURCE_CONTEXT_PACKET`의 `checked_at`, `availability_or_policy_state`, `affected_versions_or_surfaces`, `action_window`을 채운다.

## 11. Seed scan 결과

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

## 12. Notion skills, work structure, and utilization workflow

Notion은 Base의 정본이나 필수 workspace로 승격하지 않는다. **공식 제품 사실과 비공식 현업·게임 제작·연구 사례를 구분해 조사**하고, 검증된 원리만 기존 Base owner에 최소 흡수한다. 아래 `source_role`은 공식 URL의 Notion 제품 동작에만 적용하며, 실무 사례의 역할은 12.3에서 별도로 판정한다.

현행 권위는 `docs/DESKTOP_GPT_REPOSITORY_FIRST_WORKSPACE_POLICY.md`다. `NO_NEW_NOTION_WRITE_BY_DEFAULT`, `FIGMA_USAGE: DISABLED_BY_USER`를 유지한다. Notion을 조사한다는 이유로 workspace·DB·Agent를 만들거나 Figma/Huddling을 활성 참고 소스·권장 도구로 재도입하지 않는다.

```yaml
seed_group: notion-skills-work-structure
status: ACTIVE_DISCOVERY_SEED
domains:
  - PROMPT_AND_AGENT_WORKFLOW
  - SKILL_AUTHORING_AND_EVOLUTION
source_role: AUTHORITY_TARGET_FOR_NOTION_BEHAVIOR
recommended_cadence: weekly
urls:
  skills: https://www.notion.com/help/skills-for-notion-agent
  skills_current: https://www.notion.com/help/create-and-manage-skills
  custom_agents: https://www.notion.com/help/custom-agents
  notion_mcp: https://www.notion.com/help/notion-mcp
  databases: https://www.notion.com/help/category/databases
  database_automations: https://www.notion.com/help/database-automations
  backup: https://www.notion.com/help/back-up-your-data
  releases: https://www.notion.com/releases
  developers: https://developers.notion.com/
scan_surfaces:
  - Skills for Notion Agent and reusable task instructions
  - persistent Instructions vs task-scoped Skills vs autonomous Custom Agents
  - manual and automatic Skill routing, description eligibility and local export
  - databases, projects/tasks, views, relations, rollups, formulas and templates
  - database automations, buttons, triggers, webhooks and failure boundaries
  - Notion MCP, API, permissions and connected-app boundaries
  - Workers, CLI and Agent SDK only when a current official surface is verified
  - release notes, beta/general availability and plan/seat changes when adoption depends on them
  - export coverage and legacy migration without reactivating Notion as canon
```

### 12.1 흡수 질문

```text
반복 작업을 매번 긴 prompt로 다시 쓰고 있는가?
→ persistent preference는 instruction, 특정 작업의 반복 절차는 skill, 시간/이벤트 기반 자율 실행은 agent/automation으로 책임을 분리할 수 있는가?
→ database property·view·relation이 실제 의사결정과 handoff를 줄이는가, 아니면 관리 오버헤드만 늘리는가?
→ template/button/automation이 반복 수작업을 줄이되 숨은 side effect와 권한 확대를 만들지 않는가?
→ Notion MCP/API가 repository owner를 대체하려는가, 아니면 승인된 legacy 이관·프로젝트 예외에만 필요한가?
→ 공식 기능과 현업 사례에서 추출한 원리가 Base의 기존 Skill/Mode/Template에 이미 있는가?
→ 기능 availability·plan·permission이 바뀌어도 Base 정본과 프로젝트 실행이 깨지지 않는가?
```

### 12.2 승격 경계

- Notion 기능명이 생겼다는 이유로 새 `notion-*` Skill을 만들지 않는다.
- 반복 가치가 검증된 원리만 기존 owner에 `ADAPT`; 이미 있는 계약은 `ALREADY_COVERED`로 닫는다.
- Notion 페이지·database를 Base/GitHub 정본보다 높은 권한으로 만들지 않는다.
- 별도 유료 플랜·AI credit·API 비용·automation quota가 필요한 경로는 `ZERO_INCREMENTAL_COST_REQUIRED`와 새 사용자 승인을 통과하기 전 활성화하지 않는다.
- 실제 연결 workspace를 읽거나 쓰지 않은 조사에서는 Notion 사용 완료·자동화 동작을 주장하지 않는다.
- 실질 개선이 없으면 `NO_CHANGE`로 닫는다. Source 등록·문서 변경·큐 게시만으로 예약 실행 또는 심층 조사 완료가 증명되지는 않으며, 실행 증거가 없으면 `NOT_RUN`이다.

### 12.3 공식 외 현업·게임 제작·연구 source lane

아래는 같은 주간 seed의 조사 입력이다. 별도 scheduler나 새 정본이 아니다. 공식 문서는 Notion 제품 사실의 `AUTHORITY_TARGET`이고, 비공식 자료는 원저자·맥락·반례를 확인해 다음 역할로 사용한다.

| Source / 원문 시작점 | 역할 | 조사와 제한 |
|---|---|---|
| Notion VIP — https://www.notion.vip/insights/streamline-project-management-with-notion | `PROFESSIONAL_PRACTICE` | Projects/Tasks/Resources와 contextual view 원리를 비교한다. 컨설팅·템플릿 판매 이해관계가 있으며 특정 DB 수를 공용 규칙으로 복사하지 않는다. |
| Thomas Frank — https://thomasjfrank.com/docs/ultimate-tasks/databases/ | `PROFESSIONAL_PRACTICE` | 원저자의 Master DB·linked view 구조와 유지비를 비교한다. affiliate·template 사업 맥락을 기록하고 복잡한 전체 시스템을 자동 도입하지 않는다. |
| 인디/솔로 개발자·스튜디오의 공개 GDD, devlog, production workflow, postmortem | 원저자·프로젝트·조건 확인 후 `PROFESSIONAL_PRACTICE`; 그 전 `DISCOVERY_FEED` | 기존 GDC/Game Developer source에서 원 발표·개발자 자료로 역추적한다. 작업·버그·빌드·에셋·플레이테스트·출시/마케팅 연결과 실패 사례를 함께 본다. |
| Video Game Project Management Anti-patterns — https://arxiv.org/abs/2202.06183 | 원 연구의 표본·방법에 한정한 연구 근거 | 440개 postmortem **문제** 분석이다. 440개 게임 조사나 Notion 효과 실험이 아니다. Feature Creep·여러 프로젝트·도구 부적합을 검토 질문으로 사용한다. |
| Notion Marketplace의 게임 제작 템플릿·리뷰, Reddit·커뮤니티 | `DISCOVERY_FEED` | 제작자 원문·실제 사용 조건을 찾는 입력이다. 인기·별점·판매 문구·자기선택 후기만으로 생산성이나 게임 성공을 증명하지 않는다. |

원문의 `published_or_updated_at`과 이번 `checked_at`을 구분하고 `commercial_interest`, 표본·팀 규모·장르·도구·비용, `counterevidence`, 기존 owner, `actual_consumer`, 최소 변경과 폐기 조건을 기존 `SOURCE_CONTEXT_PACKET`에 기록한다. 원문을 못 읽은 범위는 `BLOCKED_UNVERIFIED`다. 문서 길이만으로 상세 GDD/PDF를 기각하지 않고 플레이어 경험·구현 이해에 필요한 설명인지, 중복 유지비를 만드는지를 판단한다.

실질 대안은 ① 기존 repository owner/template/view에 흡수, ② 승인된 프로젝트 전용 작은 실험, ③ 현행 유지·`NO_CHANGE`로 비교한다. setup/유지비·검색/문맥 전환·AI 연동·정본 충돌·다중 프로젝트·백업/이식성·비용·초보 사용성·플레이어 가치를 같은 기준으로 검토한다. `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY` 판정과 기존 5회 적대적 개선·회귀 재검사 절차를 따른다. 공용 DB 수·WIP 수·새 Skill을 먼저 고정하지 않는다.

### 12.4 Skill 자동 선택과 로컬 이식의 증거 경계

공식 `create-and-manage-skills` 본문 확인: `checked_at: 2026-08-31`. 적용 직전 현재 문서와 실제 연결 도구의 지원 범위를 다시 확인한다.

- `SKILL_AUTO_USE_REQUIRES_DATABASE_DESCRIPTION`: 현재 공식 설명상 자동 선택에는 **skills database 안의 description**이 필요하고 `Use automatically`는 기본 활성화다. standalone Skill 페이지까지 자동 실행된다고 확대하거나, task-scoped/on-demand를 수동 전용으로 단정하지 않는다.
- `NOTION_SKILL_EXPORT_IS_TRANSPORT_NOT_EQUIVALENCE`: `SKILL.md`와 공유 허용 첨부 파일의 export는 전달 기능이지 다른 agent에서 동작·권한·출력이 같다는 검증이 아니다. 가져온 지시·references·scripts·접근 권한·라이선스를 검토하고 대표 입력/경계 입력과 실제 도구 조합으로 비교한다. 조사 중 다운로드된 scripts를 자동 실행하지 않는다.
- Base의 repository `SKILL.md`와 기존 Skill owner를 정본으로 유지한다. Notion 사본을 자동 동기화하거나 Registry를 덮어쓰지 않는다. 기본 지침·작업 Skill·자율 실행기의 책임 분리만 검증 후 `ADAPT`한다.

### 12.5 최소 흡수와 정직한 scan receipt

Master DB + contextual view 사례는 **하나의 정본 owner → 목적별 파생 view/PDF/handoff**로 변형해 비교한다. GitHub Issue·PR·검증 상태를 Notion에 별도 active tracker로 복제하지 않는다. legacy export 교훈은 `templates/project-operations/NOTION_TO_REPOSITORY_MIGRATION_CHECKLIST.md`로 연결하고, Skill 원리는 `docs/AI_SKILL_ADOPTION_GUIDE.md` 및 기존 owner를 먼저 검토한다.

`last_successful_scan_at`은 실제로 읽은 source와 범위의 증거가 있을 때만 갱신한다. 한 원문 확인을 전체 채널·workspace·source family 전수 조사로 확대하지 않는다. PR/merge·테스트·예약 실행·project migration은 각자의 실제 증거로 보고하며, 동일 주제의 기존 진행 PR은 read-only로 두고 실제 경로·의미 충돌만 국소 보류한다.

## 13. Game market intelligence + verified success cases

시장조사는 인기순위 수집이 아니라 **비교 차원 → table-stakes → failure/mixed cases → 검증 가능한 성과 → transferable principle → project kick candidate**로 이어진다. 상세 판정 owner는 `skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md`다.

```yaml
seed_group: game-market-intelligence-verified-success
status: ACTIVE_DISCOVERY_SEED
domains:
  - GAME_DEVELOPMENT
recommended_cadence: weekly-or-before-market-positioning-decision
existing_consumers:
  benchmark_and_kick_method: skills/analyzing-and-refining-game-concepts/references/benchmark-player-evidence-and-playtests.md
source_roles:
  first_party_product_fact:
    - Steam / Steamworks official store and community announcements
    - Google Play public store pages
    - developer / publisher official milestone statements
  professional_market_intelligence:
    - SteamDB
    - GameDiscoverCo
    - Sensor Tower Game IQ
    - Video Game Insights / VGI
urls:
  steam_store: https://store.steampowered.com/
  steamworks: https://partner.steamgames.com/doc/home
  google_play_games: https://play.google.com/store/games
  steamdb: https://steamdb.info/
  gamediscoverco: https://gamediscover.co/
  sensor_tower_game_iq: https://sensortower.com/product/mobile-app/game-iq
  vgi: https://app.sensortower.com/vgi/
scan_surfaces:
  - release, price, platform and store positioning
  - public install / download buckets when the official store exposes them
  - first-party paid sales milestones
  - review, follower, wishlist, CCU and player-context signals without metric laundering
  - estimated owners / units / downloads / revenue with methodology and confidence retained
  - direct competitors, adjacent mechanic references and failure / mixed cases
  - genre table-stakes and observable differentiation
  - one-sentence / screenshot / GIF / trailer legibility of kick candidates
  - production cost and project fit
```

10만+ 성공 사례는 다음 네 상태를 구분한다.

```text
VERIFIED_100K_DOWNLOAD_INSTALL
VERIFIED_100K_SALES
ESTIMATED_100K_PLUS
NOT_100K_VERIFIED
```

현재 seed examples는 `checked_at: 2026-08-12` 기준으로 다음과 같이 사용할 수 있다.

```text
Shattered Pixel Dungeon — Google Play 5M+ downloads — VERIFIED_100K_DOWNLOAD_INSTALL
Mindustry — Google Play 5M+ downloads — VERIFIED_100K_DOWNLOAD_INSTALL
Slice & Dice — Google Play 1M+ downloads — VERIFIED_100K_DOWNLOAD_INSTALL
Sledding Game — developer Steam announcement, 100,000 copies in 5 days — VERIFIED_100K_SALES
God Of Weapons — developer Steam announcement, over 100,000 copies in 2 weeks — VERIFIED_100K_SALES
Astrea: Six-Sided Oracles — developer Steam announcement, over 100,000 copies within 4 months — VERIFIED_100K_SALES
```

이 사례들은 **threshold evidence**일 뿐 성공 원인의 causal proof가 아니다. success case만 보고 결론내지 않고 기존 benchmark owner의 direct competitors + adjacent mechanics + failure/mixed case 구성을 유지한다.

공통 claim ceiling:

```text
100K downloads != 100K paid sales
estimated owners / units != verified sales
revenue / gross != unit sales
wishlists / reviews / followers / CCU != downloads or sales
success milestone != causal proof of a mechanic
popularity != design-quality authority
competitor UI / art popularity != permission to copy identifiable execution
```

시장자료와 성공사례는 `PLAYER_NOTICEABLE / LOOP_RELEVANT / MARKET_LEGIBLE / PRODUCTION_FIT / NON_DERIVATIVE` 중 실제 근거가 있는 축으로 project kick candidate를 만들고, 최종 채택은 `ADOPT / ADAPT / AVOID / TEST / IGNORE`와 프로젝트 PoC/플레이어 evidence로 결정한다.
