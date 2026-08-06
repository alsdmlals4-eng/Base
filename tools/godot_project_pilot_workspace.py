import hashlib
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from tools.godot_editor_adapter_materialization import (
    build_configured_manifest,
    copy_canonical_addon,
    sha256_file,
)
from tools.godot_project_pilot_descriptor import ProjectPilotDescriptor


_BASE_PLUGIN = "res://addons/base_multi_project_pilot/plugin.cfg"
_EXCLUDED_NAMES = {
    ".git",
    ".godot",
    ".godot-live-editor",
    ".pytest_cache",
    ".tmp",
    "__pycache__",
    "_base_c0",
}
_SECTION_RE = re.compile(r"^\[([^\]]+)\]\s*$")
_QUOTED_RE = re.compile(r'"([^"]+)"')
_AUTOLOAD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=")
_MAIN_SCENE_RE = re.compile(r'^run/main_scene\s*=\s*"(res://[^"]+)"\s*$')


@dataclass(frozen=True)
class ProjectTransformReport:
    main_scene: str
    removed_plugins: tuple[str, ...]
    removed_autoloads: tuple[str, ...]
    preserved_autoloads: tuple[str, ...]
    before_sha256: str
    after_sha256: str


@dataclass(frozen=True)
class MaterializedWorkspace:
    root: Path
    main_scene: str
    manifest_path: Path
    wrapper_script: Path
    transform_report: ProjectTransformReport


def _run_git(source_root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(source_root), *args],
        check=False,
        capture_output=True,
        shell=False,
        timeout=30,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(f"GIT_INVENTORY_FAILED: {detail}")
    return completed.stdout


def list_tracked_paths(source_root: Path) -> tuple[Path, ...]:
    root = Path(source_root).resolve()
    values = _run_git(root, "ls-files", "-z").split(b"\0")
    result: list[Path] = []
    for raw in values:
        if not raw:
            continue
        relative = Path(os.fsdecode(raw))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"TRACKED_PATH_INVALID: {relative}")
        absolute = root / relative
        if absolute.is_symlink():
            target = (absolute.parent / os.readlink(absolute)).resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise ValueError(f"SYMLINK_ESCAPE: {relative}") from exc
        if not absolute.exists() and not absolute.is_symlink():
            raise ValueError(f"TRACKED_PATH_MISSING: {relative}")
        result.append(relative)
    return tuple(sorted(result, key=lambda value: value.as_posix()))


def inventory_tracked_files(source_root: Path) -> dict[str, str]:
    root = Path(source_root).resolve()
    inventory: dict[str, str] = {}
    for relative in list_tracked_paths(root):
        absolute = root / relative
        if absolute.is_symlink():
            payload = os.readlink(absolute).encode("utf-8")
            digest = hashlib.sha256(b"symlink\0" + payload).hexdigest()
        elif absolute.is_file():
            digest = sha256_file(absolute)
        else:
            raise ValueError(f"TRACKED_PATH_NOT_FILE: {relative}")
        inventory[relative.as_posix()] = digest
    return inventory


def inventory_digest(inventory: Mapping[str, str]) -> str:
    payload = json.dumps(
        {key: inventory[key] for key in sorted(inventory)},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def compare_inventories(
    before: Mapping[str, str],
    after: Mapping[str, str],
) -> tuple[str, ...]:
    keys = set(before) | set(after)
    return tuple(sorted(key for key in keys if before.get(key) != after.get(key)))


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def copy_to_workspace(source_root: Path, workspace_root: Path) -> None:
    source = Path(source_root).resolve()
    destination = Path(workspace_root).absolute()
    if destination.exists():
        raise FileExistsError(f"WORKSPACE_EXISTS: {destination}")
    destination_resolved = destination.resolve(strict=False)
    if (
        source == destination_resolved
        or _is_within(destination_resolved, source)
        or _is_within(source, destination_resolved)
    ):
        raise ValueError("WORKSPACE_OVERLAP")
    inventory_tracked_files(source)

    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {name for name in names if name in _EXCLUDED_NAMES}

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=ignore, symlinks=False)


def _sections(lines: list[str]) -> dict[str, tuple[int, int]]:
    starts: list[tuple[str, int]] = []
    seen: set[str] = set()
    for index, line in enumerate(lines):
        match = _SECTION_RE.match(line.strip())
        if match is None:
            continue
        name = match.group(1)
        if name in seen:
            raise ValueError(f"PROJECT_GODOT_UNSUPPORTED_FORMAT: duplicate section {name}")
        seen.add(name)
        starts.append((name, index))
    result: dict[str, tuple[int, int]] = {}
    for offset, (name, start) in enumerate(starts):
        end = starts[offset + 1][1] if offset + 1 < len(starts) else len(lines)
        result[name] = (start, end)
    return result


def _main_scene(lines: list[str], sections: dict[str, tuple[int, int]]) -> str:
    bounds = sections.get("application")
    if bounds is None:
        raise ValueError("MAIN_SCENE_INVALID: missing application section")
    for line in lines[bounds[0] + 1 : bounds[1]]:
        match = _MAIN_SCENE_RE.match(line.strip())
        if match is not None:
            value = match.group(1)
            if ".." in value or not value.endswith(".tscn"):
                break
            return value
    raise ValueError("MAIN_SCENE_INVALID")


def transform_project_godot(
    path: Path,
    descriptor: ProjectPilotDescriptor,
) -> ProjectTransformReport:
    project = Path(path).resolve()
    before_sha256 = sha256_file(project)
    text = project.read_text(encoding="utf-8")
    lines = text.splitlines()
    sections = _sections(lines)
    main_scene = _main_scene(lines, sections)

    removed_autoloads: list[str] = []
    preserved_autoloads: list[str] = []
    autoload_bounds = sections.get("autoload")
    autoload_line_indexes: dict[str, int] = {}
    if autoload_bounds is not None:
        for index in range(autoload_bounds[0] + 1, autoload_bounds[1]):
            match = _AUTOLOAD_RE.match(lines[index].strip())
            if match is None:
                continue
            name = match.group(1)
            if name in autoload_line_indexes:
                raise ValueError(
                    f"PROJECT_GODOT_UNSUPPORTED_FORMAT: duplicate autoload {name}"
                )
            autoload_line_indexes[name] = index
    for name in descriptor.legacy_autoloads:
        if name not in autoload_line_indexes:
            raise ValueError(f"DECLARED_LEGACY_AUTOLOAD_NOT_FOUND: {name}")
        removed_autoloads.append(name)
    for name in autoload_line_indexes:
        if name not in descriptor.legacy_autoloads:
            preserved_autoloads.append(name)

    plugin_bounds = sections.get("editor_plugins")
    plugin_line_index: int | None = None
    plugin_values: list[str] = []
    if plugin_bounds is not None:
        for index in range(plugin_bounds[0] + 1, plugin_bounds[1]):
            stripped = lines[index].strip()
            if not stripped.startswith("enabled"):
                continue
            if plugin_line_index is not None:
                raise ValueError(
                    "PROJECT_GODOT_UNSUPPORTED_FORMAT: multiple enabled plugin lines"
                )
            if "PackedStringArray(" not in stripped or not stripped.endswith(")"):
                raise ValueError(
                    "PROJECT_GODOT_UNSUPPORTED_FORMAT: unsupported plugin list"
                )
            plugin_line_index = index
            plugin_values = _QUOTED_RE.findall(stripped)
    removed_plugins: list[str] = []
    for plugin in descriptor.legacy_editor_plugins:
        if plugin not in plugin_values:
            raise ValueError(f"DECLARED_LEGACY_PLUGIN_NOT_FOUND: {plugin}")
        removed_plugins.append(plugin)

    remove_indexes = {autoload_line_indexes[name] for name in descriptor.legacy_autoloads}
    output: list[str] = []
    for index, line in enumerate(lines):
        if index in remove_indexes:
            continue
        if index == plugin_line_index:
            remaining = [
                value
                for value in plugin_values
                if value not in descriptor.legacy_editor_plugins
            ]
            rendered = ", ".join(json.dumps(value) for value in remaining)
            output.append(f"enabled=PackedStringArray({rendered})")
            continue
        output.append(line)
    project.write_text("\n".join(output) + "\n", encoding="utf-8")
    after_sha256 = sha256_file(project)
    return ProjectTransformReport(
        main_scene=main_scene,
        removed_plugins=tuple(removed_plugins),
        removed_autoloads=tuple(removed_autoloads),
        preserved_autoloads=tuple(sorted(preserved_autoloads)),
        before_sha256=before_sha256,
        after_sha256=after_sha256,
    )


def _activate_pilot_plugin(project_file: Path) -> None:
    lines = project_file.read_text(encoding="utf-8").splitlines()
    sections = _sections(lines)
    bounds = sections.get("editor_plugins")
    if bounds is None:
        lines.extend(["", "[editor_plugins]", f"enabled=PackedStringArray({json.dumps(_BASE_PLUGIN)})"])
    else:
        enabled_index: int | None = None
        values: list[str] = []
        for index in range(bounds[0] + 1, bounds[1]):
            stripped = lines[index].strip()
            if stripped.startswith("enabled"):
                enabled_index = index
                values = _QUOTED_RE.findall(stripped)
                break
        if _BASE_PLUGIN not in values:
            values.append(_BASE_PLUGIN)
        rendered = ", ".join(json.dumps(value) for value in values)
        replacement = f"enabled=PackedStringArray({rendered})"
        if enabled_index is None:
            lines.insert(bounds[1], replacement)
        else:
            lines[enabled_index] = replacement
    project_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def prepare_runtime_workspace(
    workspace_root: Path,
    descriptor: ProjectPilotDescriptor,
) -> ProjectTransformReport:
    root = Path(workspace_root).resolve()
    if not descriptor.is_runtime_project or descriptor.project_file is None:
        raise ValueError("RUNTIME_PROJECT_REQUIRED")
    project_file = root / descriptor.project_file
    if not project_file.is_file():
        raise FileNotFoundError(f"missing project file: {project_file}")
    report = transform_project_godot(project_file, descriptor)
    main_scene_file = root / report.main_scene.removeprefix("res://")
    if not main_scene_file.is_file():
        raise ValueError(f"MAIN_SCENE_INVALID: {report.main_scene}")
    return report


def materialize_runtime_workspace(
    base_root: Path,
    workspace_root: Path,
    descriptor: ProjectPilotDescriptor,
    source_commit: str,
    transform_report: ProjectTransformReport | None = None,
) -> MaterializedWorkspace:
    root = Path(workspace_root).resolve()
    if not descriptor.is_runtime_project or descriptor.project_file is None:
        raise ValueError("RUNTIME_PROJECT_REQUIRED")
    project_file = root / descriptor.project_file
    if not project_file.is_file():
        raise FileNotFoundError(f"missing project file: {project_file}")
    report = transform_report or prepare_runtime_workspace(root, descriptor)
    main_scene_file = root / report.main_scene.removeprefix("res://")
    if not main_scene_file.is_file():
        raise ValueError(f"MAIN_SCENE_INVALID: {report.main_scene}")

    copy_canonical_addon(base_root, root)
    template_root = Path(base_root).resolve() / "templates/project-operations/godot-live-editor/pilot"
    pilot_dir = root / ".godot-live-editor-pilot"
    pilot_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template_root / "scratch.tscn", pilot_dir / "scratch.tscn")
    pilot_addon = root / "addons/base_multi_project_pilot"
    pilot_addon.mkdir(parents=True, exist_ok=True)
    shutil.copy2(template_root / "multi_project_pilot.gd", pilot_addon / "plugin.gd")
    (pilot_addon / "plugin.cfg").write_text(
        '[plugin]\nname="Base Multi-Project Pilot"\ndescription="Scratch-only Base C0 validation"\n'
        'author="Base"\nversion="1.0.0"\nscript="plugin.gd"\n',
        encoding="utf-8",
    )
    context = {
        "repository": descriptor.repository,
        "source_commit": source_commit,
        "base_pilot_commit": descriptor.base_pilot_commit,
        "main_scene": report.main_scene,
        "scratch_scene": descriptor.scratch_scene_path,
    }
    (pilot_dir / "context.json").write_text(
        json.dumps(context, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    _activate_pilot_plugin(project_file)
    manifest = build_configured_manifest(root, sha256_file(project_file))
    manifest_path = root / "GODOT_LIVE_EDITOR_CAPABILITY_MANIFEST.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return MaterializedWorkspace(
        root=root,
        main_scene=report.main_scene,
        manifest_path=manifest_path,
        wrapper_script=pilot_addon / "plugin.gd",
        transform_report=report,
    )


__all__ = [
    "MaterializedWorkspace",
    "ProjectTransformReport",
    "compare_inventories",
    "copy_to_workspace",
    "inventory_digest",
    "inventory_tracked_files",
    "list_tracked_paths",
    "materialize_runtime_workspace",
    "prepare_runtime_workspace",
    "transform_project_godot",
]
