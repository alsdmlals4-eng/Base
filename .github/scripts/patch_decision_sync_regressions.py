from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"{label}: old text missing")
    return text.replace(old, new, 1)


registry_path = ROOT / "skills/SKILL_REGISTRY.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
design = next(item for item in registry["skills"] if item["skill_id"] == "managing-design-documents")
old_use = design["use_when"][0]
checkpoint_clause = " 하위 시스템 checkpoint에서는 이미 즉시 정본화된 Decision의 누락·충돌·중복·대체 관계를 감사한다."
if "하위 시스템 checkpoint" not in old_use:
    design["use_when"] = [old_use + checkpoint_clause]
registry_path.write_text(json.dumps(registry, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

protocol_path = ROOT / "skills/managing-project-intake-and-work-contract/references/grill-me-protocol.md"
protocol = protocol_path.read_text(encoding="utf-8")
protocol = replace_required(
    protocol,
    "저장소·책임 원본·Google Sheets·현재 대화에서 답을 찾을 수 없는가?",
    "저장소·책임 원본·현재 대화·Google Sheets에서 답을 찾을 수 없는가?",
    "grill protocol compatibility phrase",
)
protocol_path.write_text(protocol, encoding="utf-8")

template_path = ROOT / "templates/project-operations/GRILL_ME_DECISION_RECORD.md"
template = template_path.read_text(encoding="utf-8")
template = replace_required(
    template,
    "| Decision ID | 질문 | 분류 | 기존 Decision | GPT 권장안 | 사용자 답변 | 최종 결정 | 분야 정본 | main Commit | Sheet 위치 | 동기화 상태 |",
    "| 질문 ID / Decision ID | 질문 | 분류 | 기존 Decision | GPT 권장안 | 사용자 답변 | 최종 결정 | 분야 정본 | 반영 Commit | Sheet 위치 | 동기화 상태 |",
    "decision ledger headers",
)
template = replace_required(template, "- main Commit:", "- 반영 Commit:", "decision detail commit label")
template = replace_required(template, "## 제거·보류·기각 요소", "## 제거·보류 요소 (기각 포함)", "decision disposition heading")
template_path.write_text(template, encoding="utf-8")

adversarial_path = ROOT / "skills/running-adversarial-review-and-refinement/SKILL.md"
adversarial = adversarial_path.read_text(encoding="utf-8")
if len(adversarial.splitlines()) > 150:
    adversarial = replace_required(
        adversarial,
        "병합 후 표준 양식은 `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md`를 사용한다.\n\n## Post-merge final decisions",
        "병합 후 표준 양식은 `templates/quality/POST_MERGE_ADVERSARIAL_REVIEW.md`를 사용한다.\n## Post-merge final decisions",
        "compact skill line budget",
    )
adversarial_path.write_text(adversarial, encoding="utf-8")

if len(adversarial.splitlines()) > 150:
    raise SystemExit(f"adversarial skill still exceeds compact limit: {len(adversarial.splitlines())}")
