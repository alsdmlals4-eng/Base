# 게임 개발 Reference Source Catalog

```yaml
catalog_role: evidence-based-game-development-reference-index
checked_at: 2026-08-07
owner_method: docs/knowledge/game-development/EVIDENCE_BASED_GAME_DEVELOPMENT_METHOD.md
```

## 1. 목적

이 Catalog는 게임 기획·아트·개발·AI·접근성·유저리서치·출시 판단에 사용할 수 있는 공식·학술·현업 출처를 분류한다.

- 원문 전체를 복제하지 않는다.
- 개별 프로젝트 적용 시 게시일·버전·정책·지역·계정 조건을 다시 확인한다.
- 이 목록에 있다는 이유만으로 모든 조언이 모든 프로젝트에 적용되는 것은 아니다.
- 실제 적용은 Evidence Pack에서 현재 결정 질문과 연결하고 `ADOPT / ADAPT / TEST / AVOID / IGNORE / REFERENCE_ONLY`로 판정한다.

## 2. 근거 층

| 층 | 의미 |
|---|---|
| `T1_PRIMARY_OFFICIAL` | 공식 플랫폼·엔진·표준·원 논문·개발사 원문 |
| `T2_PROFESSIONAL_PRACTICE` | GDC 발표·개발자 회고·스튜디오 기술 블로그·현업 가이드 |
| `T3_PLAYER_BEHAVIOR` | 플레이테스트 관찰·텔레메트리·퍼널·실제 행동 |
| `T4_PLAYER_SELF_REPORT` | 리뷰·인터뷰·설문·커뮤니티 반응 |
| `T5_SYNTHESIS` | 전문 서적·리뷰 논문·종합 자료 |
| `T6_AI_INFERENCE` | AI 요약·분류·가설. 독립 권한 없음 |

## 3. 공통 Source Record

```yaml
source_id:
title:
organization_or_author:
url:
source_tier:
published_or_version:
checked_at: 2026-08-07
topics: []
use_for:
사용_한계:
재검증_조건:
```

## 4. 게임 기획·연구

### GD-MDA-001

```yaml
source_id: GD-MDA-001
title: MDA: A Formal Approach to Game Design and Game Research
organization_or_author: Robin Hunicke, Marc LeBlanc, Robert Zubek / AAAI
url: https://aaai.org/papers/ws04-04-001-mda-a-formal-approach-to-game-design-and-game-research/
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: 2004
checked_at: 2026-07-29
topics: [Mechanics, Dynamics, Aesthetics, iterative design]
use_for: 규칙·시스템 행동·플레이어 경험의 연결을 구조화한다.
사용_한계: 프레임워크만으로 대상 플레이어·제작성·접근성·행동 증거를 자동 도출하지 않는다.
재검증_조건: 원문 정의를 벗어난 확장 용어를 공용 규칙으로 만들 때.
```

### GUR-OUP-001

```yaml
source_id: GUR-OUP-001
title: Games User Research
organization_or_author: Oxford University Press / Anders Drachen, Pejman Mirza-Babaei, Lennart E. Nacke editors
url: https://academic.oup.com/book/26677
source_tier: T5_SYNTHESIS
published_or_version: 2018
checked_at: 2026-07-29
topics: [Games User Research, playtesting, analytics, methods, bias]
use_for: GUR 분야의 방법·산업 적용·편향·관찰·분석 구조를 참고한다.
사용_한계: 일부 장은 유료이며 프로젝트별 최신 도구·플랫폼 요건은 별도 확인한다.
재검증_조건: 특정 방법의 세부 절차·표본·통계 결정을 확정할 때 원 장을 확인한다.
```

### GUR-METHOD-001

```yaml
source_id: GUR-METHOD-001
title: Choose the right playtest method
organization_or_author: Games User Research / Steve Bromley
url: https://gamesuserresearch.com/choose-the-right-playtest-method/
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: updated 2023-09-25
checked_at: 2026-07-29
topics: [observation, interviews, analytics, surveys]
use_for: 연구 질문에 맞는 방법을 선택하고 행동·자기보고·규모·원인 탐색을 구분한다.
사용_한계: 상업 서비스 사이트의 현업 가이드이며 학술 원 논문과 프로젝트 제약을 함께 본다.
재검증_조건: 새로운 방법·도구·서비스 요건을 채택할 때.
```

### GUR-PLAYTEST-001

```yaml
source_id: GUR-PLAYTEST-001
title: How To Run A Games User Research Playtest
organization_or_author: Games User Research / Steve Bromley
url: https://gamesuserresearch.com/how-to-run-a-games-user-research-playtest/
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: updated 2024-06-05
checked_at: 2026-07-29
topics: [research question, recruitment, method, analysis, reporting]
use_for: 플레이테스트 전 과정을 연구 질문·참가자·방법·수집·분석·보고로 연결한다.
사용_한계: 프로젝트 규모·예산·지역·개인정보 조건에 맞춰 축소·변형해야 한다.
재검증_조건: 외부 참가자 모집·녹화·데이터 보관 절차를 실제 운영할 때.
```

### GUR-VALIDITY-001

```yaml
source_id: GUR-VALIDITY-001
title: Play as if you were at home: dealing with biases and test validity
organization_or_author: Oxford Academic / Guillaume Louvel
url: https://academic.oup.com/book/26677/chapter/195460947
source_tier: T5_SYNTHESIS
published_or_version: 2018
checked_at: 2026-07-29
topics: [test bias, validity, lab versus natural context]
use_for: 테스트 환경과 실제 플레이 환경의 차이, 편향과 결과 일반화 한계를 기록한다.
사용_한계: 원문 전체 접근 여부와 프로젝트의 실제 test setup을 별도 확인한다.
재검증_조건: 플레이테스트 결과를 전체 타깃 플레이어로 일반화할 때.
```

## 5. 아트 디렉션·에셋 생산

### ART-FRAMEWORK-001

```yaml
source_id: ART-FRAMEWORK-001
title: Building a Visual Identity: An Art Direction Framework
organization_or_author: GDC Vault / Genevieve Routhier, EA DICE
url: https://gdcvault.com/free/gdc-23/play/1028731/Art-Direction-Summit-Building-a
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2023
checked_at: 2026-07-29
topics: [art pillars, visual identity, technical and marketing considerations]
use_for: Art Direction을 key art가 아닌 예술·창작·기술·마케팅의 통합 프레임으로 설계한다.
사용_한계: AAA 조직 규모와 현재 1인 프로젝트의 제작 역량 차이를 ADAPT한다.
재검증_조건: 발표 원문·슬라이드의 세부 프레임을 직접 적용할 때.
```

### ART-GRAPHIC-001

```yaml
source_id: ART-GRAPHIC-001
title: Art Direction: Graphic Design is Key
organization_or_author: GDC Vault / Liam Wong, Ubisoft Montreal
url: https://www.gdcvault.com/play/1023276/Art-Direction-Graphic-Design-is
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2016
checked_at: 2026-07-29
topics: [visual signature, typography, iconography, logo, color, UI, key art]
use_for: 게임의 visual identity를 UI·메뉴·키아트·motion·홍보까지 일관되게 연결한다.
사용_한계: 스타일 요소 자체를 복제하지 않고 역할과 프로세스만 참고한다.
재검증_조건: 특정 상표·로고·타이포그래피를 실제 상업 자산으로 채택할 때.
```

### ART-SHAPE-001

```yaml
source_id: ART-SHAPE-001
title: Building Worlds Through Shape Language
organization_or_author: GDC Vault / Patrick Faulwetter
url: https://www.gdcvault.com/play/1025897/Art-Direction-Bootcamp-Building-Worlds
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2019
checked_at: 2026-07-29
topics: [shape language, culture, worldbuilding, architecture, costume, environment]
use_for: 세계관의 문화·가치·기능을 공통 형태 언어로 확장한다.
사용_한계: 형태 언어가 모든 대상의 다양성과 실루엣을 획일화하지 않게 검수한다.
재검증_조건: 특정 시각 상징이 실제 문화·종교·상표와 충돌할 가능성이 있을 때.
```

### ART-PREPROD-001

```yaml
source_id: ART-PREPROD-001
title: Pre-Production: The Lies We Tell
organization_or_author: GDC Vault / Greg Foertsch, Bit Reactor
url: https://gdcvault.com/play/1034593/Art-Direction-Summit-Pre-Production
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2024
checked_at: 2026-07-29
topics: [preproduction, Art Bible, evaluation gates, production readiness]
use_for: 시각 탐색·Art Bible·생산 진입 조건과 평가 지점을 분리한다.
사용_한계: 발표의 조직 계층과 일정 숫자를 1인 개발에 그대로 적용하지 않는다.
재검증_조건: Art Bible·production gate 세부 항목을 확정할 때.
```

### ART-ASSET-001

```yaml
source_id: ART-ASSET-001
title: Guerrilla Games Approach to Asset Production
organization_or_author: GDC Vault / Maarten Van Der Gaag, Guerrilla Games
url: https://www.gdcvault.com/play/1023575/Art-Direction-Bootcamp-Guerrilla-Games
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2016
checked_at: 2026-07-29
topics: [asset briefs, outsourcing, quality control, production pipeline]
use_for: AI·외주·협력 자산의 상세 Brief·검토 단계·품질 보호 원리를 참고한다.
사용_한계: 대규모 외주 조직과 자산량을 복제하지 않고 계약·검수 원리만 ADAPT한다.
재검증_조건: 외주 계약·납품 권리·비용·일정 조건을 실제 결정할 때.
```

### ART-UI-001

```yaml
source_id: ART-UI-001
title: Art Direction for AAA UI
organization_or_author: GDC Vault / Omer Younas, DICE LA
url: https://www.gdcvault.com/play/1025498/Art-Direction-for-AAA
source_tier: T2_PROFESSIONAL_PRACTICE
published_or_version: GDC 2018
checked_at: 2026-07-29
topics: [UI art direction, cognition, consistency, engine implementation]
use_for: visual identity와 정보 가독성을 concept부터 release까지 연결한다.
사용_한계: AAA UI 규모·도구를 그대로 요구하지 않고 인지·일관성 원칙을 축소 적용한다.
재검증_조건: 발표의 구체 이론·화면 사례를 공식 프로젝트 기준으로 채택할 때.
```

## 6. 접근성

### ACCESS-XAG-001

```yaml
source_id: ACCESS-XAG-001
title: Xbox Accessibility Guidelines
organization_or_author: Microsoft
url: https://learn.microsoft.com/en-us/xbox/accessibility/guidelines
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: XAG v3.2; page updated 2026-03-04
checked_at: 2026-07-29
topics: [text, contrast, cues, captions, audio, input, difficulty, UI, time, motion]
use_for: 설계·개발·테스트의 접근성 가드레일과 플레이 장벽 질문을 제공한다.
사용_한계: 법적 준수 인증이 아니며 실제 프로젝트·플랫폼·플레이어 검증을 대신하지 않는다.
재검증_조건: Microsoft guideline version 변경 또는 release checklist 확정 전.
```

### ACCESS-INPUT-001

```yaml
source_id: ACCESS-INPUT-001
title: Xbox Accessibility Guideline 107 Input
organization_or_author: Microsoft
url: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: checked current 2026-07-29
checked_at: 2026-07-29
topics: [input choice, alternative input, cancellation, remapping]
use_for: 터치·키보드·마우스·패드·비전통 입력의 장벽과 대안을 설계한다.
사용_한계: 장르의 필수 입력과 플레이어 선택 입력을 프로젝트별로 판정한다.
재검증_조건: 입력 지원 범위·플랫폼 certification을 확정할 때.
```

### ACCESS-UI-001

```yaml
source_id: ACCESS-UI-001
title: Xbox Accessibility Guidelines 112 UI navigation and 113 UI focus handling
organization_or_author: Microsoft
url: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/112
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: checked current 2026-07-29
checked_at: 2026-07-29
topics: [UI navigation, predictable focus, assistive technology]
use_for: 메뉴 구조·focus·일관성·설정 진입 장벽을 검수한다.
사용_한계: 실제 Godot focus graph와 입력 장치 테스트가 필요하다.
재검증_조건: UI architecture 또는 지원 장치가 변경될 때.
```

### ACCESS-MOTION-001

```yaml
source_id: ACCESS-MOTION-001
title: Xbox Accessibility Guideline 117 Visual distractions and motion settings
organization_or_author: Microsoft
url: https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: checked current 2026-07-29
checked_at: 2026-07-29
topics: [camera motion, shake, scrolling, blinking, auto-update]
use_for: motion reduction·camera·blinking·자동 갱신 장벽과 설정을 설계한다.
사용_한계: photosensitivity·법률·의료 판단을 대신하지 않는다.
재검증_조건: 카메라·VFX·UI animation 범위가 변경될 때.
```

## 7. Godot·Android

### GODOT-RESOLUTION-001

```yaml
source_id: GODOT-RESOLUTION-001
title: Multiple resolutions
organization_or_author: Godot Engine documentation
url: https://docs.godotengine.org/en/latest/tutorials/rendering/multiple_resolutions.html
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: latest documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [base resolution, stretch mode, stretch aspect, UI scale]
use_for: 논리 해상도·비율·2D scaling·viewport 전략을 설계한다.
사용_한계: 프로젝트 고정 Godot 버전 문서와 실제 화면·자산을 함께 검증한다.
재검증_조건: Godot version·renderer·target platform·orientation 변경 시.
```

### GODOT-ASSET-IMAGE-001

```yaml
source_id: GODOT-ASSET-IMAGE-001
title: Importing images
organization_or_author: Godot Engine documentation
url: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: stable documentation checked 2026-08-07
checked_at: 2026-08-07
topics: [texture import, VRAM compression, S3TC, BPTC, ETC2, ASTC, mipmaps, pixel art]
use_for: texture의 disk·VRAM·품질 trade-off와 desktop/mobile import profile을 설계한다.
사용_한계: renderer·Godot version·texture role에 따라 가능한 포맷과 품질이 다르므로 모든 자산에 같은 설정을 강제하지 않는다.
재검증_조건: Godot version·renderer·target GPU·texture pipeline 변경 시.
```

### GODOT-ASSET-AUDIO-001

```yaml
source_id: GODOT-ASSET-AUDIO-001
title: Importing audio samples
organization_or_author: Godot Engine documentation
url: https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_audio_samples.html
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: stable documentation checked 2026-08-07
checked_at: 2026-08-07
topics: [WAV, Ogg Vorbis, MP3, file size, CPU decoding, simultaneous voices]
use_for: SFX·music·voice의 파일 크기와 재생 CPU 비용을 함께 비교한다.
사용_한계: 실제 encoder 설정·동시 재생량·기기 CPU·청취 품질에 따라 결과가 달라진다.
재검증_조건: Godot audio importer·target device·동시 voice 수·오디오 파이프라인 변경 시.
```

### GODOT-FONT-001

```yaml
source_id: GODOT-FONT-001
title: Using Fonts
organization_or_author: Godot Engine documentation
url: https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_fonts.html
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: stable documentation checked 2026-08-07
checked_at: 2026-08-07
topics: [font resources, font size, fallback, variable fonts, UI typography]
use_for: 동일 font file의 크기별 복제를 피하고 Theme·fallback·variation을 용량·가독성 정책과 연결한다.
사용_한계: CJK·emoji·언어별 glyph coverage와 라이선스는 실제 폰트 파일로 별도 확인한다.
재검증_조건: 지원 언어·font family·Godot text rendering 설정 변경 시.
```

### ANDROID-PERF-001

```yaml
source_id: ANDROID-PERF-001
title: Android game optimization
organization_or_author: Android Developers
url: https://developer.android.com/games/optimize/overview
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: updated 2026-05-20 UTC
checked_at: 2026-07-29
topics: [GPU, CPU, memory, thermal, performance tools, device limitations]
use_for: 모바일 목표 기기에서 지속 가능한 성능·메모리·열 병목 측정 계획을 세운다.
사용_한계: 모든 API가 모든 기기·엔진 조합에 동일하게 적용되지 않는다.
재검증_조건: Android target API·ADPF·Game Mode·도구 버전 변경 시.
```

### ANDROID-GAMEMODE-001

```yaml
source_id: ANDROID-GAMEMODE-001
title: Game Mode API and interventions
organization_or_author: Android Developers
url: https://developer.android.com/games/optimize/adpf/gamemode/about-API-and-interventions
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: updated 2026-02-26 UTC
checked_at: 2026-07-29
topics: [performance mode, battery mode, OEM interventions]
use_for: 모바일 성능·배터리 설정과 사용자 선택을 고려한다.
사용_한계: 선택 기기·OEM 지원과 게임 구현 방식에 따라 달라진다.
재검증_조건: 실제 Android 출시와 지원 기기 정책 확정 전.
```

### ANDROID-SIZE-001

```yaml
source_id: ANDROID-SIZE-001
title: Reduce game size
organization_or_author: Android Developers
url: https://developer.android.com/games/optimize/game-size
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current page checked 2026-08-07
checked_at: 2026-08-07
topics: [game size, Android App Bundle, Play Asset Delivery, baseline size, asset analysis, textures]
use_for: Android 게임 용량을 optimized delivery → baseline/structure → large assets → texture optimization 순서로 조사한다.
사용_한계: 공개된 평균 절감률이나 install-conversion 관계를 개별 프로젝트의 보장 수치로 사용하지 않는다.
재검증_조건: Google Play download limit·App Bundle·PAD 정책 또는 프로젝트 delivery 구조 변경 시.
```

### ANDROID-TCF-001

```yaml
source_id: ANDROID-TCF-001
title: Target texture compression formats in Android App Bundles
organization_or_author: Android Developers
url: https://developer.android.com/guide/playcore/asset-delivery/texture-compression
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current page checked 2026-08-07
checked_at: 2026-08-07
topics: [texture compression format targeting, App Bundle, ETC2, ASTC, device targeting]
use_for: 기기별 지원 texture compression set을 전달해 불필요한 texture variant download를 줄이는 후보를 평가한다.
사용_한계: 실제 Godot export·Gradle/App Bundle 구성·기기 지원 범위를 확인하지 않고 강제하지 않는다.
재검증_조건: Android Gradle Plugin·Play delivery·Godot Android export pipeline 변경 시.
```

### ANDROID-PAD-001

```yaml
source_id: ANDROID-PAD-001
title: Play Asset Delivery
organization_or_author: Android Developers
url: https://developer.android.com/guide/playcore/asset-delivery
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current page checked 2026-08-07
checked_at: 2026-08-07
topics: [install-time, fast-follow, on-demand, asset packs, App Bundle]
use_for: 첫 세션 필수 asset과 optional/후반 콘텐츠의 전달 경계를 설계한다.
사용_한계: 초기 다운로드를 줄이기 위해 첫 실행 필수 asset을 무리하게 분리하지 않고 network/offline UX를 함께 검증한다.
재검증_조건: Google Play PAD 정책·asset pack limit·프로젝트 offline requirement 변경 시.
```

## 8. Steam·출시

### STEAM-PLAYTEST-001

```yaml
source_id: STEAM-PLAYTEST-001
title: Steam Playtest
organization_or_author: Valve Steamworks
url: https://partner.steamgames.com/doc/features/playtest
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [separate AppID, gated access, playtest operation]
use_for: 본 게임 review·wishlist와 분리된 외부 테스트 배포를 계획한다.
사용_한계: 참가자·연구 질문·피드백·텔레메트리 계약을 자동 제공하지 않는다.
재검증_조건: Steam Playtest를 실제 개설하거나 권한·Store 설정을 변경할 때.
```

### STEAM-REVIEWS-001

```yaml
source_id: STEAM-REVIEWS-001
title: User Reviews
organization_or_author: Valve Steamworks
url: https://partner.steamgames.com/doc/store/reviews
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [review score, playtime, expectations, developer response, off-topic]
use_for: 제품 약속과 실제 경험의 일치·불일치를 분석하는 자기보고 채널로 사용한다.
사용_한계: 리뷰는 전체 플레이어 행동을 대표하지 않으며 플랫폼·구매·패치·언어 맥락이 필요하다.
재검증_조건: review display·score·moderation 정책 변경 또는 출시 후 분석 전.
```

### STEAM-WISHLIST-001

```yaml
source_id: STEAM-WISHLIST-001
title: Wishlists
organization_or_author: Valve Steamworks
url: https://partner.steamgames.com/doc/marketing/wishlist
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [interest signal, notifications, regional reporting, cohort]
use_for: Store page·demo·event가 관심 신호에 미치는 변화를 관찰한다.
사용_한계: Wishlist에서 판매를 정확히 예측하는 단일 공식은 없으며 관심 원인이 다양하다.
재검증_조건: notification trigger·cooldown·reporting·Store 정책 변경 전.
```

### STEAM-COMINGSOON-001

```yaml
source_id: STEAM-COMINGSOON-001
title: Coming Soon
organization_or_author: Valve Steamworks
url: https://partner.steamgames.com/doc/store/coming_soon
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [store page, audience building, minimum public period]
use_for: 공개 가능한 gameplay·branding·description 준비와 release 의존성을 계획한다.
사용_한계: 최소 기간·review 절차·release rule은 실제 적용 시 공식 페이지로 재확인한다.
재검증_조건: Steam release 계획·store review 제출 직전.
```

### STEAM-PIPE-001

```yaml
source_id: STEAM-PIPE-001
title: Uploading to Steam / SteamPipe Content System
organization_or_author: Valve Steamworks
url: https://partner.steamgames.com/doc/sdk/uploading
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-08-07
checked_at: 2026-08-07
topics: [SteamPipe, chunks, patch size, pack files, compression, update disk, depots]
use_for: 설치 크기와 patch 크기를 분리하고 pack locality·asset ordering·compression boundary·temporary disk trade-off를 검증한다.
사용_한계: 문서의 pack-size 예시나 Unreal-specific 설정을 Godot/모든 프로젝트의 고정 수치로 복사하지 않는다.
재검증_조건: SteamPipe packaging·depot·project pack structure 또는 Valve 권장사항 변경 시.
```

## 9. AI 위험·Evals·검수

### AI-NIST-RMF-001

```yaml
source_id: AI-NIST-RMF-001
title: AI Risk Management Framework
organization_or_author: NIST
url: https://www.nist.gov/itl/ai-risk-management-framework
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: AI RMF 1.0 under revision; page checked 2026-07-29
checked_at: 2026-07-29
topics: [AI risk, governance, measurement, lifecycle]
use_for: AI 활용의 목적·위험·책임·측정·대응을 조직 작업 흐름에 연결한다.
사용_한계: 자발적 일반 프레임워크이며 게임 프로젝트의 법률·계약·제품 검증을 대신하지 않는다.
재검증_조건: AI RMF 개정판 또는 프로젝트 AI 권한·데이터 처리 변경 시.
```

### AI-NIST-GEN-001

```yaml
source_id: AI-NIST-GEN-001
title: Artificial Intelligence Risk Management Framework Generative AI Profile
organization_or_author: NIST
url: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: NIST AI 600-1, 2024; page updated 2026-04-08
checked_at: 2026-07-29
topics: [generative AI risk, trustworthiness, lifecycle]
use_for: 생성형 AI의 출처·오류·보안·사람 감독·평가 위험을 검토한다.
사용_한계: 프로젝트별 모델·도구·데이터·권한·지역 법률을 별도 검토한다.
재검증_조건: 모델 활용 범위·외부 데이터·출시 자산·자동화 권한 변경 시.
```

### AI-EVAL-001

```yaml
source_id: AI-EVAL-001
title: How evals drive the next chapter in AI for businesses
organization_or_author: OpenAI
url: https://openai.com/index/evals-drive-next-chapter-of-ai/
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: 2025-11-19
checked_at: 2026-07-29
topics: [SPECIFY, MEASURE, IMPROVE, Golden Set]
use_for: AI 작업의 기대 결과·대표 사례·측정·오류 개선 루프를 설계한다.
사용_한계: 특정 공급자 관점이며 프로젝트 독립 검수·다른 모델·도구 조건을 함께 기록한다.
재검증_조건: Eval API·모델·도구·평가 방법이 바뀔 때.
```

### AI-EVAL-VALIDITY-001

```yaml
source_id: AI-EVAL-VALIDITY-001
title: A shared playbook for trustworthy third party evaluations
organization_or_author: OpenAI
url: https://openai.com/index/trustworthy-third-party-evaluations-foundations/
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: 2026-05-29
checked_at: 2026-07-29
topics: [harness, tools, budget, validity, contamination, broken tasks]
use_for: Agentic AI 평가에서 model 외에 harness·tool·budget·validity check를 기록한다.
사용_한계: frontier AI safety 평가 맥락의 원리를 게임 개발 AI 작업에 ADAPT한다.
재검증_조건: 모델 비교·자동화 권한·장기 agent workflow Eval 설계 시.
```

### AI-CODING-EVAL-001

```yaml
source_id: AI-CODING-EVAL-001
title: Separating signal from noise in coding evaluations
organization_or_author: OpenAI
url: https://openai.com/index/separating-signal-from-noise-coding-evaluations/
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: 2026-07-08
checked_at: 2026-07-29
topics: [broken benchmark tasks, human audit, coding eval validity]
use_for: AI 실패를 결론 내리기 전 issue·test·environment가 올바른지 검증한다.
사용_한계: 특정 benchmark 감사 결과를 모든 저장소의 실패율로 일반화하지 않는다.
재검증_조건: 공용 benchmark 점수를 모델 선택·자동 승인 근거로 사용할 때.
```

### AI-GITHUB-REVIEW-001

```yaml
source_id: AI-GITHUB-REVIEW-001
title: Using GitHub Copilot code review on GitHub
organization_or_author: GitHub Docs
url: https://docs.github.com/en/copilot/how-tos/copilot-on-github/use-copilot-agents/copilot-code-review
source_tier: T1_PRIMARY_OFFICIAL
published_or_version: current documentation checked 2026-07-29
checked_at: 2026-07-29
topics: [AI code review, comments, approvals, merge gate]
use_for: Copilot Review를 보조 comment로 사용하고 사람 승인·Required Checks와 구분한다.
사용_한계: 계정·조직·플랜·Preview 기능에 따라 이용 가능성과 동작이 달라질 수 있다.
재검증_조건: Copilot policy·review effort·required approval 설정 변경 시.
```

## 10. 플레이어 증거 Source

`T3_PLAYER_BEHAVIOR`와 `T4_PLAYER_SELF_REPORT`는 고정 외부 URL 목록보다 프로젝트별 실제 Evidence Pack이 중요하다.

예:

- 목표 플레이어의 첫 경험 관찰
- Steam Playtest build와 행동 이벤트
- Google Play test track·pre-launch report
- Godot local telemetry
- Steam User Reviews·Google Play reviews
- 지원 문의·커뮤니티 주제
- A/B·Concept Test·Store page test

프로젝트별로 다음을 기록한다.

```yaml
build_and_version:
platform_and_language:
player_segment:
prior_exposure:
sample_size:
collection_method:
behavior_events:
self_report_channel:
patch_context:
bias_and_limitations:
```

## 11. 사용 한계

- 이 Catalog는 완전한 참고문헌 목록이 아니다.
- 특정 자료 하나로 제품 결정을 확정하지 않는다.
- 오래된 현업 사례도 원리와 실패를 이해하는 데 유용할 수 있지만 현재 도구·플랫폼 사실은 재검증한다.
- AAA·대규모 Live Service·모바일 대형 스튜디오의 조직·예산·일정 숫자를 1인 개발에 복사하지 않는다.
- 플레이어 리뷰와 커뮤니티는 선택 편향·패치·언어·플레이타임·오프토픽을 고려한다.
- AI 요약은 반드시 원출처와 실제 프로젝트 파일로 확인한다.

## 12. 재검증 조건

다음은 항상 적용 시점에 다시 확인한다.

- 소프트웨어·엔진·모델·API version
- 가격·요금·사용량·플랜
- Store·release·review·wishlist·test 정책
- Android target API·Google Play 요구사항
- GitHub Actions·Copilot·보안 정책
- 라이선스·상업 사용·출처·서비스 약관
- 접근성 guideline version
- 프로젝트 실제 플랫폼·기기·해상도·입력·성능
- Godot asset importer·renderer·texture/audio/font behavior
- Google Play App Bundle·Play Asset Delivery·texture targeting 정책
- SteamPipe packaging·chunking·patch/update 권장사항

## 13. 분야별 Source Router

TRPG 룰·룰북 설명 순서·Quickstart·Player/GM aid·상업/공개 SRD의 권리 경계는 이 Catalog에 개별 작품 Record를 대량 복제하지 않는다.

- 책임 Reference: `docs/knowledge/game-development/TRPG_RULE_DESIGN_REFERENCE_RADAR.md`
- 사용 질문: 판정 구조, 캐릭터 자유도, 조사/전투/GM 절차, 룰북 teaching order, support artifact, VTT presentation layer, SRD/번역/상표 권리 경계.
- 적용 판정: `ADOPT / ADAPT / TEST / AVOID / REFERENCE_ONLY`.
- 권한 경계: Radar는 프로젝트 룰 정본이 아니며, 실제 수치·세계관·즐거움·이해도·상업 사용 권리는 프로젝트 Evidence와 적용 시점의 원출처 재검증이 필요하다.
