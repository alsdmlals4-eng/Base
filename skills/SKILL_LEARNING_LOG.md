# Base Skill Learning Log

## 2026-07-24 GPT–Codex 역할 분리·Grill Me·비용 최적화 CI 교훈

- Grill Me는 요구 확인과 승인 상태를 다시 만드는 독립 Skill이 아니라 `managing-project-intake-and-work-contract`의 `clarify` Mode에 통합하는 편이 중복 질문과 상태 충돌을 줄인다.
- GPT는 기획·벤치마킹·시스템·데이터·UX·비-Godot 파일·GitHub 계약과 검수를 완료하고, Codex Plan은 최신 Godot 저장소를 읽기 전용으로 재검수하며, Codex Build는 지정 Branch의 Godot 구현만 담당하도록 의사결정 권한과 파일 권한을 분리했다.
- 동일한 플레이어 결과와 데이터 계약을 유지하는 구조·성능·안정성·테스트 개선은 기술 변경으로 허용하되 프로젝트 코어·Core Loop·플레이 규칙·MVP·주요 UX·저장 호환성 변경은 `CHANGE_PROPOSAL`로 구현과 분리한다.
- 전체 설계는 마스터 구현계획 하나로 유지하고 실제 구현은 검증 가능한 패키지, 상위 Issue, 패키지별 Branch·PR, 순차 진행, 영향도 기반 승인 게이트로 나누는 것이 회귀·롤백·중단 후 재개에 유리하다.
- GitHub Actions 첫 실제 실행에서 `actions/setup-node`의 `cache: pnpm`이 Corepack 활성화 전에 pnpm을 요구해 Ubuntu·Windows 발행 Job이 모두 실패했다. 패키지 관리자 캐시는 해당 실행 파일의 준비 순서를 보장한 뒤에만 활성화해야 한다.
- 같은 실행에서 Skill 본문만 바꾸고 Registry·Learning Log·집중 회귀 테스트를 함께 갱신하지 않은 coupled-change 누락이 정본 최신성 검사에 의해 차단됐다. Skill 계약 변경은 본문·Registry·학습·검증을 하나의 변경 단위로 취급한다.
- 현재 지식 상태: 역할 경계와 승인 정책은 사용자 승인된 `PATTERN`, 실제 여러 게임 프로젝트의 단계별 Codex 인계 효과는 `OBSERVATION`, 변경 위험별 CI 비용 절감 효과는 후속 실행량 데이터 전까지 `HYPOTHESIS`.

## 2026-07-22 원문 책임 전수 매핑·Skill 구조 최적화

- 1,201줄 학습 텍스트의 책임을 `skills/SKILL_COVERAGE.json`에 전수 매핑했다.
- 가지치기·본문 간소화·행동 보존 리팩토링은 입력·산출물·삭제 권한·검증이 달라 독립 Skill로 분리했다.
- 동기화·장기 작업 연속성·Games User Research 11영역·학습 노트·시각 대시보드·엔진 디버깅도 기존 Skill로 흡수할 수 없는 독립 계약으로 판정했다.
- 요청 명세화·Issue/Goal·MVP·벤치마킹·문서 기억·검증은 기존 Skill에 이미 기능이 있어 중복 신설하지 않았다.
- 코어 판정·코어 확정·적대적 검토·컨셉 분석·Skill 진화 본문을 compact router로 리팩토링하고 상세 판정표를 reference로 이동했다.
- 전용 checker와 PR 회귀 테스트로 coverage, Registry, front matter, 파일 존재, 본문 최소 계약과 compact line budget을 검증한다.
- 현재 지식 상태: 실제 Base 적용은 `OBSERVATION`, 여러 프로젝트 반복 전까지 새 Skill 계약은 `HYPOTHESIS`.
## 2026-07-21 프로젝트 코어·적대적 검토 Skill 분리 교훈

- 프로젝트 코어 판정은 기존 프로젝트의 승인 원본·실제 구현·의존 관계를 읽기 전용으로 대조하는 작업이며, 새 프로젝트의 코어를 제안·확정하는 기획 권한과 분리한다.
- `identifying-project-core`는 기획·시스템·코드 코어와 코어 기능·MVP 지원 기능을 제거·대체 테스트로 구분한다.
- `establishing-project-core`는 PLAN Work Mode에서 불변 조건과 변경 가능한 외피를 제안하고, 반례 검토 뒤 사용자의 명시적 승인만 `CORE_CONFIRMED`로 인정한다.
- 적대적 검토는 레드팀 공격, 비판 검증, 승인된 finding의 최소 개선, 회귀 재검토를 분리한다. 비판도 취향·과잉 요구·잘못된 전제일 수 있으므로 그대로 반영하지 않는다.
- 세 Skill은 읽기 권한, 승인 경계, 산출물이 달라 독립 Skill로 유지하되 실제 여러 프로젝트에서 오라우팅·코어 과대 판정·비판 과수용을 검증하기 전까지 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 둔다.


## 2026-07-21 Work Mode·자동 Skill 라우팅·구형본 정리 교훈

- `Mode`라는 단어를 세션 전체 작업 방식과 Skill 내부 절차에 함께 쓰면 라우팅 순서가 모호해진다. Base에서는 전자를 `Work Mode`, 후자를 `Skill Mode`로 구분한다.
- 요청 처리 순서는 `Prompt 의도·현재 단계 파악 → PLAN/BUILD/REVIEW Work Mode 선택 → Registry trigger 기반 Skill 자동 선택 → Skill Mode 선택 → 실행·검증 → 사용 이유·결과·증거 보고`가 기본이다.
- 사용자는 Skill 이름이나 Skill Mode를 선언할 필요가 없다. `load_by_default=false`는 자동 사용 금지가 아니라 trigger가 없을 때 불필요하게 로드하지 않는다는 뜻이다.
- `PLAN`은 읽기·조사·계약, `BUILD`는 승인 범위 구현, `REVIEW`는 적대적 검토·반례·증거를 기본 권한으로 둔다. 검토 중 수정이 필요하면 `REVIEW → BUILD → REVIEW`로 전환한다.
- Skill 자동 사용은 숨겨진 절차가 되어서는 안 된다. L1 이상 작업은 실제 사용한 Work Mode·Skill·Skill Mode, 선택 이유, 수행 내용, 얻은 결과, 증거와 미검증을 보고한다.
- 구형 파일 정리는 단순 삭제가 아니다. `CURRENT / UPDATE_IN_PLACE / MERGE_TO_CANONICAL / COMPATIBILITY_STUB / ARCHIVE_HISTORY / DELETE_APPROVED / KEEP_UNRESOLVED`로 판정하고 고유 정보·활성 참조·파생본·복구·승인을 확인한다.
- 구형본 탐지·정리·마이그레이션은 같은 책임 원본과 삭제 권한을 공유하므로 신규 독립 Skill보다 `managing-game-project-operating-system: reconcile-legacy` Skill Mode로 통합하는 편이 중복과 오삭제를 줄인다.
- 자동 라우팅과 구형본 정리 계약은 구조 회귀로 검증하되, 실제 서로 다른 프로젝트에서 오라우팅·과도한 보고·호환 stub 누락·오삭제 빈도를 확인하기 전까지 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 유지한다.

## 2026-07-21 DDD 빠른 보상 설계 교훈

- 이 Base의 게임 기획 맥락에서 `DDD`는 `Digital Dopamine Design`이다. 플레이 시작 또는 행동 직후 짧은 시간 안에 의미 있는 보상·변화·성취와 다음 기대를 체감시키는 빠른 보상 설계축을 뜻한다.
- DDD는 실제 도파민 분비량을 측정하거나 의학적 중독을 진단하는 표현이 아니다. `첫 의미 있는 보상까지의 시간`, `행동-피드백 지연`, `보상 명료성`, `보상 밀도`, `micro-session-meta 보상 사다리`, `다음 행동 유도`, `피로·인플레이션`을 관찰한다.
- 빠른 보상은 뾰족한 재미를 더 빨리 이해시키는 수단이어야 한다. 의미 있는 선택 없이 이펙트·팝업·숫자·알림만 반복하면 핵심 재미를 자극으로 대체한 실패다.
- 빠른 보상을 설계할 때 가치·확률·비용 은폐, 인위적인 불편 뒤 결제 해소, 손실 압박, 중단을 방해하는 연속 알림 같은 위험을 별도 표시한다.
- Base 내부 DDD 정의는 확정했지만, 외부 자료나 다른 프로젝트에서 같은 약어를 사용할 때는 해당 출처의 정의를 확인하기 전 임의 해석하지 않는다.

## 2026-07-21 외부 근거·작업 순서·플레이 검증 교훈

- 벤치마크는 인기 게임의 기능 목록을 모방하는 절차가 아니다. 현재 결정을 바꿀 질문과 비교 차원을 먼저 고정하고, 공식 제품 사실·플레이어 자기보고·행동 이벤트·퍼널·통제 실험·해석을 서로 다른 근거 층위로 관리한다.
- 플레이어 리뷰는 기대가 어떻게 설정되고 실제 경험과 어디서 어긋나는지 찾는 채널이지만, 버전·패치·플레이타임·플랫폼·언어·긍정·부정·리뷰 폭탄을 구분하지 않으면 현재 기획을 정당화하는 선택 편향이 된다.
- 외부 조사 결과는 `ADOPT / ADAPT / AVOID / TEST / IGNORE`로 변환해야 하며, 평점·판매량·강한 표현만으로 핵심 컨셉을 변경하지 않는다.
- 작업 분해는 “코딩”, “문서 수정” 같은 활동 목록이 아니라 독립 검증 가능한 결과, `BLOCKS / INFORMS / USES_OUTPUT / SHARES_RESOURCE / VALIDATES` 의존성, 병렬 경계, 단계별 게이트·롤백으로 표현한다.
- 실행 순서는 의존성 해소, 가장 위험한 가설, 핵심 사용자 가치, 피드백 속도, 되돌리기 난이도와 자원 충돌을 함께 고려하고 새 사실·실패가 생기면 이후 계획을 재구성한다.
- 플레이테스트는 빌드·버전·대상 집단·기존 노출·과제·피드백 채널·관찰 행동·이벤트·퍼널·성공 기준이 있는 검증 계약이어야 한다. A/B 테스트는 한 주요 가설과 사전 선언한 주 지표·가드레일을 비교한다.
- 접근성은 옵션 존재나 법적 준수 선언이 아니라 핵심 정보·입력·UI·시간·난이도·모션에서 실제 장벽과 대체 경로를 검수한다.
- 성능은 평균 FPS 하나가 아니라 목표 플랫폼·동일 빌드·대표·최악 장면에서 frame time, CPU·GPU·메모리·네트워크·로딩을 baseline과 비교한다.
- 위 기능은 별도 Skill을 늘리지 않고 `decompose-and-sequence`, `benchmark-and-player-research`, `playtest-and-experiment`, `accessibility-review`, `performance-profile` mode로 기존 생명주기에 흡수한다. 활성 Skill 수는 13개를 유지한다.
- 공식 자료를 근거로 계약을 만들었지만 여러 실제 프로젝트에서 오라우팅·표본 편향·측정 비용을 검증하기 전까지 신규 mode의 지식 상태는 `OBSERVATION` 또는 `HYPOTHESIS`로 유지한다.

## 2026-07-21 정본·참조 최신성 감사 교훈

- 패치 검수는 변경된 파일만 보는 것으로 충분하지 않다. 정본이 바뀌면 **변경됐어야 하지만 untouched인 소비자·템플릿·테스트·Workflow·파생본**을 함께 찾아야 한다.
- 오래된 경로·Skill ID·문서 ID와 실제 실행 참조는 차단하되, Legacy Alias·Change Log·과거 case·Git 이력의 역사 참조는 별도 허용 상태로 구분해야 한다.
- 문자열이 최신이어도 여러 활성 문서가 서로 다른 mode·정책·상태·완료 기준을 설명하면 content drift다. 자동 검색과 책임 원본 기반 수동 검토를 함께 사용한다.
- 정본 변경 전파 검사는 범용 변경 검증의 `reference-freshness` mode에서 오케스트레이션하고, 영향 지도·오래된 참조·파생본 최신성은 독립 전문 Skill이 담당하는 구조가 중복을 줄인다.
- 자동 검사 규칙은 Legacy ID 잔존, 필수 정본 링크, coupled-change 누락을 담당하고 PDF·Manifest·해시·실제 렌더는 분야별 발행·운영체계 검증과 연결한다.
- 신규 전문 Skill은 실제 여러 프로젝트에서 오탐·누락률을 확인하기 전까지 `OBSERVATION`으로 유지한다.

## 2026-07-21 핵심 컨셉·변경 검증 스킬 교훈

- 게임 기획 방향을 잡는 작업은 GDD 문장 작성이나 Vertical Slice 제작과 다르다. 핵심 컨셉·제약·뾰족한 재미·요소 정렬·PoC·재조정을 하나의 상태 흐름으로 다뤄야 한다.
- SWOT은 장단점 목록이 아니라 SO·WO·ST·WT 실행 방향으로 변환해야 의사결정 도구가 된다.
- MDA·DDE·DDD·3C·루프 같은 프레임워크는 많이 적용하는 것이 목적이 아니라 핵심 재미와 불일치를 찾아 개선 우선순위를 만드는 데 사용한다.
- PoC는 전체 게임이나 Vertical Slice가 아니라 가장 위험한 가설을 최소 비용으로 틀릴 수 있게 만드는 검증 계약이다.
- 변경 검증은 외부 AI 결과에만 필요한 절차가 아니다. 사람·Codex·자동화가 만든 코드·데이터·문서·자산 모두 승인 계약, 실제 diff, 정적·런타임·회귀 증거로 같은 기준에서 검증한다.
- 외부 AI 검수는 범용 변경 검증 Skill의 `external-source-review` mode로 흡수하고, 이전 ID는 Legacy Alias로 보존한다.

## 2026-07-21 스킬·운영 구조 통합 교훈

- 하나의 요청 생명주기를 라우팅·인터뷰·실행 계약처럼 여러 Foundation Skill로 분리하면 같은 상태·범위·검증을 반복 판정하게 된다. 하나의 통합 Skill과 mode·상태 머신으로 우선 표현한다.
- 신규 설치·기존 감사·승인된 마이그레이션·Health Review처럼 같은 구조를 다른 권한으로 다루는 작업은 mode를 분리하고 기본 권한을 읽기 전용으로 둔다.
- 기획 내용 작성과 PDF 발행이 같은 Registry·원본·상태를 읽는 경우 하나의 문서 생명주기 Skill로 통합한다.
- Skill 통합 시 이전 ID를 즉시 소실시키지 않고 `LEGACY_SKILL_ALIASES.md`에서 새 Skill과 mode로 연결한다.
- Method·Checklist·START_HERE는 실행 절차를 반복하지 않고 `OPERATING_MODEL`과 실행 Skill을 연결하는 원칙·라우터로 축소한다.
- 모든 문서에 PDF를 강제하지 않고 `source_only`, `milestone_sync`, `always_sync` 발행 정책으로 비용과 검수 수준을 구분한다.

> Base 실행 Skill의 실제 적용 결과, 실패, 예외와 갱신 결정을 기록한다. 이 문서는 기본 작업 컨텍스트가 아니며 `skills/SKILL_REGISTRY.json`에서 특정 Skill의 학습 검토가 필요할 때만 읽는다.

## 2026-07-19 운영체계 감사에서 확인한 재사용 교훈

- 프로젝트 운영 문서의 최신성은 파일 존재 검사가 아니라 활성 참조와 설치 매핑을 함께 검사해야 한다.
- 발행본의 `CURRENT` 상태와 사람의 시각 검수 완료 상태는 서로 독립적으로 관리해야 한다.
- Learning Log는 모든 호출이 아니라 실패, 중요한 결정, 재사용 가능한 교훈, 실제 검증 결과가 있을 때 기록한다.
- 11개 분야는 공용 카탈로그이며 프로젝트가 선택하지 않은 분야를 필수 진입점으로 강제하지 않는다.
- 작업에 필요한 도구·파일·인증·권한이 없으면 사용자에게 이유와 설치·적용·확인 방법을 안내하고, 완료 통보 뒤 실제 환경을 다시 검증한다.

## 기록 원칙

- Skill을 호출했다는 이유만으로 본문을 매번 바꾸지 않는다.
- 실패, 중요한 결정, 재사용 가능한 교훈 또는 실제 검증 결과가 있는 실행을 기록한다.
- 반복 실패, 새 예외, 경로·도구·검증 변경이 발생하면 Skill 계약을 검토한다.
- 한 번의 성공은 `관찰` 또는 `가설`이다.
- 여러 조건에서 재현되기 전에는 `검증`이나 공용 강제 규칙으로 승격하지 않는다.
- 프로젝트 고유 이름·수치·파일 경로·승인 자산은 Base 로그에 복사하지 않는다.

## 2026-07-19 schema v3 발행 검증 교훈

- LibreOffice의 자동 TOC 필드는 headless PDF 변환에서 빈 목차가 될 수 있으므로 고정 섹션 목록을 직접 생성해야 한다.
- 구조화 JSON의 목록 항목은 상세 객체뿐 아니라 간단 문자열도 안전하게 렌더할 수 있어야 한다.
- Mermaid는 고정 CLI와 lockfile만으로 부족하며 브라우저 실행 경로도 사전 점검해야 한다.
- 강제 LibreOffice 재빌드의 플랫폼별 바이너리 동일성을 과장하지 않고, 동일 입력 정상 재실행 무재작성·diff 0을 공식 결정성 계약으로 둔다.
- 생성 실패를 대표 fixture에서 재현해 기존 PDF·Manifest 해시 보존을 확인해야 한다.

## 실행 기록 템플릿

```md
### [날짜] [skill_id]
- 프로젝트·작업:
- 기준 스킬 커밋:
- 호출 트리거:
- 입력 범위:
- 실제 산출물:
- 실행한 검증:
- 결과: 성공 / 부분 성공 / 실패 / 미검증
- 성공 조건:
- 실패·예외·재현 조건:
- 사용자 피드백:
- 불필요하게 호출한 스킬:
- 누락된 스킬·검증:
- 스킬 본문 변경 필요: 예 / 아니오
- 변경하지 않는 이유:
- 지식 상태: 관찰 / 가설 / 패턴 / 검증 / 승격 후보
- 프로젝트 전용으로 유지할 내용:
- Base Method·Skill·Template·Test 환류 후보:
- 다음 검토 트리거:
```

## 학습 상태 승격 기준

| 상태 | 최소 근거 | 허용 사용 |
|---|---|---|
| 관찰 | 1회 실행·피드백 | 참고만 가능 |
| 가설 | 원인·적용 조건·실패 조건 제시 | 제한적 시험 적용 |
| 패턴 | 서로 다른 작업에서 반복 | 프로젝트 권장 절차 |
| 검증 | 여러 조건에서 재현·회귀 검증 | Base 공용 계약 후보 |
| 승격 후보 | 프로젝트 독립성과 중복 검수 완료 | Method·Skill·Template·Test 반영 검토 |

## 정기 Health Review

다음 중 하나가 발생하면 `managing-game-project-operating-system`의 `verify` mode 또는 `evolving-project-discipline-skills`를 호출한다.

- 동일 실패가 두 번 이상 반복됨
- 90일 이상 검토 기록이 없음
- 등록된 Markdown 또는 JSON 책임 원본·실제 경로·검증 명령 변경
- 새 분야·반복 작업 유형 추가
- Skill 절차 중복
- 새 채팅이 필요한 Skill·기획서를 찾지 못함
- 과도한 Skill 호출
- PDF·다이어그램 발행본이 Registry보다 오래됨

## 기록

### 2026-07-21 project core and adversarial review skills

- 프로젝트·작업: 프로젝트 코어 판정, PLAN 단계 코어 확정, 적대적 검토·개선 루프를 독립 Skill로 추가
- 호출 트리거: 사용자가 사람도 이해하기 쉬운 컨텍스트를 Base Skill로 분리하고 기획 모드의 코어 확정 Skill을 추가하도록 요청
- 실제 산출물: `identifying-project-core`, `establishing-project-core`, `running-adversarial-review-and-refinement`, Registry·라우팅·회귀 동기화
- 실행한 검증: Registry Schema, Skill 패키지 1:1, 진입점 발견성, 구조 회귀, 정본 최신성 검사
- 결과: 부분 성공 — 공용 계약 추가, 실제 여러 프로젝트 적용은 미검증
- 성공 조건: 코어와 MVP를 구분하고, 사용자 승인 없이 코어를 확정하지 않으며, 레드팀 비판을 검증한 뒤 유효한 문제만 수정하고 회귀를 재검사함
- 실패·예외: 모든 중요 기능을 코어로 판정, 기술 부채를 불변 코어로 고정, 비판 전부 수용, 기능 팽창, 회귀 누락
- 지식 상태: 코어 판정은 관찰, 코어 확정과 적대적 개선 루프는 가설
- 다음 검토 트리거: 서로 다른 프로젝트 적용, 승인 없는 확정, 코어 과대 판정, 비판 과수용·기각 오류


### 2026-07-21 automatic Work Mode routing and legacy reconciliation

- 프로젝트·작업: Work Mode와 Skill Mode를 분리하고, 사용자 선언 없이 필요한 Skill을 자동 선택하며, 구형 파일을 안전하게 갱신·통합·아카이브·삭제하는 운영 계약 추가
- 기준 스킬 커밋: `agent/automatic-skill-routing-and-legacy-reconcile`
- 호출 트리거: Skill과 mode의 차이 확인, main 병합, 구형 파일 갱신·삭제 절차 확인, 별도 요청 없이 Skill 자동 사용과 사용 이유·결과 보고 요구
- 입력 범위: 통합 Skill Registry, 요청 접수 Skill, 운영체계 Skill, 정본 최신성 감사, 프로젝트 Registry 템플릿, 구조 회귀와 기존 Learning Log
- 실제 산출물: `PLAN/BUILD/REVIEW` Work Mode, Skill Mode 용어 계약, automatic-trigger-match 정책, `execution-report`, `reconcile-legacy`, Skill 실행 보고·구형 파일 정리 템플릿, Registry Schema와 구조 회귀
- 실행한 검증: Registry Schema·13개 활성 경로·Work Mode·자동 선택·구형 파일 판정·템플릿 존재 회귀를 추가했으며 GitHub Actions 전체 실행으로 최종 확인한다.
- 결과: 부분 성공 — 구조·계약·회귀 반영 완료, 실제 여러 프로젝트 적용은 미검증
- 성공 조건: 사용자가 Skill을 선언하지 않아도 최소 Skill·Skill Mode가 선택되고, 최종 보고에서 이유·결과·증거가 보이며, 구형 파일 삭제 전 고유 정보·참조·파생본·복구·승인이 확인됨
- 실패·예외·재현 조건: Work Mode와 Skill Mode 혼용, 모든 작업에서 과도한 Skill 보고, 파일명만 보고 구형본 삭제, 외부 호환 경로 제거, REVIEW에서 finding 없이 즉시 수정하는 위험
- 사용자 피드백: 의도 파악→해당 Mode→Skill 실행 구조가 최선인지 확인하고, Skill은 자동 사용되며 이유와 결과를 명시할 것
- 불필요하게 호출한 스킬: 신규 독립 구형 파일 정리 Skill은 만들지 않고 운영체계 Skill Mode로 통합함
- 누락된 스킬·검증: 실제 프로젝트의 버전 복제본·외부 링크·대형 바이너리·장기 호환성 사례
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 용어·라우팅 계약은 패턴 후보, 구형본 자동 판정은 관찰·가설
- 프로젝트 전용으로 유지할 내용: 실제 정본 경로, 삭제 승인자, 외부 소비자, 보존 기간, 호환 stub 정책
- Base Method·Skill·Template·Test 환류 후보: 이번 Work Mode 문서, 두 통합 Skill, Registry 정책, 두 템플릿과 구조 회귀
- 다음 검토 트리거: 첫 두 프로젝트 적용, 오라우팅, Skill 실행 보고 누락·과다, 오삭제, 호환 stub 누락, 사용자가 자동 선택 이유를 이해하지 못함

### 2026-07-21 benchmark, sequencing, playtest, accessibility and performance modes

- 프로젝트·작업: 게임 개발 벤치마크·유저 반응 조사, 작업 분해·순서, 플레이테스트·행동 계측, 접근성·성능 검증 공백을 기존 통합 Skill mode로 흡수
- 기준 스킬 커밋: `agent/add-reference-freshness-audit-v3`
- 호출 트리거: 벤치마킹 게임·유저 반응을 인터넷에서 조사해 분석·반영·개선하고, 작업 순서·스텝을 나누며, 추가로 필요한 게임 개발 스킬을 공식 자료에서 찾아 통합하라는 사용자 요청
- 입력 범위: PR #19 DDD 기준선, PR #22 정본 최신성 구조, Steamworks Reviews·Playtest·Testing, Unity Analytics Events·Funnels·A/B testing, Scrum Guide, GitHub Issues·Dependencies·Milestones, Xbox Accessibility Guidelines, Unreal performance profiling, Unity Edit·Play·target player test 문서
- 실제 산출물: `decompose-and-sequence`, `benchmark-and-player-research`, `playtest-and-experiment`, `accessibility-review`, `performance-profile`, Vertical Slice의 `slice-contract/quality-bar/pipeline-proof/playtest-evidence/decision-gate`, 3개 상세 reference, 2개 템플릿, Registry·Operating Model·프로젝트 Workflow·Skill Adoption Guide·회귀 테스트 동기화
- 실행한 검증: 독립 Skill 추가 없이 활성 Skill 13개 유지, mode·trigger·공식 출처·참조 파일·라우팅 회귀 추가, 전체 GitHub Actions 실행 대기
- 결과: 부분 성공
- 성공 조건: 벤치마크가 기능 복사가 아니라 근거 층위와 `ADOPT/ADAPT/AVOID/TEST/IGNORE` 결정으로 연결되고, 작업 단계가 의존성·게이트·롤백을 가지며, 플레이테스트·접근성·성능이 실제 증거 계약으로 연결됨
- 실패·예외·재현 조건: 리뷰 표본·버전·플랫폼 편향, 이벤트와 감정의 혼동, 한 실험에서 여러 변수 변경, 근거 없는 일정 추정, 접근성의 법적 준수 과장, 평균 FPS만으로 성능 통과를 주장할 위험이 있음
- 사용자 피드백: 위 두 기능은 각각 별도 Skill이 아니라 통합 mode로 추가하고, 인터넷에서 필요한 게임 개발·작업 스킬을 더 찾아 통합·참고·개선할 것
- 불필요하게 호출한 스킬: 없음. 신규 독립 Skill 2개 대신 기존 Intake·Concept·Validation·Vertical Slice 생명주기에 흡수함
- 누락된 스킬·검증: 실제 프로젝트의 리뷰 표본 코딩, 외부 Playtest 모집·피드백 회수, 실제 target hardware 프로파일과 접근성 사용자 검수
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 작업 분해 원리는 패턴, 벤치마크·플레이테스트·접근성·성능 통합 계약은 관찰·가설
- 프로젝트 전용으로 유지할 내용: 실제 비교 게임, 리뷰 데이터, 테스트 빌드·표본, 이벤트 Schema·퍼널, 장르별 목표 지표, 접근성 우선순위, 성능 예산·하드웨어
- Base Method·Skill·Template·Test 환류 후보: 이번 mode·reference·template·Registry·회귀 전체
- 다음 검토 트리거: 첫 두 프로젝트 적용, 오라우팅, 표본 편향, 실험 인과 오류, 작업 단계 과분해·과병렬화, 접근성·성능 검증 비용 과다

### 2026-07-21 Digital Dopamine Design definition and reward-analysis contract

- 프로젝트·작업: Base 기획 분석의 DDD 의미를 Digital Dopamine Design으로 확정하고 빠른 보상·즉각 피드백 분석 계약을 구체화
- 기준 스킬 커밋: `agent/consolidate-skills-and-structure@5679303d056a14bfeb41c8f3a35e2271815c3982`
- 호출 트리거: DDD는 빠른 시간 안에 사용자가 보상을 체감하도록 하는 도파민형 빠른 보상 요소라는 사용자 정의
- 입력 범위: `analyzing-and-refining-game-concepts`, GAME_CONCEPT_DIRECTION_REVIEW 템플릿, Base Skill Registry, 통합 Skill 참조 회귀 테스트
- 실제 산출물: DDD 프로젝트 정의, 첫 의미 있는 보상·행동 피드백·보상 명료성·밀도·보상 사다리·다음 행동·피로 분석축, PoC 관찰 필드, 위험 가드레일, `digital-dopamine-design`·`rapid-reward`·`instant-feedback`·`reward-latency` 라우팅 태그
- 실행한 검증: Registry Schema·활성 경로, DDD 정의·측정축·가드레일·템플릿·라우팅 회귀, Python 문법, Documentation·Skill Routing·Design Publication Governance, 전체 구조·생성 회귀 79개, Windows 실제 발행 스모크 테스트, whitespace
- 결과: 성공 — GitHub Actions run #73, 79 tests 성공·1 skipped, Windows 발행·whitespace 성공
- 성공 조건: DDD가 명확한 내부 용어와 관찰 가능한 설계축을 가지며, 뾰족한 재미를 단순 자극으로 대체하지 않고 외부 동명 약어와 구분됨
- 실패·예외·재현 조건: 최초 run #71에서 기존 회귀가 요구한 `임의 해석하지 않는다` 정확 문구가 새 표현에 없어 1건 실패했다. 의미를 바꾸지 않고 호환 문장을 복원한 뒤 run #72와 Learning Log 동기화 후 run #73에서 전체 통과했다.
- 사용자 피드백: DDD는 도파민 중독형 빠른 보상, 즉 빠른 시간 안에 사용자가 도파민성 보상을 느끼게 하는 요소를 의미함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 실제 게임의 첫 보상 시간·피드백 지연·다음 행동 전환과 장기 피로 데이터는 아직 없음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: DDD 용어 정의는 사용자 승인, 보상 설계 효과와 공용 목표 수치는 가설
- 프로젝트 전용으로 유지할 내용: 장르별 목표 시간, 보상 간격, 실제 UX·경제·연출, 플레이테스트 결과와 허용 자극 강도
- Base Method·Skill·Template·Test 환류 후보: DDD 측정 필드, PoC 관찰 계약, 자극 대 핵심 재미 판정, 위험 가드레일
- 다음 검토 트리거: 서로 다른 두 프로젝트 적용, 빠른 보상이 핵심 선택을 약화함, 보상 인플레이션·피로, 목표 수치 일반화 시도

### 2026-07-21 canonical reference freshness audit

- 프로젝트·작업: Base 변경 시 오래된 파일·경로·Skill ID·정책 참조와 갱신 누락을 찾는 전문 Skill·자동 검사 추가
- 기준 스킬 커밋: `agent/add-reference-freshness-audit-v3`
- 호출 트리거: 패치나 변경 뒤 모든 활성 파일이 최신 정본을 따르는지, 오래된 파일을 참조하거나 갱신되지 않은 소비자가 있는지 찾는 Skill을 추가하라는 사용자 요청
- 입력 범위: PR #19 최종 DDD head, 통합 Skill Registry, 범용 변경 검증 Skill, Operating Model, 프로젝트 AI Workflow, Legacy Alias, 구조·참조 회귀 테스트와 Actions
- 실제 산출물: `auditing-canonical-reference-freshness`, `reference-freshness` 검증 mode, 감사 템플릿, `.github/reference-freshness.json`, 표준 라이브러리 기반 checker, 단위 테스트와 CI 연결, 13개 활성 Skill Registry
- 실행한 검증: checker 단위 테스트 4개 추가, Registry·구조·활성 진입점 테스트 갱신, Python 문법·Actions 실행 대기
- 결과: 부분 성공
- 성공 조건: DDD 정의·라우팅·PoC 관찰 계약을 보존하면서 정본 변경 영향 지도, Legacy·History 허용, stale reference·content drift·파생본·untouched 소비자 검사와 자동 coupled-change 차단이 하나의 검증 흐름으로 연결됨
- 실패·예외·재현 조건: 문자열 검색만으로 의미 drift를 완전히 판정할 수 없으며, 프로젝트별 History 허용 glob과 coupled-change 규칙이 과도하면 오탐이 발생할 수 있음
- 사용자 피드백: 모든 파일이 최신 파일을 기준으로 내용을 따르는지와 오래된 파일 참조·갱신 누락을 찾아야 하며, 완료된 DDD 스킬과 최종 검증 결과를 기준선에 포함할 것
- 불필요하게 호출한 스킬: 없음. 범용 검증에 직접 흡수하지 않고 독립 자동화·증거가 있는 specialist로 유지함
- 누락된 스킬·검증: 실제 서로 다른 프로젝트의 rename·Schema·문서 통합 사례에서 오탐·누락률 검증
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 관찰
- 프로젝트 전용으로 유지할 내용: 실제 정본 경로, History 허용 범위, 프로젝트별 coupled-change 규칙과 파생본 정책
- Base Method·Skill·Template·Test 환류 후보: reference freshness config·checker·감사 템플릿·CI 게이트
- 다음 검토 트리거: 첫 두 프로젝트 적용, Legacy 오탐, stale reference 누락, coupled-change 과도 차단, Manifest가 CURRENT지만 실제 입력과 불일치

### 2026-07-21 concept analysis and unified project-change validation

- 프로젝트·작업: Base 핵심 컨셉·뾰족한 재미·PoC 기획 분석 스킬 추가와 외부 AI 검수의 범용 변경 검증 통합
- 기준 스킬 커밋: `agent/consolidate-skills-and-structure@e679219ab1e2f993602d9e928ddf98640b69df41`
- 호출 트리거: SWOT·DDD 요소 분석과 개선 방향, 핵심 컨셉→제약→뾰족한 재미→구체화→PoC→재조정→Production 흐름을 반복 가능한 스킬로 만들고 일반 변경 검증 공백을 해소하라는 사용자 요청
- 입력 범위: 활성 Skill Registry, Operating Model, START_HERE, AGENTS, Documentation Map, Workflow·Checklist, 프로젝트 템플릿, 기존 Vertical Slice·외부 AI 검수 스킬과 구조 회귀 테스트
- 실제 산출물: `analyzing-and-refining-game-concepts`, `reviewing-and-validating-project-changes`, 기획 방향·변경 검증 템플릿, 12개 활성 Skill Registry, Legacy Alias와 프로젝트 라우터 갱신
- 실행한 검증: Registry Schema·활성 경로, 12개 선택적 라우팅, 기획 8개 mode·7단계 상태 흐름·SWOT 전략·MDA/DDE·DDD 계약, 변경 검증 6개 mode·5개 판정, 삭제 경로·Legacy Alias·프로젝트 템플릿 참조, Python 문법·BCP·Documentation·Skill Routing·Design Publication Governance, 구조·생성 회귀 78개, Windows 실제 발행 스모크 테스트, whitespace
- 결과: 성공
- 성공 조건: 기존 기획 문서·Vertical Slice·UI 감사 경계를 보존하고 새 Skill의 trigger·mode·템플릿·라우팅·회귀·Actions가 통과함
- 실패·예외·재현 조건: `BIG BLIND`와 초기 미정의 `DDD`를 외부 표준 용어로 단정하지 않고 프로젝트 정의형 용어로 처리했다. 최초 큰 파일 생성 요청이 보안 판정 불명으로 차단돼 동일 기능의 표현을 축약해 재시도했다. 1차 Actions에서 기획 템플릿의 trailing whitespace 1건을 검출해 제거했으며 최종 run #67에서 전체 통과했다.
- 사용자 피드백: 핵심 컨셉과 지속 플레이 원동력 탐색, 모든 게임 요소의 정렬, PoC 결과 기반 기획 재조정, 7단계 Production 흐름을 포함할 것
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 실제 서로 다른 게임 프로젝트에서의 반복 적용 결과와 PoC 관찰 데이터는 아직 없음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 핵심 컨셉 분석은 가설, 범용 변경 검증은 패턴
- 프로젝트 전용으로 유지할 내용: 실제 게임의 컨셉 문장·SWOT 항목·DDD 목표·PoC 결과·수치·콘텐츠·Production 판정
- Base Method·Skill·Template·Test 환류 후보: 기획 방향 상태 머신, SWOT-to-action, DDD 정의 계약, 범용 검증 판정·증거 템플릿과 Legacy Alias
- 다음 검토 트리거: 첫 두 프로젝트 적용, PoC 범위 팽창, DDD 목표 오라우팅, SWOT 일반론화, 통합 검증 Skill 비대화

### 2026-07-21 consolidated Base skills and operating structure

- 프로젝트·작업: Base 활성 Skill과 공용 운영 문서 통합
- 기준 스킬 커밋: `main@eb40b912e5f5a0e4d369105a4f0a770e0a6179a9`
- 호출 트리거: 유사하거나 순차 의존하는 Skill·Method·Checklist가 과도해 최소 호출과 책임 원본 원칙을 위반한다는 사용자 검토
- 입력 범위: 활성 Skill 17개, Skill Registry, START_HERE, AGENTS, README, Documentation Map, 공용 Rules·Workflow·Checklist, 운영·마이그레이션·발행·Handoff·Skill Evolution Method
- 실제 산출물: 활성 Skill 11개, 통합 Skill 4개, Legacy Alias, 통합 Operating Model, 축소된 라우터·원칙 문서, 발행 정책 3단계와 정책 선택 생성 도구
- 실행한 검증: Python 문법, Base Skill Registry Schema·활성 경로, Legacy Alias·삭제 경로·잔여 템플릿 참조, Documentation·Skill Routing·Design Publication Governance, 정책 선택 생성기 통합, 구조·콜드 스타트·BCP·딥인터뷰·UI 감사·DOCX/PDF 생성 회귀 78개, Ubuntu와 Windows 실제 발행 검증, whitespace
- 결과: 성공
- 성공 조건: 기존 고유 절차 보존, 활성 이전 ID 제거, 새 ID 라우팅, 자동 검사·회귀·Actions 통과, 콜드 스타트에서 최소 Skill 탐색
- 실패·예외·재현 조건: 1차 CI에서 역인터뷰와 별도 구현 PR 계약 문구 2개가 불일치해 통합 Skill 표현을 정렬했다. 추가 감사에서 3단계 발행 정책이 기존 Schema의 `always_sync` 단일 허용과 충돌한 것을 발견해 Schema·정책 선택기·Governance·회귀 테스트까지 함께 구현했다.
- 사용자 피드백: 유사하거나 통합 가능한 Skill·구조를 합치고 통합 후 정상 작동과 추가 개선을 다시 점검할 것
- 불필요하게 호출한 스킬: 통합 후 요청 접수 Foundation 연쇄 호출 3개를 1개로 축소
- 누락된 스킬·검증: 실제 게임 프로젝트에 적용한 장기 사용성·오라우팅 빈도는 아직 프로젝트 검증 전
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 각 게임의 세계관·수치·실제 경로·승인 자산·프로젝트 Skill
- Base Method·Skill·Template·Test 환류 후보: 통합 Skill mode·Legacy Alias·발행 정책·정책 선택기·잔여 참조 회귀 검사
- 다음 검토 트리거: 첫 대상 프로젝트 적용, Legacy Alias 오라우팅, 하나의 통합 Skill이 과도하게 비대해짐, 3단계 발행 정책의 실제 운영 비용 불균형

### 2026-07-19 structured design documents and human publication pipeline

- 프로젝트·작업: Base PR #8 — 모든 프로젝트·분야 기획서의 AI JSON + 사람용 DOCX/PDF + 다이어그램·승인 이미지 구조
- 기준 스킬 커밋: `51d3535afa3eea5b19d262e1fe87d06f183c2224`
- 호출 트리거: 스킬맵뿐 아니라 모든 기획서가 이미지 확인 가능한 사람용 문서를 가져야 한다는 사용자 피드백
- 입력 범위: Base 시작 규칙·운영 Method·기획서 작성·마이그레이션·발행·스킬 진화·Health Review·프로젝트 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: Design Document Registry·JSON 본책 템플릿·DOCX/PDF·다이어그램 생성기·승인 이미지 포함·세 번째 Governance Checker·실제 생성 통합 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Design Publication Governance, JSON 기획서와 Skill Registry의 DOCX/PDF·다이어그램 실제 생성, 승인 이미지 포함, PDF 전 페이지 렌더, 구조 회귀, whitespace
- 결과: 성공
- 성공 조건: 기획서·스킬맵 실제 생성, 세 Governance Checker, 구조 회귀, PDF 렌더와 whitespace가 최종 head의 GitHub Actions run #18에서 모두 통과
- 실패·예외·재현 조건: 초기 CI에서 pip 캐시 입력 파일 부재로 Python 설정이 실패해 캐시를 제거함. 다음 실행에서 Skill 진화 Method와 Health Review Skill 연결 문구 누락이 구조 테스트에 검출돼 계약을 보완함.
- 사용자 피드백: AI는 JSON을 읽고 사람은 DOCX/PDF와 이미지·다이어그램을 한눈에 확인해야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 기존 구조에는 프로젝트 전체·분야 기획서용 구조화 Registry, 승인 이미지 포함 DOCX, 생성기 해시와 전 페이지 PDF 렌더 검사가 없었음
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 실제 게임의 세계관·수치·구현 경로·승인 이미지·생성된 기획서 바이너리
- Base Method·Skill·Template·Test 환류 후보: 이번 PR의 JSON 계약·생성기·Checker·통합 테스트 전체
- 다음 검토 트리거: 첫 대상 프로젝트 실제 마이그레이션, DOCX/PDF 렌더 실패 반복, Registry와 발행본 불일치

### 2026-07-19 operating-system skill routing and learning audit

- 프로젝트·작업: Base PR #7 — 선택적 Skill 호출·지속 학습·루트 `[기획서]` 검수
- 기준 스킬 커밋: `c65ffe2e589caf8e38c546dbdfcd37e669b09f9f`
- 호출 트리거: 분야별·Foundation Skill의 항상 학습, 필요한 경우에만 호출, 운영체계 연결 검증, 루트 `[기획서]` 요청
- 입력 범위: Base START_HERE·AGENTS·README·Documentation Map·운영체계 Method·Installer·Project Operations 템플릿·GitHub 검사·회귀 테스트
- 실제 산출물: 공용·프로젝트 Skill Registry, 라우팅·Handoff·Health Review Skill, Learning Log 계약, 루트 기획서·Registry 자동 검사와 회귀 테스트
- 실행한 검증: Python 문법, Documentation Governance, Skill Routing Governance, Base 구조 테스트, `git diff --check`
- 결과: 성공
- 성공 조건: Registry·루트 기획서·동기화 실패 테스트와 whitespace 정상
- 실패·예외·재현 조건: `[기획서]` 대괄호 glob 해석 문제를 실제 폴더명 비교로 수정
- 사용자 피드백: Skill이 항상 학습 가능하고 필요한 때만 호출되며 활성 기획서는 최상위 폴더에서 보여야 함
- 불필요하게 호출한 스킬: 없음
- 누락된 스킬·검증: 요청 라우팅, Context·Handoff, Health Review와 Skill Registry 검사
- 스킬 본문 변경 필요: 예
- 변경하지 않는 이유: 해당 없음
- 지식 상태: 패턴
- 프로젝트 전용으로 유지할 내용: 대상 게임의 구체 Skill·실제 경로·승인 자산
- Base Method·Skill·Template·Test 환류 후보: Method·Skill·Registry·Health Report·Checker·회귀 테스트
- 다음 검토 트리거: 대상 프로젝트 첫 실제 적용, 동일 라우팅 실패 반복, 90일 이상 미검토
