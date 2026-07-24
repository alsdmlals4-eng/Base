# Godot 구현 패키지 계약

## 1. 패키지 상태

```yaml
package_id:
package_title:
status: DRAFT | READY_FOR_CODEX_PLAN | PLAN_REVIEWED | READY_FOR_BUILD | IN_PROGRESS | PACKAGE_APPROVED | PACKAGE_APPROVED_WITH_TECHNICAL_CHANGES | USER_REVIEW_REQUIRED | CHANGE_PROPOSAL | REVISE | BLOCKED | UNVERIFIED
parent_issue:
branch:
pr:
baseline_commit:
master_plan:
updated_at:
```

## 2. 결과

이번 패키지가 끝났을 때 플레이 가능하거나 독립 검증 가능한 결과를 한 문장으로 적는다.

## 3. 플레이어 가치

## 4. 선행 조건

## 5. 포함 범위

## 6. 제외 범위

## 7. 수정 금지 범위

## 8. 허용 Godot 파일 범위

- GDScript:
- Scene:
- Resource:
- Autoload·프로젝트 설정:
- 런타임 데이터:
- 저장·마이그레이션:
- Godot 테스트:
- 셰이더·플러그인·빌드:

## 9. 비-Godot 변경 반환 계약

구현에 필요한 비-Godot 문서·Schema·Template·CI 변경은 직접 수정하지 않고 GPT에 다음 형식으로 반환한다.

```yaml
non_godot_change_request:
  path_or_responsibility:
  reason:
  blocking_scope:
  recommended_change:
  evidence:
```

## 10. 승인된 규칙과 데이터 계약

## 11. Codex Plan 입력

- 최신 `main`:
- 지정 Branch:
- 읽을 `AGENTS.md`·책임 원본:
- 관련 실제 파일:
- 테스트 명령:

## 12. Codex Plan 보고서

- 보고서 상태:
- 승인한 기술 개선:
- `CHANGE_PROPOSAL`:
- 사용자 결정:
- 남은 `UNVERIFIED`:

## 13. 작업 단위

| 작업 ID | 결과 | 수정 파일 | Red | Green | Refactor | 회귀 | Commit |
|---|---|---|---|---|---|---|---|

## 14. Codex Git 권한

```yaml
branch:
  create_or_switch: FORBIDDEN
  allowed_branch:
  push_target: ALLOWED_BRANCH_ONLY
commit:
  godot_runtime_files_only: true
  unrelated_changes: FORBIDDEN
  preserve_user_changes: true
  force_push: FORBIDDEN
  amend: FORBIDDEN
  independent_commits: REQUIRED
pull_request:
  create_or_update: FORBIDDEN
  merge: FORBIDDEN
```

## 15. Push 전 검사

- [ ] `git status`를 확인했다.
- [ ] 기준 Branch·Commit이 계약과 일치한다.
- [ ] 변경 파일 목록에 비-Godot 파일이 없다.
- [ ] 승인 범위 밖 변경이 없다.
- [ ] 사용자 기존 변경을 보존했다.
- [ ] 필수 Godot·정적·headless·런타임 테스트를 실행했다.
- [ ] 실패·미실행 검사를 명시했다.

## 16. Push 후 보고

```yaml
commit_sha:
remote_head:
changed_files: []
tests_run: []
tests_failed: []
tests_not_run: []
technical_changes: []
change_proposals: []
remaining_risks: []
rollback:
```

## 17. GPT 검수

- 승인 명세와 diff 대조:
- 기술 변경 판정:
- 데이터·저장 호환성:
- 테스트·회귀 증거:
- 사용자 체감 검수 필요:
- 최종 패키지 상태:

## 18. 사용자 승인

- 병합 승인:
- 승인 근거:
- 승인 시점:

## 19. 롤백

## 20. 다음 패키지 선행 조건
