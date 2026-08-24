# TRPG Source Rights & Frontier Addendum — 2026-08-24

이 문서는 `TRPG_SOURCE_SCAN_2026-08-24.md`의 **권리·접근 상태를 보강**하고, 추가로 확인한 materially distinct system을 기록한다. 아래 exact URL이 본문에 축약 표기가 있는 경우 우선한다.

## Exact official URLs / rights checks

### GUMSHOE

- landing: `https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/`
- current CC PDF: `https://pelgranepress.com/gumshoe/files/GUMSHOESRDCC-3%20241209.pdf`
- rights: Creative Commons Attribution 3.0 Unported for the SRD; GUMSHOE trademark attribution conditions apply; listed setting/product trademarks are excluded.
- teaching note: Pelgrane explicitly states the SRD is a **designer reference, not a text tuned to teach or provide a playable experience**.
- Base implication: `REFERENCE_SCHEMA_IS_NOT_TEACHING_ORDER`를 룰북 설계 검수 질문으로 유지한다.

### Year Zero Engine

- SRD: `https://freeleaguepublishing.com/wp-content/uploads/2023/11/YZE-Standard-Reference-Document.pdf`
- license: `https://freeleaguepublishing.com/wp-content/uploads/2023/11/Year-Zero-Engine-License-Agreement.pdf`
- license hub: `https://freeleaguepublishing.com/community-content/free-tabletop-licenses/`
- rights: Year Zero Engine Free Tabletop License v1.0. SRD를 기반으로 tabletop RPG 및 VTT module을 만들 수 있으나 Free League의 다른 artwork/text/brands/logos는 포함되지 않는다. Video game은 이 라이선스의 VTT 범위가 아니다.
- Base implication: `FREE_PUBLICATION != OPEN_REUSE`, `SRD_LICENSE_SCOPE != WHOLE_PRODUCT_RIGHTS`를 분리한다.

### Blades in the Dark / Forged in the Dark

- SRD/searchable home: `https://bladesinthedark.com/`
- licensing: `https://bladesinthedark.com/licensing`
- downloads/player kit: `https://bladesinthedark.com/downloads`
- rights: SRD는 Creative Commons Attribution 3.0 Unported 기반. Duskwall/Shattered Isles setting, NPCs, artwork, maps 등 SRD 밖의 Product Identity는 제외된다.
- support-artifact observation: official downloads separate core playsheets, player's kit, character playbooks, crew sheets, faction/campaign tracking.

### Basic Roleplaying — Universal Game Engine

- official product/reference page: `https://www.chaosium.com/basic-roleplaying-universal-game-engine-pdf/`
- ORC license page: `https://www.chaosium.com/orc-license/`
- ORC content announcement: `https://www.chaosium.com/blogdownload-the-free-basic-roleplaying-orc-content-document-sell-the-games-you-create-royaltyfree/`
- quickstart: `https://downloads.chaosium.com/basic-roleplaying/cha2040-brp-quickstart/CHA2040_Basic_Roleplaying_Quickstart.pdf`
- rights: BRP Universal Game Engine rules text is offered as ORC Licensed Material; artwork, illustrations, graphic design, trade dress, and listed trademarks are Product Identity/excluded.

#### 특징 / 어떻게 풀어냈는가

- **문제:** 전통적이고 범용적인 캐릭터 능력을 플레이어가 확률로 직관적으로 이해하도록 한다.
- **해법:** 핵심 판정은 d100 roll-under. 캐릭터 시트의 skill/characteristic 수치가 곧 성공 확률과 직접 연결된다.
- **성장:** 캐릭터가 실제로 사용한 기술이 향상될 수 있게 하여 '행동한 것 → 성장한 것'의 연결을 강하게 만든다.
- **확장성:** core system에 여러 optional rule을 붙이는 toolkit 성격. 모든 옵션을 기본 필수 규칙으로 강제하지 않는다.
- **support artifacts:** 기본 캐릭터 시트, hit-location 시트, NPC 시트, vehicle/mount 시트, handout pack, character-generation chart를 분리 제공한다.

#### 설명 순서 / 교육 방식

공식 Quickstart는 먼저 자신이 **플레이 가능한 introduction**임을 선언하고, basic character creation + game system + combat + equipment + sample scenarios/ready characters를 한 묶음으로 제공한다. 이는 완전한 universal engine reference보다 먼저 **작게 실행 가능한 slice**를 제공하는 방식이다.

공용 관찰:

```text
universal reference / toolkit
!=
first-session teaching surface
```

따라서 범용·모듈형 시스템은 `Quickstart → Core → Options/Toolkit`의 3층을 분리할 가치가 크다.

- disposition: `ADOPT` — success probability legibility, quickstart/core/options split, support artifacts.
- project-specific mechanic adoption: `TEST` — d100 자체는 desired experience에 따라 선택한다.

## 사용자 지정 링크 5종 coverage check

| 사용자 링크 | 현재 상태 | Base에서의 역할 |
| --- | --- | --- |
| `https://cympub.kr/` | publisher page 직접 확인 | 한국어 TRPG publisher/source pool, demo/teaching 사례 |
| `https://sites.google.com/view/dwtemporary/홈` | 직접 확인 | Dungeon World 한국어 공개판, fiction-first/GM procedure/설명 순서 |
| `https://www.trpgclub.com/` | 직접 확인 | 상용 룰북 소개 + support artifact ecosystem |
| 초여명 Fate Dropbox folder | publisher 연결은 확인, direct folder listing 실패 | `UNVERIFIED_DIRECT`; 사용자가 ZIP 제공 시 파일/판본/순서 직접 분석 |
| `https://blog.naver.com/adventurekeeper` | direct crawl 실패 | `UNVERIFIED_DIRECT`; VTT/ORPG presentation layer discovery only |

이 다섯 source는 이후 ZIP 분석에서도 삭제하지 않고 source provenance로 유지한다.

## 추가 source를 고르는 기준

Source 수를 늘리는 것 자체가 목표가 아니다. 다음 중 하나를 새로 설명할 때만 frontier에 추가한다.

1. **다른 판정 가족** — d20, percentile, dice pool, step die, no-dice/token 등.
2. **다른 information model** — hidden information, core clue, oracle, shared authorship.
3. **다른 campaign loop** — mission/downtime, vow/progress, base/crew, relationship loop.
4. **다른 pedagogy** — replay-first, player-principles-first, quickstart-first, reference-first.
5. **다른 support artifact boundary** — player/GM books, cards, clocks, investigation sheets, faction maps.
6. **다른 rights model** — CC, ORC, dedicated license, commercial/reference-only.

동일한 구조를 반복하는 source는 증거 강화에는 쓸 수 있지만 새로운 공용 계약을 자동으로 만들지 않는다.
