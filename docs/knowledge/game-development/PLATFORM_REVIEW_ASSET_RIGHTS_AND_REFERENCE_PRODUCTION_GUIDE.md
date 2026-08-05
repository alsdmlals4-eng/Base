# 플랫폼 심사·에셋 권리·참조 기반 독립 제작 Guide

## 1. 목적과 적용 경계

이 Guide는 Base를 사용하는 게임 프로젝트가 Steam·STOVE·Google Play 출시를 준비하면서 이용등급, 플랫폼 설문, 에셋 출처·권리, AI·외주 계약과 참조 기반 독립 제작을 하나의 증거 흐름으로 관리하게 한다.

```text
프로젝트 코어와 핵심 경험
→ 목표 플랫폼·등급 전략
→ 콘텐츠 위험 Matrix
→ 자산 제작·도입 경로
→ 권리·출처·약관·계약 증빙
→ 참조 분석 후 독립 제작
→ 실제 build·store·trailer·questionnaire 일치
→ release decision
```

이 문서는 법률 자문, 등급기관 판정, 플랫폼 승인 보증이 아니다. 문서와 정적 테스트가 존재해도 법률 검토·실제 제출·플랫폼 승인을 통과한 것으로 보고하지 않는다.

공식 정책과 계정별 제출 화면은 바뀔 수 있다. 제출 직전에 공식 원문, locale, 계정 유형, 확인일과 실제 질문 버전을 다시 기록한다.

## 2. 등급 전략

### 2.1 기본 전략

```yaml
rating_strategy: LOWEST_VIABLE_RATING
adult_only_avoidance: AVOID_ADULTS_ONLY
```

`LOWEST_VIABLE_RATING`은 승인된 핵심 경험과 정체성을 훼손하지 않으면서 실제 콘텐츠를 정직하게 공개했을 때 가능한 가장 낮은 등급을 목표로 한다.

청소년이용불가·18+를 기본적으로 회피한다. 다만 전체이용가를 모든 프로젝트의 강제 목표로 두지 않는다. 공포·괴이·전투·범죄처럼 프로젝트 코어에 필요한 표현은 숨기지 않고 전체·12세·15세 또는 지역별 상응 등급 중 프로젝트에 맞는 목표를 선택한다.

콘텐츠를 삭제·약화해도 핵심 경험이 유지되는 경우에는 낮은 등급안을 권장할 수 있다. 핵심 경험을 훼손해야만 청소년이용불가를 피할 수 있다면 `PLANNING_CONFLICT`, `GRILL_ME_REQUIRED`, `USER_DECISION_REQUIRED`로 올리고 사용자 승인 전 확정하지 않는다.

### 2.2 콘텐츠 등급과 타깃 연령 분리

```yaml
content_rating_target:
target_audience:
children_in_target_audience:
families_policy_applicable:
```

`content_rating_target`은 콘텐츠의 적합 연령이고 `target_audience`는 실제로 설계·마케팅한 이용자 집단이다. 낮은 등급을 받았다는 이유만으로 Google Play에서 아동을 타깃으로 선언하지 않는다. 아동을 타깃에 포함하면 Families, 광고 SDK, 데이터, 개인정보, 광고 개인화와 연령 확인 의무를 별도로 적용한다.

## 3. 플랫폼별 공식 검토 Matrix

| 플랫폼 | 기본 검토 | 프로젝트 증거 | 차단 조건 |
|---|---|---|---|
| Steam | Content Survey, 일반·성인·생성형 AI 콘텐츠, 권리 보유 | questionnaire version, build/store 비교, AI 사용 기록, 권리 원장 | 설문 누락·허위, 업로드된 비접근 콘텐츠 누락, 권리 미확인 |
| STOVE | 전체·12세·15세 자체등급, 폭력성·선정성·공포·언어·약물·범죄·사행성 | 설명서, 초·중·후반 영상, 별도 위험 장면, 일러스트, 언어 파일 | 청소년이용불가 예상, 증빙과 설문 불일치, 필수 자료 누락 |
| Google Play | IARC 콘텐츠 등급, Target audience and content, Families, IP 정책 | 설문, 지역별 rating, target audience, 광고·SDK, store listing 권리 | 등급 없음·허위, 콘텐츠 변경 후 미갱신, 아동 타깃 정책 누락, 제3자 권리 없음 |

필수 비교 필드:

```yaml
build_store_questionnaire_consistency:
platform_questionnaire_versions:
platform_policy_checked_at:
content_risk_matrix:
```

빌드, 상점 설명, capsule·스크린샷, trailer, 광고, 접근 불가능하지만 업로드된 콘텐츠, UGC·온라인 기능과 설문이 일치해야 한다. 낮은 등급을 얻기 위해 콘텐츠를 숨기거나 축소 기재하지 않는다.

### 공식 출처

- Steamworks Partner Program: https://partner.steamgames.com/steamdirect/
- Steam Content Survey: https://partner.steamgames.com/doc/gettingstarted/contentsurvey?l=english
- STOVE 자체등급 Guide: https://studio-docs.onstove.com/pc/StudioGuide/selfrating.html
- Google Play Content Ratings: https://support.google.com/googleplay/android-developer/answer/9898843?hl=en
- Google Play Content Rating Requirements and Target Audience: https://support.google.com/googleplay/android-developer/answer/9859655?hl=en
- Google Play Families: https://support.google.com/googleplay/android-developer/answer/9893335?hl=en
- Google Play Intellectual Property: https://support.google.com/googleplay/android-developer/answer/9888072?hl=en

확인 기준일: 2026-08-05. 제출 직전 또는 정책·계정 화면 변경 시 재검증한다.

## 4. 자산·계약 Coverage

모든 프로젝트는 최소 다음 범주를 인벤토리한다.

1. 음악·효과음
2. 폰트
3. 캐릭터·일러스트
4. 3D 모델·애니메이션
5. 플러그인·에셋
6. 오픈소스 라이브러리
7. AI 출력·모델·서비스·약관
8. 외주 제작 계약
9. 성우·작곡가·번역가 계약

마케팅 파생물은 독립된 면책 자산이 아니다. capsule, trailer, screenshot, press kit와 광고는 원천 자산 Record와 연결한다.

## 5. 제작·도입 경로

```text
OWNED_ORIGINAL
COMMISSIONED_ORIGINAL
LICENSED_THIRD_PARTY
OPEN_SOURCE
AI_GENERATED
REFERENCE_TO_ORIGINAL
MIXED_ROUTE
```

- `OWNED_ORIGINAL`: 팀이 처음부터 제작했다. 제작자·공동저작·입력·작업 파일을 기록한다.
- `COMMISSIONED_ORIGINAL`: 외주·성우·작곡·번역 계약 결과다. 플랫폼·지역·기간·수정·2차적 이용·크레딧·AI 학습·음성 복제를 분리한다.
- `LICENSED_THIRD_PARTY`: 제품에 직접 포함한다. 라이선스와 구매·획득 증빙을 기록한다.
- `OPEN_SOURCE`: 라이선스 식별자, copyright, attribution, NOTICE, source 제공과 변경 고지를 기록한다.
- `AI_GENERATED`: 모델·서비스·버전·계정 유형·약관 날짜·입력 권리·프롬프트·후처리·사람 기여를 기록한다.
- `REFERENCE_TO_ORIGINAL`: 원본을 제품에 넣지 않고 구조·기능·일반 제작 원리만 분석해 프로젝트 고유 자산을 새로 만든다.
- `MIXED_ROUTE`: 구성 요소별 Record를 연결하며 하나의 포괄 문구로 권리를 합치지 않는다.

## 6. 권리 축

다음은 서로 다른 권리다.

```yaml
commercial_use: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
distribution_in_game_build: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
raw_source_redistribution: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
modification: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
```

원본 파일 단독 재배포가 필요하지 않은 프로젝트에 `raw_source_redistribution: ALLOWED`를 강제하지 않는다. 반대로 상업 사용 가능 문구만으로 완성된 게임 포함 배포를 추론하지 않는다.

필수 권리가 `UNKNOWN`이거나 조건 충족 증거가 없으면 상태는 `RELEASE_BLOCKED_UNVERIFIED`다.

## 7. Reference-to-Original 절차

### 7.1 참조 입력 자격

- 원출처·제작자·URL·확인일·접근 근거를 기록한다.
- 유출본, 불법 공유, 워터마크 제거본, 출처 불명 자료를 사용하지 않는다.
- 원본 파일은 reference-only 보관소에 분리하고 shipping asset root에 넣지 않는다.
- 관찰 가능하다는 사실이 복제·AI 입력·재배포 권리를 의미하지 않는다.

### 7.2 분석 카드

```yaml
reference_sources:
functional_purpose:
structure_and_information_flow:
general_production_principles:
constraints_and_failure_patterns:
forbidden_expression:
reference_brief:
```

추출 가능:

- 기능과 사용자·플레이어 가치
- 정보 위계와 상호작용 흐름
- 일반적인 형태·리듬·재질·주파수·타이밍 원리
- 성능·가독성·접근성·제작 파이프라인 원리

복제 금지:

- 식별 가능한 캐릭터 디자인·실루엣·의상·소품 조합
- 구도·로고·UI skin·아이콘 세트·서명적 형태 조합
- 멜로디·리프·가사·보컬·고유 효과음 sample
- mesh·texture·rig·animation clip·font glyph 추출
- 특정 작가·성우·실존 인물의 식별 가능한 스타일·음성 모사
- 코드의 보호되는 표현을 라이선스와 고지 없이 복사

### 7.3 독립 제작

```text
reference-only record
→ 고유 표현을 제거한 reference_brief
→ 프로젝트 정본·Art Bible·audio brief·technical constraints
→ 새 제작
→ final_asset_record
→ similarity and rights review
```

`조금 바꿨으므로`, `AI로 다시 생성했으므로`, `영감을 받았으므로` 안전하다고 판정하지 않는다. AI transformation은 입력 권리와 유사성 검토를 제거하지 않는다.

최종 자산은 참조 입력과 별도 Record를 가진다. `reference_similarity_status`가 `PASS`가 아니면 승인하지 않는다.

## 8. 분야별 참조 안전 규칙

### 이미지·캐릭터·UI

형태 언어·정보 위계·가독성 원리는 참고할 수 있지만 특정 캐릭터, 작가 스타일, 구도, UI skin과 로고를 재현하지 않는다. 결과는 다른 레퍼런스, 프로젝트 고유 정본과 실제 화면에서 비교한다.

### 음악·효과음

감정 기능, BPM 범위, 밀도, 주파수 역할, attack·decay, layer 전환 원리를 기록한다. 원본 sample, 식별 가능한 멜로디·리프·보컬을 사용하지 않는다. 라이선스가 허용해도 Content ID 등록·claim 처리·streaming 제한을 확인한다.

### 폰트

desktop 사용 허가와 게임·앱 임베딩·web embedding·서버 배포를 분리한다. subset·수정·현지화 glyph·credit 의무를 확인한다.

### 3D·애니메이션

기능적 비율, topology 목적, deformation 요구, gameplay timing을 분석한다. mesh·texture·rig·motion data를 추출하거나 재배포하지 않는다.

### 플러그인·오픈소스

공개 저장소라는 이유만으로 오픈소스로 판정하지 않는다. 라이선스, copyright, NOTICE, attribution, source 제공, 수정 고지, link·distribution 조건을 기록한다.

### 외주·성우·작곡·번역

납품 사실만으로 모든 권리를 양도받았다고 가정하지 않는다. 외주 권리 범위에는 결과물, 수정, 2차적 이용, 플랫폼, 지역, 기간, 크레딧, 재사용과 보증을 포함한다. 성우 계약은 음성 복제, synthetic voice와 AI 학습 허용·금지를 별도로 명시한다.

## 9. AI 증빙

```yaml
ai_model_service_version:
license_version_or_terms_date:
account_type:
ai_input_rights:
ai_output_terms:
prompt_or_job_reference:
human_contribution:
post_processing:
platform_disclosure:
```

AI 약관 버전과 생성일을 연결한다. 현재 약관을 과거 생성물에 자동 소급하지 않는다. Steam Content Survey를 포함한 플랫폼별 AI disclosure 상태를 프로젝트 출시 Pack에 기록한다.

## 10. 민감한 증빙 보안

공개 Base·프로젝트 저장소에 unredacted 계약서, 신분증, 주민등록번호·여권, 서명, 주소, 전화번호, 계좌·결제 정보, 세금 자료, 비공개 단가·약관을 커밋하지 않는다.

```yaml
proof_reference:
proof_hash:
secure_original_location:
redacted_excerpt:
reviewed_by:
reviewed_at:
```

`secure_original_location`은 접근 통제된 Drive, 계약 관리 시스템 또는 vault의 식별자다. 공개 저장소에는 최소 메타데이터·hash·검토 결과만 둔다. 비밀 원본의 존재만으로 권리 범위가 충족됐다고 판정하지 않는다.

## 11. 출시 Pack과 상태

```text
NOT_STARTED
IN_PROGRESS
READY_FOR_SUBMISSION
SUBMITTED
APPROVED
RETURNED
RELEASE_BLOCKED_UNVERIFIED
NOT_APPLICABLE
```

출시 전 반드시 다음을 비교한다.

- target build와 commit
- `content_rating_target`과 실제 대표 콘텐츠
- `target_audience`와 store imagery·문구
- Steam·STOVE·Google Play questionnaire version
- build·store·trailer·screenshot·ads·UGC·AI disclosure
- 모든 shipping·marketing 자산의 rights coverage
- open-source NOTICE·attribution·source obligation
- 외주·성우·작곡·번역 contract coverage
- secure evidence policy

## 12. 출시 차단

다음 중 하나라도 해결되지 않으면 `RELEASE_BLOCKED_UNVERIFIED`다.

- 필수 자산의 source·license·contract·terms version 없음
- commercial_use 또는 distribution_in_game_build가 `UNKNOWN`·`PROHIBITED`
- 조건부 권리의 조건 이행 증거 없음
- reference-only 원본이 build·marketing package에 포함됨
- `reference_brief`, `final_asset_record`, similarity review 누락
- AI 입력 권리·모델·약관·플랫폼 disclosure 미확인
- open-source NOTICE·attribution·source 의무 미이행
- 외주·음성·작곡·번역 권리 범위 미확인
- 설문과 빌드 불일치 또는 store·trailer가 다른 콘텐츠를 약속함
- 청소년이용불가·18+ 위험이 있으나 사용자 결정과 플랫폼 경로가 없음
- 아동 타깃인데 Families·광고·데이터 요구 미확인
- 민감한 계약 원본이 공개 저장소에 노출됨

## 13. 적대적 검토

반드시 다음 공격을 수행한다.

1. 상업 사용 가능하지만 게임 포함 배포 불가한 자산을 채택했는가.
2. packaged distribution과 raw redistribution을 혼동했는가.
3. 폰트 임베딩 권리 없이 desktop license만 보유했는가.
4. 음악 사용은 허용되지만 Content ID claim과 방송·streaming 제한이 남았는가.
5. 오픈소스 attribution·NOTICE·source·modification 의무가 빠졌는가.
6. AI 약관 버전 snapshot 없이 현재 약관만 연결했는가.
7. 외주 권리 범위에 플랫폼·지역·기간·수정·2차적 이용이 빠졌는가.
8. 성우 계약에 음성 복제·synthetic voice·AI training 제한이 없는가.
9. reference_brief가 여전히 식별 가능한 표현을 보존하는가.
10. 설문과 빌드 불일치, store·trailer·screenshot 불일치가 있는가.
11. 콘텐츠를 숨겨 낮은 등급을 얻으려 하는가.
12. 전체이용가 콘텐츠 등급과 아동 대상 target audience를 혼동했는가.
13. 민감한 계약 원본·개인정보를 공개 저장소에 넣었는가.
14. Template 작성만으로 법률 clearance·등급·플랫폼 승인을 주장하는가.

## 14. 검증·보고 경계

다음은 서로 다른 증거다.

```text
STATIC_EVIDENCE_CHECKED
RUNTIME_ASSET_USE_CHECKED
BUILD_STORE_CONSISTENCY_CHECKED
PLATFORM_SUBMISSION_NOT_RUN
LEGAL_REVIEW_NOT_PERFORMED
```

정적 검사는 파일 존재·필드·라우팅만 증명한다. 실제 프로젝트 자산 감사, runtime 사용, 목표 기기, 플랫폼 제출, 등급 확정과 법률 검토는 별도 수행한다.

## 15. 프로젝트 적용

- 자산별: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`
- 프로젝트 출시: `templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`
- 일반 조사 연결: `templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md`

프로젝트 Template 인스턴스가 프로젝트 증거다. Base Template 자체는 프로젝트 권리·등급의 정본이 아니다.
