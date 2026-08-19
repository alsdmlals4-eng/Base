from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8", newline="\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    if old not in text:
        raise SystemExit(f"missing anchor in {path}: {old[:120]!r}")
    write(path, text.replace(old, new, 1))


# Manifest: open PR state is backlog metadata, not active-worker evidence.
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["open_pr_policy"] = "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM"
manifest["independent_workstream_policy"] = "ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED_WHEN_ACTUALLY_ACTIVE"
manifest["active_workstream_detection"] = {
    "requires_current_owner_evidence": True,
    "open_pr_state_is_sufficient": False,
    "current_owner_evidence": [
        "USER_EXPLICITLY_IDENTIFIES_ANOTHER_ACTIVE_CHAT_OR_WORKER",
        "CURRENT_SESSION_OR_AUTOMATION_OWNERSHIP_MARKER",
        "CURRENT_RESOURCE_LOCK_OR_RUNNING_EXECUTION_WITH_MATCHING_OWNER",
    ],
    "coordinator_takeover_signals": [
        "USER_CONFIRMED_SINGLE_ACTIVE_CHAT",
        "CURRENT_COORDINATOR_CHAT",
    ],
    "open_pr_classifications": [
        "ACTIVE_OTHER_WORKER",
        "COORDINATOR_TAKEOVER",
        "SUPERSEDED_DUPLICATE",
        "STALE_BACKLOG",
        "BLOCKED_EXTERNAL",
        "READY_TO_FINISH",
    ],
    "rule": "PR state is metadata. Classify actual current ownership before deciding whether mutation is forbidden.",
}
manifest["control_plane"]["change_protocol"] = [
    "Coordinator may fix validated cross-Part or CP0 findings directly with CROSS_PART_CHANGE semantic attribution",
    "Different Part ownership alone is not a write barrier",
    "Open PR state alone is not active-worker evidence; require current owner evidence before protecting a workstream",
    "When the user confirms CURRENT_COORDINATOR_CHAT is the only active worker, classify unresolved open PRs and use COORDINATOR_TAKEOVER, READY_TO_FINISH, SUPERSEDED_DUPLICATE, STALE_BACKLOG, or BLOCKED_EXTERNAL as appropriate",
    "Only ACTIVE_OTHER_WORKER workstreams are mutation-protected unless the user explicitly authorizes takeover",
    "CROSS_PART_CHANGE_REQUEST is reserved for real authority/evidence/current-owner blockers",
    "Generated artifacts are rebuilt from authority rather than hand-edited",
    "Exact-head CI and post-merge GitHub/Notion readback are required",
]
coord = manifest["coordinator_execution"]
coord["active_independent_workstreams"] = "PROTECT_ONLY_AFTER_CURRENT_OWNER_EVIDENCE"
coord["open_pr_backlog_policy"] = "REVALIDATE_AND_CLASSIFY_NOT_AUTOMATIC_READ_ONLY"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Operating model: replace the over-broad active-workstream section.
old = '''## 독립 workstream 보호

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`

Part 경계 해제와 독립 workstream 보호는 서로 다른 규칙이다.

- **다른 Part**라는 사실은 수정 금지 사유가 아니다.
- **다른 독립 작업자의 open/draft/ready PR·branch·worktree**라는 사실은 보호 사유다.

현재 작업은 다른 활성 PR의 branch를 임의로 수정·rebase·close·merge하지 않는다. 같은 의미 수정이 필요하면:

1. 기존 활성 PR을 읽어 충돌·중복을 확인하고,
2. 최신 completed `main`에서 coordinator-owned branch로 안전하게 해결하거나,
3. 해당 active workstream 완료 후 다시 판정하거나,
4. 사용자가 명시적으로 인수하도록 지시했을 때만 기존 workstream을 직접 이어받는다.
'''
new = '''## 독립 workstream 보호와 open PR 분류

`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED_WHEN_ACTUALLY_ACTIVE`

Part 경계, PR 상태, 실제 동시 작업자는 서로 다른 개념이다.

- **다른 Part**라는 사실은 수정 금지 사유가 아니다.
- **PR이 open/draft/ready라는 상태만으로** 다른 작업자가 현재 작업 중이라고 판정하지 않는다.
- 실제 mutation 보호는 사용자 지시, 현재 세션/automation owner, Resource Lock, 실행 중인 matching workstream 등 **current owner evidence**가 있을 때만 적용한다.
- 사용자가 **“현재 작업 채팅은 이 채팅 하나”**라고 확인하면 unresolved open PR은 현재 coordinator의 backlog로 재분류한다.

열린 PR은 최신 `main`과 현재 Goal을 다시 읽은 뒤 다음 중 하나로 판정한다.

```text
ACTIVE_OTHER_WORKER
COORDINATOR_TAKEOVER
READY_TO_FINISH
SUPERSEDED_DUPLICATE
STALE_BACKLOG
BLOCKED_EXTERNAL
```

### 판정 뒤 행동

- `ACTIVE_OTHER_WORKER`: branch/worktree를 read-only 보호. takeover는 새 사용자 승인이나 명시적 owner handoff가 필요하다.
- `COORDINATOR_TAKEOVER`: 현재 coordinator가 기존 PR을 이어받거나 최신 main 기반 finish branch로 재구성할 수 있다.
- `READY_TO_FINISH`: current CI/acceptance를 다시 확인하고 정상 병합까지 닫는다.
- `SUPERSEDED_DUPLICATE`: 이미 main에 같은 의미가 유지되는지 readback한 뒤 중복 PR을 종료한다.
- `STALE_BACKLOG`: 현재 Goal에서 더 이상 가치가 없음을 근거로 종료/Archive한다.
- `BLOCKED_EXTERNAL`: 코드/기획 문제가 아니라 외부 권한·인프라·사용자 결정을 정확히 기록하고 대기한다.

즉 **open PR 목록은 보호 목록이 아니라 먼저 분류해야 하는 backlog inventory**다. 같은 채팅 하나만 활성인 상태에서 “open이므로 다른 채팅 일”이라고 보류하지 않는다.
'''
replace_once("docs/operations/BASE_PARTITION_OPERATING_MODEL.md", old, new)

# Worker prompt.
old = '''## 0B. 독립 활성 workstream 보호

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`

다른 Part라는 사실과 다른 독립 workstream이라는 사실을 구분한다.

- 다른 Part 경로: 필요하면 현재 coordinator가 수정 가능.
- 다른 사람/채팅의 open/draft/ready PR·branch·worktree: read-only가 기본.
- 기존 활성 PR을 임의로 수정·rebase·merge·close하지 않는다.
- 같은 의미 수정이 필요하면 최신 completed `main`에 coordinator-owned 변경으로 해결하거나, 그 workstream 완료 후 재검토한다.
- 사용자가 명시적으로 takeover를 지시한 경우만 기존 활성 workstream을 직접 이어받는다.
'''
new = '''## 0B. Open PR과 실제 활성 workstream 구분

`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED_WHEN_ACTUALLY_ACTIVE`

- 다른 Part 경로는 필요하면 현재 coordinator가 수정 가능하다.
- open/draft/ready는 **PR 상태**일 뿐 다른 작업자가 현재 활동 중이라는 증거가 아니다.
- 사용자 지시, current chat/automation owner, Resource Lock, 실행 중 workstream 등 current owner evidence가 있을 때만 `ACTIVE_OTHER_WORKER`로 보호한다.
- 사용자가 `CURRENT_COORDINATOR_CHAT`만 활성이라고 확인하면 열린 PR을 backlog로 읽고 `COORDINATOR_TAKEOVER / READY_TO_FINISH / SUPERSEDED_DUPLICATE / STALE_BACKLOG / BLOCKED_EXTERNAL` 중 하나로 재분류한다.
- **다른 Part라는 이유만으로 수정 보류 금지**이며, **open PR이라는 이유만으로도 수정 보류하지 않는다.**
- 실제 `ACTIVE_OTHER_WORKER`로 확인된 branch/worktree만 임의 수정·rebase·merge·close하지 않는다.
'''
replace_once("templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md", old, new)

# Integration prompt.
old = '''## 3. 독립 active workstream

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED`

open/draft/ready 독립 PR의 branch/worktree는 임의로 수정·rebase·merge·close하지 않는다. 같은 의미 수정이 필요하면 latest completed main의 coordinator-owned branch에서 해결하거나 해당 workstream의 완료 후 재평가한다.
'''
new = '''## 3. Open PR backlog와 실제 active workstream

`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`

`ACTIVE_INDEPENDENT_WORKSTREAMS_REMAIN_PROTECTED_WHEN_ACTUALLY_ACTIVE`

open/draft/ready 상태 자체는 현재 작업자 증거가 아니다. 열린 PR은 먼저 latest main과 Goal을 기준으로 `ACTIVE_OTHER_WORKER / COORDINATOR_TAKEOVER / READY_TO_FINISH / SUPERSEDED_DUPLICATE / STALE_BACKLOG / BLOCKED_EXTERNAL`로 분류한다.

사용자가 현재 활성 작업 채팅이 `CURRENT_COORDINATOR_CHAT` 하나뿐이라고 확인하면 unresolved open PR을 coordinator backlog로 인수해 직접 완료·흡수·중복 종료할 수 있다. 실제 current owner evidence가 있는 `ACTIVE_OTHER_WORKER`만 mutation-protected다.
'''
replace_once("templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md", old, new)

# AGENTS top-level invariant.
agents_path = "AGENTS.md"
agents = read(agents_path)
marker = "- L1 이상 작업은 최신 main, 현재 결정, 분야 정본, 같은 Goal의 열린·최근 병합 PR, 실제 구현을 비교해 중복·누락·충돌·구형 참조·미반영을 먼저 판정한다.\n"
addition = marker + "- **`OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`:** `open/draft/ready` PR 상태는 backlog metadata이지 다른 작업자가 현재 활동 중이라는 증거가 아니다. 실제 동시 작업자 보호는 사용자 지시, current session/automation owner, Resource Lock 등 `current owner evidence`가 있을 때만 `ACTIVE_OTHER_WORKER`로 적용한다. 사용자가 `CURRENT_COORDINATOR_CHAT` 하나만 활성이라고 확인하면 unresolved open PR은 최신 `main`과 Goal을 재검증해 `COORDINATOR_TAKEOVER / READY_TO_FINISH / SUPERSEDED_DUPLICATE / STALE_BACKLOG / BLOCKED_EXTERNAL`로 분류하고 현재 채팅에서 마무리할 수 있다.\n"
if "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM" not in agents:
    if marker not in agents:
        raise SystemExit("AGENTS L1 entry gate anchor missing")
    agents = agents.replace(marker, addition, 1)
write(agents_path, agents)

# Historical protected-followup note is superseded as an activity assumption, but keep findings.
followup_path = "docs/operations/PROTECTED_ACTIVE_WORKSTREAM_FOLLOWUPS_2026-08-19.md"
if (ROOT / followup_path).is_file():
    follow = read(followup_path)
    prefix = '''# Workstream backlog reconciliation · 2026-08-19

> **Supersession:** the earlier assumption "open PR = protected active worker" is superseded by `OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM`. The user confirmed `CURRENT_COORDINATOR_CHAT` is the only active work chat. Findings below remain evidence, but #530/#535/#537 are now coordinator backlog to revalidate and finish; they are not protected merely because they are open.

'''
    # Drop only the old first title/intro if present, preserve all finding sections.
    if follow.startswith("# Protected active-workstream follow-ups · 2026-08-19"):
        rest = follow.split("\n", 1)[1].lstrip()
        # remove the next explanatory paragraph if it is the old protection sentence
        old_intro = "These findings remain valid but are not rewritten by the sequential coordinator PR because active independent PR #530 owns the same policy/test surface.\n\n"
        if rest.startswith(old_intro):
            rest = rest[len(old_intro):]
        follow = prefix + rest
    elif "OPEN_PR_IS_NOT_ACTIVE_WORKSTREAM" not in follow:
        follow = prefix + follow
    write(followup_path, follow.rstrip() + "\n")

print("OPEN_PR_ACTIVITY_POLICY_APPLIED")
