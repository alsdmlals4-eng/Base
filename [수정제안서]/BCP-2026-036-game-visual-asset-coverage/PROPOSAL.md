# BCP-2026-036 — Game Visual Asset Coverage Preflight

## 출처와 상태

- 출처 프로젝트: `Base 공용 게임 개발 workflow`
- 기준 커밋: `713756c34c52caf8a00c86bf1d7a240f6e6a7092`
- 제출일: `2026-08-26`
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `패턴`
- approval_ref: `2026-08-26 사용자 지시 — 게임 개발 필수 이미지·에셋 목록을 적대적 검토·벤치마킹·실무 조사·교정 후 Base에 올리고, 이후 이미지 생성마다 해당 체크리스트로 누락을 추적하도록 명시 승인`
- registry_status: `DEFERRED_CONCURRENCY` — 현재 open PR #678이 `[수정제안서]/PROPOSAL_REGISTRY.json`을 소유하므로 해당 경로는 read-only로 유지한다. Registry 반영은 그 소유권이 해제된 뒤 별도 lifecycle reconciliation 대상으로 남긴다.

## 관찰과 증거

현재 Base에는 이미 다음 책임이 있다.

- `ART_DIRECTION_AND_ASSET_PLANNING_GUIDE.md`의 Visual Requirement Gate가 필요성, Delete Test, role, P0~P3, reuse/disposition을 판정한다.
- `GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`가 explicit image approval, candidate review, Notion delivery, asset promotion, runtime evidence를 소유한다.
- `designing-art-prompts-and-technique-cards`가 선정된 requirement를 실제 생성·편집·검수 계약으로 변환한다.
- `ASSET_MANIFEST.yml`, Project Asset Vault, Notion Asset/Visual record가 실제 승인 자산과 파일 상태를 소유한다.

그러나 프로젝트 전체 또는 화면·캐릭터·시스템군을 작업할 때 **어떤 종류와 상태의 시각 자산을 확인했는지**를 빠르게 점검하는 공용 coverage 기준은 분산되어 있다. 이로 인해 기본 캐릭터·배경은 있으나 버튼 상태, enemy telegraph, 피격/보상 feedback, 입력 prompt, 접근성 cue, platform/store asset, runtime 소비 규격처럼 실제 개발에서 필요한 인접 자산이 누락될 수 있다.

외부 현행 공식 자료와 비교한 결과도 같은 보강 방향을 지지한다.

- Godot는 2D/UI에서 base design size, 다양한 해상도·종횡비·stretch/scale을 명시적으로 다루며 이미지 import/compression/filter/mipmap 등 소비 조건도 자산 성격에 따라 달라진다.
- Steam은 store/library graphical assets와 gameplay screenshot을 별도 요구하며 capsule 내용 규칙을 운영하므로 release 시점의 공식 규격 재확인이 필요하다.
- 접근성 실무는 중요한 상태를 색 하나에만 의존하지 않고 형태·아이콘·텍스트 등 중복 cue로 전달하는 쪽이 안전하다.
- 다른 엔진의 대규모 production practice에서도 naming/variant/atlas 같은 반복 생산 관리 원리는 유효하지만 Godot 프로젝트에 엔진 고유 convention을 그대로 강제할 이유는 없다.

## 일반화 후보

`VISUAL_ASSET_COVERAGE_PREFLIGHT`를 기존 Visual Requirement Gate 앞의 누락 탐지 단계로 추가한다.

핵심 불변식:

1. `COVERAGE_CHECK_ONLY` — 체크리스트는 필요 후보를 발견하는 기준표다.
2. `NOT_A_SECOND_ASSET_CANON` — 실제 requirement, 승인, 파일, manifest, runtime state를 복제 소유하지 않는다.
3. `NO_AUTOMATIC_IMAGE_GENERATION_FROM_GAPS` — gap 발견은 이미지 생성·batch 확대 권한이 아니다. 기존 explicit image conversation approval을 계속 적용한다.
4. `STATE_FAMILY_COMPLETENESS` — 단일 대표 이미지뿐 아니라 소비처가 요구하는 상태군을 확인한다.
5. `PLATFORM_SPEC_RECHECK_REQUIRED` — 플랫폼 제출용 자산은 Base에 장기 고정 수치를 복제하지 않고 release 시 공식 문서를 재조회한다.
6. coverage 결과는 기존 `requirement_id` 또는 승인 asset/runtime evidence에 link하여 닫는다.

권장 coverage 상태:

`NOT_REVIEWED | NOT_APPLICABLE | COVERED_EXISTING | REQUIREMENT_LINKED | GAP_BLOCKING | GAP_NONBLOCKING | DEFERRED_BY_DECISION`

이 상태는 asset lifecycle(`GENERATED_EXPLORATION`, `PROJECT_ASSET_APPROVED`, `APPLIED_AND_RUNTIME_VERIFIED`)을 대체하지 않는다.

## 프로젝트 전용으로 남길 내용

- 특정 프로젝트의 실제 캐릭터·적·UI·건물·아이템 수량
- 프로젝트 고유 아트 스타일, 팔레트, 화면 구성, IP/세계관 표현
- 특정 플랫폼 출시 여부와 현재 플랫폼 규격 수치
- 실제 asset path, file hash, import preset, runtime 적용 상태
- 개별 이미지 생성 prompt와 승인 이미지

## 적용 조건과 비사용 조건

적용:

- 게임 프로젝트의 화면군·캐릭터군·적군·UI군·아이템군·환경군·마케팅 asset set을 계획하거나 이미지 생성을 시작할 때
- Vertical Slice/Production/Release readiness에서 player-facing visual 누락을 검사할 때
- 사용자가 “필요 이미지/에셋을 빠뜨리지 말라”는 범위 추적을 요구할 때

비사용:

- 단일 이미지 한 장의 단순 수정에서 전체 프로젝트 asset inventory를 억지로 확장할 때
- 문서/서사 작업처럼 시각 asset coverage가 소비되지 않는 작업
- coverage gap만을 근거로 사용자 승인 없이 이미지를 자동 생성하거나 대량 batch화할 때

## 반례와 위험

- 모든 항목을 무조건 P0로 만들면 scope explosion이 발생한다. 따라서 `NOT_APPLICABLE`, stage, Delete Test, priority가 필요하다.
- coverage 상태를 실제 asset 상태와 합치면 second canon이 된다. 반드시 링크만 한다.
- 플랫폼 이미지의 현재 pixel size를 공용 장기 규칙으로 하드코딩하면 stale될 수 있다.
- 3D material map, 8-direction sprite, portrait 등은 장르/기술에 따라 불필요할 수 있다.
- placeholder는 PoC에는 필요하지만 shipping-intent player-facing slice에 남아 있으면 최종 경험 검증을 왜곡한다.
- 체크리스트가 user approval gate를 우회하면 기존 이미지 생성 안전 계약과 충돌한다.

## 영향 범위와 검증

승인된 최소 구현 범위:

- 신규 subordinate guide: `docs/knowledge/game-development/GAME_VISUAL_ASSET_COVERAGE_CHECKLIST.md`
- 기존 owner 연결: `docs/GPT_IMAGE_GENERATION_AND_REVIEW_POLICY.md`
- 기존 실행 Skill 연결: `skills/designing-art-prompts-and-technique-cards/SKILL.md`
- 기존 계획/검수 템플릿 연결: `templates/planning/GPT_IMAGE_GENERATION_AND_REVIEW_PLAN.md`
- focused regression test
- 5회 이상 whole-state adversarial review receipt

제외/보호:

- 새 Skill, 새 Tool, 새 provider, 새 유료 서비스 추가 금지
- `skills/SKILL_REGISTRY.json`, generated skill view 변경 금지
- open PR #713이 소유한 Notion visual workflow/UI audit 경로 변경 금지
- open PR #660이 소유한 `docs/DOCUMENTATION_MAP.md` 변경 금지
- `[수정제안서]/PROPOSAL_REGISTRY.json`은 open PR #678이 소유 중이므로 현재 작업에서 변경 금지
- 실제 프로젝트 asset/runtime PASS 주장 금지

검증:

- test-first regression: coverage guide/owner/Skill/template routing contract
- diff/concurrency check
- 최소 5회 whole-state adversarial review
- current-main reconciliation, required checks, post-merge readback

## 필요한 도구·파일·권한

- 필요 항목: 기존 GitHub connector, Base repository write/PR 권한, 현재 연결된 web research
- 필요한 이유: 최신 main/오픈 PR 경계 확인, 공식 실무자료 검증, 별도 proposal/implementation lifecycle 수행
- 설치·적용 방법: 신규 설치 없음
- 설치 후 확인 명령: 해당 없음
- 최소 권한: Base branch/file/PR 작성 및 정상 merge 권한; admin/ruleset bypass 불필요

## 승인과 구현

- 사용자 승인 근거: `approval_ref`에 기록된 2026-08-26 명시 지시
- 구현 PR: `별도 implementation PR에서 연결 예정`
- 롤백: implementation PR 전체 revert. 기존 Visual Requirement Gate, Image Conversation Approval Gate, asset lifecycle을 삭제하거나 대체하지 않는다.
