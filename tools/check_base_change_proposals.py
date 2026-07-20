from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


PROPOSAL_ROOT = "[수정제안서]"
REGISTRY_PATH = f"{PROPOSAL_ROOT}/PROPOSAL_REGISTRY.json"
APPROVED_STATES = {"APPROVED_FOR_IMPLEMENTATION"}
ACTIVE_PROPOSAL_STATES = {"SUBMITTED", "UNDER_REVIEW", "APPROVED_FOR_IMPLEMENTATION"}
REQUIRED_HEADINGS = (
    "## 출처와 상태",
    "## 관찰과 증거",
    "## 일반화 후보",
    "## 적용 조건과 비사용 조건",
    "## 반례와 위험",
    "## 영향 범위와 검증",
    "## 승인과 구현",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_repository(root: Path) -> tuple[dict, list[str]]:
    errors: list[str] = []
    registry_path = root / REGISTRY_PATH
    schema_path = root / "schemas/base-change-proposal-registry-v1.schema.json"
    if not registry_path.is_file():
        return {}, [f"missing proposal registry: {REGISTRY_PATH}"]
    registry = load_json(registry_path)
    schema = load_json(schema_path)
    for error in Draft202012Validator(schema).iter_errors(registry):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema {location}: {error.message}")

    seen: set[str] = set()
    for proposal in registry.get("proposals", []):
        proposal_id = proposal.get("proposal_id", "")
        if proposal_id in seen:
            errors.append(f"duplicate proposal_id: {proposal_id}")
        seen.add(proposal_id)
        if proposal.get("status") not in ACTIVE_PROPOSAL_STATES:
            errors.append(
                f"terminal proposal must not remain in the active registry: {proposal_id}"
            )
        path = root / proposal.get("path", "")
        expected = root / PROPOSAL_ROOT / proposal_id / "PROPOSAL.md"
        if path.resolve() != expected.resolve():
            errors.append(f"proposal path does not match id: {proposal_id}")
        if not path.is_file():
            errors.append(f"missing proposal file: {proposal.get('path')}")
            continue
        text = path.read_text(encoding="utf-8")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                errors.append(f"{proposal_id} missing heading: {heading}")
        if proposal.get("status") in APPROVED_STATES and not proposal.get("approval_ref"):
            errors.append(f"{proposal_id} requires approval_ref in {proposal.get('status')}")
        if proposal.get("status") == "IMPLEMENTED" and not proposal.get("implementation_pr"):
            errors.append(f"{proposal_id} requires implementation_pr when IMPLEMENTED")
    return registry, errors


def git_paths(root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
    )
    return [raw.decode("utf-8") for raw in result.stdout.split(b"\0") if raw]


def registry_at_ref(root: Path, base_ref: str) -> dict | None:
    listing = subprocess.run(
        ["git", "-C", str(root), "ls-tree", "-r", "-z", base_ref],
        check=True,
        capture_output=True,
    ).stdout
    blob_sha: str | None = None
    for raw_entry in listing.split(b"\0"):
        if not raw_entry:
            continue
        metadata, raw_path = raw_entry.split(b"\t", 1)
        if raw_path.decode("utf-8") == REGISTRY_PATH:
            blob_sha = metadata.decode("ascii").split()[2]
            break
    if blob_sha is None:
        return None
    content = subprocess.run(
        ["git", "-C", str(root), "cat-file", "-p", blob_sha],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout
    return json.loads(content)


def enforce_proposal_only_diff(current: dict, previous: dict | None, changed_files: list[str]) -> list[str]:
    if previous is None:
        return []  # Proposal-governance bootstrap PR.
    previous_ids = {item["proposal_id"] for item in previous.get("proposals", [])}
    new_items = [item for item in current.get("proposals", []) if item["proposal_id"] not in previous_ids]
    if not new_items:
        return []
    errors: list[str] = []
    for item in new_items:
        if item["status"] != "SUBMITTED":
            errors.append(f"new proposal must start as SUBMITTED: {item['proposal_id']}")
    outside = [path for path in changed_files if not path.startswith(f"{PROPOSAL_ROOT}/")]
    if outside:
        errors.append("new proposal PR changes active Base paths: " + ", ".join(outside))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Base change proposals and proposal-only PR boundaries.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--base-ref")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    registry, errors = validate_repository(root)
    if args.base_ref and registry:
        previous = registry_at_ref(root, args.base_ref)
        # NUL-delimited output disables core.quotePath escaping, so non-ASCII
        # proposal roots are compared as their actual UTF-8 paths on every OS.
        changed = git_paths(root, "diff", "--name-only", "-z", f"{args.base_ref}...HEAD")
        errors.extend(enforce_proposal_only_diff(registry, previous, changed))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(registry.get('proposals', []))} Base change proposal(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
