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

## 6. Seed scan 결과

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
