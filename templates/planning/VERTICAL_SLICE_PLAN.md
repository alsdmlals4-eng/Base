# Vertical Slice 통합 데모 계획

## 0. Release-near 플레이 검증 계약

```yaml
RELEASE_NEAR_VERTICAL_SLICE_FIRST: REQUIRED
GAMEPLAY_VALIDATION_REQUIRES_SHIPPING_INTENT_SLICE: REQUIRED
SHIPPING_INTENT_UI_IMAGE_AUDIO_VFX_SYSTEM_REQUIRED: REQUIRED
SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE: REQUIRED
TECHNICAL_SPIKE_INTERNAL_ONLY: REQUIRED
EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT: REQUIRED
PLAYER_APPEAL_QUALITY_GATE: REQUIRED
```

플레이어 경험을 판단하는 Slice는 실제 게임 사용 후보인 **UI/UX · 이미지/아트 · 애니메이션/연출 · 사운드 · VFX/피드백 · 핵심 시스템/데이터/콘텐츠**를 한 짧은 흐름으로 완성한 뒤 테스트한다. 플레이어가 접하는 경로에 임시 `player-facing placeholder`나 dummy presentation을 남기지 않는다. 시스템-only PoC는 기술 질문에만 쓰며 재미·몰입·가독성·첫인상·판매력·감정·기억을 PASS 처리하지 않는다.

### Player Appeal Quality Gate
- 독창성·차별점: 왜 유사 게임 대신 이 게임을 선택하는가?
- DDD: 행동→피드백→보상 지연과 명료성이 핵심 경험을 강화하는가?
- 일관성: UI·이미지·사운드·VFX·세계관·시스템이 같은 방향을 가리키는가?
- 복잡성: 플레이어 고민을 만들지 않는 설명/규칙/버튼을 제거했는가?
- 난이도: 도전이 공정하고 읽을 수 있으며 접근 가능한가?
- 개성·기억: 첫인상과 대표 순간에 프로젝트만의 성격이 남는가?
- 인간 플레이 증거: 실제 플레이 전 재미·몰입 판정은 `NOT_RUN`인가?


## 상세 계약 라우팅

현재 작업에 필요한 문서만 읽는다.

- 4단계 Gate·PC/모바일 통합 데모: `docs/knowledge/vertical-slice/INTEGRATED_DEMO_STAGE_GATES.md`
- Skill 오케스트레이션·Grill Me·적대적 검토·완전성 증거: `docs/knowledge/vertical-slice/SKILL_ORCHESTRATION_AND_EVIDENCE.md`
- 에셋·UI·UX·사운드·마스코트·수치 조정: `docs/knowledge/vertical-slice/ASSET_MASCOT_AND_TUNING.md`
- 기본 실행·GitHub Handoff: `docs/ONE_CLICK_PLAY_HANDOFF_POLICY.md`

## 0. 상태와 실행 계약

- 프로젝트:
- 플랫폼: PC / MOBILE
- 제품 단계: `DEMO_FIRST_VERTICAL_SLICE` (`PROTOTYPE_AND_VERTICAL_SLICE`는 과거 호환 이름)
- Work Mode: PLAN / BUILD / REVIEW
- 실행 프로필:
- 기준 Branch·Commit:
- 책임 원본:
- 보호할 결정·자산:
- `BLOCKED_UNVERIFIED`:

## 0.1 One-click Project Play 계약

- 기본 프로젝트 파일:
- 기본 entrypoint:
- 실행 동작: `Project Play`
- 기대 첫 화면:
- 실제 gameplay surface:
- 대표 성공·실패·복귀 흐름:
- 핵심 HUD·도구·입력 표면:
- 별도 Scene 선택 필요 여부: `없음`이어야 함
- 편집기 수동 설정 필요 여부: `없음`이어야 함
- validation·debug 전용 entrypoint:
- 기본 실행 자동 boot·flow 테스트:
- 실제 로컬 실행 상태: `NOT_RUN / PASS / FAIL · RETEST_REQUIRED / BLOCKED`

최종 인계 상태에서는 사용자가 별도 Scene 선택이나 editor 설정 없이 프로젝트를 열고 **Project Play**만 눌러 대표 데모의 첫 화면부터 실제 플레이, 성공·실패·복귀까지 진행할 수 있어야 한다. 테스트 Scene 전용 실행은 개발 중간 증거로 사용할 수 있지만 최종 사용자 검수 경로를 대체하지 않는다.

## 1. Gate 1 입력

- 플레이어 약속:
- 목표 플레이어와 플레이 상황:
- 프로젝트 코어·비타협 조건:
- 변경 가능한 외피:
- 뾰족한 재미:
- Core Loop:
- 세일즈포인트 최대 3개:
- 세계관 마스코트·상징 동반자 후보:
- 제약·제외 범위:

## 1.1 P04_PLAYER_VALUE_TO_EVIDENCE_TRACE

`PLAYER_VALUE_TRACE_REQUIRED`를 실제 Slice 계약에서 소비한다. 기능 존재나 화면 완성도를 플레이어 가치의 대리 지표로 사용하지 않는다.

```yaml
player_promise:
meaningful_choice:
expected_experience:
research_question:
observable_signal:
evidence_ceiling:
slice_acceptance:
```

- `research_question`: 어떤 개발 결정을 바꾸기 위해 무엇을 배울지 기록한다.
- `observable_signal`: 행동·관찰·자기보고·이벤트·퍼널 중 어떤 신호를 볼지 기록한다.
- `evidence_ceiling`: 현재 확보한 증거로 주장 가능한 최대 수준을 기록한다. 기술·정적·UI 증거만으로 사람의 이해·감정·고민·기억을 PASS하지 않는다.
- `slice_acceptance`: 관찰 신호에 따라 `EXPAND / REWORK / REPEAT_SLICE / HOLD / STOP` 중 어떤 다음 결정을 내릴지 연결한다.

## 1.2 WORLD_STORYLINE_FIT_REQUIRED

기능·시스템·난이도·연출이 작동하는지만 보지 않고, 현재 프로젝트에서 실질적인 경우 **세계관·핵심 스토리·플레이어 판타지**와의 정합성을 함께 판정한다.

- 상태: `FIT / NOT_APPLICABLE / CONFLICT / UNVERIFIED`
- 세계관 불변 조건·근거:
- 핵심 스토리라인 불변 조건·근거:
- 플레이어 판타지 약속·근거:
- 이번 Slice의 충돌 가능 요소:
- 충돌 시 제거·변형·재검증 결정:

`NOT_APPLICABLE`은 세계관·스토리 축이 현재 게임에 실질적으로 없을 때만 이유와 함께 사용한다. `CONFLICT / UNVERIFIED` 상태를 기능 완성도나 벤치마크 인기로 덮어 `APPROVED` 또는 확장 판정으로 올리지 않는다.

## 2. 데모 핵심 위험·내부 Spike

별도 `CORE_POC` Gate를 만들지 않는다. 아래는 데모 전체를 차단하는 기술 불확실성이 있을 때만 작성한다.

- 데모 핵심 위험:
- 영향을 받는 플레이어 약속·범위:
- 필요한 `TECHNICAL_SPIKE` 질문:
- 데모에서 재사용할 최소 산출물:
- 빌드·환경:
- 성공·실패·중단 기준:
- 결과·증거:
- 판정: KEEP / AMPLIFY / CHANGE / REMOVE / DEFER / RETEST
- 데모 계약·품질 기준에 반영할 조정:

## 3. Slice 검증 목적

- 왜 전체 제작 전에 확인해야 하는가:
- 성공·실패가 바꿀 다음 결정:
- 대표 플레이 구간이 일반 반복 플레이를 대표하는 이유:
- 기억에 남는 하이라이트:

## 4. 대표 플레이 흐름

```text
첫인상
→ 첫 행동
→ 기본 규칙 학습
→ 첫 의미 있는 선택
→ 핵심 루프 완주
→ 성공 또는 실패
→ 복구·재도전
→ 성장·보상
→ 더 큰 가능성
→ 데모 종료
```

- 예상 플레이 시간:
- 시작 조건:
- 종료 조건:
- 데모 종료 CTA:

## 5. 포함 범위

- 시스템:
- 콘텐츠:
- 캐릭터·적·장소:
- UI·UX:
- 아트·애니메이션:
- 사운드·연출:
- 마스코트 역할:
- 데이터·저장:
- 플랫폼·성능:
- 접근성:

## 6. 제외 범위

- 전체 콘텐츠:
- 장기 성장·경제:
- 추가 캐릭터·적·스테이지:
- 출시 후 기능:
- 이번 검증과 무관한 기능:

## 7. WHY→플레이→판매 추적표

| 요소 | WHY | 플레이어 행동 | 규칙·피드백 | 데모 장면 | 트레일러 | 스크린샷 | 테스트 지표 | 반복 제작 증거 |
|---|---|---|---|---|---|---|---|---|

## 8. 품질 기준

| 영역 | 관찰 가능한 기준 | 검증 방법 | 결과·증거 |
|---|---|---|---|
| 조작 |  |  |  |
| 정보 전달 |  |  |  |
| UI·UX |  |  |  |
| 아트·애니메이션 |  |  |  |
| 음악·효과음 |  |  |  |
| 마스코트 |  |  |  |
| 저장·복구 |  |  |  |
| 성능 |  |  |  |
| 접근성 |  |  |  |

## 9. 제작 파이프라인 증명

```text
기획
→ 데이터
→ 기존 자산·에셋스토어 조사
→ 신규 제작이 필요한 최소 자산
→ 구현
→ 통합
→ QA
→ 문서·Handoff
→ 두 번째 유사 콘텐츠 제작
```

- 반복 제작할 단위:
- 두 번째 콘텐츠:
- 실제 제작 시간:
- 병목·대기:
- 자동화 후보:
- 폴백·제거 절차:

## 10. 에셋·라이선스

- 기존 승인 자산:
- 보유 자산:
- 조사한 Godot 기본 기능·Asset Store·플러그인:
- ADOPT / ADAPT / TRIAL / REJECT / BUILD_CUSTOM 판정:
- 사용자 승인 필요한 유료 구매:
- Asset License Ledger 경로:

## 11. Balance Tuning Backlog

| ID | 시스템 | 변수 | 상태 | 임시값·범위 | 의도 | 관찰 지표 | 다음 검증 |
|---|---|---|---|---|---|---|---|

## 12. DEMO_VALIDATION (`SLICE_VALIDATION` 호환)

- 빌드·버전:
- 대상 플레이어:
- 이전 노출:
- 모집·접근:
- 플레이 과제·시간:
- 관찰 지점:
- 이벤트·퍼널:
- 설문·인터뷰:
- 버그 신고:
- 성공·실패·중단 기준:

## 13. PC 통합 데모 패키지

PC 프로젝트에서만 작성한다.

### Steam

- [ ] 출시 예정 페이지 문구
- [ ] 실제 플레이 트레일러
- [ ] 실제 플레이 스크린샷
- [ ] 장르·태그·지원 언어
- [ ] 캡슐·키아트
- [ ] 찜하기 CTA

### STOVE

- [ ] 튜토리얼 검증
- [ ] UI 가독성·UX·조작성
- [ ] 난이도·실패 이유
- [ ] 핵심 재미 시작점
- [ ] 구매·반복 플레이 의향

### Steam Playtest

- [ ] 전용 빌드·테스트 계약
- [ ] 행동 이벤트·퍼널
- [ ] 피드백·버그 신고
- [ ] 종료 기준

### 텀블벅

- [ ] 캐릭터·세계관·팬덤 가치
- [ ] 실제 플레이 영상
- [ ] OST·아트북·설정집 가치
- [ ] 남은 범위·비용·기간
- [ ] 디지털 리워드·전달 계획
- [ ] 위험·대응

### itch.io

- [ ] 제한 테스트·데모 배포 역할
- [ ] 크리에이터·언론용 빌드

## 14. 모바일 통합 데모 패키지

모바일 프로젝트에서만 작성한다.

- [ ] Google Play 등록 자료 초안
- [ ] 내부·비공개 테스트 AAB
- [ ] 릴리스 서명·키 백업
- [ ] 터치·빠른 입력·뒤로가기
- [ ] 작은 화면·화면비·세이프 영역
- [ ] 백그라운드·중단·복귀
- [ ] 저장·재설치·업데이트 호환
- [ ] 저사양·발열·배터리·메모리
- [ ] 광고·결제 성공·취소·실패
- [ ] 개인정보·SDK·데이터 수집
- [ ] 튜토리얼 퍼널·첫 세션·재방문
- [ ] 단계적 배포·롤백

## 15. 위험과 Finding

### P0

- 없음

### P1

- 없음

### P2

- 없음

### P3

- 없음

### TECHNICAL_REVIEW_PROPOSAL

- 없음

### USER_DECISION_REQUIRED

- 없음

### BLOCKED_UNVERIFIED

- 없음

## 16. Skill 실행 증거

| Skill | Mode | Trigger | 상태 | 산출물·증거 |
|---|---|---|---|---|

## 17. Gate 2 판정

- 판정: APPROVED / APPROVED_WITH_CONDITIONS / REWORK / REPEAT_VALIDATION / HOLD / STOP / UNVERIFIED
- 근거:
- 조건:
- 다음 제품 단계:
- Base에 남길 일반 교훈:
- 프로젝트에 남길 전용 결정:

## 18. 완전성 감사

### Requirement Coverage

- [ ] 사용자 최신 요구와 승인 결정이 모두 추적됨
- [ ] 기본 Project Play에서 대표 플레이의 시작·성공·실패·복귀까지 연결됨

### Skill Coverage

- [ ] 현재 Gate에 필요한 Skill 책임과 실행 증거가 있음

### Artifact Coverage

- [ ] 게임·데이터·자산·문서·스토어·테스트 산출물이 실제로 존재함