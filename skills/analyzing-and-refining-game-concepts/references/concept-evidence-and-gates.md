# 컨셉·기술 Spike 상세 계약

## 핵심 컨셉

```text
[대상 플레이어]는 [핵심 행동과 선택]을 반복하며
[고유한 감정·판타지·성취]를 경험한다.
이 게임은 [비교 대상]과 달리 [차별화된 원리] 때문에 계속 플레이된다.
```

핵심 컨셉은 플레이어 역할, 반복 행동, 중요한 선택, 즉시 피드백, 다음 플레이를 부르는 미완료 욕구와 요소 추가·삭제 기준을 포함한다.

## 제약 확인

| 제약 | 확인 내용 |
|---|---|
| 플레이 환경 | 세션 길이, 입력 방식, 온라인·오프라인, 접근성 |
| 제작 | 인력, 기술, 일정, 자산 생산 속도, 반복 비용 |
| 콘텐츠 | 필요한 변형 수, 재사용성, 소모 속도 |
| 시스템 | 저장, 경제, 난이도, AI, 멀티플레이 의존성 |
| 표현 | 아트 스타일, 연출, 가독성, 플랫폼 성능 |
| 사업·시장 | 대상층, 가격·운영 방식, 경쟁작, 포지셔닝 |

제약은 아이디어를 약화시키는 목록이 아니라 뾰족한 재미를 선명하게 하는 설계 경계다.

## 뾰족한 재미 확인

1. 플레이어가 직접 하는 행동인가?
2. 반복할수록 판단·숙련·표현이 깊어지는가?
3. 성공·실패 피드백이 명확한가?
4. 한 문장과 짧은 플레이로 설명 가능한가?
5. 다른 요소가 이 재미를 강화하는가?
6. 콘텐츠 양을 늘리지 않아도 변주가 생기는가?
7. 다음 판·단계·빌드를 시도할 이유가 생기는가?
8. DDD 보상이 이 재미를 빠르게 드러내는가, 자극으로 가리는가?
9. 외부 사례·플레이어 반응에서 같은 기대·불만이 반복되는가?

후보는 `핵심 / 보조 / 장식 / 충돌 / 미검증`으로 분류한다.

## Concept structuring / BIG BLIND

GDD 핵심 규칙, 레벨, 등장인물, 캐릭터 스타일, 스테이지, 세계관, UI·아트·사운드, 성장·수집·경제와 DDD 리듬을 핵심 컨셉에 대조한다.

- `AMPLIFY`: 핵심 재미를 직접 강화.
- `SUPPORT`: 이해·리듬·동기를 보조.
- `NEUTRAL`: 존재하지만 핵심에 기여하지 않아 삭제·축소 후보.
- `CONFLICT`: 핵심 컨셉과 충돌해 재설계 후보.
- `UNPROVEN`: 추가 증거가 필요한 가설. **기술 불확실성**이면 `TECHNICAL_SPIKE_INTERNAL_ONLY`, 플레이어의 재미·몰입·가독성·첫인상·감정·기억처럼 사람 경험이 질문이면 `RELEASE_NEAR_VERTICAL_SLICE_FIRST`로 분리한다.

## 분석 렌즈

- SWOT: `SO` 강점으로 기회 확대, `WO` 기회를 위한 약점 보완, `ST` 강점으로 위협 방어, `WT` 약점과 위협이 겹치는 범위 제거·회피.
- MDA/DDE: Mechanics·Design → Dynamics → Aesthetics·Experience의 인과를 확인한다.
- 3C: Character/Control/Camera 또는 프로젝트가 정의한 3C의 실제 플레이 영향.
- 루프·동기: Micro → Session → Meta가 다음 행동과 장기 목표를 연결하는가.
- 차별화·제작성: 장르 관습이 아니라 핵심 행동의 차이이며 현재 팀과 파이프라인으로 반복 생산 가능한가.

## Technical Spike 계약

```text
TECHNICAL_SPIKE_INTERNAL_ONLY
SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE
```

```yaml
technical_question:
riskiest_technical_assumption:
minimal_implementation:
comparison_or_baseline:
machine_or_runtime_observation:
success_failure_stop_criteria:
validation_environment:
result:
decision: KEEP/AMPLIFY/CHANGE/REMOVE/DEFER/RETEST
next_gate:
```

과거 `PoC` / `poc-contract` 기록은 compatibility 자료로 읽을 수 있지만, 새 실행에서는 **좁은 기술 Spike**로 해석한다. Technical Spike는 전체 게임이나 Vertical Slice가 아니다. 알고리즘·성능·호환성·저장/데이터 흐름·엔진 제약처럼 완성형 데모 구현을 막는 기술 질문 하나만 최소 구현으로 확인하고 결과를 본 뒤 성공 기준을 바꾸지 않는다.

- 사람의 재미·몰입·가독성·첫인상·판매력·감정·기억·전체 UX를 Technical Spike 결과로 PASS 처리하지 않는다.
- 사람 행동 관찰이 필요한 질문은 이 계약의 입력/판정으로 끌어오지 않고 `designing-vertical-slices`의 완성형 Slice와 `playtest-evidence`로 넘긴다.
- Spike 구현이 유효하면 폐기용 별도 제품 단계로 남기지 말고 release-near Vertical Slice의 실제 시스템/데이터/파이프라인에 재사용하거나 Decision evidence로 기록한다.
- Technical Spike가 필요하지 않으면 생략한다. 횟수를 채우기 위한 PoC를 만들지 않는다.

## Release-near Vertical Slice handoff

플레이어 경험 검증은 `designing-vertical-slices`가 소유한다.

```text
RELEASE_NEAR_VERTICAL_SLICE_FIRST
→ actual game-use candidate UI/UX
→ image/art + animation/presentation
→ representative music/SFX
→ VFX/feedback
→ core system/data/content integration
→ complete short Vertical Slice
→ human play evidence
```

`SYSTEM_ONLY_POC_NOT_PLAYER_EXPERIENCE_EVIDENCE` 때문에 회색 상자·dummy UI·무음/무연출 PoC는 위 흐름을 대체하지 않는다. 기존 승인 자산·구현·엔진 기능·검증된 라이브러리/도구가 있으면 `EXISTING_SOLUTION_FIRST_ADAPT_TO_PROJECT`로 먼저 `ADOPT / ADAPT / REJECT`한다.

## Production gate

컨셉 단계와 본제작 확대 판정을 분리한다.

### `SLICE_BUILD_READY`

다음 조건이 충족되면 완성형 release-near Vertical Slice 구현으로 진행할 수 있다.

- 핵심 컨셉과 뾰족한 재미를 한 문장으로 설명할 수 있다.
- 세계관·핵심 스토리·플레이어 판타지와 주요 시스템의 충돌이 닫혔다.
- 데모 구현을 막는 기술 불확실성이 있으면 필요한 Technical Spike가 성공·실패·중단 기준까지 판정됐다.
- DDD 보상이 핵심 행동의 결과와 다음 행동을 연결하도록 설계됐다.
- 제품 사실·기존 플레이어 반응·행동 근거·해석·제안을 분리했다.
- 벤치마크 발견을 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 판정했다.
- 주요 요소가 코어에 정렬되고 제작 제약·위험·제외 범위가 명확하다.

`SLICE_BUILD_READY`는 재미·몰입이 증명됐다는 뜻이 아니다. 사람 경험은 아직 `NOT_RUN`일 수 있다.

### 본제작 확대 판정

`PRODUCTION_READY`는 `designing-vertical-slices`의 release-near Slice가 목표 품질·시스템 연결·파이프라인과 필요한 human play evidence를 현재 evidence ceiling 안에서 통과한 뒤에만 사용한다.

```text
PRODUCTION_READY
REPEAT_VERTICAL_SLICE
HOLD
STOP
```

- `PRODUCTION_READY`: 대표 경험·목표 품질·제작성·필요한 사람 증거가 함께 성립한다.
- `REPEAT_VERTICAL_SLICE`: 구간·표본·가설·통합 품질이 대표적이지 않아 완성형 Slice 조건을 바꿔 재검증한다.
- `HOLD`: 외부 의존성·환경·권리·비용 때문에 판정 근거가 부족하다.
- `STOP`: 핵심 제품 약속이나 제작성이 현재 증거에서 성립하지 않는다.

정적 문서, 자동 테스트, Technical Spike 성공만으로 `PRODUCTION_READY`를 선언하지 않는다.