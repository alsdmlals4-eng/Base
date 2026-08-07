# Game Build Size and Asset Optimization Design

Date: 2026-08-07
Status: DESIGN_APPROVED_BY_USER_PENDING_WRITTEN_SPEC_REVIEW
Base main baseline: `4f98f968a377f7b6a11aafa4fc94d11bddbebedc`
Target repository: `alsdmlals4-eng/Base`

## 1. Direction anchor

게임의 용량을 단순히 최소화하는 것이 아니라 **플레이어가 체감하는 시각·청각 품질과 핵심 플레이 경험을 보존하면서 전달·설치·런타임·업데이트에 낭비되는 byte를 제거한다.**

공통 아트·폰트·자산 정책과 품질 등급은 한 책임 원본으로 통일하되, 실제 압축 포맷·해상도·패키징·다운로드 방식은 Windows PC와 Android의 하드웨어·스토어·패치 특성에 맞게 분리한다.

## 2. Problem

현재 Base에는 다음 기반이 이미 존재한다.

- `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
  - `quality_profile`
  - `package_and_download_size`
  - Windows/Android 실제 기기 성능 검증
- `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
  - CPU/GPU/memory/loading/thermal/package 예산
- `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
  - Asset Specification의 dimensions/export/import/performance/validation 계약
- `reviewing-and-validating-project-changes`
  - 성능·회귀 증거 책임
- `running-adversarial-review-and-refinement`
  - 설계 공격·비판 검증·회귀 재공격 책임

그러나 현재 구조만으로는 다음 질문을 일관되게 답하기 어렵다.

1. 실제 배포 용량에서 무엇이 가장 큰 비중을 차지하는가?
2. 폰트·텍스처·오디오·비디오·mesh·animation·SDK 중 무엇부터 최적화해야 하는가?
3. 같은 원본 자산을 PC와 Android에서 어떤 방식으로 다르게 import/export해야 하는가?
4. 초기 다운로드를 줄인 것이 첫 실행 추가 다운로드 증가로 전가되지 않았는가?
5. 설치 용량을 줄인 것이 런타임 메모리·CPU·GPU·발열 문제를 만들지 않았는가?
6. Steam의 작은 콘텐츠 수정이 거대한 patch download로 확대되지 않는가?
7. 최적화 전후 품질 저하가 실제 플레이 화면에서 허용 가능한가?

따라서 `package_and_download_size`라는 단일 필드를 더 구체적인 **Build Size & Asset Optimization Contract**로 확장할 필요가 있다.

## 3. Existing Solution First decision

### Option A — dedicated Guide + existing Profile/owners extension — RECOMMENDED

새 광역 Skill은 만들지 않는다.

- 전문 지식 Guide 추가
- 기존 PC/Android Delivery Profile에 프로젝트별 측정 필드 추가
- 기존 Art/Asset Guide에 자산 사양 연결
- 기존 validation/adversarial Skill이 검증
- 기존 Registry trigger에 필요한 경우 size/asset optimization 관련 trigger만 추가

장점:

- 현재 Base의 단일 책임·최소 Skill 원칙을 유지한다.
- PC-only, Android-only, 향후 iOS/console에도 지식 Guide를 재사용할 수 있다.
- 실행 책임을 새 Skill에 중복시키지 않는다.

### Option B — PC_ANDROID Guide에 모든 내용을 직접 추가 — REJECTED

장점은 변경 파일 수가 적다는 점이다. 그러나 font/audio/patching/asset audit 같은 공용 지식이 Windows+Android 문서에 종속되어 문서가 비대해지고 재사용성이 낮아진다.

### Option C — 독립 Optimization Skill 생성 — REJECTED

호출은 직관적이지만 `analyzing-and-refining-game-concepts`, art/asset, vertical slice, validation과 책임이 겹친다. Base의 Existing Solution First 및 “새 광역 Skill보다 기존 책임 흡수 우선” 원칙에 맞지 않는다.

## 4. Proposed authority structure

### New knowledge Guide

`docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`

책임:

- 용량 측정 모델
- 자산 분류와 최적화 순서
- 플랫폼별 asset quality/import/export 정책
- font/texture/audio/video/mesh/animation/package optimization
- download/install/runtime/patch trade-off
- 품질 회귀 Gate
- 측정·증거·rollback 원칙

비책임:

- 프로젝트별 실제 목표 MB 수치
- 프로젝트별 특정 texture max size
- 프로젝트별 실제 font family 선정
- 실제 Godot 파일 변경
- 실제 Steam/Google Play 배포 승인
- Art Direction 자체

### Existing owners

`PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- 새 Guide를 `quality_profile`, performance budget, release validation에서 선택적으로 참조한다.

`PC_ANDROID_DELIVERY_PROFILE.md`
- 프로젝트별 size budget과 실측 결과를 기록한다.

`ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- Asset Specification이 `size_quality_class`, `platform_import_profile`, `quality_validation`을 가질 수 있게 연결한다.

`REFERENCE_SOURCE_CATALOG.md`
- Godot/Android/Steam의 공식 자료를 T1 근거로 등록한다.

`START_HERE.md` / `DOCUMENTATION_MAP.md`
- “게임 용량·다운로드·자산 최적화” 요청에서 새 Guide를 발견 가능하게 한다.

`skills/SKILL_REGISTRY.json`
- 새 Skill 추가 없이 기존 owner의 trigger가 실제 요청을 놓칠 때만 최소 trigger를 추가한다.

## 5. Measurement model

용량은 한 숫자로 관리하지 않는다.

### Windows

```yaml
windows_size_budget:
  download_compressed_bytes:
  installed_bytes:
  first_launch_additional_download_bytes:
  typical_patch_download_bytes:
  worst_expected_patch_download_bytes:
  patch_temporary_disk_bytes:
  runtime_peak_memory_bytes:
```

### Android

```yaml
android_size_budget:
  play_served_download_bytes:
  installed_bytes_before_first_launch:
  first_launch_additional_download_bytes:
  first_session_total_download_bytes:
  typical_player_content_bytes:
  full_optional_content_bytes:
  runtime_peak_memory_bytes:
```

### Common asset breakdown

```yaml
asset_size_breakdown:
  executable_and_engine:
  font:
  ui_texture:
  world_texture:
  sprite_and_2d_art:
  mesh:
  animation:
  audio_sfx:
  audio_music:
  audio_voice:
  video:
  shader_and_generated_data:
  localization:
  platform_sdk:
  optional_content:
  duplicate_or_unused:
  other:
```

각 값은 추정치와 실측치를 구분한다.

```yaml
measurement:
  source_build:
  platform:
  device_or_store_configuration:
  measured_at:
  tool:
  measured_value:
  state: ESTIMATE | LOCAL_BUILD_MEASURED | DEVICE_MEASURED | STORE_SERVED_MEASURED
```

## 6. Optimization order

고정 압축률을 먼저 정하지 않는다.

```text
production release build baseline
→ delivered/install/runtime size split
→ asset-category breakdown
→ Top-N largest contributors
→ duplicate/unused/oversized detection
→ quality-value classification
→ cheapest reversible optimizations first
→ platform-specific import/export
→ rebuild
→ byte delta
→ quality/performance regression check
→ accept/reject/rollback
```

Top-N 대상은 절대 개수보다 “전체 크기에 의미 있는 비중을 차지하는가”로 선택한다. 모든 작은 파일을 미세 최적화하는 작업은 YAGNI로 본다.

## 7. Quality classes

프로젝트가 모든 자산에 동일한 해상도·압축을 강제하지 않도록 공통 등급을 정의한다.

```yaml
quality_class:
  HERO:
    meaning: 플레이어가 크게·가깝게·오래 보는 대표 자산
    optimization_bias: quality_first
  GAMEPLAY_CRITICAL:
    meaning: 판정·식별·가독성에 직접 영향
    optimization_bias: readability_first
  STANDARD:
    meaning: 일반 반복 플레이 자산
    optimization_bias: balanced
  BACKGROUND:
    meaning: 작게·멀리·짧게 보이는 보조 자산
    optimization_bias: size_first_with_visual_gate
  OPTIONAL:
    meaning: 핵심 첫 플레이에 필요하지 않은 콘텐츠
    optimization_bias: delivery_separation_candidate
```

이 등급은 프로젝트별 실제 pixel size, viewing distance, screen percentage, reuse count와 함께 판단한다.

## 8. Font policy

### Principle

**font family와 역할은 통일하되 font file을 size마다 복제하지 않는다.**

Godot 4에서는 font size가 font resource 자체가 아니라 사용하는 Control/Theme에 정의되므로, 16px/20px/28px을 위해 같은 TTF/OTF를 여러 번 복제하지 않는다.

권장 계약:

```yaml
font_profile:
  primary_family:
  fallback_families:
  required_languages:
  required_glyph_sets:
  required_weights:
  variable_font_candidate:
  duplicated_font_files:
  unused_weights:
  license_verified:
  runtime_fallback_tested:
```

규칙:

- 동일 family/weight 파일의 중복 저장 금지.
- 사용하지 않는 weight/style은 패키지에 포함하지 않는다.
- variable font가 실제로 여러 weight 파일을 대체하고 엔진/플랫폼/품질에 문제가 없을 때만 채택한다.
- CJK/emoji/다국어 지원 때문에 필요한 fallback을 “폰트 하나” 원칙으로 제거하지 않는다.
- system font 사용은 설치 용량을 줄일 수 있지만 플랫폼별 metrics·외형 차이를 만들 수 있으므로 브랜드 UI의 기본 해법으로 강제하지 않는다.
- glyph subsetting은 실제 언어·문자 범위가 확정되고 license/toolchain/누락 검증이 가능한 경우에만 사용한다.
- font 최적화는 glyph missing, tofu, line break, clipping, fallback metric regression을 검증해야 한다.

## 9. Texture and image policy

### Shared source, platform-specific delivery

원본 아트의 정본은 공유할 수 있지만 실제 GPU texture format과 max resolution은 플랫폼 profile로 분리한다.

Godot의 VRAM compression은 플랫폼별로 다른 포맷을 사용한다. 고품질 모드에서 desktop은 BPTC, mobile은 ASTC를 사용할 수 있고 기본 저품질 경로는 desktop S3TC, mobile/web ETC2를 사용할 수 있다. 따라서 “모바일/PC 동일 압축 포맷”은 공용 규칙이 아니다.

```yaml
texture_profile:
  source_resolution:
  actual_max_screen_coverage:
  quality_class:
  alpha_required:
  normal_or_data_texture:
  mipmap_policy:
  windows_import_profile:
    max_resolution:
    compression:
    high_quality:
  android_import_profile:
    max_resolution:
    compression:
    high_quality:
  visual_validation_scene:
```

### Resolution

- source resolution을 보존하는 것과 packaged resolution을 동일하게 유지하는 것을 구분한다.
- 실제 최대 화면 점유보다 과도하게 큰 텍스처는 우선 검사한다.
- 4K/2K/1K 같은 숫자를 모든 자산에 일괄 강제하지 않는다.
- UI, pixel art, line art, normal map, gradient처럼 compression artifact가 쉽게 보이는 자산은 별도 profile을 허용한다.

### Mipmaps

- 3D와 축소/zoom되는 2D에서는 품질·bandwidth 이점이 있을 수 있다.
- 고정 크기 UI처럼 축소되지 않는 2D 자산은 불필요한 mipmap이 메모리/용량을 늘릴 수 있다.
- mipmap 전체 삭제를 공용 최적화 규칙으로 두지 않는다.

### Android texture delivery

Android App Bundle/Play Asset Delivery의 Texture Compression Format Targeting을 사용할 수 있는 프로젝트는 기기별 최적 포맷 전달을 후보로 평가한다.

- ETC2: 넓은 현대 Android 호환 기본 후보
- ASTC: 지원 기기에서 품질/용량 trade-off를 세밀하게 조정 가능한 후보
- 실제 지원 기기 범위와 Godot export pipeline을 확인하지 않고 강제하지 않는다.

## 10. Audio policy

Godot의 WAV/Ogg Vorbis/MP3는 disk size와 CPU cost가 다르므로 “가장 작은 형식” 하나로 통일하지 않는다.

```yaml
audio_profile:
  role: SFX | MUSIC | VOICE | AMBIENCE
  duration:
  simultaneous_voice_risk:
  looped:
  quality_class:
  format:
  bitrate_or_quality:
  channels:
  sample_rate:
  size_bytes:
  cpu_profile:
  listening_test:
```

기본 후보:

- 매우 짧고 빈번한 SFX: WAV/light compression 후보. CPU 비용을 낮추는 가치가 크면 파일 증가를 허용한다.
- music/voice/long ambience: Ogg Vorbis 우선 후보.
- 모바일에서 다수 compressed stream 동시 재생이 CPU/발열 문제를 만들면 MP3 등 다른 trade-off를 비교한다.
- stereo 의미가 없는 효과음/voice는 mono 후보를 검토한다.
- sample rate와 bitrate는 실제 audible difference와 target device speaker/headphone에서 A/B 테스트 후 낮춘다.

## 11. Video, mesh and animation

### Video

- 시작 로고/튜토리얼 영상이 초기 다운로드에서 큰 비중이면 resolution/bitrate/framerate/audio track을 개별 검토한다.
- 게임 플레이에서 바로 필요하지 않은 대형 영상은 optional delivery 후보가 될 수 있다.
- 영상 제거가 UX/스토리 경험을 훼손하면 용량 절감을 우선하지 않는다.

### Mesh

- 화면 점유·silhouette·deformation에 기여하지 않는 subdivision/hidden geometry를 후보로 찾는다.
- mesh decimation은 silhouette, normal, UV, animation deformation 회귀를 검증한다.
- LOD는 단순 disk 절감 수단이 아니라 runtime performance와 함께 판단한다. LOD 추가가 오히려 package size를 늘릴 수 있음을 기록한다.

### Animation

- duplicate clips, unused tracks, excessive key density를 검사한다.
- compression/tolerance 변경은 hand/face/contact timing과 gameplay readability 회귀를 검증한다.

## 12. Duplicate and unused asset gate

압축 전에 “필요 없는 byte”부터 제거한다.

검사 후보:

- 동일 hash 파일
- 이름만 다른 duplicate asset
- 이전 버전/backup/export artifact
- 프로젝트에 import되지만 활성 Scene/Resource/데이터에서 소비되지 않는 자산
- 여러 폴더에 복제된 동일 font/audio/icon
- disabled feature의 stale asset
- debug/test-only asset의 release export 혼입

단, 문자열/동적 path/runtime load/모드/DLC/플랫폼 SDK처럼 정적 reference scan만으로 unused 판정하기 어려운 항목은 자동 삭제하지 않는다.

상태:

```text
USED_CONFIRMED
DUPLICATE_CONFIRMED
UNUSED_CONFIRMED
DYNAMIC_REFERENCE_UNVERIFIED
PLATFORM_REQUIRED
KEEP_FOR_ROLLBACK
```

## 13. Packaging and delivery

### Windows / Steam

SteamPipe는 파일을 chunk 단위로 비교하므로 설치 용량과 patch 크기를 별도로 본다.

공용 원칙:

- 거대한 monolithic pack을 기본 해법으로 강제하지 않는다.
- asset reorder가 pack 전체의 binary layout을 흔들지 않게 한다.
- 변경 빈도·level·feature 단위로 pack/depot 경계를 검토한다.
- 일반 압축이 asset boundary를 넘어 변화 범위를 확산시키지 않는지 검증한다.
- 패치 전후 실제 diff/Steam preview에서 update size를 측정한다.
- patch 적용 중 새 파일을 옆에 구성하는 경우 필요한 임시 disk headroom도 기록한다.

### Android / Google Play

초기 APK/AAB 크기만 줄이고 첫 실행에서 GB 단위 다운로드를 강요하는 것을 성공으로 판정하지 않는다.

콘텐츠는 필요성과 UX에 따라 분리한다.

```text
install-time
fast-follow
after-start / on-demand
```

다음은 optional delivery 후보이다.

- 후반 지역
- 고해상도 optional voice pack
- 선택 언어 voice
- 재플레이용 대형 영상
- 아직 접근 불가능한 콘텐츠

다음은 기본적으로 install-time을 우선 검토한다.

- 첫 실행 UI
- tutorial/core loop
- 첫 세션 필수 audio/visual feedback
- network failure에서도 첫 플레이를 성립시키는 필수 자산

## 14. Quality regression gate

용량 절감은 다음 중 하나가 실패하면 자동 성공이 아니다.

### Visual

- representative scene screenshot before/after
- worst-case zoom/distance
- UI text and icon readability
- compression artifacts/banding/halo
- transparent edge quality
- normal map/specular artifacts
- animation contact/silhouette

### Audio

- A/B listening
- loop seam
- voice intelligibility
- transient loss in gameplay SFX
- simultaneous playback CPU cost

### Runtime

- frame time
- loading time
- peak memory
- hitching
- thermal/battery on Android

### Delivery

- clean install
- update from previous public-like build
- first-launch additional download
- offline/poor-network fallback where applicable
- free disk requirement during update

## 15. Optimization decision record

각 변경은 다음 기록을 남긴다.

```yaml
optimization_change:
  asset_or_group:
  platform:
  baseline_bytes:
  optimized_bytes:
  byte_saving:
  percentage_saving:
  build_or_patch_effect:
  runtime_memory_effect:
  cpu_gpu_effect:
  visual_or_audio_effect:
  quality_evidence:
  performance_evidence:
  delivery_evidence:
  decision: ACCEPT | REJECT_QUALITY_LOSS | REJECT_RUNTIME_COST | DEFER | BLOCKED_UNVERIFIED
  rollback:
```

단일 변경에서 작은 byte 절감 때문에 명확한 품질·CPU·발열 회귀가 생기면 `REJECT_*`가 정상 결론이다.

## 16. Project profile extension

`templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`의 기존 `performance_budget.package_and_download_size`를 제거하지 않고 호환 필드로 유지하되, 세부 profile을 추가한다.

```yaml
build_size_and_asset_optimization:
  baseline_build:
  target_budget_status:
  windows_size_budget:
  android_size_budget:
  asset_size_breakdown:
  top_contributors:
  font_profile:
  texture_profiles:
  audio_profiles:
  delivery_partition:
  duplicate_unused_audit:
  accepted_optimizations:
  rejected_optimizations:
  visual_quality_evidence:
  audio_quality_evidence:
  runtime_evidence:
  patch_evidence:
  unresolved:
```

프로젝트별 MB 목표는 여기에서만 둔다. Base 공용 Guide에는 임의 숫자를 고정하지 않는다.

## 17. Routing design

### Primary discipline

이번 지식 체계 자체의 구현 주 책임은 기존 Base 문서/기획 계약에 둔다. 실제 프로젝트 적용은 요청에 따라 현재 owner가 달라진다.

- 초기 플랫폼/제약/production gate: `analyzing-and-refining-game-concepts`
- 실제 자산 제작 specification: 기존 art/asset 책임
- Vertical Slice 품질·성능 증명: `designing-vertical-slices`
- 실제 변경의 size/performance/quality 회귀: `reviewing-and-validating-project-changes`
- 실패 가정/반례/결정 재검토: `running-adversarial-review-and-refinement`

### Trigger examples

- game build size
- package size
- download size
- install size
- asset optimization
- texture size
- texture compression
- font size optimization
- audio size optimization
- mobile package optimization
- Steam patch size
- Play Asset Delivery

Registry에는 동일 책임을 가진 새 Skill을 등록하지 않는다.

## 18. Validation and tests

Base 구현 시 최소 검증:

1. `tools/run_local_validation.py`
2. Skill Registry JSON/schema 검사
3. documentation map/reference freshness 검사
4. generated active skill view가 Registry와 일치하는지 확인
5. 새 Guide가 START_HERE에서 한 단계로 발견 가능한지 확인
6. PC_ANDROID Guide와 Profile이 새 Guide를 소비하는지 확인
7. Art Guide의 Asset Specification과 새 Guide가 충돌하지 않는지 확인
8. legacy ID 또는 새 광역 Skill이 실수로 만들어지지 않았는지 확인
9. 실제 프로젝트 값처럼 보이는 고정 MB/해상도/bitrate가 Base 공용 규칙에 유입되지 않았는지 검사
10. external source URL과 checked-at/version을 Reference Source Catalog에서 확인

실제 Godot build, Android device, Steam upload를 이 Base 문서 변경의 테스트 통과로 주장하지 않는다. 해당 증거는 프로젝트 적용 시 생산한다.

## 19. Adversarial pre-review

### Finding A — `폰트 하나로 통일`은 과잉 일반화

위험:
- CJK/emoji fallback 누락
- 브랜드 font의 부족한 glyph coverage
- variable font가 오히려 필요 없는 glyph/axis를 포함할 가능성

판정: `MUST_FIX_IN_DESIGN`

해결:
- family/role 최소화를 목표로 하되 fallback과 glyph coverage를 품질 Gate로 둔다.

### Finding B — `모바일/PC 동일 texture compression`은 잘못된 통일

위험:
- GPU 지원 차이
- mobile memory/bandwidth 악화
- desktop quality 손실

판정: `MUST_FIX_IN_DESIGN`

해결:
- shared source + platform import profile 구조.

### Finding C — `해상도 일괄 하향`은 품질 회귀를 숨긴다

위험:
- UI/text/line art의 선명도 손실
- hero asset의 판매/브랜드 품질 손실

판정: `MUST_FIX_IN_DESIGN`

해결:
- actual screen coverage + quality class + A/B validation.

### Finding D — `최종 설치 크기` 하나만 최적화하면 delivery UX를 왜곡한다

위험:
- 첫 실행 추가 다운로드 증가
- patch 폭증
- 업데이트 임시 disk 부족

판정: `MUST_FIX_IN_DESIGN`

해결:
- download/install/runtime/patch를 별도 예산으로 관리.

### Finding E — `최대 압축`은 runtime cost를 무시한다

위험:
- 오디오 decode CPU
- loading hitch
- mobile thermal/battery

판정: `MUST_FIX_IN_DESIGN`

해결:
- byte saving과 CPU/GPU/memory/loading/thermal을 함께 기록.

### Finding F — asset splitting 자체가 목적이 될 수 있다

위험:
- 다운로드 UX 복잡화
- network failure 처리 증가
- CDN/스토어 pipeline 유지 비용

판정: `SHOULD_FIX_IN_DESIGN`

해결:
- core first-session asset은 기본 포함, optional partition은 명확한 플레이 단계 경계가 있을 때만 허용.

## 20. External evidence basis

공식 T1 근거를 구현 시 `REFERENCE_SOURCE_CATALOG.md`에 등록한다.

### Godot

- Importing images / texture compression and mipmaps
  - https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
  - 핵심 적용: platform-specific VRAM formats, high-quality BPTC/ASTC paths, mipmap trade-off.
- Importing audio samples
  - https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
  - 핵심 적용: WAV/Ogg Vorbis/MP3의 disk-size vs CPU trade-off.
- Using Fonts
  - https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_fonts.html
  - 핵심 적용: Godot 4 font size와 font resource 분리, variable font/fallback 특성.

### Android / Google Play

- Reduce game size
  - https://developer.android.com/games/optimize/game-size
  - 핵심 적용: production baseline → size structure → large assets → texture optimization 순서, App Bundle/PAD.
- Target texture compression formats in Android App Bundles
  - https://developer.android.com/guide/playcore/asset-delivery/texture-compression
  - 핵심 적용: device-targeted TCF, ETC2 default candidate, ASTC quality/size trade-off.
- Play Asset Delivery
  - https://developer.android.com/guide/playcore/asset-delivery
  - 핵심 적용: install-time / fast-follow / on-demand 전달 경계.

### Steam

- Uploading to Steam / SteamPipe Content System
  - https://partner.steamgames.com/doc/sdk/uploading
  - 핵심 적용: ~1 MB chunk delta, pack ordering/locality, pack size, per-asset compression, update temporary disk behavior.

### Cross-engine benchmark

이 문서는 Godot 중심이지만 원리가 엔진 특이 현상인지 확인하기 위해 다음 공통 패턴을 참고한다.

- Unity GPU Texture Formats
  - https://docs.unity3d.com/6000.0/Documentation/Manual/texture-formats-reference.html
- Unity Addressables content updates
  - https://docs.unity3d.com/Packages/com.unity.addressables@1.21/manual/content-update-builds-overview.html
- Unreal Engine asset chunking / patching
  - https://dev.epicgames.com/documentation/en-us/unreal-engine/preparing-assets-for-chunking-in-unreal-engine

공통적으로 확인되는 원리는 `platform texture profile`, `content grouping`, `incremental update`, `optional/remote delivery`, `actual build measurement`이며, 엔진별 구체 API를 Base 공용 강제 규칙으로 만들지 않는다.

## 21. Implementation scope after written-spec review

사용자가 이 written spec을 승인하면 다음 구현 계획으로 전환한다.

Expected files:

- ADD `docs/knowledge/game-development/GAME_BUILD_SIZE_AND_ASSET_OPTIMIZATION_GUIDE.md`
- UPDATE `docs/knowledge/game-development/PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`
- UPDATE `docs/knowledge/game-development/ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`
- UPDATE `docs/knowledge/game-development/REFERENCE_SOURCE_CATALOG.md`
- UPDATE `docs/knowledge/game-development/README.md`
- UPDATE `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md`
- UPDATE `START_HERE.md`
- UPDATE `docs/DOCUMENTATION_MAP.md`
- UPDATE `skills/SKILL_REGISTRY.json` only if trigger coverage audit proves a gap
- UPDATE generated/coverage/tests only where current Base generators/contracts require it

Out of scope:

- project-specific MB targets
- actual game asset recompression
- actual Godot `.import` changes
- real Steam/Google Play publish
- new broad Skill
- new addon/MCP/tool unless a later evidence-backed Existing Solution First Gate independently justifies it

## 22. Success criteria

설계 구현은 다음을 만족할 때 성공이다.

1. 게임 용량 최적화 요청이 Base cold start에서 한 단계로 발견된다.
2. 새 광역 Skill 없이 기존 책임 경계가 유지된다.
3. font/texture/audio/package 각각에 size-quality-performance trade-off가 명시된다.
4. Windows와 Android의 전달·압축 차이가 공통 정본 안에서 분리된다.
5. download/install/runtime/patch를 별도 측정한다.
6. 프로젝트별 숫자는 Template에만 기록하고 Base는 측정 방법을 소유한다.
7. 품질 저하를 byte 절감 성공으로 오판하지 않는 회귀 Gate가 있다.
8. Steam update locality와 Android asset delivery가 포함된다.
9. 공식 근거와 checked-at가 기록된다.
10. Base 정적/Registry/reference-freshness 검증을 통과한다.

## 23. Rollback

구현 중 책임 중복이나 문서 비대화가 확인되면:

1. 새 Guide 추가를 되돌린다.
2. 기존 `PC_ANDROID_CROSS_PLATFORM_DELIVERY_GUIDE.md`와 `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 원상태를 보존한다.
3. 프로젝트별 실측용 Profile 확장은 독립 가치가 있는지 다시 판단한다.
4. 새 Skill은 만들지 않는다.

설계 자체는 Git 이력으로 보존하며 활성 Base 계약과 구현을 구분한다.
