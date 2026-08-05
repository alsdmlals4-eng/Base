# 플랫폼 심사·에셋 권리·참조 기반 독립 제작 설계

## 1. 목표

Base를 적용한 게임 프로젝트가 PC의 Steam·STOVE와 모바일의 Google Play를 준비할 때 다음을 개발 초기부터 하나의 공용 계약으로 관리한다.

```text
목표 플랫폼·희망 이용등급
→ 콘텐츠 위험 요소 추적
→ 에셋 제작·도입 경로 분류
→ 출처·권리·약관·계약 증빙
→ 참조 분석 후 독립 제작
→ 빌드·스토어 자료·등급 설문 일치 검토
→ 출시 차단 판정
→ 제출·출시 후 변경 재검토
```

이 설계의 목적은 심사나 등급분류를 회피하는 것이 아니다. 프로젝트가 목표한 이용등급과 플랫폼 정책에 맞게 콘텐츠를 설계하고, 실제 빌드·상점 자료·설문·권리 증빙의 불일치 때문에 반려·삭제·분쟁이 발생하는 위험을 줄이는 것이다.

법률 자문이나 플랫폼 승인 보증을 제공하지 않는다. 정책·법령·약관은 변할 수 있으므로 제출 직전에 공식 출처와 실제 계정 화면에서 재검증한다.

## 2. 사용자 요구의 해석

### 2.1 기본 플랫폼

- PC: Steam, STOVE
- 모바일: Google Play

프로젝트가 다른 플랫폼을 추가하면 같은 계약을 확장하되, 위 세 플랫폼을 Base의 기본 출시 검토 대상으로 둔다.

### 2.2 모든 자료의 증빙 대상

다음 자료는 직접 제작·구매·오픈소스·AI·외주·참조 전용 여부와 관계없이 출처와 사용 경로를 기록한다.

- 배경음악과 효과음
- 폰트
- 캐릭터와 일러스트
- 3D 모델과 애니메이션
- 플러그인과 에셋
- 오픈소스 라이브러리
- AI 생성물과 사용 모델·서비스·약관
- 외주 제작 계약서
- 성우·작곡가·번역가 계약서

게임 빌드나 마케팅 자료에 포함되는 자료는 상업적 이용, 완성품 포함 배포, 수정, 지역·플랫폼, 기간, 좌석·프로젝트, 고지 의무를 확인한다. 원본·소스 파일 자체의 재배포 권리는 완성품 포함 배포 권리와 분리한다.

### 2.3 참조 기반 독립 제작

이미지·사운드·UI·애니메이션 등의 기존 파일을 그대로 포함하거나 약간 변형해 사용하는 것을 기본 방식으로 삼지 않는다. 합법적으로 접근한 자료에서 기능·구조·제작 원리와 일반적 특성을 분석하고, 고유 표현을 제거한 새 제작 브리프를 만든 뒤 프로젝트 고유 정본에 맞는 자산을 새로 제작한다.

`참조했으므로 권리가 필요 없다`, `조금 바꿨으므로 안전하다`, `AI로 다시 만들었으므로 원본과 무관하다`는 판정을 금지한다.

## 3. 현행 Base 구조 분석

### 3.1 이미 존재하는 책임

- `AGENTS.md`는 최신 정본·실제 구현·같은 Goal의 PR을 먼저 비교하고, 실행하지 않은 검증을 통과로 보고하지 않도록 요구한다.
- `TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md`는 에셋·플러그인 라이선스, Store 약속, Google Play 출시 전 공식 정책 재검증을 다룬다.
- `evaluating-godot-assets-and-plugins-before-creation`은 Godot 기본 기능·오픈소스·상용 후보와 직접 제작을 비교하고 라이선스·재배포·제거 가능성을 판정한다.
- `designing-art-prompts-and-technique-cards`는 이미지 레퍼런스의 원출처·라이선스·유사성을 확인하고 표면 복제를 금지한다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`는 특정 상업 IP·작가 스타일과의 과도한 유사성, 모델·서비스·프롬프트·생성일, Asset License Ledger 연결을 요구한다.
- `GAME_DEVELOPMENT_EVIDENCE_PACK.md`는 아트·오디오·AI·권리·출시 근거와 적대적 검토를 기록한다.
- `REFERENCE_SOURCE_CATALOG.md`는 외부 자료의 원문 전체를 복제하지 않고 프로젝트 적용 전에 최신성과 사용 한계를 재검증하도록 한다.

### 3.2 확인된 공백

현재 규칙은 여러 문서에 분산되어 있고 다음이 하나의 필수 출시 Gate로 고정되지 않았다.

1. Steam·STOVE·Google Play별 콘텐츠·등급 Matrix
2. 모든 에셋 유형을 포괄하는 권리·출처·계약 원장
3. 직접 포함과 참조 전용 입력의 명확한 구분
4. 참조 자료를 독립 제작물로 변환하는 공용 절차
5. 이미지 외 사운드·음악·폰트·3D·애니메이션의 비복제 기준
6. 민감한 계약 원본을 공개 저장소에서 분리하는 보안 규칙
7. 실제 빌드·상점 설명·트레일러·설문의 일치 검토
8. 권리·등급이 미확인된 자산을 출시 빌드에서 차단하는 판정

### 3.3 구조 결정

새 광역 Skill은 만들지 않는다. 기존 Skill의 책임을 유지하며 다음 공용 Guide와 프로젝트 Template을 추가하고 기존 소비자에 연결한다.

```text
공용 정책·방법
└─ PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md

프로젝트 증빙
├─ ASSET_RIGHTS_AND_PROVENANCE_RECORD.md
└─ GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md

기존 실행 책임
├─ managing-game-project-operating-system
├─ evaluating-godot-assets-and-plugins-before-creation
├─ designing-art-prompts-and-technique-cards
├─ designing-vertical-slices
└─ reviewing-and-validating-project-changes
```

도메인별 제작 Skill이 존재하면 해당 Skill이 실제 분석·제작·QA를 수행한다. 별도 Skill이 없는 사운드·폰트·외주 계약 등은 공용 Guide와 프로젝트의 등록된 책임 원본·작업 계약이 책임지며, 이번 변경만을 위해 넓은 오디오·법무 Skill을 추가하지 않는다.

## 4. 검토한 구현 접근

### 접근 A — 기존 출시 Guide에 경고문만 추가

장점:

- 변경량이 작다.
- 현재 문서 구조를 거의 건드리지 않는다.

단점:

- 프로젝트별 실제 기록 형식이 달라진다.
- 참조 전용과 직접 포함을 구분하기 어렵다.
- 출시 전 누락을 자동 검증하기 어렵다.

판정: 기각. 권고문만으로는 사용자가 요청한 자료별 증빙과 출시 차단 계약을 충족하지 못한다.

### 접근 B — 공용 Guide + 두 프로젝트 Template + 기존 Skill 연결

장점:

- 정책과 실제 프로젝트 기록을 분리한다.
- 직접 포함, 참조 기반 독립 제작, AI, 외주, 오픈소스를 같은 원장으로 추적할 수 있다.
- 기존 Skill 수를 늘리지 않는다.
- 테스트 가능한 필수 필드를 제공한다.

단점:

- 여러 기존 소비자와 테스트를 동기화해야 한다.
- 프로젝트 도입 시 기존 자산 인벤토리 마이그레이션이 필요하다.

판정: 채택.

### 접근 C — 전용 Compliance Skill과 자동 스캐너 신설

장점:

- 장기적으로 강한 자동화와 전용 라우팅이 가능하다.

단점:

- 파일 해시·오픈소스 manifest·상점 제출 정보만으로 실제 권리와 유사성을 자동 판정할 수 없다.
- 현재 Base의 단일 책임 Skill 원칙과 충돌할 가능성이 높다.
- 검증되지 않은 자동 법률 판정 위험이 있다.

판정: 보류. 여러 프로젝트에서 수동 누락 패턴과 자동화 가능한 입력이 반복 검증된 뒤 별도 Base Change Proposal로 검토한다.

## 5. 에셋 제작·도입 경로

모든 자산 Record는 다음 중 하나의 `creation_route`를 가진다.

```text
OWNED_ORIGINAL
COMMISSIONED_ORIGINAL
LICENSED_THIRD_PARTY
OPEN_SOURCE
AI_GENERATED
REFERENCE_TO_ORIGINAL
MIXED_ROUTE
```

### `OWNED_ORIGINAL`

팀이나 개발자가 처음부터 제작했다. 작업 파일·제작자·제작일·사용된 입력·공동 저작 여부를 기록한다.

### `COMMISSIONED_ORIGINAL`

외주·성우·작곡·번역 등 계약으로 제작했다. 결과물 사용 범위, 저작재산권 또는 이용허락, 수정, 2차적 이용, 지역·기간·플랫폼, 크레딧, 재사용, AI 학습·음성 합성 권리를 각각 분리한다. 일반 납품 계약이 모든 권리를 자동 양도한다고 가정하지 않는다.

### `LICENSED_THIRD_PARTY`

구매·무료 배포 자산을 제품에 직접 포함한다. 상업적 이용과 완성품 포함 배포를 확인하며 원본 파일 단독 재배포 가능 여부를 별도 기록한다.

### `OPEN_SOURCE`

라이선스 식별자·버전·저작권 고지·NOTICE·소스 제공·변경 고지·동적/정적 링크 조건을 기록한다. 단순히 GitHub에 공개되어 있다는 이유로 오픈소스로 판정하지 않는다.

### `AI_GENERATED`

모델·서비스·버전·약관 확인일·계정 유형·입력 자료 권리·프롬프트·후처리·사람 기여·출력 사용 조건을 기록한다. Steam 콘텐츠 설문과 목표 플랫폼의 관련 공개·안전 요구를 별도 추적한다. AI 생성은 원본 침해 위험이나 제3자 권리 검토를 면제하지 않는다.

### `REFERENCE_TO_ORIGINAL`

외부 자료는 제품에 포함하지 않고 분석 입력으로만 사용한다. 출처와 접근 근거를 기록하고, 고유 표현을 제거한 제작 브리프에서 새 자산을 제작한다. 최종 자산은 별도 Record를 가지며 참조 Record와 연결된다.

### `MIXED_ROUTE`

여러 경로가 결합된 경우 각 구성 요소의 Record를 연결한다. 예를 들어 라이선스된 베이스 메시를 수정하고 자체 텍스처와 AI 보조 이미지를 사용했다면 하나의 포괄 문구로 합치지 않는다.

## 6. Reference-to-Original Asset 절차

### 6.1 입력 자격 확인

- 원출처·제작자·게시 위치·확인일을 기록한다.
- 유출본·불법 공유·워터마크 제거본·출처 불명 파일을 참조 입력으로 채택하지 않는다.
- 라이선스가 제품 사용을 허용하지 않더라도 단순 관찰 가능한 자료를 참조할 수 있는지는 프로젝트 상황과 지역 법률에 따라 달라질 수 있으므로, 파일 복사·재배포·모델 입력·팀 공유 권한을 추정하지 않는다.
- 비공개 계약 자료와 고객 자료는 계약·기밀 조건을 먼저 확인한다.

### 6.2 추출 가능한 분석 항목

고유 표현이 아니라 기능과 일반 원리를 기술한다.

```yaml
asset_role:
player_or_user_need:
information_hierarchy:
shape_or_motion_principles:
color_value_material_roles:
lighting_and_depth_roles:
tempo_rhythm_density:
frequency_and_dynamic_role:
timing_envelope_layering:
technical_constraints:
production_method:
accessibility_function:
what_not_to_copy:
```

### 6.3 복제 금지 항목

- 원본 파일, 샘플, 텍스처, 메시, 리그, 애니메이션 클립, 코드의 직접 추출
- 트레이싱, 오버페인트, 픽셀 단위 재현
- 식별 가능한 캐릭터·실루엣·구도·로고·문자·상표·UI 스킨
- 한 곡의 식별 가능한 멜로디·보컬·음색 샘플·효과음 녹음
- 특정 성우·실존 인물의 동의 없는 음성 모사
- 한 작품이나 한 작가의 표면 특징을 그대로 재현하도록 지시
- 약간의 색·속도·피치·배치 변경만으로 새 자산이라고 판정
- 원본을 AI 입력으로 사용한 사실을 숨기거나 출력물이 자동 독립 창작이라고 주장

### 6.4 독립 제작 브리프

참조 파일 자체를 제작 단계의 필수 입력으로 유지하지 않는다. 분석 결과를 다음처럼 프로젝트 고유 요구로 다시 작성한다.

```text
프로젝트 정본·Decision·사용 화면
→ 필요한 기능·감정·정보 역할
→ 프로젝트 고유 형태·재질·음향 언어
→ 기술 규격·성능·접근성
→ 원본에서 제외할 고유 표현
→ 새 변형 축과 제작 방식
→ 실패·유사성·권리 검토 기준
```

가능하면 하나의 원본을 모방하지 않고 서로 다른 출처와 프로젝트 내부 원리를 비교해 일반적 설계 원리만 종합한다. 다중 참조는 자동 안전 판정이 아니며, 최종 결과의 식별 가능한 유사성은 별도로 검토한다.

### 6.5 도메인별 적용

#### 이미지·캐릭터·일러스트·UI

분석 대상은 정보 위계, 시선 흐름, 형태 대비, 색의 역할, 재질, 광원, 카메라 목적, 제작 공정이다. 고유 캐릭터, 의상 조합, 상징, 구도, UI 스킨과 로고는 복제하지 않는다.

#### 배경음악·효과음

분석 대상은 게임 상태 전달 역할, 템포 범위, 밀도, 다이내믹, 주파수 역할, 어택·디케이·길이, 레이어 전환, 반복 피로와 믹스 공간이다. 원본 오디오 샘플, 식별 가능한 멜로디·리프·보컬·고유 효과음을 사용하지 않는다. 새 녹음·새 합성·새 연주·새 편곡 자산을 제작하고 소스와 세션 기록을 남긴다.

#### 폰트

서체 이미지를 추적해 유사 폰트를 만드는 것을 기본 방식으로 삼지 않는다. 라이선스된 폰트의 게임·앱 임베딩 권리를 확인하거나 프로젝트가 실제로 새 서체를 설계한다. 폰트 파일과 화면에 렌더링된 글자의 이용 조건을 구분한다.

#### 3D 모델·애니메이션

분석 대상은 기능적 비율, 가동 범위, 실루엣 역할, 토폴로지 목적, 리깅 요구, 동작의 게임플레이 타이밍이다. 메시·텍스처·리그·키프레임을 추출하지 않고 자체 메시·리그·키프레임 또는 권리가 확인된 모션 캡처로 제작한다.

#### 플러그인·오픈소스·코드

공개 동작과 아키텍처 원리를 참고할 수 있으나 보호되는 코드를 복사하지 않는다. 실제 코드를 채택하면 해당 라이선스를 따른다. 클린룸 재구현이 필요한 경우 관찰·명세 작성과 구현 역할을 분리할지 판정하고, API·특허·상표·호환성 위험을 별도 검토한다.

### 6.6 유사성 검토

최종 후보와 참조 자료를 비교해 다음을 확인한다.

- 일반적 기능이나 장르 관습이 아니라 식별 가능한 고유 표현이 남았는가
- 캐릭터·실루엣·구도·로고·문자·멜로디·음성·샘플·모션이 출처를 연상시키는 핵심 식별자로 작동하는가
- 한두 개의 표면 변경만 있고 전체 인상이 사실상 같은가
- 프로젝트 내부 Art Bible·Audio Bible·Asset Specification에서 독립적으로 도출된 요소가 충분한가
- 마케팅 캡처·트레일러에서도 혼동 가능성이 있는가

검토 결과는 `PASS / REVISION_REQUIRED / REJECTED / BLOCKED_UNVERIFIED`로 기록한다. 이 검토는 법률상 비침해 판정이 아니며 위험이 높으면 법률 전문가나 권리자 확인으로 올린다.

## 7. 플랫폼 콘텐츠·등급 Matrix

### 7.1 공통 원칙

프로젝트는 먼저 `target_rating`을 정하고, 기획·시나리오·아트·사운드·UI·상점 자료에 영향을 주는 콘텐츠 요소를 추적한다. 등급을 낮추기 위해 숨기거나 설문을 왜곡하지 않는다. 목표 등급과 프로젝트 코어가 충돌하면 사용자 결정으로 올린다.

공통 추적 항목:

- 폭력과 유혈·신체 훼손
- 선정성과 노출·성적 표현
- 공포와 충격 표현
- 욕설·차별·모욕적 언어
- 술·담배·약물
- 범죄와 불법 행위
- 사행성·도박·확률형 요소
- 아동 관련 위험
- 온라인 상호작용·UGC·채팅
- 결제·광고·외부 링크
- 개인정보·추적·계정
- AI 생성·실시간 생성 콘텐츠
- 지역별 법률·금지 콘텐츠

### 7.2 Steam

- 권리를 보유하지 않았거나 적절한 이용허락이 없는 콘텐츠를 배포하지 않는다.
- 콘텐츠 설문, AI 생성 콘텐츠 설명, 성인 콘텐츠 표시와 연령 제한, 상점 페이지·마케팅 자료와 실제 빌드의 일치를 검토한다.
- 사전 생성 AI와 실시간 생성 AI를 구분한다.
- 출시 전 Steam의 최신 Rules and Guidelines와 Content Survey를 공식 문서에서 재확인한다.

공식 기준:

- https://partner.steamgames.com/steamdirect/
- https://partner.steamgames.com/doc/gettingstarted/contentsurvey

### 7.3 STOVE

- 전체이용가·12세·15세는 STOVE 자체등급 절차 사용 가능 여부를 확인한다.
- 청소년이용불가 예상이면 STOVE 자체등급으로 처리할 수 있다고 가정하지 않고 GRAC 경로를 확인한다.
- 폭력성·선정성·공포·부적절한 언어·약물·범죄·사행성 항목을 추적한다.
- 게임 설명서, 초반·중반·후반 플레이 영상, 별도 폭력·선정 장면, 일러스트, 필요한 언어 파일이 실제 빌드와 일치해야 한다.
- 제출 직전 STOVE Studio의 최신 자체등급 Guide를 재확인한다.

공식 기준:

- https://studio-docs.onstove.com/pc/StudioGuide/selfrating.html
- https://studio-docs.onstove.com/pc/StudioGuide/basicrelease.html

### 7.4 Google Play

- 모든 앱은 정확한 IARC 콘텐츠 등급 설문을 완료하고 콘텐츠·기능 변경 시 다시 제출한다.
- 앱과 Store Listing의 모든 제3자 IP에 필요한 라이선스·허가를 보유하며 요청 시 문서를 제시할 수 있어야 한다.
- 단순 수정한 저작물도 침해 판정이 날 수 있으므로 독창적인 콘텐츠 제작을 기본 안전 경로로 둔다.
- 앱이 사용자에게 생성형 AI 기능을 제공하면 Google Play의 AI 생성 콘텐츠·신고·안전 요구를 별도 적용한다. 개발 과정에서만 AI를 사용한 게임 자산과 앱 내부 생성형 AI 기능을 혼동하지 않는다.
- 출시 직전 Developer Program Policy, Content Ratings, Intellectual Property 정책을 재확인한다.

공식 기준:

- https://support.google.com/googleplay/android-developer/answer/9898843
- https://support.google.com/googleplay/android-developer/answer/9888072
- https://support.google.com/googleplay/android-developer/answer/13985936

## 8. 증빙 모델

### 8.1 자산별 Record

`ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`는 한 자산 또는 분리 가능한 구성 요소 한 묶음의 권리와 제작 경로를 기록한다.

필수 필드:

```yaml
asset_id:
asset_category:
asset_name:
creation_route:
creator_vendor_or_model:
source_url_or_contract_reference:
source_checked_at:
acquired_or_created_at:
license_contract_or_terms:
license_version_or_terms_date:
commercial_use:
distribution_in_compiled_game:
source_asset_redistribution:
modification_and_derivative_rights:
attribution_and_notice:
territory_platform_duration:
seat_project_account_restrictions:
ai_input_and_output_rights:
reference_only_source_ids:
original_production_brief:
similarity_review:
proof_reference:
proof_hash:
secure_original_location:
public_redacted_copy:
reviewed_by:
reviewed_at:
status:
release_block_reason:
```

상태:

```text
DRAFT
REFERENCE_ONLY_INPUT
RIGHTS_REVIEW_REQUIRED
APPROVED_FOR_PRODUCTION
APPROVED_FOR_SHIPPING
CONDITIONAL
REJECTED
BLOCKED_UNVERIFIED
SUPERSEDED
```

### 8.2 출시 Compliance Pack

`GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md`는 자산 Record를 집계하고 다음을 연결한다.

- 대상 플랫폼과 국가·지역
- 희망·예상·확정 이용등급
- 콘텐츠 위험 Matrix
- Steam 콘텐츠 설문과 AI 설명
- STOVE 자체등급 또는 GRAC 경로
- Google Play IARC·IP·AI·Store Listing 검토
- 실제 빌드·상점 설명·스크린샷·트레일러·언어 파일 버전
- 자산 인벤토리와 미확인 권리
- 제출 문서·담당자·확인일
- 반려·변경·재제출 기록
- 최종 출시 Gate

### 8.3 권리 구분

다음 세 항목을 합치지 않는다.

1. 상업적 이용
2. 완성된 게임·앱·마케팅 자료에 포함하여 배포
3. 원본·소스 에셋 자체를 단독 재배포

일반적인 게임 출시에는 1과 2가 필요하다. 3은 소스 에셋을 제공·판매·공유하는 경우에만 필요할 수 있으며, 원본 재배포가 금지되어도 정상적인 완성품 배포가 허용될 수 있다.

## 9. 민감한 증빙 보관

공개 저장소에 다음 원본을 커밋하지 않는다.

- 서명·주소·전화번호·신분증·주민등록번호가 포함된 계약
- 은행·결제·세금 정보
- 비공개 판매 약관이나 NDA 자료
- 외주자의 불필요한 개인정보
- 라이선스 키·계정 자격 증명

GitHub에는 다음만 남긴다.

- 증빙 종류와 Record ID
- 계약·구매·약관 날짜와 버전
- 검토 결과
- 접근 통제된 원본 저장 위치의 참조 ID
- 해시
- 필요한 경우 개인정보를 제거한 공개 사본

원본 저장소는 프로젝트가 승인한 접근 통제 Drive·계약 보관소 등을 사용한다. 링크가 존재한다는 이유만으로 접근 가능하거나 내용이 검증됐다고 주장하지 않는다.

## 10. 출시 차단 Gate

다음 중 하나라도 해당하면 `RELEASE_BLOCKED_UNVERIFIED` 또는 `RELEASE_BLOCKED`다.

- 빌드·Store Listing·마케팅에 포함되는 자산의 권리 근거가 없음
- 상업 이용과 완성품 포함 배포 조건이 불명확함
- 필요한 고지·NOTICE·소스 제공·크레딧이 누락됨
- 참조 전용 원본 파일이나 샘플이 최종 자산에 포함됨
- 식별 가능한 고유 표현 유사성 Finding이 해결되지 않음
- 외주 계약의 사용 범위·수정·플랫폼·기간이 필요한 사용처를 덮지 못함
- AI 모델·서비스·입력 자료·약관의 핵심 조건이 미확인임
- 실제 빌드와 플랫폼 설문·등급 자료·Store Listing이 다름
- 콘텐츠 변경 뒤 등급·설문 재검토가 수행되지 않음
- 민감한 계약 원본이 공개 저장소에 노출됨

`APPROVED_FOR_PRODUCTION`은 `APPROVED_FOR_SHIPPING`이 아니다. 최종 출시 승인은 실제 배포 후보 빌드와 마케팅 자료를 기준으로 다시 판정한다.

## 11. 기존 Skill 연결

### `managing-game-project-operating-system`

- 신규 프로젝트 설치 시 자산 권리 Record와 출시 Compliance Pack 경로를 제공한다.
- 기존 프로젝트 감사 시 실제 자산·manifest·계약 참조와 원장 누락을 비교한다.
- 파일 존재만으로 권리 검토 완료를 주장하지 않는다.

### `evaluating-godot-assets-and-plugins-before-creation`

- `ADOPT / ADAPT / TRIAL`은 직접 포함 경로로, `BUILD_CUSTOM`은 독립 제작 경로로 연결한다.
- `REFERENCE_TO_ORIGINAL`을 라이선스 회피 수단으로 사용하지 않는다.
- 완성품 포함 배포와 원본 재배포를 분리한다.

### `designing-art-prompts-and-technique-cards`

- 이미지·UI 레퍼런스는 구조·기법·정보 역할만 추출한다.
- 작가명·작품명·상업 IP를 표면 스타일 지시로 사용하지 않는다.
- 참조 입력, 프로젝트 고유 제작 브리프, 생성 후보, 유사성 QA를 서로 다른 상태로 기록한다.

### `designing-vertical-slices`

- Vertical Slice의 대표 아트·UI·사운드·플러그인이 출시 후보 경로를 대표하는지 검토한다.
- 임시·권리 미확인 자산은 데모 완료 증거와 출시 준비 증거를 분리한다.

### `reviewing-and-validating-project-changes`

- actual diff와 자산 인벤토리, 라이선스·계약 Record, Store 자료, 플랫폼 설문의 일치를 검사한다.
- 정적 파일 검사와 실제 권리·사람 검토를 분리한다.

### `running-adversarial-review-and-refinement`

- 직접 포함된 미확인 자산, 위장된 참조 복제, 설문 누락, 계약 노출, untouched 소비자, stale 플랫폼 정책을 공격한다.

## 12. 변경 범위

구현 시 다음 파일을 기본 변경 대상으로 한다.

```text
AGENTS.md
START_HERE.md
docs/DOCUMENTATION_MAP.md
docs/knowledge/game-development/README.md
docs/knowledge/game-development/TECHNICAL_PRODUCTION_AND_RELEASE_GUIDE.md
docs/knowledge/game-development/PLATFORM_REVIEW_ASSET_RIGHTS_AND_REFERENCE_PRODUCTION_GUIDE.md
docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md
skills/managing-game-project-operating-system/SKILL.md
skills/evaluating-godot-assets-and-plugins-before-creation/SKILL.md
skills/designing-art-prompts-and-technique-cards/SKILL.md
skills/SKILL_LEARNING_LOG.md
templates/research/GAME_DEVELOPMENT_EVIDENCE_PACK.md
templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md
templates/project-operations/GAME_RELEASE_COMPLIANCE_EVIDENCE_PACK.md
templates/project-operations/github/documentation-governance.json
docs/CHANGELOG.md
tests/test_platform_review_asset_rights_contract.py
기존 운영 회귀 테스트 중 canonical companion 검사 파일
```

정확한 파일 목록은 구현 계획에서 현재 main의 테스트·생성기·문서 권위 검사를 다시 읽고 최소화한다. `skills/SKILL_REGISTRY.json`, 생성된 Skill 목록, release lock과 frozen snapshot은 기존 Skill ID·trigger로 충분하다면 변경하지 않는다.

## 13. 테스트 설계

전용 계약 테스트는 최소 다음을 검증한다.

1. 공용 Guide가 Steam·STOVE·Google Play를 기본 플랫폼으로 명시한다.
2. STOVE 자체등급 7영역과 청소년이용불가의 별도 경로를 다룬다.
3. Google Play IARC 갱신과 IP 증빙을 다룬다.
4. Steam 권리 미보유 콘텐츠 금지와 AI 콘텐츠 설문을 다룬다.
5. 요구된 자산·계약 9개 범주가 누락되지 않는다.
6. 상업 이용, 완성품 포함 배포, 원본 재배포가 분리된다.
7. 모든 자산에 `creation_route`와 증빙 필드가 있다.
8. `REFERENCE_TO_ORIGINAL` 절차가 원본 파일 포함·트레이싱·샘플링·식별 가능한 모사를 금지한다.
9. 이미지·사운드·폰트·3D·애니메이션·코드의 도메인별 비복제 규칙이 있다.
10. AI 모델·버전·약관·입력 권리 기록을 요구한다.
11. 외주·성우·작곡·번역 계약 범위를 분리한다.
12. 민감한 계약 원본의 공개 저장소 커밋을 금지한다.
13. 미확인 권리·등급 불일치가 출시 차단으로 이어진다.
14. Guide·Template이 START_HERE·Documentation Map·knowledge hub·소유 Skill에서 발견된다.
15. 새 광역 Skill이나 Registry drift가 발생하지 않는다.

TDD 순서:

```text
focused contract test RED
→ Guide·Template 최소 구현
→ 기존 Skill·라우팅 소비자 연결
→ focused GREEN
→ canonical reference freshness·documentation·operating regressions
→ 전체 local validation 또는 가능한 동일 범위 CI
→ actual diff 적대적 검토
→ exact-head GitHub Actions
```

컨테이너·네트워크·도구 제한으로 실행하지 못한 검증은 `BLOCKED_ENVIRONMENT` 또는 `NOT_RUN`으로 기록한다.

## 14. 적대적 검토

### 필수 공격 가설

- 라이선스가 불명확한 자산을 `REFERENCE_TO_ORIGINAL`로 재분류해 사실상 포함한다.
- 원본을 AI에 넣어 거의 같은 결과를 만든 뒤 독립 제작으로 표시한다.
- 이미지에는 비복제 규칙이 있지만 사운드 샘플·멜로디·음성은 누락된다.
- 무료 폰트의 인쇄·웹 사용 허용을 게임 임베딩 허용으로 오해한다.
- 오픈소스 코드의 고지·소스 제공 의무를 누락한다.
- 구매 영수증만 있고 실제 라이선스 버전과 조건을 보존하지 않는다.
- 외주 납품 사실만 있고 게임·마케팅·현지화·수정·후속작 사용 권한이 없다.
- 성우 계약을 근거로 음성 복제·AI 학습 권리까지 보유한다고 가정한다.
- Steam·STOVE·Google Play 설문이 실제 빌드의 폭력·선정·언어·사행성·AI 기능과 다르다.
- 목표 이용등급을 지키기 위해 콘텐츠를 숨기거나 설문을 축소 기재한다.
- 마케팅 캡슐·트레일러 자산은 빌드 밖이라는 이유로 권리 검토에서 제외한다.
- 계약 원본과 개인정보가 공개 GitHub에 노출된다.
- 새 Guide가 추가됐지만 프로젝트 Template·START_HERE·Skill·Test가 소비하지 않는다.
- 플랫폼 정책 확인일이 오래됐는데 현재 사실처럼 사용한다.

### 승인 Finding 처리

- `MUST_FIX`: 출시·권리·개인정보·정본 발견성을 막는 검증된 결함
- `SHOULD_FIX`: 반복 누락 가능성이 크고 범위 안에서 안전하게 개선 가능한 결함
- `USER_DECISION_REQUIRED`: 목표 이용등급과 프로젝트 코어·상업 범위가 충돌하는 선택
- `BLOCKED_UNVERIFIED`: 권리 원문·계약·계정 화면·실제 빌드를 읽을 수 없는 항목
- `REJECTED_CRITIQUE`: 모든 참조를 금지하거나 모든 원본 재배포 권리를 요구하는 등 실제 출시 권리 구조를 왜곡하는 주장

## 15. 완료 기준

- 공용 Guide와 두 프로젝트 Template이 존재하고 한 단계로 발견된다.
- 모든 요구 자산 범주에 권리·출처·약관·계약 Record가 적용된다.
- 직접 포함과 참조 기반 독립 제작이 분리된다.
- 참조 자료는 고유 표현을 제거한 제작 브리프를 거쳐 새 자산으로 제작된다.
- 이미지뿐 아니라 사운드·폰트·3D·애니메이션·플러그인·오픈소스·AI·외주에 적용된다.
- Steam·STOVE·Google Play 콘텐츠·등급·권리 검토가 실제 빌드와 Store 자료에 연결된다.
- 미확인 권리와 설문 불일치가 출시 차단 상태로 표시된다.
- 민감한 증빙 원본은 공개 저장소 밖에 있고 해시·참조 ID만 연결된다.
- 기존 Skill 책임은 유지되고 새 광역 Skill이 없다.
- focused test와 관련 운영·문서·freshness 회귀가 통과하거나 실행 불가 범위가 정직하게 기록된다.
- exact-head PR 검토에서 P0/P1 Finding과 unresolved thread가 남지 않는다.

## 16. 제외 범위

- 특정 프로젝트의 실제 에셋 전수 권리 감사
- 개별 계약서의 법률 자문·유효성 확정
- 저작권·상표·특허 비침해 보증
- 자동 이미지·음악 유사성 판정 모델 구현
- Steam·STOVE·Google Play 계정 생성이나 실제 제출
- GRAC 등급 신청 대행
- 새 오디오·폰트·법무 전문 Skill 생성
- 기존 release lock·frozen snapshot 갱신

## 17. 롤백

문제가 발생하면 신규 Guide·두 Template·전용 테스트를 제거하고, 기존 Guide·Skill·정책·Evidence Pack·라우터·Documentation Map·Change/Learning Log를 변경 전 commit으로 되돌린다. 기존 Skill ID와 프로젝트 정본 경로는 유지하므로 프로젝트 자산 원장을 삭제하거나 실제 계약 증빙을 손상시키지 않아야 한다.
