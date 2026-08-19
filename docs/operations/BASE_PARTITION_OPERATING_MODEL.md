# Base Partition Operating Model v1

## 목적

Base 전체를 여러 GPT 채팅이 동시에 깊게 최적화하더라도 **정본·Skill·Module·Test·PR 소유권이 충돌하지 않도록** 책임 경계를 고정한다. 이 문서는 사람이 읽는 설계 설명이고, 기계 경계는 `docs/operations/BASE_PARTITION_MANIFEST.json`이 소유한다.

설계 기준 main: `f93016dbe90d3d1d906afaaaa75005b490220e90`. 실제 Part 시작 시에는 이 SHA를 그대로 재사용하지 않고 최신 `main`을 다시 읽어 exact baseline으로 pin한다.

## 현행 상태 요약

- `skills/SKILL_REGISTRY.json`이 active Skill routing의 유일한 권위이고 현재 active Skill은 30개다.
- `docs/generated/BASE_ACTIVE_SKILLS.md` 같은 generated map은 Registry 파생물이며 직접 편집 대상이 아니다.
- `docs`, `skills`, `tools`, `schemas`, `templates`, `tests`, `.github`가 기능별로 교차 연결된다.
- 하나의 기능 변경이 Skill 본체뿐 아니라 Guide·Template·Test·reference freshness·generated view까지 건드릴 수 있다.
- Base는 프로젝트 운영, 게임기획, 시각/UX, Godot/runtime, release/platform, AI executor, 서사/콘텐츠까지 포함한다.
- 기존 `.github/CODEOWNERS`는 단일 사용자 소유권을 표현하지만 여러 GPT 채팅의 논리적 Part 소유권까지 구분하지는 않는다.

## 분할 대안 Trade Study

| 대안 | 구조 | 장점 | 치명적 약점 | 판정 |
|---|---|---|---|---|
| **A · 디렉터리 계층 분할** | docs / skills / tools / tests | 매우 단순 | 하나의 기능이 여러 계층을 동시에 바꿔 cross-part 요청과 충돌이 폭증 | REJECT |
| **B · 기능/도메인 분할** | 기획 / 아트 / Godot / AI 등 | 응집도가 높음 | Registry·AGENTS·Documentation Map·generated artifacts 같은 공용 파일에서 경쟁 수정 발생 | ADAPT |
| **C · Control Plane + End-to-End Capability Partition** | 공용 권위는 CP0 잠금, 기능은 rule→skill→guide/tool→test 단위 Part | 독립성·장기 안정성·사용자 학습성·rollback이 가장 균형적 | 마지막 Integration 단계가 필요 | **ADOPT** |
| **D · 동적 의존성 그래프 재클러스터링** | 변경 그래프에 따라 Part 자동 재편 | 이론상 결합도 최소화 가능 | Part ID/소유권이 자주 바뀌어 1인 운영과 학습 비용 증가, 재현성 저하 | DEFER |

### BETTER_ALTERNATIVE_SEARCH

C 선택 뒤에도 D를 재검토했다. 현재 Base에서는 안정된 Part 이름과 반복 학습 가치가 자동 최적 클러스터보다 중요하다. 자동 클러스터링은 분석 보조 지표로는 유용하지만 **쓰기 권한을 매번 재편하는 권위**로 쓰지 않는다.

### LONG_TERM_PLAN_FIT_REQUIRED

C는 Base가 커져도 CP0와 Part ID를 유지하면서 Part 내부만 분리·병합할 수 있다. 사용자는 “어디에 어떤 규칙/Skill/Module이 있는지”를 누적 학습할 수 있고, 각 PR은 Part 단위로 rollback 가능하다. 단, cross-part request가 지속적으로 많아지면 경계가 틀린 것이므로 재분할한다.

## 외부 실무 벤치마크

- Git 공식 `git-worktree` 문서는 하나의 저장소에 여러 linked worktree를 두고 서로 다른 branch를 동시에 checkout할 수 있음을 명시한다. 따라서 Part별 branch/worktree 격리는 Git 자체 모델과 맞는다.
- GitHub CODEOWNERS는 경로 책임자를 지정하고 review routing에 사용할 수 있다. 현재 Base는 실제 사람 owner가 하나이므로, 채팅별 논리 소유권은 별도 Manifest가 담당한다.
- GitHub required status checks/rulesets는 merge 전에 CI 통과를 강제할 수 있다. 따라서 Part scope checker와 partition contract CI는 최종 merge gate의 기계 증거로 사용한다.

공식 참고:
- https://git-scm.com/docs/git-worktree
- https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets

## CP0 · Base Control Plane

일반 Part worker는 CP0를 **읽을 수 있지만 쓰지 않는다.**

대표 CP0:

- `AGENTS.md`, `README.md`, `START_HERE.md`
- `docs/OPERATING_MODEL.md`
- `docs/WORK_MODE_AND_SKILL_ROUTING.md`
- `docs/DOCUMENTATION_MAP.md`
- `docs/LONG_HORIZON_WORK_EXECUTION_POLICY.md`
- Partition Operating Model / Manifest / Context Packs / 공통 Prompt
- `skills/SKILL_REGISTRY.json`, shared routes, central behavior/coverage/evidence contracts
- `docs/generated/**`
- `.github/**`
- Base v9 global schema/integrity/generation surface

Part에서 CP0 수정 필요성을 발견하면 직접 고치지 않고 다음을 남긴다.

```yaml
CROSS_PART_CHANGE_REQUEST:
  from_part: Pxx
  target_owner: CP0 | Pyy
  target_paths: []
  reason:
  evidence:
  required_semantic_change:
  acceptance_criteria: []
  blocking: true | false
```

Integration GPT가 모든 요청을 모아 중복·충돌을 판정한 뒤 canonical owner를 한 번만 수정한다.

## 9개 Part

| Part | 책임 | 대표 Skill | 주 연결 |
|---|---|---|---|
| P01 | Project Planning, Operations & Notion | intake, project OS, docs, handoff, continuity, learning | P02/P03 |
| P02 | Skill Governance, Canon Freshness & Legacy | discipline, freshness, BCP, simplify, prune, legacy | 모든 Part |
| P03 | Adversarial Quality, Refactoring & Git Integrity | adversarial, refactor, git sync | P02/P07 |
| P04 | Game Design, Core, Player Research & Vertical Slice | concept, core, vertical slice, user research | P05/P06/P07 |
| P05 | Art, UX/UI & Visual Assets | art prompt, UI audit, visual dashboard | P01/P04/P06 |
| P06 | Godot, Runtime & Technical Toolchain | runtime diagnosis, addon/plugin evaluation | P04/P05/P07 |
| P07 | Platform, Release & Execution Validation | reviewing/validating changes | P03/P06 |
| P08 | AI Operations & External Executors | DeepSeek worktree, AI model/cost | P01/P03/P07 |
| P09 | Content, Narrative & Publication | YouTube, serial fiction | P04/P05/P07 |

각 Part의 세부 write scope·read-only dependency·검증·재검토 조건은 Manifest와 Context Pack이 정본이다.

## 병렬 실행

세 그룹은 **서로 다른 선행 merge를 기다리지 않고 같은 exact baseline에서 시작할 수 있다.** 그룹은 사용자가 관리하기 쉬운 시각적 묶음일 뿐 직렬 dependency가 아니다.

```text
G1 FOUNDATION        P01 P02 P03
G2 GAME PRODUCTION   P04 P05 P06
G3 DELIVERY/AI/CONTENT P07 P08 P09
                     ↓
                 Integration
                     ↓
                    CP0
```

각 Part는 자기 branch/PR만 소유한다. 다른 Part 결과가 필요하면 그 Part의 미병합 branch를 읽어 결합하지 않고 `CROSS_PART_CHANGE_REQUEST`로 넘긴다.

## 파일 상태 모델

- `PART_OWNED`: 해당 Part가 직접 수정할 수 있는 경로.
- `READ_ONLY_DEPENDENCY`: 판단에 필요하지만 직접 수정하지 않는 자료.
- `CONTROL_PLANE`: Integration만 쓴다.
- `DERIVED_OR_GENERATED`: 원본 수정 후 생성기로 재생성한다. 직접 hand-edit 금지.

Manifest에 명시되지 않은 경로는 자동 자유영역이 아니다. 기본 `READ_ONLY`이며 Integration이 owner를 지정하거나 Part가 cross-part request를 제출한다.

## Scope Checker

Part 구현 branch에서는 최소 다음을 실행한다.

```powershell
python tools/check_base_partition_scope.py --part P04 --base <BASELINE_SHA> --head HEAD
```

판정:

- `CONTROL_PLANE_WRITE_FORBIDDEN`: 일반 Part가 CP0를 수정함.
- `OUT_OF_PARTITION_WRITE`: 자기 owned/allowed-new scope 밖을 수정함.
- `PASS`: 현재 changed paths가 모두 허용 범위.

Integration은 `--integration`으로 모든 changed path를 분류해 Part boundary 위반과 CP0 변경을 감사한다.

## GPT / Codex 실행 구조

GPT가 기본 작업자다. Part별로 현행 조사·최소 3개 대안·벤치마킹·기획·검수·Notion/GitHub 대조·적대적 검토를 닫는다. Codex는 code/Scene/Resource/data 수정, 대규모 기계 변경, 로컬 runtime test 등 실행 권위가 실제로 필요할 때만 `OPTIONAL_CODEX_EXECUTOR`로 호출한다.

Codex가 필요하면 해당 Part의 manifest/context pack, exact baseline, protected paths, acceptance criteria와 필요한 repository/Notion readback을 하나의 실행 packet으로 넘긴다.

## Visualized PoC

UI/UX/가독성/첫인상/아트 맥락이 PoC 판단에 중요하면:

```text
GPT 기획 → UX/UI flow → visual requirement → 이미지 생성/선택
→ 정확한 Project Notion 배치 + readback → 승인
→ 승인 visual을 구현 입력으로 사용 → PoC/demo → runtime UX/play test
```

순수 로직 가설에는 완성 visual을 강제하지 않는다.

## Legacy Retirement Map

| 폐기 surface | 1차 owner | 흡수 destination | 완료 조건 |
|---|---|---|---|
| Google Sheets | P02 | P01/P04/P05 + repository | UNIQUE 이관/readback + consumer 0 |
| Figma 참조/flow | P05 | Notion/P05 | 고유 원리/증거만 흡수 + active authority 0 |
| external HTML workspace | P05 | Notion | unique human-view 기능 흡수 + route 0 |
| custom local visual Tool/Hub | P05 | P05/P06 | unique capability audit 후 흡수/삭제 |
| QA Evidence Studio/local QA | P06 | P07/repository evidence | 대체 불가 unique 검증기능만 유지, 나머지 retire |

삭제는 “오래됨”만으로 결정하지 않는다. `UNIQUE / DUPLICATE / OBSOLETE`를 한 번 분류하고 UNIQUE의 destination readback이 먼저다.

## Part 완료 계약

각 Part는 `FULL_LOOP_COUNT_MINIMUM: 5`, `MINIMUM_FULL_LOOPS_BEFORE_CLEAN_EXIT: 5`를 적용한다. 최소 5회의 완전한 전체 적대적 개선 루프 후에도 유효 오류·충돌·누락·blocker가 있으면 6..N회를 계속한다. `CLEAN_REVIEW_EXIT` 전에는 완료가 아니다.

완료 보고는 사용자 학습형으로 다음을 먼저 설명한다.

1. 이 Part가 무엇을 하는가
2. 중요한 규칙 3~10개와 작동 시점
3. 핵심 Skill/Mode와 책임 차이
4. 핵심 Module의 입력→처리→출력→검증
5. 유지/개선/흡수/삭제/의도적 비추가
6. BEFORE→AFTER→기대효과→trade-off
7. 장기 적합성·재검토 조건
8. 실행 증거·NOT_RUN·남은 위험

## Integration

P01..P09가 끝나면 별도 Integration GPT가 다음 순서를 수행한다.

1. latest main + Manifest version 확인
2. 각 PR의 `ACTUAL_CHANGED_PATHS`와 owned scope 비교
3. CROSS_PART_CHANGE_REQUEST 모음·중복 제거
4. CP0를 한 번만 수정
5. Registry/Documentation Map/generated map 동기화
6. legacy retirement 요청 처리
7. Notion `Base · 작업 시스템 & Skill 지도` 갱신
8. 전체 Base 회귀검증
9. 최소 5회 전체 적대적 개선 + 이후 clean까지 반복
10. exact-head merge
11. post-merge main/Notion readback

## Rollback

- Part PR은 Part 경계 단위로 독립 revert 가능하다.
- Integration 문제는 Integration commit/PR을 revert하고 Part PR의 증거는 유지한다.
- 다른 채팅/독립 workstream은 rollback에 포함하지 않는다.
- destructive legacy deletion은 흡수 destination과 Git history 복구 경로를 먼저 확인한다.

## 재검토 조건

다음이면 Partition 자체를 다시 Trade Study한다.

- active Skill > 40
- Part당 cross-part request 중앙값 > 3
- 한 Part가 반복적으로 GPT practical context를 초과
- 동일 semantic owner를 두 Part가 반복적으로 요구
- 새 major engine/product domain 추가
- Notion/GitHub authority model 변경
- 동적 dependency clustering이 **안정된 Part ID를 유지하면서** 충돌을 실질적으로 더 줄일 수 있게 됨
