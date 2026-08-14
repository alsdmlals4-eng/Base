from pathlib import Path
import os
import py_compile
import site
import subprocess

import pytest

import tool_hub.adapters as adapters_module
from tool_hub.adapters import AdapterError, build_launch_spec
from tool_hub.environment import LaunchContext
from tool_hub.projects import ProjectBinding
from tool_hub.registry import HubRegistryError, load_reviewed_tools


BASE_ROOT = Path(__file__).resolve().parents[3]


def _context(tmp_path: Path) -> LaunchContext:
    return LaunchContext(
        base_root=BASE_ROOT,
        runtime_root=tmp_path / "runtime",
        python_executable=BASE_ROOT / ".venv" / "bin" / "python",
        launch_nonce="n" * 43,
    )


def _project(tmp_path: Path) -> ProjectBinding:
    root = tmp_path / "Project with spaces; $(never-run)"
    root.mkdir()
    return ProjectBinding(
        project_id="demo-game",
        root=root,
        repository="owner/demo-game",
        engine="Godot 4.7",
        fingerprint="b" * 64,
        adapter_sha256="a" * 64,
        protected_paths=("project.godot",),
        validator_sha256="c" * 64,
    )


@pytest.mark.parametrize(
    "tool_id,module",
    [
        ("qa-evidence-studio", "qa_evidence_studio.app"),
        ("expression-studio", "expression_studio.app"),
        ("sprite-animation-studio", "sprite_animation_studio.app"),
    ],
)
def test_each_reviewed_tool_has_one_fixed_owner_adapter_and_module(
    tmp_path: Path, tool_id: str, module: str
) -> None:
    """Changing any owner/adapter mapping must not redirect a Hub launch."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == tool_id)

    project = _project(tmp_path)
    spec = build_launch_spec(tool, project, _context(tmp_path))

    assert spec.argv[:6] == (str(BASE_ROOT / ".venv" / "bin" / "python"), "-I", "-S", "-B", "-X", f"pycache_prefix={spec.env['PYTHONPYCACHEPREFIX']}")
    assert spec.argv[spec.argv.index("-c") + 5] == module
    assert spec.cwd == BASE_ROOT / str(tool["owner_path"])
    assert spec.argv[spec.argv.index("--project-root") + 1] == str(project.root)
    assert spec.startup_file.parent == tmp_path / "runtime"
    assert spec.expected_identity["tool_id"] == tool_id
    assert spec.expected_identity["project_id"] == "demo-game"


def test_launch_binding_uses_inherited_descriptors_instead_of_reopening_reviewed_paths(
    tmp_path: Path,
) -> None:
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    spec = build_launch_spec(tool, _project(tmp_path), _context(tmp_path))

    bound = adapters_module.bind_launch_spec(spec)
    try:
        assert bound.argv[0].startswith("/proc/self/fd/")
        code_index = bound.argv.index("-c")
        assert all(
            value.startswith("/proc/self/fd/")
            for value in bound.argv[code_index + 2 : code_index + 5]
        )
        assert str(bound.cwd).startswith("/proc/self/fd/")
        assert len(bound.pass_fds) == 4
    finally:
        for descriptor in bound.pass_fds:
            os.close(descriptor)


def test_launch_argv_enforces_bytecode_isolation_in_a_real_child_process(tmp_path: Path) -> None:
    """Removing the argv flags would let isolated Python ignore the private cache policy."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    spec = build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    code_index = spec.argv.index("-c")
    probe = (
        *spec.argv[:code_index],
        "-c",
        "import sys; print(sys.pycache_prefix); print(sys.dont_write_bytecode)",
    )

    result = subprocess.run(probe, check=True, capture_output=True, text=True, env=dict(spec.env))

    assert result.stdout.splitlines() == [spec.env["PYTHONPYCACHEPREFIX"], "True"]


def test_launch_argv_ignores_malicious_checkout_bytecode_in_a_real_child_process(tmp_path: Path) -> None:
    """Without a private pycache prefix, a checked-out pyc could replace reviewed source."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    spec = build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    source = tmp_path / "reviewed-source"
    source.mkdir()
    module = source / "victim.py"
    module.write_text("VALUE = 'EVIL'\n", encoding="utf-8")
    py_compile.compile(module, doraise=True)
    original = module.stat()
    module.write_text("VALUE = 'SAFE'\n", encoding="utf-8")
    os.utime(module, ns=(original.st_atime_ns, original.st_mtime_ns))
    code_index = spec.argv.index("-c")
    probe = (
        *spec.argv[:code_index],
        "-c",
        "import importlib,sys; sys.path[:0]=[sys.argv[1]]; print(importlib.import_module('victim').VALUE)",
        str(source),
    )

    result = subprocess.run(probe, check=True, capture_output=True, text=True, env=dict(spec.env))

    assert result.stdout == "SAFE\n"


@pytest.mark.parametrize("tool_id", ["expression-studio", "sprite-animation-studio"])
def test_visual_studios_have_fixed_import_mode_and_canonical_evidence_paths(tmp_path: Path, tool_id: str) -> None:
    """A caller must not turn a Hub launch into a paid engine or choose evidence paths."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == tool_id)
    project = _project(tmp_path)

    spec = build_launch_spec(tool, project, _context(tmp_path))

    assert spec.argv[spec.argv.index("--run-mode") + 1] == "subscription_handoff_import"
    assert spec.argv[spec.argv.index("--figma-target-registry") + 1] == str(
        BASE_ROOT / "docs" / "operations" / "PROJECT_FIGMA_TARGET_REGISTRY.json"
    )
    assert spec.argv[spec.argv.index("--approved-anchor-registry") + 1] == str(
        project.root / "docs" / "APPROVED_VISUAL_ANCHORS.json"
    )
    assert "--output-root" not in spec.argv
    assert "--flag" not in spec.argv
    assert "sh -c" not in spec.argv
    # The hostile project path remains one literal argv element; it is never parsed by a shell.
    assert str(project.root) in spec.argv
    assert "OPENAI_API_KEY" not in spec.env
    assert "CODEX_HOME" not in spec.env


def test_rejects_interpreter_outside_the_reviewed_venv(tmp_path: Path) -> None:
    """Using a caller interpreter could import arbitrary sitecustomize or packages."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    context = LaunchContext(BASE_ROOT, tmp_path / "runtime", Path("/usr/bin/python3"), "n" * 43)

    with pytest.raises(AdapterError, match="interpreter"):
        build_launch_spec(tool, _project(tmp_path), context)


def test_rejects_interpreter_bytes_that_no_longer_match_the_startup_pin(tmp_path: Path) -> None:
    tool = dict(
        next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    )
    tool["_interpreter_sha256"] = "0" * 64

    with pytest.raises(AdapterError, match="interpreter"):
        build_launch_spec(tool, _project(tmp_path), _context(tmp_path))


def test_rejects_reviewed_source_changed_after_registry_load(tmp_path: Path) -> None:
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    source = BASE_ROOT / "tools" / "expression-studio" / "src" / "expression_studio" / "__init__.py"
    original = source.read_bytes()
    try:
        source.write_bytes(original + b"\n# launch-time drift\n")
        with pytest.raises(AdapterError, match="source"):
            build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    finally:
        source.write_bytes(original)


def test_registry_validator_is_verified_before_its_module_code_executes(tmp_path: Path) -> None:
    validator = BASE_ROOT / "tools" / "validate_tool_registry.py"
    marker = tmp_path / "validator-executed"
    original = validator.read_bytes()
    try:
        validator.write_bytes(
            original
            + f"\nfrom pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n".encode()
        )
        with pytest.raises(HubRegistryError, match="registry"):
            load_reviewed_tools(BASE_ROOT)
        assert not marker.exists()
    finally:
        validator.write_bytes(original)


def test_rejects_untracked_directory_link_added_to_reviewed_source_after_pinning(
    tmp_path: Path,
) -> None:
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    outside = tmp_path / "outside-source"
    outside.mkdir()
    link = BASE_ROOT / "tools" / "expression-studio" / "src" / "shadow_package"
    link.symlink_to(outside, target_is_directory=True)
    try:
        with pytest.raises(AdapterError, match="source"):
            build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    finally:
        link.unlink()


def test_rejects_directory_link_added_to_python_environment_after_pinning(tmp_path: Path) -> None:
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    outside = tmp_path / "outside-package"
    outside.mkdir()
    site_packages = BASE_ROOT / ".venv" / "lib" / "python3.12" / "site-packages"
    link = site_packages / "shadow_package"
    link.symlink_to(outside, target_is_directory=True)
    try:
        with pytest.raises(AdapterError, match="environment"):
            build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    finally:
        link.unlink()


def test_rejects_a_symlink_replacement_of_the_reviewed_owner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Replacing a Studio owner path must not change the launched module's source tree."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    hostile_base = tmp_path / "base"
    (hostile_base / "tools").mkdir(parents=True)
    (tmp_path / "outside").mkdir()
    (hostile_base / "tools" / "expression-studio").symlink_to(tmp_path / "outside", target_is_directory=True)
    (hostile_base / ".venv" / "bin").mkdir(parents=True)
    interpreter = hostile_base / ".venv" / "bin" / "python"
    interpreter.write_text("#!/bin/sh\n", encoding="utf-8")
    context = LaunchContext(hostile_base, tmp_path / "runtime", interpreter, "n" * 43)

    with pytest.raises(AdapterError, match="owner"):
        build_launch_spec(tool, _project(tmp_path), context)


def test_rejects_a_symlinked_nested_studio_source_root(tmp_path: Path) -> None:
    """A fixed owner directory must not import a module through a replaced nested source root."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    hostile_base = tmp_path / "base"
    (hostile_base / "tools" / "expression-studio").mkdir(parents=True)
    (hostile_base / "tools" / "base-tool-contracts" / "src").mkdir(parents=True)
    outside = tmp_path / "outside-source"
    outside.mkdir()
    (hostile_base / "tools" / "expression-studio" / "src").symlink_to(outside, target_is_directory=True)
    (hostile_base / ".venv" / "bin").mkdir(parents=True)
    (hostile_base / ".venv" / "bin" / "python").symlink_to(BASE_ROOT / ".venv" / "bin" / "python")
    context = LaunchContext(
        hostile_base,
        tmp_path / "runtime",
        hostile_base / ".venv" / "bin" / "python",
        "n" * 43,
    )

    with pytest.raises(AdapterError, match="source"):
        build_launch_spec(tool, _project(tmp_path), context)


def test_rejects_cross_wired_registry_data(tmp_path: Path) -> None:
    """A reviewed adapter label alone cannot select a different module owner."""
    tool = dict(next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio"))
    tool["launch_adapter"] = "sprite_animation_studio"

    with pytest.raises(AdapterError, match="fixed reviewed tuple"):
        build_launch_spec(tool, _project(tmp_path), _context(tmp_path))


def test_rejects_existing_or_replaced_startup_path(tmp_path: Path) -> None:
    """A child must exclusively create its own authenticated startup report."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    context = _context(tmp_path)
    context.runtime_root.mkdir()
    (context.runtime_root / "expression-studio-demo-game.json").write_text("attacker", encoding="utf-8")

    with pytest.raises(AdapterError, match="startup"):
        build_launch_spec(tool, _project(tmp_path), context)


def test_rejects_untracked_checkout_bytecode_under_a_reviewed_studio_owner(tmp_path: Path) -> None:
    """Unchecked .pyc files could run before the Studio's reviewed source code."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    bytecode = BASE_ROOT / "tools" / "expression-studio" / "src" / "expression_studio" / "__pycache__"
    created = not bytecode.exists()
    bytecode.mkdir(exist_ok=True)
    malicious = bytecode / "checkout_payload.pyc"
    malicious.write_bytes(b"not trusted")
    try:
        with pytest.raises(AdapterError, match="bytecode"):
            build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    finally:
        malicious.unlink(missing_ok=True)
        if created:
            bytecode.rmdir()


def test_rejects_a_symlinked_runtime_directory_before_selecting_startup_path(tmp_path: Path) -> None:
    """The startup report parent must remain Hub-owned and component-safe."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    outside = tmp_path / "outside"
    outside.mkdir()
    runtime = tmp_path / "runtime"
    runtime.symlink_to(outside, target_is_directory=True)
    context = LaunchContext(BASE_ROOT, runtime, BASE_ROOT / ".venv" / "bin" / "python", "n" * 43)

    with pytest.raises(AdapterError, match="runtime"):
        build_launch_spec(tool, _project(tmp_path), context)


def test_launch_argv_prevents_pth_and_sitecustomize_before_fixed_bootstrap(tmp_path: Path) -> None:
    """Without -S, installed .pth and sitecustomize execute before the reviewed bootstrap."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    spec = build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    marker = tmp_path / "pre-bootstrap-ran"
    site_packages = Path(site.getsitepackages()[0])
    pth = site_packages / "task3-pre-bootstrap.pth"
    custom = site_packages / "sitecustomize.py"
    assert not pth.exists()
    assert not custom.exists()
    pth.write_text(f"import pathlib; pathlib.Path({str(marker)!r}).write_text('pth')\n", encoding="utf-8")
    custom.write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).open('a').write('sitecustomize')\n",
        encoding="utf-8",
    )
    code_index = spec.argv.index("-c")
    probe = (*spec.argv[:code_index], "-c", "print('fixed bootstrap')")
    try:
        subprocess.run(probe, check=True, capture_output=True, text=True, env=dict(spec.env))

        assert not marker.exists()
    finally:
        pth.unlink(missing_ok=True)
        custom.unlink(missing_ok=True)


def test_site_disabled_bootstrap_still_imports_reviewed_studio_and_contract_dependencies(tmp_path: Path) -> None:
    """The pre-site boundary must retain only the explicitly injected reviewed dependencies."""
    tool = next(item for item in load_reviewed_tools(BASE_ROOT) if item["tool_id"] == "expression-studio")
    spec = build_launch_spec(tool, _project(tmp_path), _context(tmp_path))
    code_index = spec.argv.index("-c")
    contract_source, owner_source, site_packages = spec.argv[code_index + 2 : code_index + 5]
    probe = (
        *spec.argv[:code_index],
        "-c",
        "import sys; contract,owner,packages=sys.argv[1:]; sys.path[:0]=[contract,owner,packages]; import base_tool_contracts, expression_studio.app; print('reviewed imports ready')",
        contract_source,
        owner_source,
        site_packages,
    )

    result = subprocess.run(probe, check=True, capture_output=True, text=True, env=dict(spec.env))

    assert result.stdout == "reviewed imports ready\n"
