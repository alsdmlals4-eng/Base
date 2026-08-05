# Game Release Compliance Evidence Pack

> Steam·STOVE·Google Play 출시 전 이용등급, target audience, 실제 build·store·questionnaire 일치와 자산 권리 Coverage를 프로젝트 단위로 검토한다. 이 Template 작성은 법률 자문·등급 확정·플랫폼 승인 보증이 아니다.

## 0. Metadata

```yaml
release_pack_id:
project:
repository:
baseline_commit:
target_build:
created_at:
updated_at:
owner:
status: DRAFT | IN_PROGRESS | READY_FOR_SUBMISSION | SUBMITTED | APPROVED | RETURNED | RELEASE_BLOCKED_UNVERIFIED | SUPERSEDED
```

## 1. Rating and audience decision

```yaml
rating_strategy: LOWEST_VIABLE_RATING | FIXED_PROJECT_TARGET | PLATFORM_ASSIGNED | UNDECIDED
adult_only_avoidance: AVOID_ADULTS_ONLY | USER_APPROVED_EXCEPTION | NOT_APPLICABLE
core_experience_protected:
content_rating_target:
target_audience:
children_in_target_audience: true | false | UNDECIDED
families_policy_applicable: true | false | UNDECIDED
rating_decision_id:
rating_rationale:
```

규칙:

- `ALL_AGES` is a candidate, not a universal Base mandate.
- Content rating and target audience are independent declarations.
- 전체이용가를 모든 프로젝트의 강제 목표로 두지 않는다.
- 청소년이용불가·18+를 기본적으로 회피하되, 핵심 경험 충돌은 `GRILL_ME_REQUIRED`로 사용자 승인받는다.
- 낮은 등급을 얻기 위해 콘텐츠를 숨기거나 설문을 축소 기재하지 않는다.

## 2. Platform ratings

```yaml
platform_ratings:
  Steam:
    target_or_assigned_rating:
    regional_ratings:
    questionnaire_version_or_checked_at:
    build_evidence:
    store_evidence:
    trailer_screenshot_evidence:
    mature_content_disclosure:
    ai_disclosure:
    ads_ugc_online_interaction:
    status: NOT_STARTED | IN_PROGRESS | READY_FOR_SUBMISSION | SUBMITTED | APPROVED | RETURNED | RELEASE_BLOCKED_UNVERIFIED | NOT_APPLICABLE
  STOVE:
    target_or_assigned_rating:
    self_rating_scope: ALL_AGES | AGE_12 | AGE_15 | ADULT_ONLY_GRAC_REQUIRED | UNDECIDED
    questionnaire_version_or_checked_at:
    game_manual_evidence:
    gameplay_video_evidence:
    risk_scene_evidence:
    illustration_evidence:
    language_file_evidence:
    build_evidence:
    store_evidence:
    status: NOT_STARTED | IN_PROGRESS | READY_FOR_SUBMISSION | SUBMITTED | APPROVED | RETURNED | RELEASE_BLOCKED_UNVERIFIED | NOT_APPLICABLE
  Google_Play:
    target_or_assigned_rating:
    regional_iarc_ratings:
    questionnaire_version_or_checked_at:
    target_audience_declaration:
    families_policy_status:
    ads_sdk_data_privacy_status:
    build_evidence:
    store_listing_evidence:
    trailer_screenshot_evidence:
    ai_generated_content_status:
    status: NOT_STARTED | IN_PROGRESS | READY_FOR_SUBMISSION | SUBMITTED | APPROVED | RETURNED | RELEASE_BLOCKED_UNVERIFIED | NOT_APPLICABLE
```

## 3. Policy snapshots

```yaml
platform_questionnaire_versions:
platform_policy_checked_at:
platform_policy_locale:
platform_account_type:
platform_source_urls:
```

공식 정책과 계정별 질문은 제출 직전에 다시 확인한다.

## 4. Content risk matrix

| Risk | Present | Severity/frequency/context | Build evidence | Store/trailer evidence | Platform answer | Mitigation without core damage | Status |
|---|---|---|---|---|---|---|---|
| violence |  |  |  |  |  |  |  |
| sexual content |  |  |  |  |  |  |  |
| horror |  |  |  |  |  |  |  |
| language |  |  |  |  |  |  |  |
| drugs/alcohol/tobacco |  |  |  |  |  |  |  |
| crime |  |  |  |  |  |  |  |
| gambling/simulated gambling |  |  |  |  |  |  |  |
| ads/IAP |  |  |  |  |  |  |  |
| UGC/online interaction |  |  |  |  |  |  |  |
| AI-generated/live-generated content |  |  |  |  |  |  |  |

## 5. Consistency review

```yaml
build_store_questionnaire_consistency:
  target_build_matches_review_build:
  store_description_matches_features:
  capsule_and_screenshots_match_build:
  trailer_matches_representative_play:
  inaccessible_uploaded_content_disclosed:
  ads_and_offers_match_content_rating:
  online_ugc_features_disclosed:
  ai_content_disclosed:
  result: PASS | REVISION_REQUIRED | RELEASE_BLOCKED_UNVERIFIED
```

## 6. Asset rights coverage

```yaml
asset_rights_coverage:
  MUSIC_SFX:
  FONT:
  CHARACTER_ILLUSTRATION:
  MODEL_3D_ANIMATION:
  PLUGIN_ASSET:
  OPEN_SOURCE_LIBRARY:
  AI_OUTPUT_MODEL_TERMS:
  OUTSOURCING_CONTRACT:
  VOICE_COMPOSER_TRANSLATOR_CONTRACT:
open_source_notice_status:
ai_disclosure_status:
contract_coverage:
reference_to_original_coverage:
```

각 항목은 프로젝트의 `ASSET_RIGHTS_AND_PROVENANCE_RECORD.md` 인스턴스와 shipping·marketing 사용처를 연결한다.

## 7. Secure evidence policy

```yaml
secure_evidence_policy:
  public_repository_contains_unredacted_contracts: false
  public_repository_contains_ids_or_signatures: false
  secure_original_location_scheme:
  proof_hash_policy:
  redaction_review:
  access_control_owner:
```

공개 저장소에는 unredacted 계약서·신분증·서명·주소·전화번호·결제·세금·개인정보를 넣지 않는다. `secure_original_location`과 최소 metadata·hash·합법적인 redacted excerpt만 남긴다.

## 8. Unresolved items

| ID | Area | Missing fact/evidence | Risk | Owner | Resolution condition | Status |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

다음은 자동으로 `RELEASE_BLOCKED_UNVERIFIED`다.

- 필요한 권리 값이 `UNKNOWN` 또는 `PROHIBITED`
- 조건부 권리의 조건 이행 증거 없음
- reference-only 원본이 build·store·trailer에 포함됨
- AI model·terms version·input rights·platform disclosure 누락
- open-source attribution·NOTICE·source 의무 누락
- 외주·성우·작곡·번역 contract scope 누락
- build·store·trailer·questionnaire 불일치
- 청소년이용불가·18+ 위험에 대한 사용자 결정·플랫폼 경로 없음
- 아동 target audience인데 Families·ads SDK·data·privacy 확인 없음
- 민감 원본이 공개 저장소에 노출됨

## 9. Release decision

```yaml
release_decision: READY_FOR_SUBMISSION | RELEASE_BLOCKED_UNVERIFIED | RETURN_TO_PRODUCTION | NOT_APPLICABLE
reviewed_by:
reviewed_at:
exact_build_commit:
static_evidence_status:
runtime_asset_use_status:
build_store_consistency_status:
platform_submission_status:
legal_review_status:
notes:
```

증거 상태는 분리한다.

```text
STATIC_EVIDENCE_CHECKED
RUNTIME_ASSET_USE_CHECKED
BUILD_STORE_CONSISTENCY_CHECKED
PLATFORM_SUBMISSION_NOT_RUN
LEGAL_REVIEW_NOT_PERFORMED
```

Template 작성이나 자동 테스트 통과만으로 `APPROVED`를 주장하지 않는다.
