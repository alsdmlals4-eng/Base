# Base Partition 독립 최적화 — GPT 작업지시문

당신은 Base 전체가 아니라 제공된 **하나의 Partition**만 책임진다.

## 0. 시작 입력

```text
PART_ID: {{PART_ID}}
PART_NAME: {{PART_NAME}}
MANIFEST: docs/operations/BASE_PARTITION_MANIFEST.json
CONTEXT_PACK: {{CONTEXT_PACK}}
```

작업 시작 시 최신 `main`, `AGENTS.md`, Manifest, 해당 Context Pack, 실제 Skill/파일/Test, 같은 Goal의 열린·최근 병합 PR을 다시 읽는다. 전달받은 과거 SHA를 최신 상태처럼 가정하지 않는다.

## 1. 실행 주체

GPT가 기본 작업자다. 현행조사·기획·벤치마킹·최소 3개 대안·규칙/Skill/Module 검토·Notion/GitHub 대조·검수·적대적 검토를 GPT에서 닫는다.

`OPTIONAL_CODEX_EXECUTOR`는 code/Scene/Resource/data의 실제 filesystem 변경, 대규모 기계 점검, 로컬 Godot/runtime test처럼 실행 권위가 실제로 필요할 때만 사용한다. GPT 단계가 끝났다는 이유만으로 Codex를 호출하지 않는다.

Codex가 필요하면 PowerShell에서 가능한 한 한 번에 붙여넣을 launcher + 전체 실행 packet을 제공하고, Codex가 GitHub·Notion·프로젝트 실제 파일을 다시 읽게 한다.

## 2. 쓰기 경계

Manifest의 해당 Part `owned_write_paths`와 `allowed_new_paths`만 직접 쓴다. `control_plane.protected_write_paths`, 다른 Part 경로, 다른 채팅의 branch/worktree/PR은 수정하지 않는다.

필요하면 직접 고치지 말고:

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: {{PART_ID}}
  target_owner: CP0 | Pxx
  target_paths: []
  reason:
  evidence:
  required_semantic_change:
  acceptance_criteria: []
  blocking: true | false
```

를 남긴다.

작업 전/후:

```powershell
python tools/check_base_partition_scope.py --part {{PART_ID}} --base <BASELINE_SHA> --head HEAD
```

를 실행한다. `CONTROL_PLANE_WRITE_FORBIDDEN`, `OUT_OF_PARTITION_WRITE`가 하나라도 있으면 Part PR은 merge-ready가 아니다.

## 3. 현행 구조 복원

파일 목록이 아니라 다음 질문에 답한다.

- 이 Part는 Base 전체에서 무엇을 책임지는가?
- 중요한 규칙은 어디가 canonical source인가?
- 각 Skill/Mode는 언제 호출되고 입력/출력이 무엇인가?
- Module은 어떤 public responsibility를 가지는가?
- 어떤 consumer/Test가 결과를 사용하거나 검증하는가?
- 없애면 무엇이 깨지는가?

## 4. 중요 규칙 검토

중복·충돌·상하위 권한 역전·consumer 없는 규칙·Test 없는 핵심 규칙·다른 Part 침범·복제 drift를 찾는다.

## 5. Skill/Mode 검토

각 Skill을 `KEEP / IMPROVE / MERGE / ABSORB / SPLIT / RECLASSIFY / DEPRECATE / ARCHIVE / BLOCKED_UNVERIFIED` 중 하나로 판정한다. 새 Skill은 최후 수단이다. Guide/Module이면 충분한 기능을 Skill로 유지하지 않는다.

## 6. Module 검토

응집도, 결합도, interface, canonical owner, 재사용, 교체 가능성, 독립 검증 가능성을 본다. 기본 대안은 `현행 유지 / 최소 정리 / 책임 경계 재구성`이며 더 강한 대안을 계속 탐색한다.

## 7. 대안·벤치마킹

L1 이상 중요 결정은 `MINIMUM_VIABLE_ALTERNATIVES: 3`의 materially distinct 대안을 확보한다. 현행 유지도 유효 후보가 될 수 있다. 현업/1차 자료와 성공·실패 사례를 현재 결정에 필요한 만큼 조사하고 `ADOPT / ADAPT / REJECT`한다.

최초 권장안 뒤 `BETTER_ALTERNATIVE_SEARCH`, 최종 선택 전 `LONG_TERM_PLAN_FIT_REQUIRED`와 `revisit_conditions`를 기록한다.

## 8. UX/UI/Visual/PoC 관련 Part

시각 요소가 플레이 판단에 실질 영향을 주면:

```text
GPT 기획 → UX/UI flow → Visual Requirement
→ 이미지 생성/선택 → 정확한 Project Notion 배치 + readback
→ 승인 → 승인 visual을 구현 입력으로 사용
→ PoC/demo → runtime UX/play test
```

순수 로직 PoC는 `VISUAL_NOT_MATERIAL_TO_THIS_POC`로 생략 가능하다.

## 9. Legacy

Figma, Google Sheets, external HTML workspace, 폐기 custom local Tool/Hub를 신규 기본 surface로 부활시키지 않는다. 발견 시 한 번만 `UNIQUE / DUPLICATE / OBSOLETE`로 분류한다. UNIQUE는 현행 Notion/repository owner로 흡수·readback 후 원본 consumer 0에서 제거한다.

## 9A. 작업마다 교훈·학습

모든 완료 작업은 Manifest의 해당 Part `learning_log`에 Learning Checkpoint 하나를 추가한다. 최소 필드는 `work_ref`, 결과, worked/failed, `reusable_lesson`, anti-pattern, 영향을 받은 규칙·Skill·Module, evidence, reuse scope, source follow-up, revisit condition이다.

새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`을 기록한다. 단지 형식을 채우기 위해 가짜 교훈·새 규칙·새 Skill을 만들지 않는다. 프로젝트 고유 교훈은 `PROJECT_ONLY`, Part 내부만 유효하면 `PART_ONLY`, 여러 프로젝트/Part에 재사용 가치와 evidence가 있으면 `BASE_PROMOTION_CANDIDATE`다. Base 승격은 이 Part가 직접 CP0를 수정하지 않고 `CROSS_PART_CHANGE_REQUEST`/Integration으로 넘긴다.

### 주기 Source Learning

전역 `Periodic Source Scan Queue`와 Manifest의 `source_discovery`를 사용한다. 기존 Source의 새/변경 자료를 확인하고, 각 작업의 실패·빈 coverage·재검토 조건에서 **추가 관련 사이트/Source 검색 질문**을 만든다. 발견 자료는 원출처·날짜·범위·반례·commercial interest·consumer·validation을 확인하기 전 `UNVERIFIED_DISCOVERY`다. Source 수 자체를 목표로 하지 않는다.

## 10. 비용

기본 유료 플랜은 `GPT_PRO` 하나다. Notion paid 기능은 실제 blocker와 무료 대안 비교 뒤 사용자 승인 전에는 도입하지 않는다.

## 11. 적대적 검토

```text
FULL_LOOP_COUNT_MINIMUM: 5
MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5
```

각 회차는 전체 Part를 다시 `ATTACK → VALIDATE → FIX → VERIFY → BETTER_ALTERNATIVE_SEARCH → LONG_TERM_PLAN_FIT_RECHECK → RE-ATTACK`한다.

1~5회는 의무 full-scope loop다. 5회 전에는 finding 0이어도 종료하지 않는다. 5회 이후 유효 오류·충돌·누락·blocking finding/회귀/acceptance failure가 하나라도 있으면 6..N회로 계속한다. 최대 횟수는 없다. 가짜 finding이나 불필요한 변경을 만들지 않는다.

최소 5회 완료 후 post-minimum 전체 재공격이 blocker 0, 회귀 0, acceptance/정본/증거 조건 충족일 때만 `CLEAN_REVIEW_EXIT`다.

## 12. PR

자기 Part branch/PR만 만든다. 다른 Part PR을 merge/rebase/close/수정하지 않는다. PR에는 `PART_ID`, `BASELINE_SHA`, `OWNED_WRITE_PATHS`, `ACTUAL_CHANGED_PATHS`, `CROSS_PART_CHANGE_REQUESTS`, tests, loop evidence, long-term fit, revisit conditions, NOT_RUN, rollback을 기록한다.

## 13. 사용자 학습형 완료보고

단순 `완료/테스트 통과`로 끝내지 않는다.

1. **이 Part는 무엇인가**
2. **가장 중요한 규칙 3~10개** — 무엇을 보장하고 언제 작동하는가
3. **핵심 Skill/Mode** — 호출 조건·책임 차이
4. **핵심 Module** — 입력→처리→출력→consumer/검증
5. **잘 유지한 것 / 개선한 것 / 흡수·통합 / 제거·Archive / 의도적으로 추가하지 않은 것**
6. **BEFORE → AFTER → 사용자/플레이어 효과 → trade-off**
7. **장기 적합성 / 재검토 조건**
8. **실제 검증 / NOT_RUN / BLOCKED_UNVERIFIED / 남은 위험**
9. **프로젝트/Part 고유 교훈 vs Base 전체 승격 후보**

이 보고와 Part scope PASS, `CLEAN_REVIEW_EXIT`까지 완료해야 Part 완료다.
