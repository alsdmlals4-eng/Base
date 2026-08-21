# Synchronizing Local and GitHub State — Learning Log

## 2026-08-21 — Capability fallback vocabulary must survive authorization hardening

- **Status:** `PATTERN`
- **Observed failure:** open-PR authorization을 더 강한 named PR/action 계약으로 교체하는 과정에서 `github_connector / local_git / gh_cli` provider 판정과 connector Git Data publication 단계가 Skill 본문에서 사라졌다. 보안 계약은 강화됐지만 optional `gh` 부재 복구의 실행 발견성이 약해졌다.
- **Correction:** 열린 PR read-only와 named authorization 계약은 유지하고, 독립된 `GITHUB_CAPABILITY_FALLBACK` 절에 provider 순서, `create_blob → create_tree → create_commit → update_ref(force=false)`, 반복 설치·재인증 금지를 복구했다.
- **Evidence ceiling:** 계약과 회귀 테스트는 capability routing의 발견성을 증명하지만 실제 connector 권한, 원격 write, CI, merge 성공은 각 실행에서 별도로 readback해야 한다.
- **Regression trigger:** authorization·owner 정책 개편이 missing-CLI fallback provider나 non-force Git Data 경로를 다시 제거하면 이 패턴을 재검토한다.

## 2026-08-18 — Reconcile moving integration state before overwriting or merging stale owners

- **Status:** `PATTERN`
- **Observed failures:** During the Base long-horizon governance integration, an attempted `AGENTS.md` write returned HTTP 409 because the branch file had advanced after the read. A broad Base-v9 run also caught floating GitHub Action tags in a newly added workflow even though the focused governance tests were already green. Several old open owner PRs still described RED or pre-successor states after stronger implementations had landed on `main`.
- **Recovery:** Treat both write conflicts and stale owner PRs as readback triggers, not as reasons to overwrite or merge wholesale. Re-read the exact current blob/head, preserve the newer material, selectively apply only the missing delta, and re-run broad exact-head contracts. For CI actions, use the repository's current exact 40-character action pins rather than a floating major tag.
- **Owner-PR reconciliation:** Close an old owner PR only after a current-main successor or integration proves that its unique material delta is fully absorbed. Preserve unrelated residual work as a separate scope instead of forcing it into the active integration.
- **Evidence ceiling:** A focused GREEN does not imply Base-wide compatibility. The Base-v9/GPO gates remain independent evidence; `NOT_RUN`, stale workflow results, or old PR bodies never become PASS by inference.
- **Regression trigger:** Any workflow that overwrites after a stale-blob/409 signal, merges a stale whole owner branch despite a current-main successor, uses floating action tags where Base requires exact pins, or treats focused CI as proof of repository-wide compatibility must reopen this pattern.

## 2026-08-16 — Latest-main copy integration becomes the standing conflict recovery

- **Status:** `PATTERN`
- **Observed failure:** `OBSERVED_FAILURE`. Per-case `PROVISIONAL_INTEGRATION` authorization and all-open-PR scheduled guards protected owner branches, but they also serialized unrelated work and repeatedly left approved work idle while long-running PRs remained open.
- **User decision:** adopt `BASE_COPY_INTEGRATION_STANDING_AUTHORIZATION_2026_08_16` as the Base coordination default. Existing owner PR branches remain read-only; approved same-goal/path/semantic overlap is reproduced on a separate branch from exact latest completed `main` using selective copy and semantic reconciliation.
- **Material-delta rule:** record `absorbed_owner_deltas` and `residual_owner_deltas`. Owner PR open state alone is not a merge blocker after all required material delta is accounted, stale duplicates are removed, latest main is reconciled, and exact-head safety gates pass. Fully absorbed owner PRs may be superseded after merge; residual unique work remains open.
- **Scheduled automation correction:** unrelated open PRs do not block Source analysis. Bounded repository writes compare the generated `changed-files.txt` with foreign PR changed paths and defer only actual overlap that cannot be safely reconciled by the automation.
- **Preserved boundary:** standing coordination authority does not authorize product-scope expansion, destructive migrations, payments, account/security privilege expansion, direct main writes, force push, `--admin`, ruleset bypass, or evidence inflation.
- **TDD evidence:** PR #436 first RED head `d2edf12d016e718808be87762fc9ae47a40b3bad` failed exactly two Evidence Knowledge assertions because the old scheduled all-open-PR guard and old workflow tokens were still present. No unrelated Evidence Knowledge regression was observed in that RED run.
- **Regression trigger:** any workflow that waits solely because a foreign PR is open, overwrites newer main with a stale whole-file copy, mutates an owner PR branch, loses residual unique work, or uses standing authorization to bypass exact-head/high-risk gates must reopen this policy.

## 2026-08-15 — Explicit provisional integration can reduce waiting without mutating owner PRs

- **Status:** `PATTERN`
- **Observed constraint:** `OBSERVED_FAILURE`. Long-running open owner PRs can hold the same Tool Hub paths for hours while their feature cores are already substantially implemented but stale integration baselines keep focused CI red. Treating every overlap as indefinite `WAITING_RESOURCE` forces independent latest-main integration work to stop even when the user explicitly wants a parallel integration branch.
- **Decision:** extend the existing `CONCURRENT_CHANGE_PREFLIGHT` rather than creating a second lock framework. Add `PROVISIONAL_INTEGRATION` only when the user gives explicit authorization for a latest-main integration PR. Record `owner_pr_head_shas`, `provisional_overlap_paths`, and `provisional_semantic_resources`; keep owner PR branches read-only.
- **Reconciliation rule:** owner PR merge/close/supersede/head movement or material main advance immediately triggers semantic reconciliation on the integration branch. Preserve the stronger/current canonical security, cost, platform, and data contract; remove stale provisional duplicates; rerun exact-head validation.
- **Merge boundary:** `PROVISIONAL_INTEGRATION` never means `CLEAR`. The integration PR must not merge while an overlapping owner remains unresolved unless that owner is merged and absorbed, explicitly handed off/superseded, or the user explicitly authorizes replacement. Without explicit provisional authorization, the default remains `WAITING_RESOURCE` / `DUPLICATE_WORK`.
- **TDD evidence:** RED workflow run `31852789710` failed because `PROVISIONAL_INTEGRATION` was absent from Base governance. GREEN run `31852960596` passed the same focused contract after the minimal rule was added. The temporary focused workflow was removed before the final merge candidate so the policy does not create a permanent redundant CI surface.
- **Adversarial result:** P0/P1/P2 = 0 for authorization bypass, owner-branch mutation, stale owner-head reuse, textual-only reconciliation, stale-CI reuse, and unresolved-owner merge attacks. This is governance evidence only; a later product integration PR must independently prove its Windows/Linux/runtime/Figma behavior.
- **Regression trigger:** any future workflow that treats ordinary continuous work as provisional-overlap authorization, writes to owner PR branches, hides overlap as `CLEAR`, or merges a provisional integration PR before owner resolution must reopen this policy.

## 2026-08-14 — Missing optional GitHub CLI must not override connector capability

- **Status:** `PATTERN`
- **Observed failure:** `OBSERVED_FAILURE`. A verified feature branch was ready to publish, but the workflow stopped at `gh: command not found` and asked the user to install or authenticate again even though an authenticated GitHub connector exposed Branch, Git object, PR, workflow-status, and merge operations.
- **Root cause:** tool identity was treated as the requirement. The real requirement was safe GitHub read/write capability at exact SHAs; `gh` was only one possible provider.
- **Correction:** keep `synchronizing-local-and-github-state` as the owner and add `GITHUB_CAPABILITY_FALLBACK`: prefer the GitHub connector for supported operations, retain `local_git` for local evidence, use `gh_cli` only for uncovered required capabilities, and classify missing CLI alone as `MISSING_OPTIONAL_CLI` rather than a global blocker.
- **Security boundary:** do not copy a user's Windows token into a cloud container or persist authentication through a non-secret `GH_TOKEN`. If every available provider lacks the exact required capability, report `BLOCKED_UNVERIFIED` with that capability instead of claiming completion.
- **Evidence:** the same session created a remote Branch, Git blobs/tree/commit, non-force ref update, and PR through the GitHub connector after unauthenticated `git push` failed. CI, merge, release, and post-merge readback remain separate gates.
- **Regression trigger:** any future workflow that asks for repeated CLI installation or authentication before checking connector coverage, or stops globally on missing optional `gh`, must reopen this policy.

## 2026-08-13 — Concurrent work needs identity, semantic ownership, and phase-bound SHAs

- **Status:** `PATTERN`
- **Trigger:** 여러 ChatGPT/Codex/외부 Agent가 같은 Base 저장소를 동시에 다루는 상황에서 열린 PR #312가 visual/Figma/shared-tool 경로를 소유하고 있었다. 감사 중 검색 결과만으로 README의 ACTIVE Skill 표시가 생성 정본과 어긋났다는 가설도 세웠다.
- **Correction:** `INVALIDATED_FINDING`. `main@453f790821a108a1d4f6e1f4e45f6931c2396ee0`, 병합 후 `main@190511e3b7dcc368f45eb61348b23d2b5a93f3c2`, PR #312 HEAD를 exact-SHA readback한 결과 README는 모두 `docs/generated/BASE_ACTIVE_SKILLS.md`로 위임하고 있었고 별도 Skill 수·목록을 유지하지 않았다. 검색 snippet은 탐색 단서일 뿐 verified repository fact가 아니며, exact ref의 실제 파일을 읽기 전에는 finding으로 승격하면 안 된다.
- **Verified finding:** local/remote ahead·behind와 textual path overlap만으로는 안전한 write·PR·merge를 증명할 수 없다. 다른 파일이 같은 Canon·Schema·generated derivative·Scene·asset family를 변경할 수 있고, `current Task/PR` 자체를 same-goal duplicate로 오인하거나 첫 write parent와 최종 reviewed head를 같은 SHA 의미로 섞을 수도 있다.
- **Decision:** 새 ACTIVE Skill이나 lock service를 만들지 않고 기존 `synchronizing-local-and-github-state`에 cooperative `CONCURRENT_CHANGE_PREFLIGHT`를 흡수한다. `current_task_or_pr_identity`, `source_main_sha`, `current_main_sha`, `write_parent_sha`, `expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>`, intended paths, semantic resource locks, same-goal PRs와 changed paths를 함께 판정한다. 증거가 없으면 `BLOCKED_UNVERIFIED`, main 이동은 `STALE_BASE_SHA`, 다른 writer는 `WAITING_RESOURCE`, 동일 Goal은 `DUPLICATE_WORK`로 fail closed한다.
- **Coordination evidence:** PR #312와 PR #313의 changed-path 교집합은 0이었다. 잘못된 README 가설에 근거해 남긴 조정 요청은 후속 정정 comment로 철회하며, PR #312에 추가 수정 책임을 부과하지 않는다. comment 자체는 resource release가 아니고, 동시작업 안전성은 exact changed paths와 semantic ownership으로 판정한다.
- **TDD evidence:** initial RED `acb59559701f90ceb835a8a271c630058b863696`에서 preflight/first-write 계약 누락만 2건 재현했고, adversarial RED `dc120e173922d97b610c115f82ba683d9c32157d`에서 current-PR self-conflict와 write-phase SHA 누락만 2건 재현했다. 첫 통합 후보 `617778650deb644e0b549fc675ed942c786a6389`는 Base v9 focused suite 327개를 통과했으나 canonical-reference freshness가 이 Skill 변경의 기존 통합 test companion과 Learning Log 누락을 정확히 차단했다. 병합 후 exact-SHA readback은 별도 정정 회귀를 추가해 검색 단서의 과승격도 차단했다.
- **Boundary:** 이 계약은 GitHub가 강제하는 mutex·ruleset·merge queue 설정 증거가 아니다. semantic resource 명명 품질에 따라 false positive/negative가 생길 수 있다. 이 connector-only 실행은 로컬 full validation, `git fsck`, Godot runtime/render를 실행했다고 주장하지 않는다.
- **Next trigger:** 실제 parallel-work 충돌 또는 불필요한 대기 사례가 누적될 때, semantic resource naming fixture나 machine-enforced lease가 필요한지 별도 Existing Solution First 검토를 수행한다.

## 2026-08-20 — Open PR state is not execution-surface owner evidence

- **Status:** `PATTERN`
- An open/draft/ready PR is backlog metadata, not proof of another active worker.
- Protect mutation only when current owner evidence exists; otherwise a user-confirmed single coordinator may revalidate and take over stale backlog on latest main.
- Connector-only execution must still use `GITHUB_CONNECTOR_ONLY` / `NOT_APPLICABLE_CONNECTOR_ONLY` and never invent local evidence.
