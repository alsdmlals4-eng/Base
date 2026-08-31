# 프로젝트 작업 규율 및 Base 제안서 교정 실행 계획

## 승인 범위와 기준점

- 사용자 승인: 2026-08-31. 프로젝트 작업 시작 전 fresh-read, 장르·세계관·시각 기준과 벤치마킹, 효율적인 Blueprint 형식, 필요 시 Godot 직접 실행, 안전한 GitHub fetch/pull/push/PR, 용량·경로 규율, 실제 구현·증거 우선, machine-primary 및 사용자 선언 시 1회 human validation을 기존 Base owner에 교정한다.
- 추가 승인: Blueprint는 새 산출물 의무가 아니라 기존 사례에서 검증된 정보 구조를 재사용하여 더 짧고 추적 가능한 형식으로 개선한다. `[수정제안서]`와 후보보고서는 공통 교훈과 최소 수정 요청을 명시한다.
- fresh-read 기준: `origin/main` = `1f0ef9d8bdb1869c9ba25b33efdcb34cf2ccba83`.
- 작업 브랜치: `codex/project-work-discipline-correction-20260831`.
- 격리: 현재 checkout의 독립 브랜치를 사용한다. 별도 worktree를 새로 만들지 않으며, 사용자 소유의 untracked `Base-worktrees/` 및 그 하위 worktree는 읽기·이동·삭제·추적 대상에서 제외한다.

## 소유 문서와 최소 변경

1. `templates/project-operations/WORK_PROJECT_START_CANON_CHECKLIST.md`
   - fresh-read receipt에 장르·세계관·시각/구도 anchor 및 benchmark `ADOPT / ADAPT / REJECT` 근거를 추가한다.
2. `templates/project-operations/WORK_FIVE_PHASE_VERTICAL_SLICE_EXECUTION_CONTRACT.md`
   - 복잡한 시스템일 때만 기존 System Blueprint를 reuse/adapt하고, machine-primary 및 프로젝트 선언 후 한 번의 final user review 경계를 명확히 한다.
3. `templates/project-operations/WORK_CODEX_MINIMUM_TRANSITION_STARTER_PROMPT.md`
   - GitHub safe fetch/pull/push/PR, callable Godot direct launch, 기존 경로 안의 task-owned temporary cleanup, actual implementation/evidence gate를 한 작업 수신 계약으로 보강한다.
4. `docs/operations/project-workspace/NOTION_SYSTEM_BLUEPRINT_CONTRACT.md`
   - 기존 Node ID 형식을 유지하면서 player intent → decision → state → feedback → owner/validation을 하나의 압축된 결정 사슬로 재사용하는 Blueprint 효율성 기준을 추가한다.
5. `skills/managing-base-change-proposals/SKILL.md`와 `templates/BASE_CHANGE_PROPOSAL.md`
   - 후보보고서/수정제안서에 공통성, 실제 관찰, 재사용 가능한 교훈, 기존 owner의 gap, 최소 교정 요청, 반례, evidence ceiling, 검증·롤백을 분리하도록 보강한다.

## 검증 순서

1. 대상 계약 테스트에 새 토큰·경계 요구를 먼저 추가하고, source 수정 전 실패를 확인한다.
2. 위 기존 owner만 수정하고 targeted unittest 및 proposal checker를 실행한다.
3. changed-file diff, Git status, Base-worktrees 비침범, main baseline/branch ancestry를 readback한다.
4. `reviewing-and-validating-project-changes` 기준으로 기계 검증과 human/runtime evidence ceiling을 확인하고, 다섯 차례 adversarial self-review에서 각 차례 새 문제를 수정하거나 clean 근거를 남긴다.
5. 검증된 변경만 commit → push → PR로 제출한다. `main` 직접 push, force push, ruleset bypass는 하지 않는다.

## 비목표와 롤백

- 첨부 PDF의 프로젝트 고유 설정·이미지·결론을 Base canon으로 승격하지 않는다.
- 모든 프로젝트에 Blueprint 또는 human study를 강제하지 않는다.
- 고아 worktree, untracked artifact, 프로젝트 자료를 이번 작업에서 정리·삭제하지 않는다.
- 롤백은 이 브랜치의 문서·테스트 커밋만 되돌리는 것이며 프로젝트 runtime이나 Base main은 변경하지 않는다.
