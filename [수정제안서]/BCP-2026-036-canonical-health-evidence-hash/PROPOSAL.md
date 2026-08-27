# BCP-2026-036 — Canonical Health Evidence Hash Across Checkout EOL

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 기준 커밋: `a94f95253206212a822402f002f100282f214323`
- 제출일: 2026-08-27
- 상태: `IMPLEMENTED`
- 지식 상태: `검증`

## 관찰과 증거

- Base Issue [#751](https://github.com/alsdmlals4-eng/Base/issues/751)에서 `core.autocrlf=true` Windows checkout이 health evidence의 working-tree raw-byte SHA-256을 변경해 valid committed evidence를 실패시키는 것을 재현했다.
- 증거 파일은 project `HEAD` 대비 변경되지 않았고, health record와 해당 evidence는 같은 project commit `b28533cba722e293fdbfc1d1b43478dd8ded380d`에서 함께 갱신됐다.
- 현재 검증기는 working-tree bytes만 해시하므로 checkout EOL 변환이 `CURRENT` Sheet claim의 unique verified evidence 판정을 연쇄적으로 실패시킨다.

## 일반화 후보

Git 추적 파일의 clean health evidence 무결성은 기존 working-tree raw-byte hash와 현재 `HEAD`의 canonical Git blob hash를 함께 허용해야 한다. 이렇게 하면 기존 raw-byte record와 checkout EOL 변환 모두 호환한다. Git 객체를 확인할 수 없거나 추적되지 않은 evidence는 기존 working-tree raw-byte hash를 유지한다.

## 프로젝트 전용으로 남길 내용

- OMENWARD의 evidence ID, Sheet ID, 경로, SHA-256 값, protected baseline, Godot/visual/runtime 상태
- Issue #751의 project-specific reproduction values

## 적용 조건과 비사용 조건

- 적용: Git repository 안의 `HEAD`가 가리키는 regular tracked health-evidence file.
- 비사용: untracked/generated evidence, symlink, repository 밖 경로, 또는 Git object lookup 실패 경로. 이 경우 기존 confined working-tree hash 계약을 사용한다.

## 반례와 위험

- Working tree가 `HEAD`와 다른 substantive content이면 canonical blob hash만으로는 변경을 놓칠 수 있다. 구현은 Git diff로 clean tracked 상태를 먼저 확인하고, 내용 변경이 있으면 canonical hash를 허용하지 않아 working-tree raw-byte comparison만 유지한다.
- 이 규칙은 evidence source confinement, existence, unique source/ID, verdict/maturity gate를 약화하지 않는다.

## 영향 범위와 검증

- Base `tools/project_operating_contract.py`의 health evidence hash resolver와 관련 unit tests만 변경한다.
- Baseline: LF evidence validates.
- Regression: CRLF-converted checkout evidence validates against the same declared canonical SHA-256.
- Counterexample: substantive text mutation still fails.
- Git-object lookup failure falls back to working-tree raw bytes.

## 필요한 도구·파일·권한

- 필요 항목: `git cat-file`, Base contract checker, Python unittest.
- 필요한 이유: canonical blob bytes를 read-only로 얻고 contract behavior를 verify한다.
- 설치·적용 방법: existing Git executable only; no new dependency or project mutation.
- 설치 후 확인 명령: focused unittest and `check_approved_project_operating_contract.py` against the clean OMENWARD checkout.
- 최소 권한: Base implementation PR write; no protected project paths.

## 승인과 구현

- 사용자 승인 근거: current Codex task의 “전환했어 진행해”가 Base Issue #751 범위를 승인했다. Proposal registration PR #752 병합 뒤 이 승인 상태를 별도 PR로 기록했다.
- 구현 PR: [#755](https://github.com/alsdmlals4-eng/Base/pull/755), squash merge `49598091d9cd1491b583a24602c4f852ee77e330`.
- 구현 검증: focused autocrlf/health-evidence 회귀 2건 및 원격 `base-v9-contract`, `ubuntu-contract`, `core-regression`, `publication-validation`, `docs-validation`, `adversarial-gate` PASS. 로컬 전체 34건은 `publication_v3.py`의 선택 의존성 Pillow 부재로 1건 중단됐으며, 원격 publication validation에서 해당 의존성을 설치해 PASS했다.
- 롤백: canonical resolver와 tests를 되돌리면 legacy raw working-tree behavior로 복귀한다.
