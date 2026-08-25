# BCP-2026-031 Implementation Closeout

## 상태

- BCP: `BCP-2026-031-web-platform-native-ui-capability`
- 최종 상태: `IMPLEMENTED`
- 구현 PR: `https://github.com/alsdmlals4-eng/Base/pull/667`
- 구현 squash merge: `dc8e5ed6b36b3937b38e56a40814aa464438d45e`
- closeout 기준일: `2026-08-25`
- 추가 금전 비용: `0`

## 승인 범위

사용자가 2026-08-25 현재 작업에서 승인한 범위는 다음 세 파일의 최소 구현이었다.

1. `docs/knowledge/research/WEB_PLATFORM_NATIVE_UI_CAPABILITY_GUIDE.md`
2. `docs/knowledge/README.md`의 최소 라우팅
3. `tests/test_web_platform_native_ui_capability.py`

신규 Skill·Tool·dependency·runtime·별도 workspace, 전역 framework 강제/금지, 퇴역 surface 재활성화는 승인 범위가 아니었다.

## 실제 변경

구현 PR `#667`은 승인된 세 파일만 변경했다.

- `docs/knowledge/research/WEB_PLATFORM_NATIVE_UI_CAPABILITY_GUIDE.md`
  - `PLATFORM_NATIVE_FIRST`
  - `CAPABILITY_NOT_DEVICE_LABEL`
  - `PROGRESSIVE_ENHANCEMENT_REQUIRED_FOR_NEWLY_AVAILABLE`
  - `NATIVE_IS_NOT_AUTOMATIC_UX_PASS`
  - `SUPPORT_STATUS_IS_DATED_EVIDENCE`
  - `ACCESSIBILITY_INPUT_FALLBACK_REQUIRED`
  - `LIVE_BEHAVIOR_EVIDENCE_OVER_CODE_SNIPPET`
  - `RETIRED_SURFACE_IS_NOT_REACTIVATED`
  - Semantic HTML → Native CSS → Browser API → 기존 구현 → 경량 dependency → Minimal Custom Implementation 순서
  - 지원 상태를 `verified_at`이 붙은 dated evidence로 관리
  - native 기능도 UX·접근성·실제 target-browser 증거 없이는 자동 PASS하지 않도록 규정
- `docs/knowledge/README.md`
  - Web Platform native UI capability Guide로 가는 라우팅 한 줄만 추가
- `tests/test_web_platform_native_ui_capability.py`
  - 위 계약·라우팅·퇴역 surface 보호를 회귀 테스트로 고정

## TDD 증거

### RED

- test-only HEAD: `1116d82fd73a5929a789127a071ccdd0b5008341`
- core regression job: `97645016314`
- 결과: `1 failed, 285 passed`
- 유일한 실패: 승인된 Web Platform native UI capability Guide가 아직 존재하지 않는다는 assertion
- 기존 회귀 285개는 통과했으므로 새 계약의 부재를 정확히 포착한 RED로 판정했다.

### GREEN

- 최종 구현 HEAD: `9c620799971a1510339267cd2b80157c91fcdc1c`
- `Validate Base v9 Workflow Contract`: run `32795636633` — `success`
- `Validate Game Project Operating System`: run `32795636648` — `success`
- core regression job: `97646330259` — `success`
- failure diagnostic upload는 실패가 없어 실행되지 않았다.

GREEN 단계에서는 추정 테스트 수를 기록하지 않고, 최종 HEAD의 전체 core-regression job 성공을 완료 증거로 사용한다.

## Post-merge readback

구현 PR `#667`을 exact HEAD로 squash merge한 뒤 main `dc8e5ed6b36b3937b38e56a40814aa464438d45e`에서 다시 읽어 다음을 확인했다.

- Guide가 main에 존재하고 승인된 공용 계약과 구현 선택 순서를 포함한다.
- `docs/knowledge/README.md`에 Guide 라우팅이 존재한다.
- 기존 `docs/DEPRECATED_PROJECT_SURFACE_RETIREMENT_POLICY.md`의 Tool Hub·QA Evidence Studio retirement marker가 유지된다.
- 구현 PR의 변경 파일은 승인된 세 파일뿐이다.

## 범위 보호와 적대적 검토 결과

- draft PR `#660`이 소유 중인 `docs/DOCUMENTATION_MAP.md`는 수정하지 않았다.
- 구현 중 README 전체 파일 재작성에서 승인 범위 밖 문구 1줄이 우발적으로 바뀐 것을 diff 검토에서 발견했고, 병합 전에 원문으로 복구했다. 최종 README diff는 라우팅 한 줄뿐이다.
- `Tool Hub`를 active/default project route로 부활시키지 않았다.
- `QA Evidence Studio`를 active/default project route로 부활시키지 않았다.
- `external HTML workspace`를 canonical project-management surface로 부활시키지 않았다.
- 신규 Skill·Tool·dependency·runtime·workspace를 추가하지 않았다.
- React/Vue/Svelte 등 특정 framework의 전역 사용 금지/강제 규칙을 추가하지 않았다.
- 브라우저 지원 상태는 영구 정본 allow-list가 아니라 공식 출처와 `verified_at`을 가진 dated evidence로 제한했다.

## 롤백

필요 시 구현 squash merge `dc8e5ed6b36b3937b38e56a40814aa464438d45e`를 revert하거나, 승인된 세 변경 요소(Guide, README 라우팅, focused test)를 함께 제거하면 이전 authority 구조로 복귀한다. 퇴역 surface 정책과 기존 Base runtime에는 별도 migration이 없다.

## 결론

BCP-2026-031은 사용자 승인 범위 안에서 구현·검증·main readback까지 완료되었다. closeout 이후 상태는 `IMPLEMENTED`로 관리한다.
