#!/usr/bin/env python3
"""Fail-closed publication gate for a human Blueprint progress snapshot."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from human_blueprint_incremental_revision import validate_blueprint_revision
from human_blueprint_progress_projection import render_projection
from human_blueprint_progress_projection_validation import validate_projection


def validate_publication_projection(
    projection: dict[str, Any],
    *,
    expected_source_sha: str | None = None,
) -> list[str]:
    """Validate progress facts and the predecessor-to-successor revision receipt."""
    errors = validate_projection(
        projection,
        expected_source_sha=expected_source_sha,
    )
    errors.extend(validate_blueprint_revision(projection))
    return errors


def _md(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def _render_revision(projection: dict[str, Any]) -> str:
    revision = projection["blueprint_revision"]
    mode = revision["revision_mode"]
    predecessor_ref = revision.get("predecessor_blueprint_ref") or (
        "N/A — INITIAL_CREATION_NO_VALID_PREDECESSOR"
    )
    predecessor_source = revision.get("predecessor_source_commit") or "N/A"
    lines = [
        "## Blueprint 증분 수정·보존",
        "",
        "`BLUEPRINT_LOSS_REGRESSION_GATE: PASS`",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        f"| revision mode | `{_md(mode)}` |",
        f"| predecessor Blueprint | {_md(predecessor_ref)} |",
        f"| predecessor source commit | `{_md(predecessor_source)}` |",
        f"| successor source commit | `{_md(projection['source_main_sha'])}` |",
        "| publication status | `READY` |",
        "",
        "### Semantic delta",
    ]
    lines.extend(f"- {_md(item)}" for item in revision["semantic_delta_summary"])
    justifications = revision["removal_or_downgrade_justifications"]
    lines.extend(["", "### 삭제·대체·상태 하향 기록"])
    if not justifications:
        lines.append("- 없음 — predecessor의 선언된 내용과 상태가 유지됨")
    else:
        for item in justifications:
            replacements = ", ".join(item["replacement_refs"]) or "없음"
            lines.append(
                "- `"
                + _md(item["change_key"])
                + "` — "
                + _md(item["change_type"])
                + "; reason: "
                + _md(item["reason"])
                + "; replacement: "
                + _md(replacements)
                + "; verification impact: "
                + _md(item["verification_impact"])
            )
    return "\n".join(lines)


def render_publication_projection(
    projection: dict[str, Any],
    *,
    expected_source_sha: str | None = None,
) -> str:
    """Render the revision receipt and progress view only after all gates pass."""
    errors = validate_publication_projection(
        projection,
        expected_source_sha=expected_source_sha,
    )
    if errors:
        raise ValueError("; ".join(errors))
    progress = render_projection(
        projection,
        expected_source_sha=expected_source_sha,
    )
    return _render_revision(projection) + "\n\n" + progress


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError("input root must be an object")
    return value


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate the current progress projection and its lossless "
            "incremental Blueprint revision receipt."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--expected-source-sha", required=True)
    parser.add_argument("--render-markdown", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        projection = _load(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"HUMAN BLUEPRINT INCREMENTAL PUBLICATION: FAIL\n- {exc}")
        return 2

    errors = validate_publication_projection(
        projection,
        expected_source_sha=args.expected_source_sha,
    )
    if errors:
        print("HUMAN BLUEPRINT INCREMENTAL PUBLICATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("HUMAN BLUEPRINT INCREMENTAL PUBLICATION: PASS")
    if args.render_markdown:
        print()
        print(
            render_publication_projection(
                projection,
                expected_source_sha=args.expected_source_sha,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
