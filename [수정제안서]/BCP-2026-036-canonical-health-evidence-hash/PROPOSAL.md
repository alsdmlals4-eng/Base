# BCP-2026-036 — Canonical Health Evidence Hash Across Checkout EOL

## 출처와 상태

- 출처 프로젝트: `alsdmlals4-eng/omenward`
- 기준 커밋: `a94f95253206212a822402f002f100282f214323`
- 제출일: 2026-08-27
- 상태: `SUBMITTED`
- 지식 상태: `검증`

## 관찰과 증거

- Base Issue [#751](https://github.com/alsdmlals4-eng/Base/issues/751)에서 `core.autocrlf=true` Windows checkout이 health evidence의 working-tree raw-byte SHA-256을 변경해 valid committed evidence를 실패시키는 것을 재현했다.
- 증거 파일은 project `HEAD` 대비 변경되지 않았고, health record와 해당 evidence는 같은 project commit `b28533cba722e293fdbfc1d1b43478dd8ded380d`에서 함께 갱신됐다.
- 현재 검증기는 working-tree bytes만 해시하므로 checkout EOL 변환이 `CURRENT` Sheet claim의 unique verified evidence 판정을 연쇄적으로 실패시킨다.

## 일반화 후보

Git 추적 파일의 health evidence 무결성은 working-tree 변환 바이트가 아니라 현재 `HEAD`의 canonical Git blob bytes로 검증해야 한다. Git 객체를 확인할 수 없거나 추적되지 않은 evidence는 기존 working-tree raw-byte hash를 유지한다.

## 프로젝트 전용으로 남길 내용

- OMENWARD의 evidence ID, Sheet ID, 경로, SHA-256 값, protected baseline, Godot/visual/runtime 상태
- Issue #751의 project-specific reproduction values

## 적용 조건과 비사용 조건

- 적용: Git repository 안의 `HEAD`가 가리키는 regular tracked health-evidence file.
- 비사용: untracked/generated evidence, symlink, repository 밖 경로, 또는 Git object lookup 실패 경로. 이 경우 기존 confined working-tree hash 계약을 사용한다.

## 반례와 위험

- Working tree가 `HEAD`와 다른 substantive content이면 canonical blob hash만으로는 변경을 놓칠 수 있다. 구현은 canonical hash 사용 전에 working-tree raw bytes가 canonical blob bytes와 같은 경우에만 canonical comparison을 허용하고, 내용이 실제로 다르면 working-tree raw-byte comparison을 유지한다.
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

- 사용자 승인 근거: current Codex task의 “전환했어 진행해”가 Base Issue #751 범위를 승인했다. 다만 Base proposal lifecycle에 따라 이 PR은 `SUBMITTED` 등록만 수행하며, 승인 상태 승격은 등록 병합 뒤 별도 PR에서 기록한다.
- 구현 PR: `PENDING`
- 롤백: canonical resolver와 tests를 되돌리면 legacy raw working-tree behavior로 복귀한다.
