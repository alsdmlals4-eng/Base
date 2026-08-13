# Synchronizing Local and GitHub State — Learning Log

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
