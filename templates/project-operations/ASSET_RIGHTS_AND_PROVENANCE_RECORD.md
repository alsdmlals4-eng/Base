# Asset Rights and Provenance Record

> 프로젝트가 직접 포함·오픈소스·AI·외주·참조 전용 자산의 출처와 필요한 사용 권리를 자산 단위로 증명할 때 복사해 사용한다. Base Template 자체는 프로젝트 증거가 아니다.

## Record

```yaml
asset_id:
category: MUSIC_SFX | FONT | CHARACTER_ILLUSTRATION | MODEL_3D_ANIMATION | PLUGIN_ASSET | OPEN_SOURCE_LIBRARY | AI_OUTPUT_MODEL_TERMS | OUTSOURCING_CONTRACT | VOICE_COMPOSER_TRANSLATOR_CONTRACT | OTHER
name:
project:
creation_route: OWNED_ORIGINAL | COMMISSIONED_ORIGINAL | LICENSED_THIRD_PARTY | OPEN_SOURCE | AI_GENERATED | REFERENCE_TO_ORIGINAL | MIXED_ROUTE
creator_or_vendor:
source_url_or_path:
source_checked_at:
acquired_or_created_at:
license_or_contract:
license_version_or_terms_date:
commercial_use: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
distribution_in_game_build: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
raw_source_redistribution: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
modification: ALLOWED | CONDITIONAL | PROHIBITED | NOT_REQUIRED | UNKNOWN
attribution:
platform_or_territory_restrictions:
term_or_expiration:
seat_account_or_project_restrictions:
open_source_notice_or_source_obligation:
ai_model_service_version:
ai_input_rights:
ai_output_terms:
contract_scope:
voice_clone_or_ai_training_rights:
reference_sources:
reference_brief:
forbidden_expression:
final_asset_record:
reference_similarity_status: PASS | REVISION_REQUIRED | BLOCKED_UNVERIFIED | NOT_APPLICABLE
proof_reference:
proof_hash:
secure_original_location:
redacted_excerpt:
reviewed_by:
reviewed_at:
status: APPROVED | CONDITIONAL | REJECTED | RELEASE_BLOCKED_UNVERIFIED | SUPERSEDED
notes:
```

## Required interpretation

- `commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`, `modification`은 서로 다른 권리다.
- 실제 사용에 필요한 권리가 `UNKNOWN`이거나 조건 충족 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.
- `raw_source_redistribution`이 필요하지 않은 경우 `NOT_REQUIRED`로 기록할 수 있다.
- `REFERENCE_TO_ORIGINAL`은 참조 입력 Record와 별도 `final_asset_record`를 연결한다.
- 참조 원본은 shipping build·store asset·trailer package에 포함하지 않는다.
- 최종 자산은 `AI-generated`, `modified`, `inspired`라는 이유만으로 안전성을 상속하지 않는다.
- `reference_similarity_status`가 `PASS`가 아니면 제품 자산으로 승인하지 않는다.
- 오픈소스는 공개 저장소에 있다는 이유만으로 판정하지 않고 license·copyright·NOTICE·source·modification 의무를 확인한다.
- AI는 모델·서비스·버전·약관 날짜·계정 유형·입력 권리·출력 조건·사람 기여·후처리를 기록한다.
- 외주·성우·작곡·번역 계약은 플랫폼·지역·기간·수정·2차적 이용·크레딧·재사용·음성 복제·AI 학습 범위를 분리한다.

## Public repository safety

공개 저장소에 unredacted 계약서, 신분증, 서명, 주소, 전화번호, 계좌·결제·세금 정보, 비공개 단가·약관을 넣지 않는다.

`secure_original_location`에는 접근 통제된 Drive, 계약 시스템 또는 vault의 식별자만 기록한다. `proof_hash`와 합법적인 redacted excerpt를 보조 증거로 남길 수 있지만 원본 존재만으로 권리 범위를 통과 처리하지 않는다.

## Reference-to-original review

```yaml
reference_only_input_excluded_from_build:
functional_or_general_principles_extracted:
identifiable_expression_removed:
project_specific_canon_applied:
independent_working_files:
comparison_set:
reviewer:
reviewed_at:
reference_similarity_status:
```

금지 예:

- 이미지 tracing·overpaint·식별 가능한 캐릭터·구도·UI skin 복제
- 음악·효과음 sample, 멜로디·리프·보컬 재사용
- mesh·texture·rig·animation clip·font glyph 추출
- 특정 작가·성우·실존 인물의 식별 가능한 스타일·음성 모사
- AI 변환을 이용한 입력 권리·유사성 검토 회피
