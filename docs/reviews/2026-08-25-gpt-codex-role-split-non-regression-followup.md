# GPT–Codex 역할 분리 · Non-Regression Follow-up — 2026-08-25

> **STATUS: SUPERSEDED_BY_GODOT_PRODUCT_SCOPE_CORRECTION**
>
> 이 문서는 역할 분리 첫 설계에서 안전 capability를 복원한 역사적 follow-up이다. 당시의 `generic implementation → Codex` owner 결론은 폐기됐고, 현재 owner 경계는 `docs/GPT_CODEX_WORKFLOW_POLICY.md`가 소유한다.

## 현재 역할

```text
GPT = Base + Notion + planning + research + review + docs + tables + visuals + Godot work instruction + final review
Codex = actual game-project Godot product implementation/code/runtime-play tests
```

Codex는 일반 GitHub/코드 executor가 아니다.

## 이 follow-up에서 계속 보존할 비퇴행 capability

### Continuous work

- 승인된 같은 범위는 불필요한 재승인으로 멈추지 않는다.
- Base/Notion/noncoding finding은 GPT가 직접 교정한다.
- 실제 Godot product finding만 project-specific Codex handoff한다.
- executor가 없다고 다른 independent GPT task까지 멈추지 않는다.

### Project authoring / runtime safety

- HiGodot 등 채택된 persistent authoring authority를 임의 우회하지 않는다.
- stale PID/session을 current truth로 쓰지 않는다.
- wrong target/project/worktree 방지
- dirty/diverged 확인
- destructive reset/clean, force push, history rewrite 금지

이 runtime safety는 **실제 Godot 제품 구현을 수행하는 Codex**에게 적용된다. Base maintenance에 Codex를 강제하는 근거가 아니다.

### Preflight

고위험 Godot 구현에서 읽기 전용 technical preflight는 선택적으로 사용할 수 있다.

```text
CODEX_PREFLIGHT_OPTIONAL
PLAN_REVIEW_ONLY
file_write: FORBIDDEN
commit_push_pr_issue: FORBIDDEN
```

### Merge / post-merge

- exact remote HEAD
- required checks
- unresolved thread 0
- approved-scope merge authority
- post-merge main readback
- `PRE_MERGE_SNAPSHOT`과 `LIVE_CONTINUATION_STATE` 분리

### Adversarial non-regression

- 동의 편향 방지
- 반대를 위한 반대 금지
- 최소 5회 full-scope review 후 clean까지 반복
- 실제 owner가 구현한 finding을 review owner가 중복 구현하지 않음
- `NOT_RUN`을 PASS로 과장하지 않음

## 잘못된 중간 해석

다음은 이 follow-up 이후 사용자 교정으로 폐기됐다.

- Base machine consumer mutation → Codex
- Registry/generated/checker → Codex
- Base test/CI → Codex
- 모든 code/data/Scene/Resource/config/test/build/runtime → Codex

현재 기준은 **actual game-project Godot product runtime**이다.

## PR #674

#674는 Base governance workstream이므로 GPT가 끝까지 교정·test·Registry/generated·CI validation을 수행한다. Codex handoff는 `NOT_APPLICABLE`이다.

## 현재 검토 Gate

- current role source와 consumer 일치
- Base/Notion owner drift 0
- Godot-only Codex boundary 명확
- safety capability 비퇴행
- exact-head Base validation
- 최소 5회 whole-state adversarial clean exit

프로젝트 공용 작업지시문 새 revision은 별도 후속 작업으로 보류한다.
