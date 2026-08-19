from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
execution = manifest.setdefault("execution_model", {})
execution["open_pr_policy"] = "OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP"
execution["foreign_workstream_protection_basis"] = "ACTUAL_ACTIVE_OWNERSHIP_ONLY"
execution["single_chat_override"] = "CURRENT_CHAT_ONLY_WHEN_USER_CONFIRMS"
execution["cross_part_repair_conditions"] = [
    "Identify the semantic owner and affected consumers/tests before repair",
    "Protect a foreign workstream only when another user/chat/agent is actually active on it; an open/draft/ready PR alone is not active ownership",
    "The repair must serve the current authorized Base goal or regression closure",
    "Update owner-correct companions and record changed-path attribution",
    "Preserve exact-head verification and rollback",
]
manifest["collaboration_isolation"]["github"]["other_open_draft_ready_workstreams"] = "NOT_AUTOMATICALLY_ACTIVE_OWNERSHIP"
manifest["collaboration_isolation"]["github"]["actual_active_foreign_workstreams"] = "READ_ONLY_UNLESS_EXPLICIT_TRANSFER"
manifest["integration"]["ordered_steps"] = [
    step.replace(
        "no unrelated open/draft/ready workstream owns the target",
        "no actually active foreign workstream owns the target",
    )
    for step in manifest["integration"]["ordered_steps"]
]
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_all(path: Path, replacements: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new in replacements:
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")

agents_path = ROOT / "AGENTS.md"
agents = agents_path.read_text(encoding="utf-8")
if "OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP" not in agents:
    marker = "- **`SINGLE_COORDINATOR_CHAT_SEQUENTIAL_PARTS`:**"
    idx = agents.find(marker)
    if idx < 0:
        raise SystemExit("single coordinator marker missing")
    end = agents.find("\n", idx)
    extra = (
        "- **`OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP`:** open/draft/ready PR이나 남아 있는 branch만으로 다른 채팅·사용자·agent가 현재 작업 중이라고 추정하지 않는다. "
        "실제 활성 소유권은 최신 사용자 지시, 현재 실행 세션/작업자 정보, 명시적 handoff/lock처럼 검증 가능한 상태로 판정한다. "
        "사용자가 현재 활성 채팅이 하나뿐이라고 확인하면 그 coordinator는 미완료 열린 PR을 읽어 유효 변경을 흡수·수정·정리할 수 있다. 단, 실제 활성 외부 작업자가 확인되면 explicit ownership transfer 전에는 그 workstream을 read-only로 보호한다.\n"
    )
    agents = agents[: end + 1] + extra + agents[end + 1 :]
agents_path.write_text(agents, encoding="utf-8")

replace_all(
    ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md",
    [
        (
            "**별도 진행 중 workstream 보호는 계속 강제한다.** 다른 open/draft/ready PR·branch·worktree가 같은 경로나 의미를 소유하면 explicit ownership transfer 전에는 read-only다.",
            "`OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP`: 열린 PR/branch가 남아 있다는 사실만으로 실제 활성 workstream이라 판단하지 않는다. 최신 사용자 지시·실행 세션·명시적 handoff/lock 등으로 **실제 활성 소유권**이 확인된 외부 작업만 explicit ownership transfer 전까지 read-only다. 사용자가 현재 활성 채팅이 하나라고 확인하면 이 coordinator가 미완료 PR의 유효 변경을 흡수·수정·정리할 수 있다.",
        ),
        (
            "각 checkpoint는 최신 completed `main`, 진행 중 독립 PR, 정본/consumer/test를 다시 확인한다. cross-Part 수정이 필요하면 동일 coordinator가 owner-correct 변경으로 처리하되 active foreign workstream은 침범하지 않는다.",
            "각 checkpoint는 최신 completed `main`, 열린/최근 PR, 정본/consumer/test를 다시 확인한다. `OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP`에 따라 열린 PR은 변경 후보로 비교하고, **실제 활성** 외부 workstream만 보호한다. cross-Part 수정은 동일 coordinator가 owner-correct하게 처리한다.",
        ),
    ],
)

replace_all(
    ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md",
    [
        (
            "- **다른 open/draft/ready PR·branch·worktree가 같은 경로나 의미를 이미 소유하면 explicit ownership transfer 전에는 read-only다.** 그 active workstream 자체를 rebase/merge/close/rewrite하지 않는다.\n",
            "- `OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP`: open/draft/ready PR·branch가 존재한다는 사실만으로 **실제 활성** 다른 작업자가 있다고 추정하지 않는다. 최신 사용자 지시·실행 세션·handoff/lock으로 실제 활성 외부 소유권이 확인된 경우에만 explicit transfer 전 read-only다. 현재 coordinator만 활성이라고 확인되면 미완료 PR의 유효 변경을 흡수·수정·정리할 수 있다.\n",
        )
    ],
)

replace_all(
    ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md",
    [
        (
            "다른 open/draft/ready PR·branch·worktree는 explicit ownership transfer 전까지 read-only다.\n",
            "`OPEN_PR_IS_NOT_ACTIVE_OWNERSHIP`: 열린 PR/branch 자체는 active ownership 증거가 아니다. 최신 사용자 지시·실행 세션·handoff/lock으로 **실제 활성** 외부 workstream이 확인된 경우에만 explicit ownership transfer 전까지 read-only다. 현재 coordinator만 활성이라면 미완료 PR을 비교·흡수·수정·정리할 수 있다.\n",
        )
    ],
)

skill_path = ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md"
skill = skill_path.read_text(encoding="utf-8")
if "FULL_LOOP_IS_NOT_A_REVIEW_LENS" not in skill:
    marker = "한 전체 회차:\n"
    idx = skill.find(marker)
    if idx < 0:
        raise SystemExit("adversarial full loop marker missing")
    section = """### Full loop counting correction

`FULL_LOOP_IS_NOT_A_REVIEW_LENS`

**관점 하나만 검사한 것은 full loop로 계수하지 않는다.** 다음처럼 회차를 서로 다른 lens로 쪼개는 방식은 최소 5회 계약을 충족하지 않는다.

```text
Loop 1 = scope
Loop 2 = UX
Loop 3 = consumer
Loop 4 = alternatives
Loop 5 = CI
```

각 계수 회차는 같은 승인 범위 전체에 대해 **현행·정본·범위 재확인 → material decision의 최소 3개 실질 대안/현행 비교 → attack → validate-critique → refine-approved-findings → regression-recheck / execution verification → BETTER_ALTERNATIVE_SEARCH → LONG_TERM_PLAN_FIT_RECHECK → RE-ATTACK resulting state**를 모두 수행한다. 회차 보고에서 가장 큰 finding이나 특정 lens를 강조할 수는 있지만 그 lens만 검사한 회차는 full loop가 아니다.

"""
    skill = skill[:idx] + section + skill[idx:]
skill_path.write_text(skill, encoding="utf-8")

print("ACTUAL_ACTIVE_OWNERSHIP_POLICY_APPLIED")
