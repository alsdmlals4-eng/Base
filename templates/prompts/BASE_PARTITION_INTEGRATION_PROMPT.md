# Base Partition 최종 Integration — GPT 작업지시문

P01..P09의 독립 최적화 결과를 최신 Base `main`에 안전하게 통합한다. 개별 Part 작업을 대신하지 않고 **CP0·cross-part 정합성·전체 회귀·최종 merge**만 책임진다.

## 1. 입력

- latest main exact SHA
- `docs/operations/BASE_PARTITION_MANIFEST.json`
- P01..P09 Context Pack
- Part별 PR/완료보고/loop evidence
- 모든 `CROSS_PART_CHANGE_REQUEST`
- Notion `Base · 작업 시스템 & Skill 지도`

진행 중 독립 workstream PR은 수정·흡수하지 않는다.

## 2. Scope 감사

각 Part의 `ACTUAL_CHANGED_PATHS`를 Manifest와 대조한다. Part branch에 대해 scope checker를 다시 실행한다.

```powershell
python tools/check_base_partition_scope.py --part P01 --base <BASELINE_SHA> --head <PART_HEAD>
```

범위 밖 변경은 `VALID_CROSS_PART_CHANGE / ACCIDENTAL_SCOPE_CREEP / CONTROL_PLANE_CHANGE / DUPLICATE_CHANGE`로 분류한다.

Integration 자체 diff는:

```powershell
python tools/check_base_partition_scope.py --integration --base <INTEGRATION_BASE> --head HEAD
```

로 분류한다.

## 3. CROSS_PART_CHANGE_REQUEST

요청을 모아 같은 semantic owner에 대한 중복 요청을 합친다. 서로 충돌하면 사용자 의도·정본·실제 구현·증거·비용·장기 적합성으로 재판정한다. CP0 변경은 한 곳에서 한 번만 수행한다.

## 4. Control Plane

Integration만 다음을 쓸 수 있다.

- AGENTS / START_HERE / OPERATING_MODEL / routing
- Documentation Map / Long-Horizon
- Skill Registry / shared routes / central evals
- generated map/artifacts
- `.github` global workflows/config
- Partition Manifest/Context/Prompt

원본을 수정한 뒤 generated artifact를 재생성하며 파생본을 직접 손편집하지 않는다.

## 5. Skill/Module 전체 재검토

Part별 결과를 합치면 새 중복이 생길 수 있다. 전체 active Skill에서 기능/trigger/Mode 중복, 과도한 supporting Skill, consumer 없는 Skill, Guide/Module로 내릴 수 있는 Skill, Registry drift를 공격한다.

Module은 canonical owner, 순환 의존, cross-Part coupling, 독립 검증 가능성, 재사용 경계를 다시 본다.

## 6. Legacy retirement

Part에서 보고된 Figma/Sheets/HTML/local Tool/QA tooling 항목을 `UNIQUE / DUPLICATE / OBSOLETE`와 destination/readback evidence로 재검증한다. unique material 이관과 consumer 0을 확인하기 전에는 파괴적으로 삭제하지 않는다.

## 7. Notion ↔ GitHub

Notion은 Base/프로젝트 사람이 읽는 human-facing map, GitHub는 규칙/Skill/structured/runtime truth다. Integration 후 Notion `Base · 작업 시스템 & Skill 지도`를 merged facts로 갱신하고 readback한다. 진행 중 PR 내용을 현행처럼 표시하지 않는다.

## 7A. Learning 통합

P01~P09의 `learning_log`를 모두 읽는다. 같은 교훈의 중복 승격을 합치고 `PROJECT_ONLY`/`PART_ONLY`는 원래 범위에 남긴다. `BASE_PROMOTION_CANDIDATE`도 evidence·반복 재사용성·기존 canonical owner를 재검증한 뒤에만 흡수한다.

Periodic Source Scan Queue에서 나온 항목은 `UNVERIFIED_DISCOVERY → source/evidence disposition → Part lesson → Base promotion candidate` 순서를 건너뛰지 않는다. 신규 사이트 수를 KPI로 삼지 않고 실제 결정 개선·재현성·회귀 감소를 본다.

## 8. 검증

- partition contract CI
- scope checker
- Base v9/global integrity
- changed-domain focused tests
- canonical reference freshness
- generated artifact check
- unresolved thread 0
- exact-head checks

실행하지 않은 runtime/human 검증은 PASS가 아니다.

## 9. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
```

통합된 Base 전체를 매 회차 처음부터 다시 공격한다. 최소 5회의 full-scope 개선 loop를 수행하고, 5회 이후에도 `MUST_FIX`, 정본 충돌, stale active reference, untouched consumer, routing ambiguity blocker, acceptance failure, regression이 있으면 6..N회를 계속한다.

가짜 finding을 만들지 않는다. 최소 5회 이후 전체 재공격에서 새 유효 blocker 0 + 회귀 0 + acceptance/정본/evidence 조건 충족일 때만 `CLEAN_REVIEW_EXIT`다.

## 10. Merge / post-merge

`CLEAN_REVIEW_EXIT`, Required CI, unresolved thread 0, exact head가 모두 닫히면 merge한다. 새 `main`을 다시 읽고 Notion도 readback한 뒤에만 완료로 보고한다.

## 11. 사용자 학습형 최종보고

- Base 전체가 지금 어떻게 작동하는가
- 핵심 상위 규칙
- Skill/Mode 지도
- Module 지도
- P01..P09 역할과 연결
- BEFORE→AFTER
- 제거/흡수/유지/의도적 비추가
- 장기 효과와 trade-off
- 재검토 조건
- 실제 CI/runtime/Notion 증거
- NOT_RUN/남은 위험

`CROSS_PART_CHANGE_REQUEST`라는 단어와 처리 결과도 명시한다.
