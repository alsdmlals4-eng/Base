#!/usr/bin/env python3
"""Run web-grounded daily Source analysis and render bounded repository evidence."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from datetime import date
from pathlib import Path

from tools.periodic_source_analysis_contract import (
    ANALYSIS_SCHEMA,
    REVIEW_SCHEMA,
    DEFAULT_BATCH_SIZE,
    DEFAULT_MODEL,
    AnalysisBlocked,
    build_context_request,
    build_research_request,
    build_review_request,
    collect_source_urls,
    deterministic_gate,
    extract_output_text,
    post_response,
    validate_analysis_packet,
    validate_review_packet,
)
from tools.periodic_source_analysis_render import render_scan_markdown
from tools.periodic_source_candidate_state import update_candidate_ledger
from tools.periodic_source_operations_state import update_operations_ledger
from tools.periodic_source_scan_queue import (
    load_ledger,
    parse_iso_date,
    select_due_source_batch,
)

__all__ = [
    "ANALYSIS_SCHEMA",
    "REVIEW_SCHEMA",
    "AnalysisBlocked",
    "build_context_request",
    "build_research_request",
    "build_review_request",
    "collect_source_urls",
    "deterministic_gate",
    "extract_output_text",
    "render_scan_markdown",
    "update_candidate_ledger",
    "update_operations_ledger",
    "validate_analysis_packet",
    "validate_review_packet",
]

Transport = Callable[[dict[str, object], str], dict[str, object]]
_SAFE_RUN_ID = re.compile(r"[^A-Za-z0-9._-]+")
_API_KEY_ENV = "OPENAI" + "_API_KEY"


def _safe_run_id(value: str) -> str:
    result = _SAFE_RUN_ID.sub("-", value).strip("-._")
    if not result or len(result) > 100:
        raise AnalysisBlocked("BLOCKED_PATH_SCOPE", "invalid run ID")
    return result


def _atomic_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="\n", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    temporary.replace(path)


def _write_json(path: Path, payload: Mapping[str, object]) -> None:
    _atomic_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _write_status(path: Path, state: str, **fields: object) -> None:
    payload: dict[str, object] = {"state": state}
    payload.update(fields)
    _write_json(path, payload)


def _parse_structured(response: Mapping[str, object], code: str) -> object:
    try:
        return json.loads(extract_output_text(response))
    except json.JSONDecodeError as error:
        raise AnalysisBlocked(code, "structured output was not valid JSON") from error


def _load_json_object(path: Path, code: str) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AnalysisBlocked(code, f"invalid JSON file: {path}") from error
    if not isinstance(payload, dict):
        raise AnalysisBlocked(code, f"JSON root must be an object: {path}")
    return payload


def run_analysis(
    *,
    operations_ledger_path: Path,
    candidate_ledger_path: Path,
    output_root: Path,
    run_date: date,
    run_id: str,
    model: str,
    batch_size: int,
    api_key: str,
    transport: Transport | None = None,
) -> dict[str, object]:
    if batch_size < 1 or batch_size > 20:
        raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "batch size must be between 1 and 20")
    safe_run_id = _safe_run_id(run_id)
    operations = load_ledger(operations_ledger_path)
    if "receipt_reconciliation_state" in operations:
        raise AnalysisBlocked(
            "BLOCKED_RECEIPT_RECONCILIATION_REQUIRED",
            "identity-enabled Operations Ledger must use reviewed receipt reconciliation before any model transport",
        )
    selected = select_due_source_batch(operations, run_date, batch_size)
    if not selected:
        return {"state": "NO_CHANGE", "detail": "No Source family is due."}

    caller = transport or post_response
    research_response = caller(
        build_research_request(selected, run_date, model=model), api_key
    )
    source_urls = collect_source_urls(research_response)
    research_digest = extract_output_text(research_response)

    context_response = caller(
        build_context_request(
            research_digest, source_urls, selected, run_date, model=model
        ),
        api_key,
    )
    selected_ids = {str(row["source_id"]) for row in selected}
    analysis = validate_analysis_packet(
        _parse_structured(context_response, "BLOCKED_CONTEXT_SCHEMA"),
        source_urls,
        selected_ids,
        run_date,
    )

    review_response = caller(
        build_review_request(analysis, source_urls, run_date, model=model), api_key
    )
    candidate_ids = {
        str(row["candidate_id"])
        for row in analysis["candidates"]
        if isinstance(row, dict)
    }
    review = validate_review_packet(
        _parse_structured(review_response, "BLOCKED_ADVERSARIAL_SCHEMA"),
        candidate_ids,
        run_date,
    )
    retained_ids = deterministic_gate(analysis, review, source_urls)
    retained_set = set(retained_ids)
    retained = [
        row
        for row in analysis["candidates"]
        if isinstance(row, dict) and row["candidate_id"] in retained_set
    ]

    candidate_ledger = update_candidate_ledger(
        _load_json_object(candidate_ledger_path, "BLOCKED_CONTEXT_SCHEMA"),
        analysis["new_source_candidates"],
        run_date,
    )
    updated_operations = update_operations_ledger(
        operations,
        set(analysis["scanned_sources"]),
        retained,
        run_date,
    )

    relative = Path(str(run_date.year), f"{run_date.month:02d}")
    base_name = f"{run_date.isoformat()}-{safe_run_id}"
    json_path = output_root / relative / f"{base_name}.json"
    markdown_path = output_root / relative / f"{base_name}.md"
    record = {
        "schema_version": 1,
        "record_role": "daily-source-context-analysis",
        "run_id": safe_run_id,
        "model": model,
        "source_urls": sorted(source_urls),
        "analysis": analysis,
        "adversarial_review": review,
        "retained_candidate_ids": retained_ids,
        "record_evidence_tier": "T6_AI_INFERENCE",
    }

    _write_json(json_path, record)
    _atomic_text(
        markdown_path,
        render_scan_markdown(
            analysis, review, retained_ids, model=model, run_id=safe_run_id
        ),
    )
    _write_json(operations_ledger_path, updated_operations)
    _write_json(candidate_ledger_path, candidate_ledger)
    return {
        "state": "READY_FOR_PR",
        "run_id": safe_run_id,
        "selected_source_ids": sorted(selected_ids),
        "scanned_source_ids": analysis["scanned_sources"],
        "retained_candidate_ids": retained_ids,
        "generated_paths": [
            str(json_path),
            str(markdown_path),
            str(operations_ledger_path),
            str(candidate_ledger_path),
        ],
    }


def main(argv: Sequence[str] | None = None, *, transport: Transport | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Analyze due external Sources through Evidence and adversarial gates."
    )
    parser.add_argument("--operations-ledger", type=Path, required=True)
    parser.add_argument("--candidate-ledger", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--date", dest="run_date", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--status-output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        run_date = parse_iso_date(args.run_date)
        if run_date is None:
            raise AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", "run date cannot be null")
        result = run_analysis(
            operations_ledger_path=args.operations_ledger,
            candidate_ledger_path=args.candidate_ledger,
            output_root=args.output_root,
            run_date=run_date,
            run_id=args.run_id,
            model=args.model,
            batch_size=args.batch_size,
            api_key=os.environ.get(_API_KEY_ENV, ""),
            transport=transport,
        )
        state = str(result.pop("state"))
        _write_status(args.status_output, state, **result)
        return 0
    except (ValueError, OSError) as error:
        blocked = AnalysisBlocked("BLOCKED_CONTEXT_SCHEMA", str(error))
        _write_status(args.status_output, blocked.code, detail=blocked.detail)
        print(str(blocked), file=sys.stderr)
        return 0
    except AnalysisBlocked as error:
        _write_status(args.status_output, error.code, detail=error.detail)
        print(str(error), file=sys.stderr)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
