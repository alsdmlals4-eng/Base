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

<a id="fun-verification-lifecycle"></a>

## Fun verification lifecycle

`FUN_VERIFICATION_LIFECYCLE`: 플레이어 경험에 영향을 주는 신규·의미 있는 변경은 기능 기획부터 설계·구현·검증·교정까지 같은 경험 가설을 추적한다. Base는 **검증 방법과 증거 경계**, 프로젝트는 **대상 플레이어·핵심/보조 경험·보호할 의미·판정 기준**을 소유한다. 아래 내용은 공용 운영 계약이지 재미를 보장하는 과학적 공식이 아니다.

### 적용 범위와 비용 경계

- L1 이상 플레이어-facing 기능·시스템·콘텐츠·UI/UX·피드백 변경에 적용한다. L1은 기존 Brief·Decision·작업 계약에 짧게 연결하며 새 Spec·보고서·대시보드를 요구하지 않는다. L2 주요 기능만 기존 `GAME_FEATURE_DESIGN_SPEC.md`와 필요한 `FEATURE_SPEC_TRACEABILITY_PACKET.md`를 사용한다.
- L0 오탈자, 동작을 바꾸지 않는 기계 수정, 순수 내부 도구는 이유 있는 `NOT_APPLICABLE` 또는 기존 경험의 비퇴행 검사로 처리한다. 내부 기반 기능도 실제 플레이어-facing consumer에 미치는 영향이 있으면 해당 경로만 검토한다.
- 동일 승인·가설·consumer·대표 구간의 유효한 근거는 `REUSED_EVIDENCE`로 연결한다. 파일마다 전체 재미 연구를 반복하지 않으며 변경된 경험·상태·표본·환경 때문에 무효가 된 부분만 재검증한다.
- 승인된 방향을 다시 승인받지 않는다. 핵심 경험·서사·경제 의미·주요 UX·비용·범위를 바꾸는 교정만 `USER_DECISION_REQUIRED`로 올린다. `NEUTRAL / CONFLICT / UNPROVEN`은 검토 후보이지 자동 삭제·재설계 권한이 아니다.

### 공용 방법과 프로젝트별 값

프로젝트의 기존 핵심 기획/Experience Intent owner를 `source_id + path + section`으로 참조한다. 핵심 경험과 보조 경험, 대상/플레이 맥락, 금지 방향, 대표 Slice와 현재 근거·승인 상태를 그 owner에 결합한다. Base에 프로젝트별 수치·세계관·판정 결과를 복제하지 않는다. 정본에 없는 경험 목표는 `HYPOTHESIS / UNVERIFIED`이며 장르명·과거 채팅으로 확정하지 않는다.

`NO_UNIVERSAL_FUN_SCORE`: 모든 장르에 같은 점수·재도전율·난도·선택 수·보상 빈도를 강제하지 않는다. 서사는 이해·감정·기억, 표현/꾸미기는 자기 방식의 표현, 휴식형 경험은 부담과 편안함처럼 **프로젝트가 승인한 약속에 맞는 질문**을 선택한다. 이는 가능한 적용 예시이며 장르별 의무 목록이 아니다. 도전·숙련·반복 플레이가 핵심이 아닌 작품에 이를 필수 합격 기준으로 만들지 않는다.

### 기능 생명주기 연결

| 단계 | 기존 정본에 남길 최소 연결 | 다음 단계 판단 |
|---|---|---|
| PLAN — 기능 기획 | 기능/Requirement ID → 승인된 경험 원본 → `AMPLIFY / SUPPORT / NEUTRAL / CONFLICT / UNPROVEN` → 어떤 상황·행동·정보·결과가 어떤 경험을 만들 것인지의 가설 | 기능 수가 아니라 플레이어 가치와 보호 범위로 채택·보류를 판단한다. |
| DESIGN — 설계 | 같은 가설 → 입력·상태·규칙·의미 있는 선택 또는 표현 → 피드백/보상/결과 → `runtime_consumer` → 가장 작은 대표 Slice와 관찰 질문 | Godot이면 실제 Scene·Node·Resource·Script, 데이터/save-load, UI 상태·입력, 필요한 자산, 기존 통합·실패·회귀를 연결한다. 미구현 경로는 계획으로 표시한다. |
| IMPLEMENT — 구현 | 승인 Requirement → 실제 파일·Scene·데이터·자산 consumer → 기계/실행 검증 → 필요한 최소 관찰 지점 | 기존 로그·리플레이·캡처를 우선하며 재미 측정을 이유로 분석 서버·상주 에이전트·유료 도구를 자동 도입하지 않는다. |
| VERIFY — 검증 | exact 빌드/commit·환경·대상·표본·대표 구간 → 행동 관찰 + 자기보고 + 필요한 로그 → 의도와 실제 경험의 차이·`counterevidence` | 경험 가설별 지지·반박·미확인을 판단한다. 관측하지 않은 질문은 `NOT_RUN`이다. |
| LEARN — 교정 | 원인 분류 → `KEEP / CHANGE / DEFER / RETEST` 등 기존 Decision → 최소 수정·재검증 → 정본/Active Context·기존 Learning Log | 프로젝트 전용 교훈과 Base 공용 후보를 구분한다. 문서 계약 추가를 재미 개선 실증으로 승격하지 않는다. |

설계의 목표·규칙은 `managing-design-documents`의 기존 owner, 실행 결과는 기존 validation evidence owner가 소유한다. 이 reference는 그 내용을 다시 소유하지 않는다. L2의 `GAME_FEATURE_DESIGN_SPEC.md` §2는 가설·계획, Packet은 승인·구현·증거 ID 연결을 맡는다.

### 검증과 감독의 책임 경계

- 테스트 전에 바꿀 개발 결정, 대표 구간, 성공·실패·중단 기준을 정한다. `benchmark-player-evidence-and-playtests.md`의 기존 방법을 재사용한다. 한 번에 가장 중요한 경험 가설을 우선하되 인위적인 표본 수·테스트 횟수를 공용 합격 기준으로 고정하지 않는다.
- 관찰은 행동, 자기보고는 당사자의 해석, 로그는 기록된 사건을 보여준다. 서로 모순되면 숨기지 말고 대안 설명과 추가 검증을 남긴다. 오래 고민함=흥미로운 선택, 긴 플레이=몰입, 높은 재도전율=만족으로 단정하지 않는다. DDD는 설계 렌즈이지 실제 도파민의 측정이 아니다.
- 첫 플레이의 이해·도달과 반복 플레이의 숙련·변주·피로를 구분한다. 짧은 세션 결과로 장기 유지율·전체 게임·다른 집단을 검증했다고 하지 않는다. 테스트 중 설명·힌트·유도 개입이 있었다면 기록한다.
- 이해 실패, 선택/규칙 실패, 피드백/감각 실패, 리듬/콘텐츠 피로, 빌드/환경 결함을 분리한다. 같은 관찰에 여러 원인이 있을 수 있으므로 보상·기능 추가를 기본 해법으로 삼지 않는다.
- '재미 감독'은 `analyzing-and-refining-game-concepts`의 **경험 가설과 증거 차이를 종합하는 책임**이다. 이 책임만을 이유로 새 독립 Skill·승인권자·가상 플레이어를 자동 추가하지 않는다. `designing-vertical-slices`의 사람 플레이 증거와 실제 변경 검증 owner를 연결하며 AI 자체 평가는 HUMAN 증거가 아니다. 게임 내부의 runtime Director는 별도 기능 요구가 있을 때만 검토한다.
- `DOC / MACHINE / RUNTIME / HUMAN / USER_APPROVAL / RELEASE`는 별개 검증층이다. 자동 테스트·AI 검토·로그만으로 HUMAN PASS나 `FUN_PASS`를 만들지 않는다. 문서 테스트는 계약·링크의 존재만 확인하며 AI의 실제 준수나 게임 재미를 강제/보증하지 않는다.
- 사람 증거가 없다고 승인된 Slice 구현 자체를 순환 차단하지 않는다. 아래 `SLICE_BUILD_READY`와 `PRODUCTION_READY`의 구분을 유지하고, 필요한 HUMAN 검증·승격만 `NOT_RUN / BLOCKED_UNVERIFIED`로 남긴다. release-near Slice의 짧은 범위를 유지하며 전체 게임 완성을 테스트 선행 조건으로 만들지 않는다.

### 조사 근거와 적용 한계

2026-09-18 확인. 아래 원출처를 기존 Base 계약과 비교해 방법만 흡수했으며 개별 프로젝트 재미를 검증하지 않았다.

- **ADOPT** — [Choose the right playtest method](https://gamesuserresearch.com/choose-the-right-playtest-method/): 연구 질문에 맞는 방법 선택, 관찰·인터뷰·분석의 상호 보완. 본문 확인; 특정 표본 수나 성공률의 근거로 쓰지 않는다.
- **ADAPT** — [Interesting Decisions, GDC 2012](https://www.gdcvault.com/play/1015756/): 선택·정보·피드백·pacing을 함께 검토한다는 발표자 공개 개요. 개요 확인만 했으며 전체 영상 검토나 모든 장르의 의무 기준으로 확대하지 않는다.
- **ADAPT** — [Slay the Spire: Metrics Driven Design and Balance, GDC 2019](https://www.gdcvault.com/play/1025731/-Slay-the-Spire-Metrics): 지표와 커뮤니티 피드백을 함께 다룬다는 발표자 공개 개요. 개별 알고리즘·표본·실험 효과는 이 개요만으로 추정하지 않는다.
- **REJECT** — 보편적 재미 점수, 로그만으로 감정을 확정하는 판정, 중복 감독 계층, 프로젝트 정체성과 채택 version을 무시하는 일괄 전파.

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