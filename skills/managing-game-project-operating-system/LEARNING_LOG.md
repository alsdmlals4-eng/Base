# Managing Game Project Operating System Learning Log

## 2026-08-21 — Merge is followed by GitHub/Notion adversarial progress closure

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** Base 복구 병합은 성공했지만 복구 기준 자체의 stale canon/test/routing이 남아 전체 회귀 19건과 Notion current SHA drift가 병합 뒤에야 드러났다.
- **Finding:** premerge 검증만으로는 새 main에서의 untouched consumer, Notion 사람용 current-state, 진행도 재계산 누락을 완전히 막지 못한다. 병합을 종료 신호로 해석하면 복구 성공과 시스템 CLEAN을 혼동한다.
- **Decision:** 기존 `verify`에 `POSTMERGE_GITHUB_NOTION_ADVERSARIAL_PROGRESS_LOOP`를 흡수한다. exact new main readback → 전체 범위 적대 검토 → 검증된 finding의 새 Branch/PR 교정 → 회귀 → 적용 가능한 Notion current block 갱신 → 양쪽 destination readback → remaining work 재계산을 반복한다.
- **TDD evidence:** `tests/test_postmerge_github_notion_long_term_contract.py` RED가 Project OS consumer의 병합 후 교정·readback 계약 부재를 재현했다. 최종 증거는 전체 discovery와 exact-head CI에서 확정한다.
- **Boundary:** 열린 다른 PR은 번호·동작의 명시적 승인 없이 수정하지 않는다. 역사 Notion 블록을 current state처럼 일괄 치환하지 않으며, Notion이 적용되지 않는 작업에 가짜 sync를 만들지 않는다.
- **Next trigger:** GitHub merge 뒤 Notion current-state가 stale하거나, postmerge finding이 진행도에서 사라지거나, 교정이 direct main/기존 open PR mutation으로 우회될 때.

## 2026-08-05 — 플랫폼 심사·자산 권리·참조 기반 독립 제작

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** Steam·STOVE·Google Play 출시를 준비하면서 등급 위험, 모든 에셋 범주의 상업·배포 권리, AI·외주 계약, 이미지·사운드 등의 참조 후 독립 제작을 Base 공용 구조에 반영하라는 승인된 요청.
- **Finding:** 기존 출시 Guide, Godot 에셋 평가, 이미지 프롬프트·검수, Vertical Slice와 Evidence Pack에 관련 규칙이 분산돼 있었지만, 직접 포함과 `REFERENCE_TO_ORIGINAL`, 게임 포함 배포와 원본 재배포, 등급과 target audience, 공개 저장소와 민감 계약 원본을 하나의 출시 차단 계약으로 연결하지 못했다.
- **Decision:** 새 광역 Skill을 추가하지 않음. 기존 `managing-game-project-operating-system`, 에셋 평가, 아트 프롬프트, Vertical Slice, 변경 검증 Skill에 공용 Guide와 두 프로젝트 증빙 Template을 연결한다. 등급은 `LOWEST_VIABLE_RATING`과 `AVOID_ADULTS_ONLY`를 사용해 청소년이용불가·18+를 기본 회피하되 전체이용가를 강제하지 않는다.
- **Reference production:** 외부 이미지·사운드·폰트·3D·애니메이션·UI·코드에서 기능·구조·일반 제작 원리만 추출하고, 식별 가능한 표현을 `forbidden_expression`으로 제거한 `reference_brief`에서 별도 최종 자산을 제작한다. 약간 수정하거나 AI로 재생성했다는 사실은 독립성 증거가 아니다.
- **Rights evidence:** `commercial_use`, `distribution_in_game_build`, `raw_source_redistribution`, 수정·고지·NOTICE·AI 약관·외주 범위를 분리하며, 필수 증거가 없으면 `RELEASE_BLOCKED_UNVERIFIED`다.
- **Security boundary:** 공개 저장소에 unredacted 계약·신분증·서명·결제·개인정보를 넣지 않고 최소 metadata·hash·검토 결과와 `secure_original_location`만 둔다.
- **Automation boundary:** 자동 법률 판정기를 추가하지 않음. 파일·hash·설문 필드로 실제 권리, 침해 유사성, 법률 clearance나 플랫폼 승인을 자동 확정할 수 없으므로 자동 검사는 누락과 상태 불일치만 차단한다.
- **Evidence:** PR #163의 focused RED에서 기존 167개 테스트 중 새 Guide·Template·라우팅 부재만 실패했다. 구현 뒤 exact-head GREEN, 전체 회귀, 참조 최신성, 독립 검토는 별도 완료 증거로 기록한다.
- **Boundary:** 실제 프로젝트 자산 감사, runtime 사용, store·build 비교, 법률 검토, 등급 제출과 플랫폼 승인은 `NOT_RUN`이며 Template·정적 테스트로 대체하지 않는다.
- **Next trigger:** 여러 프로젝트에서 동일한 누락 패턴이 반복되고 구조화 입력으로 안전하게 검사 가능한 항목이 확인될 때만 전용 자동 validator 또는 별도 Skill 책임을 재검토한다.

## 2026-08-05 — Cloud Run 게임 백엔드 Capability Pack

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** 여러 게임 프로젝트에서 로그인·클라우드 저장·리더보드·비동기 결과·AI proxy 등 서버 기능이 필요할 때 Cloud Run을 무조건 채택하지 않고 재사용 가능한 적합성·운영·검증 계약으로 판단하려는 승인된 요청.
- **Decision:** 새 활성 Skill과 `BASE_SHARED_SKILL_ROUTES.json` 항목을 추가하지 않았다. 기존 게임 개념·프로젝트 운영·Vertical Slice·AI 비용·통합 검증 owner에 Guide와 프로젝트 Contract를 연결했다.
- **Boundary:** `CLOUD_RUN_DEFAULT_CANDIDATE`는 조건부 기본 검토 후보다. high-frequency authoritative realtime, UDP, indefinite worker, instance-local durable authority는 별도 아키텍처가 필요하다.
- **Evidence:** RED에서는 신규 Guide·Contract·라우팅 부재만 실패했고 기존 회귀는 통과했다. 정적 GREEN은 파일·계약·경로·반례만 증명한다.
- **Not run:** 실제 deployment, runtime persistence, load, connection storm, dependency failure, cost, security, production readiness는 `NOT_RUN`이다.
- **Next trigger:** 실제 프로젝트 Pilot에서 기존 owner 라우팅이 반복 실패하거나 독립 도구·승인·검증 경계가 입증될 때만 별도 Skill을 재검토한다.

## 2026-08-05 — 게임 entitlement·integrity·DRM Capability Pack

- **상태:** `PATTERN_CANDIDATE`
- **Decision:** 새 활성 Skill과 shared route를 추가하지 않고 기존 운영·플랫폼 도입 평가·Vertical Slice·통합 검증 owner에 Guide와 프로젝트 Record를 연결했다.
- **Boundary:** `PLATFORM_NATIVE_FIRST`, `NO_CUSTOM_DRM_DEFAULT`, 플랫폼별 의미 보존, 단일 신호 영구 제재 금지, offline/outage·지원/이의제기·save access·sunset·privacy 결정이 필수다.
- **Evidence:** 정적 테스트는 계약·라우팅·반례만 증명한다. Steam/Google Play/STOVE sandbox, 사람 오탐 복구, 법률 검토, 플랫폼 승인과 production readiness는 실행하지 않았다.
- **Not run:** platform SDK integration `NOT_RUN`, human false-positive recovery `HUMAN_NOT_RUN`, legal/platform approval `NOT_PERFORMED`.

## 2026-08-19 — Notion/Repository workspace authority consumer normalization

- **상태:** `PATTERN_CANDIDATE`
- **Trigger:** canonical workspace contract가 이미 `NOTION_HUMAN_FACING_CANON + REPOSITORY_STRUCTURED_CANON + Google Sheets COMPATIBILITY_ONLY`로 바뀌었지만 Project OS consumer가 구형 active-Sheet 입력을 계속 요구하는지 P01 독립 감사.
- **Finding:** authority migration 자체는 이미 존재했지만 stale Skill consumer와 template 표현 때문에 신규 프로젝트가 Google Sheets를 다시 필수 작업면처럼 해석할 위험이 있었다. 반대로 legacy Sheet 계약은 reference-freshness의 별도 coupled test owner와 묶여 있어 P01 단독 변경이 ownership 경계를 넘었다.
- **Decision:** 새 Skill/Mode/policy를 만들지 않고 Project OS의 active read/install/verify 경로만 Notion/Repository authority로 정규화한다. `docs/PROJECT_GDD_GOOGLE_SHEETS_POLICY.md`는 legacy migration 의미의 canonical reference로 유지한다. 별도 coupled test owner가 필요한 legacy workbook 본문은 P01에서 임의로 단독 재작성하지 않고 cross-part follow-up으로 넘긴다.
- **Evidence:** PR #534에서 permanent Base v9 test의 실제 RED → production 정규화 후 GREEN을 확인했다. 이후 Game Project Operating System workflow가 canonical reference/consumer 회귀를 잡아 Vertical Slice entrypoint와 Sheet migration policy reference를 복원했다.
- **Reusable lesson:** canonical authority migration 뒤에는 새 abstraction보다 active consumer drift와 coupled-test ownership을 먼저 감사한다. P01 소유 Skill을 고칠 때는 Skill-local learning + P01-owned companion test를 같이 움직여 reference-freshness 계약을 실제로 소비한다.
- **Anti-pattern:** legacy 호환 파일을 current workspace로 확대 해석; coupled test를 통과시키려고 다른 Part 테스트를 수정; 새 canon을 만들어 stale Manifest path를 맞춤.
- **Boundary:** 실제 프로젝트 Notion migration E2E, legacy Sheet의 UNIQUE material 이관·삭제, 사람 UX/기기 검증은 `NOT_RUN`이다.
- **Next trigger:** legacy Sheet coupled-test owner가 Integration에서 정리되거나 실제 Project Notion migration pilot에서 새로운 consumer gap이 발견될 때 재검토한다.

## 2026-08-19 · self-contained Project Home before drilldown

- 관찰: Project Home이 핵심 방향은 보여주지만 시스템/검증/구현 설명을 하위 페이지 링크에 의존하면 사용자가 프로젝트 전체를 읽기 위해 계속 이동해야 한다.
- 교훈: Notion human-facing canon의 첫 화면은 `HUMAN_HOME_SELF_CONTAINED_BEFORE_DRILLDOWN`을 만족해야 하며, 하위 페이지는 상세 증거용이어야 한다.
- 기대효과: cold-start 이해도 향상, 반복 질문 감소, 잘못된 project-state 추정 감소.
- reuse_scope: BASE_PROMOTION_CANDIDATE
