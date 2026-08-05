# BCP-2026-006 — 게임 개발 YouTube 개발일지·마케팅 제작 Workflow

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `ecbd93f16b65a1527269bfd8fef9facad6b2f40b`
- 제출일: `2026-08-05`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴`
- 사용자 방향 승인: `2026-08-05 — 독립 전문 Skill + BCP 분리 생명주기`
- 최종 제안 승인 근거: `https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204`
- 구현 계획: `docs/superpowers/plans/2026-08-05-game-development-youtube-skill.md`
- 구현 PR: `없음`

제안 등록 PR #167이 exact-head CI 통과 후 병합됐으며, 사용자 승인 근거가 안정적인 GitHub 댓글로 기록됐다. 이 상태 전이는 활성 구현을 허용하지만 구현 완료를 의미하지 않는다. 활성 Skill 구현은 별도 Branch와 별도 PR에서 TDD로 진행한다.

## 관찰과 증거

사용자는 여러 게임 프로젝트를 하나의 스튜디오 YouTube 채널에서 프로젝트별 재생목록으로 운영하고, 개발 영상을 인지도·팬 형성·데모·후원·위시리스트·구매 전환에 사용하는 반복 Workflow를 요청했다.

사용자 제공 벤치마크 표본:

- Doublecap
- Vedinad
- PieMastah
- FOUNTAINS
- Imphenzia
- 푸른갈피

표본에서 반복 관찰한 구조:

- 작업량 나열보다 한 영상에 하나의 문제·갈등·변화·결과를 둔다.
- 실제 게임 결과, 실패, 비포·애프터를 제목·썸네일·초반에 제시한다.
- 장문 개발일지와 Shorts를 서로 다른 발견·관계 형성 수단으로 병행한다.
- 실제 게임 화면, 짧은 자막, 비교 장면과 명확한 시각 초점을 사용한다.
- 채널·영상에서 게임 또는 스토어 페이지로 이동할 경로를 제공한다.

공식 YouTube 자료와 정합하는 원칙:

- 제목·썸네일은 실제 내용을 정확히 표현하고 중요한 정보를 앞쪽에 둔다.
- 첫 30초 유지율은 제목·썸네일 약속과 도입부의 일치를 판단하는 주요 신호다.
- 패키지 실험은 충분히 다른 후보를 비교하고 시청시간·유지·하위 전환과 함께 해석한다.
- 채널 홈의 맞춤 섹션과 재생목록으로 여러 프로젝트를 구분할 수 있다.

증거 한계:

- 표본은 특정 시점의 관찰이며 채널 성장의 인과를 증명하지 않는다.
- 조회수·구독자 규모에는 언어, 장르, 출시 상태, 기존 팬덤, 업로드 역사와 외부 노출이 함께 작용한다.
- 특정 채널의 식별 가능한 문구·썸네일·편집 표현을 복제하지 않는다.
- Base Skill 구현, 실제 영상 Pilot, 사람 시청자 유지·클릭·전환 검증은 아직 실행하지 않았다.

## 일반화 후보

새 공용 전문 Skill 후보:

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

핵심 계약:

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

반복 산출물:

- 채널·프로젝트 재생목록 구조
- 영상 목적·대상 시청자·한 문장 약속·주 CTA
- Hook·대본·샷리스트·편집 비트시트
- 제목 후보·썸네일 콘셉트와 약속 일치 검토
- 설명란·챕터·고정 댓글·재생목록·엔드스크린 계획
- Shorts 파생 후보
- 실제 빌드·권리·등급·스포일러·개인정보·보안 점검
- 게시 후 유지율·유입·재방문·하위 전환·제작시간 분석
- `KEEP / CHANGE / STOP / INSUFFICIENT_SAMPLE` 판정

프로젝트 전용으로 남길 요소:

- 스튜디오·채널·게임 이름, 로고, 색상과 썸네일 스타일
- 세계관·장르·스포일러·비공개 정보 경계
- 실제 빌드 버전과 공개 가능한 기능
- 스토어·후원 링크와 CTA
- 영상 길이·제작시간 예산·업로드 일정
- CTR·유지율·전환율의 절대 합격선
- 특정 크리에이터의 표현

독립 Skill 경계:

- 입력: 실제 빌드·캡처·공개 범위·시청자·마케팅 단계·제작시간 예산
- 산출물: 대본·샷리스트·편집표·제목·썸네일·게시 Packet·Analytics 판정
- 도구: YouTube Studio·Analytics·영상 편집·외부 전환 측정
- 품질 기준: 약속 일치·실제 빌드 증거·CTA·권리·보안·제작 지속 가능성
- 실패 조건: 클릭베이트·미구현 과장·개발 일정 잠식·프로젝트 혼선·KPI 과잉 일반화

기존 책임과의 분리:

- `analyzing-and-refining-game-concepts`: 게임의 핵심 재미·플레이어 약속
- `designing-vertical-slices`: 공개할 대표 빌드와 Quality Bar
- `designing-art-prompts-and-technique-cards`: 승인된 썸네일 후보 이미지 제작
- 플랫폼 심사·에셋 권리 Workflow: 등급·출처·라이선스·reference-to-original 안전성
- `reviewing-and-validating-project-changes`: 실제 빌드·링크·권리·게시 상태 검증
- `running-adversarial-review-and-refinement`: 과장·보안·스포일러·KPI 왜곡 공격

새 Skill은 게임 자체 기획, 이미지 생성, 플랫폼 심사, 에셋 권리 원장 또는 영상 편집 프로그램 실행을 소유하지 않는다.

## 적용 조건과 비사용 조건

사용 조건:

- 게임 개발일지·기능 공개·제작 과정·트레일러형 영상·Shorts를 기획하거나 제작할 때
- 여러 게임을 하나의 스튜디오 채널에서 구분해 운영할 때
- 데모·후원·위시리스트·출시 페이지 전환을 설계할 때
- 게시 후 Analytics로 다음 영상과 마케팅 결정을 개선할 때

비사용 조건:

- 게임 자체의 코어·시스템·밸런스 설계가 주목적일 때
- 승인된 썸네일 이미지 한 장의 생성만 필요할 때
- 게시된 영상의 단순 오탈자·인코딩 수정일 때
- 프로젝트 정본·실제 빌드·공개 범위를 확인할 수 없을 때
- 특정 유튜버와 동일한 말투·대본·썸네일을 복제하려 할 때

## 반례와 위험

반례:

- 라이브서비스·후속작·커뮤니티를 지속 운영하는 IP는 독립 채널이 더 강할 수 있다.
- 영업비밀·스포일러·권리 위험이 큰 프로젝트는 과정 공개보다 결과 중심 제한 공개가 적합하다.
- 검색형 기술 영상은 게임 구매보다 스튜디오 신뢰·채용·에셋 판매 같은 별도 목표를 달성할 수 있다.
- 잦은 개발일지보다 소수의 고품질 출시 영상이 제작비 대비 효율적일 수 있다.

MUST_FIX 위험:

- 실제 빌드에 없는 기능을 구현된 것처럼 약속함
- 제목·썸네일과 초반 내용이 불일치함
- 음악·폰트·이미지·게임 에셋 권리가 확인되지 않음
- API 키·계정·개인정보·비공개 저장소·스포일러가 노출됨
- Shorts 조회수나 CTR을 게임 수요로 곧바로 해석함
- 영상 제작이 핵심 게임 개발을 반복적으로 지연함
- 성공 채널 표본만 보고 보편 KPI를 고정함
- 여러 프로젝트를 성급히 채널 분리해 운영 비용과 팬층을 분산함
- YouTube 기능 지원 범위를 확인하지 않고 A/B 테스트를 가정함

## 영향 범위와 검증

승인된 구현 계획의 최소 범위:

```text
skills/producing-game-development-youtube-videos/SKILL.md
templates/game-development-youtube/EPISODE_PACKET.md
skills/SKILL_REGISTRY.json
skills/SKILL_LEARNING_LOG.md
skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json
skills/SKILL_IMPLEMENTATION_EVIDENCE.json
docs/generated/BASE_SKILL_IMPLEMENTATION_EVIDENCE.md
docs/generated/BASE_ACTIVE_SKILLS.md
docs/OPERATING_MODEL.md
.github/reference-freshness.json
tests/test_game_development_youtube_skill.py
tests/test_skill_package_integrity.py
tests/test_base_v9_5_skill_operating_refinement.py
tests/test_skill_behavior_evidence_hardening.py
tests/test_skill_implementation_evidence.py
tests/test_skill_behavior_governance_integration.py
tests/test_skill_behavior_adversarial_boundaries.py
```

`BASE_SHARED_SKILL_ROUTES.json`은 프로젝트 Adapter가 존재할 때만 사용하는 선택 경로이므로 이번 Base 공용 Skill 구현에서는 수정하지 않는다. `SKILL_BEHAVIOR_EVALS.json`은 외부 모델 실행 결과용으로 유지하고, 정적 활성·비활성 경계 사례는 `SKILL_BEHAVIOR_COVERAGE_EVALS.json`에 둔다.

구현 계획:

```text
docs/superpowers/plans/2026-08-05-game-development-youtube-skill.md
```

활성 Skill 구현 전에 다음을 테스트 우선으로 고정한다.

- 기본 개발일지 Packet 생성
- 검색형·Shorts·출시 공지 변형
- 미구현 기능 과장 거절
- 실제 빌드·공개 범위 부재 시 차단
- 권리·등급·스포일러·보안 미확인 시 게시 차단
- 특정 창작자 표현 복제 거절
- CTR·조회수 단독 결론 거절
- 작은 표본의 `INSUFFICIENT_SAMPLE`
- 제작시간 예산 초과 시 축소·보류
- 기존 Skill과의 라우팅·책임 충돌 부재
- Registry·학습 로그·행동 Eval·문서 소비자 동기화
- 제안 PR과 구현 PR의 분리 및 approval_ref 추적

실제 영상·시청자·전환 검증이 없으면 다음 상태를 유지한다.

```yaml
active_skill_implementation: NOT_STARTED
model_behavior_evaluation: NOT_RUN
real_project_video_pilot: NOT_RUN
human_audience_validation: HUMAN_NOT_RUN
conversion_validation: CONVERSION_UNVERIFIED
```

롤백:

- 새 Skill과 전용 Template·Registry·Eval·Test·문서 소비자 변경을 하나의 구현 PR 단위로 되돌린다.
- 프로젝트별 실제 Episode Packet은 Base 롤백 대상이 아니며 프로젝트 책임 원본에 남긴다.
- 이미 수집한 Analytics는 관찰 기록으로 보존하되 검증된 보편 규칙으로 승격하지 않는다.

## 승인과 구현

사용자는 2026-08-05 22:44 KST에 제안과 설계를 승인했다.

안정적 승인 근거:

```text
https://github.com/alsdmlals4-eng/Base/pull/167#issuecomment-5192600204
```

현재 생명주기:

1. 제안 등록 PR #167 병합 완료.
2. 상태를 `APPROVED_FOR_IMPLEMENTATION`으로 전이하고 `approval_ref`를 Registry에 기록.
3. TDD 구현 계획을 `docs/superpowers/plans/2026-08-05-game-development-youtube-skill.md`에 기록.
4. 활성 Skill·Template·Registry·Eval·Test 변경은 별도 구현 PR에만 둔다.
5. 구현·회귀·행동 Eval·문서 동기화가 통과한 뒤 별도 상태 전이에서 `IMPLEMENTED`와 구현 PR을 연결한다.
6. 실제 시청자·전환 검증 전에는 실전 성과를 확정하지 않는다.
