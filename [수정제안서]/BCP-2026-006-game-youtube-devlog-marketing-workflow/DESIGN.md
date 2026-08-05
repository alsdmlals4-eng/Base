# 게임 개발 YouTube 개발일지·마케팅 Skill 설계

- 상태: `APPROVED_DESIGN`
- 사용자 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204`
- 기준 Base main: `48273f79ab261a1f064adfc7431c99a74a22c33a`
- Work Mode: `PLAN`
- BCP: `BCP-2026-006-game-youtube-devlog-marketing-workflow`
- 활성 구현: `NOT_STARTED`
- 실제 영상 Pilot: `NOT_RUN`
- 사람 시청자 검증: `HUMAN_NOT_RUN`

## 1. 목적

게임 프로젝트의 실제 정본·빌드·공개 가능 범위를 복원한 뒤, YouTube 개발일지·Shorts·기능 공개·출시 홍보 영상을 다음 폐쇄 루프로 생산한다.

```text
채널 포트폴리오
→ 에피소드 역할·약속
→ 대본·샷·편집 설계
→ 제목·썸네일 패키지
→ 공개 전 검증·게시
→ Analytics·전환·제작비 학습
→ 다음 실험
```

기본 포트폴리오:

```text
스튜디오 통합 채널
→ 프로젝트별 재생목록·홈 섹션
→ 장문 개발일지 / Shorts / 트레일러 역할 분리
→ 독립 팬덤·지속 업로드·운영 필요가 입증된 IP만 별도 채널 검토
```

## 2. 책임 구조

주 책임 Skill:

```text
producing-game-development-youtube-videos
```

Modes:

```text
channel-portfolio
→ episode-concept
→ script-and-shot-plan
→ title-thumbnail-package
→ production-and-publish
→ analytics-review
```

지원 책임:

- `managing-project-intake-and-work-contract`: 목표·범위·승인·완료 기준
- `analyzing-and-refining-game-concepts`: 핵심 재미·플레이어 약속
- `designing-vertical-slices`: 공개할 대표 빌드·Quality Bar
- `designing-art-prompts-and-technique-cards`: 승인된 썸네일 후보 이미지 제작
- 플랫폼 심사·에셋 권리 Workflow: 등급·출처·라이선스·reference-to-original 안전성
- `reviewing-and-validating-project-changes`: 실제 빌드·링크·권리·게시 상태 검증
- `running-adversarial-review-and-refinement`: 클릭베이트·과장·보안·KPI 왜곡 공격
- `auditing-canonical-reference-freshness`: Registry·Guide·Template·Test 소비자 전파

비소유:

- 게임 자체 기획·밸런스
- 썸네일 이미지 생성
- 플랫폼 심사와 에셋 권리 원장
- 영상 편집 도구의 실제 조작
- 프로젝트별 브랜딩·세계관·KPI 절대값

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
channel_and_playlist_context:
spoiler_confidentiality_security_limits:
available_footage_and_assets:
asset_rights_rating_and_licenses:
production_time_budget:
publish_window_and_dependencies:
analytics_access_and_external_conversion_tracking:
```

차단 상태:

- 정본·실제 빌드 부재: `BLOCKED_UNVERIFIED`
- 공개 범위 불명: `PUBLICATION_BOUNDARY_UNVERIFIED`
- 권리·등급 불명: `RIGHTS_OR_RATING_UNVERIFIED`
- 외부 CTA 추적 부재: `CONVERSION_UNVERIFIED`
- 실제 시청 데이터 부재: `HUMAN_NOT_RUN`

## 4. Mode 계약

### 4.1 `channel-portfolio`

정의:

- 스튜디오 채널의 대상 시청자와 한 문장 약속
- 프로젝트별 재생목록·홈 섹션
- 공통 브랜드와 프로젝트별 식별 요소
- 장문·Shorts·트레일러의 역할
- 채널 분리 검토 Gate

별도 채널 검토 조건:

- 해당 IP만으로 지속적인 업로드가 가능함
- 독립 팬덤과 커뮤니티 운영 요구가 확인됨
- 다른 프로젝트 영상이 기존 시청자 만족을 반복적으로 떨어뜨림
- 분리 후 운영 비용을 감당할 수 있음

### 4.2 `episode-concept`

한 영상에 우선하는 것:

- 주 시청자 1개
- Episode Job 1개
- 한 문장 약속 1개
- 핵심 갈등·변화·결과 1개
- 주 CTA 1개

Episode Job:

- `DISCOVERY`: 신규 시청자 발견
- `TRUST`: 판단·실패·개선 과정으로 신뢰 형성
- `SEARCH`: 제작·기술 질문의 검색 유입
- `CONVERSION`: 데모·알림·위시리스트·후원·구매 행동
- `RETENTION`: 기존 팬에게 진행도·업데이트·다음 기대 제공

보류 조건:

- 보여줄 실제 변화나 판단 가치가 없음
- 내부 작업 목록만 존재함
- 공개 위험이 기대 가치보다 큼
- 제작비가 게임 개발 가치보다 큼
- 기존 영상과 같은 질문을 반복함

### 4.3 `script-and-shot-plan`

장문 기본 구조:

```text
0~10초: 결과·갈등·실패·비포/애프터
→ 시청자가 이해해야 할 문제
→ 기존 방식의 한계
→ 시도·실패·선택
→ 실제 빌드 결과
→ 남은 문제와 다음 단계
→ 주 CTA 또는 구체적 질문
```

조건부 변형:

- 검색형: 질문·결과 → 조건 → 해결 과정 → 한계 → 적용
- Shorts: 한 변화 → 즉시 결과 → 최소 맥락 → 반복 가능한 끝
- 출시 공지: 핵심 판타지 → 플레이 증거 → 출시 정보 → CTA

모든 주장과 장면은 실제 빌드 버전·캡처 날짜·상태에 연결하고 기획·실험·부분 구현·완료를 구분한다.

### 4.4 `title-thumbnail-package`

필드:

- 제목 후보
- 썸네일 콘셉트
- 제목과 썸네일이 만드는 질문
- 첫 30초에서 약속을 충족하는 장면
- 클릭베이트·오해·스포일러 위험
- 작은 화면의 단일 초점과 가독성
- 프로젝트 식별 요소

규칙:

- 실제 콘텐츠에 없는 결과를 약속하지 않는다.
- 게임명·Devlog 번호보다 변화·문제·결과를 앞세운다.
- 특정 채널의 식별 가능한 문구·구도·캐릭터 배치를 복제하지 않는다.
- 기능이 지원될 때만 충분히 다른 패키지를 실험한다.
- CTR 단독이 아니라 시청시간·유지·하위 전환을 함께 해석한다.

### 4.5 `production-and-publish`

제작 Packet:

- 캡처·촬영 샷리스트와 증거 버전
- 내레이션·자막 대본
- B-roll·UI·비교 장면
- 편집 비트·음악·효과음 계획
- 설명란·챕터·고정 댓글
- 재생목록·엔드스크린 연결
- Shorts 파생 후보
- 공개 전 정확성·권리·등급·스포일러·보안 검사
- 게시 URL·버전·게시 시각

게시 Gate:

```text
ACTUAL_BUILD_VERIFIED
and TITLE_THUMBNAIL_PROMISE_MATCH
and RIGHTS_AND_RATING_VERIFIED
and NO_SECRET_OR_PRIVATE_DATA
and SPOILER_BOUNDARY_APPROVED
and PRIMARY_CTA_LIVE
```

### 4.6 `analytics-review`

공통 관찰:

- 노출 경로와 대상 시청자
- 첫 30초 유지
- 이탈·재시청·공유 구간
- 신규·일반·정기 시청자
- 프로젝트 재생목록·다음 영상 이동
- 설명란·고정댓글·엔드스크린 클릭
- 데모·알림·후원·위시리스트·구매 등 하위 전환
- 영상 제작시간과 게임 개발 지연 비용

판정:

- `KEEP`
- `CHANGE`
- `STOP`
- `INSUFFICIENT_SAMPLE`
- `CONVERSION_UNVERIFIED`
- `HUMAN_NOT_RUN`

조회수·CTR·Shorts 노출 하나만으로 게임 마케팅 성공을 확정하지 않는다.

## 5. Episode Packet

```md
# Game Development YouTube Episode Packet

## Project canon and actual build evidence
## Target viewer and episode job
## One-sentence promise
## Conflict, change, and visible result
## Marketing stage and primary CTA
## Spoiler, confidentiality, security, rights, and rating limits
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

Base는 공용 Template과 방법론만 소유한다. 실제 Packet은 프로젝트 저장소에 둔다.

## 6. 벤치마크 계약

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

원칙:

- 성공·실패·혼합 가능성을 함께 본다.
- 장르·언어·출시 상태·채널 규모 차이를 기록한다.
- 조회수만으로 원인과 효과를 확정하지 않는다.
- 구조적 원리만 `ADAPT`하며 표현은 새로 제작한다.

## 7. 보호 계약

정확성:

- 미구현·기획·실험·부분 구현·확정을 구분한다.
- 편집으로 결과를 정상 플레이처럼 위장하지 않는다.
- 로드맵 약속은 승인 범위·조건·변경 가능성을 표시한다.

권리·등급:

- 음악·효과음·폰트·이미지·영상·게임 에셋의 사용 조건을 확인한다.
- 플랫폼 심사·에셋 권리 Workflow의 provenance와 reference-to-original 규칙을 재사용한다.
- 등급 또는 공개 제한에 영향을 주는 장면은 공개 전 확인한다.

보안·개인정보:

- API 키, 토큰, 계정 정보, 개인 이메일, 결제·정산 정보, 비공개 저장소·대화·문서를 가린다.
- 캡처 전 공개용 환경 또는 보안 체크를 사용한다.

개발 지속 가능성:

- 제작 전 시간 예산을 고정한다.
- 재사용 가능한 캡처·자막·설명란 Template을 사용한다.
- 영상 제작이 핵심 개발을 반복 지연하면 빈도·길이·편집 복잡도를 낮춘다.

## 8. 검증 Matrix

기준:

- 실제 빌드·정본·공개 범위가 있는 개발일지

대표 변형:

- 검색형 기술 영상
- Shorts
- 출시 공지
- 여러 프로젝트가 있는 통합 채널

반례:

- 보여줄 변화가 없는 작업 목록
- 권리·등급·스포일러·보안 미확인
- 미구현 기능을 완료처럼 표현
- 특정 유튜버의 식별 가능한 표현 복제
- 표본이 작은 Analytics
- 조회수·CTR만 높은 영상
- 제작비가 게임 개발 가치를 초과한 영상
- 채널 분리 조건이 없는 신규 프로젝트

회귀:

- 기존 게임 기획·Vertical Slice·아트·권리·검증 Skill의 책임을 침범하지 않음
- Registry·Route·학습 로그·행동 Eval·문서 소비자가 동기화됨
- 제안 PR과 구현 PR이 분리됨
- `approval_ref`와 구현 PR이 추적됨

## 9. 구현 경계

최소 후보:

```text
skills/producing-game-development-youtube-videos/SKILL.md
templates/game-development-youtube/EPISODE_PACKET.md
skills/SKILL_REGISTRY.json
skills/SKILL_LEARNING_LOG.md
skills/SKILL_BEHAVIOR_EVALS.json
skills/BASE_SHARED_SKILL_ROUTES.json
tests/test_game_development_youtube_skill.py
tests/test_skill_package_integrity.py
tests/test_skill_routing_governance.py
docs/OPERATING_MODEL.md 또는 최소 책임 소비자
```

최신 결합 변경 규칙을 읽어 실제 파일 범위를 최소화한다.

구현하지 않는 것:

- YouTube API 자동 업로드
- 영상 편집기 자동 조작
- 프로젝트별 실제 Episode Packet
- 프로젝트별 KPI 절대값
- 특정 크리에이터 스타일 복제
- 실전 성과의 확정 주장

## 10. 완료 조건

정적 완료:

- Skill·Template·Registry·Route·학습 로그·행동 Eval·문서 소비자가 동기화됨
- 기준·대표·변형·반례·회귀 테스트 통과
- 제안·승인·구현 PR 연결 완료
- rollback 단위와 미검증 상태 명시

별도 실전 Gate:

```yaml
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```
