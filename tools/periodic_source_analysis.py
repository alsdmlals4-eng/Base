#!/usr/bin/env python3
"""Public interface for the daily Source context-analysis pipeline."""

from tools.periodic_source_analysis_contract import (
    ANALYSIS_SCHEMA,
    REVIEW_SCHEMA,
    AnalysisBlocked,
    build_context_request,
    build_research_request,
    build_review_request,
    collect_source_urls,
    deterministic_gate,
    extract_output_text,
    validate_analysis_packet,
    validate_review_packet,
)
from tools.periodic_source_analysis_render import render_scan_markdown
from tools.periodic_source_candidate_state import update_candidate_ledger
from tools.periodic_source_operations_state import update_operations_ledger

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


def main() -> int:
    from tools.periodic_source_analysis_runner import main as runner_main

    return runner_main()


if __name__ == "__main__":
    raise SystemExit(main())
