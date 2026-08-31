from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path.cwd()
EVIDENCE = ROOT / "tests-evidence"
CANDIDATE = ROOT / "candidate"
TEST_SOURCE = ROOT / ".github/workflows-support/temp_ai_solution_layer_test.py"
TEST_PATH = ROOT / "tests/test_ai_solution_layer_selection_contract.py"
INTAKE_PATH = ROOT / "skills/managing-project-intake-and-work-contract/SKILL.md"
CAPABILITY_PATH = ROOT / "docs/CAPABILITY_COMPOSITION_MAP.md"

FOCUSED_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "tests",
    "-p",
    "test_ai_solution_layer_selection_contract.py",
    "-v",
]
PUBLIC_VIDEO_COMMAND = [
    sys.executable,
    "-m",
    "unittest",
    "discover",
    "-s",
    "tests",
    "-p",
    "test_public_video*.py",
    "-v",
]

PUBLIC_VIDEO_CONTRACT = r'''`PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER` / `VIDEO_LINK_IS_NOT_UNREADABLE_UNTIL_DECLARED_READER_LADDER_EXHAUSTED`: 사용자가 YouTube 같은 공개 영상의 내용 확인·요약·역공학·흡수를 요청하면 일반 웹 페이지 렌더 실패만으로 링크를 읽을 수 없다고 판정하지 않는다. 먼저 현재 Base의 `RM-TOOL-005 PUBLIC_VIDEO_RESEARCH_INGEST_ADAPTER`와 `tools/public_video_research_ingest.py`를 읽고 다음 source-type-specific reader ladder를 실제로 시도한다.

```text
exact video identity/title/channel readback
→ accessible manual caption
→ accessible automatic caption
→ current connected capability or caller-supplied local .vtt/.srt/.txt normalized by the existing adapter
→ already-installed bounded local ASR when authorized and necessary
→ BLOCKED_UNVERIFIED
```

- 이 ladder는 root `AGENTS.md`의 unreadable external-link blocker를 약화하지 않는다. 선언된 전용 reader와 허용 fallback을 소진하기 전에는 “현재 도구로 읽지 못함”이 확정되지 않았다는 source-specific 해석이다.
- 영상·오디오 자체를 자동 다운로드하거나 `yt-dlp`·ASR·새 패키지를 자동 설치하지 않는다. 별도 유료 transcript API·계정·credit를 기본 fallback으로 추가하지 않는다.
- 자막 전문은 local research evidence로만 다루고 repository에는 결정에 필요한 파생 요약·짧은 인용·timestamp·source identity만 남긴다.
- local transcript는 원 영상 binding과 생성 출처가 별도 검증되기 전 `UNVERIFIED`다. `TRANSCRIPT_READY_IS_NOT_FACT_OR_PROJECT_FIT_PASS`: caption ingest 성공도 발언의 사실성·프로젝트 적합성·Base 흡수 승인이 아니다.
- 내용 증거를 확보한 뒤 `PROJECT_REUSE_OPPORTUNITY_SCAN`과 현재 owner 비교로 `ADOPT / ADAPT / REJECT`를 판정한다. 제목·검색 스니펫·주변 자료를 본문 대신 사용하지 않는다.

'''

AI_LAYER_TABLE_ROW = "| AI solution layer selection (`AI_SOLUTION_LAYER_SELECTION`) | PLAN, BUILD, REVIEW; AI-assisted products and internal workflows | task evidence → simplest sufficient model/context/retrieval/tool/workflow-or-agent layer → harness evidence | cannot treat model training, current knowledge, MCP connectivity, agent autonomy, or AGI vocabulary as interchangeable proof | task-specific eval + source/provenance + exact integration/runtime evidence |\n"

AI_LAYER_CONTRACT = r'''## AI solution layer selection contract

`AI_SOLUTION_LAYER_SELECTION` prevents a familiar architecture error: treating every AI term as another feature that should be installed, or using one layer's success as proof that a different layer works. These are composable choices, not a mandatory maturity ladder.

```text
task failure and acceptance evidence
→ MODEL_AND_TRAINING_LAYER when base capability or learned behavior is the bottleneck
→ CONTEXT_AND_KNOWLEDGE_LAYER when instructions or current/private facts are the bottleneck
→ TOOL_AND_INTEGRATION_LAYER when the model must inspect or change external state
→ ORCHESTRATION_LAYER: deterministic workflow first, open-ended agent only when justified
→ HARNESS_LAYER for authority, context management, evals, state, recovery, evidence and cost control
→ HORIZON_VOCABULARY remains awareness-only
```

`DO_NOT_STACK_EVERY_LAYER_BY_DEFAULT`: select the smallest combination that closes the measured failure. A larger model, RAG, MCP, an agent and a new harness do not become one required bundle merely because all can appear in the same product.

### Layer and term boundaries

| Term | Operational role | Does not prove |
| --- | --- | --- |
| LLM | Parametric language/reasoning capability used by an application | current facts, project canon, tool access, or completed work |
| Multimodal model/input | Accepts and represents one or more declared modalities such as text, image, audio or video | accuracy on the exact task, cross-modal grounding quality, or runtime integration |
| RLHF and related preference post-training | Adjust learned behavior from demonstrations, preferences or reward signals | a live policy engine, current knowledge source, per-run approval, or factual correctness |
| Fine-tuning | Changes model behavior for measured recurring task patterns using curated training examples | automatic ingestion of changing company/project documents or a replacement for retrieval |
| Prompt and context engineering | Supplies goals, constraints, examples, current source material, history and tool results at inference time | durable model learning or source truth without readback and evaluation |
| Knowledge base | Stores and governs documents or structured facts under an owner | relevant retrieval, complete coverage, freshness, truth, or model access by itself |
| Retrieval/RAG | Selects external evidence and conditions generation on retrieved material | correct retrieval, authoritative sources, faithful synthesis, or a true answer by default |
| API/tool/MCP | Exposes typed external capabilities and context through an integration contract | agent autonomy, user approval, permission to mutate, successful action, or semantic correctness |
| Deterministic workflow | Runs a predefined, observable and testable sequence | good handling of unbounded unknown steps outside the declared path |
| Agent | Dynamically plans and uses tools from environment feedback for an open-ended goal | unrestricted autonomy, independent truth, or completion without external evidence |
| Harness | Composes instructions, context policy, tools, workflow/agent loop, state, evals, recovery, observability, evidence and cost controls around a model | that every component is necessary, current, secure, or effective without measurement |
| AGI/ASI | Horizon vocabulary for hypothetical broadly general or superhuman capability | a currently available component, delivery date, implementation plan, permission or completion state |

### Selection rules

1. `MODEL_CAPABILITY_IS_NOT_APPLICATION_ARCHITECTURE`: model capability and the application around it are separate evidence surfaces. Record the model/version and also test the actual input, tool, state and result path.
2. `MULTIMODAL_INPUT_IS_NOT_TASK_COMPETENCE`: accepting an image, audio track or video does not establish useful perception or reasoning for the target task. Test the exact modality, resolution/duration, language and required output.
3. `RLHF_IS_POST_TRAINING_NOT_RUNTIME_CONTROL`: RLHF is a post-training/alignment method. Runtime authority, project rules, safety gates and user approval remain application/harness responsibilities.
4. `EVAL_BEFORE_LAYER_ESCALATION` / `PROMPT_AND_CONTEXT_BEFORE_FINE_TUNING`: establish representative evals, then try clear instructions, examples and relevant context. Fine-tuning is justified only when a recurring learned-behavior gap remains and measured benefit repays data, training, versioning and maintenance cost.
5. `CURRENT_KNOWLEDGE_IS_NOT_FINE_TUNING_DEFAULT`: current, private or frequently changing facts should normally come from an authoritative source through bounded context or retrieval with provenance. Do not retrain merely to make a model read the latest project documents.
6. `KNOWLEDGE_BASE_IS_STORAGE_NOT_RETRIEVAL_OR_TRUTH`: define the canonical owner, scope, freshness and access boundary separately from indexing or search. A populated store can still be stale, incomplete, inaccessible or non-authoritative.
7. `RAG_RETRIEVES_EVIDENCE_BUT_DOES_NOT_GUARANTEE_TRUTH`: evaluate retrieval relevance, source freshness, provenance, authorization, missing evidence and answer faithfulness. Preserve a route from generated claims to the retrieved authoritative source.
8. `MCP_IS_INTEROPERABILITY_NOT_AGENT_AUTHORITY_OR_APPROVAL`: MCP standardizes context/tool interoperability and capability negotiation. The host authority, consent, project permissions, typed operation contract, readback and `MCP_CONNECTED_IS_NOT_BEHAVIOR_PASS` remain in force.
9. `DETERMINISTIC_WORKFLOW_BEFORE_OPEN_ENDED_AGENT`: use a fixed and testable path when steps and failure handling are predictable. Use an agent only for genuinely open-ended work requiring dynamic planning, and give it a bounded tool set, stopping condition, environment readback, recovery path and task-specific eval.
10. `HARNESS_IS_COMPOSED_CONTROL_AND_EVIDENCE_SYSTEM`: a harness is not one framework or wrapper. It is the composed system that makes model behavior usable and inspectable across authority, context, tools, orchestration, state, validation and recovery.
11. `HARNESS_COMPONENTS_REQUIRE_LOAD_BEARING_EVIDENCE` / `HARNESS_ABLATION_AND_PRUNING`: each extra prompt, memory layer, retriever, tool, reviewer, retry or coordinator must close a measured failure. Re-run ablation or equivalent baseline comparisons after an exact model/tool version change and remove components that no longer improve quality, reliability, cost or maintainability.
12. `MODEL_VS_HARNESS_IS_AN_EVAL_QUESTION`: do not assume either the model or the surrounding harness dominates in every task. Compare representative outcomes, interventions, latency, cost and failure recovery under equivalent inputs.
13. `AGI_ASI_AWARENESS_ONLY`: AGI/ASI discussion may inform long-range research awareness, but it cannot create an implementation feature, schedule assumption, budget, approval, permission, project scope or completion claim.
14. `NO_NEW_AI_GLOSSARY_OR_SKILL`: this section is a decision and composition route under the existing capability owner. It does not create a broad AI glossary, a new Skill, a provider dependency or automatic project adoption.

### Base mapping

`BASE_ALREADY_COMPOSES_A_HARNESS_NO_NEW_FRAMEWORK`: Base already composes repository instructions, progressive context loading, Skill/Tool routing, canonical owners, approvals, deterministic checks, runtime evidence, recovery and reporting. Improve the specific weak owner or consumer instead of installing a second generic “harness” authority.

Use this mapping when a new AI feature is proposed:

| Observed need | First candidate | Required proof before escalation |
| --- | --- | --- |
| New image/audio/video input | a model and adapter that explicitly support the modality | representative task eval and end-to-end input/result evidence |
| Inconsistent format or recurring behavior | eval → prompt/examples/context | repeated residual gap and fine-tuning cost/maintenance case |
| Current/private/changeable facts | authoritative source → bounded retrieval/context | coverage, freshness, provenance, access and faithful-answer eval |
| External inspection or mutation | typed API/tool/MCP adapter | exact capability, host authority, approval, result readback and rollback |
| Predictable repeated procedure | deterministic workflow | normal/failure/boundary tests and observable state transitions |
| Unknown steps that depend on environment feedback | bounded agent loop | sandboxed trials, stopping/recovery, compounding-error and cost evidence |
| Long-running reliability | minimal load-bearing harness components | exact model/tool version, state continuity, eval, recovery and ablation evidence |

Evidence ceilings:

```text
MODEL_SUPPORTS_MODALITY != PROJECT_TASK_PASS
RLHF_OR_FINE_TUNING != CURRENT_FACT_ACCESS
KNOWLEDGE_BASE_EXISTS != RELEVANT_RETRIEVAL
RAG_RETRIEVAL_SUCCESS != ANSWER_TRUE
MCP_CONNECTED != ACTION_AUTHORIZED_OR_SUCCEEDED
AGENT_COMPLETION_MESSAGE != VERIFIED_RESULT
HARNESS_EXISTS != EACH_COMPONENT_LOAD_BEARING
AGI_ASI_TERM != AVAILABLE_CAPABILITY
```

Primary comparison basis: OpenAI model-optimization guidance (evals → prompt/context → optional task-specific fine-tuning), Lewis et al. `arXiv:2005.11401` for parametric plus retrieved non-parametric memory, Anthropic's *Building Effective Agents* and *Effective context engineering for AI agents*, and the current Model Context Protocol architecture/specification. Recheck current primary documentation before provider-specific implementation because models, training surfaces and protocol details change.

'''


def run(command: list[str], log_name: str) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (EVIDENCE / log_name).write_text(result.stdout, encoding="utf-8")
    return result


def apply_owner_changes() -> None:
    intake = INTAKE_PATH.read_text(encoding="utf-8")
    intake_marker = "새 MCP·addon·CLI·framework·Skill·Mode·공용 실행 계층 요청은 일반 설계보다 먼저"
    if intake_marker not in intake:
        raise RuntimeError("intake insertion marker missing")
    INTAKE_PATH.write_text(
        intake.replace(intake_marker, PUBLIC_VIDEO_CONTRACT + intake_marker, 1),
        encoding="utf-8",
        newline="\n",
    )

    capability = CAPABILITY_PATH.read_text(encoding="utf-8")
    table_marker = "| AI game-engine machine boundary (`AI_GAME_ENGINE_MACHINE_BOUNDARY`)"
    section_marker = "## AI game-engine machine boundary contract"
    if table_marker not in capability or section_marker not in capability:
        raise RuntimeError("capability insertion marker missing")
    capability = capability.replace(table_marker, AI_LAYER_TABLE_ROW + table_marker, 1)
    capability = capability.replace(section_marker, AI_LAYER_CONTRACT + section_marker, 1)
    CAPABILITY_PATH.write_text(capability, encoding="utf-8", newline="\n")


def copy_candidate() -> None:
    destinations = {
        INTAKE_PATH: CANDIDATE / "skills/managing-project-intake-and-work-contract/SKILL.md",
        CAPABILITY_PATH: CANDIDATE / "docs/CAPABILITY_COMPOSITION_MAP.md",
        TEST_PATH: CANDIDATE / "tests/test_ai_solution_layer_selection_contract.py",
    }
    for source, destination in destinations.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def restore_candidate() -> None:
    shutil.copy2(
        CANDIDATE / "skills/managing-project-intake-and-work-contract/SKILL.md",
        INTAKE_PATH,
    )
    shutil.copy2(CANDIDATE / "docs/CAPABILITY_COMPOSITION_MAP.md", CAPABILITY_PATH)
    shutil.copy2(
        CANDIDATE / "tests/test_ai_solution_layer_selection_contract.py",
        TEST_PATH,
    )


def expect_mutation_failure(label: str, path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"mutation source missing: {label}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
    result = run(FOCUSED_COMMAND, f"{label}.log")
    with (EVIDENCE / "negative-controls.log").open("a", encoding="utf-8") as stream:
        stream.write(f"{label} exit={result.returncode}\n")
    if result.returncode == 0:
        raise RuntimeError(f"negative control unexpectedly passed: {label}")
    restore_candidate()


def write_final_artifacts() -> None:
    diff_result = subprocess.run(
        [
            "git",
            "diff",
            "--",
            str(INTAKE_PATH.relative_to(ROOT)),
            str(CAPABILITY_PATH.relative_to(ROOT)),
            str(TEST_PATH.relative_to(ROOT)),
        ],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if diff_result.returncode != 0:
        raise RuntimeError(diff_result.stdout)
    (CANDIDATE / "task.diff").write_text(diff_result.stdout, encoding="utf-8")

    digest_lines: list[str] = []
    for path in (
        CANDIDATE / "skills/managing-project-intake-and-work-contract/SKILL.md",
        CANDIDATE / "docs/CAPABILITY_COMPOSITION_MAP.md",
        CANDIDATE / "tests/test_ai_solution_layer_selection_contract.py",
        CANDIDATE / "task.diff",
    ):
        digest_lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(ROOT)}")
    (CANDIDATE / "sha256.txt").write_text("\n".join(digest_lines) + "\n", encoding="utf-8")

    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (CANDIDATE / "status.txt").write_text(status.stdout, encoding="utf-8")


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    CANDIDATE.mkdir(parents=True, exist_ok=True)
    test_text = TEST_SOURCE.read_text(encoding="utf-8").replace(
        "parents[2]", "parents[1]", 1
    )
    TEST_PATH.write_text(test_text, encoding="utf-8", newline="\n")

    red = run(FOCUSED_COMMAND, "red.log")
    (EVIDENCE / "red-status.txt").write_text(
        f"RED_EXIT={red.returncode}\n", encoding="utf-8"
    )
    if red.returncode == 0:
        raise RuntimeError("focused contract unexpectedly passed before owner changes")
    if "FAILED" not in red.stdout and "ERROR" not in red.stdout:
        raise RuntimeError("RED did not fail through the expected unittest path")

    apply_owner_changes()
    green = run(FOCUSED_COMMAND, "green.log")
    if green.returncode != 0:
        raise RuntimeError(green.stdout)
    public_video = run(PUBLIC_VIDEO_COMMAND, "public-video-regression.log")
    if public_video.returncode != 0:
        raise RuntimeError(public_video.stdout)

    compile_result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(TEST_PATH)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (EVIDENCE / "py-compile.log").write_text(compile_result.stdout, encoding="utf-8")
    if compile_result.returncode != 0:
        raise RuntimeError(compile_result.stdout)

    diff_check = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    (EVIDENCE / "diff-check.log").write_text(diff_check.stdout, encoding="utf-8")
    if diff_check.returncode != 0:
        raise RuntimeError(diff_check.stdout)

    copy_candidate()
    (EVIDENCE / "negative-controls.log").write_text("", encoding="utf-8")
    expect_mutation_failure(
        "mutation-video-route",
        INTAKE_PATH,
        "PUBLIC_VIDEO_SOURCE_RECOVERY_BEFORE_BLOCKER",
        "REMOVED_VIDEO_RECOVERY",
    )
    expect_mutation_failure(
        "mutation-rag-boundary",
        CAPABILITY_PATH,
        "RAG_RETRIEVES_EVIDENCE_BUT_DOES_NOT_GUARANTEE_TRUTH",
        "REMOVED_RAG_BOUNDARY",
    )
    expect_mutation_failure(
        "mutation-workflow-boundary",
        CAPABILITY_PATH,
        "DETERMINISTIC_WORKFLOW_BEFORE_OPEN_ENDED_AGENT",
        "REMOVED_WORKFLOW_BOUNDARY",
    )
    expect_mutation_failure(
        "mutation-harness-evidence",
        CAPABILITY_PATH,
        "HARNESS_COMPONENTS_REQUIRE_LOAD_BEARING_EVIDENCE",
        "REMOVED_HARNESS_EVIDENCE",
    )
    expect_mutation_failure(
        "mutation-horizon-boundary",
        CAPABILITY_PATH,
        "AGI_ASI_AWARENESS_ONLY",
        "REMOVED_HORIZON_BOUNDARY",
    )

    final_focused = run(FOCUSED_COMMAND, "final-focused.log")
    final_public_video = run(PUBLIC_VIDEO_COMMAND, "final-public-video.log")
    if final_focused.returncode != 0 or final_public_video.returncode != 0:
        raise RuntimeError("final restored candidate regression failed")

    final_diff_check = subprocess.run(
        ["git", "diff", "--check"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if final_diff_check.returncode != 0:
        raise RuntimeError(final_diff_check.stdout)

    write_final_artifacts()
    (CANDIDATE / "run-summary.json").write_text(
        json.dumps(
            {
                "baseline": "32f4dd5ba6042dc34611e2c8912f300b90491e0a",
                "red_exit": red.returncode,
                "focused_green": True,
                "public_video_regression": True,
                "negative_controls": 5,
                "diff_check": True,
                "claim_ceiling": "DOCUMENT_AND_ROUTING_CONTRACT_ONLY",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
