#!/usr/bin/env python3
"""Select publishable design documents by Registry policy and invoke the v3 builder."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ACTIVE_STATUSES = {"ACTIVE", "CURRENT"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--include-milestone", action="store_true")
    parser.add_argument("--source-commit", default=os.environ.get("GITHUB_SHA", ""))
    parser.add_argument("--human-visual-review", default="NOT_RUN", choices=["NOT_RUN", "PASSED", "FAILED"])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    return parser.parse_args()


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 3:
        raise ValueError(f"Schema v3 design document registry is required: {path}")
    return data


def select_documents(registry: dict[str, Any], selected: set[str], include_milestone: bool) -> list[dict[str, Any]]:
    documents = [
        item for item in registry.get("documents", [])
        if isinstance(item, dict) and item.get("status") in ACTIVE_STATUSES
    ]
    available = {str(item.get("document_id")): item for item in documents}
    missing = sorted(selected - set(available))
    if missing:
        raise ValueError(f"Requested active document_id not found: {', '.join(missing)}")
    source_only = sorted(
        document_id for document_id in selected
        if available[document_id].get("publication_policy") == "source_only"
    )
    if source_only:
        raise ValueError(f"source_only documents have no publication output: {', '.join(source_only)}")
    result = []
    for item in documents:
        policy = item.get("publication_policy")
        document_id = str(item.get("document_id"))
        if selected:
            if document_id in selected:
                result.append(item)
            continue
        if policy == "always_sync" or (policy == "milestone_sync" and include_milestone):
            result.append(item)
    return result


def main() -> int:
    options = parse_args()
    registry_path = Path(options.registry).resolve()
    registry = load_registry(registry_path)
    chosen = select_documents(registry, set(options.only), options.include_milestone)
    if not chosen:
        print("No design documents are eligible for publication under the selected policy.")
        return 0
    filtered = dict(registry)
    filtered["documents"] = chosen
    example = filtered.get("document_contract_example")
    if isinstance(example, dict) and example.get("publication_policy") == "source_only":
        filtered["document_contract_example"] = chosen[0]
    builder = Path(__file__).with_name("build_design_documents.py")
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".json",
        prefix=".publication-registry-",
        dir=registry_path.parent,
        delete=False,
    ) as stream:
        json.dump(filtered, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
        temporary_registry = Path(stream.name)
    command = [sys.executable, str(builder), "--registry", str(temporary_registry)]
    if options.source_commit:
        command += ["--source-commit", options.source_commit]
    if options.human_visual_review != "NOT_RUN":
        command += ["--human-visual-review", options.human_visual_review]
    if options.force:
        command.append("--force")
    if options.preflight:
        command.append("--preflight")
    try:
        completed = subprocess.run(command, cwd=builder.parent.parent, check=False)
        return completed.returncode
    finally:
        temporary_registry.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
