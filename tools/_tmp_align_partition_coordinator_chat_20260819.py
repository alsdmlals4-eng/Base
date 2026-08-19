from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
model_path = ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md"
integration_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md"
worker_prompt_path = ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md"

manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
integration = manifest["integration"]
integration.pop("chat_count", None)
integration["integration_chat"] = "CURRENT_COORDINATOR_CHAT"
integration["new_integration_chat_count"] = 0
integration["worker_chat_count"] = 9
integration["total_new_gpt_chats_after_task_1"] = 9
integration["final_confirmation_chat"] = "CURRENT_COORDINATOR_CHAT"
steps = integration["ordered_steps"]
return_step = "Return P01..P09 completion packets to CURRENT_COORDINATOR_CHAT"
if return_step not in steps:
    steps.insert(0, return_step)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

model = model_path.read_text(encoding="utf-8")
marker = "### 새 채팅 수와 최종 Integration 위치\n"
if marker not in model:
    anchor = "- 동일 의미를 GitHub/Notion 양쪽에 독립 정본으로 만들지 않는다. GitHub가 구조화 규칙/Skill/Test 정본이고 Notion은 사람이 보는 설명·시각화·학습면이다.\n"
    section = """

### 새 채팅 수와 최종 Integration 위치

- **새 GPT 채팅은 P01~P09의 9개만** 만든다.
- 각 새 채팅은 자기 Part를 처음부터 완료보고·PR·Notion 갱신까지 맡는다.
- 각 Part가 끝나면 결과를 이 Partition 설계를 수행한 원래 총괄 채팅인 `CURRENT_COORDINATOR_CHAT`으로 회수한다.
- 별도의 새 Integration 채팅을 만들지 않는다. `CURRENT_COORDINATOR_CHAT`이 CP0 변경, cross-part 조정, 전체 회귀, 최종 적대적 검토, 병합 후 확인을 수행한다.
- 이 위치 규칙은 사용자 편의만이 아니라 Part 결과를 같은 총괄 맥락에서 다시 합쳐 누락·충돌을 찾기 위한 continuity 계약이다.
"""
    if anchor not in model:
        raise SystemExit("operating model coordinator anchor missing")
    model = model.replace(anchor, anchor + section, 1)
model_path.write_text(model, encoding="utf-8", newline="\n")

prompt = integration_prompt_path.read_text(encoding="utf-8")
marker = "## 0A. 실행 위치 — CURRENT_COORDINATOR_CHAT\n"
if marker not in prompt:
    anchor = "Partition의 최종 산출물은 9개의 독립 Base가 아니라 **하나의 통합 Base**다. 필요한 Part만 활성화할 수 있으며, Integration은 실제로 수행된 Part의 결과만 모아 CP0·정본·Skill/Module 관계를 정리한다. 모든 일반 작업에 9개 Part 실행을 강제하지 않는다.\n"
    section = """

## 0A. 실행 위치 — CURRENT_COORDINATOR_CHAT

- 이 Integration은 새 채팅을 추가로 만들지 않는다.
- P01~P09를 분배하기 전 Partition 설계를 수행한 **현재 총괄 채팅**을 `CURRENT_COORDINATOR_CHAT`으로 부른다.
- 9개 Part 채팅이 끝나면 각 completion packet, PR, Notion 결과, `CROSS_PART_CHANGE_REQUEST`를 이 채팅으로 가져와 최종 통합한다.
- 이 채팅은 Part별 소유권을 침범하지 않고, 병합된/완료된 결과만 CP0와 ONE BASE에 통합한다.
"""
    if anchor not in prompt:
        raise SystemExit("integration prompt coordinator anchor missing")
    prompt = prompt.replace(anchor, anchor + section, 1)
integration_prompt_path.write_text(prompt, encoding="utf-8", newline="\n")

worker = worker_prompt_path.read_text(encoding="utf-8")
marker = "## 완료 후 회수 위치\n"
if marker not in worker:
    anchor = "- 이미지·다이어그램은 Part 전용이면 자기 Notion 페이지에, 프로젝트 고유이면 정확한 Project Notion에 배치한다. 공용 자료의 중복 복사는 금지한다.\n"
    section = """

## 완료 후 회수 위치

Part가 `CLEAN_REVIEW_EXIT`와 자기 PR/Notion readback까지 완료되면 completion packet을 `CURRENT_COORDINATOR_CHAT`으로 전달한다. 새 Integration 채팅을 만들거나 다른 Part 채팅의 PR을 직접 합치지 않는다.
"""
    if anchor not in worker:
        raise SystemExit("worker coordinator anchor missing")
    worker = worker.replace(anchor, anchor + section, 1)
worker_prompt_path.write_text(worker, encoding="utf-8", newline="\n")

print("PARTITION_COORDINATOR_CHAT_ALIGNED")
