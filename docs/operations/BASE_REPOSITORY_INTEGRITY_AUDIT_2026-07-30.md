# Base 저장소 전체 무결성 감사 — 2026-07-30

> 상태: `IN_PROGRESS`
> Work Mode: `REVIEW → BUILD → REVIEW`
> 기준 main: `dc98a666563b1f0f87b665eac97dbd8a8be37576`
> 작업 Branch: `agent/base-repository-integrity-audit-20260730`
> 작업 PR: `PR #72`
> 프로젝트 Google Sheets: `BASE_EXCLUDED`

## 1. 요청·범위·보호 대상

목표는 Base의 현행 Skill·작업 구조를 이해한 뒤 저장소 전체의 충돌·누락·구형 참조·중복·장문·고아 파일·파생본 drift를 적대적으로 감사하고, 검증된 기술 결함을 최소 수정하는 것이다.

포함:

- Base 진입 문서·운영 정책·Documentation Map
- Skill Registry·Legacy Alias·Skill package·agent metadata
- Template·Prompt·Test·Workflow·생성본·Archive
- 열린·최근 PR과 현재 Issue의 중복·대체 관계

제외·보호:

- 개별 프로젝트 저장소와 Google Sheets
- 제품 코드·Scene·data·Resource·asset·balance·플레이 규칙
- 사용자 결정 없는 대량 삭제·정본 교체·프로젝트 방향 변경

## 2. 실행한 Skill·Mode

| Work Mode | Skill·프로토콜 | Mode·사용 이유 | 현재 결과 |
|---|---|---|---|
| PLAN | Superpowers `brainstorming` | 목표·범위·승인 경계 확인 | 저장소 감사와 충돌 Grill Me 계약 확정 |
| PLAN | Superpowers `writing-plans` | 다중 단계 작업 순서화 | 인벤토리 → 분류 → 최소 수정 → 검증 순서 고정 |
| REVIEW | `running-adversarial-review-and-refinement` | `repository-wide-audit` | 이중 정본·구형 Skill 경로·열린 PR·파생본 후보 수집 |
| PLAN/BUILD | `governing-legacy-retention-and-archives` | `inventory / classify / reconcile / archive` | `docs/ACTIVE_HANDOFF.md` 처리안 A 승인·적용 중 |
| BUILD | Superpowers `test-driven-development` | Archive 권한 계약 회귀 방지 | RED 확인 후 구현 진행 |
| REVIEW | `auditing-canonical-reference-freshness` | 정본·경로 변경 소비자 확인 | Documentation Map·Test·Manifest 연결 중 |
| REVIEW | Superpowers `verification-before-completion` | 완료 주장 전 실제 CI 확인 | 최종 GREEN 전에는 완료로 보고하지 않음 |

## 3. 감사 범위와 미검증 범위

확인한 기준:

- `START_HERE.md`, `AGENTS.md`, `docs/OPERATING_MODEL.md`, `docs/DOCUMENTATION_MAP.md`
- `skills/SKILL_REGISTRY.json`, `skills/LEGACY_SKILL_ALIASES.md`, 생성된 27-Skill 목록
- Base v9 release·integrity·adversarial 문서
- 관련 Skill 본문과 repository-wide audit·archive contract
- main 대비 release commit 이후 변경
- 열린 PR #5, #18, #28, #29, #30과 Issue #54, #55, #71
- PR #72의 GitHub Actions RED 증거

미검증:

- Connector 검색 결과만으로는 tracked 전체 목록·모든 inbound reference를 완전 증명할 수 없다.
- 로컬 checkout이 없어 전체 `python -m unittest discover`, `git diff --check`, 로컬 링크 검사 명령은 직접 실행하지 못했다.
- GitHub Actions는 PR #72에서 실행하며, 각 변경 commit의 결과를 별도 기록한다.
- 개별 프로젝트와 Sheet는 범위 밖이며 상태 일치를 추정하지 않는다.

## 4. 권한 지도

| 책임 | CURRENT_AUTHORITY | 소비자·호환·이력 |
|---|---|---|
| Base 운영 생명주기 | `docs/OPERATING_MODEL.md` | `START_HERE.md`, `AGENTS.md`, `docs/DOCUMENTATION_MAP.md` |
| 활성 Skill | `skills/SKILL_REGISTRY.json` | `docs/generated/BASE_ACTIVE_SKILLS.md`, snapshot·plugin metadata |
| 이전 Skill ID | `skills/LEGACY_SKILL_ALIASES.md` | 과거 Issue·PR·case·호환 검색 |
| Base 완료 상태 | `docs/CHANGELOG.md` | release·operations 문서 |
| 진행 중 Base 변경 | GitHub Issue·PR·Actions | PR #72 |
| 프로젝트 현재 상태 | 각 프로젝트 저장소 책임 원본 | Base에서 현재 상태를 복제하지 않음 |
| Base Archive | `docs/archive/ARCHIVE_MANIFEST.json` | `docs/archive/README.md`, compatibility Stub |

## 5. Finding

### F-001 — Base 내부 프로젝트 간 Active Handoff 이중 정본

- 유형: `DUPLICATE_ACTIVE_SOURCE / CONFLICTING_SOURCE`
- 심각도: `MUST_FIX`
- 후보: `docs/ACTIVE_HANDOFF.md`
- 충돌: Base 콜드 스타트 계약은 프로젝트별 활성 상태를 Base에 두지 않지만, 해당 파일은 다섯 프로젝트의 현재 상태·다음 작업을 활성 Handoff처럼 제시했다.
- 고유 정보: 2026-07-29 확산 기준 commit, 프로젝트별 Gate, 당시 미검증·롤백 기록.
- 사용자 결정: `DEC-2026-07-30-001` — 선택지 A 승인.
- 판정: 원문은 `ARCHIVE_HISTORY`, 기존 경로는 `COMPATIBILITY_ONLY`.
- Archive: `docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md`
- Manifest: `docs/archive/ARCHIVE_MANIFEST.json`
- Rollback ref: `dc98a666563b1f0f87b665eac97dbd8a8be37576`
- 검증: TDD RED에서 Archive 부재로 정확히 실패함. GREEN 재검증 대기.

### F-002 — `skills/README.md`가 통합 전 Skill ID를 활성 목록처럼 안내

- 유형: `STALE_REFERENCE / CONFLICTING_SOURCE`
- 심각도: `MUST_FIX`
- 근거: Registry는 27개 활성 Skill을 권한으로 삼지만 README는 `conducting-deep-requirement-interviews`, `transforming-requests-into-prompts`, `writing-game-design-documents` 등 이전 ID를 활성 실행 스킬 표에 둔다.
- 처리 방향: 활성 목록을 중복 유지하지 않고 Registry 생성 뷰·Legacy Alias·Skill 배치 원칙만 안내하는 Router로 축약.
- 상태: `PENDING_FIX`.

### F-003 — 통합 전 Skill agent metadata가 구형 경로에 잔존

- 유형: `ORPHANED_REFERENCE / STALE_REFERENCE`
- 심각도: `SHOULD_FIX` 후보
- 후보: `skills/conducting-deep-requirement-interviews/agents/openai.yaml`
- 현재 사실: 해당 `SKILL.md`는 제거됐지만 agent metadata는 이전 Skill ID와 default prompt를 유지한다.
- 필요한 판정: 현행 `managing-project-intake-and-work-contract` package로 승계할 고유 metadata가 있는지 확인 후 `COMPATIBILITY_ONLY / MERGE_TO_CANONICAL / DELETE_APPROVED` 결정.
- 상태: `INVESTIGATING`.

### F-004 — v7·v8 통합 Prompt 동시 존재

- 유형: `STALE_PROMPT_CONTRACT` 후보
- 심각도: `SHOULD_FIX / ALLOWED_LEGACY` 판정 대기
- 현재 사실: START_HERE와 Documentation Map은 v8을 현행으로 사용하지만 v7 테스트·파일도 존재한다.
- 필요한 판정: v7이 명시적 compatibility fixture인지, 활성 소비자가 남았는지, v8과 중복 권한을 주장하는지 대조.
- 상태: `INVESTIGATING`.

### F-005 — v9 이전 base SHA에서 갈라진 열린 PR 5개

- 유형: `DUPLICATE_WORK / SUPERSEDED_WORK` 후보
- 대상: PR #5, #18, #28, #29, #30
- 현재 사실: 모두 Base v9 release 전 기준에서 시작했고, 일부 내용은 Issue #54·v9 migration에서 고유 요구를 승계했다고 명시한다.
- 위험: 그대로 병합하면 현행 Registry·운영 모델을 되돌리거나 이중 책임을 재도입할 수 있다.
- 처리: 고유 commit·제안·승계 여부를 확인한 뒤 `KEEP / SUPERSEDED_CLOSE / PROPOSAL_RETAIN` 중 사용자 결정이 필요한 충돌만 Grill Me로 질문한다.
- 상태: `USER_DECISION_SEQUENCE_PENDING`.

### F-006 — 릴리스 전 감사 보고서의 `UNVERIFIED` 표현과 현재 `BASE_RELEASED` 상태

- 유형: `HISTORY_CURRENT_STATUS_AMBIGUITY`
- 심각도: `SHOULD_FIX` 후보
- 현재 사실: `docs/operations/BASE_V9_INTEGRITY_AUDIT.md`는 “final verification 전 상태”를 보존하고, `docs/BASE_RULES_VERSION.md`는 v9.0.0이 release evidence와 함께 병합됐다고 선언한다.
- 처리 방향: 과거 보고서를 다시 쓰지 않고 상단에 `HISTORY_ONLY / release 당시 최종 상태는 BASE_RULES_VERSION·RELEASE_CONTRACT 참조`를 명시하는 호환 보완 검토.
- 상태: `INVESTIGATING`.

## 6. 실제 반영한 변경

- PR #72와 격리 Branch 생성.
- `tests/test_v9_governance_documents.py`에 Archive 권한 회귀 테스트 추가.
- `docs/archive/README.md`와 `docs/archive/ARCHIVE_MANIFEST.json` 생성.
- UX/UI 확산 Handoff 원문을 `docs/archive/handoffs/2026-07-29-ux-ui-common-system-expansion.md`로 보존.
- `docs/ACTIVE_HANDOFF.md`를 `COMPATIBILITY_ONLY` Stub으로 교체.
- `docs/DOCUMENTATION_MAP.md`를 책임 원본·프로젝트 경계·Archive·Reference 중심 Router로 컴팩트화.

## 7. RED 증거

PR #72 commit `4f6687506ec5ce039a79a9797d239fa8cfea86bf`의 `Validate Base v9 RC` run `30521143559`:

- integrity topology: `PASSED`
- 기존 검사: 19개 통과
- 신규 Archive 계약: Archive 파일 부재로 1개 실패
- 전체: `Ran 20 tests`, `FAILED (failures=1)`

이 실패는 구현 전 기대한 원인과 일치한다.

## 8. 다음 순서

1. F-001 GREEN CI와 hash·Manifest·link·cold-start 회귀 확인.
2. F-002 `skills/README.md`를 Registry-derived Router로 수정.
3. F-003 구형 agent metadata의 승계·호환·제거 Gate 판정.
4. v7/v8 Prompt 소비자·테스트·별칭 감사.
5. 릴리스 전 operations 보고서의 역사/현재 상태 경계 보완.
6. 열린 PR별 고유 요구를 비교하고 사용자 결정을 한 번에 하나씩 Grill Me로 진행.
7. 전체 관련 Workflow와 최종 적대적 회귀 실행.

## 9. 현재 판정

`IN_PROGRESS / PASS_NOT_CLAIMED`

F-001의 구조 변경은 반영됐지만 GREEN CI와 후속 Finding 처리가 남았다. 실행하지 않은 전체 회귀·로컬 검사·프로젝트 검증은 완료로 보고하지 않는다.
