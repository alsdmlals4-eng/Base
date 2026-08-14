"""Fixed argv specifications for the reviewed Tool Hub child owners."""

from __future__ import annotations

from dataclasses import dataclass, replace
import os
from pathlib import Path
import re
import sys
from types import MappingProxyType
from typing import Mapping

from base_tool_contracts.trusted_files import TrustedFileError, open_directory_nofollow

from .environment import LaunchContext, child_environment, ensure_runtime_directory
from .projects import ProjectBinding
from .runtime_trust import RuntimeTrustError, assert_runtime_pins


class AdapterError(ValueError):
    pass


@dataclass(frozen=True)
class LaunchSpec:
    argv: tuple[str, ...]
    cwd: Path
    env: Mapping[str, str]
    startup_file: Path
    expected_identity: Mapping[str, str]
    pass_fds: tuple[int, ...] = ()


_REVIEWED_TUPLES: dict[str, tuple[str, str, tuple[str, ...], str]] = {
    "qa-evidence-studio": (
        "tools/qa-evidence-studio",
        "qa_evidence_studio",
        ("developer_pc_review", "image_evidence", "qa_evidence_packet"),
        "qa_evidence_studio.app",
    ),
    "expression-studio": (
        "tools/expression-studio",
        "expression_studio",
        (
            "expression_variation",
            "identity_preserving_edit",
            "outfit_variation",
            "scene_relocation",
            "image_import",
            "figma_delivery_packet",
        ),
        "expression_studio.app",
    ),
    "sprite-animation-studio": (
        "tools/sprite-animation-studio",
        "sprite_animation_studio",
        ("sprite_action", "expression_variation", "pose_sequence", "effect_stages"),
        "sprite_animation_studio.app",
    ),
}
_RUN_REVIEWED_MODULE = (
    "import runpy,sys; "
    "contract_source,owner_source,site_packages,module,*args=sys.argv[1:]; "
    "sys.path[:0]=[contract_source,owner_source,site_packages]; "
    "sys.argv=[module,*args]; "
    "runpy.run_module(module,run_name='__main__')"
)


def bind_launch_spec(spec: LaunchSpec) -> LaunchSpec:
    """Bind every executable/import root to inherited descriptors before Popen."""
    descriptors: list[int] = []
    try:
        executable = Path(spec.argv[0]).resolve(strict=True)
        executable_fd = os.open(
            executable,
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        descriptors.append(executable_fd)
        cwd_fd = open_directory_nofollow(spec.cwd)
        descriptors.append(cwd_fd)
        argv = list(spec.argv)
        argv[0] = f"/proc/self/fd/{executable_fd}"
        code_index = argv.index("-c")
        for index in (code_index + 2, code_index + 4):
            descriptor = open_directory_nofollow(Path(argv[index]))
            descriptors.append(descriptor)
            argv[index] = f"/proc/self/fd/{descriptor}"
        argv[code_index + 3] = f"/proc/self/fd/{cwd_fd}/src"
        return replace(
            spec,
            argv=tuple(argv),
            cwd=Path(f"/proc/self/fd/{cwd_fd}"),
            pass_fds=tuple(descriptors),
        )
    except (OSError, ValueError, TrustedFileError) as error:
        for descriptor in descriptors:
            os.close(descriptor)
        raise AdapterError("reviewed launch paths could not be descriptor-bound") from error


def _reviewed_tuple(tool: dict[str, object]) -> tuple[str, str, tuple[str, ...], str]:
    tool_id = tool.get("tool_id")
    if not isinstance(tool_id, str) or tool_id not in _REVIEWED_TUPLES:
        raise AdapterError("tool does not have a fixed reviewed tuple")
    reviewed = _REVIEWED_TUPLES[tool_id]
    if (
        tool.get("owner_path") != reviewed[0]
        or tool.get("launch_adapter") != reviewed[1]
        or tuple(tool.get("capabilities", ())) != reviewed[2]
    ):
        raise AdapterError("tool does not have its fixed reviewed tuple")
    return reviewed


def _verified_owner(context: LaunchContext, owner_relative: str) -> Path:
    root = Path(context.base_root).absolute()
    owner = root / owner_relative
    try:
        for path in (root, root / "tools", owner):
            descriptor = open_directory_nofollow(path)
            os.close(descriptor)
    except (OSError, TrustedFileError) as error:
        raise AdapterError("reviewed Studio owner is unavailable or replaced") from error
    return owner


def _verified_source_roots(context: LaunchContext, owner: Path) -> tuple[Path, Path, Path]:
    """Validate every source root supplied to the isolated child without links."""
    root = Path(context.base_root).absolute()
    contract_source = root / "tools" / "base-tool-contracts" / "src"
    owner_source = owner / "src"
    site_packages = root / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    try:
        for path in (contract_source, owner_source, site_packages):
            descriptor = open_directory_nofollow(path)
            os.close(descriptor)
    except (OSError, TrustedFileError) as error:
        raise AdapterError("reviewed source root is unavailable or replaced") from error
    return contract_source, owner_source, site_packages


def _reject_untracked_sourceless_bytecode(owner: Path) -> None:
    """Reject bytecode that does not correspond to a reviewed source module."""
    for candidate in owner.rglob("*.pyc"):
        stem = candidate.name.split(".cpython-", 1)[0].removesuffix(".pyc")
        if not (candidate.parent.parent / f"{stem}.py").is_file():
            raise AdapterError("reviewed Studio owner contains untracked bytecode")


def _verified_interpreter(context: LaunchContext) -> Path:
    expected = Path(context.base_root).absolute() / ".venv" / "bin" / "python"
    selected = Path(context.python_executable).absolute()
    try:
        if not os.path.samefile(expected, selected):
            raise AdapterError("interpreter is outside the reviewed Tool Hub virtual environment")
    except OSError as error:
        raise AdapterError("interpreter is outside the reviewed Tool Hub virtual environment") from error
    return expected


def _startup_file(context: LaunchContext, tool_id: str, project_id: str) -> Path:
    if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_id) is None:
        raise AdapterError("project identity is invalid")
    try:
        runtime = ensure_runtime_directory(context.runtime_root)
    except ValueError as error:
        raise AdapterError(str(error)) from error
    startup = runtime / f"{tool_id}-{project_id}.json"
    if os.path.lexists(startup):
        raise AdapterError("startup report path is already present or replaced")
    return startup


def build_launch_spec(tool: dict[str, object], project: ProjectBinding, context: LaunchContext) -> LaunchSpec:
    """Return a browser-independent, import-only launch specification."""
    owner_relative, _, _, module = _reviewed_tuple(tool)
    owner = _verified_owner(context, owner_relative)
    contract_source, owner_source, site_packages = _verified_source_roots(context, owner)
    _reject_untracked_sourceless_bytecode(owner)
    interpreter = _verified_interpreter(context)
    try:
        assert_runtime_pins(context.base_root, owner_relative, interpreter, tool)
    except RuntimeTrustError as error:
        message = str(error)
        if "interpreter" in message or "environment" in message:
            raise AdapterError("reviewed interpreter environment changed before launch") from error
        raise AdapterError("reviewed source changed before launch") from error
    if not project.adapter_sha256 or not project.fingerprint:
        raise AdapterError("project binding has incomplete immutable identity")
    startup = _startup_file(context, project_id=project.project_id, tool_id=str(tool["tool_id"]))
    environment = child_environment(context, project.adapter_sha256, project.fingerprint)
    cache_prefix = environment["PYTHONPYCACHEPREFIX"]
    argv = [
        str(interpreter),
        "-I",
        "-S",
        "-B",
        "-X",
        f"pycache_prefix={cache_prefix}",
        "-c",
        _RUN_REVIEWED_MODULE,
        str(contract_source),
        str(owner_source),
        str(site_packages),
        module,
        "--project-root",
        str(project.root),
        "--project-id",
        project.project_id,
        "--port",
        "0",
        "--startup-file",
        str(startup),
    ]
    tool_id = str(tool["tool_id"])
    if tool_id in {"expression-studio", "sprite-animation-studio"}:
        argv.extend(
            [
                "--run-mode",
                "subscription_handoff_import",
                "--figma-target-registry",
                str(Path(context.base_root).absolute() / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"),
                "--approved-anchor-registry",
                str(project.root / "docs" / "APPROVED_VISUAL_ANCHORS.json"),
            ]
        )
    if tool_id == "qa-evidence-studio":
        argv.extend(["--launch-nonce", context.launch_nonce])
    expected_identity = MappingProxyType(
        {
            "tool_id": tool_id,
            "project_id": project.project_id,
            "launch_nonce": context.launch_nonce,
            "adapter_sha256": project.adapter_sha256,
            "root_fingerprint": project.fingerprint,
        }
    )
    return LaunchSpec(tuple(argv), owner, environment, startup, expected_identity)
