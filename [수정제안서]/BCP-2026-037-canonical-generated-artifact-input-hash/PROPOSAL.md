# BCP-2026-037 — Canonical Generated-Artifact Input Hash Across Checkout EOL

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 기준 커밋: `a94f95253206212a822402f002f100282f214323`
- 제출일: 2026-08-27
- 상태: `APPROVED_FOR_IMPLEMENTATION`
- 지식 상태: `검증`

## 관찰과 증거

- Base Issue [#757](https://github.com/alsdmlals4-eng/Base/issues/757)에서 Windows `core.autocrlf=true` checkout으로 clean OMENWARD `main`을 읽었다.
- `check_approved_project_operating_contract.py`는 health evidence 문제 없이 통과 단계까지 진행했지만, generated artifact 5개가 stale이라고 판정했다.
- 같은 committed input에서 Base `build_artifacts(..., prevalidated=True)`가 `PROJECT_BASE_ADAPTER.json` 및 legacy input의 CRLF working-tree raw SHA-256을 출력에 기록했다. Git blob/LF 기준 committed output의 hash field만 바뀌었으며 product source는 변경되지 않았다.
- 생성 결과를 버리고 committed artifacts로 되돌리면 project worktree는 clean으로 복구된다. 따라서 원인은 project content가 아니라 generator input hash의 checkout-byte 의존성이다.

## 일반화 후보

clean tracked generator input의 source/legacy hash는 working-tree EOL 변환에 의존하지 않아야 한다. generator는 clean tracked file의 canonical `HEAD` Git blob SHA-256을 기록하고, untracked·Git lookup 불가 input은 기존 working-tree raw-byte hash로 fallback한다. substantive dirty content는 clean canonical path에 진입하지 않아야 한다.

## 프로젝트 전용으로 남길 내용

- OMENWARD Run Command protected baseline, approval manifest, asset 목록과 produced mismatch path
- OMENWARD의 Base release pin 및 current visual/runtime 상태

## 적용 조건과 비사용 조건

- 적용: project repository root 안에서 `HEAD` clean 상태로 Git 추적되는 generator input.
- 비사용: untracked input, repository 밖 경로, symlink/reparse escape, Git object lookup/state inspection failure. 기존 confined working-tree raw-byte hash를 유지한다.

## 반례와 위험

- dirty content에서 canonical blob hash를 허용하면 실제 source 변경이 감춰질 수 있다. implementation은 Git diff로 dirty input을 배제한다.
- field label `RAW_FILE_BYTES_SHA256`은 기존 data contract다. implementation은 label을 조용히 재정의하거나 project adapter schema를 넓히지 않고, compatibility impact와 migration 필요성을 focused test로 확인한다.
- generated artifact output과 source authority, protected-path/approval policy, health evidence uniqueness·maturity gate는 약화하지 않는다.

## 영향 범위와 검증

- Base `tools/project_operating_contract.py`의 generated source/legacy input fingerprint resolver와 focused unit tests만 변경 후보로 둔다.
- Baseline: LF committed generator output validates.
- Regression: CRLF clean checkout produces byte-identical generated artifacts.
- Counterexample: substantive tracked input mutation remains fail-closed rather than using canonical blob content.
- Existing Base checks and the approved OMENWARD contract checker are run after implementation.

## 필요한 도구·파일·권한

- 필요 항목: existing Git executable, Base contract checker, Python unittest.
- 필요한 이유: canonical Git bytes readback, deterministic artifact comparison, and cross-checkout regression verification.
- 설치·적용 방법: no new dependency; existing repository tools only.
- 설치 후 확인 명령: focused unittest, Base CI, and approved OMENWARD contract check.
- 최소 권한: Base proposal/approval/implementation PR write; no OMENWARD protected source mutation.

## 승인과 구현

- 사용자 승인 근거: current Codex task의 autonomous continuation authority; proposal PR #758 merged and Base Issue #757 scope is approved for a separate minimal implementation PR.
- 구현 PR: `PENDING`
- 롤백: canonical generator-input resolver와 regression test를 revert하면 existing raw working-tree behavior로 돌아간다.
