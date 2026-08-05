# BCP-2026-006 — 게임 개발 YouTube 개발일지·마케팅 제작 Workflow

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/Base`
- 기준 커밋: `5e23aaad85842505e009fa7f1872e70576ef59f0`
- 제출일: `2026-08-05`
- 상태: `SUBMITTED`
- 지식 상태: `패턴`
- 사용자 승인 근거: `현재 대화에서 2026-08-05 권장안(독립 전문 Skill + BCP 분리 생명주기) 승인; 안정적인 GitHub approval_ref는 제안 PR 검토 기록으로 확정 예정`
- 구현 PR: `없음`

## 관찰과 증거

사용자는 여러 게임 프로젝트를 하나의 스튜디오 YouTube 채널에서 프로젝트별 재생목록으로 운영하고, 게임 개발 영상 자체를 마케팅·수요 검증·팬 형성에 사용하는 반복 Workflow를 요청했다.

사용자 제공 벤치마크 표본:

- Doublecap (`@DoublecapGames`)
- Vedinad (`@Vedinad`)
- PieMastah (`@Pie_Mastah`)
- FOUNTAINS (`@fountainsgame`)
- Imphenzia (`@Imphenzia`)
- 푸른갈피 (`https://www.youtube.com/@%ED%91%B8%EB%A5%B8%EA%B0%88%ED%94%BC/featured`)

사용자 제공 2026-08-05 화면 캡처에서 반복 관찰된 형식은 다음과 같다.

- 개발량 나열보다 한 영상에 하나의 문제·갈등·결과를 배치한다.
- 결과 장면, 실패, 강한 변화 또는 감정적 상황을 제목·썸네일·첫 장면에서 먼저 제시한다.
- 장문 개발일지와 Shorts를 역할별로 병행한다.
- 실제 게임 화면을 중심으로 짧은 자막, 비교 장면, 비포·애프터를 사용한다.
- 게임 또는 스튜디오 페이지로 이동할 수 있는 링크를 채널 전면에 둔다.

공식 YouTube 기준과도 다음 원리가 정합한다.

- 제목과 썸네일은 실제 내용을 정확히 표현하고 중요한 단어를 앞쪽에 둔다.
- 첫 30초 유지율은 제목·썸네일의 약속과 실제 도입부가 맞는지 판단하는 핵심 신호다.
- 제목·썸네일 A/B 테스트는 최대 3개 조합을 비교하며 단순 CTR이 아니라 시청시간을 기준으로 승자를 판정한다.
- 채널 홈은 최대 12개 맞춤 섹션으로 재생목록과 프로젝트 묶음을 구성할 수 있다.

공식 참고:

- https://support.google.com/youtube/answer/12340300?hl=ko
- https://support.google.com/youtube/answer/9314415?hl=ko
- https://support.google.com/youtube/answer/16391400?hl=ko
- https://support.google.com/youtube/answer/3219384?hl=ko

증거 한계:

- 첨부 화면은 사용자가 수집한 특정 시점 표본이며 채널 전체 성과 인과를 증명하지 않는다.
- 각 채널의 조회수·구독자 규모는 콘텐츠 구조 외 언어, 장르, 출시 상태, 기존 팬덤, 업로드 역사 등의 영향을 받는다.
- 아직 Base Skill로 구현하거나 실제 프로젝트 영상에 반복 적용하지 않았다.
- 사람 시청자 유지율·클릭·데모 전환·후원·위시리스트 개선은 `HUMAN_NOT_RUN`이다.

## 일반화 후보

새 공용 전문 Skill 후보:

```text
producing-game-development-youtube-videos
```

목적:

게임 프로젝트의 실제 정본·구현·공개 가능 범위를 복원한 뒤, YouTube 개발일지·Shorts·출시 홍보 영상을 `채널 구성 → 에피소드 기획 → 대본·샷 설계 → 제목·썸네일 패키징 → 제작·게시 → Analytics 학습`의 폐쇄 루프로 생산한다.

제안 Skill Modes:

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
→ RIGHTS_SPOILER_SECURITY_REVIEW
→ ONE_PRIMARY_CTA
→ PUBLISH
→ ANALYTICS_WITH_SAMPLE_LIMITS
→ LEARNING_AND_NEXT_EXPERIMENT
```

반복 산출물:

- 채널·프로젝트 포트폴리오 구조
- 영상 목적·대상 시청자·한 문장 약속·CTA
- 제목 후보와 썸네일 콘셉트
- Hook·대본·샷리스트·편집 비트시트
- 설명란·챕터·고정 댓글·재생목록·엔드스크린 계획
- Shorts 파생안
- 공개 가능 범위·스포일러·보안·저작권 점검
- 게시 후 시청 유지·유입·재방문·하위 전환 분석
- 유지·수정·중단할 패턴과 다음 실험

## 프로젝트 전용으로 남길 내용

다음은 Base에 고정하지 않고 각 프로젝트의 책임 원본과 영상 Packet에 둔다.

- 스튜디오·채널·게임 이름과 로고
- 프로젝트별 색상·썸네일 스타일·자막 톤
- 게임 장르·세계관·스포일러 경계
- 실제 빌드 버전·공개 가능한 기능·출시 상태
- itch.io·STOVE·Steam·Google Play·텀블벅 링크
- 영상 길이·제작시간 예산·업로드 일정
- CTR·유지율·전환율의 임의 절대 합격선
- 특정 크리에이터의 문구·썸네일·편집 표현

## 기존 책임과 경계

### 독립 Skill이 필요한 이유

`evolving-project-discipline-skills`의 consolidation-first 기준으로 검토한 결과, 다음 독립 경계가 반복적으로 필요하다.

- 입력: 실제 빌드·캡처·공개 범위·시청자·마케팅 단계·제작시간 예산
- 산출물: 영상 대본·샷리스트·편집표·제목·썸네일·게시 Packet·Analytics 판정
- 도구: YouTube Studio·Analytics·A/B 테스트·영상 편집 도구
- 품질 기준: 시청자 약속 일치·도입 유지·실제 빌드 증거·CTA 전환·권리·보안
- 실패 조건: 클릭베이트·미구현 기능 과장·개발 방해·프로젝트 혼선·KPI 과잉 일반화

### 기존 Skill과의 비중복

- `analyzing-and-refining-game-concepts`: 게임의 핵심 재미·플레이어 약속·벤치마크 질문을 제공하지만 영상 제작·게시를 소유하지 않는다.
- `designing-art-prompts-and-technique-cards`: 승인된 썸네일 후보 이미지 제작을 지원하지만 영상 전략·대본·Analytics를 소유하지 않는다.
- `creating-user-learning-notes`: 사용자의 학습 문서를 만들며 게임 마케팅 영상을 소유하지 않는다.
- `designing-vertical-slices`: 공개할 대표 빌드와 Quality Bar를 제공하지만 홍보 영상 제작을 소유하지 않는다.
- `reviewing-and-validating-project-changes`: 실제 게시 Packet·권리·링크·빌드 일치를 검증하지만 작성 책임을 갖지 않는다.
- `running-adversarial-review-and-refinement`: 클릭베이트·과장·권리·보안·전환 왜곡을 공격하고 검증한다.
- 플랫폼 심사·에셋 권리 Workflow: 외부 자산 출처·라이선스·표현 유사성·플랫폼 공개 위험을 제공하되 영상 제작을 소유하지 않는다.

## 적용 조건과 비사용 조건

사용 조건:

- 게임 개발일지, 기능 공개, 제작 과정, 트레일러형 개발 영상 또는 Shorts를 기획·제작·게시할 때
- 한 스튜디오에서 여러 게임 프로젝트의 YouTube 구조를 운영할 때
- 게시 뒤 Analytics를 통해 다음 영상과 게임 마케팅 결정을 개선할 때
- 데모, 텀블벅, Steam 위시리스트, 출시 페이지 등으로 연결할 CTA를 설계할 때

사용하지 않을 조건:

- 단순 게임 기능 설명 문서를 작성할 때
- 게임 자체의 코어·시스템·밸런스 설계가 주목적일 때
- 완성된 영상 파일의 단순 인코딩·업로드만 수행할 때
- 프로젝트 정본·실제 빌드·공개 가능 범위를 확인할 수 없을 때
- 특정 유튜버의 썸네일·대본·말투를 복제해 달라는 요청일 때

## 제안 설계

### 채널 포트폴리오

기본 권장 구조:

```text
스튜디오 통합 채널
→ 프로젝트별 재생목록·홈 섹션
→ 장문 개발일지 / Shorts / 트레일러 역할 분리
→ 충분한 독립 팬덤·업로드 빈도·운영 필요가 생긴 성공 IP만 별도 채널 검토
```

### Episode Job

한 영상은 다음 중 하나의 주 역할을 선택한다.

- `DISCOVERY`: 신규 시청자에게 게임과 갈등을 처음 노출
- `TRUST`: 개발 과정·판단·실패를 통해 신뢰 형성
- `SEARCH`: 구체적 문제·기술·제작 질문의 검색 유입
- `CONVERSION`: 데모·알림·위시리스트·후원·구매 행동 유도
- `RETENTION`: 기존 팬에게 진행도·업데이트·다음 기대 제공

한 영상에 주 시청자 1개, 약속 1개, 주 CTA 1개를 우선한다.

### 기본 서사 구조

```text
결과·갈등·실패 장면
→ 왜 중요한 문제인가
→ 기존 방식의 한계
→ 시도·실패·선택
→ 실제 빌드 결과
→ 남은 위험과 다음 단계
→ 구체적 CTA 또는 질문
```

모든 영상이 동일 형식을 강제받지는 않으며 검색형·Shorts·출시 공지에는 조건부 변형을 허용한다.

### 제목·썸네일 계약

- 실제 영상과 빌드에 존재하는 내용만 약속한다.
- 게임명·Devlog 번호보다 시청자에게 중요한 변화·문제·결과를 앞세운다.
- 썸네일은 작은 화면에서 단일 초점과 읽을 수 있는 정보 위계를 유지한다.
- 장문 영상은 가능하면 서로 충분히 다른 2~3개 패키지로 A/B 테스트한다.
- Shorts에는 현재 YouTube A/B 테스트 지원 범위를 잘못 적용하지 않는다.
- 승자는 CTR 단독이 아니라 시청시간·유지·하위 전환을 함께 본다.

### Analytics 판정

결과를 보기 전에 영상 목적에 맞는 관찰값과 중단 조건을 선언한다.

- 도입 30초 유지와 제목·썸네일 약속 일치
- 이탈·재시청·공유 구간
- 신규·일반·정기 시청자 구성
- 프로젝트별 재생목록 이동
- 설명란·고정댓글·엔드스크린 클릭
- 데모 다운로드·알림·후원·위시리스트 등 가능한 하위 전환
- 제작시간 대비 게임 개발 지연 비용

표본이 적으면 `INSUFFICIENT_SAMPLE`, 외부 전환 추적이 없으면 `CONVERSION_UNVERIFIED`, 사람 반응이 없으면 `HUMAN_NOT_RUN`으로 유지한다.

## 반례와 위험

### MUST-FIX 위험

- 실제 빌드에 없는 기능을 제목·썸네일·대본에서 구현된 것처럼 홍보한다.
- 유료 에셋 원본, 개인정보, API 키, 저장소 비밀, 계약상 비공개 자료를 화면에 노출한다.
- 출처·라이선스를 확인하지 않은 음악·이미지·영상·폰트를 사용한다.
- 프로젝트마다 채널을 조기 분리해 표본·구독·업로드를 분산한다.
- 게임 개발보다 영상 제작이 우선되어 핵심 제작 일정이 붕괴한다.
- 조회수·CTR만 최적화해 게임 관심·데모·후원·구매와 무관한 시청자만 유입한다.
- 특정 채널의 표현·썸네일·편집 문법을 식별 가능하게 복제한다.

### SHOULD-FIX 위험

- 모든 장르와 채널에 하나의 영상 길이·업로드 빈도·합격 수치를 강제한다.
- Shorts 조회수와 장문 시청·게임 전환을 같은 성공으로 취급한다.
- 개발일지 번호와 내부 작업 용어만 사용해 신규 시청자가 내용을 이해하지 못한다.
- 다수 CTA가 한 영상에서 경쟁한다.
- 분석 표본과 노출 경로가 다른 영상을 직접 비교한다.

### 반례

- 한 IP가 라이브서비스·후속작·커뮤니티 운영을 지속하고 독립 업로드를 안정적으로 공급하면 별도 채널이 더 강할 수 있다.
- 개발 과정 자체가 영업비밀·스포일러·권리 위험을 크게 만들면 결과 중심의 제한 공개가 더 적합하다.
- 검색형 기술 영상이 게임 구매 전환은 낮아도 스튜디오 신뢰·채용·에셋 판매 등 다른 명시적 목표를 달성할 수 있다.
- 소수의 고품질 출시 영상이 잦은 개발일지보다 제작 비용 대비 효율적일 수 있다.

## 영향 범위와 구현 후보

승인 후 별도 구현 PR에서만 다음 후보를 상세 설계·TDD 검증한다.

```text
skills/producing-game-development-youtube-videos/SKILL.md
docs/knowledge/game-development/GAME_DEVELOPMENT_YOUTUBE_PRODUCTION_GUIDE.md
templates/marketing/GAME_DEVELOPMENT_YOUTUBE_EPISODE_PACKET.md
START_HERE.md
docs/knowledge/game-development/README.md
skills/SKILL_REGISTRY.json
skills/SKILL_BEHAVIOR_EVALS.json
skills/SKILL_BEHAVIOR_COVERAGE_EVALS.json
skills/SKILL_IMPLEMENTATION_EVIDENCE.json
skills/SKILL_LEARNING_LOG.md
skills/SKILL_COVERAGE.json
tests/test_game_development_youtube_workflow_contract.py
필요한 generated view와 canonical-reference freshness 소비자
```

Registry와 frozen release snapshot은 자동 변경하지 않는다. 현재 release lock이 요구하는 절차와 generated artifact 규칙을 구현 설계 단계에서 다시 확인한다.

## 검증 계획

### 계약 TDD

초기 RED에서 다음을 실패시킨 뒤 최소 구현으로 GREEN을 만든다.

- 신규 Skill·Guide·Template의 부재
- Registry trigger·use/do-not-use·review trigger 누락
- `PROJECT_CANON_AND_ACTUAL_BUILD_FIRST` 누락
- 실제 빌드 증거와 미구현 과장 방지 계약 누락
- 한 영상의 viewer job·promise·CTA 경계 누락
- 제목·썸네일·도입 약속 일치와 A/B 제한 누락
- 권리·스포일러·보안 검토 누락
- Analytics 표본·전환·사람 증거 상태 분리 누락
- 기존 Skill과의 중복 소유
- START_HERE·knowledge hub·coverage·evidence 소비자 전파 누락

### 행동평가

Primary 사례:

- 여러 게임을 한 채널에서 운영하며 다음 개발일지 영상의 대본·샷·제목·썸네일·CTA·게시 후 분석을 요청한다.

Non-selection 사례:

- 게임의 핵심 전투 시스템 자체를 설계해 달라는 요청
- 완성된 썸네일 이미지 한 장의 생성 프롬프트만 요청
- 이미 게시된 영상의 단순 자막 오탈자 수정
- 프로젝트 정본이나 실제 빌드 없이 유명 채널 스타일을 복제해 달라는 요청

실제 모델 결과가 실행되지 않으면 `MODEL_RUN_STATUS: NOT_RUN`을 유지한다.

### 적대적 검토

```text
attack
→ validate-critique
→ refine-approved-findings
→ regression-recheck
→ decision-report
```

필수 공격 관점:

- 신규 Skill 과분할·기존 책임 침범
- 프로젝트 전용 마케팅 수치의 Base 강제
- 클릭베이트·과장·권리·보안·스포일러
- 채널 분리 조기 최적화
- 영상 제작이 게임 제작을 잠식
- KPI 표본·인과·전환 과장
- 공식 YouTube 기능 변화에 대한 stale 계약
- untouched Registry·entrypoint·coverage·evidence·test·generated consumer

### PR Gate

- 최신 `main` 재동기화
- 같은 Goal의 열린·최근 병합 PR 비교
- changed-file 전수 목록
- focused test RED→GREEN 증거
- 필요한 Base 검증 suite와 exact-HEAD CI
- unresolved review thread 0
- P0/P1 또는 MUST_FIX 0
- Registry·generated·release lock 상태의 사실 보고
- 사람 영상 성과·실제 프로젝트 적용은 별도 미검증 상태 유지

## 필요한 도구·파일·권한

- 필요 항목: Base GitHub 쓰기 권한
- 필요한 이유: Proposal·설계·구현 Branch·PR·검증 연결
- 설치·적용 방법: 연결된 GitHub App의 최소 Contents·Pull requests·Issues 권한 사용
- 설치 후 확인 명령: GitHub connector의 repo permission·Branch·PR·Commit 조회
- 최소 권한: Base 저장소 Branch 파일 작성과 Draft PR 생성; main 직접 Push·force push·자동 병합 권한은 사용하지 않음

영상 제작 시 프로젝트별 필요 항목:

- 실제 게임 빌드와 캡처 환경
- 편집 가능한 원본 영상·음향·이미지
- YouTube Studio 접근
- 사용 자산의 출처·라이선스·공개 권리
- 공개 가능한 프로젝트 정보와 스포일러 경계
- Analytics와 외부 CTA 전환 확인 수단

누락 시 실제 영상 제작·게시·성과 검증을 완료로 보고하지 않는다.

## 승인과 구현

- 현재 BCP는 활성 Skill을 변경하지 않는 제안 단계다.
- 사용자는 독립 Skill 경계와 BCP 분리 생명주기를 대화에서 승인했다.
- 안정적인 GitHub 승인 근거는 이 제안 PR의 사용자 검토 또는 연결 Issue 댓글로 확정한다.
- 구현은 `APPROVED_FOR_IMPLEMENTATION`과 비어 있지 않은 `approval_ref`가 Registry에 기록된 뒤 별도 PR에서만 시작한다.
- 구현 전 written design을 사용자에게 다시 검토받고 `writing-plans`로 TDD 계획을 작성한다.

## 롤백

제안 단계 롤백은 이 Proposal 폴더와 Registry 항목만 되돌린다. 활성 Skill·Template·Registry·release lock·프로젝트 저장소에는 변경이 없으므로 마이그레이션은 필요 없다.
