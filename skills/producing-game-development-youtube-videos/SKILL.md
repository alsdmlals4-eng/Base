---
name: producing-game-development-youtube-videos
description: Use when a verified actual build must become a truthful YouTube devlog, Short, feature reveal, or release-marketing episode with scripts, shots, packaging, publication gates, and sample-limited analytics learning.
---

# 게임 개발 YouTube 개발일지·마케팅 영상 제작

## 목적과 권한 경계

이 Skill은 게임 프로젝트의 실제 정본·현재 빌드·공개 가능 범위를 바탕으로 YouTube 개발일지, Shorts, 기능 공개, 출시 홍보 영상의 **채널 구조 → 에피소드 약속 → 대본·샷 → 제목·썸네일 패키지 → 공개 전 검증 → 게시 후 학습**을 설계한다.

핵심 계약은 다음과 같다.

```text
PROJECT_CANON_AND_ACTUAL_BUILD_FIRST
→ ONE_VIEWER_JOB
→ ONE_EPISODE_PROMISE
→ RESULT_OR_CONFLICT_FIRST
→ ACTUAL_BUILD_EVIDENCE
→ TITLE_THUMBNAIL_PROMISE_MATCH
→ RIGHTS_RATING_SPOILER_SECURITY_REVIEW
→ ONE_PRIMARY_CTA
→ PUBLISH
→ ANALYTICS_WITH_SAMPLE_LIMITS
→ LEARNING_AND_NEXT_EXPERIMENT
```

이 Skill은 다음 책임을 소유하지 않는다.

- **게임 자체 기획**·코어 재미·시스템·밸런스: `analyzing-and-refining-game-concepts`
- 공개할 대표 빌드와 품질 기준: `designing-vertical-slices`
- **썸네일 이미지 생성**과 시각 후보 제작: `designing-art-prompts-and-technique-cards`
- **플랫폼 심사**·등급·출처·라이선스·**에셋 권리 원장**: 기존 플랫폼 심사·에셋 권리 Workflow
- 실제 빌드·링크·권리·게시 상태의 최종 검증: `reviewing-and-validating-project-changes`
- **영상 편집 도구**의 실제 조작·인코딩·업로드 자동화
- 프로젝트별 브랜딩·스포일러·CTA URL·업로드 일정·**프로젝트별 KPI 절대값**

Base는 공용 방법론과 Template만 소유한다. 실제 Episode Packet과 게시·Analytics 기록은 각 프로젝트 책임 원본에 둔다.

## Skill Modes

- `channel-portfolio`: 스튜디오 통합 채널, 프로젝트별 재생목록·홈 섹션, 장문·Shorts·트레일러 역할과 채널 분리 Gate를 설계한다.
- `episode-concept`: 주 시청자, Episode Job, 한 문장 약속, 핵심 갈등·변화·결과, 주 CTA를 하나씩 우선한다.
- `script-and-shot-plan`: 실제 빌드 증거에 연결된 Hook, 대본, 샷리스트, 비교 장면과 편집 비트시트를 작성한다.
- `title-thumbnail-package`: 실제 영상과 일치하는 제목·썸네일 후보, 첫 30초 약속 충족 장면, 오해·스포일러 위험을 검토한다.
- `production-and-publish`: 캡처·편집·설명란·챕터·고정 댓글·재생목록·엔드스크린과 공개 전 Gate를 관리한다.
- `analytics-review`: 시청·이동·하위 전환·제작시간을 목적과 표본 한계에 맞춰 해석하고 다음 실험을 정한다.

필요한 Mode만 사용하되 게시 준비가 목적이면 앞 단계의 증거를 생략하지 않는다.

## 사용 조건

- 실제 게임 빌드에서 개발일지·Shorts·기능 공개·출시 홍보 영상을 만들려 한다.
- 여러 게임 프로젝트를 하나의 스튜디오 채널에서 구분해 운영하려 한다.
- 영상 한 편의 시청자·약속·갈등·CTA·대본·샷·패키지를 정해야 한다.
- 데모·알림·위시리스트·후원·구매 등 하위 전환을 설계한다.
- 게시 뒤 Analytics를 다음 영상과 개발·마케팅 판단에 제한적으로 반영한다.

## 비사용 조건

- 게임의 핵심 재미·시스템·밸런스만 설계한다.
- 썸네일 이미지 한 장의 생성·편집만 요청한다.
- 플랫폼 심사나 에셋 권리 원장 자체가 주 작업이다.
- 완성 영상의 단순 인코딩·파일 변환·업로드만 수행한다.
- 프로젝트 정본·실제 빌드·공개 가능 범위를 확인할 수 없다.
- 특정 유튜버의 말투·대본·썸네일·편집 표현을 식별 가능하게 복제하려 한다.

## Required inputs

```yaml
project_canon_and_current_decisions:
actual_build_version:
capture_date:
implementation_status:
public_release_boundary:
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
analytics_access:
external_conversion_tracking:
```

입력이 없거나 검증되지 않으면 빈칸을 추정으로 채우지 않는다.

```yaml
missing_project_canon_or_build: BLOCKED_UNVERIFIED
missing_public_boundary: PUBLICATION_BOUNDARY_UNVERIFIED
missing_rights_or_rating: RIGHTS_OR_RATING_UNVERIFIED
missing_conversion_tracking: CONVERSION_UNVERIFIED
missing_human_viewing_data: HUMAN_NOT_RUN
```

## Read first

1. 프로젝트의 현재 정본·승인 Decision·실제 구현 상태
2. 캡처 대상 빌드 버전과 캡처 날짜
3. 공개 가능 범위·스포일러·비밀·개인정보 경계
4. 음악·폰트·이미지·영상·게임 에셋의 권리·등급 기록
5. `templates/game-development-youtube/EPISODE_PACKET.md`
6. 필요 시 `docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md`
7. 승인 제안과 설계:
   - `[수정제안서]/BCP-2026-006-game-youtube-devlog-marketing-workflow/PROPOSAL.md`
   - `[수정제안서]/BCP-2026-006-game-youtube-devlog-marketing-workflow/DESIGN.md`

## Process

### 1. 정본과 실제 빌드를 먼저 고정한다

`PROJECT_CANON_AND_ACTUAL_BUILD_FIRST`와 `ACTUAL_BUILD_EVIDENCE`를 만족하도록 다음을 기록한다.

```yaml
build_version:
capture_date:
feature_status: PLANNED | EXPERIMENTAL | PARTIAL | IMPLEMENTED | RELEASED
source_decision_or_canon:
visible_evidence:
known_limitations:
public_claim_allowed:
```

기획·실험·부분 구현·완료를 같은 말로 표현하지 않는다. 편집된 장면을 정상 플레이의 보편 결과처럼 위장하지 않는다.

### 2. 채널 포트폴리오를 최소 운영비로 구성한다

기본 구조:

```text
스튜디오 통합 채널
→ 프로젝트별 재생목록·홈 섹션
→ 장문 개발일지 / Shorts / 트레일러 역할 분리
→ 독립 팬덤·지속 업로드·운영 필요가 입증된 IP만 별도 채널 검토
```

별도 채널은 다음이 모두 또는 대부분 확인될 때만 검토한다.

- 해당 IP만으로 지속적인 업로드가 가능하다.
- 독립 팬덤과 커뮤니티 운영 요구가 확인됐다.
- 다른 프로젝트 영상이 기존 시청자 만족을 반복적으로 저하시킨다.
- 분리 후 운영·분석·브랜딩 비용을 감당할 수 있다.

신규 프로젝트라는 이유만으로 채널을 분리하지 않는다.

### 3. 한 편의 Viewer Job과 Promise를 고정한다

`ONE_VIEWER_JOB`, `ONE_EPISODE_PROMISE`, `ONE_PRIMARY_CTA`를 적용한다.

Episode Job:

- `DISCOVERY`: 신규 시청자에게 게임과 갈등을 처음 노출한다.
- `TRUST`: 판단·실패·개선 과정을 통해 신뢰를 만든다.
- `SEARCH`: 구체적 제작·기술 질문의 검색 수요를 해결한다.
- `CONVERSION`: 데모·알림·위시리스트·후원·구매 행동을 돕는다.
- `RETENTION`: 기존 팬에게 진행도·업데이트·다음 기대를 제공한다.

한 영상에 모든 Job과 모든 CTA를 동급으로 넣지 않는다. 주 역할과 주 CTA를 고르고 나머지는 보조로 낮춘다.

보류 조건:

- 보여줄 실제 변화·갈등·판단 가치가 없다.
- 내부 작업 목록만 존재한다.
- 공개 위험이 기대 가치보다 크다.
- 제작시간이 게임 개발 가치보다 크다.
- 기존 영상과 같은 질문·약속을 반복한다.

### 4. 결과·갈등 중심 대본과 샷을 만든다

장문 기본 구조:

```text
0~10초: 결과·갈등·실패·비포/애프터
→ 왜 중요한 문제인가
→ 기존 방식의 한계
→ 시도·실패·선택
→ 실제 빌드 결과
→ 남은 위험과 다음 단계
→ 주 CTA 또는 구체적 질문
```

조건부 변형:

- 검색형: 질문·결과 → 조건 → 해결 과정 → 한계 → 적용
- Shorts: 한 변화 → 즉시 결과 → 최소 맥락 → 반복 가능한 끝
- 출시 공지: 핵심 판타지 → 실제 플레이 증거 → 출시 정보 → CTA

샷마다 빌드 버전·캡처 날짜·주장 상태·보호 범위를 연결한다. 필요한 장면이 없으면 대본의 확정 표현을 낮추거나 촬영 전 단계로 되돌린다.

### 5. 제목·썸네일 약속을 초반 내용과 일치시킨다

`TITLE_THUMBNAIL_PROMISE_MATCH` 검사:

```yaml
title_candidate:
thumbnail_concept:
viewer_question_created:
actual_video_evidence:
first_30_seconds_fulfillment:
misleading_risk:
spoiler_risk:
small_screen_readability:
project_identity:
status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED
```

규칙:

- 실제 영상·빌드에 없는 결과를 약속하지 않는다.
- 게임명·Devlog 번호보다 시청자가 이해할 변화·문제·결과를 앞세운다.
- 썸네일은 작은 화면에서 단일 초점과 읽을 수 있는 정보 위계를 유지한다.
- 특정 창작자의 식별 가능한 문구·구도·캐릭터 배치·편집 표현을 복제하지 않는다.
- 플랫폼 기능이 실제 지원될 때만 충분히 다른 후보를 실험한다.

### 6. 공개 전 권리·등급·스포일러·보안을 검증한다

`RIGHTS_RATING_SPOILER_SECURITY_REVIEW`는 다음을 확인한다.

- 음악·효과음·폰트·이미지·영상·게임 에셋 사용 조건
- 등급·플랫폼 공개 제한에 영향을 주는 장면
- 미공개 스토리·기능·파트너 정보·계약 정보
- API 키·토큰·계정·개인 이메일·결제·정산 정보
- 비공개 저장소·대화·문서·서버 주소
- 실제 CTA URL과 접근 가능 상태

게시 Gate:

```text
ACTUAL_BUILD_VERIFIED
and TITLE_THUMBNAIL_PROMISE_MATCH
and RIGHTS_AND_RATING_VERIFIED
and NO_SECRET_OR_PRIVATE_DATA
and SPOILER_BOUNDARY_APPROVED
and PRIMARY_CTA_LIVE
```

하나라도 충족하지 않으면 `production-and-publish` 산출물을 준비본으로 유지하고 게시 완료를 주장하지 않는다.

### 7. 게시 기록과 제작비를 남긴다

```yaml
publish_url:
published_at:
video_version:
build_evidence:
playlist:
end_screen:
primary_cta_url:
production_hours:
game_development_delay:
verification_status: PASSED | PARTIAL | FAILED | NOT_RUN | BLOCKED
```

영상 제작이 핵심 개발을 반복 지연하면 길이·빈도·편집 복잡도를 낮추거나 `STOP`·보류한다.

### 8. Analytics를 목적과 표본 한계에 맞춰 해석한다

`ANALYTICS_WITH_SAMPLE_LIMITS` 관찰값:

- 노출 경로와 대상 시청자
- 첫 30초 유지와 약속 일치
- 이탈·재시청·공유 구간
- 신규·일반·정기 시청자
- 프로젝트 재생목록·다음 영상 이동
- 설명란·고정 댓글·엔드스크린 클릭
- 데모·알림·후원·위시리스트·구매 등 하위 전환
- 제작시간과 게임 개발 지연 비용

사전 기록:

```yaml
episode_job:
primary_metric:
supporting_metrics:
external_conversion_event:
minimum_observation_window:
minimum_interpretable_sample:
change_condition:
stop_condition:
known_confounders:
```

판정:

- `KEEP`: 목적과 비용 기준에서 유지할 충분한 증거가 있다.
- `CHANGE`: 약속·도입·샷·패키지·CTA 중 수정할 축이 특정됐다.
- `STOP`: 반복 비용 또는 위험이 기대 가치보다 크다.
- `INSUFFICIENT_SAMPLE`: 표본·기간·유입 맥락이 부족하다.
- `CONVERSION_UNVERIFIED`: 외부 행동을 측정하지 못했다.
- `HUMAN_NOT_RUN`: 실제 사람 시청 데이터가 없다.

조회수·CTR·Shorts 노출 하나만으로 게임 수요·구매 의사·채널 전략의 성공을 확정하지 않는다.

## Output contract

```yaml
mode:
project_and_build_evidence:
channel_portfolio:
target_viewer:
episode_job:
one_sentence_promise:
conflict_change_or_visible_result:
primary_cta:
hook_and_script:
shot_list_and_capture_evidence:
edit_beat_sheet:
title_thumbnail_packages:
publication_review:
publish_record:
analytics_precommit:
analytics_result:
decision: KEEP | CHANGE | STOP | INSUFFICIENT_SAMPLE
next_experiment:
unresolved_states:
verification_status: PASSED | PARTIAL | FAILED | NOT_RUN | BLOCKED
```

상세 산출물은 `templates/game-development-youtube/EPISODE_PACKET.md`를 사용한다.

## Adversarial review

공개 또는 성공 판정 전에 다음 공격을 수행한다.

- 실제 빌드에 없는 기능을 완료처럼 말하고 있지 않은가.
- 제목·썸네일 약속을 첫 장면과 본문이 충족하는가.
- 성공 채널 표본을 인과·보편 법칙으로 오해하지 않았는가.
- 특정 창작자의 식별 가능한 표현을 복제하지 않았는가.
- 권리·등급·스포일러·개인정보·비밀 누출이 없는가.
- Shorts 조회수·CTR을 게임 수요로 대체하지 않았는가.
- 프로젝트별 KPI 절대값을 Base 공용 규칙으로 고정하지 않았는가.
- 통합 채널을 검증 없이 분리하지 않았는가.
- 제작시간이 게임 개발을 잠식하지 않는가.
- Repository Test를 실제 시청자·전환 검증으로 오인하지 않았는가.

## Failure conditions

- `BLOCKED_UNVERIFIED` 상태에서 게시 가능하다고 보고한다.
- 미구현·기획·실험·부분 구현·완료를 구분하지 않는다.
- 제목·썸네일이 실제 영상과 다른 결과를 약속한다.
- 권리·등급·스포일러·보안 검토 없이 게시한다.
- 특정 유튜버의 문구·썸네일·편집 표현을 식별 가능하게 모사한다.
- 조회수·CTR 하나로 게임 마케팅 성공을 확정한다.
- 작은 표본을 `INSUFFICIENT_SAMPLE` 없이 일반화한다.
- 외부 전환 추적이 없는데 구매·위시리스트 성과를 주장한다.
- 제작시간 예산과 개발 지연 비용을 숨긴다.
- 프로젝트 Adapter가 없는데 `BASE_SHARED_SKILL_ROUTES.json`에 공용 route를 만든다.
- 정적 테스트 통과를 `HUMAN_NOT_RUN` 해소로 보고한다.

## Validation scenarios

1. 실제 빌드와 공개 범위가 있는 개발일지에서 대본·샷·패키지·게시 Gate가 한 Packet으로 연결된다.
2. 검색형·Shorts·출시 공지가 같은 서사 형식을 강제받지 않고 조건부 변형된다.
3. 미구현 기능 과장 요청은 `BLOCKED_UNVERIFIED` 또는 수정된 주장으로 되돌아간다.
4. 권리·등급·스포일러·보안 미확인은 게시 차단 상태를 유지한다.
5. 썸네일 이미지만 요청하면 아트 Skill이 주 책임이며 이 Skill은 주 라우트가 아니다.
6. 전투 밸런스·게임 코어만 요청하면 게임 기획 Skill이 주 책임이다.
7. 작은 표본·CTR 단독 결과는 `INSUFFICIENT_SAMPLE` 또는 `CONVERSION_UNVERIFIED`다.
8. 제작시간이 게임 개발 가치를 넘으면 축소·보류·`STOP`을 제안한다.

## Evidence boundary

Repository의 계약·라우팅·회귀 테스트는 Skill 구현 증거다. 다음을 증명하지 않는다.

```yaml
model_behavior_evaluation: NOT_RUN unless actually executed
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
production_marketing_effectiveness: NOT_PROVEN
```

## Learning Log

반복 성공·실패·새 YouTube 기능·권리·등급·표본 해석 문제는 `skills/SKILL_LEARNING_LOG.md`에 기록한다. 공용 규칙 승격은 여러 프로젝트·영상에서 재현되고 반례가 관리된 경우에만 수행한다.
