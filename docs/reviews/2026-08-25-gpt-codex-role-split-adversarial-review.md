# GPT–Codex 역할 분리 · 적대적 검토 기록 — 2026-08-25

> **STATUS: SUPERSEDED_BY_GODOT_PRODUCT_SCOPE_CORRECTION**
>
> 이 문서는 같은 날의 중간 역할 설계를 검토한 역사 기록이다. 당시 `Codex = generic implementation executor`로 범위를 넓힌 결론은 이후 사용자 교정으로 폐기됐다. 현재 정본은 `docs/GPT_CODEX_WORKFLOW_POLICY.md`다.

## 현재 교정 결론

```text
GPT_NONCODING_PROJECT_OWNER
GPT_BASE_NOTION_GOVERNANCE_OWNER
CODEX_GODOT_PRODUCT_IMPLEMENTATION_OWNER
CODEX_NOT_GENERAL_REPOSITORY_EXECUTOR
```

현재 의미:

- GPT: 기획·조사·벤치마킹·적대적 검수·Base·Notion·문서·표·이미지·Godot Work Instruction·최종 검수
- Codex: 실제 게임 프로젝트의 GDScript·Scene·Resource·runtime wiring·build/export·implementation/runtime/play test
- Base Python test·Registry/generated·CI contract는 GPT 작업
- Codex는 이미지 생성·생성형 편집 금지
- 실제 Godot 구현 전에 해당 프로젝트 GitHub + Notion 재수화

## 역사적 검토에서 유지하는 유효 Finding

중간 설계의 최종 owner 결론은 폐기됐지만 다음 비퇴행 finding은 계속 유효하다.

1. **Role ownership은 명시적이어야 한다.** GPT와 Codex가 같은 persistent product implementation owner가 되면 충돌한다.
2. **GitHub + Notion rehydration이 필요하다.** stale handoff만으로 actual project implementation을 시작하면 안 된다.
3. **Visual boundary가 필요하다.** Codex는 current-use 승인 + Notion upload/attach/readback된 Visual만 소비한다.
4. **wrong-target/session/freshness 안전성은 유지한다.** stale PID/session, 잘못된 worktree, dirty/diverged, destructive Git을 fail-closed로 본다.
5. **중립적 적대검토 의미를 보존한다.** 동의 편향을 막되 반대를 위한 반대를 하지 않는다.
6. **schema/compatibility unrelated delta를 역할 변경과 섞지 않는다.** Workspace schema v3 compatibility를 유지한다.
7. **consumer inventory 후 교정한다.** `PRESERVE_SEMANTIC / MIGRATE_OWNER / STALE_EXPECTATION / HISTORICAL_SNAPSHOT`으로 분류한다.

## 폐기된 중간 결론

다음은 current authority가 아니다.

```text
CODEX_IMPLEMENTATION_EXECUTOR                  # generic repository owner 의미
IMPLEMENTATION_REQUIRES_CODEX_HANDOFF          # 모든 implementation 의미
Base tests / Registry / generated → Codex
Base CI / checker → Codex
모든 code/data mutation → Codex
```

파일이 코드인지가 아니라 **실제 게임 프로젝트의 Godot 제품 runtime 구현인지**가 Codex 진입 기준이다.

## 현재 #674 판정

PR #674는 Base governance workstream이므로:

```text
execution_owner: GPT_BASE_NOTION_GOVERNANCE_OWNER
codex_handoff: NOT_APPLICABLE
```

#674의 Base 문서·Skill·test·Registry/generated·CI validation까지 GPT가 끝까지 교정·검증한다.

## 작업지시문 revision

프로젝트 공용 작업지시문 새 revision은 사용자 지시에 따라 별도 후속 작업으로 계속 보류한다.

## Evidence ceiling

이 기록은 역할 migration의 설계/검토 evidence다. 실제 게임 프로젝트의 Godot runtime PASS를 주장하지 않는다.
