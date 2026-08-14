from __future__ import annotations

import json
import os
from pathlib import Path
import signal
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from tool_hub.adapters import LaunchSpec
from tool_hub.projects import ProjectBinding
import tool_hub.supervisor as supervisor_module
from tool_hub.supervisor import LaunchError, ProcessSupervisor


CHILD = r"""
import json, os, signal, subprocess, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

startup, tool_id, project_id, nonce, adapter, fingerprint, mode, project_root = sys.argv[1:]
if mode == "crash":
    raise SystemExit(17)
if mode == "noisy-crash":
    print((startup + nonce) * 300 + " controlled-log-marker " + project_root + "/Private File With Spaces.txt", file=sys.stderr)
    raise SystemExit(18)
if mode == "delayed-output-crash":
    time.sleep(0.3)
    print("must-stay-on-validated-fd", file=sys.stderr, flush=True)
    raise SystemExit(19)
if mode == "timeout":
    time.sleep(30)
    raise SystemExit(0)
if mode == "delayed":
    time.sleep(0.3)
identity = {
    "tool_id": tool_id,
    "project_id": project_id,
    "process_id": os.getpid(),
    "launch_nonce": nonce,
    "adapter_sha256": adapter,
    "root_fingerprint": fingerprint,
}
if mode == "wrong-nonce": identity["launch_nonce"] = "x" * 43
if mode == "wrong-pid": identity["process_id"] = os.getpid() + 1000
if mode == "wrong-hash": identity["adapter_sha256"] = "f" * 64

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {**identity, "status": "ready"}
        if os.path.exists(startup + ".wrong"):
            payload["launch_nonce"] = "z" * 43
        if os.path.exists(startup + ".unready"):
            payload["status"] = "failed"
        encoded = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
identity["port"] = server.server_address[1]
if mode == "ignore-term":
    def ignore_term(signum, frame):
        with open(os.path.join(project_root, "term-marker"), "w", encoding="utf-8") as marker:
            marker.write("TERM")
    signal.signal(signal.SIGTERM, ignore_term)
if mode == "descendant":
    descendant = subprocess.Popen([sys.executable, "-I", "-c", "import time; time.sleep(30)"])
    with open(startup + ".descendant", "w", encoding="utf-8") as stream:
        stream.write(str(descendant.pid))
if mode == "symlink-startup":
    outside = startup + ".outside"
    with open(outside, "x", encoding="utf-8") as stream:
        json.dump(identity, stream)
    os.symlink(outside, startup)
    server.serve_forever()
if mode == "linked-startup":
    temporary = startup + ".temporary"
    with open(temporary, "x", encoding="utf-8") as stream:
        json.dump(identity, stream)
    os.link(temporary, startup)
    time.sleep(0.2)
    os.unlink(temporary)
    server.serve_forever()
with open(startup, "x", encoding="utf-8") as stream:
    json.dump(identity, stream)
server.serve_forever()
"""


class BindingLocator:
    def __init__(self, root: Path) -> None:
        self.root = root

    def resolve(self, project_id: str) -> ProjectBinding:
        return ProjectBinding(
            project_id,
            self.root,
            f"owner/{project_id}",
            "Godot 4.7",
            "a" * 64,
            "b" * 64,
        )

    def preflight_visual(self, project_id, figma_registry, anchor_registry) -> ProjectBinding:
        return self.resolve(project_id)


class ChildSpecs:
    def __init__(self) -> None:
        self.modes: dict[tuple[str, str], str] = {}
        self.calls: list[tuple[str, str]] = []

    def __call__(self, tool, project, context) -> LaunchSpec:
        tool_id = str(tool["tool_id"])
        self.calls.append((tool_id, project.project_id))
        startup = context.runtime_root / "startup.json"
        expected = {
            "tool_id": tool_id,
            "project_id": project.project_id,
            "launch_nonce": context.launch_nonce,
            "adapter_sha256": project.adapter_sha256,
            "root_fingerprint": project.fingerprint,
        }
        argv = (
            sys.executable,
            "-I",
            "-c",
            CHILD,
            str(startup),
            tool_id,
            project.project_id,
            context.launch_nonce,
            project.adapter_sha256,
            project.fingerprint,
            self.modes.get((tool_id, project.project_id), "healthy"),
            str(project.root),
        )
        return LaunchSpec(argv, context.runtime_root, {}, startup, expected)


TOOLS = tuple(
    {
        "tool_id": tool_id,
        "health_path": "/api/status",
        "owner_path": "unused",
        "launch_adapter": "unused",
        "capabilities": [],
    }
    for tool_id in ("qa-evidence-studio", "expression-studio", "sprite-animation-studio")
)


def supervisor(tmp_path: Path, specs: ChildSpecs, **kwargs) -> ProcessSupervisor:
    project_root = kwargs.get("project_root", tmp_path)
    return ProcessSupervisor(
        kwargs.get("runtime_root", tmp_path / "runtime"),
        tmp_path,
        BindingLocator(tmp_path),
        TOOLS,
        machine_lock_root=kwargs.get("machine_lock_root", tmp_path / "machine-runtime"),
        spec_builder=specs,
        spec_binder=lambda spec: spec,
        binding_resolver=lambda tool_id, project_id: BindingLocator(project_root).resolve(project_id),
        startup_timeout=kwargs.get("startup_timeout", 2.0),
        health_timeout=kwargs.get("health_timeout", 2.0),
        stop_timeout=kwargs.get("stop_timeout", 0.5),
        poll_interval=0.01,
    )


def wait_until(predicate, timeout: float = 2.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.01)
    raise AssertionError("condition did not become true before timeout")


def process_is_gone(process_id: int) -> bool:
    try:
        stat_value = Path(f"/proc/{process_id}/stat").read_text(encoding="utf-8")
    except FileNotFoundError:
        return True
    return stat_value.split()[2] == "Z"


def test_same_key_is_idempotent_and_four_keys_have_independent_processes(tmp_path: Path) -> None:
    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    try:
        first = owner.start("expression-studio", "left-game")
        repeated = owner.start("expression-studio", "left-game")
        children = [
            first,
            owner.start("sprite-animation-studio", "left-game"),
            owner.start("expression-studio", "right-game"),
            owner.start("sprite-animation-studio", "right-game"),
        ]

        assert repeated.process_id == first.process_id
        assert len({child.process_id for child in children}) == 4
        assert len({child.port for child in children}) == 4
        assert specs.calls.count(("expression-studio", "left-game")) == 1
        assert {child.public_view()["status"] for child in children} == {"RUNNING"}
    finally:
        owner.stop_all()


def test_concurrent_same_key_start_creates_one_child(tmp_path: Path) -> None:
    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    try:
        with ThreadPoolExecutor(max_workers=8) as pool:
            children = list(
                pool.map(
                    lambda _: owner.start("expression-studio", "demo-game"),
                    range(8),
                )
            )

        assert len({child.process_id for child in children}) == 1
        assert specs.calls == [("expression-studio", "demo-game")]
    finally:
        owner.stop_all()


def test_stop_all_waits_for_a_different_key_start_and_closes_the_supervisor(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "slow-game")] = "delayed"
    owner = supervisor(tmp_path, specs)
    with ThreadPoolExecutor(max_workers=2) as pool:
        future = pool.submit(owner.start, "expression-studio", "slow-game")
        wait_until(lambda: owner.view("expression-studio", "slow-game").status == "STARTING")
        try:
            owner.stop_all()
            child = future.result(timeout=2)

            wait_until(lambda: process_is_gone(child.process_id))
            assert owner.view("expression-studio", "slow-game").status == "STOPPED"
            with pytest.raises(LaunchError, match="closing"):
                owner.start("sprite-animation-studio", "other-game")
        finally:
            if not future.done():
                future.cancel()
            try:
                owner.stop_all()
            except LaunchError:
                pass


def test_idempotent_start_rechecks_ready_health_state(tmp_path: Path) -> None:
    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    try:
        owner.start("expression-studio", "demo-game")
        startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
        marker = Path(str(startup) + ".unready")
        marker.touch()

        with pytest.raises(LaunchError, match="unhealthy"):
            owner.start("expression-studio", "demo-game")
        assert owner.view("expression-studio", "demo-game").status == "UNHEALTHY"
        marker.unlink()
    finally:
        owner.stop_all()


@pytest.mark.parametrize("mode", ["wrong-nonce", "wrong-pid", "wrong-hash"])
def test_start_rejects_a_child_with_wrong_authenticated_identity(tmp_path: Path, mode: str) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = mode
    owner = supervisor(tmp_path, specs)
    try:
        with pytest.raises(LaunchError, match="startup identity"):
            owner.start("expression-studio", "demo-game")
        assert owner.view("expression-studio", "demo-game").status == "START_FAILED"
    finally:
        owner.stop_all()


def test_stale_startup_file_blocks_before_child_creation(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "timeout"
    owner = supervisor(tmp_path, specs, startup_timeout=0.2)
    original = specs.__call__

    def stale_spec(tool, project, context):
        spec = original(tool, project, context)
        spec.startup_file.write_text('{"port": 1234}', encoding="utf-8")
        return spec

    owner.spec_builder = stale_spec
    try:
        with pytest.raises(LaunchError, match="startup report path"):
            owner.start("expression-studio", "demo-game")
        assert owner.started_process_count == 0
    finally:
        owner.stop_all()


def test_startup_identity_read_rejects_a_child_published_symlink(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "symlink-startup"
    owner = supervisor(tmp_path, specs)
    try:
        with pytest.raises(LaunchError, match="startup identity"):
            owner.start("expression-studio", "demo-game")
    finally:
        owner.stop_all()


def test_startup_identity_waits_for_atomic_hardlink_publication(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "linked-startup"
    owner = supervisor(tmp_path, specs)
    try:
        child = owner.start("expression-studio", "demo-game")

        assert child.state == "RUNNING"
    finally:
        owner.stop_all()


@pytest.mark.parametrize(
    ("mode", "message"),
    [("crash", "exited before startup"), ("timeout", "startup identity timeout")],
)
def test_start_failure_is_bounded_and_does_not_leave_a_child(
    tmp_path: Path, mode: str, message: str
) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = mode
    owner = supervisor(tmp_path, specs, startup_timeout=0.2)
    started = time.monotonic()
    try:
        with pytest.raises(LaunchError, match=message):
            owner.start("expression-studio", "demo-game")
        assert time.monotonic() - started < 2
        assert owner.view("expression-studio", "demo-game").status == "START_FAILED"
    finally:
        owner.stop_all()


def test_failure_log_tail_is_bounded_and_sanitized(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "noisy-crash"
    owner = supervisor(tmp_path, specs)
    try:
        with pytest.raises(LaunchError) as caught:
            owner.start("expression-studio", "demo-game")

        assert len(str(caught.value)) <= 1400
        assert str(tmp_path) not in str(caught.value)
    finally:
        owner.stop_all()


def test_failure_log_redacts_bound_project_root_and_whitespace_path(tmp_path: Path) -> None:
    project_root = tmp_path / "Bound Project Root With Spaces"
    project_root.mkdir()
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "noisy-crash"
    owner = supervisor(tmp_path, specs, project_root=project_root)
    try:
        with pytest.raises(LaunchError) as caught:
            owner.start("expression-studio", "demo-game")

        public_error = str(caught.value)
        assert str(project_root) not in public_error
        assert "Bound Project Root With Spaces" not in public_error
        assert "Private File With Spaces.txt" not in public_error
    finally:
        owner.stop_all()


def test_failed_launch_removes_private_launch_directory_after_tail_capture(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "noisy-crash"
    owner = supervisor(tmp_path, specs)
    try:
        with pytest.raises(LaunchError) as caught:
            owner.start("expression-studio", "demo-game")

        assert str(caught.value)
        assert owner.view("expression-studio", "demo-game").log_tail
        assert list((tmp_path / "runtime").glob("launch-*")) == []
    finally:
        owner.stop_all()


def test_log_drain_does_not_follow_replaced_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "delayed-output-crash"
    owner = supervisor(tmp_path, specs)
    outside = tmp_path / "outside.log"
    outside.write_text("SAFE", encoding="utf-8")
    reopen_waiting = threading.Event()
    release_reopen = threading.Event()
    original_open = Path.open

    def controlled_open(path: Path, mode: str = "r", *args, **kwargs):
        if path.name == "child.log" and mode == "r+b":
            reopen_waiting.set()
            release_reopen.wait(timeout=2)
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", controlled_open)
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(owner.start, "expression-studio", "demo-game")
        try:
            wait_until(lambda: any((tmp_path / "runtime").glob("launch-*/child.log")))
            reopen_waiting.wait(timeout=0.2)
            log_path = next((tmp_path / "runtime").glob("launch-*/child.log"))
            log_path.unlink()
            log_path.symlink_to(outside)
            release_reopen.set()
            with pytest.raises(LaunchError):
                future.result(timeout=2)

            assert outside.read_text(encoding="utf-8") == "SAFE"
        finally:
            release_reopen.set()
            try:
                owner.stop_all()
            except LaunchError:
                pass


def test_child_crash_changes_public_state_to_unhealthy(tmp_path: Path) -> None:
    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    try:
        child = owner.start("expression-studio", "demo-game")
        os.kill(child.process_id, signal.SIGKILL)
        os.waitpid(child.process_id, 0)

        assert owner.view("expression-studio", "demo-game").status == "UNHEALTHY"
    finally:
        owner.stop_all()


def test_stop_requires_current_authenticated_ownership(tmp_path: Path) -> None:
    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    try:
        child = owner.start("expression-studio", "demo-game")
        startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
        Path(str(startup) + ".wrong").touch()

        with pytest.raises(LaunchError, match="ownership"):
            owner.stop("expression-studio", "demo-game")
        assert os.kill(child.process_id, 0) is None
        Path(str(startup) + ".wrong").unlink()
    finally:
        owner.stop_all()


def test_machine_lock_prevents_a_second_supervisor_from_starting(tmp_path: Path) -> None:
    left_specs = ChildSpecs()
    right_specs = ChildSpecs()
    left = supervisor(tmp_path, left_specs)
    right = supervisor(tmp_path, right_specs)
    try:
        left.start("expression-studio", "left-game")

        with pytest.raises(LaunchError, match="machine ownership"):
            right.start("expression-studio", "right-game")
        assert right.started_process_count == 0
    finally:
        left.stop_all()
        right.stop_all()


def test_machine_lock_is_shared_across_distinct_project_config_runtimes(tmp_path: Path) -> None:
    shared_machine_root = tmp_path / "machine-runtime"
    left = supervisor(
        tmp_path / "left-config",
        ChildSpecs(),
        runtime_root=tmp_path / "left-runtime",
        machine_lock_root=shared_machine_root,
    )
    right = supervisor(
        tmp_path / "right-config",
        ChildSpecs(),
        runtime_root=tmp_path / "right-runtime",
        machine_lock_root=shared_machine_root,
    )
    try:
        left.start("expression-studio", "left-game")

        with pytest.raises(LaunchError, match="machine ownership"):
            right.start("expression-studio", "right-game")
        assert right.started_process_count == 0
    finally:
        left.stop_all()
        right.stop_all()


def test_default_machine_lock_address_is_not_scoped_by_os_user(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(os, "geteuid", lambda: 1001)
    left = supervisor_module.default_machine_lock_address()
    monkeypatch.setattr(os, "geteuid", lambda: 2002)
    right = supervisor_module.default_machine_lock_address()

    assert left == right
    assert left == ("127.0.0.1", 47640)


def test_stop_all_surfaces_failed_ownership_and_retains_machine_lock(tmp_path: Path) -> None:
    left = supervisor(tmp_path, ChildSpecs())
    right = supervisor(tmp_path, ChildSpecs())
    child = left.start("expression-studio", "left-game")
    startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
    marker = Path(str(startup) + ".wrong")
    marker.touch()
    try:
        with pytest.raises(LaunchError, match="could not stop all"):
            left.stop_all()
        with pytest.raises(LaunchError, match="machine ownership"):
            right.start("expression-studio", "right-game")
        assert os.kill(child.process_id, 0) is None
    finally:
        marker.unlink()
        left.stop_all()
        right.stop_all()


def test_stop_terminates_process_group_descendant_and_releases_machine_lock(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "left-game")] = "descendant"
    left = supervisor(tmp_path, specs)
    right = supervisor(tmp_path, ChildSpecs())
    try:
        child = left.start("expression-studio", "left-game")
        startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
        descendant_id = int(Path(str(startup) + ".descendant").read_text(encoding="utf-8"))

        assert left.stop("expression-studio", "left-game").status == "STOPPED"
        left.stop_all()
        wait_until(lambda: process_is_gone(child.process_id))
        wait_until(lambda: process_is_gone(descendant_id))
        replacement = right.start("expression-studio", "right-game")
        assert replacement.public_view()["status"] == "RUNNING"
    finally:
        left.stop_all()
        right.stop_all()


def test_stop_terminates_descendant_after_the_group_leader_crashes(tmp_path: Path) -> None:
    specs = ChildSpecs()
    specs.modes[("expression-studio", "left-game")] = "descendant"
    owner = supervisor(tmp_path, specs)
    try:
        child = owner.start("expression-studio", "left-game")
        startup = next((tmp_path / "runtime").glob("launch-*/startup.json"))
        descendant_id = int(Path(str(startup) + ".descendant").read_text(encoding="utf-8"))
        os.kill(child.process_id, signal.SIGKILL)
        wait_until(lambda: process_is_gone(child.process_id))
        wait_until(lambda: owner.view("expression-studio", "left-game").status == "UNHEALTHY")

        assert owner.stop("expression-studio", "left-game").status == "UNHEALTHY"
        wait_until(lambda: process_is_gone(descendant_id))
    finally:
        owner.stop_all()


def test_stop_escalates_from_term_to_kill_for_an_uncooperative_group(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    specs = ChildSpecs()
    specs.modes[("expression-studio", "demo-game")] = "ignore-term"
    owner = supervisor(tmp_path, specs, stop_timeout=0.1, project_root=project_root)
    try:
        child = owner.start("expression-studio", "demo-game")
        assert owner.stop("expression-studio", "demo-game").status == "STOPPED"
        assert (project_root / "term-marker").is_file()
        wait_until(lambda: process_is_gone(child.process_id))
    finally:
        owner.stop_all()


def test_invalid_caller_keys_do_not_allocate_supervisor_state(tmp_path: Path) -> None:
    owner = supervisor(tmp_path, ChildSpecs())

    for index in range(100):
        with pytest.raises(LaunchError):
            owner.start(f"unregistered-tool-{index}", f"invalid-project-{index}")
    with pytest.raises(LaunchError):
        owner.start("expression-studio", "../../attacker")
    with pytest.raises(LaunchError):
        owner.stop("unregistered-tool", "demo-game")
    with pytest.raises(LaunchError):
        owner.stop("expression-studio", "../../attacker")

    assert owner._locks == {}
    assert owner._states == {}


def test_missing_valid_project_keys_have_bounded_retained_state(tmp_path: Path) -> None:
    owner = supervisor(tmp_path, ChildSpecs())

    def missing_project(tool_id: str, project_id: str) -> ProjectBinding:
        from tool_hub.projects import ProjectBindingError

        raise ProjectBindingError("registered project was not found")

    owner.binding_resolver = missing_project
    for index in range(400):
        with pytest.raises(LaunchError):
            owner.start("expression-studio", f"missing-project-{index}")

    assert owner._locks == {}
    assert len(owner._states) <= 256


def test_windows_is_blocked_before_child_creation(tmp_path: Path, monkeypatch) -> None:
    import tool_hub.supervisor as module

    specs = ChildSpecs()
    owner = supervisor(tmp_path, specs)
    monkeypatch.setattr(module, "_POSIX_PROCESS_GROUPS", False)
    try:
        with pytest.raises(LaunchError, match="Windows process ownership"):
            owner.start("expression-studio", "demo-game")
        assert owner.started_process_count == 0
        assert owner.view("expression-studio", "demo-game").status == "BLOCKED_PLATFORM"
    finally:
        owner.stop_all()
