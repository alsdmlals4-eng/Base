from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "docs/operations/BASE_PARTITION_MANIFEST.json"
OPERATING_MODEL = ROOT / "docs/operations/BASE_PARTITION_OPERATING_MODEL.md"
LEARNING_SYSTEM = ROOT / "docs/operations/BASE_PARTITION_LEARNING_SYSTEM.md"
WORKER_PROMPT = ROOT / "templates/prompts/BASE_PARTITION_OPTIMIZATION_PROMPT.md"
INTEGRATION_PROMPT = ROOT / "templates/prompts/BASE_PARTITION_INTEGRATION_PROMPT.md"
SOURCE_SCRIPT = ROOT / "tools/periodic_source_scan_queue.py"
RUN_SCRIPT = ROOT / "tools/run_periodic_source_scan_queue.sh"
PARTITION_TEST = ROOT / "tests/test_base_partition_contract.py"
PARTITION_WORKFLOW = ROOT / ".github/workflows/base-partition-contract.yml"
SOURCE_WORKFLOW = ROOT / ".github/workflows/periodic-source-scan-queue.yml"

SOURCE_MAP = {
    "P01": {
        "domains": ["PROMPT_AND_AGENT_WORKFLOW", "SKILL_AUTHORING_AND_EVOLUTION"],
        "questions": [
            "Notion/project operating systems that reduce duplicate decisions and handoff loss",
            "human-facing documentation patterns that preserve one machine/runtime truth",
            "agent instruction/context patterns that reduce repeated clarification and unnecessary executor hops",
        ],
    },
    "P02": {
        "domains": ["SKILL_AUTHORING_AND_EVOLUTION", "CODE_ENGINEERING", "PROMPT_AND_AGENT_WORKFLOW"],
        "questions": [
            "skill consolidation, progressive disclosure, routing precision and evaluation",
            "deprecation/legacy retirement patterns that preserve unique knowledge before deletion",
            "canonical-reference freshness and stale-reference detection practices",
        ],
    },
    "P03": {
        "domains": ["CODE_ENGINEERING", "PROMPT_AND_AGENT_WORKFLOW"],
        "questions": [
            "adversarial review and defect-finding methods that avoid performative checklist loops",
            "contract-preserving refactoring and semantic regression detection",
            "Git/worktree/PR concurrency and exact-head integration safety",
        ],
    },
    "P04": {
        "domains": ["GAME_DEVELOPMENT"],
        "questions": [
            "player motivation, choice, reward, memory and first-impression evidence",
            "vertical-slice and prototype validation practices for small teams",
            "game balance, difficulty, onboarding and player-research methods with usable evidence",
        ],
    },
    "P05": {
        "domains": ["GAME_DEVELOPMENT"],
        "questions": [
            "art direction and visual-consistency pipelines that reduce synthetic/AI-looking artifacts",
            "game UX/UI readability, accessibility and first-impression evaluation",
            "image-to-structured-layer/reusable-asset workflows and visual provenance management",
        ],
    },
    "P06": {
        "domains": ["GAME_DEVELOPMENT", "CODE_ENGINEERING"],
        "questions": [
            "current Godot engine/runtime/debugging guidance and regressions",
            "addon/plugin evaluation, editor tooling and local execution reliability",
            "runtime QA tooling that provides unique evidence without duplicating the authoring authority",
        ],
    },
    "P07": {
        "domains": ["GAME_DEVELOPMENT", "CODE_ENGINEERING"],
        "questions": [
            "platform/store/build/release requirements and official policy changes",
            "evidence-led validation, accessibility/performance/release readiness practices",
            "backend, entitlement, DRM, rights and distribution practices appropriate for small games",
        ],
    },
    "P08": {
        "domains": ["PROMPT_AND_AGENT_WORKFLOW", "SKILL_AUTHORING_AND_EVOLUTION", "CODE_ENGINEERING"],
        "questions": [
            "current agent/context/prompt/eval patterns that reduce tool and skill overload",
            "model routing and cost-control practices that preserve quality without new paid dependencies",
            "safe external-executor/worktree patterns for long-running coding tasks",
        ],
    },
    "P09": {
        "domains": ["FICTION_AND_INTERACTIVE_NARRATIVE", "YOUTUBE_AND_VIDEO_EDITING"],
        "questions": [
            "serial-fiction revision, character voice and continuity methods",
            "interactive narrative, mystery/clue and worldbuilding practices with audience evidence",
            "game-development YouTube packaging, script, edit and analytics practices without copying expression",
        ],
    },
}


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}_PATTERN_COUNT={count}")
    return text.replace(old, new, 1)


manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
protected = manifest["control_plane"]["protected_write_paths"]
if "docs/operations/base-partitions/**" in protected:
    protected.remove("docs/operations/base-partitions/**")
for part in manifest["parts"]:
    context_path = part["context_pack"]
    if context_path not in protected:
        protected.append(context_path)
for path in [
    "docs/operations/BASE_PARTITION_LEARNING_SYSTEM.md",
]:
    if path not in protected:
        protected.append(path)

manifest["learning_system"] = {
    "contract": "WORK_COMPLETION_LEARNING_CHECKPOINT_PLUS_PERIODIC_SOURCE_DISCOVERY",
    "required_after_each_part_work": True,
    "no_forced_lesson_token": "NO_NEW_REUSABLE_LESSON",
    "promotion_flow": "PART_LEARNING_LOG -> CROSS_PART_CHANGE_REQUEST/PROMOTION_CANDIDATE -> INTEGRATION -> canonical Base owner",
    "periodic_source_queue": ".github/workflows/periodic-source-scan-queue.yml",
    "source_policy_owner": "docs/knowledge/game-development/PERIODIC_EXTERNAL_SOURCE_WATCHLIST.md",
    "operations_ledger": "docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json",
    "research_executor": "USER_DIRECTED_CHATGPT_REVIEW",
    "auto_canon_write": False,
    "auto_learning_claim": False,
    "rules": [
        "Every completed Part work records one checkpoint, including NO_NEW_REUSABLE_LESSON when appropriate",
        "Project-specific lessons stay project-specific unless the Base promotion gate is satisfied",
        "External discovery remains UNVERIFIED_DISCOVERY until original-source review and evidence disposition",
        "New source count is not a success metric; decision improvement and reproducibility are",
        "Source Queue preparation does not imply research completion or learning completion",
    ],
}

for part in manifest["parts"]:
    pid = part["part_id"]
    learning_path = f"docs/operations/base-partitions/learning/{pid}_LEARNING_LOG.md"
    if learning_path not in part["owned_write_paths"]:
        part["owned_write_paths"].append(learning_path)
    part["learning_log"] = learning_path
    part["learning_capture"] = {
        "required_after_each_work": True,
        "fields": [
            "work_ref", "baseline_and_result", "what_worked", "what_failed_or_was_rejected",
            "reusable_lesson", "anti_pattern", "affected_rules_skills_modules", "evidence",
            "reuse_scope", "promotion_candidate", "source_followup_questions", "revisit_condition",
        ],
        "reuse_scope_values": ["PART_ONLY", "BASE_PROMOTION_CANDIDATE", "PROJECT_ONLY", "NO_NEW_REUSABLE_LESSON"],
    }
    part["source_discovery"] = {
        "periodic_queue": "Periodic Source Scan Queue",
        "source_domains": SOURCE_MAP[pid]["domains"],
        "discovery_questions": SOURCE_MAP[pid]["questions"],
        "existing_source_action": "CHECK_DUE_OR_MATERIAL_NEW_OR_UPDATED_ITEMS",
        "new_source_action": "SEARCH_FOR_ADDITIONAL_PRIMARY_OR_PROFESSIONAL_SOURCES",
        "disposition_required": True,
        "allowed_dispositions": ["ADOPT", "ADAPT", "TEST", "PROJECT_ONLY", "REFERENCE_ONLY", "AVOID", "IGNORE", "BLOCKED_UNVERIFIED", "PROMOTION_CANDIDATE"],
    }

steps = manifest["integration"]["ordered_steps"]
learning_step = "Review P01..P09 learning logs and promote only validated reusable lessons"
source_step = "Route periodic Source Queue discoveries to P01..P09 and preserve UNVERIFIED_DISCOVERY until reviewed"
if learning_step not in steps:
    steps.insert(3, learning_step)
if source_step not in steps:
    steps.insert(4, source_step)

MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

learning_dir = ROOT / "docs/operations/base-partitions/learning"
learning_dir.mkdir(parents=True, exist_ok=True)
for part in manifest["parts"]:
    pid = part["part_id"]
    path = ROOT / part["learning_log"]
    if not path.exists():
        path.write_text(
            f"# {pid} · {part['name']} — Learning Log\n\n"
            "> 이 로그는 해당 Part 작업에서 실제로 확인된 교훈만 축적한다. 추정·외부 snippet·미검증 Source는 학습 사실로 승격하지 않는다.\n\n"
            "## 작업별 Learning Checkpoint\n\n"
            "각 완료 작업마다 아래 형식으로 하나의 checkpoint를 추가한다. 새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`로 명시하고 억지 교훈을 만들지 않는다.\n\n"
            "```yaml\n"
            "date:\nwork_ref:\nbaseline_and_result:\nwhat_worked: []\nwhat_failed_or_was_rejected: []\n"
            "reusable_lesson:\nanti_pattern: []\naffected_rules_skills_modules: []\nevidence: []\n"
            "reuse_scope: PART_ONLY | BASE_PROMOTION_CANDIDATE | PROJECT_ONLY | NO_NEW_REUSABLE_LESSON\n"
            "promotion_candidate:\nsource_followup_questions: []\nrevisit_condition:\n"
            "```\n\n"
            "## Source Learning\n\n"
            f"- Source domains: {', '.join(part['source_discovery']['source_domains'])}\n"
            "- 전역 `Periodic Source Scan Queue`의 due/new-source 후보를 이 Part 질문으로 검토한다.\n"
            "- `UNVERIFIED_DISCOVERY`는 원출처·날짜·적용 범위·반례·consumer·검증을 확인하기 전 학습/정본이 아니다.\n"
            "- 실제 Base 공용 개선으로 재사용할 가치가 있을 때만 `BASE_PROMOTION_CANDIDATE`로 Integration에 보낸다.\n",
            encoding="utf-8",
            newline="\n",
        )

LEARNING_SYSTEM.write_text(
    "# Base Partition Learning & Source Discovery System\n\n"
    "## 목적\n\n"
    "P01~P09가 단발 최적화로 끝나지 않고 **작업마다 실제 교훈을 축적하고, 주기적으로 새 외부 Source를 찾아 검증한 뒤 필요한 최소 개선만 흡수**하도록 한다. 새 광역 Skill이나 별도 유료 AI 파이프라인을 만들지 않고 기존 Periodic Source Scan Queue를 재사용한다.\n\n"
    "## 1. 작업마다 Learning Checkpoint\n\n"
    "모든 Part 작업은 완료 직전에 자기 `learning_log`에 checkpoint 하나를 남긴다. 이것은 회고문이 아니라 재사용 가능한 운영 증거다.\n\n"
    "- 무엇이 실제로 잘 작동했는가\n- 무엇이 실패/기각됐는가\n- 어떤 규칙·Skill·Module에 영향을 주는가\n- evidence는 무엇인가\n- Part 전용인가, 프로젝트 전용인가, Base 승격 후보인가\n- 다음에 확인할 Source 질문과 재검토 조건은 무엇인가\n\n"
    "새 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`을 기록한다. 작업마다 억지로 새 원칙을 만들지 않는다.\n\n"
    "## 2. 승격 흐름\n\n"
    "```text\nPart work\n→ Part Learning Log\n→ PART_ONLY / PROJECT_ONLY / NO_NEW_REUSABLE_LESSON / BASE_PROMOTION_CANDIDATE\n→ BASE_PROMOTION_CANDIDATE만 Integration 검토\n→ 기존 canonical owner가 있으면 흡수\n→ 없고 반복 재사용 가치가 입증될 때만 새 owner 검토\n→ regression + adversarial review + merge\n```\n\n"
    "Learning Log는 새 정본이 아니다. 현행 정책·Skill과 충돌하면 기존 canonical owner가 우선하며, Integration이 승격을 판정한다.\n\n"
    "## 3. 주기 Source Learning\n\n"
    "기존 `.github/workflows/periodic-source-scan-queue.yml`이 주기적으로 due Source Queue를 준비한다. Queue 준비는 무료/결정론적이며 AI 웹조사를 자동 수행하지 않는다. 실제 조사와 Evidence disposition은 `USER_DIRECTED_CHATGPT_REVIEW`가 수행한다.\n\n"
    "Queue는 Manifest의 각 Part `source_discovery`를 읽어 P01~P09별 Learning Radar를 보여준다. 각 Radar는 기존 Source 새 글/변경과 **추가 신규 Source 사이트 탐색** 질문을 함께 가진다.\n\n"
    "### Source 후보 판정\n\n"
    "`ADOPT | ADAPT | TEST | PROJECT_ONLY | REFERENCE_ONLY | AVOID | IGNORE | BLOCKED_UNVERIFIED | PROMOTION_CANDIDATE` 중 하나로 닫는다. Source 개수, 조회수, 기사 제목, AI 요약만으로 Canon/학습을 만들지 않는다.\n\n"
    "## 4. Part별 Source Radar\n\n"
    + "\n".join(
        f"### {part['part_id']} · {part['name']}\n"
        f"- domains: {', '.join(part['source_discovery']['source_domains'])}\n"
        + "\n".join(f"- {q}" for q in part['source_discovery']['discovery_questions'])
        for part in manifest["parts"]
    )
    + "\n\n## 5. Integration\n\n"
    "Integration GPT는 Part별 Learning Log를 읽어 같은 교훈을 중복 승격하지 않는다. Part 고유 교훈은 Part에 남기고, 여러 Part/프로젝트에서 반복되며 evidence가 있는 교훈만 기존 Base canonical owner에 반영한다.\n\n"
    "## 6. 완료/안전 경계\n\n"
    "- Queue prepared != research completed\n- research completed != lesson validated\n- lesson validated != Base canon promoted\n- external source != project/runtime truth\n- periodic scan 때문에 새 Skill/Tool을 강제로 만들지 않음\n- 추가 유료 API/SaaS를 기본 경로로 만들지 않음\n",
    encoding="utf-8",
    newline="\n",
)

op = OPERATING_MODEL.read_text(encoding="utf-8")
anchor = "## Part 완료 계약\n"
learning_section = """## 작업별 Learning + 주기 Source Learning\n\n각 Part는 작업을 마칠 때 자기 `docs/operations/base-partitions/learning/Pxx_LEARNING_LOG.md`에 Learning Checkpoint 하나를 남긴다. `BASE_PROMOTION_CANDIDATE`만 Integration에서 Base 공용 승격을 검토하고, 프로젝트 전용 교훈은 프로젝트에 남긴다. 새 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`을 기록해 억지 원칙 생성을 막는다.\n\n기존 `Periodic Source Scan Queue`를 재사용한다. Queue가 Manifest의 Part별 `source_discovery` 질문을 렌더링해 **기존 Source의 새/변경 자료 + 신규 관련 사이트/Source 탐색**을 정기적으로 요청한다. Queue 생성 자체는 학습 완료가 아니며, 실제 ChatGPT 원출처 검토·Evidence disposition 후에만 Learning Log/owner 개선 후보가 된다.\n\n자세한 계약: `docs/operations/BASE_PARTITION_LEARNING_SYSTEM.md`.\n\n"""
if learning_section not in op:
    op = replace_once(op, anchor, learning_section + anchor, "OPERATING_MODEL_LEARNING")
OPERATING_MODEL.write_text(op, encoding="utf-8", newline="\n")

worker = WORKER_PROMPT.read_text(encoding="utf-8")
worker_anchor = "## 10. 비용\n"
worker_learning = """## 9A. 작업마다 교훈·학습\n\n모든 완료 작업은 Manifest의 해당 Part `learning_log`에 Learning Checkpoint 하나를 추가한다. 최소 필드는 `work_ref`, 결과, worked/failed, `reusable_lesson`, anti-pattern, 영향을 받은 규칙·Skill·Module, evidence, reuse scope, source follow-up, revisit condition이다.\n\n새 재사용 교훈이 없으면 `reusable_lesson: NO_NEW_REUSABLE_LESSON`을 기록한다. 단지 형식을 채우기 위해 가짜 교훈·새 규칙·새 Skill을 만들지 않는다. 프로젝트 고유 교훈은 `PROJECT_ONLY`, Part 내부만 유효하면 `PART_ONLY`, 여러 프로젝트/Part에 재사용 가치와 evidence가 있으면 `BASE_PROMOTION_CANDIDATE`다. Base 승격은 이 Part가 직접 CP0를 수정하지 않고 `CROSS_PART_CHANGE_REQUEST`/Integration으로 넘긴다.\n\n### 주기 Source Learning\n\n전역 `Periodic Source Scan Queue`와 Manifest의 `source_discovery`를 사용한다. 기존 Source의 새/변경 자료를 확인하고, 각 작업의 실패·빈 coverage·재검토 조건에서 **추가 관련 사이트/Source 검색 질문**을 만든다. 발견 자료는 원출처·날짜·범위·반례·commercial interest·consumer·validation을 확인하기 전 `UNVERIFIED_DISCOVERY`다. Source 수 자체를 목표로 하지 않는다.\n\n"""
if worker_learning not in worker:
    worker = replace_once(worker, worker_anchor, worker_learning + worker_anchor, "WORKER_LEARNING")
WORKER_PROMPT.write_text(worker, encoding="utf-8", newline="\n")

integration = INTEGRATION_PROMPT.read_text(encoding="utf-8")
int_anchor = "## 8. 검증\n"
int_learning = """## 7A. Learning 통합\n\nP01~P09의 `learning_log`를 모두 읽는다. 같은 교훈의 중복 승격을 합치고 `PROJECT_ONLY`/`PART_ONLY`는 원래 범위에 남긴다. `BASE_PROMOTION_CANDIDATE`도 evidence·반복 재사용성·기존 canonical owner를 재검증한 뒤에만 흡수한다.\n\nPeriodic Source Scan Queue에서 나온 항목은 `UNVERIFIED_DISCOVERY → source/evidence disposition → Part lesson → Base promotion candidate` 순서를 건너뛰지 않는다. 신규 사이트 수를 KPI로 삼지 않고 실제 결정 개선·재현성·회귀 감소를 본다.\n\n"""
if int_learning not in integration:
    integration = replace_once(integration, int_anchor, int_learning + int_anchor, "INTEGRATION_LEARNING")
INTEGRATION_PROMPT.write_text(integration, encoding="utf-8", newline="\n")

source = SOURCE_SCRIPT.read_text(encoding="utf-8")
if "def load_partition_manifest(" not in source:
    insert_anchor = "def _cell(value: object) -> str:\n    return (\"\" if value is None else str(value)).replace(\"|\", \"\\\\|\").replace(\"\\n\", \" \").strip()\n\n\n"
    extra = '''def load_partition_manifest(path: Path) -> dict[str, object]:\n    try:\n        payload: Any = json.loads(path.read_text(encoding="utf-8"))\n    except json.JSONDecodeError as error:\n        raise ValueError(f"invalid JSON partition manifest: {path}") from error\n    if not isinstance(payload, dict) or payload.get("contract_id") != "BASE_PARTITION_OPERATING_MODEL_V1":\n        raise ValueError("invalid Base partition manifest")\n    return payload\n\n\ndef render_partition_learning_radar(manifest: dict[str, object]) -> str:\n    parts = manifest.get("parts")\n    if not isinstance(parts, list):\n        raise ValueError("partition manifest parts must be a list")\n    lines = [\n        "## Partition Learning Radar",\n        "",\n        "> 각 Part는 기존 Source의 새/변경 자료와 추가 신규 Source 사이트를 탐색한다. 아래 항목은 조사 질문이며 그 자체로 학습·Canon이 아니다.",\n        "",\n    ]\n    for raw in parts:\n        if not isinstance(raw, dict):\n            raise ValueError("partition entry must be an object")\n        part_id = _text(raw.get("part_id"), "part_id")\n        name = _text(raw.get("name"), "name")\n        discovery = raw.get("source_discovery")\n        if not isinstance(discovery, dict):\n            raise ValueError(f"missing source_discovery for {part_id}")\n        domains = discovery.get("source_domains")\n        questions = discovery.get("discovery_questions")\n        if not isinstance(domains, list) or not domains or not isinstance(questions, list) or not questions:\n            raise ValueError(f"invalid source_discovery for {part_id}")\n        lines.extend([f"### {part_id} · {name}", "", f"- Source domains: {', '.join(str(x) for x in domains)}"])
        lines.extend(f"- [ ] {str(question)}" for question in questions)
        lines.extend(["- [ ] 기존 Watchlist/원출처보다 더 권위 있거나 더 직접적인 신규 Source 후보가 있는지 탐색했다.", "- [ ] 후보를 current owner/consumer/validation/revisit condition에 연결했다.", ""])
    return "\\n".join(lines).rstrip()\n\n\n'''
    source = replace_once(source, insert_anchor, insert_anchor + extra, "SOURCE_HELPERS")
    source = replace_once(source, "def render_issue_body(payload: dict[str, object], today: date) -> str:\n", "def render_issue_body(payload: dict[str, object], today: date, partition_manifest: dict[str, object] | None = None) -> str:\n", "SOURCE_SIGNATURE")
    source = replace_once(source, "    return \"\\n\".join(lines)\n\n\ndef main", "    if partition_manifest is not None:\n        lines.extend([\"\", render_partition_learning_radar(partition_manifest), \"\"])\n    return \"\\n\".join(lines)\n\n\ndef main", "SOURCE_RENDER_APPEND")
    source = replace_once(source, "    parser.add_argument(\"--output\", type=Path, required=True)\n", "    parser.add_argument(\"--output\", type=Path, required=True)\n    parser.add_argument(\"--partition-manifest\", type=Path)\n", "SOURCE_ARG")
    source = replace_once(source, "    args.output.write_text(render_issue_body(load_ledger(args.ledger), queue_date), encoding=\"utf-8\", newline=\"\\n\")\n", "    partition_manifest = load_partition_manifest(args.partition_manifest) if args.partition_manifest else None\n    args.output.write_text(render_issue_body(load_ledger(args.ledger), queue_date, partition_manifest), encoding=\"utf-8\", newline=\"\\n\")\n", "SOURCE_MAIN")
SOURCE_SCRIPT.write_text(source, encoding="utf-8", newline="\n")

run = RUN_SCRIPT.read_text(encoding="utf-8")
old_call = "  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \\\n  --date \"$QUEUE_DATE\" \\\n  --output \"$QUEUE_PATH\""
new_call = "  --ledger docs/knowledge/game-development/PERIODIC_SOURCE_OPERATIONS_LEDGER.json \\\n  --partition-manifest docs/operations/BASE_PARTITION_MANIFEST.json \\\n  --date \"$QUEUE_DATE\" \\\n  --output \"$QUEUE_PATH\""
if "--partition-manifest" not in run:
    run = replace_once(run, old_call, new_call, "RUN_SCRIPT_MANIFEST")
RUN_SCRIPT.write_text(run, encoding="utf-8", newline="\n")

workflow = SOURCE_WORKFLOW.read_text(encoding="utf-8")
if '"docs/operations/BASE_PARTITION_MANIFEST.json"' not in workflow:
    workflow = replace_once(workflow, '      - "docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md"\n', '      - "docs/knowledge/game-development/PERIODIC_SOURCE_SCAN_QUEUE.md"\n      - "docs/operations/BASE_PARTITION_MANIFEST.json"\n      - "docs/operations/BASE_PARTITION_LEARNING_SYSTEM.md"\n', "SOURCE_WORKFLOW_PATHS")
SOURCE_WORKFLOW.write_text(workflow, encoding="utf-8", newline="\n")

pt = PARTITION_TEST.read_text(encoding="utf-8")
if "BASE_PARTITION_LEARNING_SYSTEM.md" not in pt:
    pt = replace_once(pt, 'SCOPE_CHECKER = ROOT / "tools" / "check_base_partition_scope.py"\n', 'SCOPE_CHECKER = ROOT / "tools" / "check_base_partition_scope.py"\nLEARNING_SYSTEM = ROOT / "docs" / "operations" / "BASE_PARTITION_LEARNING_SYSTEM.md"\n', "TEST_CONSTANT")
    pt = replace_once(pt, "        for path in (MANIFEST, OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT, SCOPE_CHECKER):\n", "        for path in (MANIFEST, OPERATING_MODEL, WORKER_PROMPT, INTEGRATION_PROMPT, SCOPE_CHECKER, LEARNING_SYSTEM):\n", "TEST_ARTIFACTS")
    test_insert = '''\n    def test_each_part_has_learning_log_and_source_discovery(self) -> None:\n        manifest = self.load_manifest()\n        self.assertTrue(manifest["learning_system"]["required_after_each_part_work"])\n        for part in manifest["parts"]:\n            learning_log = ROOT / part["learning_log"]\n            self.assertTrue(learning_log.exists(), part["part_id"])\n            self.assertIn(part["learning_log"], part["owned_write_paths"])\n            capture = part["learning_capture"]\n            self.assertTrue(capture["required_after_each_work"])\n            self.assertIn("NO_NEW_REUSABLE_LESSON", capture["reuse_scope_values"])\n            discovery = part["source_discovery"]\n            self.assertTrue(discovery["source_domains"])\n            self.assertGreaterEqual(len(discovery["discovery_questions"]), 3)\n\n    def test_periodic_source_queue_renders_partition_learning_radar(self) -> None:\n        from tools.periodic_source_scan_queue import render_partition_learning_radar\n        text = render_partition_learning_radar(self.load_manifest())\n        self.assertIn("Partition Learning Radar", text)\n        for part_id in [f"P{i:02d}" for i in range(1, 10)]:\n            self.assertIn(part_id, text)\n        self.assertIn("신규 Source 후보", text)\n\n'''
    pt = replace_once(pt, "\n\nif __name__ == \"__main__\":\n", test_insert + "\nif __name__ == \"__main__\":\n", "TEST_INSERT")
PARTITION_TEST.write_text(pt, encoding="utf-8", newline="\n")

pw = PARTITION_WORKFLOW.read_text(encoding="utf-8")
if "tools/periodic_source_scan_queue.py" not in pw:
    pw = replace_once(pw, "        run: python -m py_compile tools/check_base_partition_scope.py tests/test_base_partition_contract.py\n", "        run: python -m py_compile tools/check_base_partition_scope.py tools/periodic_source_scan_queue.py tests/test_base_partition_contract.py\n", "PARTITION_WORKFLOW_COMPILE")
    pw = replace_once(pw, "        run: python -m unittest tests.test_base_partition_contract -v\n", "        run: python -m unittest tests.test_base_partition_contract tests.test_periodic_source_scan_queue -v\n", "PARTITION_WORKFLOW_TEST")
PARTITION_WORKFLOW.write_text(pw, encoding="utf-8", newline="\n")

for part in manifest["parts"]:
    context_path = ROOT / part["context_pack"]
    text = context_path.read_text(encoding="utf-8")
    if "## 학습 루프" not in text:
        section = (
            "\n## 학습 루프\n"
            f"- 작업마다 `{part['learning_log']}`에 Learning Checkpoint를 남긴다.\n"
            "- 새 공용 교훈이 없으면 `NO_NEW_REUSABLE_LESSON`; 프로젝트 전용이면 `PROJECT_ONLY`; Base 승격 후보면 `BASE_PROMOTION_CANDIDATE`.\n"
            f"- 주기 Source domains: {', '.join(part['source_discovery']['source_domains'])}.\n"
            "- 전역 Periodic Source Scan Queue에서 기존 Source 새/변경 자료와 신규 관련 사이트를 탐색하고, 원출처 검증 전에는 `UNVERIFIED_DISCOVERY`로 유지한다.\n"
        )
        context_path.write_text(text.rstrip() + section + "\n", encoding="utf-8", newline="\n")

Path(__file__).unlink()
print("BASE_PARTITION_LEARNING_SYSTEM_APPLIED")
