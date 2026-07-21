# 접근성 장벽·성능 예산 검증 모델

이 문서는 `reviewing-and-validating-project-changes`의 `accessibility-review`, `performance-profile` mode가 사용하는 상세 기준이다. 접근성은 법적 적합성 선언이 아니라 플레이 장벽 검수이며, 성능은 느낌이나 평균 FPS가 아니라 목표 플랫폼에서 재현 가능한 측정으로 판정한다.

## 1. 접근성 검수 입력

```yaml
target_players_and_contexts:
platforms_and_input_devices:
core_gameplay_information:
required_visual_audio_haptic_cues:
ui_navigation_and_focus:
text_and_localization:
time_limits_and_difficulty:
motion_flashing_and_photosensitivity:
communication_features:
known_barriers_and_user_feedback:
```

Microsoft Xbox Accessibility Guidelines는 디자이너의 아이디어 촉진, 개발자의 가드레일, 테스트 팀의 검수 기준으로 사용할 수 있지만 법적 준수 체크리스트로 간주하지 않는다.

## 2. 접근성 검수 축

| 축 | 최소 확인 |
|---|---|
| 텍스트·가독성 | 크기, 간격, 배경, 확대·스타일 옵션, 실제 플레이 거리 |
| 대비·색상 | 색만으로 상태를 구분하지 않는가, 중요한 요소가 명확한가 |
| 다중 감각 채널 | 핵심 시각·음향 신호가 자막·아이콘·진동 등 다른 채널로 전달되는가 |
| 자막·오디오 | 대사·핵심 효과 구분, 개별 볼륨, 자막 가독성·화자 표시 |
| 입력 | 키·버튼 재지정, 홀드·연타·복합 입력 대안, 장치 전환, 포인터 의존성 |
| 난이도·도움 | 장벽을 조정하는 옵션, 실패 후 학습·복구, 핵심 경험 보존 |
| UI 탐색 | 일관된 이동, 포커스 표시, 순환·탈출, 보조 입력과의 호환 |
| 시간 제한 | 읽기·판단·입력 시간이 충분한가, 일시정지·연장·비활성 옵션이 있는가 |
| 오류·파괴 행동 | 원인·복구·결과가 명확하고 되돌릴 수 있는가 |
| 모션·광과민 | 화면 흔들림·깜빡임·과도한 이동을 줄이거나 끌 수 있는가 |
| 문서화 | 구매·시작 전 필요한 접근성 기능과 조작 정보를 알 수 있는가 |

검수는 핵심 플레이 경로와 설정 메뉴 양쪽에서 한다. 설정 화면에 옵션이 존재해도 실제 게임 상태에 적용되지 않으면 통과가 아니다.

## 3. 접근성 결과

```yaml
barrier_id:
player_context:
trigger:
blocked_or_degraded_action:
severity:
existing_alternative:
recommended_change:
core_experience_tradeoff:
validation_scenario:
status:
```

심각도:

- `BLOCKING`: 시작·진행·설정·복구가 불가능하다.
- `MAJOR`: 핵심 경험의 상당 부분이 손실된다.
- `MODERATE`: 반복적인 피로·혼란·오입력을 만든다.
- `MINOR`: 품질·편의 개선이다.

## 4. 성능 검수 입력

```yaml
target_hardware_and_os:
build_configuration:
representative_scenes_and_loads:
frame_time_budget_ms:
cpu_gpu_memory_network_budgets:
loading_and_streaming_targets:
baseline_commit_and_capture:
profiler_and_capture_tools:
measurement_repetitions:
```

## 5. 성능 원칙

- 목표 플랫폼·실제 빌드에 가까운 환경에서 측정한다.
- 평균 FPS보다 frame time(ms), 하위 구간, hitch·spike와 일관성을 본다.
- CPU·GPU·메모리·네트워크·로딩을 분리한다.
- 에디터·디버거·프로파일러 오버헤드를 기록한다.
- 재현 가능한 대표 장면과 입력을 고정한다.
- 한 번의 캡처보다 여러 번 측정해 변동을 확인한다.
- 병목을 측정하기 전에 임의 최적화하지 않는다.
- 변경 전 baseline과 변경 후 capture를 같은 조건에서 비교한다.

Unreal Engine 공식 문서는 30·60·120 FPS 같은 목표를 frame time과 목표 하드웨어 예산으로 연결하고, Unreal Insights·Stat Commands 등으로 CPU·GPU·메모리·네트워크를 측정하도록 안내한다. 또한 에디터 노이즈를 줄이고 목표 환경과 가까운 재현 사례에서 밀리초 단위로 비교할 것을 권장한다.

## 6. 성능 검수 절차

```text
목표·예산 고정
→ 대표·최악·경계 장면 선택
→ baseline 반복 측정
→ CPU/GPU/메모리/네트워크 병목 분리
→ 최소 수정
→ 같은 조건 재측정
→ 품질·기능 회귀 확인
→ 목표 플랫폼 통과·실패 판정
```

대표 장면만 최적화하고 콘텐츠 최대량·저사양 장치·긴 세션·메모리 누적을 생략하지 않는다.

## 7. 엔진·플랫폼 테스트 층

Unity Test Framework처럼 엔진이 Edit Mode, Play Mode, target player를 구분하면 다음을 별도 증거로 남긴다.

- 정적·순수 로직: Edit Mode 또는 동등한 빠른 테스트
- 프레임·씬·코루틴·입력·물리: Play Mode
- 플랫폼 API·성능·해상도·입력 장치: 실제 target player

한 층의 통과를 다른 층의 통과로 대신하지 않는다.

## 8. 출력 형식

```md
## 접근성 장벽
- 대상 플레이어·맥락
- 핵심 정보 채널
- 입력·UI·시간·난이도·모션 장벽
- 심각도·대안·검증 시나리오

## 성능 예산·프로파일
- 목표 플랫폼·빌드·장면
- baseline과 변경 후 frame time
- CPU·GPU·메모리·네트워크 병목
- profiler 오버헤드와 반복 변동
- 품질·기능 trade-off
- 통과·미통과·미검증
```

## 9. 실패 조건

- 접근성을 색약 모드나 자막 유무 하나로 축소한다.
- 옵션 존재만 확인하고 실제 핵심 경로에 적용되는지 테스트하지 않는다.
- 접근성 검수 결과를 법적 준수 인증으로 표현한다.
- 평균 FPS 하나만 보고 hitch·frame time·저사양 장치를 무시한다.
- 에디터의 빈 장면만 측정해 실제 빌드 성능으로 주장한다.
- profiler 없이 추측으로 병목을 최적화한다.
- baseline·장면·빌드 조건이 다른 수치를 직접 비교한다.
- 성능 개선으로 게임 규칙·가독성·아트 약속이 훼손됐는데 회귀를 생략한다.

## 공식 참고 자료

- Microsoft — Xbox Accessibility Guidelines: https://learn.microsoft.com/en-us/xbox/accessibility/guidelines
- Microsoft — XAG 103 Additional channels: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103
- Microsoft — XAG 107 Input: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107
- Microsoft — XAG 112 UI navigation: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/112
- Microsoft — XAG 116 Time limits: https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/116
- Epic Games — Performance Profiling and Configuration: https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine
- Epic Games — Performance and Profiling Overview: https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-and-profiling-overview
- Unity — Edit Mode vs Play Mode tests: https://docs.unity3d.com/Packages/com.unity.test-framework@2.0/manual/edit-mode-vs-play-mode-tests.html
