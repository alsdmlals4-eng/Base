# UI/UX·비주얼 디자인 통합 Rulebook

> 확인일: 2026-08-10
> owner: `auditing-and-refining-ui-art`
> scope: 게임 UI, Godot UI, Web/앱형 보조 UI, UX 흐름, 비주얼 폴리싱
> principle: **접근성·의미·복구·프로젝트 코어를 보호하고, 심리학과 시각 팁은 증거 강도에 맞게 사용한다.**

이 문서는 Laws of UX, GUI 관례, 접근성 표준·플랫폼 가이드, 게임 접근성, 비주얼 디자인 휴리스틱을 하나의 실행 계약으로 묶는다. 외부 자료를 그대로 복제하지 않고 Base의 기존 `experience → flow → pattern → design system → accessibility → polishing → runtime audit` 흐름에 맞게 변환한다.

---

## 1. 규칙 강도

| Tier | 의미 | 위반 처리 |
|---|---|---|
| `MUST` | 사용자 지시·프로젝트 정본을 존중하면서도 의미 문법, 접근성, 안전, 복구, 명백한 상호작용 오류를 막는 공용 Gate | 충돌이 없으면 기본 적용. 예외는 이유·동등 경로·검증 필요 |
| `SHOULD` | 높은 확률로 이해·효율·일관성을 높이는 UX 기본값 | 프로젝트 코어/장르/입력과 충돌하면 `ADAPT` 또는 `TEST_REQUIRED` |
| `STYLE_DEFAULT` | 시각 완성도를 빠르게 높이는 안전 기본값 | 아트 방향·브랜드·플랫폼·접근성과 충돌하면 자유롭게 변경 가능 |
| `TEST_REQUIRED` | 맥락 민감하거나 행동 심리 효과가 큰 항목 | 실제 렌더·입력·플레이/사용자 증거 없이 전역 규칙으로 확정 금지 |

### 증거 유형

1. **규범 표준**: WCAG 등 명시된 적용 범위에서 준수 판단에 쓰는 기준.
2. **플랫폼 권고**: Apple, Android, Xbox 등 특정 입력·기기·생태계에서 강한 기본값.
3. **인지·사용성 휴리스틱**: Laws of UX, Nielsen 계열처럼 문제를 설명하고 가설을 세우는 근거.
4. **시각 스타일 휴리스틱**: Anthony Hobday, Adham Dannaway 계열처럼 미감·일관성·가독성의 출발점.

**금지:** 서로 다른 증거 유형을 같은 권위로 합치거나, 플랫폼 단위를 지워 하나의 전역 상수로 만든다.

---

## 2. 판단 우선순위

```text
사용자 최신 지시·프로젝트 코어·보호된 아트 방향
→ 의미/상태/복구/안전
→ 접근성·입력 완결성
→ 화면 중심 질문·정보 위계
→ 플랫폼 관례와 멘탈 모델
→ 인지·사용성 휴리스틱
→ 시각 스타일 기본값
→ 장식과 delight
```

- 스타일 규칙이 대비, 포커스, 읽기, 입력 성공을 약화시키면 스타일 규칙을 버린다.
- 일반 앱의 단순성 규칙이 게임의 의도적 미스터리·긴장·탐색을 제거하면 장르 목적을 보존하되 **조작 방법, 현재 포커스, 취소/복구, 필수 피드백**은 모호하게 만들지 않는다.
- 수치 충족은 실제 플레이어 성공의 대리 지표일 뿐이다. 실기기·실제 거리·실제 입력·긴 한국어·접근성 설정에서 다시 검증한다.

---

# Part A. 상호작용 문법 — 사용자가 추측하지 않게 한다

## 3. GUI 상호작용 알파벳

### 3.1 버튼 — 행동 실행

**MUST**

- 버튼은 저장·구매·전송·삭제·확정처럼 **상태를 바꾸는 명령**에 사용한다. 이동은 링크/탐색 패턴을 우선한다.
- `OK`, `Submit`보다 `Save Invoice`, `Place Order`, `Delete 3 Files`처럼 **결과 중심** 레이블을 쓴다.
- custom 버튼은 normal/focused/pressed/disabled 등 필요한 상태가 구분되어야 한다.
- 화면마다 시각적으로 지배적인 primary action은 원칙적으로 하나만 둔다.
- disabled 상태를 이유 없이 숨기지 않는다. 보여줄 필요가 있다면 왜 비활성인지, 어떻게 활성화하는지 알려준다.

**SHOULD**

- 자주 쓰는 목표는 크게, 가까이 둔다. 이는 Fitts 원리와 일치한다.
- 읽기/입력 흐름이 끝나는 지점에 다음 행동을 둔다.

### 3.2 링크 — 목적지 이동

**MUST**

- 링크는 장소/문서/화면으로 이동하는 약속이다. 버튼처럼 꾸며 의미를 섞지 않는다.
- 링크 문구는 `Click here`, `Learn more`보다 목적지를 예측할 수 있어야 한다.
- 본문 링크는 색상만으로 구분하지 않는다. 밑줄·형태·문맥 등 추가 신호를 둔다.
- 새 창/탭을 열어야 하면 이유와 결과가 분명해야 한다. 기본은 현재 탐색 모델을 보존한다.

### 3.3 폼과 입력

**MUST**

- placeholder를 label 대체로 쓰지 않는다. 입력 중에도 필드 의미가 남아야 한다.
- 오류는 문제가 있는 위치, 문제의 원인, 복구 행동을 평이한 언어로 제공하고 기존 입력을 보존한다.
- 가능한 입력 형식의 변형은 합리적으로 수용하고 정규화한다. 단 Postel 원칙은 보안·schema·경제/도메인 제약을 넘어서지 않는다.
- 꼭 필요하지 않은 필드는 제거한다.

**SHOULD**

- 관련 필드는 그룹화하고 읽기 순서가 모호하지 않게 배치한다.
- 날짜, 범위, 색상 등은 작업에 맞는 전용 컨트롤을 우선한다.
- 실시간 검증이 사용자를 방해하면 blur/제출 시점 검증을 검토한다.

### 3.4 메뉴와 탐색

**MUST**

- 카테고리명은 사용자가 기대하는 어휘와 목적을 드러내야 한다.
- 현재 위치와 선택 상태가 명확해야 한다.
- hover만으로 핵심 메뉴 접근을 제한하지 않는다.

**SHOULD**

- 가장 빈번한 소수의 명령은 깊은 메뉴에서 꺼내 직접 노출한다.
- 데스크톱 공간이 충분한데 핵심 탐색을 무조건 hamburger에 숨기지 않는다.
- hover 계단식 메뉴는 깊이를 얕게 유지하고 pointer 이동 실패를 줄인다.

**중요 보정:** Miller의 `7±2`를 메뉴 항목 개수의 하드 캡으로 쓰지 않는다. 보이는 선택지는 recall 부담을 줄일 수 있으며, 긴 명확한 목록이 짧고 모호한 목록보다 나을 수 있다.

### 3.5 대화상자·모달

**MUST**

- modal은 실제로 작업을 차단해야 하는 결정, 필수 입력, 되돌리기 어려운 결과에만 쓴다.
- `OK/Cancel` 대신 실제 결과를 적는다.
- 되돌릴 수 있는 행동은 반복 확인보다 **실행 취소**를 우선 검토한다.
- modal을 닫으면 이전 의미 있는 focus/선택으로 복귀한다.
- modal 위에 modal을 쌓지 않는다.

### 3.6 알림·오류·피드백

**MUST**

- 오류는 “무엇이/어디서/왜 실패했는지/다음에 무엇을 할지”를 알려준다.
- 색상만으로 warning/error/success를 구분하지 않는다.
- 사용자가 조치해야 하는 오류를 자동으로 사라지는 toast에만 넣지 않는다.

**SHOULD**

- 단순 성공 확인은 toast, 수정 전까지 남아야 하는 문제는 inline, 재앙적/차단 상황만 modal을 검토한다.
- 알림 기본량을 낮추고 중요도와 반복 빈도에 따라 feedback budget을 배분한다.

### 3.7 아이콘

**MUST**

- 검색·설정·휴지통처럼 널리 학습된 소수 외에는 label 또는 접근 가능한 이름을 제공한다.
- 같은 의미는 같은 아이콘 문법을 유지하고, 다른 의미인데 같은 형태를 쓰지 않는다.
- 아이콘의 장식성 때문에 텍스트/상태보다 시각적으로 과도하게 무거워지지 않게 한다.

### 3.8 체크박스·라디오·토글

**MUST**

- 체크박스: 독립적인 on/off 또는 복수 선택.
- 라디오: 상호 배타적인 집합에서 하나 선택.
- 토글: 변경 즉시 적용되는 설정. 별도 Save가 필요한 의미라면 체크박스/선택 패턴을 검토한다.
- label 전체를 가능한 한 hit target에 포함한다.

**SHOULD**

- 2~4개의 작은 선택 집합은 dropdown보다 직접 노출한 radio가 빠른 비교에 유리한지 검토한다.
- 부정문/이중 부정을 피한다.

### 3.9 탭

**MUST**

- 같은 수준의 병렬 콘텐츠에만 사용한다. 순차 wizard 단계를 탭으로 위장하지 않는다.
- selected/focused/hover 상태가 구분되어야 한다.
- 서로 비교해야 하는 데이터를 탭으로 갈라 working memory에 떠넘기지 않는다.

### 3.10 검색

**MUST**

- 사용자가 탐색 구조를 모를 수 있는 큰 정보 공간에서는 검색을 탈출구로 검토한다.
- 오타·동의어·복수형 등 합리적인 변형을 허용한다.
- 결과 화면에서 현재 query와 수정 경로를 보존한다.

**SHOULD**

- 검색 로그/실패 질의를 실제 사용자 어휘와 IA 개선 근거로 사용한다.

### 3.11 창·스크롤·포인터

**MUST**

- scroll hijacking으로 기본 속도/방향/근육 기억을 가로채지 않는다.
- 핵심 footer/다음 행동이 있는데 infinite scroll로 영구히 밀어내지 않는다.
- 클릭 불가능한 장식에 pointer hand를 주지 않는다.
- 중요한 정보/행동에 접근하는 유일한 수단으로 hover를 사용하지 않는다.
- keyboard/controller focus는 항상 화면에 보이고 숨은 요소에 갇히지 않는다.

---

# Part B. 인지·행동 원칙 — 사용자가 기억·추측·과잉 결정하지 않게 한다

## 4. 인지와 지각

| 원칙 | Tier | Base 적용 | 적대적 오용 방지 |
|---|---|---|---|
| Aesthetic-Usability Effect | `TEST_REQUIRED` | 미적 완성도는 신뢰·인지된 사용성을 높일 수 있으므로 P0~P2 뒤 P3 polish를 수행 | 아름다움이 실제 usability defect를 가릴 수 있으므로 테스트에서 미감 점수와 task success를 분리 |
| 인지 부하 | `SHOULD` | 불필요한 장식·중복 상태·기억 부담을 줄이고 현재 목표에 필요한 정보만 우선 | 장르적 복잡성 자체를 삭제하지 말고 extraneous load를 줄임 |
| 선택적 주의 | `SHOULD` | 첫 시선·primary action·critical cue에 대비와 위치를 집중 | 모든 요소를 강조해 경쟁시키지 않음 |
| 작업 기억 | `SHOULD` | 비교 정보는 같은 화면/축에 유지하고, 이전 선택·맥락을 시스템이 기억 | `7±2`를 기계적 항목 제한으로 사용 금지 |
| 멘탈 모델 | `SHOULD` | 익숙한 관례와 프로젝트 내부 일관성을 사용 | 새 모델이 더 낫더라도 migration/onboarding 없이 갑자기 뒤집지 않음 |

## 5. 의사결정

| 원칙 | Tier | Base 적용 | 적대적 오용 방지 |
|---|---|---|---|
| Choice Overload | `SHOULD` | search/filter/recommendation/side-by-side 비교로 결정 부담을 줄임 | 선택 자체가 핵심 재미인 게임에서 옵션 수를 무조건 줄이지 않음 |
| Hick | `SHOULD` | 반응 시간이 중요한 순간의 선택 수·복잡성을 줄이고 긴 절차를 단계화 | 과도한 단순화로 의미를 숨기지 않음 |
| Fitts | `SHOULD` | 빈번/중요 target을 크게·가깝게 하고 target 사이 오입력을 줄임 | 시각 크기와 실제 hit region을 혼동하지 않음 |
| Jakob | `SHOULD` | 플랫폼과 장르의 학습된 관례를 활용 | 관례를 핑계로 프로젝트 고유 가치나 더 접근 가능한 패턴을 금지하지 않음 |

## 6. Gestalt와 정보 구조

- `SHOULD` **Law of Common Region**: 같은 경계/배경 영역은 같은 그룹으로 인식되므로 실제 의미 관계와 맞춰 사용한다.
- `SHOULD` **Law of Proximity**: 관련 요소를 더 가깝게 둔다. 외부 padding은 내부 item 간격과 같거나 큰 것이 좋은 출발점이다.
- `SHOULD` **Law of Similarity**: 같은 기능/상태는 같은 시각 문법을 쓰고, 다른 기능이면 필요한 차이를 만든다.
- `SHOULD` **Uniform Connectedness**: 선·프레임·연결 표시를 실제 관계에만 사용한다.
- `SHOULD` **Law of Prägnanz**: 복잡한 형상을 가능한 단순하게 해석하는 경향을 고려해 shape/outline을 명료하게 한다.
- `SHOULD` **Chunking**: 내용은 의미 단위로 묶고 heading/spacing/alignment를 사용한다.
- `SHOULD` **Serial Position Effect**: 중요한 시작/마지막 행동의 기억 우위를 고려한다. 단 focus/reading order와 실제 task sequence가 우선이다.
- `TEST_REQUIRED` **Von Restorff**: 핵심 CTA/critical state를 고립시켜 기억성을 높일 수 있지만 강조 남용·광고 오인·색상 단독 강조를 금지한다.

## 7. 몰입·동기·기억

| 원칙 | Tier | Base 적용 | 윤리/게임성 Gate |
|---|---|---|---|
| Flow | `TEST_REQUIRED` | skill과 challenge의 균형, 즉시 이해 가능한 feedback, 불필요한 UI friction 제거 | 난이도·긴장을 UI 편의성 하나로 평준화하지 않음 |
| Goal-Gradient | `TEST_REQUIRED` | 실제 완료에 가까워지는 과정은 progress indicator로 명료화 | **허위 진행**·기만적 사전 채움으로 행동을 강제하지 않음 |
| Zeigarnik | `TEST_REQUIRED` | 미완료 task/collection의 재개 지점을 명확히 할 수 있음 | 불안·강박을 유도하는 badge/unfinished pressure를 retention 장치로 남용 금지 |
| Peak-End | `TEST_REQUIRED` | 중요한 성공/실패 peak와 session ending의 clarity/recovery/delight를 다듬음 | 중간의 지속적 불편을 화려한 끝 연출로 정당화하지 않음 |

심리학은 플레이어의 선택을 **지원**하기 위한 것이다. 다크 패턴, 숨은 비용, 강제 연속 사용, 기만적 희소성, 취소 방해의 정당화 근거가 아니다.

---

# Part C. 시스템·시간 원칙

## 8. 반응성과 시간

- `SHOULD` **Doherty Threshold**: 400ms 이내 상호작용은 “서로 기다린다”는 감각을 줄이는 유용한 휴리스틱이다. compliance 상수로 쓰지 않는다.
- `MUST` 입력을 받았는지 가능한 즉시 명확히 보여준다. 처리 결과와 입력 접수를 혼동하지 않는다.
- `SHOULD` 1초 이상 눈에 띄는 대기에는 진행/작업 중 상태를 제공한다.
- `TEST_REQUIRED` skeleton/progress animation은 perceived performance를 개선할 수 있지만 실제 작업 상태와 불일치해서는 안 된다.
- **근거 없는 의도적 지연**으로 가치·신뢰를 꾸미는 것은 금지한다. 안전 확인, 네트워크 안정성, 이해 가능성, 연출 pacing처럼 명시된 목적이 있을 때만 `TEST_REQUIRED`로 검토한다.

## 9. 복잡성·견고성·단순성

- `SHOULD` **Tesler**: 제거할 수 없는 복잡성은 시스템이 흡수할 수 있는지 검토하되, 사용자가 제어·이해해야 하는 중요한 선택까지 숨기지 않는다.
- `SHOULD` **Postel**: 입력 변형은 관대하게 수용하고 출력은 일관되게 한다. 보안, validation schema, 경제/결제, 저장 포맷의 경계를 넘지 않는다.
- `SHOULD` **Occam**: 같은 목표를 달성하는 해결책 중 불필요한 가정·컴포넌트·장식을 줄인다.
- `SHOULD` **Pareto**: 실제 사용 데이터가 있으면 빈번·가치 높은 소수 흐름에 polish/접근성/성능 투자를 우선한다. “80/20”을 측정 없는 사실로 쓰지 않는다.
- `TEST_REQUIRED` **Parkinson**: 명확한 범위·시간 frame은 흐름을 돕지만 countdown/urgency를 인위적으로 만들어 압박하지 않는다.

---

# Part D. 접근성·플랫폼 — 숫자는 단위와 적용 범위를 보존한다

## 10. Web/WCAG 2.2 baseline

### `MUST` — Web surface가 WCAG 2.2 AA를 목표로 할 때

- 일반 텍스트 대비: **4.5:1** 이상, large text는 **3:1** 이상.
- 의미 있는 비텍스트 UI/그래픽 대비: 적용되는 SC 1.4.11 범위에서 **3:1**.
- pointer target: SC 2.5.8에서 원칙적으로 **24×24 CSS px** 이상 또는 규정된 spacing/equivalent/inline 등 예외 조건을 충족.
- text는 assistive technology 없이 **200%**까지 확대해도 콘텐츠·기능 손실이 없어야 한다.
- focus가 가려지지 않고, keyboard navigation이 기능을 완주해야 한다.
- 의미를 색상만으로 전달하지 않는다.

**보정:** WCAG의 24×24 CSS px를 모바일·게임 HUD의 “권장 크기”로 오해하지 않는다. 이는 특정 성공 기준의 최소 floor이며 플랫폼 권고는 더 클 수 있다.

## 11. Apple touch profile

- `SHOULD` iOS/iPadOS 일반 hit target은 **44×44 pt** 이상을 출발점으로 한다.
- 버튼 사이 spacing과 press state를 명확히 한다.
- macOS/tvOS/watchOS/visionOS는 각 플랫폼 HIG 수치를 별도로 확인한다. iPhone 값을 전역 복제하지 않는다.

## 12. Android touch profile

- `SHOULD` touch target은 **48×48 dp** 이상을 출발점으로 한다.
- 보이는 icon이 작아도 padding/semantics로 실제 touch region을 확장할 수 있다.
- mouse/trackpad 같은 precise pointer surface는 별도 profile로 검토한다.

## 13. 게임/Xbox 접근성 profile

**MUST/SHOULD를 프로젝트 지원 범위에 맞게 적용:**

- `controller focus`: 현재 focus가 항상 뚜렷하고 offscreen/hidden control로 이동하지 않는다.
- `remapping`: 지원 입력은 가능한 한 재매핑/대체 입력을 검토하고, UI는 복수 동시 입력을 불필요하게 강요하지 않는다.
- `subtitles/captions`: 중요한 음성/비음성 audio cue를 동등하게 이해할 경로를 제공하고, 배경·크기·opacity·위치 설정과 preview를 검토한다.
- `TV 거리`: PC 책상 거리의 글자 크기/대비를 TV couch distance에 그대로 적용하지 않는다.
- 중요 HUD/text/targets는 실제 배경이 계속 변하는 gameplay에서도 읽히도록 outline/background/high-contrast option을 검토한다.
- `FOV`, `camera movement`, sensitivity, camera shake, scrolling/blinking/auto-updating visual은 motion sickness·주의 장벽을 줄일 설정을 검토한다.
- `Reduced Motion`, mute, haptic-off에서 핵심 정보·규칙 결과·다음 행동이 유지된다.
- 중요한 상태를 **색상만**으로 전달하지 않는다.

---

# Part E. 타이포그래피·레이아웃·색·깊이 — STYLE_DEFAULT로 관리

## 14. 타이포그래피

### `STYLE_DEFAULT`

- UI는 하나의 읽기 쉬운 sans-serif를 기본으로 시작하고, 컨셉 강화가 명확할 때 최대 2개 서체를 검토한다. **최대 2개 서체**는 미감 기본값이지 접근성 표준이 아니다.
- regular/bold 중심으로 weight system을 단순하게 시작한다. semibold 등은 hierarchy와 locale에서 필요하면 사용한다.
- 장문은 언어의 자연스러운 reading edge에 정렬한다. 영어식 left-align 규칙을 RTL 언어에 그대로 강제하지 않는다.
- full uppercase는 짧은 label/강조 외에는 제한한다.
- 큰 x-height와 충분한 glyph 구분이 작은 UI text에 유리한지 검토한다.
- 웹 body **16px** 이상은 유용한 시작점이지만 전역 game font minimum이 아니다. 실제 DPI·TV 거리·해상도·locale·사용자 scale을 검증한다.
- 본문 line-height 1.5 전후를 읽기 좋은 시작점으로 쓰되, font metrics와 한글/일본어/중국어 등 script에 맞게 조정한다.
- line length는 대략 **70자**(약 60~80자 범위)를 장문 Web/문서의 시작점으로 검토하되 HUD·표·좁은 panel에 강제하지 않는다.
- display text가 커질수록 letter/line spacing을 상대적으로 줄이는 접근은 optical 검증 후 사용한다.

## 15. 색과 대비

### `MUST`

- 접근성 contrast requirement가 `STYLE_DEFAULT`보다 우선한다.
- 인터랙션·상태·오류를 색상 하나로만 구분하지 않는다.

### `STYLE_DEFAULT`

- pure black/white 대신 **near-black / near-white**로 시작하면 장시간 사용에서 덜 거칠 수 있다. 단 필요한 contrast를 잃으면 즉시 철회한다.
- neutral에 아주 낮은 saturation을 더해 palette 일관성을 만들 수 있다. warm/cool neutral 체계는 하나의 방향으로 시작하되 프로젝트 아트 방향이 우선이다.
- 중요 content/action은 높은 contrast, divider/shadow 같은 구조 요소는 낮은 visual weight로 시작한다.
- palette color는 hue뿐 아니라 brightness/value 차이도 검토해 서로 경쟁하지 않게 한다.
- 장식용 brand color보다 interaction/status의 의미 전달을 먼저 정의한다.

## 16. spacing·grid·alignment

### `SHOULD`

- 관련 요소는 proximity/alignment로 묶고, container는 관계를 더 강하게 보여줘야 할 때 사용한다.
- 모든 요소는 의도된 alignment/anchor 관계를 가져야 한다.
- semantic reading order와 keyboard/controller focus order는 visual weight ordering보다 우선한다.

### `STYLE_DEFAULT`

- spacing과 size는 **8 기반** 등 일관된 scale에서 시작한다. 4/8/12/16/24/32처럼 프로젝트가 선택한 scale을 token화한다.
- `optical alignment`가 mathematical center보다 자연스러운 icon/shape는 눈으로 보정하되 token/exception 근거를 남긴다.
- Web marketing/application grid에서 **12-column**은 유연한 시작점이다. 모바일, HUD, radial UI, split-screen, TV UI에 전역 강제하지 않는다.
- container outer padding은 내부 item gap과 같거나 크게 시작하면 grouping이 명료한 경우가 많다.
- high-contrast edge 사이의 실제 지각 spacing을 검토한다.

## 17. shape·border·depth

### `STYLE_DEFAULT`

- nested radius는 외부 radius와 inset 관계를 고려해 시각적으로 자연스럽게 맞춘다. 단 exact subtraction은 모든 shape의 법칙이 아니다.
- border는 container와 주변 배경 양쪽에서 구분돼야 한다.
- 인접한 hard divide(배경 전환+border+divider)를 중복해 시각적 소음을 만들지 않는다.
- 하나의 surface에서 depth 기법을 일관되게 사용한다.
- `shadow` blur를 offset의 약 2배로 시작하는 방법은 시각 휴리스틱일 뿐 물리 법칙이 아니다.
- dark UI에서 shadow가 읽히지 않으면 border/value shift/overlay 등 다른 depth cue를 우선 검토한다.
- **container brightness** 차이 12%(dark)/7%(light) 같은 값은 특정 웹 관찰 기반 휴리스틱이므로 `TEST_REQUIRED` 없이 접근성 또는 게임 UI 상수로 승격하지 않는다.

## 18. visual hierarchy와 복잡도

- `SHOULD` squint test/blur test에서 화면 목적, primary action, critical state의 우선순위가 남는지 본다.
- `SHOULD` 같은 기능은 같은 형태·동작을 유지하고, 같은 모양인데 기능이 다르면 구분한다.
- `SHOULD` 장식이 의미·grouping·brand promise를 전달하지 못하면 제거한다.
- `STYLE_DEFAULT` simple foreground + complex background 또는 complex foreground + simple background로 시작한다. complex-on-complex는 실제 readability 검증이 필요하다.
- `STYLE_DEFAULT` visual weight가 큰 요소를 흐름 바깥 edge에 두는 구성은 미감 기본값일 뿐 semantic/focus order를 바꾸지 않는다.
- `STYLE_DEFAULT` button horizontal padding을 vertical padding보다 크게 두어 button affordance를 만든다. 정확히 2배는 강제 상수가 아니다.

---

# Part F. 적용·검증 프로토콜

## 19. 프로젝트 Rule Profile

각 프로젝트는 필요한 규칙만 아래 형식으로 채택한다.

```yaml
rule_id:
source_type: normative | platform | usability_heuristic | visual_heuristic
tier: MUST | SHOULD | STYLE_DEFAULT | TEST_REQUIRED
platform: web | ios | android | pc | console | tv | gamepad | touch | mixed
project_decision: ADOPT | ADAPT | AVOID | TEST | IGNORE
exception_reason:
equivalent_path:
verification:
evidence_status: NOT_RUN | PARTIAL | PASSED | FAILED | BLOCKED
```

## 20. 적대적 검토 순서

```text
1. 이 규칙이 실제 문제를 해결하는가?
2. 규범 표준인가, 플랫폼 권고인가, 휴리스틱인가?
3. 단위·플랫폼·입력·거리·언어를 보존했는가?
4. 프로젝트 코어·아트 방향과 충돌하는가?
5. 접근성·semantic·focus/read order를 약화시키는가?
6. 심리 원칙이 다크 패턴/압박/기만으로 변질되는가?
7. 자동 점수나 contrast 숫자가 실제 사용성을 과장하는가?
8. 최소 해상도·긴 한국어·최대 수치·빈/오류/locked 상태에서 버티는가?
9. pointer·keyboard·controller·touch 중 선언한 경로를 완주하는가?
10. 실제 렌더·실기기·사람 이해 증거가 필요한 항목을 TEST_REQUIRED로 남겼는가?
```

## 21. 완료 조건

- `MUST` 위반 0 또는 승인된 exception + 동등 경로 + 검증이 있다.
- `SHOULD` 미적용은 프로젝트 코어·장르·입력·비용 근거가 있다.
- `STYLE_DEFAULT`는 토큰/아트 방향에 흡수되고 접근성보다 높은 권한을 갖지 않는다.
- `TEST_REQUIRED`는 미검증이면 `NOT_RUN/BLOCKED`를 유지한다.
- 자동 검사, 전문가 리뷰, 실제 사용자/플레이어 검증 결과를 분리한다.

---

# Sources and provenance

## 공식·플랫폼

- W3C WCAG 2.2: https://www.w3.org/TR/WCAG22/
- W3C Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Apple Human Interface Guidelines — Accessibility: https://developer.apple.com/design/human-interface-guidelines/accessibility/
- Apple UI Design Tips: https://developer.apple.com/design/tips/
- Android Developers — Accessibility: https://developer.android.com/guide/topics/ui/accessibility/apps.html
- Xbox Accessibility Guidelines: https://learn.microsoft.com/en-us/xbox/accessibility/guidelines

## 인지·사용성

- Laws of UX: https://lawsofux.com/
- Nielsen Norman Group 10 Usability Heuristics: https://www.nngroup.com/articles/ten-usability-heuristics/

## 시각 디자인 실무 휴리스틱

- Anthony Hobday, Visual design rules you can safely follow every time: https://anthonyhobday.com/sideprojects/saferules/
- Adham Dannaway, 16 little UI design tips that make a big impact: https://www.adhamdannaway.com/blog/ui-design/ui-design-tips

## 사용자 제공 자료

- 2026-08-10 사용자 제공 Laws of UX 요약, Anthony Hobday 규칙 요약, Adham Dannaway UI tips 요약.
- 2026-08-10 사용자 제공 GUI 기본 요소/86개 지침 요약: 버튼·폼·메뉴·링크·대화상자·알림·아이콘·선택 컨트롤·탭·검색 및 창/스크롤·포인터/커서.

외부 요약은 출발점이며, 충돌 시 공식 원문·프로젝트 실제 조건·검증 증거를 우선한다.
