from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas/project-integration-capsule-v1.schema.json"
CANONICAL_ADAPTER_PATH = "skills/PROJECT_BASE_ADAPTER.json"
ZERO_SHA40 = "0" * 40
REQUIRED_ALLOWED_SERVICE_CLASSES = {
    "GPT_PRO",
    "NOTION_FREE",
    "LOCAL_OPEN_SOURCE_TOOLS",
}
ALLOWED_SERVICE_CLASSES = REQUIRED_ALLOWED_SERVICE_CLASSES | {"GITHUB_FREE_OR_INCLUDED"}
REQUIRED_PROHIBITED_METERED_SERVICES = {
    "OPENAI_API_PAYG",
    "PAID_CI_RUNNER",
    "PAID_NOTION_AI",
    "PAID_REMOTE_HOSTING",
}
REQUIRED_GODOT_FORBIDDEN_PATHS = {
    "project.godot",
    "**/*.gd",
    "**/*.tscn",
    "**/*.tres",
    "**/*.res",
    "**/*.scn",
}
ALLOWED_GODOT_CACHE_PREFIXES = (
    ".godot/editor/",
    ".godot/imported/",
    ".godot/shader_cache/",
)
ALLOWED_GODOT_CACHE_FILES = {
    ".godot/.gdignore",
    ".godot/extension_list.cfg",
    ".godot/global_script_class_cache.cfg",
    ".godot/scene_groups_cache.cfg",
    ".godot/uid_cache.bin",
}
GODOT_AUTHORING_OR_EXECUTABLE_SUFFIXES = {
    ".cs",
    ".dll",
    ".gd",
    ".gdextension",
    ".gdnlib",
    ".gdshader",
    ".pck",
    ".res",
    ".scn",
    ".so",
    ".tscn",
    ".tres",
    ".wasm",
}


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object")
    return value


def _sha256(path: Path) -> str | None:
    try:
        payload = path.read_bytes()
    except OSError:
        return None
    return hashlib.sha256(payload).hexdigest()


def _safe_child(root: Path, relative: str) -> Path | None:
    if not isinstance(relative, str) or "\x00" in relative:
        return None
    normalized = relative.replace("\\", "/")
    if normalized.startswith("/") or any(part == ".." for part in normalized.split("/")):
        return None
    try:
        resolved_root = root.resolve()
        candidate = (resolved_root / normalized).resolve()
        candidate.relative_to(resolved_root)
    except (OSError, ValueError):
        return None
    return candidate


def _git_environment() -> dict[str, str]:
    environment = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("GIT_")
    }
    environment.update(
        {
            "GIT_NO_LAZY_FETCH": "1",
            "GIT_OPTIONAL_LOCKS": "0",
            "GIT_TERMINAL_PROMPT": "0",
        }
    )
    return environment


def _git_command(root: Path, *args: str) -> list[str]:
    return [
        "git",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.untrackedCache=false",
        "-C",
        str(root),
        *args,
    ]


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    command = _git_command(root, *args)
    try:
        return subprocess.run(
            command,
            text=True,
            encoding="utf-8",
            errors="surrogateescape",
            capture_output=True,
            check=False,
            env=_git_environment(),
        )
    except OSError as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def _git_show_bytes(root: Path, commit: str, relative: str) -> bytes | None:
    command = _git_command(root, "show", f"{commit}:{relative}")
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            check=False,
            env=_git_environment(),
        )
    except OSError:
        return None
    return completed.stdout if completed.returncode == 0 else None


def _github_repository_slug(remote_url: str) -> str | None:
    candidate = remote_url.strip()
    if candidate.startswith("git@github.com:"):
        path = candidate.removeprefix("git@github.com:")
    else:
        parsed = urlparse(candidate)
        if parsed.hostname != "github.com":
            return None
        path = parsed.path.lstrip("/")
    if path.endswith(".git"):
        path = path[:-4]
    parts = path.split("/")
    if len(parts) != 2 or not all(parts):
        return None
    return "/".join(parts)


def _is_rfc3339(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
        r"(?:[Zz]|[+-]\d{2}:\d{2})",
        value,
    ):
        return False
    try:
        normalized = value[:-1] + "+00:00" if value[-1] in "Zz" else value
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _path_exists_at_commit(root: Path, commit: str, relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    return _git(root, "cat-file", "-e", f"{commit}:{normalized}").returncode == 0


def _blob_objects_available(root: Path, object_ids: list[str]) -> bool:
    if not object_ids:
        return True
    try:
        completed = subprocess.run(
            _git_command(
                root,
                "cat-file",
                "--batch-check=%(objectname) %(objecttype)",
            ),
            input=("\n".join(object_ids) + "\n").encode("ascii"),
            capture_output=True,
            check=False,
            env=_git_environment(),
        )
    except OSError:
        return False
    if completed.returncode:
        return False
    try:
        observed = completed.stdout.decode("ascii").splitlines()
    except UnicodeError:
        return False
    expected = [f"{object_id} blob" for object_id in object_ids]
    return observed == expected


def _git_blob_oid(path: Path, algorithm: str, expected_size: int) -> str | None:
    try:
        digest = hashlib.new(algorithm)
    except ValueError:
        return None
    digest.update(f"blob {expected_size}\0".encode("ascii"))
    observed_size = 0
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(1024 * 1024):
                observed_size += len(chunk)
                digest.update(chunk)
    except OSError:
        return None
    if observed_size != expected_size:
        return None
    return digest.hexdigest()


def _parse_tree_entries(output: str) -> dict[str, tuple[str, str, str]] | None:
    entries: dict[str, tuple[str, str, str]] = {}
    for record in output.split("\0"):
        if not record:
            continue
        try:
            metadata, relative = record.split("\t", 1)
            mode, object_type, object_id = metadata.split(" ", 2)
        except ValueError:
            return None
        if relative in entries:
            return None
        entries[relative] = (mode, object_type, object_id)
    return entries


def _parse_index_entries(output: str) -> dict[str, list[tuple[str, str, str]]] | None:
    entries: dict[str, list[tuple[str, str, str]]] = {}
    for record in output.split("\0"):
        if not record:
            continue
        try:
            metadata, relative = record.split("\t", 1)
            mode, object_id, stage = metadata.split(" ", 2)
        except ValueError:
            return None
        entries.setdefault(relative, []).append((mode, object_id, stage))
    return entries


def _raw_snapshot_findings(root: Path, commit: str) -> list[Finding]:
    findings: list[Finding] = []
    tree_result = _git(root, "ls-tree", "-r", "-z", "--full-tree", commit)
    tree_entries = (
        _parse_tree_entries(tree_result.stdout) if tree_result.returncode == 0 else None
    )
    if tree_entries is None:
        return [
            Finding(
                "TRACKED_SNAPSHOT_UNREADABLE",
                "/change_boundary/unexpected_tracked_diff",
                "Cannot enumerate the exact committed tree without filters.",
            )
        ]

    object_format_result = _git(root, "rev-parse", "--show-object-format")
    object_format = object_format_result.stdout.strip()
    if object_format_result.returncode or object_format not in {"sha1", "sha256"}:
        return [
            Finding(
                "GIT_OBJECT_FORMAT_UNSUPPORTED",
                "/change_boundary/unexpected_tracked_diff",
                "Cannot identify a supported Git object hash format.",
            )
        ]

    blob_object_ids = sorted(
        object_id
        for mode, object_type, object_id in tree_entries.values()
        if mode not in {"160000", "120000"} and object_type == "blob"
    )
    if not _blob_objects_available(root, blob_object_ids):
        findings.append(
            Finding(
                "TRACKED_OBJECT_UNAVAILABLE",
                "/change_boundary/unexpected_tracked_diff",
                "One or more committed blobs are unavailable with lazy fetch disabled.",
            )
        )

    index_result = _git(root, "ls-files", "--stage", "-z")
    index_entries = (
        _parse_index_entries(index_result.stdout) if index_result.returncode == 0 else None
    )
    expected_index = {
        relative: [(mode, object_id, "0")]
        for relative, (mode, _object_type, object_id) in tree_entries.items()
    }
    if index_entries is None:
        findings.append(
            Finding(
                "INDEX_TREE_UNREADABLE",
                "/change_boundary/unexpected_tracked_diff",
                "Cannot enumerate the Git index for exact tree comparison.",
            )
        )
    elif index_entries != expected_index:
        findings.append(
            Finding(
                "INDEX_TREE_MISMATCH",
                "/change_boundary/unexpected_tracked_diff",
                "The Git index does not exactly match result_sha.",
            )
        )

    gitlinks = sorted(
        relative
        for relative, (mode, object_type, _object_id) in tree_entries.items()
        if mode == "160000" or object_type == "commit"
    )
    if gitlinks:
        findings.append(
            Finding(
                "GITLINK_UNSUPPORTED",
                "/change_boundary/unexpected_tracked_diff",
                "Read-only v1 does not verify submodule worktrees: " + ", ".join(gitlinks),
            )
        )

    symlinks = sorted(
        relative
        for relative, (mode, object_type, _object_id) in tree_entries.items()
        if mode == "120000" and object_type == "blob"
    )
    if symlinks:
        findings.append(
            Finding(
                "SYMLINK_UNSUPPORTED",
                "/change_boundary/unexpected_tracked_diff",
                "Read-only v1 does not follow tracked symlinks: " + ", ".join(symlinks),
            )
        )

    raw_mismatch = False
    for relative, (mode, object_type, object_id) in tree_entries.items():
        if mode in {"160000", "120000"} or object_type != "blob":
            continue
        worktree_path = _safe_child(root, relative)
        if worktree_path is None:
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_TYPE_MISMATCH",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Tracked path cannot be read as a confined regular file: {relative}.",
                )
            )
            continue
        try:
            observed_stat = worktree_path.lstat()
        except OSError as error:
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_UNREADABLE",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Cannot stat tracked file {relative}: {error}",
                )
            )
            continue
        if not stat.S_ISREG(observed_stat.st_mode):
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_TYPE_MISMATCH",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Tracked blob is not a regular worktree file: {relative}.",
                )
            )
            continue
        expected_executable = mode == "100755"
        observed_executable = bool(observed_stat.st_mode & 0o111)
        if os.name != "nt" and observed_executable != expected_executable:
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_MODE_MISMATCH",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Worktree executable mode differs from result_sha for {relative}.",
                )
            )
        observed_object_id = _git_blob_oid(
            worktree_path,
            object_format,
            observed_stat.st_size,
        )
        if observed_object_id is None:
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_UNREADABLE",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Cannot hash tracked file as raw Git blob bytes: {relative}.",
                )
            )
            continue
        if observed_object_id != object_id:
            raw_mismatch = True
            findings.append(
                Finding(
                    "TRACKED_FILE_BYTES_MISMATCH",
                    "/change_boundary/unexpected_tracked_diff",
                    f"Raw worktree bytes differ from result_sha for {relative}.",
                )
            )

    if raw_mismatch or index_entries is None or index_entries != expected_index:
        findings.append(
            Finding(
                "TRACKED_WORKTREE_DIRTY",
                "/change_boundary/unexpected_tracked_diff",
                "Tracked project bytes or index entries differ from result_sha.",
            )
        )
    return findings


def _is_exact_release_or_commit(value: Any) -> bool:
    if not isinstance(value, str) or value != value.strip():
        return False
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/@+-]{0,127}", value):
        return False
    return value.casefold() not in {
        "not_configured",
        "latest",
        "head",
        "main",
        "master",
        "develop",
        "development",
        "stable",
        "nightly",
        "canary",
        "dev",
    }


def _is_allowed_generated_godot_cache(relative: str) -> bool:
    normalized = relative.replace("\\", "/")
    suffix = Path(normalized).suffix.casefold()
    if suffix in GODOT_AUTHORING_OR_EXECUTABLE_SUFFIXES:
        return False
    return normalized in ALLOWED_GODOT_CACHE_FILES or normalized.startswith(
        ALLOWED_GODOT_CACHE_PREFIXES
    )


def _schema_findings(payload: dict[str, Any]) -> list[Finding]:
    schema = _load_json(SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(payload),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    return [
        Finding(
            "SCHEMA_INVALID",
            "/" + "/".join(str(part) for part in error.absolute_path),
            error.message,
        )
        for error in errors
    ]


def validate_capsule(
    capsule_path: Path,
    *,
    project_root: Path | None = None,
    schema_only: bool = False,
) -> list[Finding]:
    try:
        payload = _load_json(capsule_path)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        return [Finding("CAPSULE_UNREADABLE", "/", str(error))]

    findings = _schema_findings(payload)
    adapter_binding_for_path = payload.get("base_adapter")
    declared_adapter_path = (
        adapter_binding_for_path.get("path")
        if isinstance(adapter_binding_for_path, dict)
        else None
    )
    if isinstance(declared_adapter_path, str) and declared_adapter_path != CANONICAL_ADAPTER_PATH:
        findings.append(
            Finding(
                "NONCANONICAL_BASE_ADAPTER_PATH",
                "/base_adapter/path",
                f"Base adapter must use the canonical path {CANONICAL_ADAPTER_PATH}.",
            )
        )
    if findings or schema_only:
        return findings

    if payload["status"] == "TEMPLATE_NOT_CONFIGURED":
        return [
            Finding(
                "CAPSULE_NOT_CONFIGURED",
                "/status",
                "The template is structurally valid but cannot be used as read-only integration evidence.",
            )
        ]

    if payload["status"] != "READ_ONLY_BINDING_VERIFIED":
        findings.append(
            Finding(
                "CAPSULE_STATUS_NOT_READY",
                "/status",
                "Only READ_ONLY_BINDING_VERIFIED may pass the local receipt-binding gate.",
            )
        )

    project = payload["project"]
    decision = payload["decision"]
    notion = payload["notion"]
    codex = payload["codex"]
    godot = payload["godot"]
    cost = payload["cost_surface"]
    reality = payload["reality_gate"]

    if decision["approval_status"] != "APPROVED":
        findings.append(
            Finding(
                "DECISION_UNAPPROVED",
                "/decision/approval_status",
                "Receipt binding requires an explicitly approved Decision record.",
            )
        )

    if notion["project_relation_count"] != 1:
        findings.append(
            Finding(
                "NOTION_PROJECT_RELATION_REQUIRED",
                "/notion/project_relation_count",
                "Exactly one Notion Project relation is required.",
            )
        )
    expected_prefix = f'{notion["project_key"]}::'
    if not notion["record_key"].startswith(expected_prefix):
        findings.append(
            Finding(
                "NOTION_PROJECT_MISMATCH",
                "/notion/record_key",
                "Record Key must be scoped by the exact Notion Project Key.",
            )
        )
    record_key_parts = notion["record_key"].split("::")
    if len(record_key_parts) != 3 or any(not part for part in record_key_parts):
        findings.append(
            Finding(
                "NOTION_RECORD_KEY_INVALID",
                "/notion/record_key",
                "Record Key must be <ProjectKey>::<RecordType>::<LocalId>.",
            )
        )
    if notion["revision"] < 1 or notion["readback_status"] != "PASS":
        findings.append(
            Finding(
                "NOTION_READBACK_UNVERIFIED",
                "/notion",
                "Receipt binding requires revision metadata and destination readback PASS.",
            )
        )
    if not _is_rfc3339(notion["last_edited"]):
        findings.append(
            Finding(
                "NOTION_LAST_EDITED_INVALID",
                "/notion/last_edited",
                "Receipt binding requires a timezone-qualified RFC3339 Last Edited value.",
            )
        )

    if codex["godot_direct_write"] != "FORBIDDEN":
        findings.append(
            Finding(
                "SECOND_GODOT_WRITER",
                "/codex/godot_direct_write",
                "Codex filesystem writes to Godot authority paths would create a second writer.",
            )
        )
    if godot["direct_filesystem_write_enforcement"] != "PASS":
        findings.append(
            Finding(
                "WRITER_EXCLUSIVITY_UNVERIFIED",
                "/godot/direct_filesystem_write_enforcement",
                "The path-level second-writer canary has not passed.",
            )
        )

    allowed_service_classes = set(cost["allowed_service_classes"])
    prohibited_metered_services = set(cost["prohibited_metered_services"])
    if (
        cost["status"] != "DECLARED_ZERO_INCREMENTAL_COST_POLICY"
        or not REQUIRED_ALLOWED_SERVICE_CLASSES.issubset(allowed_service_classes)
        or not allowed_service_classes.issubset(ALLOWED_SERVICE_CLASSES)
        or prohibited_metered_services != REQUIRED_PROHIBITED_METERED_SERVICES
    ):
        findings.append(
            Finding(
                "COST_GATE_BLOCKED",
                "/cost_surface",
                "The declared cost policy must allow only included/free classes and explicitly prohibit metered services.",
            )
        )

    change_boundary = payload["change_boundary"]
    if not REQUIRED_GODOT_FORBIDDEN_PATHS.issubset(
        set(change_boundary["codex_forbidden_godot_paths"])
    ):
        findings.append(
            Finding(
                "CHANGE_BOUNDARY_INCOMPLETE",
                "/change_boundary/codex_forbidden_godot_paths",
                "The read-only boundary must deny every canonical Godot authoring path class.",
            )
        )
    if change_boundary["unexpected_tracked_diff"] != "PASS":
        findings.append(
            Finding(
                "CHANGE_BOUNDARY_UNVERIFIED",
                "/change_boundary/unexpected_tracked_diff",
                "Receipt binding requires an observed tracked-diff PASS.",
            )
        )

    evidence_by_id: dict[str, dict[str, Any]] = {}
    evidence_kind_counts: dict[str, int] = {}
    for index, evidence in enumerate(payload["evidence"]):
        evidence_id = evidence["evidence_id"]
        if evidence_id in evidence_by_id:
            findings.append(
                Finding(
                    "DUPLICATE_EVIDENCE_ID",
                    f"/evidence/{index}/evidence_id",
                    f"Duplicate evidence ID: {evidence_id}",
                )
            )
        evidence_by_id[evidence_id] = evidence
        evidence_kind_counts[evidence["kind"]] = evidence_kind_counts.get(evidence["kind"], 0) + 1
        expected_level = {
            "NOTION_READBACK": "E3_RUNTIME",
            "WRITER_EXCLUSIVITY_CANARY": "E2_TEST",
        }.get(evidence["kind"])
        if expected_level is not None and evidence["level"] != expected_level:
            findings.append(
                Finding(
                    "EVIDENCE_LEVEL_MISMATCH",
                    f"/evidence/{index}/level",
                    f"{evidence['kind']} requires {expected_level} evidence.",
                )
            )

    acceptance_ids: set[str] = set()
    mapped_evidence_ids: set[str] = set()
    for index, acceptance in enumerate(payload["acceptance"]):
        if acceptance["acceptance_id"] in acceptance_ids:
            findings.append(
                Finding(
                    "DUPLICATE_ACCEPTANCE_ID",
                    f"/acceptance/{index}/acceptance_id",
                    f"Duplicate acceptance ID: {acceptance['acceptance_id']}",
                )
            )
        acceptance_ids.add(acceptance["acceptance_id"])
        if acceptance["status"] != "PASS":
            findings.append(
                Finding(
                    "ACCEPTANCE_NOT_PASS",
                    f"/acceptance/{index}/status",
                    f'Acceptance {acceptance["acceptance_id"]} is not PASS.',
                )
                )
        if not acceptance["evidence_ids"]:
            findings.append(
                Finding(
                    "ACCEPTANCE_EVIDENCE_MISSING",
                    f"/acceptance/{index}/evidence_ids",
                    f"Acceptance {acceptance['acceptance_id']} has no evidence.",
                )
            )
        for evidence_id in acceptance["evidence_ids"]:
            mapped_evidence_ids.add(evidence_id)
            if evidence_id not in evidence_by_id:
                findings.append(
                    Finding(
                        "UNMAPPED_EVIDENCE",
                        f"/acceptance/{index}/evidence_ids",
                        f"Unknown evidence ID: {evidence_id}",
                    )
                )

    for required_kind in ("NOTION_READBACK", "WRITER_EXCLUSIVITY_CANARY"):
        if evidence_kind_counts.get(required_kind, 0) != 1:
            findings.append(
                Finding(
                    "REQUIRED_EVIDENCE_CARDINALITY",
                    "/evidence",
                    f"Receipt binding requires exactly one {required_kind} receipt.",
                )
            )

    required_evidence_ids = {
        evidence["evidence_id"]
        for evidence in payload["evidence"]
        if evidence["kind"] in {"NOTION_READBACK", "WRITER_EXCLUSIVITY_CANARY"}
    }
    if not required_evidence_ids.issubset(mapped_evidence_ids):
        findings.append(
            Finding(
                "ORPHAN_REQUIRED_EVIDENCE",
                "/acceptance",
                "Every required receipt must support at least one PASS acceptance.",
            )
        )

    expected_reality = {
        "exact_head": "PASS",
        "notion_readback": "PASS",
        "godot_import": "NOT_APPLICABLE",
        "writer_exclusivity": "PASS",
        "rollback_drill": "NOT_APPLICABLE",
        "final_status": "READ_ONLY_BINDING_VERIFIED",
    }
    for field, expected in expected_reality.items():
        if reality[field] != expected:
            findings.append(
                Finding(
                    "REALITY_GATE_NOT_READY",
                    f"/reality_gate/{field}",
                    f"Expected {expected}, observed {reality[field]}.",
                )
            )

    if payload["rollback"]["drill_status"] != "NOT_APPLICABLE":
        findings.append(
            Finding(
                "ROLLBACK_DRILL_STATE_INVALID",
                "/rollback/drill_status",
                "Read-only v1 performs no mutation, so rollback drill status must be NOT_APPLICABLE.",
            )
        )

    if payload["evidence_ceiling"] != "LOCAL_RECEIPT_BINDING_ONLY":
        findings.append(
            Finding(
                "EVIDENCE_CEILING_TOO_LOW",
                "/evidence_ceiling",
                "The verified state is limited to local, Git-bound integration receipts.",
            )
        )

    if project_root is None:
        findings.append(
            Finding(
                "PROJECT_ROOT_REQUIRED",
                "/project/worktree_relative_root",
                "A live project root is required to verify exact HEAD and local evidence.",
            )
        )
        return findings

    try:
        supplied_root = project_root.resolve()
    except (OSError, ValueError) as error:
        findings.append(
            Finding(
                "PROJECT_ROOT_UNREADABLE",
                "/project/worktree_relative_root",
                f"Cannot resolve supplied project root: {error}",
            )
        )
        return findings
    root = _safe_child(supplied_root, project["worktree_relative_root"])
    editor_root = _safe_child(supplied_root, godot["editor_project_root"])
    if root is None or editor_root is None:
        findings.append(
            Finding(
                "UNSAFE_PROJECT_PATH",
                "/project/worktree_relative_root",
                "Project and editor roots must stay inside the supplied project root.",
            )
        )
        return findings
    if root != editor_root:
        findings.append(
            Finding(
                "EDITOR_WORKTREE_MISMATCH",
                "/godot/editor_project_root",
                "Godot Editor root must resolve to the exact Git worktree root.",
            )
        )

    for authority_name, authority_path in payload["authority_refs"].items():
        if not (ROOT / authority_path).is_file():
            findings.append(
                Finding(
                    "BASE_AUTHORITY_REF_MISSING",
                    f"/authority_refs/{authority_name}",
                    f"Referenced Base authority is missing: {authority_path}",
                )
            )

    head_result = _git(root, "rev-parse", "HEAD")
    if head_result.returncode:
        findings.append(
            Finding("GIT_WORKTREE_UNREADABLE", "/project", head_result.stderr.strip())
        )
        return findings

    top_level_result = _git(root, "rev-parse", "--show-toplevel")
    if top_level_result.returncode or Path(top_level_result.stdout.strip()).resolve() != root:
        findings.append(
            Finding(
                "WORKTREE_ROOT_MISMATCH",
                "/project/worktree_relative_root",
                "The bound project root must be the exact Git worktree top level.",
            )
        )

    origin_result = _git(root, "remote", "get-url", "origin")
    observed_repository = (
        _github_repository_slug(origin_result.stdout) if origin_result.returncode == 0 else None
    )
    if observed_repository is None:
        findings.append(
            Finding(
                "REPOSITORY_IDENTITY_UNVERIFIED",
                "/project/repository",
                "The origin remote must resolve to one GitHub owner/repository identity.",
            )
        )
    elif observed_repository.casefold() != project["repository"].casefold():
        findings.append(
            Finding(
                "REPOSITORY_IDENTITY_MISMATCH",
                "/project/repository",
                f"Recorded repository {project['repository']} does not match origin {observed_repository}.",
            )
        )

    base_ref = f"refs/heads/{project['base_branch']}"
    base_result = _git(root, "rev-parse", "--verify", base_ref)
    if base_result.returncode:
        findings.append(
            Finding(
                "BASE_BRANCH_UNRESOLVABLE",
                "/project/base_branch",
                f"Local base branch does not resolve: {project['base_branch']}.",
            )
        )
    elif base_result.stdout.strip() != project["base_sha"]:
        findings.append(
            Finding(
                "BASE_BRANCH_SHA_MISMATCH",
                "/project/base_sha",
                "base_sha must equal the exact local base-branch tip.",
            )
        )

    remote_base_ref = f"refs/remotes/origin/{project['base_branch']}"
    remote_base_result = _git(root, "rev-parse", "--verify", remote_base_ref)
    if remote_base_result.returncode:
        findings.append(
            Finding(
                "REMOTE_BASE_REF_UNRESOLVABLE",
                "/project/base_branch",
                "The local origin tracking ref must exist after a fresh fetch.",
            )
        )
    elif remote_base_result.stdout.strip() != project["base_sha"]:
        findings.append(
            Finding(
                "REMOTE_BASE_SHA_MISMATCH",
                "/project/base_sha",
                "base_sha must equal the fetched origin tracking ref.",
            )
        )
    observed_head = head_result.stdout.strip()
    if observed_head != project["result_sha"]:
        findings.append(
            Finding(
                "STALE_RESULT_SHA",
                "/project/result_sha",
                f"Recorded result SHA {project['result_sha']} does not match HEAD {observed_head}.",
            )
        )

    if project["base_sha"] != project["result_sha"]:
        findings.append(
            Finding(
                "READ_ONLY_COMMIT_DELTA",
                "/project/base_sha",
                "A read-only observation must begin and end at the same commit.",
            )
        )

    findings.extend(_raw_snapshot_findings(root, project["result_sha"]))

    index_entries = _git(root, "ls-files", "-v", "-z")
    visibility_overrides = []
    if index_entries.returncode:
        findings.append(
            Finding(
                "INDEX_VISIBILITY_SCAN_UNREADABLE",
                "/change_boundary/unexpected_tracked_diff",
                "Cannot inspect skip-worktree and assume-unchanged index flags.",
            )
        )
    else:
        for entry in index_entries.stdout.split("\0"):
            if not entry:
                continue
            tag = entry[0]
            if tag == "S" or tag.islower():
                visibility_overrides.append(entry[2:])
    if visibility_overrides:
        findings.append(
            Finding(
                "GIT_INDEX_VISIBILITY_OVERRIDE",
                "/change_boundary/unexpected_tracked_diff",
                "skip-worktree/assume-unchanged hides tracked paths: "
                + ", ".join(visibility_overrides),
            )
        )

    allowed_untracked: set[str] = set()
    try:
        allowed_untracked.add(capsule_path.resolve().relative_to(root).as_posix())
    except (OSError, ValueError):
        pass
    untracked_result = _git(root, "ls-files", "--others", "--exclude-standard", "-z")
    if untracked_result.returncode:
        findings.append(
            Finding(
                "UNTRACKED_SCAN_UNREADABLE",
                "/change_boundary/unexpected_tracked_diff",
                "Cannot enumerate untracked project files with repository excludes.",
            )
        )
    else:
        unexpected_untracked = sorted(
            path
            for path in untracked_result.stdout.split("\0")
            if path and path not in allowed_untracked
        )
        if unexpected_untracked:
            findings.append(
                Finding(
                    "UNTRACKED_PROJECT_FILE",
                    "/change_boundary/unexpected_tracked_diff",
                    "Read-only snapshot contains untracked files: "
                    + ", ".join(unexpected_untracked),
                )
            )

    ignored_result = _git(
        root,
        "ls-files",
        "--others",
        "--ignored",
        "--exclude-standard",
        "-z",
    )
    if ignored_result.returncode:
        findings.append(
            Finding(
                "IGNORED_SCAN_UNREADABLE",
                "/change_boundary/codex_forbidden_godot_paths",
                "Cannot enumerate ignored project files with repository excludes.",
            )
        )
    else:
        hidden_authoring = sorted(
            path
            for path in ignored_result.stdout.split("\0")
            if path
            and path not in allowed_untracked
            and not _is_allowed_generated_godot_cache(path)
        )
        if hidden_authoring:
            findings.append(
                Finding(
                    "IGNORED_GODOT_AUTHORING_FILE",
                    "/change_boundary/codex_forbidden_godot_paths",
                    "Ignored non-generated project files are outside the exact snapshot: "
                    + ", ".join(hidden_authoring),
                )
            )

    decision_path = _safe_child(root, decision["decision_record_path"])
    if decision_path is None:
        findings.append(
            Finding(
                "UNSAFE_DECISION_RECORD_PATH",
                "/decision/decision_record_path",
                "Decision record path escapes the project root.",
            )
        )
    elif not decision_path.is_file():
        findings.append(
            Finding(
                "DECISION_RECORD_MISSING",
                "/decision/decision_record_path",
                f"Decision record does not exist: {decision['decision_record_path']}",
            )
        )
    else:
        if not _path_exists_at_commit(root, project["result_sha"], decision["decision_record_path"]):
            findings.append(
                Finding(
                    "DECISION_RECORD_NOT_AT_RESULT_SHA",
                    "/decision/decision_record_path",
                    "Decision record must be tracked at result_sha.",
                )
            )
        try:
            decision_text = decision_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            findings.append(
                Finding(
                    "DECISION_RECORD_UNREADABLE",
                    "/decision/decision_record_path",
                    f"Decision record must be readable UTF-8 text: {error}",
                )
            )
        else:
            required_decision_bindings = {
                "decision_id": decision["decision_id"],
                "approval_ref": decision["approval_ref"],
                "approval_status": "APPROVED",
                "project_id": project["project_id"],
                "repository": project["repository"],
                "notion_project_key": notion["project_key"],
                "notion_record_key": notion["record_key"],
            }
            missing_bindings = [
                label
                for label, value in required_decision_bindings.items()
                if value not in decision_text
            ]
            if missing_bindings:
                findings.append(
                    Finding(
                        "CROSS_SYSTEM_PROJECT_MISMATCH",
                        "/decision/decision_record_path",
                        "Decision record is missing exact integration bindings: "
                        + ", ".join(missing_bindings),
                    )
                )

    adapter: dict[str, Any] = {}
    adapter_binding = payload["base_adapter"]
    if adapter_binding["path"] != CANONICAL_ADAPTER_PATH:
        findings.append(
            Finding(
                "NONCANONICAL_BASE_ADAPTER_PATH",
                "/base_adapter/path",
                f"Base adapter must use the canonical path {CANONICAL_ADAPTER_PATH}.",
            )
        )
    adapter_path = _safe_child(root, adapter_binding["path"])
    if adapter_path is None:
        findings.append(
            Finding(
                "UNSAFE_BASE_ADAPTER_PATH",
                "/base_adapter/path",
                "Base adapter path escapes the project root.",
            )
        )
    elif not adapter_path.is_file():
        findings.append(
            Finding(
                "BASE_ADAPTER_MISSING",
                "/base_adapter/path",
                f"Base adapter does not exist: {adapter_binding['path']}",
            )
        )
    else:
        if not _path_exists_at_commit(root, project["result_sha"], adapter_binding["path"]):
            findings.append(
                Finding(
                    "BASE_ADAPTER_NOT_AT_RESULT_SHA",
                    "/base_adapter/path",
                    "Base adapter must be tracked at result_sha.",
                )
            )
        if _sha256(adapter_path) != adapter_binding["sha256"]:
            findings.append(
                Finding(
                    "BASE_ADAPTER_HASH_MISMATCH",
                    "/base_adapter/sha256",
                    "Base adapter bytes do not match the recorded hash.",
                )
            )
        try:
            adapter = _load_json(adapter_path)
        except (OSError, ValueError, json.JSONDecodeError):
            findings.append(
                Finding(
                    "BASE_ADAPTER_INVALID",
                    "/base_adapter/path",
                    "Base adapter must be a valid JSON object.",
                )
            )
        else:
            from tools import project_operating_contract as operating_contract
            from tools.base_release_index import (
                RELEASE_FINALIZATION_COMMITS,
                install_release_lock_paths,
            )

            try:
                adapter_schema_path, adapter_schema_label = operating_contract.adapter_schema(
                    adapter
                )
                adapter_schema = _load_json(adapter_schema_path)
            except (OSError, ValueError, operating_contract.ContractError):
                adapter_schema_label = "unsupported"
                adapter_errors = ["unsupported or unreadable adapter schema"]
            else:
                adapter_errors = list(
                    Draft202012Validator(adapter_schema).iter_errors(adapter)
                )
            if adapter_errors:
                findings.append(
                    Finding(
                        "BASE_ADAPTER_INVALID",
                        "/base_adapter/path",
                        f"Base adapter does not satisfy {adapter_schema_label}.",
                    )
                )
            else:
                adapter_project = adapter["project"]
                adapter_project_id = adapter_project.get("project_id")
                if (
                    (
                        adapter_project_id is not None
                        and adapter_project_id != project["project_id"]
                    )
                    or adapter_project["repository"].casefold()
                    != project["repository"].casefold()
                    or adapter_project["root"] != project["worktree_relative_root"]
                ):
                    findings.append(
                        Finding(
                            "BASE_ADAPTER_PROJECT_MISMATCH",
                            "/base_adapter/path",
                            "Base adapter project identity does not match the integration capsule.",
                        )
                    )

                install_release_lock_paths(operating_contract)
                try:
                    release_errors, _, _ = operating_contract._release_lock_contract(
                        adapter,
                        ROOT,
                        git_runner=_git,
                        git_show_bytes=_git_show_bytes,
                    )
                except (KeyError, TypeError, ValueError) as error:
                    release_errors = [f"release lock validation failed: {error}"]
                base_release = adapter["base_release"]
                expected_finalization = RELEASE_FINALIZATION_COMMITS.get(
                    base_release["version"]
                )
                if (
                    release_errors
                    or expected_finalization is None
                    or base_release.get("finalization_commit") != expected_finalization
                ):
                    findings.append(
                        Finding(
                            "BASE_RELEASE_UNVERIFIED",
                            "/base_adapter/path",
                            "Base adapter release/evidence/finalization pins do not match "
                            "the canonical Base release lock.",
                        )
                    )

    adoption_path = _safe_child(root, godot["adoption_record_path"])
    if adoption_path is None:
        findings.append(
            Finding(
                "UNSAFE_HIGODOT_ADOPTION_PATH",
                "/godot/adoption_record_path",
                "HiGodot adoption record path escapes the project root.",
            )
        )
    elif not adoption_path.is_file():
        findings.append(
            Finding(
                "HIGODOT_ADOPTION_MISSING",
                "/godot/adoption_record_path",
                f"HiGodot adoption record does not exist: {godot['adoption_record_path']}",
            )
        )
    else:
        if not _path_exists_at_commit(root, project["result_sha"], godot["adoption_record_path"]):
            findings.append(
                Finding(
                    "HIGODOT_ADOPTION_NOT_AT_RESULT_SHA",
                    "/godot/adoption_record_path",
                    "HiGodot adoption record must be tracked at result_sha.",
                )
            )
        if _sha256(adoption_path) != godot["adoption_record_sha256"]:
            findings.append(
                Finding(
                    "HIGODOT_ADOPTION_HASH_MISMATCH",
                    "/godot/adoption_record_sha256",
                    "HiGodot adoption record bytes do not match the recorded hash.",
                )
            )
        try:
            adoption = _load_json(adoption_path)
        except (OSError, ValueError, json.JSONDecodeError):
            adoption = {}
        exact_pin = adoption.get("exact_release_or_commit")
        adapter_project_for_engine = adapter.get("project")
        adapter_engine = (
            adapter_project_for_engine.get("engine", "")
            if isinstance(adapter_project_for_engine, dict)
            else ""
        )
        host_clients = adoption.get("host_clients")
        verification_evidence = adoption.get("verification_evidence")
        rollback_pin = adoption.get("rollback_release_or_commit")
        writer_receipt_paths = {
            evidence["path"]
            for evidence in payload["evidence"]
            if evidence["kind"] == "WRITER_EXCLUSIVITY_CANARY"
        }
        adoption_ready = (
            adoption.get("schema_version") == 1
            and adoption.get("artifact_role") == "HIGODOT_ADOPTION_RECORD"
            and adoption.get("provider") == godot["authoring_provider"]
            and _is_exact_release_or_commit(exact_pin)
            and adoption.get("godot_version") not in (None, "NOT_CONFIGURED")
            and str(adoption.get("godot_version")) in adapter_engine
            and isinstance(host_clients, dict)
            and isinstance(host_clients.get("codex"), str)
            and host_clients.get("codex") not in {"", "NOT_CONFIGURED", "FORBIDDEN", "FAIL"}
            and host_clients.get("deepseek") == "FORBIDDEN"
            and adoption.get("network_mode") == "LOOPBACK_ONLY"
            and adoption.get("unverified_domains") == []
            and _is_rfc3339(adoption.get("last_verified_at"))
            and isinstance(verification_evidence, list)
            and all(isinstance(path, str) for path in verification_evidence)
            and bool(
                writer_receipt_paths.intersection(
                    set(verification_evidence)
                )
            )
            and _is_exact_release_or_commit(rollback_pin)
            and adoption.get("connection_status") == "PASS"
        )
        if not adoption_ready:
            findings.append(
                Finding(
                    "HIGODOT_ADOPTION_UNVERIFIED",
                    "/godot/adoption_record_path",
                    "Canonical HiGodot adoption evidence is incomplete or not exact-pinned.",
                )
            )

    branch_result = _git(root, "branch", "--show-current")
    observed_branch = branch_result.stdout.strip()
    if branch_result.returncode or observed_branch != project["worktree_branch"]:
        findings.append(
            Finding(
                "WORKTREE_BRANCH_MISMATCH",
                "/project/worktree_branch",
                f"Recorded branch {project['worktree_branch']} does not match {observed_branch or 'DETACHED'}.",
            )
        )

    ancestry = _git(root, "merge-base", "--is-ancestor", project["base_sha"], project["result_sha"])
    if ancestry.returncode:
        findings.append(
            Finding(
                "BASE_RESULT_ANCESTRY_INVALID",
                "/project/base_sha",
                "base_sha must exist and be an ancestor of result_sha.",
            )
        )

    rollback = _git(root, "cat-file", "-e", f'{payload["rollback"]["rollback_ref"]}^{{commit}}')
    if rollback.returncode:
        findings.append(
            Finding(
                "ROLLBACK_REF_UNRESOLVABLE",
                "/rollback/rollback_ref",
                "rollback_ref must resolve to a commit in the project repository.",
            )
        )
    if payload["rollback"]["rollback_ref"] != project["base_sha"]:
        findings.append(
            Finding(
                "ROLLBACK_BASE_MISMATCH",
                "/rollback/rollback_ref",
                "A no-product-mutation binding must use its exact base/result commit.",
            )
        )

    project_file = _safe_child(root, "project.godot")
    if project_file is None or not project_file.is_file():
        findings.append(
            Finding("PROJECT_GODOT_MISSING", "/godot", "project.godot is missing from the bound root.")
        )
    elif _sha256(project_file) != godot["project_godot_sha256"]:
        findings.append(
            Finding(
                "PROJECT_GODOT_FINGERPRINT_MISMATCH",
                "/godot/project_godot_sha256",
                "project.godot bytes do not match the recorded fingerprint.",
            )
        )
    elif not _path_exists_at_commit(root, project["result_sha"], "project.godot"):
        findings.append(
            Finding(
                "PROJECT_GODOT_NOT_AT_RESULT_SHA",
                "/godot/project_godot_sha256",
                "project.godot must be tracked at result_sha.",
            )
        )

    for index, evidence in enumerate(payload["evidence"]):
        evidence_path = _safe_child(root, evidence["path"])
        if evidence_path is None:
            findings.append(
                Finding(
                    "UNSAFE_EVIDENCE_PATH",
                    f"/evidence/{index}/path",
                    "Evidence path escapes the project root.",
                )
            )
        elif not evidence_path.is_file():
            findings.append(
                Finding(
                    "EVIDENCE_MISSING",
                    f"/evidence/{index}/path",
                    f"Evidence file does not exist: {evidence['path']}",
                )
            )
        elif not _path_exists_at_commit(root, project["result_sha"], evidence["path"]):
            findings.append(
                Finding(
                    "EVIDENCE_NOT_AT_RESULT_SHA",
                    f"/evidence/{index}/path",
                    f"Evidence is not tracked at result_sha: {evidence['path']}",
                )
            )
        elif _sha256(evidence_path) != evidence["sha256"]:
            findings.append(
                Finding(
                    "EVIDENCE_HASH_MISMATCH",
                    f"/evidence/{index}/sha256",
                    f"Evidence bytes do not match the recorded hash: {evidence['path']}",
                )
            )
        else:
            try:
                receipt = _load_json(evidence_path)
            except (OSError, ValueError, json.JSONDecodeError):
                findings.append(
                    Finding(
                        "EVIDENCE_RECEIPT_INVALID",
                        f"/evidence/{index}/path",
                        f"Evidence receipt must be a JSON object: {evidence['path']}",
                    )
                )
                continue

            if evidence["kind"] == "NOTION_READBACK":
                expected_receipt = {
                    "source": "NOTION_OFFICIAL_MCP_SEARCH_FETCH",
                    "access_mode": "SEARCH_FETCH_ONLY",
                    "existing_page_write": "FORBIDDEN",
                    "project": notion["project_key"],
                    "project_relation_count": 1,
                    "record_key": notion["record_key"],
                    "revision": notion["revision"],
                    "last_edited": notion["last_edited"],
                    "status": "PASS",
                }
                mismatched = [
                    key for key, expected in expected_receipt.items() if receipt.get(key) != expected
                ]
                if mismatched:
                    findings.append(
                        Finding(
                            "NOTION_EVIDENCE_MISMATCH",
                            f"/evidence/{index}/path",
                            "Notion readback receipt does not match capsule fields: "
                            + ", ".join(mismatched),
                        )
                    )
            elif evidence["kind"] == "WRITER_EXCLUSIVITY_CANARY":
                required_paths = set(payload["change_boundary"]["codex_forbidden_godot_paths"])
                observed_paths = receipt.get("blocked_paths", [])
                receipt_matches = (
                    receipt.get("attempted_actor") == "CODEX"
                    and receipt.get("attempted_path") == "project.godot"
                    and receipt.get("authoring_provider") == godot["authoring_provider"]
                    and receipt.get("operation_level") == godot["operation_level"]
                    and receipt.get("observed") == "BLOCKED"
                    and receipt.get("second_writer_blocked") is True
                    and receipt.get("status") == "PASS"
                    and isinstance(observed_paths, list)
                    and all(isinstance(path, str) for path in observed_paths)
                    and required_paths.issubset(set(observed_paths))
                )
                if not receipt_matches:
                    findings.append(
                        Finding(
                            "WRITER_CANARY_EVIDENCE_MISMATCH",
                            f"/evidence/{index}/path",
                            "Writer canary receipt does not prove the declared Codex/Godot boundary.",
                        )
                    )

    if project["base_sha"] == ZERO_SHA40 or project["result_sha"] == ZERO_SHA40:
        findings.append(
            Finding(
                "PLACEHOLDER_SHA_FORBIDDEN",
                "/project",
                "Verified receipt binding cannot use placeholder SHAs.",
            )
        )

    return findings
