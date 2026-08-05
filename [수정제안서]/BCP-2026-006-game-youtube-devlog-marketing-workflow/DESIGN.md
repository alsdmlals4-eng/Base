# 게임 개발 YouTube 개발일지·마케팅 Skill 설계

- 상태: `PROPOSED_DESIGN`
- 사용자 방향 승인: `2026-08-05 — 독립 전문 Skill과 BCP 분리 생명주기 권장안 승인`
- 기준 Base main: `5e23aaad85842505e009fa7f1872e70576ef59f0`
- Work Mode: `PLAN`
- BCP: `BCP-2026-006-game-youtube-devlog-marketing-workflow`
- 활성 구현: `NOT_STARTED`
- 실제 영상 Pilot: `NOT_RUN`
- 사람 시청자 검증: `HUMAN_NOT_RUN`

## 1. 목적

여러 게임 프로젝트를 운영하는 1인 또는 소규모 개발자가 게임 개발 과정과 실제 빌드를 YouTube 장문 영상·Shorts·출시 홍보 콘텐츠로 변환할 때, 단순 작업일지나 특정 크리에이터 모방에 빠지지 않고 시청자 가치와 게임 마케팅 전환을 함께 관리하는 반복 가능한 제작 계약을 제공한다.

이 설계의 기본 채널 전략은 다음과 같다.

```text
스튜디오 통합 채널 1개
→ 프로젝트별 재생목록·홈 섹션
→ 장문 개발일지·Shorts·트레일러의 역할 분리
→ 데이터와 운영 필요가 입증된 성공 IP만 별도 채널 검토
```

## 2. 책임 경계

### 새 전문 Skill

```text
producing-game-development-youtube-videos
```

이 Skill은 다음 전체 흐름을 단일 주 책임으로 소유한다.

```text
channel-portfolio
→ episode-concept
→ script-and-shot-plan
→ title-thumbnail-package
→ production-and-publish
→ analytics-review
```

### 기존 Skill 연결

- `managing-project-intake-and-work-contract`: 요청 범위·시청자·영상 목적·승인·실행 계약
- `analyzing-and-refining-game-concepts`: 게임의 핵심 재미·플레이어 약속·비교 근거
- `designing-vertical-slices`: 공개 가능한 대표 빌드와 Quality Bar
- `designing-art-prompts-and-technique-cards`: 썸네일 후보 이미지·홍보 시각 후보
- `reviewing-and-validating-project-changes`: 실제 빌드·링크·공개 상태·권리 증거 검증
- `running-adversarial-review-and-refinement`: 클릭베이트·과장·권리·보안·스포일러·KPI 왜곡 공격
- `auditing-canonical-reference-freshness`: Registry·entrypoint·Guide·Template·Test 전파

새 Skill은 게임 자체 기획, 썸네일 이미지 생성, 플랫폼 심사, 자산 권리 원장 또는 일반 사용자 학습 노트의 책임을 빼앗지 않는다.

## 3. 입력 계약

```yaml
project_canon_and_current_decisions:
actual_build_version_and_capture_date:
public_implementation_status:
target_viewer:
episode_job: DISCOVERY | TRUST | SEARCH | CONVERSION | RETENTION
one_sentence_promise:
conflict_change_or_visible_result:
marketing_stage:
primary_cta:
secondary_cta_optional:
channel_and_playlist_context:
spoiler_confidentiality_security_limits:
available_footage_and_assets:
asset_rights_and_licenses:
production_time_budget:
publish_window_and_dependencies:
analytics_access_and_external_conversion_tracking:
```

입력이 없을 때의 처리:

- 실제 빌드 또는 정본 부재: `BLOCKED_UNVERIFIED`
- 공개 범위 불명: `PUBLICATION_BOUNDARY_UNVERIFIED`
- 자산 권리 불명: `RIGHTS_UNVERIFIED`
- 외부 전환 추적 부재: `CONVERSION_UNVERIFIED`
- 사람 시청 데이터 부재: `HUMAN_NOT_RUN`

## 4. Mode 설계

### `channel-portfolio`

목적:

- 스튜디오 통합 채널의 정체성과 대상 시청자를 정의한다.
- 프로젝트별 재생목록·홈 섹션·썸네일 식별 체계를 설계한다.
- 장문·Shorts·트레일러·라이브의 역할을 분리한다.
- 채널 분리 조건을 데이터와 운영 필요로 판단한다.

산출물:

- 채널 한 문장 약속
- 프로젝트별 재생목록 지도
- 홈 섹션 우선순위
- 공통 브랜드와 프로젝트 식별 요소
- 성공 IP 별도 채널 검토 Gate

### `episode-concept`

목적:

한 편의 영상이 누구에게 어떤 가치를 제공하고 어떤 게임 행동으로 이어질지 확정한다.

규칙:

- 주 시청자 1개
- Episode Job 1개
- 한 문장 약속 1개
- 주 갈등·변화·결과 1개
- 주 CTA 1개

영상화하지 않을 조건:

- 화면으로 보여줄 변화나 판단 가치가 없음
- 내부 작업 목록만 존재함
- 실제 게임 개발보다 제작비가 큼
- 공개 위험이 가치보다 큼
- 기존 영상과 차별되는 질문이 없음

### `script-and-shot-plan`

기본 구조:

```text
0~10초: 결과·갈등·실패·비포/애프터
→ 시청자가 이해해야 할 문제
→ 기존 방식의 한계
→ 시도·실패·선택
→ 실제 빌드 결과
→ 남은 문제·다음 단계
→ CTA 또는 구체적 질문
```

변형:

- 검색형: 질문·결과 → 조건 → 해결 과정 → 한계 → 적용
- Shorts: 한 변화 → 즉시 결과 → 짧은 맥락 → 루프 가능한 끝
- 출시 공지: 핵심 판타지 → 플레이 증거 → 출시 정보 → CTA

모든 주장과 화면은 실제 빌드 버전·캡처 날짜·상태로 추적한다.

### `title-thumbnail-package`

패키지마다 다음을 만든다.

- 제목 후보 3개 이내
- 썸네일 콘셉트 3개 이내
- 제목·썸네일이 함께 만드는 질문
- 영상 첫 30초가 약속을 어떻게 충족하는지
- 오해·클릭베이트·스포일러 위험
- 작은 화면 가독성
- 프로젝트 식별과 채널 일관성

규칙:

- 실제 내용과 정확히 일치
- 중요한 변화·문제·결과를 앞쪽에 배치
- Devlog 번호·스튜디오 브랜딩은 뒤쪽 보조 정보
- 한 썸네일에 단일 초점
- 특정 벤치마크 채널의 식별 가능한 구성 복제 금지
- 장문 영상에서 기능이 지원되면 충분히 다른 조합을 A/B 테스트
- Shorts에는 지원되지 않는 A/B 기능을 가정하지 않음

### `production-and-publish`

제작 Packet:

- 촬영·캡처 샷리스트
- 내레이션·자막 대본
- B-roll·UI·그래프·비교 장면
- 편집 비트·음향·음악 계획
- 설명란·챕터·고정댓글
- 재생목록·엔드스크린·카드
- Shorts 파생 후보
- 공개 전 권리·보안·스포일러·정확성 체크
- 실제 게시 URL·버전·게시 시각

게시 Gate:

```text
actual_build_verified
and title_thumbnail_promise_match
and rights_verified
and no_secret_or_private_data
and spoiler_boundary_approved
and primary_cta_live
```

### `analytics-review`

영상 목적별로 결과 전에 관찰값을 정한다.

공통 관찰:

- 노출 경로와 대상 시청자
- 첫 30초 유지
- 이탈·재시청·공유 구간
- 신규·일반·정기 시청자
- 프로젝트 재생목록 이동
- 설명란·고정댓글·엔드스크린 클릭
- 가능한 데모·알림·후원·위시리스트·구매 전환
- 영상 제작시간과 게임 개발 지연 비용

판정:

- `KEEP`: 반복할 가치가 있는 검증된 요소
- `CHANGE`: 수정 가설과 다음 실험이 필요한 요소
- `STOP`: 비용·위험·전환 기준상 중단할 형식
- `INSUFFICIENT_SAMPLE`: 표본 부족
- `CONVERSION_UNVERIFIED`: 하위 전환 미측정
- `HUMAN_NOT_RUN`: 실제 시청자 데이터 없음

조회수나 CTR 단독으로 게임 마케팅 성공을 판정하지 않는다.

## 5. 프로젝트용 Episode Packet

```md
# Game Development YouTube Episode Packet

## Project and build evidence
## Target viewer and episode job
## One-sentence promise
## Conflict, change, and visible result
## Marketing stage and primary CTA
## Spoiler, confidentiality, security, and rights limits
## Hook alternatives
## Script
## Shot list and capture evidence
## Edit beat sheet
## Title and thumbnail packages
## Description, chapters, pinned comment, playlist, and end screen
## Shorts derivatives
## Pre-publish adversarial review
## Publish record
## Analytics precommit
## Analytics result and sample limits
## KEEP / CHANGE / STOP / INSUFFICIENT_SAMPLE
## Learning and next experiment
```

프로젝트 저장소에 실제 Episode Packet을 두고, Base는 공용 Template과 방법론만 소유한다.

## 6. Benchmark 사용 계약

벤치마크는 특정 크리에이터의 표현을 복제하는 목록이 아니다.

각 사례는 다음 항목으로 기록한다.

```yaml
source_channel_and_url:
observed_date:
video_or_short_format:
target_viewer_inference:
opening_promise:
conflict_or_result:
title_thumbnail_relationship:
editing_and_visual_evidence:
cta_and_destination:
likely_strength:
possible_failure_or_bias:
ADOPT_ADAPT_AVOID_TEST_IGNORE:
project_specific_translation:
```

반드시 성공 사례뿐 아니라 실패·혼합 가능성, 표본 편향, 장르·언어·채널 규모 차이를 함께 기록한다.

## 7. 보호·안전 계약

### 정확성

- 미구현·기획·실험·확정 상태를 구분한다.
- 영상 편집으로 결과를 과장하거나 정상 플레이처럼 위장하지 않는다.
- 로드맵 약속은 승인된 범위·조건·변경 가능성을 표시한다.

### 권리

- 음악·효과음·폰트·이미지·영상·게임 에셋의 사용 조건을 확인한다.
- 레퍼런스는 기능·원리만 분석하고 표현을 복제하지 않는다.
- 게임 내 제3자 IP 또는 계약상 비공개 자산을 노출하지 않는다.

### 보안·개인정보

- API 키, 토큰, 계정 정보, 로컬 경로, 개인 이메일, 결제·정산 정보, 비공개 저장소·대화·문서를 가린다.
- 캡처 전 별도 공개용 환경 또는 보안 체크를 사용한다.

### 개발 지속 가능성

- Episode Brief에서 제작시간 상한을 정한다.
- 영상 제작이 승인된 게임 개발 Gate를 지연시키면 범위를 줄이거나 보류한다.
- 모든 개발 작업을 영상화하지 않는다.

## 8. 적대적 검토

필수 실패 가정:

- 채널은 성장하지만 게임 관심자는 늘지 않는다.
- 제목과 썸네일은 클릭되지만 첫 30초에서 약속이 깨진다.
- 특정 유튜버의 성공 공식을 표면 복제한다.
- 여러 프로젝트가 섞여 시청자가 채널 정체성을 이해하지 못한다.
- Shorts 조회수 때문에 장문·데모·후원 전환이 왜곡된다.
- 개발 공개가 스포일러·권리·보안 사고를 만든다.
- 영상 제작이 게임 개발을 잠식한다.
- 표본이 작은데 절대 KPI를 확정한다.
- 이미 성공한 채널의 생존자 편향을 일반 규칙으로 만든다.

Finding 분류:

- `MUST_FIX`
- `SHOULD_FIX`
- `USER_DECISION_REQUIRED`
- `DEFER`
- `REJECTED_CRITIQUE`
- `BLOCKED_UNVERIFIED`

## 9. 구현 구조 후보

```text
skills/producing-game-development-youtube-videos/
├─ SKILL.md
└─ LEARNING_LOG.md (필요성은 구현 계획에서 기존 공용 Log와 비교)

docs/knowledge/game-development/
└─ GAME_DEVELOPMENT_YOUTUBE_PRODUCTION_GUIDE.md

templates/marketing/
└─ GAME_DEVELOPMENT_YOUTUBE_EPISODE_PACKET.md

tests/
└─ test_game_development_youtube_workflow_contract.py
```

연결 소비자:

- `START_HERE.md`
- `docs/knowledge/game-development/README.md`
- `skills/SKILL_REGISTRY.json`
- `skills/SKILL_COVERAGE.json`
- `skills/SKILL_BEHAVIOR_EVALS.json`
- `skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json`
- `skills/SKILL_IMPLEMENTATION_EVIDENCE.json`
- `skills/SKILL_LEARNING_LOG.md`
- generated active Skill·implementation evidence view
- canonical-reference freshness와 필요한 CI suite

구현 계획은 현재 main과 release lock을 다시 읽어 실제 변경 파일을 최소화한다.

## 10. 검증 설계

### TDD

1. 신규 계약 경로와 핵심 문자열 부재를 실패시키는 focused test 작성
2. RED 실행·원인 기록
3. Skill·Guide·Template 최소 구현
4. Registry·entrypoint·coverage·behavior·evidence 연결
5. focused GREEN
6. Base 관련 전체 suite
7. exact-HEAD CI

### Behavior Eval

Primary:

> 여러 게임을 하나의 스튜디오 채널에서 운영한다. 특정 프로젝트의 실제 최신 빌드와 공개 범위를 확인하고 다음 개발일지 영상의 대상 시청자, 한 문장 약속, 대본, 샷리스트, 제목·썸네일 후보, CTA, 게시 체크와 분석 계획을 만들어 달라.

Non-selection:

> 이 게임의 전투 시스템과 난이도 곡선을 설계해 달라.

> 이미 승인된 캐릭터 이미지로 YouTube 썸네일 후보 이미지만 생성해 달라.

> 게시된 영상 설명란의 오탈자 하나만 고쳐 달라.

> 유명 개발 유튜버와 똑같은 썸네일과 대본을 만들어 달라.

실제 모델 결과가 없으면 fixture 유효성만 검증하고 `MODEL_RUN_STATUS: NOT_RUN`으로 둔다.

### Human Pilot

최소 하나의 실제 프로젝트에서 다음을 수행하기 전 효과 검증을 주장하지 않는다.

- Episode Packet 작성
- 영상 제작·게시
- 최소 비교 가능한 Analytics 기간 확보
- 첫 30초·이탈 구간·CTA 이동 확인
- 제작시간 비용 기록
- 프로젝트별 다음 실험 결정

## 11. 설계 선택과 기각안

### 채택: 독립 전문 Skill

이유:

- 독립 입력·산출물·도구·Quality Bar·실패 조건이 있다.
- 여러 게임 프로젝트에서 반복 사용한다.
- 기존 게임 기획 Skill에 흡수하면 과대 책임이 된다.
- Guide만으로는 자동 라우팅과 게시 후 학습 책임이 약하다.

### 기각: `analyzing-and-refining-game-concepts`의 mode

게임의 핵심 재미·시스템 설계와 영상 대본·편집·게시·Analytics의 책임 경계가 다르다.

### 기각: Guide·Template만 추가

실제 요청에서 전체 제작 Workflow를 소유할 주 Skill이 없어 Foundation·아트·검증 Skill이 임의 조합될 위험이 있다.

## 12. 완료 기준

제안 단계 완료:

- BCP Proposal과 이 설계가 `[수정제안서]` 안에만 존재한다.
- Proposal Registry에 동일 ID·상태·경로가 연결된다.
- 활성 Skill·Registry·Template·release lock은 변경하지 않는다.
- 중복·반례·위험·비사용 조건·롤백이 명시된다.
- 사용자가 written design을 검토할 수 있는 Draft PR이 생성된다.

구현 단계 완료는 별도 승인·계획·PR에서 판단한다.

## 13. 자체 검토

- Placeholder: 없음
- 상충: 독립 Skill 소유와 기존 Skill 지원 경계가 분리됨
- 범위: Proposal·설계만 포함, 활성 구현 제외
- 모호성: 영상 유형별 변형을 허용하되 공통 정확성·권리·실제 빌드 Gate는 강제
- 미검증: 실제 모델 행동·영상 제작·사람 반응·전환 효과를 명시적으로 미검증 유지
