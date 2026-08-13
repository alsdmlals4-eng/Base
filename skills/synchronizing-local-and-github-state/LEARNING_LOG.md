# Synchronizing Local and GitHub State — Learning Log

## 2026-08-13 — Concurrent work needs identity, semantic ownership, and phase-bound SHAs

- **Status:** `PATTERN`
- **Trigger:** 여러 ChatGPT/Codex/외부 Agent가 같은 Base 저장소를 동시에 다루는 상황에서 열린 PR #312가 `README.md` 등을 소유하고 있었고, 별도 감사 작업에서도 같은 stale consumer를 발견했다.
- **Finding:** local/remote ahead·behind와 textual path overlap만으로는 안전한 write·PR·merge를 증명할 수 없다. 다른 파일이 같은 Canon·Schema·generated derivative·Scene·asset family를 변경할 수 있고, `current Task/PR` 자체를 same-goal duplicate로 오인하거나 첫 write parent와 최종 reviewed head를 같은 SHA 의미로 섞을 수도 있다.
- **Decision:** 새 ACTIVE Skill이나 lock service를 만들지 않고 기존 `synchronizing-local-and-github-state`에 cooperative `CONCURRENT_CHANGE_PREFLIGHT`를 흡수한다. `current_task_or_pr_identity`, `source_main_sha`, `current_main_sha`, `write_parent_sha`, `expected_head_sha: PENDING_FIRST_WRITE | <exact-sha>`, intended paths, semantic resource locks, same-goal PRs와 changed paths를 함께 판정한다. 증거가 없으면 `BLOCKED_UNVERIFIED`, main 이동은 `STALE_BASE_SHA`, 다른 writer는 `WAITING_RESOURCE`, 동일 Goal은 `DUPLICATE_WORK`로 fail closed한다.
- **Coordination evidence:** PR #312의 changed paths를 보호하고 README의 `27` 대 Registry-derived `30` drift는 해당 소유 PR comment로 전달했다. comment 자체는 resource release가 아니며 이 변경은 비중첩 경로만 사용한다.
- **TDD evidence:** initial RED `acb59559701f90ceb835a8a271c630058b863696`에서 preflight/first-write 계약 누락만 2건 재현했고, adversarial RED `dc120e173922d97b610c115f82ba683d9c32157d`에서 current-PR self-conflict와 write-phase SHA 누락만 2건 재현했다. 첫 통합 후보 `617778650deb644e0b549fc675ed942c786a6389`는 Base v9 focused suite 327개를 통과했으나 canonical-reference freshness가 이 Skill 변경의 기존 통합 test companion과 Learning Log 누락을 정확히 차단했다.
- **Boundary:** 이 계약은 GitHub가 강제하는 mutex·ruleset·merge queue 설정 증거가 아니다. semantic resource 명명 품질에 따라 false positive/negative가 생길 수 있다. 이 connector-only 실행은 로컬 full validation, `git fsck`, Godot runtime/render를 실행했다고 주장하지 않는다.
- **Next trigger:** 실제 parallel-work 충돌 또는 불필요한 대기 사례가 누적될 때, semantic resource naming fixture나 machine-enforced lease가 필요한지 별도 Existing Solution First 검토를 수행한다.
