# Public Video Research & Creative Provider Adapter Design

## Status

```yaml
status_scope: USER_APPROVED_IMPLEMENTATION_DESIGN
work_mode: PLAN_TO_IMPLEMENT
base_main: 182f98b1c1a0f0fa578994b453d0d5f7b57a57c7
branch: feat/video-research-ingest-adapter
new_broad_skill: NONE
new_hub_or_gui: NONE
project_repo_mutation: NONE
incremental_paid_cost: 0
```

## 1. Goal

공개 YouTube 영상·강연·튜토리얼이 Base/프로젝트 연구 입력으로 들어올 때 **실제 자막/전사 provenance와 timestamp를 잃지 않고 수집**하고, 그 Evidence를 기존 `PROJECT_REUSE_OPPORTUNITY_SCAN`에 넘길 수 있게 한다. 동시에 외부 AI/이미지/수작업 제작 도구는 특정 공급자에 종속시키지 않고 기존 Visual owner가 교체 가능한 provider adapter로 소비하며, 실제 절감 효과는 생성 시간이 아니라 사람 수정·통합·QA까지 포함한 `HUMAN_EDIT_DELTA`로 측정한다.

이 변경은 사용자가 제공한 특정 영상의 미검증 내용을 Base 사실로 흡수하지 않는다. 해당 영상의 전체 transcript를 현재 세션에서 검증하지 못한 상태에서는 내용 수준의 claim을 만들지 않으며, 이번 어댑터는 향후 같은 상황에서 `BLOCKED_UNVERIFIED`를 줄이기 위한 연구 입력 계약이다.

## 2. Existing owners and non-goals

Existing owners:

- 외부 사례 역공학·재사용 후보 추출: `docs/knowledge/research/REVERSE_ENGINEERING_REUSE_PIPELINE.md`
- 공용 Tool/Workflow 모듈: `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- Visual reusable modules: `docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md`
- 공용 module index: `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- 프로젝트 스캔 결과 형식: `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`
- AI/Skill 배치 원칙: `docs/AI_SKILL_ADOPTION_GUIDE.md`
- 자산 권리·출처: `templates/project-operations/ASSET_RIGHTS_AND_PROVENANCE_RECORD.md`

Non-goals:

- AI Art Hub, Tool Hub, transcript GUI를 새로 만들지 않는다.
- 새 광역 Skill/Agent를 만들지 않는다.
- 영상/오디오 자체를 Base 저장소에 다운로드·보관하지 않는다.
- 제3자 transcript 전문을 Git history에 넣지 않는다.
- 유료 transcript API, residential proxy, 별도 API credit를 기본 fallback으로 사용하지 않는다.
- 프로젝트별 Visual Canon이나 `PROJECT_ASSET_APPROVED` 권위를 Base adapter가 대체하지 않는다.
- local ASR 엔진을 이번 변경에서 설치하거나 vendoring하지 않는다.

## 3. Alternatives considered

| Approach | 장점 | 단점/위험 | 판정 |
|---|---|---|---|
| A. `ytscribe` 직접 의존 | subtitles-first, local Whisper fallback, Markdown provenance가 이미 있음 | 신규·소규모 dependency, channel-wide 기능이 현재 범위보다 큼, upstream 변화에 추가 의존 | `REFERENCE_ONLY / POSSIBLE_BOUNDED_PILOT` |
| B. Base-native thin adapter + `yt-dlp` caption metadata | 필요한 기능만 구현, 무과금, manual/auto caption 분리 가능, local-only storage 강제 가능 | YouTube/yt-dlp extractor 변화에 영향, wrapper 유지 필요 | **`ADOPT`** |
| C. `youtube-transcript-api` 직접 의존 | API가 단순하고 manual/auto transcript 구분 | cloud/provider IP block 위험, README가 proxy workaround를 설명하며 zero-cost 장기 경로가 약함 | `TEST_ONLY` |
| D. hosted transcript SaaS | 구현량 적음 | API credit/구독·rate cost, Base `ZERO_INCREMENTAL_COST_REQUIRED`와 충돌 | `REJECT` |
| E. YouTube Data API captions | 공식 API | arbitrary public research caption text retrieval과 권한 모델이 맞지 않고 OAuth/owner context가 중심 | `REJECT_FOR_THIS_USE` |

선택: **B**. `yt-dlp`는 metadata와 caption track URL discovery만 담당하고 Base tool은 WebVTT를 normalize한다. caption track이 없으면 자동으로 영상/오디오를 내려받지 않고 `ASR_FALLBACK_REQUIRED`를 반환한다. local ASR이 이미 준비된 소비 환경에서만 별도 project/local adapter로 처리한다.

## 4. RM-TOOL-005 · PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER

### Contract

```yaml
module: PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER
inputs:
  source_url:
  preferred_languages: [ko, en, en-US]
  yt_dlp_executable: yt-dlp
source_ladder:
  - accessible_manual_caption
  - accessible_auto_caption
  - optional_existing_local_asr_adapter
  - BLOCKED_UNVERIFIED
outputs:
  schema_version:
  source_url:
  video_id:
  title:
  uploader_or_channel:
  duration_sec:
  published_or_uploaded_at:
  retrieval:
    tool:
    tool_version:
  transcript:
    status:
    source_kind:
    language:
    is_generated:
    segment_count:
    segments:
      - start_sec:
        end_sec:
        text:
storage_policy:
  full_transcript: LOCAL_RESEARCH_ONLY
  default_output_root: .tmp/public-video-research
  repository_evidence: DERIVED_NOTES_AND_TIMESTAMPS_ONLY
```

### Fail-closed behavior

- `yt-dlp`가 없으면 `MISSING_YT_DLP`.
- metadata retrieval이 실패하면 `METADATA_FETCH_FAILED`.
- caption track이 없으면 `ASR_FALLBACK_REQUIRED`; 영상/오디오 자동 다운로드 금지.
- caption URL이 없거나 VTT가 비어 있으면 `CAPTION_FETCH_FAILED` 또는 `EMPTY_TRANSCRIPT`.
- transcript가 없으면 영상 내용 claim은 `BLOCKED_UNVERIFIED`.
- manual caption과 auto caption을 같은 evidence strength로 위장하지 않는다.
- output은 기본적으로 `.tmp/`에 저장해 Git 추적에서 제외한다.

### Evidence ceiling

이 Tool의 PASS는 `caption provenance + normalized timestamped text를 재현 가능하게 준비했다`는 뜻이다. 다음을 증명하지 않는다.

- 영상 발언의 사실성.
- 저작권/재배포 허가.
- 프로젝트 적합성.
- speaker claim의 일반화 가능성.
- ASR/caption의 완전한 정확성.

## 5. RM-VIS-006 · VISUAL_CREATIVE_PROVIDER_ADAPTER

Visual 생산 owner는 특정 AI 회사·모델을 canonical workflow로 만들지 않는다. AI 서비스, 로컬 모델, 수작업, 외주 모두 동일한 bounded provider slot으로 취급한다.

```yaml
module: VISUAL_CREATIVE_PROVIDER_ADAPTER
brief_id:
project_visual_canon_ref:
provider_route: AI_SERVICE | LOCAL_MODEL | MANUAL | OUTSOURCE
provider_or_tool:
model_or_version:
terms_or_license_checked_at:
protected_constraints: []
changeable_scope: []
reference_inputs: []
requested_variants: []
outputs: []
provenance_record_ref:
rights_status:
HUMAN_EDIT_DELTA:
  baseline_total_minutes:
  candidate_generation_or_creation_minutes:
  attempt_count:
  human_edit_minutes:
  integration_minutes:
  qa_minutes:
  candidate_total_minutes:
  net_minutes_saved:
  quality_delta:
  consistency_delta:
  repeatability:
```

Rules:

1. provider는 교체 가능한 backend이며 Project Visual Canon/brief가 authority다.
2. provider-specific magic wording을 Base canonical contract로 승격하지 않는다.
3. separately metered API/credit/새 유료 구독은 기본 경로에서 제외한다.
4. 생성 결과는 human visual review와 rights/provenance review 전 `PROJECT_ASSET_APPROVED`가 아니다.
5. `HUMAN_EDIT_DELTA`가 음수이거나 품질/일관성이 낮으면 빠른 생성 속도만으로 채택하지 않는다.
6. 프로젝트 고유 표현·trade dress·reference similarity guard는 기존 Visual/Asset owner를 따른다.

## 6. HUMAN_EDIT_DELTA placement

별도 `RM-WORK-003`이나 새 Skill을 만들지 않는다. 기존 `RM-WORK-002 · SKILL_WORKFLOW_PATTERN_EVAL`에 다음 production-effort fields를 추가한다.

```yaml
HUMAN_EDIT_DELTA:
  baseline_total_minutes:
  candidate_generation_or_creation_minutes:
  attempt_count:
  human_edit_minutes:
  integration_minutes:
  qa_minutes:
  candidate_total_minutes:
  net_minutes_saved:
  quality_delta:
  consistency_delta:
  repeatability:
```

이 값은 AI visual뿐 아니라 외부 workflow/tool 채택의 실제 총비용 비교에도 사용할 수 있다.

## 7. Public video evidence handoff

`PROJECT_REUSE_OPPORTUNITY_SCAN`에 공개 영상 source가 들어오면 다음 provenance만 project/repository evidence에 남긴다.

```yaml
public_video_evidence:
  source_url:
  video_id:
  title:
  checked_at:
  transcript_source_kind:
  transcript_language:
  retrieval_tool_and_version:
  timestamp_evidence: []
  content_claim_ceiling:
```

전체 transcript 전문은 기본적으로 local cache에만 둔다. 프로젝트/PR 문서에는 현재 결정에 필요한 derived note, 짧은 인용, timestamp를 남긴다.

## 8. Implementation files

Create:

- `tools/public_video_research_ingest.py` — standard-library wrapper, yt-dlp metadata/caption discovery, VTT normalize, local JSON packet.
- `tests/test_public_video_research_ingest.py` — URL parsing, manual-over-auto selection, language priority, rolling-caption dedupe, fail-closed no-caption behavior.

Modify:

- `docs/knowledge/game-development/reuse/PRODUCTION_TOOL_WORKFLOW_MODULES.md`
- `docs/knowledge/game-development/reuse/VISUAL_ASSET_MATERIAL_MODULES.md`
- `docs/knowledge/game-development/reuse/REUSABLE_MODULE_REGISTRY.md`
- `templates/research/PROJECT_REUSE_OPPORTUNITY_SCAN.md`
- `tests/test_p04_reverse_engineering_reuse_pipeline.py`
- `.github/workflows/validate-evidence-knowledge.yml` — include new tool/test in relevant contract run.

## 9. Validation

1. TDD RED: new tool test must fail before production module exists.
2. GREEN: unit tests use local fixture metadata/VTT only; network-free and deterministic.
3. static contract regression: P04 reuse test requires new module IDs/names and `HUMAN_EDIT_DELTA`.
4. `py_compile` on new tool/test.
5. relevant evidence-knowledge CI after PR creation.
6. full branch diff adversarial review minimum 5 loops before PR creation.
7. post-PR: inspect exact-head CI. No branch mutation after opening PR unless user explicitly authorizes that PR number and action.

## 10. Rollback

- Tool is additive and local-output-only; removing `tools/public_video_research_ingest.py` and its registry/docs/test references restores the prior state.
- No project repository adopts the module in this change, so rollback does not require project migrations.
- No paid service/account/API secret is introduced.
