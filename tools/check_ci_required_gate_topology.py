#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


CANONICAL_WORKFLOW = Path(".github/workflows/validate-game-project-operating-system.yml")
REQUIRED_GATE_NEEDS = (
    "classify-changes",
    "docs-validation",
    "core-regression",
    "ubuntu-contract",
    "publication-validation",
    "platform-smoke-windows",
)
REQUIRED_GATE_ENV = {
    "CLASSIFY_RESULT": "${{ needs.classify-changes.result }}",
    "DOCS_RESULT": "${{ needs.docs-validation.result }}",
    "CORE_REQUIRED": "${{ needs.classify-changes.outputs.run_core }}",
    "CORE_REGRESSION_RESULT": "${{ needs.core-regression.result }}",
    "CONTRACT_REQUIRED": "${{ needs.classify-changes.outputs.run_contract }}",
    "CONTRACT_RESULT": "${{ needs.ubuntu-contract.result }}",
    "PUBLICATION_REQUIRED": "${{ needs.classify-changes.outputs.run_publication }}",
    "PUBLICATION_RESULT": "${{ needs.publication-validation.result }}",
    "WINDOWS_REQUIRED": "${{ needs.classify-changes.outputs.run_windows }}",
    "WINDOWS_RESULT": "${{ needs.platform-smoke-windows.result }}",
}
TOPOLOGY_COMMAND = "python tools/check_ci_required_gate_topology.py"
EVALUATOR_COMMAND = "python tools/evaluate_ci_required_gate.py"
CHECKOUT_ACTION = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"


class AmbiguousYaml(ValueError):
    pass


@dataclass(frozen=True)
class MappingLine:
    indent: int
    key: str
    raw_value: str
    list_item: bool


def _line_indent(line: str) -> int | None:
    content = line.rstrip("\r\n")
    if not content.strip() or content.lstrip(" ").startswith("#"):
        return None
    if "\t" in content[: len(content) - len(content.lstrip())]:
        raise AmbiguousYaml("tab indentation is unsupported")
    return len(content) - len(content.lstrip(" "))


def _strip_comment(value: str) -> str:
    quote: str | None = None
    for index, character in enumerate(value):
        if quote:
            if character == quote:
                quote = None
            continue
        if character in "'\"":
            quote = character
        elif character == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.rstrip()


def _simple_key(raw_key: str, context: str) -> str:
    key = raw_key.strip()
    if key == "<<":
        raise AmbiguousYaml(f"{context}: merge key is unsupported")
    if not key:
        raise AmbiguousYaml(f"{context}: empty mapping key")
    if key[0] in "'\"":
        quote = key[0]
        if len(key) < 2 or key[-1] != quote:
            raise AmbiguousYaml(f"{context}: malformed quoted mapping key")
        inner = key[1:-1]
        if "\\" in inner or quote in inner:
            raise AmbiguousYaml(f"{context}: escaped quoted mapping key is unsupported")
        key = inner
    elif any(character in key for character in "{}[]&*!|>@?\"'"):
        raise AmbiguousYaml(f"{context}: advanced mapping key is unsupported")
    if not key or any(character.isspace() for character in key) or ":" in key:
        raise AmbiguousYaml(f"{context}: non-simple mapping key is unsupported")
    return key


def _simple_scalar(raw_value: str, context: str, *, allow_empty: bool = False) -> str:
    value = _strip_comment(raw_value.strip())
    if not value:
        if allow_empty:
            return ""
        raise AmbiguousYaml(f"{context}: empty scalar is unsupported")
    if value[0] in "'\"":
        quote = value[0]
        if len(value) < 2 or value[-1] != quote:
            raise AmbiguousYaml(f"{context}: malformed quoted scalar")
        inner = value[1:-1]
        if "\\" in inner or quote in inner:
            raise AmbiguousYaml(f"{context}: escaped quoted scalar is unsupported")
        return inner
    if value[0] in "|>&*![]{}@`" or value.startswith("<<"):
        raise AmbiguousYaml(f"{context}: advanced scalar is unsupported")
    return value


def _mapping_line(line: str, context: str) -> MappingLine | None:
    content = line.rstrip("\r\n")
    indent = _line_indent(content)
    if indent is None:
        return None
    stripped = content[indent:]
    list_item = False
    if stripped.startswith("- "):
        list_item = True
        stripped = stripped[2:].lstrip(" ")

    quote: str | None = None
    colon = -1
    for index, character in enumerate(stripped):
        if quote:
            if character == quote:
                quote = None
            continue
        if character in "'\"":
            quote = character
        elif character == ":":
            colon = index
            break
    if colon < 0:
        return None
    key = _simple_key(stripped[:colon], context)
    return MappingLine(indent, key, stripped[colon + 1 :].strip(), list_item)


def _entry_at(line: str, indent: int, context: str) -> MappingLine | None:
    line_indent = _line_indent(line)
    if line_indent != indent:
        return None
    return _mapping_line(line, context)


def _indented_block(text: str, header: str, indent: int, context: str) -> str | None:
    lines = text.splitlines(keepends=True)
    matches: list[int] = []
    for index, line in enumerate(lines):
        entry = _entry_at(line, indent, context)
        if entry is None or entry.list_item or entry.key != header:
            continue
        if _simple_scalar(entry.raw_value, context, allow_empty=True):
            raise AmbiguousYaml(f"{context}: {header} must use a block mapping")
        matches.append(index)
    if len(matches) > 1:
        raise AmbiguousYaml(f"{context}: duplicate protected mapping key {header!r}")
    if not matches:
        return None

    body: list[str] = []
    for candidate in lines[matches[0] + 1 :]:
        candidate_indent = _line_indent(candidate)
        if candidate_indent is not None and candidate_indent <= indent:
            break
        body.append(candidate)
    return "".join(body)


def _mapping_blocks(text: str, indent: int, context: str) -> list[tuple[str, str]]:
    lines = text.splitlines(keepends=True)
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        entry = _entry_at(line, indent, context)
        if entry is None:
            continue
        if entry.list_item:
            raise AmbiguousYaml(f"{context}: unexpected sequence entry")
        if _simple_scalar(entry.raw_value, context, allow_empty=True):
            raise AmbiguousYaml(f"{context}: flow or scalar job mapping is unsupported")
        starts.append((index, entry.key))

    blocks: list[tuple[str, str]] = []
    seen: set[str] = set()
    for position, (start, key) in enumerate(starts):
        if key in seen:
            raise AmbiguousYaml(f"{context}: duplicate mapping key {key!r}")
        seen.add(key)
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        blocks.append((key, "".join(lines[start + 1 : end])))
    return blocks


def _direct_values(text: str, indent: int, context: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        entry = _entry_at(line, indent, context)
        if entry is None:
            continue
        if entry.list_item:
            raise AmbiguousYaml(f"{context}: unexpected sequence entry")
        if entry.key in values:
            raise AmbiguousYaml(f"{context}: duplicate mapping key {entry.key!r}")
        values[entry.key] = entry.raw_value
    return values


def _scalar(values: dict[str, str], key: str, context: str) -> str | None:
    if key not in values:
        return None
    return _simple_scalar(values[key], f"{context}.{key}")


def _job_blocks(text: str, context: str) -> dict[str, str]:
    jobs = _indented_block(text, "jobs", 0, context)
    if jobs is None:
        return {}
    return dict(_mapping_blocks(jobs, 2, f"{context}.jobs"))


def _job_names(text: str, context: str) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for job_id, body in _job_blocks(text, context).items():
        values = _direct_values(body, 4, f"{context}.jobs.{job_id}")
        name = _scalar(values, "name", f"{context}.jobs.{job_id}")
        if name is not None:
            if "${{" in name:
                raise AmbiguousYaml(
                    f"{context}.jobs.{job_id}.name: "
                    "dynamic workflow job name is unsupported"
                )
            found.append((job_id, name))
    return found


def _sequence_blocks(text: str, indent: int, context: str) -> list[str]:
    lines = text.splitlines(keepends=True)
    starts: list[int] = []
    for index, line in enumerate(lines):
        entry = _entry_at(line, indent, context)
        if entry is None:
            continue
        if not entry.list_item:
            raise AmbiguousYaml(f"{context}: expected a sequence entry")
        starts.append(index)
    return [
        "".join(lines[start : starts[position + 1] if position + 1 < len(starts) else len(lines)])
        for position, start in enumerate(starts)
    ]


def _step_values(step: str, context: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in step.splitlines():
        line_indent = _line_indent(line)
        if line_indent not in {6, 8}:
            continue
        entry = _mapping_line(line, context)
        if entry is None or not (
            (entry.list_item and entry.indent == 6)
            or (not entry.list_item and entry.indent == 8)
        ):
            continue
        if entry.key in values:
            raise AmbiguousYaml(f"{context}: duplicate mapping key {entry.key!r}")
        values[entry.key] = entry.raw_value
    return values


def _needs(job: str, context: str) -> list[str]:
    values = _direct_values(job, 4, context)
    if values.get("needs", "").strip():
        return [_simple_scalar(values["needs"], f"{context}.needs")]
    block = _indented_block(job, "needs", 4, context)
    if block is None:
        return []
    found: list[str] = []
    for line in block.splitlines():
        indent = _line_indent(line)
        if indent is None:
            continue
        stripped = line[indent:]
        if indent != 6 or not stripped.startswith("- "):
            raise AmbiguousYaml(f"{context}.needs: only a simple block sequence is supported")
        found.append(_simple_scalar(stripped[2:], f"{context}.needs"))
    return found


def _has_unconditional_docs_topology_step(canonical_text: str, context: str) -> bool:
    docs_validation = _job_blocks(canonical_text, context).get("docs-validation")
    if docs_validation is None:
        return False
    job_context = f"{context}.jobs.docs-validation"
    job_values = _direct_values(docs_validation, 4, job_context)
    if "if" in job_values or "continue-on-error" in job_values:
        return False
    steps = _indented_block(docs_validation, "steps", 4, job_context)
    if steps is None:
        return False
    for index, step in enumerate(_sequence_blocks(steps, 6, f"{job_context}.steps")):
        step_context = f"{job_context}.steps[{index}]"
        values = _step_values(step, step_context)
        if "if" in values or "continue-on-error" in values or "shell" in values:
            continue
        run = _scalar(values, "run", step_context)
        if run == TOPOLOGY_COMMAND:
            return True
    return False


def _validate_canonical_gate(canonical_text: str, context: str) -> list[str]:
    errors: list[str] = []
    gate = _job_blocks(canonical_text, context).get("ci-gate")
    if gate is None:
        return ["canonical workflow must declare job ci-gate"]

    gate_context = f"{context}.jobs.ci-gate"
    job_values = _direct_values(gate, 4, gate_context)
    if _scalar(job_values, "name", gate_context) != "ci-gate":
        errors.append("canonical ci-gate job name must be ci-gate")
    if _scalar(job_values, "if", gate_context) != "always()":
        errors.append("canonical ci-gate job must use if: always()")
    if "continue-on-error" in job_values:
        errors.append("canonical ci-gate job must not declare continue-on-error")

    needs = _needs(gate, gate_context)
    if len(needs) != len(REQUIRED_GATE_NEEDS) or set(needs) != set(REQUIRED_GATE_NEEDS):
        errors.append(
            "canonical ci-gate dependencies must match exactly: "
            f"expected {list(REQUIRED_GATE_NEEDS)}, found {needs}"
        )

    steps = _indented_block(gate, "steps", 4, gate_context)
    if steps is None:
        errors.append("canonical ci-gate must have exactly two steps")
        errors.append("canonical ci-gate must checkout the repository first")
        errors.append("canonical ci-gate must execute the evaluator exactly once")
        return errors
    step_blocks = _sequence_blocks(steps, 6, f"{gate_context}.steps")
    step_values = [
        _step_values(step, f"{gate_context}.steps[{index}]")
        for index, step in enumerate(step_blocks)
    ]
    evaluator_count = sum(
        _scalar(values, "run", f"{gate_context}.steps[{index}]")
        == EVALUATOR_COMMAND
        for index, values in enumerate(step_values)
    )
    if evaluator_count != 1:
        errors.append("canonical ci-gate must execute the evaluator exactly once")
    if len(step_blocks) != 2:
        errors.append("canonical ci-gate must have exactly two steps")

    if not step_values:
        errors.append("canonical ci-gate must checkout the repository first")
        return errors

    checkout_context = f"{gate_context}.steps[0]"
    checkout_values = step_values[0]
    checkout_action = _scalar(checkout_values, "uses", checkout_context)
    if checkout_action is None:
        errors.append("canonical ci-gate must checkout the repository first")
    elif checkout_action != CHECKOUT_ACTION:
        errors.append("canonical ci-gate checkout must use the pinned action")
    if "if" in checkout_values or "continue-on-error" in checkout_values:
        errors.append("canonical ci-gate checkout must be unconditional and unmasked")
    if "run" in checkout_values or "shell" in checkout_values:
        errors.append("canonical ci-gate checkout step must only use the checkout action")

    if len(step_values) < 2:
        return errors
    step_context = f"{gate_context}.steps[1]"
    evaluate_values = step_values[1]
    run = _scalar(evaluate_values, "run", step_context)
    if run != EVALUATOR_COMMAND:
        errors.append("canonical ci-gate evaluator step must use the exact evaluator command")
    if "if" in evaluate_values or "continue-on-error" in evaluate_values:
        errors.append("canonical ci-gate evaluator step must be unconditional and unmasked")
    if "shell" in evaluate_values:
        errors.append("canonical ci-gate evaluator step must not declare a custom shell")
    if "uses" in evaluate_values:
        errors.append("canonical ci-gate evaluator step must use run, not uses")

    env = _indented_block(step_blocks[1], "env", 8, step_context)
    env_values: dict[str, str] = {}
    if env is not None:
        raw_env = _direct_values(env, 10, f"{step_context}.env")
        env_values = {
            key: _simple_scalar(value, f"{step_context}.env.{key}")
            for key, value in raw_env.items()
        }
    if env_values != REQUIRED_GATE_ENV:
        errors.append("canonical ci-gate environment mappings must match exactly")
    return errors


def validate_topology(root: Path) -> list[str]:
    workflow_root = root / ".github/workflows"
    workflows = sorted([*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml")])
    errors: list[str] = []
    named_gates: list[tuple[str, str]] = []
    ambiguous: set[Path] = set()
    for workflow in workflows:
        relative = workflow.relative_to(root).as_posix()
        text = workflow.read_text(encoding="utf-8")
        try:
            for job_id, job_name in _job_names(text, relative):
                if job_name == "ci-gate":
                    named_gates.append((relative, job_id))
        except AmbiguousYaml as error:
            ambiguous.add(workflow)
            errors.append(f"{relative}: ambiguous YAML in protected structure: {error}")
    if len(named_gates) != 1:
        errors.append(f"exactly one workflow job must be named ci-gate; found {named_gates}")
    elif named_gates[0] != (CANONICAL_WORKFLOW.as_posix(), "ci-gate"):
        errors.append(f"ci-gate must be owned by {CANONICAL_WORKFLOW.as_posix()} job ci-gate")

    canonical = root / CANONICAL_WORKFLOW
    if not canonical.is_file():
        errors.append(f"canonical workflow is missing: {CANONICAL_WORKFLOW.as_posix()}")
        return errors
    if canonical in ambiguous:
        return errors

    context = CANONICAL_WORKFLOW.as_posix()
    canonical_text = canonical.read_text(encoding="utf-8")
    try:
        on_block = _indented_block(canonical_text, "on", 0, context)
        pull_request = (
            _indented_block(on_block, "pull_request", 2, f"{context}.on")
            if on_block is not None
            else None
        )
        if on_block is None or pull_request is None:
            errors.append("canonical workflow must declare a pull_request trigger")
        else:
            trigger_keys = _direct_values(pull_request, 4, f"{context}.on.pull_request")
            if "paths" in trigger_keys or "paths-ignore" in trigger_keys:
                errors.append(
                    "canonical pull_request trigger must not declare paths or paths-ignore"
                )
        if not _has_unconditional_docs_topology_step(canonical_text, context):
            errors.append("canonical workflow must execute the Required Check topology checker")
        errors.extend(_validate_canonical_gate(canonical_text, context))
    except AmbiguousYaml as error:
        errors.append(f"{context}: ambiguous YAML in protected structure: {error}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_topology(args.root.resolve())
    if errors:
        print("CI REQUIRED GATE TOPOLOGY: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("CI REQUIRED GATE TOPOLOGY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
