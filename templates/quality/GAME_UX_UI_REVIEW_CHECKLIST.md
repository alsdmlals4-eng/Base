# 게임 UX/UI 검토 체크리스트

## 1. 계약과 범위

- [ ] 플레이어 가치와 화면별 중심 질문이 기능 목록보다 먼저 정의됐다.
- [ ] 포함·제외·보호 대상과 상태 소유자가 명시됐다.
- [ ] 프로젝트 코어·수치·저장·보상을 UI가 재계산하지 않는다.
- [ ] 외부 레퍼런스가 정본이나 구현 사실로 사용되지 않는다.
- [ ] 실제 최소·목표 해상도와 입력 장치가 선언됐다.

## 2. 사용자 여정·정보 구조

- [ ] 진입·정상·취소·실패·복귀 경로가 있다.
- [ ] 한 화면의 중심 질문과 첫 시선이 명확하다.
- [ ] 핵심 결정 화면에서 `현재 상황 / 무엇을 선택할 수 있는가 / 선택에 필요한 정보 / 비용·위험·결과`가 읽힌다.
- [ ] 의도적으로 숨긴 정보가 있어도 플레이어의 행동 목적과 선택 가능성을 숨기지 않는다.
- [ ] 상시 정보, 선택 상세, 실행 전 예상, 실행 후 결과·복기가 분리됐다.
- [ ] 점진 공개가 핵심 기능을 숨기거나 기존 저장을 회귀시키지 않는다.
- [ ] 복귀 플레이어가 현재 목표·최근 변화·다음 행동을 재확인할 수 있다.

## 3. 상호작용·상태·피드백

- [ ] 입력 접수, 처리 중, 성공, 실패가 구분된다.
- [ ] 비용·위험·조건·불확실성을 실행 전에 확인할 수 있다.
- [ ] 비교 선택지는 같은 위치·단위·축으로 표시된다.
- [ ] normal/hover/focused/pressed/selected가 혼동되지 않는다.
- [ ] disabled·locked·loading·warning·error·new 중 필요한 상태가 있다.
- [ ] 비활성·잠금·오류의 원인과 가능한 다음 행동이 있다.
- [ ] 파괴적 행동은 되돌리기 가능성과 확인 강도를 구분한다.
- [ ] 결과 인과가 연출을 건너뛰어도 로그·텍스트·수치로 남는다.

## 3A. GUI 의미 문법

- [ ] **버튼과 링크**를 섞지 않았다: 행동/상태 변경은 버튼, 목적지 이동은 링크·탐색 패턴을 우선한다.
- [ ] 버튼·확인 UI가 `OK`, `Submit` 같은 추상어보다 결과 중심 문구를 사용한다.
- [ ] placeholder가 지속 label을 대체하지 않는다.
- [ ] 폼 오류가 문제 위치·원인·복구 행동을 알려주고 기존 입력을 보존한다.
- [ ] **체크박스·라디오·토글**의 의미가 구분된다: 독립/복수 선택, 상호배타 단일 선택, 즉시 적용 설정.
- [ ] modal은 실제 차단이 필요한 결정에만 쓰며, 되돌릴 수 있는 행동은 실행 취소를 먼저 검토했다.
- [ ] icon-only control은 보편적으로 학습된 소수이거나 label/accessible name/tooltip을 제공한다.
- [ ] tab을 순차 wizard나 비교해야 하는 데이터를 숨기는 용도로 쓰지 않았다.
- [ ] 중요한 기능의 유일한 접근 수단이 hover가 아니다.
- [ ] scroll hijacking, 숨은 focus, 장식 요소의 거짓 pointer affordance가 없다.

## 4. UI 폴리싱 게이트

- [ ] 폴리싱 준비도에서 기능 흐름·정보 구조·상태 소유권·입력 baseline이 확인됐다.
- [ ] `P0 BLOCKER`와 `P1 CLARITY`, `P2 CONSISTENCY`가 해결되거나 명시적으로 차단되기 전 `P3 DELIGHT` 장식을 우선하지 않았다.
- [ ] 새 요소 추가 전에 `REMOVE → REDUCE → MERGE → CLARIFY → FEEDBACK → ADD`를 검토했다.
- [ ] routine·confirming·warning·reward·critical의 피드백 예산이 행동 중요도와 반복 빈도에 맞는다.
- [ ] 자주 반복되는 행동이 희귀 보상·위험 경고보다 강한 모션·음향·햅틱을 사용하지 않는다.
- [ ] 시각·음향·햅틱이 같은 원인과 결과를 전달하며 하나의 채널에만 의미를 의존하지 않는다.
- [ ] `reduced motion`, mute, haptic off에서도 같은 상태·결과·다음 행동이 남는다.
- [ ] 빠른 반복 입력·중복 입력에서 구매·보상·저장·전환 결과가 중복되지 않는다.
- [ ] 애니메이션 중단·즉시 완료·재진입에서 누적 transform, 포커스 손실, 입력 지연이 없다.
- [ ] modal 종료·화면 재진입 뒤 이전 의미 있는 선택과 포커스가 복구된다.
- [ ] 반복 사용에서 효과 피로·조작 지연·Signal/Tween/Timer 누적 위험을 검토했다.
- [ ] 전후 Artifact가 같은 build·상태·해상도·입력·locale·접근성 설정을 사용한다.
- [ ] 폴리싱이 미확정 코어·정보 구조·도메인 규칙 문제를 가리지 않는다.

## 4A. 외부 UI 조달·시각 품질 Gate

- [ ] 현재 프로젝트가 Godot 전용인지 Web UI 코드가 실제로 필요한지 먼저 판정했다.
- [ ] Registry/MCP의 공식 출처, exact version/commit, item, source hash와 license 근거를 기록했다.
- [ ] dependency·script/postinstall·secret·network·추가/교체 파일을 설치 전에 검토했다.
- [ ] MCP 연결 성공이나 Registry 조회 성공을 설치 승인으로 해석하지 않았다.
- [ ] 일회성 격리 fixture의 조달·빌드 결과와 실제 프로젝트 설치 결과를 분리했다.
- [ ] 실제 프로젝트 Theme·컴포넌트·상태 책임과의 중복·충돌을 확인했다.
- [ ] `Design Read`와 프로젝트 시각 토큰을 기준으로 generic card grid, AI-purple glow, 무목적 glass·gradient·motion 반복을 실제 렌더에서 검사했다.
- [ ] keyboard/focus, disabled/error/loading, reduced motion, 긴 한국어, 최소 해상도와 접근성을 실제 렌더·입력으로 확인했다.
- [ ] rollback 경로가 있고, 미검증이면 `BLOCKED_UNVERIFIED`로 유지했다.

## 4B. 생성형 visual scope·deliverable Gate

- [ ] `VISUAL_TASK_SCOPE_FIDELITY`: 생성 전에 `visual_question / target_screen / target_state / excluded_scope`를 고정했고, broad dashboard·unrelated screen·undeclared state를 같은 deliverable의 PASS로 세지 않았다.
- [ ] `BATCH_COUNT_MEANS_INDEPENDENT_DELIVERABLES`: N개 결과 요청을 N개의 독립 검토·교체·배치 가능한 deliverable로 검증했고, collage는 요청·명시 승인된 경우에만 동등하게 셌다.
- [ ] `DECISION_CRITICAL_VISUAL_SEMANTIC_REDUNDANCY`: 중요한 경로·선택·잠금·상태가 art/background와 경쟁할 때 style replacement, color/intensity-only, identity-preserving independent cues를 비교했다.
- [ ] semantic cue를 특정 색·화살표·두께 같은 Base 전역 상수로 고정하지 않았다.
- [ ] repository contract, mock, screenshot, Notion readback을 실제 `human comprehension`, 접근성, runtime/device correctness PASS로 승격하지 않았다.

## 5. 접근성

- [ ] 중요한 의미가 색 하나에만 의존하지 않는다.
- [ ] 중요한 의미가 소리 하나에만 의존하지 않는다.
- [ ] 중요한 의미가 모션 하나에만 의존하지 않는다.
- [ ] 선언한 입력 장치마다 핵심 흐름을 완주할 수 있다.
- [ ] 포커스 시작·이동·modal·복귀 순서가 시각 순서와 일치한다.
- [ ] 숨김·비활성 항목에 포커스가 갇히지 않는다.
- [ ] 긴 한국어·최대 수치·확대 텍스트에서 핵심 정보가 잘리지 않는다.
- [ ] 모션 감소·음향 끄기·자산 누락이 규칙 결과를 바꾸지 않는다.
- [ ] 시간 제한·반복 입력·정밀 입력에는 필요한 대체 경로가 있다.

## 5A. 플랫폼 수치·접근성 오용 방지

- [ ] Web/WCAG 2.2를 목표로 하는 surface는 일반 텍스트 4.5:1, large text 3:1, 적용되는 비텍스트 UI 3:1 대비 기준을 확인했다.
- [ ] Web pointer target의 **24×24 CSS px** 최소 기준과 예외를 플랫폼 범위 안에서 해석했다.
- [ ] Apple touch surface는 **44×44 pt**, Android touch surface는 **48×48 dp** 권고를 각각의 단위로 검토했다.
- [ ] 서로 다른 target size 기준을 하나의 전역 px 상수로 합치지 않았다.
- [ ] Web 200% text resize 같은 웹 성공 기준을 게임 UI의 단일 font-size 상수로 오해하지 않았다.
- [ ] controller focus가 항상 보이고 offscreen/hidden control로 이동하지 않는다.
- [ ] 프로젝트가 지원하는 입력에서 remapping 또는 동등 경로가 필요한지 검토했다.
- [ ] subtitles/captions가 중요한 audio cue의 동등 경로를 제공하고 크기·배경·opacity·위치 설정을 검토했다.
- [ ] TV 거리, handheld 거리, desktop 거리의 글자·대비·HUD 판단을 같은 기준으로 합치지 않았다.
- [ ] FOV, camera movement/shake, scrolling/blinking/auto-updating visual에 motion 장벽 완화 옵션이 필요한지 검토했다.

## 5B. UX 심리 법칙 윤리·범위 Gate

- [ ] Hick/Fitts/Jakob/Choice Overload/인지 부하/작업 기억을 문제 설명과 가설에 사용했으며 장르의 핵심 복잡성을 무조건 삭제하지 않았다.
- [ ] **Miller의 7±2**를 메뉴 항목 수의 하드 제한으로 사용하지 않았다.
- [ ] Goal-Gradient나 Zeigarnik을 **허위 진행**, 강박적 badge, 취소 방해에 사용하지 않았다.
- [ ] Peak-End를 중간 구간의 지속적 불편을 감추는 근거로 사용하지 않았다.
- [ ] Doherty/perceived performance를 **의도적 지연**의 일반 정당화로 사용하지 않았다.
- [ ] Postel의 관대한 입력 처리가 보안·schema·결제·저장 포맷 경계를 침범하지 않는다.
- [ ] 심리 원칙이 다크 패턴, 숨은 비용, 기만적 희소성, 강제 연속 사용으로 변질되지 않았다.

## 5C. 비주얼 STYLE_DEFAULT Gate

- [ ] near-black/near-white, tinted neutral, 8 기반 spacing scale 등은 승인 아트 방향과 접근성을 보조하는 `STYLE_DEFAULT`로만 사용했다.
- [ ] **12-column**을 Web용 유용한 시작점 이상으로 해석해 HUD·mobile·TV·radial UI에 강제하지 않았다.
- [ ] body **16px**를 게임 전체 font minimum으로 고정하지 않고 DPI·거리·locale·사용자 scale을 검증했다.
- [ ] 장문 **70자** line length를 HUD·표·좁은 panel까지 기계적으로 강제하지 않았다.
- [ ] shadow blur/offset, container brightness, nested radius의 경험적 수치를 물리 법칙이나 접근성 표준으로 승격하지 않았다.
- [ ] optical alignment를 적용해도 semantic reading order와 keyboard/controller focus order가 깨지지 않는다.
- [ ] visual weight 순서가 실제 행동 순서·접근성 순서보다 높은 권한을 갖지 않는다.
- [ ] 색상·border·shadow·gradient·motion을 추가한 이유를 화면 중심 질문 또는 아트 방향으로 설명할 수 있다.
- [ ] squint/blur test에서 primary action, critical status, 주요 content가 여전히 구분된다.

## 6. Godot 구현 경계

- [ ] 기존 Theme·Scene·Container·레이아웃·편집 시스템을 먼저 조사했다.
- [ ] UI는 View Data를 받고 사용자 의도를 `Signal`/Command로 반환한다.
- [ ] 도메인 계산과 권위 상태는 UI 밖에 있다.
- [ ] 반복 의미가 있는 최소 단위만 재사용 Scene으로 분리했다.
- [ ] Theme type/variation과 semantic token이 화면별 복제를 줄인다.
- [ ] 수동 좌표는 의도와 검증 조건이 있을 때만 사용한다.
- [ ] animation 완료가 규칙 처리의 권위 시점이 아니다.

## 7. 자동·정적 증거

- [ ] Markdown·JSON·Schema·참조 경로 검사 결과가 있다.
- [ ] 정적 UI 스캔 결과는 `CANDIDATE`로만 취급했다.
- [ ] Godot parse/import와 관련 테스트 결과가 분리돼 있다.
- [ ] 변경된 파일뿐 아니라 untouched 소비자·Template·Test를 확인했다.
- [ ] 제품 코드·Scene·데이터가 범위 밖이면 diff 0건을 확인했다.

## 8. 런타임 증거

- [ ] 최소·목표 해상도 실제 렌더가 있다.
- [ ] 정상·빈 상태·잠금·오류·누락 자산 fixture를 확인했다.
- [ ] 포인터·키보드·게임패드·터치 중 선언한 경로를 실제 입력으로 확인했다.
- [ ] modal, 취소, 뒤로, 포커스 복귀를 확인했다.
- [ ] 모션 감소·음향 끄기·빠른 재생/즉시 완료를 확인했다.
- [ ] 전후 렌더와 회귀 비교가 있다.

## 9. 사람 이해 증거

자동 검사는 **사람 이해**를 대체하지 않는다.

- [ ] 정확한 build·commit·해상도·입력 장치가 기록됐다.
- [ ] 참가자 경험과 프로젝트 사전 노출이 기록됐다.
- [ ] 정답을 암시하지 않은 과제와 우선 가설 하나가 있다.
- [ ] 행동 증거와 설명 증거를 함께 수집했다.
- [ ] 플레이어가 중심 질문과 다음 행동을 설명한다.
- [ ] 비용·위험·결과를 실행 전에 설명한다.
- [ ] 실패 원인과 복구를 도움 없이 수행한다.
- [ ] 결과 원인과 다음에 바꿀 전략을 설명한다.
- [ ] 실제 보조기기·장애 사용자 검증 여부를 분리했다.

사람 플레이를 실행하지 않았으면 상태는 `HUMAN_NOT_RUN`이다. 자동 검사, 전문가 리뷰, 접근성 API 노출만으로 `PASSED`로 바꾸지 않는다.

## 10. 적대적 검토

- [ ] 이 화면이 실패했다고 가정하고 오해·오입력·누락·악용·경계 실패를 공격했다.
- [ ] 비판의 사실성·발생 가능성·영향·범위·수정 비용을 재검증했다.
- [ ] 취향·과잉 요구·잘못된 전제는 `REJECTED_CRITIQUE`로 분리했다.
- [ ] 기획 방향 변경은 `USER_DECISION_REQUIRED`로 분리했다.
- [ ] 검증된 `MUST_FIX`와 승인된 `SHOULD_FIX`만 최소 수정했다.
- [ ] 수정 뒤 코어·정상 경로·입력·폴백·새 결함을 다시 공격했다.
- [ ] 규범 표준, 플랫폼 권고, 인지/사용성 휴리스틱, 시각 `STYLE_DEFAULT`의 증거 강도를 바꿔치기하지 않았다.

## 11. 최종 판정

```yaml
contract: PASS | PARTIAL | FAIL | BLOCKED
static_validation: PASS | PARTIAL | FAIL | NOT_RUN
runtime_validation: PASS | PARTIAL | FAIL | NOT_RUN
human_validation: PASSED | PARTIAL | FAILED | HUMAN_NOT_RUN
accessibility_user_validation: PASSED | PARTIAL | FAILED | HUMAN_NOT_RUN
remaining_must_fix:
remaining_risks:
rollback:
next_gate:
```

## UI 모션·상호작용 검수

- [ ] 모션 목적과 상태 변화가 명확하다.
- [ ] 입력 접수·처리 중·실제 결과가 구분된다.
- [ ] AnimationPlayer·Tween이 도메인 상태 권위를 소유하지 않는다.
- [ ] 중단·즉시 완료·빠른 반복·재진입에서 결과 중복과 transform drift가 없다.
- [ ] Reduced Motion·mute·haptic-off에서 핵심 정보와 결과가 유지된다.
- [ ] 목표 해상도·긴 한국어·성능·전후 증거를 실제로 검사했다.
