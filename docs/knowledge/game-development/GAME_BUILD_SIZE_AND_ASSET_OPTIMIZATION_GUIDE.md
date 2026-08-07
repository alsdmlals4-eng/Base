# 게임 빌드 용량·자산 최적화 Guide

```yaml
guide_role: reusable-game-build-size-and-asset-optimization-method
checked_at: 2026-08-07
primary_scope: Windows PC + Android mobile
engine_focus: Godot 4.x
```

## 1. 목적과 비목표

이 Guide의 목적은 게임 파일을 무조건 가장 작게 만드는 것이 아니다.

> **플레이어가 체감하는 시각·청각 품질과 핵심 플레이 경험을 보존하면서 다운로드·설치·런타임·업데이트에 낭비되는 byte를 제거한다.**

공통 아트·폰트·자산 정책과 품질 등급은 하나의 책임 원본으로 유지하되, 실제 압축 포맷·해상도·패키징·다운로드 방식은 Windows PC와 Android의 하드웨어·스토어·패치 특성에 맞게 분리할 수 있다.

이 Guide는 다음을 책임진다.

- 다운로드·설치·런타임·패치 용량의 분리 측정
- 폰트·텍스처·오디오·비디오·mesh·animation·SDK·중복 자산의 크기 기여도 분석
- 품질 중요도에 따른 최적화 순서
- Windows/Android 플랫폼별 import/export/delivery 차이
- Steam patch locality와 Google Play asset delivery의 선택적 적용
- 최적화 전후 품질·성능·전달 회귀 Gate
- 실측 근거와 rollback 기록

이 Guide가 책임지지 않는 것:

- 프로젝트별 고정 MB 목표
- 모든 게임에 공통인 texture max size
- 모든 게임에 공통인 bitrate·sample rate
- 프로젝트별 실제 font family 선정
- 실제 Godot `.import` 변경
- 실제 Steam/Google Play 배포 승인
- Art Direction 자체

프로젝트별 목표·실측·증거는 `templates/planning/PC_ANDROID_DELIVERY_PROFILE.md` 또는 프로젝트가 선언한 동등 책임 원본에 기록한다.

## 2. 핵심 원칙

### 2.1 한 숫자로 최적화하지 않는다

`게임 용량`은 최소 다음 네 종류를 분리한다.

```text
DOWNLOAD
INSTALLED
RUNTIME
PATCH
```

초기 다운로드만 작게 만들고 첫 실행 추가 다운로드를 크게 만드는 것, 설치 크기만 줄이고 런타임 메모리·CPU·발열을 악화시키는 것, 설치 크기는 작지만 작은 수정마다 거대한 업데이트가 발생하는 것은 성공이 아니다.

### 2.2 원본 정책은 공유하고 전달 프로필은 플랫폼별로 분리한다

```text
shared source intent
→ shared quality class
→ shared readability/identity rule
→ Windows import/delivery profile
→ Android import/delivery profile
→ platform evidence
```

PC와 모바일에 같은 texture compression, 같은 packaged resolution, 같은 delivery partition을 강제하지 않는다.

### 2.3 압축 전에 불필요한 byte부터 제거한다

다음 순서를 기본으로 한다.

```text
unused / duplicate / stale
→ oversized source delivery
→ unnecessary language/weight/channel/track
→ platform-inappropriate format
→ compression tuning
→ optional delivery
```

필요 없는 자산을 더 강하게 압축하는 것보다 패키지에서 제거하는 것이 우선이다.

### 2.4 byte 절감은 품질·성능 회귀를 이기지 못한다

작은 용량 절감 때문에 다음이 명확히 악화되면 해당 최적화는 거절할 수 있다.

- UI·텍스트 가독성
- 캐릭터·아이콘·실루엣 식별
- compression artifact·banding·halo
- 음성 명료도·효과음 transient·loop seam
- 로딩 hitch
- peak memory
- CPU/GPU frame time
- Android 발열·배터리
- Steam patch size·update disk requirement

## 3. 측정 모델

### 3.1 Windows

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

`installed_bytes`와 `patch_temporary_disk_bytes`를 혼동하지 않는다. 업데이트 시스템이 새 파일을 기존 파일 옆에 구성하는 경우 사용자는 설치 크기보다 훨씬 많은 임시 여유 공간을 필요로 할 수 있다.

### 3.2 Android

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

Google Play에서 전달되는 실제 크기와 로컬 AAB/APK 파일 크기를 같은 값으로 취급하지 않는다.

### 3.3 공통 자산 분해

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

측정값은 상태를 가진다.

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

`ESTIMATE`를 실제 배포 측정으로 승격하지 않는다.

## 4. 최적화 순서

```text
production-like release build baseline
→ delivered / installed / runtime / patch split
→ asset-category breakdown
→ Top-N largest contributors
→ duplicate / unused / oversized detection
→ quality-value classification
→ cheapest reversible optimizations first
→ platform-specific import/export/delivery
→ rebuild
→ byte delta
→ quality/performance/delivery regression check
→ ACCEPT / REJECT / DEFER / ROLLBACK
```

Top-N은 고정 개수를 의미하지 않는다. 전체 빌드에 의미 있는 비중을 차지하는 항목부터 처리한다. 수천 개의 작은 파일을 미세하게 줄이느라 가장 큰 영상·음원·텍스처·중복 자산을 놓치지 않는다.

## 5. 품질 등급

모든 자산에 동일한 해상도와 압축률을 적용하지 않는다.

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

등급 판단에는 실제 화면 점유율, viewing distance, zoom, 반복 노출, 정보 역할, 세일즈/브랜드 역할을 함께 본다.

## 6. 폰트 정책

### 6.1 통일의 의미

**폰트 family와 역할은 가능한 한 통일하되, 파일 하나만 강제하지 않는다.**

Godot 4의 UI에서는 font resource와 표시 size를 분리할 수 있으므로 16px·20px·28px 같은 크기별로 동일 TTF/OTF를 여러 번 복제할 필요가 없다.

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

- 동일 family/weight 파일의 중복 저장을 제거한다.
- 실제 사용하지 않는 weight/style은 패키지 포함 여부를 검토한다.
- 크기별 동일 font file 복제를 금지한다.
- variable font는 여러 weight 파일을 실제로 대체하고 엔진·플랫폼·품질 문제가 없을 때 후보로 사용한다.
- CJK·emoji·다국어 fallback을 `폰트 하나`라는 이유로 제거하지 않는다.
- system font는 설치 크기 절감 가능성이 있지만 OS별 외형·metrics 차이가 있으므로 브랜드 UI의 기본 해법으로 강제하지 않는다.
- glyph subsetting은 실제 지원 언어·문자 범위, 라이선스, 생성 도구와 누락 검증이 가능한 경우에만 사용한다.

필수 검증:

- 한글·영문·숫자·구두점·기호
- 지원 언어 전체
- missing glyph / tofu
- fallback 전환
- line break·line height·baseline
- 버튼·표·tooltip clipping
- 굵기·가독성

## 7. 텍스처·이미지 정책

### 7.1 Shared source, platform-specific delivery

원본 아트의 정본은 공유할 수 있지만 실제 GPU texture format과 packaged max resolution은 플랫폼 profile로 분리한다.

Godot의 VRAM compression은 플랫폼과 렌더러에 따라 다른 포맷을 사용한다. 고품질 경로에서 desktop은 BPTC, mobile은 ASTC를 사용할 수 있고, 기본 경로에서는 desktop S3TC와 mobile/web ETC2가 사용될 수 있다. 따라서 동일 압축 포맷을 PC와 모바일에 강제하지 않는다.

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

### 7.2 해상도

- source resolution 보존과 packaged resolution 보존을 구분한다.
- 실제 최대 화면 점유보다 과도하게 큰 texture를 우선 조사한다.
- `4K/2K/1K` 또는 `1024` 같은 값을 모든 자산에 일괄 적용하지 않는다.
- UI, pixel art, line art, normal/data map, gradient, transparent edge처럼 artifact가 눈에 띄기 쉬운 자산은 별도 profile을 허용한다.
- 동일 자산의 고해상도 variant가 실제로 사용되는지 확인한다.

### 7.3 Mipmap

- 3D와 축소·zoom되는 2D에서는 품질·cache/bandwidth에 이점이 있을 수 있다.
- 고정 크기 UI처럼 축소되지 않는 2D 자산은 불필요한 mipmap이 용량·메모리를 늘릴 수 있다.
- mipmap 전체 삭제를 공용 최적화 규칙으로 두지 않는다.

### 7.4 2D·pixel art 보호

Godot 공식 문서는 낮은 해상도의 pixel art texture에서 VRAM compression이 외형을 해칠 수 있음을 경고한다. 작은 2D/UI texture를 무조건 VRAM compressed로 전환하지 않는다.

### 7.5 Android texture delivery

Android App Bundle의 Texture Compression Format Targeting을 사용할 수 있는 프로젝트는 기기별 최적 texture set 전달을 후보로 평가한다.

- ETC2: 폭넓은 현대 Android 호환 후보
- ASTC: 지원 기기에서 품질/용량 trade-off를 더 세밀하게 조정할 수 있는 후보

실제 지원 기기 범위와 Godot Android export pipeline을 확인하지 않고 강제하지 않는다.

## 8. 오디오 정책

Godot의 WAV·Ogg Vorbis·MP3는 disk size와 CPU cost가 다르므로 하나의 포맷을 모든 오디오에 강제하지 않는다.

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

기본 판단:

- 짧고 매우 빈번한 SFX는 WAV 또는 가벼운 압축 후보가 될 수 있다. 파일 증가보다 낮은 decode 비용이 더 중요한 상황이 있다.
- music·voice·긴 ambience는 Ogg Vorbis 우선 후보가 될 수 있다.
- Ogg Vorbis는 같은 수준의 일반적인 손실 압축에서 파일 크기 이점이 크지만 WAV보다 decode CPU 비용이 높다.
- MP3는 Ogg Vorbis보다 같은 품질에서 더 클 수 있지만 decode 비용이 낮아 모바일/웹에서 다수 압축 stream 동시 재생 시 후보가 될 수 있다.
- stereo 의미가 없는 voice/SFX는 mono 후보를 검토한다.
- 과도한 sample rate·bitrate를 실제 target speaker/headphone A/B 테스트 후 낮춘다.
- 앞뒤 무음, 불필요한 baked reverb, 중복 channel/track을 검사한다.

품질 검증:

- A/B listening
- voice intelligibility
- transient loss
- loop seam
- spatial/phase 역할
- 동시 재생 CPU
- Android 장시간 발열

## 9. 비디오·Mesh·Animation

### 9.1 Video

- 시작 로고·튜토리얼·스토리 영상이 초기 다운로드에서 큰 비중이면 resolution·bitrate·framerate·audio track을 개별 검토한다.
- 첫 플레이에 필요하지 않은 대형 영상은 optional delivery 후보가 될 수 있다.
- 영상 제거가 서사·온보딩·브랜드 품질을 훼손하면 용량 절감을 우선하지 않는다.

### 9.2 Mesh

- 화면 점유·silhouette·deformation에 기여하지 않는 subdivision·hidden geometry를 후보로 찾는다.
- decimation은 silhouette, normal, UV, animation deformation 회귀를 검증한다.
- LOD는 runtime 성능을 위한 구조이며 disk 절감과 동일하지 않다. 추가 LOD가 package size를 증가시킬 수 있다.

### 9.3 Animation

- duplicate clips
- unused tracks
- excessive key density
- 동일 motion의 중복 export

compression/tolerance 변경 뒤 hand/face/contact timing과 gameplay readability를 검증한다.

## 10. 중복·미사용 자산 Gate

압축 전에 다음을 검사한다.

- 동일 hash 파일
- 이름만 다른 duplicate asset
- 이전 버전·backup·export artifact
- 실제 Scene/Resource/데이터에서 소비되지 않는 자산
- 여러 폴더에 복제된 font/audio/icon
- disabled feature의 stale asset
- debug/test-only asset의 release export 혼입

상태:

```text
USED_CONFIRMED
DUPLICATE_CONFIRMED
UNUSED_CONFIRMED
DYNAMIC_REFERENCE_UNVERIFIED
PLATFORM_REQUIRED
KEEP_FOR_ROLLBACK
```

문자열 path, 동적 load, mod/DLC, 플랫폼 SDK처럼 정적 reference scan만으로 판단하기 어려운 항목은 자동 삭제하지 않는다.

## 11. Windows·Steam 패키징과 패치 지역성

SteamPipe는 파일을 대략 1 MB chunk로 나누고 이전 빌드와 일치하는 chunk를 재사용한다. 작은 asset 변경이 pack 전체의 binary layout을 흔들면 실제 수정량보다 훨씬 큰 업데이트가 발생할 수 있다.

따라서 설치 크기와 patch 크기를 별도 예산으로 관리한다.

권장 원칙:

- 거대한 monolithic pack을 기본 해법으로 강제하지 않는다.
- asset 변경이 pack 내부에서 가능한 한 지역화되게 한다.
- asset ordering이 작은 수정마다 대규모로 재배열되지 않게 한다.
- level·realm·feature·변경 빈도에 따라 pack/depot 경계를 검토한다.
- 새로운 대형 콘텐츠는 기존 거대 pack을 재작성하는 대신 새 pack 후보를 검토한다.
- 일반 압축이 asset boundary를 넘어 변화 범위를 확산시키지 않는지 확인한다.
- Steam의 build preview 또는 실제 배포 전 size preview로 update 크기를 확인한다.
- update 과정에서 새 pack을 기존 pack 옆에 구성할 수 있으므로 temporary disk headroom을 기록한다.

Steam 문서의 예시 숫자를 모든 엔진·프로젝트의 고정 pack-size 목표로 승격하지 않는다. 핵심은 locality와 실측 patch 결과다.

## 12. Android·Google Play 전달 분할

Google은 게임 크기를 줄일 때 optimized delivery, 실제 baseline·구조 파악, 큰 자산 탐색, texture 최적화 순으로 접근하도록 안내한다. Android App Bundle은 기기 구성에 맞는 APK를 전달하고 Play Asset Delivery는 대형 asset을 분리할 수 있다.

PAD 전달 유형:

```text
install-time
fast-follow
on-demand
```

초기 AAB만 줄이고 첫 실행에서 대규모 다운로드를 강요하면 성공으로 판정하지 않는다.

### install-time 우선 후보

- 첫 실행 UI
- tutorial/core loop
- 첫 세션 필수 feedback
- 첫 플레이 필수 font/localization
- network failure에서도 최소 플레이를 성립시키는 필수 자산

### optional delivery 후보

- 후반 지역
- 선택 언어 voice pack
- 고해상도 optional pack
- 재플레이용 대형 영상
- 아직 접근 불가능한 콘텐츠

optional 분할은 다음 비용도 함께 본다.

- 다운로드 UX
- 실패·재시도 처리
- 저장 공간 예측
- CDN/스토어 pipeline 유지
- 버전 호환성
- 오프라인 플레이

명확한 플레이 단계 경계가 없는 콘텐츠를 억지로 분할하지 않는다.

## 13. 품질·성능·전달 회귀 Gate

### 13.1 Visual

- representative scene screenshot before/after
- worst-case zoom/distance
- UI text/icon readability
- compression artifact·banding·halo
- transparent edge
- normal/specular artifact
- animation contact/silhouette

### 13.2 Audio

- A/B listening
- loop seam
- voice intelligibility
- gameplay SFX transient
- simultaneous playback CPU

### 13.3 Runtime

- frame time
- loading time
- peak memory
- hitching
- Android thermal/battery

### 13.4 Delivery

- clean install
- update from previous public-like build
- first-launch additional download
- first-session total download
- poor-network/offline fallback where applicable
- patch temporary disk

실행하지 않은 증거는 통과로 표시하지 않는다.

## 14. 최적화 변경 기록

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

작은 byte 절감 때문에 명확한 품질·CPU·발열·패치 회귀가 생기면 `REJECT_*`가 정상 결론이다.

## 15. 프로젝트 적용 계약

프로젝트별 실제 값은 다음 형태로 기록한다.

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

Base가 임의로 목표 MB·texture resolution·bitrate를 채우지 않는다. 초기 목표는 프로젝트 장르·콘텐츠량·스토어·대표 기기·실제 baseline을 보고 정한다.

## 16. 적용 단계

```text
PLAN
→ target platforms / player context / store delivery 확인
→ production-like baseline 측정 계획
→ quality classes와 보호 대상 결정

BUILD
→ 가장 큰 기여자부터 가역적인 변경
→ platform import/delivery profile 적용
→ 변경별 byte delta 기록

REVIEW
→ visual/audio/runtime/delivery 회귀
→ patch/update 경로
→ 적대적 재검토
→ ACCEPT / REJECT / DEFER / BLOCKED_UNVERIFIED
```

Vertical Slice 단계에서는 대표 장면과 최악 장면에서 품질·메모리·로딩을 함께 본다. 출시 단계에서는 실제 store-served size와 update path를 별도로 확인한다.

## 17. 금지되는 과잉 일반화

다음을 Base 공용 규칙으로 만들지 않는다.

- `폰트는 무조건 하나`
- `모든 텍스처는 동일 해상도`
- `모바일과 PC는 동일 texture compression`
- `mipmap은 전부 제거`
- `오디오는 가장 작은 포맷 하나로 통일`
- `압축률은 무조건 최대로`
- `한 개의 거대한 pack이 항상 최적`
- `초기 다운로드가 작으면 전체 전달도 최적`
- `설치 용량이 작으면 업데이트도 작음`
- `에디터·로컬 파일 크기만으로 실제 store-served size 확정`

## 18. 공식 근거

다음은 이 Guide를 작성할 때 사용한 주요 T1 공식 근거다. 세부 버전·정책·플랫폼 조건은 실제 프로젝트 적용 전에 재검증한다.

### Godot

- Importing images / texture compression and mipmaps
  - https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
  - 사용: VRAM compression, platform-specific format, mipmap/2D artifact trade-off.
- Importing audio samples
  - https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
  - 사용: WAV/Ogg Vorbis/MP3의 disk-size와 CPU trade-off.
- Using Fonts
  - https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_fonts.html
  - 사용: font resource, font size, fallback/variation 구조.

### Android / Google Play

- Reduce game size
  - https://developer.android.com/games/optimize/game-size
  - 사용: optimized delivery → baseline/structure → large assets → texture optimization 순서.
- Target texture compression formats in Android App Bundles
  - https://developer.android.com/guide/playcore/asset-delivery/texture-compression
  - 사용: device-targeted texture compression sets.
- Play Asset Delivery
  - https://developer.android.com/guide/playcore/asset-delivery
  - 사용: install-time / fast-follow / on-demand 전달 경계.

### Steam

- Uploading to Steam / SteamPipe Content System
  - https://partner.steamgames.com/doc/sdk/uploading
  - 사용: 약 1 MB chunk 기반 delta, pack locality, pack size·ordering·compression과 patch/update disk trade-off.

## 19. 재검증 조건

다음이 바뀌면 공식 근거와 프로젝트 profile을 다시 확인한다.

- Godot major/minor upgrade가 import/export behavior를 바꿈
- renderer 변경
- Android minimum/target device class 변경
- Google Play App Bundle/PAD 정책 변경
- Steam packaging/depot 구조 변경
- 지원 언어·voice 범위 증가
- Art Direction 또는 base resolution 변경
- 대형 DLC/지역/영상 추가
- patch size 또는 first-session download가 budget을 초과
- Android memory/thermal regression 발생

## 20. 완료 판정

문서 작성만으로 최적화 완료를 선언하지 않는다.

```text
GUIDE_AVAILABLE
→ PROJECT_BASELINE_MEASURED
→ TOP_CONTRIBUTORS_IDENTIFIED
→ OPTIMIZATIONS_APPLIED
→ QUALITY_RUNTIME_DELIVERY_RECHECKED
→ STORE_SERVED_AND_PATCH_EVIDENCE_WHEN_RELEASE_RELEVANT
→ OPTIMIZATION_VERIFIED
```

실제 build·device·store·human 검증이 없으면 해당 상태는 각각 `NOT_RUN`, `DEVICE_NOT_RUN`, `STORE_NOT_RUN`, `HUMAN_NOT_RUN` 또는 `BLOCKED_UNVERIFIED`로 유지한다.
