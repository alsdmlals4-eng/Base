# Godot·Web UI 아트 fixture 전후 시각 검수

## 목적과 범위

`auditing-and-refining-ui-art`의 A~E 감사가 정적 후보 수집에 그치지 않고 실제 Web·Godot 렌더와 함께 검수되는지 확인한다. 이 fixture는 제품 아트 승인이 아니라 검사 계약의 대표 증거다.

## 실행 환경

- 운영체제: Windows
- Web 렌더: Google Chrome headless, 1280×720
- Godot 렌더: Godot 4.7.1 stable, Compatibility/OpenGL 3.3, 숨김 창 실행
- Godot headless 주의: dummy rendering driver에서는 viewport texture가 생성되지 않아 시각 캡처가 불가능했다. 기존 프로세스나 산출물을 건드리지 않고 해당 실행을 종료한 뒤 숨김 창의 실제 렌더러로 재실행했다.
- 정적 감사: `scan_ui_art_signals.py`, Godot/Web 어댑터

## 추적 자산

| 플랫폼 | 상태 | 렌더 | SHA-256 |
|---|---|---|---|
| Web | before | `tests/fixtures/ui-art/render/web/before/render.png` | `bd61757f580cdfb80574cff633bf4e146b9a66e1e69a59d6ba1f89ee010faf81` |
| Web | after | `tests/fixtures/ui-art/render/web/after/render.png` | `e0c4330edb55c9bff37930a950e49a43aabac4f0c9419afc4858cb35733a672d` |
| Godot | before | `tests/fixtures/ui-art/render/godot/before/render.png` | `1ea18c5de172b03597c2fbc9dbe1bd873d92f487a9ebb4e196f69ed257f34851` |
| Godot | after | `tests/fixtures/ui-art/render/godot/after/render.png` | `70bb7355760ee92a51482e51fbd8e65ef46350316ce1c53c90b812e97997fd63` |

Findings 원본은 `docs/audits/evidence/ui-art/`의 플랫폼·상태별 JSON과 Markdown에 있다.

## 정적 결과와 해석

| 플랫폼 | before 후보 | after 후보 | 판정 |
|---|---:|---:|---|
| Web | 25 | 2 | A~D의 반복 장식·고정 구조·불규칙 간격·타입 효과가 제거됐다. after의 색상 literal 2건은 CSS 변수 선언으로, 상태 체계의 책임 원본이므로 수동 검수에서 보존한다. |
| Godot | 41 | 29 | Container 구조와 시각 계층은 개선됐다. remaining 후보 대부분은 root Margin의 해상도 제약과 Theme 색상 override로, 정적 패턴만으로 결함 확정할 수 없음을 보여주는 의도적 사례다. |

후보 수만으로 품질 통과를 선언하지 않았다. 특히 Godot의 offset은 anchor 기반 Margin 제약에 필요하고, 색상 literal은 fixture에 별도 Theme 자산을 두지 않은 제한된 시각 계약이다.

## 전 페이지 Codex 시각 검수

네 렌더를 원본 해상도로 처음부터 끝까지 직접 확인했다.

### Web

- before: 보라색 그라디언트·글로우·유리 표면과 반복 카드가 정보 우선순위를 평준화한다. 작은 회색 본문, 이탤릭 대형 제목, 장식 eyebrow와 emoji가 판독보다 표면 스타일을 앞세운다.
- after: 제목 → 상태 → 세 단계 → 다음 행동의 읽기 순서가 분명하다. 황색은 문맥·경계·단계·행동에 일관되게 쓰이며, 카드 설명과 버튼이 1280×720에서 잘리거나 겹치지 않는다.
- 남은 확인: 키보드 포커스와 760px 이하 반응형 규칙은 소스에 있으나 이번 정지 이미지 한 장만으로 실제 상호작용을 통과 처리하지 않는다.

### Godot

- before: 보라색 표면 안에 같은 크기의 카드가 반복되고 부제 대비가 낮다. 버튼의 emoji와 고정 좌표가 정보 구조보다 장식·배치를 앞세운다.
- after: Container가 세 단계의 동일 규격을 유지하고 제목·경계 상태·다음 행동을 분리한다. 한글 글리프, 줄바꿈, 여백, 선, 버튼이 1280×720에서 잘림·겹침 없이 렌더된다.
- 첫 after 렌더에서 버튼 글자가 어두운 기본 Button 표면과 충돌하는 결함을 실제 시각 검수로 발견했다. 승인된 황색 `StyleBoxFlat`을 적용해 재렌더했고 현재 해시의 화면에서 대비와 행동 우선순위가 복구됐음을 확인했다.
- 남은 확인: 키보드·게임패드 focus, hover·pressed·disabled 상태와 다른 stretch 해상도는 정지 이미지로 통과 처리하지 않는다.

## 최종 판정

- [검증] Godot/Web before·after 실제 렌더 생성
- [검증] 네 이미지 전부 Codex 직접 시각 검수
- [검증] 정적 검사가 소스 파일을 수정하지 않고 JSON·Markdown 후보만 생성
- [검증] after를 새 검사 호출로 재감사
- [검증] 정적 후보가 남아도 목적과 실제 렌더를 대조해 보존 가능
- [미검증] 실제 제품 UI의 입력 상태·다중 해상도·사용자 사람 검수

이 검수는 정적 패턴을 자동 삭제 규칙으로 사용하지 않고, 실행 결과와 승인된 의도를 완료 근거로 삼는 스킬 계약을 증명한다.
